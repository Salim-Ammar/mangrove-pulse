"""Exploratory reference-agreement baseline. Execute in the team's Colab only."""
from pathlib import Path, PurePosixPath
import json,zipfile,hashlib,csv,sys,traceback
from datetime import datetime,timezone
STAGE='input'
def dump(p,x):p.write_text(json.dumps(x,indent=2))

def extract_required_members(archive, destination, required):
    destination = destination.resolve()
    targets = []
    total = 0
    for name in required:
        path = PurePosixPath(name)
        target = (destination / name).resolve()
        if (path.is_absolute() or '..' in path.parts or path.as_posix() != name
                or '\\' in name or ':' in name or not target.is_relative_to(destination)):
            raise ValueError('Unsafe required archive path: ' + name)
        entries = [info for info in archive.infolist() if info.filename == name]
        if len(entries) != 1 or entries[0].file_size > 50_000_000:
            raise ValueError('Wrong/incomplete comparison ZIP: ' + name)
        total += entries[0].file_size
        if total > 100_000_000:
            raise ValueError('Required archive payload exceeds 100 MB.')
        targets.append((name, target))
    for name, target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(name))

def run(input_zip,out):
 global STAGE
 import numpy as np,rasterio
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.colors import ListedColormap,BoundaryNorm
 from rasterio.plot import plotting_extent
 data=out/'inputs';data.mkdir()
 required=['run_status.json','comparison_summary.json','previous/gmw2018_on_scl_grid.tif','previous/input_crops/item_unsigned.json','previous/input_manifest.json','nov30_item_unsigned.json','ATTRIBUTION.md']
 for prefix in ['previous/input_crops','nov30_crops']:
  required += [prefix+'/'+k+'_crop.tif' for k in ['SCL','B04','B08']]
 with zipfile.ZipFile(input_zip) as z:
  extract_required_members(z,data,required)
 if json.loads((data/'run_status.json').read_text()).get('status')!='succeeded':raise ValueError('Comparison input did not succeed.')
 prior=json.loads((data/'comparison_summary.json').read_text())
 previous_hashes=json.loads((data/'previous/input_manifest.json').read_text())['crop_sha256']
 for k in ['SCL','B04','B08']:
  p=data/'previous/input_crops'/(k+'_crop.tif')
  if hashlib.sha256(p.read_bytes()).hexdigest()!=previous_hashes[p.name]:raise ValueError('Old crop hash changed.')
 if prior['old_item']!='S2B_MSIL2A_20181120T065159_R020_T40RDN_20201008T201621' or prior['new_item']!='S2B_MSIL2A_20181130T065229_R020_T40RDN_20201008T230116':raise ValueError('Unexpected scenes.')
 refpath=data/'previous/gmw2018_on_scl_grid.tif'
 if hashlib.sha256(refpath.read_bytes()).hexdigest()!=prior['fixed_gmw_mask_sha256']:raise ValueError('Reference hash changed.')
 with rasterio.open(refpath) as ds:
  ref=ds.read(1);tx=ds.transform;crs=ds.crs;extent=plotting_extent(ds);profile=ds.profile.copy()
 if crs.to_epsg()!=32640 or not np.allclose([tx.a,tx.e],[20,-20]) or tx.b or tx.d:raise ValueError('Expected north-up 20 m UTM grid.')
 inside=ref!=255;y=ref==1;shape=ref.shape
 if int(y.sum())!=1158 or int(inside.sum())!=13401:raise ValueError('Reference footprint changed.')
 rr,cc=np.indices(shape);xs,ys=tx*(cc+.5,rr+.5)
 # Geographical split fixed before reading features or optimizing any threshold.
 cut=float((ys[inside].min()+ys[inside].max())/2)
 north=inside&(ys>=cut+100);south=inside&(ys<=cut-100)
 plan={'method':'One spatial holdout; northern calibration and southern evaluation',
       'cut_northing_m':cut,'excluded_half_gap_m':100,'gap_total_m':200,
       'calibration_centres_before_quality':int(north.sum()),'evaluation_centres_before_quality':int(south.sum()),
       'feature':'(mean raw B08 - mean raw B04)/(mean raw B08 + mean raw B04), 2x2 native pixels',
       'feature_caveat':'Normalized red/NIR digital-value contrast, not asserted calibrated NDVI or a health measurement.',
       'threshold_candidates':'-1.00 through 1.00, step 0.01; predict mangrove if contrast >= threshold',
       'selection':'Maximum calibration F1 against GMW; ties choose highest threshold',
       'quality':'SCL 4,5,6 and four valid nonzero subpixels in each band; water retained',
       'minimum_each_class_per_split':50,'minimum_note':'Practical stop rule, not a statistical adequacy guarantee.',
       'primary_date':'2018-11-20, retained before fitting; November 30 is a fixed-threshold sensitivity check',
       'evaluation_rules':'No threshold retuning or split changes based on southern results.'}
 dump(out/'frozen_experiment_plan.json',plan)
 STAGE='features';features={};eligible={};scene_meta={}
 for date,prefix,meta in [('2018-11-20','previous/input_crops','previous/input_crops/item_unsigned.json'),('2018-11-30','nov30_crops','nov30_item_unsigned.json')]:
  item=json.loads((data/meta).read_text());scene_meta[date]=item['properties']
  if item['properties'].get('s2:processing_baseline')!='02.12':raise ValueError('Processing baseline changed; no automatic calibration assumptions.')
  with rasterio.open(data/prefix/'SCL_crop.tif') as d:
   if d.crs!=crs or d.shape!=shape or d.transform!=tx:raise ValueError('SCL grids differ.')
   scl=d.read(1)
  means={};valid=inside&np.isin(scl,[4,5,6])
  for key in ['B04','B08']:
   path=data/prefix/(key+'_crop.tif')
   if date=='2018-11-30' and hashlib.sha256(path.read_bytes()).hexdigest()!=prior['new_assets'][key]['sha256']:raise ValueError('New crop hash differs.')
   with rasterio.open(path) as d:
    if d.crs!=crs or not np.allclose(d.res,[10,10]) or d.transform.b or d.transform.d:raise ValueError('Expected native 10 m bands.')
    a=d.read(1);parts=[];ok=np.ones(shape,bool)
    for dx,dy in [(-5,-5),(-5,5),(5,-5),(5,5)]:
     c,r=(~d.transform)*(xs+dx,ys+dy)
     if not np.allclose(c-np.floor(c),.5,atol=1e-6,rtol=0) or not np.allclose(r-np.floor(r),.5,atol=1e-6,rtol=0):raise ValueError('10 m centres do not align with 20 m cells.')
     c=np.floor(c).astype(int);r=np.floor(r).astype(int)
     within=(c>=0)&(r>=0)&(c<d.width)&(r<d.height)
     v=np.zeros(shape,float);v[within]=a[r[within],c[within]]
     good=within&np.isfinite(v)&(v>0)
     if d.nodata is not None:good &= v!=d.nodata
     ok &= good;parts.append(v)
    means[key]=np.mean(parts,axis=0);valid &= ok
  denom=means['B08']+means['B04'];contrast=np.divide(means['B08']-means['B04'],denom,out=np.full(shape,np.nan),where=denom>0)
  valid &= np.isfinite(contrast);features[date]=contrast;eligible[date]=valid
 def counts(mask):return {'total':int(mask.sum()),'mapped_mangrove':int((mask&y).sum()),'not_mapped':int((mask&~y).sum())}
 def metrics(pred,mask):
  tp=int((pred&y&mask).sum());fp=int((pred&~y&mask).sum());fn=int((~pred&y&mask).sum());tn=int((~pred&~y&mask).sum())
  def div(a,b):return a/b if b else None
  return {'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':div(tp,tp+fp),'recall':div(tp,tp+fn),'f1':div(2*tp,2*tp+fp+fn),'iou':div(tp,tp+fp+fn),'specificity':div(tn,tn+fp),'accuracy':div(tp+tn,tp+fp+fn+tn),'note':'Agreement with GMW labels, not field accuracy'}
 train=north&eligible['2018-11-20'];test=south&eligible['2018-11-20']
 diagnostics={'north_calibration':counts(train),'south_evaluation':counts(test),
              'full_aoi_coverage':{d:{'eligible':counts(m),'excluded':counts(inside&~m)} for d,m in eligible.items()}}
 dump(out/'split_and_coverage.json',diagnostics)
 for name,m in [('calibration',train),('evaluation',test)]:
  c=counts(m)
  if min(c['mapped_mangrove'],c['not_mapped'])<50:raise ValueError(name+' has fewer than 50 centres in one reference class; stop rather than moving the split.')
 STAGE='calibration';trials=[]
 for t in np.linspace(-1,1,201):
  result=metrics(features['2018-11-20']>=t,train);trials.append({'threshold':float(t),'calibration_f1':result['f1']})
 best=max(trials,key=lambda r:(r['calibration_f1'] if r['calibration_f1'] is not None else -1,r['threshold']))
 threshold=best['threshold']
 dump(out/'frozen_threshold.json',{'threshold':threshold,'selected_using':'northern November 20 only','calibration_f1':best['calibration_f1']})
 with (out/'calibration_thresholds.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=trials[0]);w.writeheader();w.writerows(trials)
 STAGE='held-out reference agreement';results={};common=south&eligible['2018-11-20']&eligible['2018-11-30'];predictions={}
 for date in features:
  pred=features[date]>=threshold;predictions[date]=pred;m=south&eligible[date]
  results[date]={'evaluation_coverage':counts(m),'evaluation_excluded':counts(south&~eligible[date]),
                'all_eligible_southern_cells':metrics(pred,m),'same_cells_both_dates':metrics(pred,common),
                'always_not_mapped_control':metrics(np.zeros(shape,bool),m),'always_mapped_control':metrics(np.ones(shape,bool),m)}
  prof=profile.copy();prof.update(dtype='uint8',nodata=255,compress='deflate')
  with rasterio.open(out/(date+'_predictions.tif'),'w',**prof) as d:
   d.write(np.where(eligible[date],pred,255).astype('uint8'),1)
   d.update_tags(description='Exploratory GMW-agreement baseline. 0=negative,1=positive,255=excluded. See split map for held-out area.')
 split=np.full(shape,255,'uint8');split[inside]=0;split[north]=1;split[south]=2
 with rasterio.open(out/'geographic_split.tif','w',**prof) as d:d.write(split,1);d.update_tags(description='0=buffer,1=north calibration,2=south held-out,255=outside AOI')
 report={'status':'completed_exploratory_reference_agreement','threshold':threshold,'calibration':metrics(predictions['2018-11-20'],train),
         'held_out':results,'matched_evaluation_cells':counts(common),'split_and_coverage':diagnostics,
         'limitations':['Single small AOI and one spatial split; no robust regional generalization estimate.',
          '200 m gap reduces direct adjacency; it does not prove absence of spatial dependence.',
          'GMW background is not verified negative ground truth; map errors remain.',
          'Threshold fitted to GMW, so report reference agreement, not independent ecological accuracy.',
          'SCL screening can exclude relevant canopy; exclusion counts are part of the result.',
          'Feature is a raw-DN red/NIR contrast; do not interpret it as calibrated NDVI or health.',
          'Cross-date results are sensitivity checks; no second-date retuning and no stress/change claim.']}
 dump(out/'baseline_summary.json',report)
 fig,axes=plt.subplots(1,3,figsize=(13,6),layout='constrained')
 axes[0].imshow(np.ma.masked_equal(split,255),extent=extent,cmap=ListedColormap(['#cccccc','#3182bd','#e6550d']),norm=BoundaryNorm([-.5,.5,1.5,2.5],3),interpolation='nearest')
 axes[0].set_title('Blue: calibration north\nOrange: evaluation south; grey: gap',fontsize=10)
 for ax,(date,pred) in zip(axes[1:],predictions.items()):
  ax.imshow(np.ma.array(pred,mask=~eligible[date]),extent=extent,cmap=ListedColormap(['#e6e6e6','#22964b']),vmin=0,vmax=1,interpolation='nearest')
  ax.contour(xs[0,:],ys[:,0],y.astype(int),levels=[.5],colors=['#ff9900'],linewidths=.6)
  ax.set_title(date+'\nGreen: prediction; orange: GMW boundary',fontsize=10)
 for ax in axes:
  ax.axhline(cut+100,color='black',ls='--',lw=.8);ax.axhline(cut-100,color='black',ls='--',lw=.8);ax.set_aspect('equal');ax.tick_params(labelsize=7)
 fig.suptitle('Exploratory reference-agreement baseline — not health or validated extent',fontsize=12)
 fig.savefig(out/'baseline_inspection.png',dpi=160,bbox_inches='tight');plt.close(fig)
 (out/'ATTRIBUTION.md').write_text((data/'ATTRIBUTION.md').read_text()+'\nAdditional modifications: 2x2 mean red/NIR contrast, fixed geographic split, threshold predictions and GMW agreement statistics.\n')
 print('Baseline complete. Return ZIP before changing thresholds, masks or geography.',flush=True)
if __name__=='__main__':
 input_zip,out=map(Path,sys.argv[1:3]);out.mkdir(parents=True,exist_ok=True)
 status={'status':'running','started_utc':datetime.now(timezone.utc).isoformat()}
 try:
  import importlib.metadata
  dump(out/'environment.json',{'python':sys.version,'packages':{k:importlib.metadata.version(k) for k in ['numpy','rasterio','matplotlib']}})
  run(input_zip,out);status['status']='succeeded'
 except Exception as exc:
  status.update(status='failed',stage=STAGE,error=str(exc));(out/'failure.txt').write_text(traceback.format_exc());print('FAILED:',STAGE,str(exc),flush=True)
 finally:
  status['finished_utc']=datetime.now(timezone.utc).isoformat();dump(out/'run_status.json',status)
 sys.exit(0 if status['status']=='succeeded' else 1)
