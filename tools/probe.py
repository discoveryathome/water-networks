from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import *
h=Hydraulic();rows=[]
for label,x in [('all_large',[5]*34),('published',[SPEC['diameters_in'].index(d) for d in SPEC['reference_diameters_in']])]:
 for task,scenarios in SPEC['tasks'].items():
  t=time.perf_counter();v=h.evaluate(x,scenarios);rows.append({'label':label,'task':task,'indices':x,'verification':v,'seconds':time.perf_counter()-t});print(label,task,v['cost'],v['feasible'],[(s['scenario'],s['minimum_pressure_m']) for s in v['scenarios']],flush=True)
h.close();(ROOT/'research/baseline-probe.json').write_text(json.dumps(rows,indent=2)+'\n')
