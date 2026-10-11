"""Reproduce the frozen cached-data workflow; execute only in the team's Colab.

The inspection brief and drone roadmap are documentation outputs. This runner
checks reference agreement, not field accuracy, ecological condition or drone
capability. Its execution logic is unchanged from the verified cached run.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math, subprocess, sys, traceback, zipfile
from datetime import datetime, timezone

def read(p): return json.loads(p.read_text())
def dump(p, obj): p.write_text(json.dumps(obj, indent=2) + '\n')
def compare(a, b, where='value'):
    if isinstance(a, dict):
        if not isinstance(b, dict) or set(a) != set(b): raise ValueError(where + ': keys differ')
        for k in a: compare(a[k], b[k], where + '.' + k)
    elif isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b): raise ValueError(where + ': length differs')
        for i, (x,y) in enumerate(zip(a,b)): compare(x,y,where+f'[{i}]')
    elif isinstance(a, (int, float)) and not isinstance(a, bool):
        if not isinstance(b,(int,float)) or not math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10):
            raise ValueError(where + ': number differs')
    elif a != b: raise ValueError(where + ': value differs')

def compare_csv(saved, new):
    def records(p):
        with p.open(newline='') as f: return list(csv.DictReader(f))
    a,b=records(saved),records(new)
    if len(a)!=len(b): raise ValueError(saved.name+': row count differs')
    for i,(x,y) in enumerate(zip(a,b)):
        if set(x)!=set(y): raise ValueError(saved.name+': columns differ')
        for k in x:
            if x[k]==y[k]: continue
            try:
                if math.isclose(float(x[k]),float(y[k]),rel_tol=1e-10,abs_tol=1e-8): continue
            except ValueError: pass
            raise ValueError(f'{saved.name}: row {i}, {k} differs')

def run(root,out):
    if any(out.iterdir()): raise ValueError('Output directory must be fresh and empty.')
    state={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),
           'scope':'cached comparison -> baseline -> audit; no new acquisition or ecological validation',
           'remote_imagery_load_status':'not_checked_by_runner'}
    dump(out/'run_status.json',state)
    checks=[]
    try:
        manifest=read(root/'SHA256SUMS.json')
        for name,expected in manifest.items():
            p=root/name
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
                raise ValueError('Packaged file changed/missing: '+name)
        checks.append('All packaged-file hashes match.')
        import importlib.metadata
        dump(out/'environment.json',{'python':sys.version,'packages':{n:importlib.metadata.version(n) for n in ['numpy','rasterio','matplotlib']}})
        def engine(name,inp,target):
            print('Running '+name,flush=True)
            with (out/(name+'.log')).open('w') as log:
                proc=subprocess.run([sys.executable,str(root/'src'/name),str(inp),str(target)],
                                    stdout=log,stderr=subprocess.STDOUT,timeout=300)
            if proc.returncode: raise RuntimeError(name+' failed; see its log and stage run_status.json.')
            if read(target/'run_status.json').get('status')!='succeeded':
                raise RuntimeError(name+' did not report success.')
        baseline=out/'baseline'; audit=out/'audit'
        engine('reference_baseline.py',root/'data/Khor_Kalba_Date_Comparison_Results.zip',baseline)
        # Compare before passing predictions to the audit. Never tune to resolve a mismatch.
        for name in ['baseline_summary.json','frozen_experiment_plan.json','frozen_threshold.json','split_and_coverage.json']:
            compare(read(root/'examples/baseline'/name),read(baseline/name),name)
        import numpy as np, rasterio
        for name in ['2018-11-20_predictions.tif','2018-11-30_predictions.tif','geographic_split.tif']:
            with rasterio.open(root/'examples/baseline'/name) as a, rasterio.open(baseline/name) as b:
                if a.crs!=b.crs or a.transform!=b.transform or a.shape!=b.shape or not np.array_equal(a.read(1),b.read(1)):
                    raise ValueError(name+': decoded grid/values differ')
        checks.append('Baseline summaries, frozen plan, threshold, split and decoded predictions match.')
        package=out/'reproduced_baseline.zip'
        with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(baseline.rglob('*')):
                if p.is_file(): z.write(p,p.relative_to(baseline))
        engine('disagreement_audit.py',package,audit)
        compare(read(root/'examples/audit/audit_summary.json'),read(audit/'audit_summary.json'),'audit_summary')
        for name in ['all_audit_cells.csv','all_clusters.csv']:
            compare_csv(root/'examples/audit'/name,audit/name)
        checks.append('Audit summary and all cell/cluster records match.')
        with (audit/'all_clusters.csv').open(newline='') as f:
            clusters={r['cluster_id']:r for r in csv.DictReader(f)}
        for case in read(root/'examples/review/case_reviews.json'):
            cid=case['case']
            if int(clusters[cid]['centres'])!=case['cells'] or int(clusters[cid]['rank_within_category'])!=1:
                raise ValueError('Curated case no longer matches reproduced cluster: '+cid)
        checks.append('Three curated cases retain their recorded size and rank.')
        state['status']='succeeded'
        print('REPRODUCTION MATCHED. No independent ecological accuracy or new visual review established.',flush=True)
    except Exception as exc:
        state.update(status='failed',error=str(exc))
        (out/'failure_log.txt').write_text(traceback.format_exc())
        print('FAILED: '+str(exc),flush=True)
    finally:
        state['finished_utc']=datetime.now(timezone.utc).isoformat()
        dump(out/'checks.json',checks);dump(out/'run_status.json',state)
    return state['status']=='succeeded'

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    sys.exit(0 if run(args.root.resolve(),args.out.resolve()) else 1)
