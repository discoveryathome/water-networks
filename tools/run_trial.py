from pathlib import Path
import sys,json,time,random,logging,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import *
logging.getLogger('wntr.epanet.toolkit').setLevel(logging.ERROR)
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--out',default='results/initial');args=parser.parse_args();out=(ROOT/args.out).resolve();assert out.is_relative_to(ROOT),'Output must remain inside project';out.mkdir(parents=True,exist_ok=False);rows=[];BUDGET=4000
class Budget(Exception):pass
class Search:
 def __init__(self,h,scenarios,budget,trace):self.h=h;self.scenarios=scenarios;self.budget=budget;self.trace=trace;self.calls=0;self.best=None;self.bestx=None
 def eval(self,x):
  if self.calls>=self.budget:raise Budget
  v=self.h.evaluate(x,self.scenarios);self.calls+=1;improved=v['feasible'] and (self.best is None or v['cost']<self.best['cost'])
  if improved:self.best=v;self.bestx=x.copy()
  self.trace.write(json.dumps({'call':self.calls,'indices':x,'cost':v['cost'],'violation':v['violation'],'feasible':v['feasible'],'solver_ok':v['solver_ok'],'minimum_pressure':min(s['minimum_pressure_m'] for s in v['scenarios']),'incumbent_improved':improved})+'\n');return v
 def repair(self,x):
  x=x.copy();v=self.eval(x)
  for _ in range(170):
   if v['feasible']:return x,v
   options=[]
   for i in range(34):
    if x[i]==5:continue
    q=x.copy();q[i]+=1;w=self.eval(q)
    if w['solver_ok'] and w['violation']<v['violation']:options.append(((v['violation']-w['violation'])/(w['cost']-v['cost']),q,w))
   if not options:return x,v
   _,x,v=max(options,key=lambda z:z[0])
  return x,v
 def descend(self,x,rng):
  x=x.copy();v=self.eval(x)
  if not v['feasible']:return x,v
  for _ in range(2):
   changed=False;order=list(range(34));rng.shuffle(order)
   for i in order:
    for level in range(x[i]):
     q=x.copy();q[i]=level;w=self.eval(q)
     if w['feasible']:x=q;v=w;changed=True;break
   if not changed:break
  return x,v
h=Hydraulic();reference=[SPEC['diameters_in'].index(x) for x in SPEC['reference_diameters_in']]
for task,scenarios in SPEC['tasks'].items():
 t=time.perf_counter()
 with (out/f'{task}-baseline-trace.jsonl').open('w') as f:
  setup=Search(h,scenarios,8000,f);x,v=setup.repair(reference);assert v['feasible'];x,v=setup.descend(x,random.Random(991));initial=setup.bestx;baseline=setup.best
 base={'task':task,'indices':initial,'verification':baseline,'preparation_calls':setup.calls,'preparation_seconds':time.perf_counter()-t,'network_sha256':SPEC['network_sha256']};(out/f'{task}-baseline.json').write_text(json.dumps(base,indent=2)+'\n');print('BASELINE',task,baseline['cost'],setup.calls,flush=True)
 for seed in [419,503,719]:
  for arm in ['multistart','perturb_repair']:
   rng=random.Random(seed);t=time.perf_counter();cp=out/f'{task}-{seed}-{arm}.json'
   with (out/f'{task}-{seed}-{arm}-trace.jsonl').open('w') as trace:
    search=Search(h,scenarios,BUDGET,trace);search.eval(initial)
    try:
     while True:
      if arm=='multistart':search.descend([5]*34,rng)
      else:
       q=search.bestx.copy()
       for i in rng.sample(range(34),rng.randint(2,5)):q[i]=max(0,min(5,q[i]+rng.choice([-2,-1,1,2])))
       q,v=search.repair(q)
       if v['feasible']:search.descend(q,rng)
    except Budget:pass
   cert={'task':task,'seed':seed,'arm':arm,'indices':search.bestx,'network_sha256':SPEC['network_sha256'],'problem_sha256':hashlib.sha256((ROOT/'data/problem.json').read_bytes()).hexdigest(),'cost':search.best['cost'],'verification':search.best,'baseline_cost':baseline['cost'],'design_evaluations':search.calls,'hydraulic_solves':search.calls*len(scenarios),'seconds':time.perf_counter()-t};cp.write_text(json.dumps(cert,indent=2)+'\n');row={k:v for k,v in cert.items() if k not in ['indices','verification']};row['certificate']=str(cp.relative_to(ROOT));rows.append(row);(out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(task,seed,arm,baseline['cost'],cert['cost'],cert['seconds'],flush=True)
h.close()
