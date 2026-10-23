from pathlib import Path
import json,hashlib,tempfile,logging
from numbers import Integral
import numpy as np
from wntr.epanet.toolkit import ENepanet
from wntr.epanet.util import EN
ROOT=Path(__file__).resolve().parents[1]
SPEC=json.loads((ROOT/'data/problem.json').read_text())
def validate(x):
 assert len(x)==34 and all(isinstance(v,Integral) and not isinstance(v,(bool,np.bool_)) and 0<=v<6 for v in x),'Expected34integer catalog indices0..5'
def cost(x):
 validate(x);return float(np.dot(np.array(SPEC['length_m']),1.1*np.array(SPEC['diameters_in'])[x]**1.5))
class Hydraulic:
 def __init__(self):
  assert hashlib.sha256((ROOT/SPEC['network']).read_bytes()).hexdigest()==SPEC['network_sha256'];self.temp=tempfile.TemporaryDirectory();d=Path(self.temp.name);self.en=ENepanet(version=2.2);self.en.ENopen(str(ROOT/SPEC['network']),str(d/'run.rpt'),str(d/'run.bin'));self.nodes=[self.en.ENgetnodeindex(n) for n in SPEC['junctions']];self.links=[self.en.ENgetlinkindex(n) for n in SPEC['pipes']];self.demands=[self.en.ENgetnodevalue(i,EN.BASEDEMAND) for i in self.nodes];self.en.ENopenH()
 def evaluate(self,x,scenarios):
  validate(x);reports=[]
  for i,v in zip(self.links,x):self.en.ENsetlinkvalue(i,EN.DIAMETER,float(SPEC['diameters_in'][v]*25.4))
  for name in scenarios:
   multipliers=SPEC['scenarios'][name] if isinstance(name,str) else name
   for i,d,m in zip(self.nodes,self.demands,multipliers):self.en.ENsetnodevalue(i,EN.BASEDEMAND,d*m)
   self.en.ENinitH(10);self.en.ENrunH();code=self.en.errcode;pressures=[self.en.ENgetnodevalue(i,EN.PRESSURE) for i in self.nodes];assert np.isfinite(pressures).all()
   reports.append({'scenario':name if isinstance(name,str) else 'custom','pressures_m':pressures,'minimum_pressure_m':min(pressures),'epanet_code':code})
  violation=sum(max(0,30-p) for r in reports for p in r['pressures_m']);valid=all(r['epanet_code']==0 for r in reports)
  return {'cost':cost(x),'violation':violation,'feasible':valid and violation==0,'scenarios':reports,'solver_ok':valid}
 def close(self):self.en.ENcloseH();self.en.ENclose();self.temp.cleanup()
