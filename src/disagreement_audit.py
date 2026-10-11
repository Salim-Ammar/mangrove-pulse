"""Audit frozen predictions only. No downloads, refitting or threshold selection."""
from pathlib import Path
import json,zipfile,hashlib,csv,sys,traceback
from datetime import datetime,timezone
STAGE='inputs'
def dump(p,x):p.write_text(json.dumps(x,indent=2))
def run(package,out):
 global STAGE
 import numpy as np,rasterio
 from rasterio.plot import plotting_extent
 from rasterio.warp import transform
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.colors import ListedColormap,BoundaryNorm
 from matplotlib.patches import Patch
 data=out/'inputs';data.mkdir()
 required=['run_status.json','baseline_summary.json','frozen_experiment_plan.json','geographic_split.tif','inputs/previous/gmw2018_on_scl_grid.tif','inputs/previous/input_manifest.json','inputs/comparison_summary.json','ATTRIBUTION.md']
 for date in ['2018-11-20','2018-11-30']:required.append(date+'_predictions.tif')
 for prefix in ['inputs/previous/input_crops','inputs/nov30_crops']:
  required += [prefix+'/'+k+'_crop.tif' for k in ['SCL','B04','B08']]
 with zipfile.ZipFile(package) as z:
  for n in required:
   entries=[i for i in z.infolist() if i.filename==n]
   if len(entries)!=1 or entries[0].file_size>50_000_000:raise ValueError('Expected baseline-results member: '+n)
   p=data/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 if json.loads((data/'run_status.json').read_text()).get('status')!='succeeded':raise ValueError('Baseline did not succeed.')
 baseline=json.loads((data/'baseline_summary.json').read_text());plan=json.loads((data/'frozen_experiment_plan.json').read_text())
 if baseline['threshold']!=.49 or plan['gap_total_m']!=200:raise ValueError('Unexpected baseline threshold or split; review required.')
 prior=json.loads((data/'inputs/comparison_summary.json').read_text())
 oldhash=json.loads((data/'inputs/previous/input_manifest.json').read_text())['crop_sha256']
 def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 refpath=data/'inputs/previous/gmw2018_on_scl_grid.tif'
 if sha(refpath)!=prior['fixed_gmw_mask_sha256']:raise ValueError('Reference hash mismatch.')
 with rasterio.open(refpath) as ds:
  ref=ds.read(1);tx=ds.transform;crs=ds.crs;shape=ds.shape;extent=plotting_extent(ds)
 def aligned(p):
  with rasterio.open(p) as d:
   if d.crs!=crs or d.transform!=tx or d.shape!=shape:raise ValueError('Audit grids differ.')
   return d.read(1)
 split=aligned(data/'geographic_split.tif');south=split==2;inside=ref!=255;truth=ref==1
 rr,cc=np.indices(shape);xx,yy=tx*(cc+.5,rr+.5)
 expected=inside&(yy<=plan['cut_northing_m']-plan['excluded_half_gap_m'])
 if not np.array_equal(south,expected):raise ValueError('Southern split changed.')
 preds={};scls={};nir={};red={};ex10={}
 for date,prefix in [('2018-11-20','inputs/previous/input_crops'),('2018-11-30','inputs/nov30_crops')]:
  preds[date]=aligned(data/(date+'_predictions.tif'));scls[date]=aligned(data/prefix/'SCL_crop.tif')
  if not set(np.unique(preds[date])).issubset({0,1,255}):raise ValueError('Unknown prediction code.')
  for key,target in [('B08',nir),('B04',red)]:
   p=data/prefix/(key+'_crop.tif');expected_hash=oldhash[p.name] if date=='2018-11-20' else prior['new_assets'][key]['sha256']
   if sha(p)!=expected_hash:raise ValueError('Crop hash mismatch.')
   with rasterio.open(p) as d:
    if d.crs!=crs:raise ValueError('Display CRS differs.')
    target[date]=d.read(1);ex10[date]=plotting_extent(d)
  eligible=south&(preds[date]!=255);p=preds[date]==1
  counts={'tp':int((eligible&p&truth).sum()),'fp':int((eligible&p&~truth).sum()),'fn':int((eligible&~p&truth).sum()),'tn':int((eligible&~p&~truth).sum())}
  expected_counts=baseline['held_out'][date]['all_eligible_southern_cells']
  if any(counts[k]!=expected_counts[k] for k in counts):raise ValueError('Prediction counts disagree with baseline report.')
 STAGE='audit';print('Frozen predictions and split verified. Building audit only.',flush=True)
 groups={};maps={}
 names=['predicted_positive_reference_negative','predicted_negative_reference_positive','excluded_reference_positive']
 for date,p in preds.items():
  valid=p!=255
  groups[date]={names[0]:south&valid&(p==1)&~truth,names[1]:south&valid&(p==0)&truth,names[2]:south&~valid&truth}
  a=np.full(shape,np.nan);a[south]=0;a[groups[date][names[0]]]=1;a[groups[date][names[1]]]=2;a[groups[date][names[2]]]=3;a[south&~valid&~truth]=4;maps[date]=a
 # One-cell adjacency to a reference label transition, not measured positional error.
 boundary=np.zeros(shape,bool)
 pad=np.pad(ref,1,constant_values=255)
 for i in range(3):
  for j in range(3):
   neighbour=pad[i:i+shape[0],j:j+shape[1]]
   boundary |= inside&(neighbour!=255)&(neighbour!=ref)
 summary={}
 for date,g in groups.items():
  summary[date]={}
  for name,m in g.items():
   n=int(m.sum());near=int((m&boundary).sum())
   summary[date][name]={'centres':n,'adjacent_to_reference_transition':near,'not_adjacent':n-near,
      'scl_counts':{str(i):int((m&(scls[date]==i)).sum()) for i in range(12)}}
 components=[];cell_rows=[];selected={};counter=0
 def connected(m):
  unseen=set(map(tuple,np.argwhere(m)));parts=[]
  while unseen:
   start=min(unseen);unseen.remove(start);stack=[start];part=[]
   while stack:
    r,c=stack.pop();part.append((r,c))
    for dr in [-1,0,1]:
     for dc in [-1,0,1]:
      q=(r+dr,c+dc)
      if q in unseen:unseen.remove(q);stack.append(q)
   parts.append(sorted(part))
  return sorted(parts,key=lambda p:(-len(p),p[0]))
 for name in names:
  parts=connected(groups['2018-11-20'][name]);selected[name]=[]
  for rank,part in enumerate(parts,1):
   counter+=1;cid=f'C{counter:03d}';rs=np.array([p[0] for p in part]);cs=np.array([p[1] for p in part])
   m=np.zeros(shape,bool);m[rs,cs]=True
   row={'cluster_id':cid,'category':name,'rank_within_category':rank,'centres':len(part),
        'adjacent_to_reference_transition':int(boundary[rs,cs].sum()),
        'same_category_nov30':int(groups['2018-11-30'][name][rs,cs].sum()),
        'excluded_nov30':int((preds['2018-11-30'][rs,cs]==255).sum()),
        'x_min':float(xx[rs,cs].min()-10),'y_min':float(yy[rs,cs].min()-10),'x_max':float(xx[rs,cs].max()+10),'y_max':float(yy[rs,cs].max()+10),
        'review_note':'','cause':'unverified'}
   components.append(row)
   if rank<=2:selected[name].append((row,m))
   lon,lat=transform(crs,'EPSG:4326',xx[rs,cs].tolist(),yy[rs,cs].tolist())
   for idx,(r,c) in enumerate(part):
    p30=int(preds['2018-11-30'][r,c]);status30='excluded' if p30==255 else ('agrees_with_reference' if p30==int(truth[r,c]) else 'disagrees_with_reference')
    cell_rows.append({'cluster_id':cid,'category_nov20':name,'row':int(r),'column':int(c),'longitude':lon[idx],'latitude':lat[idx],
       'gmw':int(ref[r,c]),'prediction_nov20':int(preds['2018-11-20'][r,c]),'prediction_nov30':p30,'status_nov30':status30,
       'scl_nov20':int(scls['2018-11-20'][r,c]),'scl_nov30':int(scls['2018-11-30'][r,c]),'adjacent_to_reference_transition':bool(boundary[r,c]),
       'review_note':'','cause':'unverified'})
 def writecsv(name,rows):
  with (out/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 if components:writecsv('all_clusters.csv',components)
 if cell_rows:writecsv('all_audit_cells.csv',cell_rows)
 dump(out/'audit_summary.json',{'threshold_unchanged':.49,'split_unchanged':True,'category_counts':summary,
   'nov20_cluster_count':len(components),'contact_sheet_rule':'Two largest 8-connected clusters per category; ties sorted by row/column. All clusters/cells remain in CSV.',
   'boundary_definition':'Any of 8 neighbouring 20 m cells has a different 0/1 GMW value. Outside-AOI cells ignored. Not a physical-distance accuracy estimate.',
   'limitations':['No model refit, new scores, shifted map, changed mask or new imagery.',
     'Reference disagreements are not established classification errors.',
     'An edge-adjacent disagreement does not identify its cause or prove the reference/model wrong.',
     'Two dates from the same sensor and the same reference are not independent validation.',
     'Blank review fields are intentional: visual review and independent evidence are still needed.',
     'Held-out results are now inspected; any later model revision needs fresh evaluation or an explicit post-hoc label.']})
 STAGE='figures'
 colors=['#eeeeee','#cf2877','#2879ca','#e89d26','#666666'];labels=['Agreement','Pred+ / GMW−','Pred− / GMW+','Excluded GMW+','Other excluded']
 fig,axes=plt.subplots(1,2,figsize=(11,7),layout='constrained')
 for ax,date in zip(axes,preds):
  ax.imshow(maps[date],extent=extent,cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(-.5,5),5),interpolation='nearest');ax.set_title(date+' | southern audit')
  ax.set_ylim(extent[2],plan['cut_northing_m']-100);ax.set_aspect('equal');ax.tick_params(labelsize=7)
 fig.legend(handles=[Patch(color=c,label=l) for c,l in zip(colors,labels)],loc='outside lower center',ncol=3,fontsize=8)
 fig.suptitle('Frozen baseline: reference disagreements and excluded areas\nColours do not establish which source is correct',fontsize=12)
 fig.savefig(out/'audit_overview.png',dpi=160,bbox_inches='tight');plt.close(fig)
 # Same global NIR display range across dates; no calibrated-reflectance inference.
 vals=np.concatenate([a[a>0] for a in nir.values()]);lo,hi=np.percentile(vals,[2,98])
 for group,examples in selected.items():
  if not examples:continue
  fig,axes=plt.subplots(len(examples),2,figsize=(10,5*len(examples)),squeeze=False,layout='constrained')
  for row,(info,m) in enumerate(examples):
   for col,date in enumerate(preds):
    ax=axes[row,col];ax.imshow(nir[date],extent=ex10[date],cmap='gray',vmin=lo,vmax=hi,interpolation='nearest')
    ax.contour(xx[0,:],yy[:,0],truth.astype(int),levels=[.5],colors=['#ffaf30'],linewidths=.9)
    rs,cs=np.where(m);ax.scatter(xx[rs,cs],yy[rs,cs],s=22,facecolors='none',edgecolors='#00e5ff',linewidths=.8)
    ax.set_xlim(info['x_min']-60,info['x_max']+60);ax.set_ylim(info['y_min']-60,info['y_max']+60);ax.set_aspect('equal')
    ax.set_title(f"{info['cluster_id']} | {date} | {info['centres']} selected cells",fontsize=9);ax.tick_params(labelsize=7)
  fig.suptitle(group.replace('_',' ')+'\nNIR digital values: bright ≠ confirmed mangrove; orange=GMW, cyan=November 20 audit cells',fontsize=10)
  fig.savefig(out/(group+'_examples.png'),dpi=150,bbox_inches='tight');plt.close(fig)
 (out/'ATTRIBUTION.md').write_text((data/'ATTRIBUTION.md').read_text()+'\nAdditional modifications: frozen-prediction audit, connected components, cell/cluster tables and NIR inspection panels.\n')
 dump(out/'input_manifest.json',{'baseline_zip_sha256':sha(package),'extracted_file_sha256':{n:sha(data/n) for n in required}})
 print('Audit ready. Return ZIP; leave cause fields unverified until evidence review.',flush=True)
if __name__=='__main__':
 package,out=map(Path,sys.argv[1:3]);out.mkdir(parents=True,exist_ok=True)
 status={'status':'running','started_utc':datetime.now(timezone.utc).isoformat()}
 try:
  import importlib.metadata
  dump(out/'environment.json',{'python':sys.version,'packages':{p:importlib.metadata.version(p) for p in ['numpy','rasterio','matplotlib']}})
  run(package,out);status['status']='succeeded'
 except Exception as exc:
  status.update(status='failed',stage=STAGE,error=str(exc));(out/'failure.txt').write_text(traceback.format_exc());print('FAILED',STAGE,str(exc),flush=True)
 finally:
  status['finished_utc']=datetime.now(timezone.utc).isoformat();dump(out/'run_status.json',status)
 sys.exit(0 if status['status']=='succeeded' else 1)
