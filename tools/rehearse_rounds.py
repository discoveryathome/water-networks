"""One bounded design -> challenge -> revised design rehearsal."""
from pathlib import Path
import sys,json,hashlib,random,time,copy,logging
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from model import SPEC,Hydraulic,cost
from rounds import digest,validate_demand,design_verdict,challenge_verdict
logging.getLogger('wntr.epanet.toolkit').setLevel(logging.ERROR)
OUT=ROOT/'results/ticktock';OUT.mkdir(exist_ok=False)
protocol={'envelope':'each node1.0..1.2; demand-weighted total<=1.105; synthetic,not calibrated','round1':'original four-scenario suite, previous baseline and cheaper design registered immutably','challenge':'512fixed random envelope-feasible samples at seed88173; select up to3largest verified failures separated by L-infinity>=.02','round2':'freeze original suite plus selected challenges; greedy repair/descent then fixed4000evaluation perturb-repair at seeds1301,1453; keep separately initialized greedy control','fresh_evaluation':'128new samples at seed20261024 evaluated only after all designs frozen; all exposed prior samples remain development evidence','stop':'one cycle; no selection feedback from fresh evaluation','acceptance':'both hydraulic solvers; no global robustness or Pareto-dominance assumption'}
(ROOT/'research/distribution-prep/ticktock-protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
def write(path,obj):path.parent.mkdir(parents=True,exist_ok=True);assert not path.exists();path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
h=Hydraulic();weights=h.demands
r1={'schema':'water-round/v1','round_id':'r001','parent_round_sha256':None,'network_sha256':SPEC['network_sha256'],'problem_sha256':hashlib.sha256((ROOT/'data/problem.json').read_bytes()).hexdigest(),'demand_weights':weights,'envelope':{'lower':1.0,'upper':1.2,'weighted_total_max':1.105},'challenge_minimum_shortfall_m':.005,'challenge_minimum_linf_distance':.02,'scenarios':[{'id':n,'multipliers':SPEC['scenarios'][n],'origin':'initial synthetic task'} for n in SPEC['tasks']['stress']],'scientific_status':'synthetic benchmark assumptions,review pending'}
write(ROOT/'rounds/r001/round.json',r1)
def design(round_,indices,provenance):return {'type':'design','round_id':round_['round_id'],'round_sha256':digest(round_),'network_sha256':round_['network_sha256'],'indices':indices,'cost':cost(indices),'provenance':provenance}
b=json.loads((ROOT/'results/initial/stress-baseline.json').read_text());cheap=json.loads((ROOT/'results/initial/stress-719-perturb_repair.json').read_text())
initial=[]
for name,c in [('baseline',b),('cheaper',cheap)]:
 d=design(r1,c['indices'],'retained author-run initial trial');write(ROOT/'rounds/r001/designs'/f'{name}.json',d);initial.append((name,d));write(OUT/f'{name}-r001-verification.json',design_verdict(d))

def sample(rng,n):
 out=[];w=np.array(weights)
 for _ in range(n):
  x=rng.uniform(0,.2,31);mean=float(np.dot(w,x)/sum(w))
  if mean>.105:x*=.105/mean
  # Floating arithmetic stays inside an explicit acceptance tolerance, not above hydraulic thresholds.
  out.append((1+x).tolist())
 return out
samples=sample(np.random.default_rng(88173),512);traces=[];ranked=[];target=initial[1][1]
for i,m in enumerate(samples):
 validate_demand(m,r1);v=h.evaluate(target['indices'],[m]);short=30-v['scenarios'][0]['minimum_pressure_m'];traces.append({'sample':i,'multipliers':m,'minimum_pressure_m':30-short,'solver_ok':v['solver_ok']})
 if v['solver_ok'] and short>=.005:ranked.append((short,i,m))
write(OUT/'challenge-search.json',traces);challenges=[];checks=[]
for short,i,m in sorted(ranked,reverse=True):
 c={'type':'challenge','round_id':'r001','round_sha256':digest(r1),'target_sha256':digest(target),'multipliers':m,'provenance':{'seed':88173,'sample':i}}
 try:v=challenge_verdict(c,challenges)
 except AssertionError:continue
 challenges.append(c);checks.append(v);write(ROOT/'rounds/r001/challenges'/f'challenge-{len(challenges):02d}.json',c)
 if len(challenges)==3:break
assert challenges,'Rehearsal produced no verified challenge';write(OUT/'challenge-verification.json',checks)
r2=copy.deepcopy(r1);r2['round_id']='r002';r2['parent_round_sha256']=digest(r1);r2['scenarios'] += [{'id':f'challenge-{i+1:02d}','multipliers':c['multipliers'],'origin_sha256':digest(c)} for i,c in enumerate(challenges)];write(ROOT/'rounds/r002/round.json',r2)
# Reuse the tested optimizer primitives without executing their previous driver.
source=(ROOT/'tools/run_trial.py').read_text();chunk=source[source.index('class Budget'):source.index('h=Hydraulic();reference')];namespace={'json':json};exec(compile(chunk,'historical-search-primitives','exec'),namespace);Search=namespace['Search'];Budget=namespace['Budget']
scenarios=[s['multipliers'] for s in r2['scenarios']];round2=[]
with (OUT/'repair-trace.jsonl').open('w') as trace:
 s=Search(h,scenarios,12000,trace);x,v=s.repair(target['indices']);assert v['feasible'];s.descend(x,random.Random(9901));seedx=s.bestx
control=design(r2,seedx,'greedy repair/descent control; setup calls='+str(s.calls));write(ROOT/'rounds/r002/designs/control.json',control);round2.append(('control',control))
for seed in [1301,1453]:
 rng=random.Random(seed);start=time.perf_counter()
 with (OUT/f'design-{seed}-trace.jsonl').open('w') as trace:
  s=Search(h,scenarios,4000,trace);s.eval(seedx)
  try:
   while True:
    q=s.bestx.copy()
    for i in rng.sample(range(34),rng.randint(2,5)):q[i]=max(0,min(5,q[i]+rng.choice([-2,-1,1,2])))
    q,v=s.repair(q)
    if v['feasible']:s.descend(q,rng)
  except Budget:pass
 d=design(r2,s.bestx,{'algorithm':'perturb_repair','seed':seed,'design_evaluations':s.calls,'seconds':time.perf_counter()-start});write(ROOT/'rounds/r002/designs'/f'design-{seed}.json',d);round2.append((str(seed),d))
for name,d in round2:write(OUT/f'{name}-r002-verification.json',design_verdict(d))
all_designs=[('r001-'+n,d) for n,d in initial]+[('r002-'+n,d) for n,d in round2];write(OUT/'candidate-freeze.json',{n:digest(d) for n,d in all_designs})
# Fresh generator is invoked only after the final design hashes are frozen.
fresh=sample(np.random.default_rng(20261024),128);evaluations=[]
for n,d in all_designs:
 v=h.evaluate(d['indices'],fresh);mins=[x['minimum_pressure_m'] for x in v['scenarios']];evaluations.append({'design':n,'round_id':d['round_id'],'cost':d['cost'],'passed':sum(x>=30 for x in mins),'total':128,'worst_pressure_m':min(mins),'minimum_pressures_m':mins,'design_sha256':digest(d)})
write(OUT/'fresh-evaluation.json',{'seed':20261024,'multipliers':fresh,'designs':evaluations,'selection_feedback':False});h.close()
write(OUT/'summary.json',{'verified_challenges':len(challenges),'challenge_pressure_shortfalls':[v['confirmed_shortfall_m'] for v in checks],'round1_designs':2,'round2_designs':3,'fresh_evaluation':evaluations,'claim':'One complete author-run workflow rehearsal; fresh sampling does not certify the full demand envelope'})
write(ROOT/'rounds/index.json',{'current_design_round':'r002','rounds':{'r001':{'digest':digest(r1),'status':'archived,design validity preserved'},'r002':{'digest':digest(r2),'status':'open for designs and challenges'}},'review_status':'pre-release author-run rehearsal,scientific review pending'})
print(json.dumps({'challenges':len(challenges),'fresh':[{k:v for k,v in x.items() if k!='minimum_pressures_m'} for x in evaluations]},indent=2))
