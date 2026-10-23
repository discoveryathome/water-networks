from pathlib import Path
import sys,json,hashlib
import numpy as np,wntr
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import Hydraulic,SPEC,validate

def check(path):
 c=json.loads(Path(path).read_text());validate(c['indices']);assert c['network_sha256']==SPEC['network_sha256'];assert hashlib.sha256((ROOT/SPEC['network']).read_bytes()).hexdigest()==SPEC['network_sha256']
 if 'problem_sha256' in c:assert c['problem_sha256']==hashlib.sha256((ROOT/'data/problem.json').read_bytes()).hexdigest()
 assert c['task'] in SPEC['tasks'];diam=[SPEC['diameters_in'][i] for i in c['indices']];h=Hydraulic()
 try:native=h.evaluate(c['indices'],SPEC['tasks'][c['task']])
 finally:h.close()
 assert native['feasible'],'EPANET constraint failure'
 checks=[];independent_cost=None
 for name,nr in zip(SPEC['tasks'][c['task']],native['scenarios']):
  w=wntr.network.WaterNetworkModel(str(ROOT/SPEC['network']))
  for pid,d in zip(SPEC['pipes'],diam):w.get_link(pid).diameter=d*.0254
  # Independently accumulate cost from the input model, rather than stored lengths/results.
  independent_cost=sum(w.get_link(pid).length*1.1*d**1.5 for pid,d in zip(SPEC['pipes'],diam))
  for node,m in zip(SPEC['junctions'],SPEC['scenarios'][name]):
   for demand in w.get_node(node).demand_timeseries_list:demand.base_value*=m
  sim=wntr.sim.WNTRSimulator(w);res=sim.run_sim(solver_options={'TOL':1e-10,'MAXITER':300},convergence_error=True)
  heads=res.node['head'].loc[0];pressure=res.node['pressure'].loc[0,SPEC['junctions']].to_numpy();flows=res.link['flowrate'].loc[0];demands=res.node['demand'].loc[0];assert np.isfinite(pressure).all() and min(pressure)>=30,'Independent hydraulic constraint failure'
  mass={node:-float(demands[node]) for node in SPEC['junctions']};energy=[]
  for pid,p in w.pipes():
   q=float(flows[pid]);a=p.start_node_name;b=p.end_node_name
   if a in mass:mass[a]-=q
   if b in mass:mass[b]+=q
   loss=10.666829500036352*p.length/p.roughness**1.852/p.diameter**4.871*q*abs(q)**.852
   energy.append(abs(float(heads[a]-heads[b])-loss))
  maxmass=max(abs(x) for x in mass.values());maxenergy=max(energy);delta=float(np.max(abs(pressure-np.array(nr['pressures_m']))));assert maxmass<1e-8 and maxenergy<1e-4,(maxmass,maxenergy);assert delta<.001,delta
  checks.append({'scenario':name,'minimum_pressure_m':float(min(pressure)),'max_pressure_difference_vs_epanet_m':delta,'max_mass_residual_m3s':maxmass,'max_headloss_residual_m':maxenergy})
 expected=c.get('cost',c.get('verification',{}).get('cost'));assert expected is not None and abs(independent_cost-expected)<1e-6
 return {'verified':True,'task':c['task'],'cost':independent_cost,'epanet':native,'independent_wntr':checks,'limits':'Checks fixed benchmark assumptions; not calibration or certification of a real water system'}
if __name__=='__main__':print(json.dumps(check(sys.argv[1]),indent=2))
