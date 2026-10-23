"""Bounded starter contribution; never changes an accepted round."""
from pathlib import Path
import argparse,json,sys,random,time,logging
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from model import Hydraulic,cost
from rounds import read_round,digest,design_verdict,challenge_verdict
from search import Search,Budget
logging.getLogger('wntr.epanet.toolkit').setLevel(logging.ERROR)
p=argparse.ArgumentParser();p.add_argument('mode',choices=['design','challenge']);p.add_argument('--round');p.add_argument('--seed',type=int,default=77173);p.add_argument('--budget',type=int,default=512);p.add_argument('--out',required=True);a=p.parse_args();assert 1<=a.budget<=20000;out=(ROOT/a.out).resolve();assert out.is_relative_to(ROOT);out.mkdir(parents=True,exist_ok=False)
round_id=a.round or json.loads((ROOT/'rounds/index.json').read_text())['current_design_round'];r=read_round(round_id);targets=[json.loads(p.read_text()) for p in sorted((ROOT/'rounds'/round_id/'designs').glob('*.json'))];target=min(targets,key=lambda x:x['cost']);h=Hydraulic();start=time.perf_counter()
try:
 if a.mode=='design':
  rng=random.Random(a.seed)
  with (out/'trace.jsonl').open('w') as trace:
   s=Search(h,[x['multipliers'] for x in r['scenarios']],a.budget,trace);s.eval(target['indices'])
   try:
    while True:
     q=s.bestx.copy()
     for i in rng.sample(range(34),rng.randint(2,5)):q[i]=max(0,min(5,q[i]+rng.choice([-2,-1,1,2])))
     q,v=s.repair(q)
     if v['feasible']:s.descend(q,rng)
   except Budget:pass
  c={'type':'design','round_id':round_id,'round_sha256':digest(r),'network_sha256':r['network_sha256'],'indices':s.bestx,'cost':cost(s.bestx),'provenance':{'seed':a.seed,'budget':a.budget,'method':'bounded perturb-repair from current accepted design'}};v=design_verdict(c);(out/'submission.json').write_text(json.dumps(c,indent=2)+'\n');report={'verified':True,'type':'design','improved_cost':c['cost']<target['cost'],'verification':v}
 else:
  rng=np.random.default_rng(a.seed);w=np.array(r['demand_weights']);archive=[json.loads(p.read_text()) for p in (ROOT/'rounds'/round_id/'challenges').glob('*.json')];candidates=[];trace=[]
  for i in range(a.budget):
   x=rng.uniform(0,r['envelope']['upper']-1,len(w));average=float(np.dot(w,x)/sum(w));limit=r['envelope']['weighted_total_max']-1
   if average>limit:x*=limit/average
   m=(1+x).tolist();v=h.evaluate(target['indices'],[m]);minimum=v['scenarios'][0]['minimum_pressure_m'];trace.append({'sample':i,'multipliers':m,'minimum_pressure_m':minimum,'solver_ok':v['solver_ok']})
   if v['solver_ok'] and minimum<=30-r['challenge_minimum_shortfall_m']:candidates.append((minimum,i,m))
  (out/'trace.json').write_text(json.dumps(trace)+'\n');report={'verified_search_execution':True,'type':'challenge','found':False,'budget':a.budget,'note':'No verified counterexample is not a robustness proof'}
  for _,i,m in sorted(candidates):
   c={'type':'challenge','round_id':round_id,'round_sha256':digest(r),'target_sha256':digest(target),'multipliers':m,'provenance':{'seed':a.seed,'sample':i,'budget':a.budget}}
   try:v=challenge_verdict(c,archive)
   except AssertionError:continue
   (out/'submission.json').write_text(json.dumps(c,indent=2)+'\n');report={'verified':True,'type':'challenge','found':True,'verification':v};break
finally:h.close()
report['seconds']=time.perf_counter()-start;(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
