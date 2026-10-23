"""Versioned design/challenge validation. No search or frontier mutation on import."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import wntr
from model import ROOT,SPEC,Hydraulic,validate,cost

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def read_round(round_id):
 assert isinstance(round_id,str) and round_id in {'r001','r002'},'Unknown frozen round'
 p=ROOT/'rounds'/round_id/'round.json';r=json.loads(p.read_text())
 assert r['round_id']==round_id and r['network_sha256']==SPEC['network_sha256']
 assert r['problem_sha256']==hashlib.sha256((ROOT/'data/problem.json').read_bytes()).hexdigest()
 assert hashlib.sha256((ROOT/SPEC['network']).read_bytes()).hexdigest()==r['network_sha256']
 assert len(r['demand_weights'])==31 and sum(r['demand_weights'])>0
 for s in r['scenarios']:validate_demand(s['multipliers'],r)
 return r
def validate_demand(m,r):
 assert isinstance(m,list) and len(m)==31,'Exactly31demand multipliers required'
 assert all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in m),'Finite numeric multipliers required'
 e=r['envelope'];assert all(e['lower']<=x<=e['upper'] for x in m),'Outside per-node envelope'
 weighted=sum(d*x for d,x in zip(r['demand_weights'],m))/sum(r['demand_weights'])
 assert weighted<=e['weighted_total_max']+1e-12,'Outside total-demand budget'
 return weighted

def audit(indices,multipliers):
 """Independent WNTR hydraulics, mass and energy residuals; no feasibility assumption."""
 validate(indices);w=wntr.network.WaterNetworkModel(str(ROOT/SPEC['network']))
 for pid,i in zip(SPEC['pipes'],indices):w.get_link(pid).diameter=SPEC['diameters_in'][i]*.0254
 for node,m in zip(SPEC['junctions'],multipliers):
  for d in w.get_node(node).demand_timeseries_list:d.base_value*=m
 res=wntr.sim.WNTRSimulator(w).run_sim(solver_options={'TOL':1e-10,'MAXITER':300},convergence_error=True)
 heads=res.node['head'].loc[0];pressure=res.node['pressure'].loc[0,SPEC['junctions']].to_numpy();flows=res.link['flowrate'].loc[0];demand=res.node['demand'].loc[0]
 assert np.isfinite(pressure).all();mass={n:-float(demand[n]) for n in SPEC['junctions']};energy=[]
 for pid,p in w.pipes():
  q=float(flows[pid]);a=p.start_node_name;b=p.end_node_name
  if a in mass:mass[a]-=q
  if b in mass:mass[b]+=q
  loss=10.666829500036352*p.length*q*abs(q)**.852/p.roughness**1.852/p.diameter**4.871
  energy.append(abs(float(heads[a]-heads[b])-loss))
 mass_res=max(abs(x) for x in mass.values());head_res=max(energy)
 assert mass_res<1e-8 and head_res<1e-4,(mass_res,head_res)
 independent_cost=sum(w.get_link(pid).length*1.1*SPEC['diameters_in'][i]**1.5 for pid,i in zip(SPEC['pipes'],indices))
 return {'pressures_m':pressure.tolist(),'minimum_pressure_m':float(min(pressure)),'cost':independent_cost,'max_mass_residual_m3s':mass_res,'max_headloss_residual_m':head_res}

def design_verdict(c):
 assert c['type']=='design';r=read_round(c['round_id']);assert c['round_sha256']==digest(r),'Wrong round digest';assert c['network_sha256']==r['network_sha256'];validate(c['indices'])
 assert isinstance(c['cost'],(int,float)) and not isinstance(c['cost'],bool) and math.isfinite(c['cost']) and abs(c['cost']-cost(c['indices']))<1e-6,'Wrong cost'
 h=Hydraulic()
 try:native=h.evaluate(c['indices'],[s['multipliers'] for s in r['scenarios']])
 finally:h.close()
 assert native['feasible'],'Design violates round scenarios'
 checks=[]
 for s,v in zip(r['scenarios'],native['scenarios']):
  independent=audit(c['indices'],s['multipliers']);delta=max(abs(a-b) for a,b in zip(v['pressures_m'],independent['pressures_m']));assert delta<.001,'Solvers disagree';assert independent['minimum_pressure_m']>=30,'Independent solver rejects design';assert abs(independent['cost']-c['cost'])<1e-6
  checks.append({'scenario':s['id'],'epanet_minimum_m':v['minimum_pressure_m'],'independent_minimum_m':independent['minimum_pressure_m'],'solver_difference_m':delta,'mass_residual':independent['max_mass_residual_m3s'],'headloss_residual':independent['max_headloss_residual_m']})
 return {'verified':True,'type':'design','round_id':r['round_id'],'cost':c['cost'],'checks':checks,'claim':'Feasible for this fixed round only; no universal robustness claim'}

def challenge_verdict(c,archive=None):
 assert c['type']=='challenge';r=read_round(c['round_id']);assert c['round_sha256']==digest(r),'Wrong round digest';weighted=validate_demand(c['multipliers'],r)
 targets=[]
 for p in (ROOT/'rounds'/r['round_id']/'designs').glob('*.json'):
  t=json.loads(p.read_text())
  if digest(t)==c['target_sha256']:targets.append(t)
 assert len(targets)==1,'Target must be an immutable registered design';target=targets[0]
 # Do not trust a target merely because the challenger labels it accepted.
 design_verdict(target)
 h=Hydraulic()
 try:native=h.evaluate(target['indices'],[c['multipliers']])
 finally:h.close()
 assert native['solver_ok'],'Hydraulic warning or failure is not a verified challenge';ind=audit(target['indices'],c['multipliers']);v=native['scenarios'][0];delta=max(abs(a-b) for a,b in zip(v['pressures_m'],ind['pressures_m']));assert delta<.001,'Solvers disagree'
 severity=30-max(v['minimum_pressure_m'],ind['minimum_pressure_m']);assert severity>=r['challenge_minimum_shortfall_m'],'No reproducible pressure failure beyond solver margin'
 prior=[s['multipliers'] for s in r['scenarios']]
 if archive is not None:
  for old in archive:
   if old['round_id']==r['round_id']:prior.append(old['multipliers'])
 novelty=min(float(np.max(np.abs(np.array(c['multipliers'])-np.array(m)))) for m in prior)
 assert novelty>=r['challenge_minimum_linf_distance'],'Duplicate or near-duplicate demand scenario'
 return {'verified':True,'type':'challenge','round_id':r['round_id'],'target_sha256':c['target_sha256'],'confirmed_shortfall_m':severity,'weighted_total_multiplier':weighted,'nearest_scenario_linf':novelty,'epanet_minimum_m':v['minimum_pressure_m'],'independent_minimum_m':ind['minimum_pressure_m'],'solver_difference_m':delta,'claim':'Counterexample inside the declared synthetic envelope; prior round design validity is unchanged'}
