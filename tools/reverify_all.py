from pathlib import Path
import json,sys,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];from verify import check
sys.path.insert(0,str(ROOT/'src'));from model import Hydraulic
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args();out=(ROOT/args.out).resolve();assert out.is_relative_to(ROOT);out.mkdir(parents=True,exist_ok=False)
paths=[ROOT/x['certificate'] for x in json.loads((ROOT/'results/initial/summary.json').read_text())]+[ROOT/'results/initial'/f'{task}-baseline.json' for task in ['nominal','stress']]
freeze={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
# Hash every candidate before any post-freeze evaluation.
(out/'candidate-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
checks=[]
for p in paths:
 v=check(p);checks.append({'certificate':str(p.relative_to(ROOT)),**v});print(p.name,'verified',flush=True)
(out/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
rng=np.random.default_rng(991023);scenarios=rng.uniform(1,1.2,(20,31)).tolist();h=Hydraulic();rows=[]
for p in paths:
 assert hashlib.sha256(p.read_bytes()).hexdigest()==freeze[str(p.relative_to(ROOT))];c=json.loads(p.read_text());v=h.evaluate(c['indices'],scenarios);rows.append({'certificate':str(p.relative_to(ROOT)),'task':c['task'],'cost':v['cost'],'passed_scenarios':sum(s['minimum_pressure_m']>=30 and s['epanet_code']==0 for s in v['scenarios']),'total_scenarios':20,'minimum_pressures_m':[s['minimum_pressure_m'] for s in v['scenarios']]})
h.close();(out/'post-freeze.json').write_text(json.dumps({'seed':991023,'multipliers':scenarios,'candidates':rows,'limits':'20sampled synthetic demand scenarios, not a universal robustness guarantee; no feedback to selection'},indent=2)+'\n')
