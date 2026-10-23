from pathlib import Path
import sys,json
import pytest,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'tools'))
from model import validate,cost,Hydraulic,SPEC
from verify import check
@pytest.mark.parametrize('x',[[0]*33,[6]*34,[0.5]*34,[True]*34])
def test_bad_design(x):
 with pytest.raises(AssertionError):validate(x)
def test_cost_units():
 assert abs(cost([0]*34)-sum(SPEC['length_m'])*1.1*12**1.5)<1e-6
def test_published_reference_and_too_small():
 h=Hydraulic()
 try:
  x=[SPEC['diameters_in'].index(d) for d in SPEC['reference_diameters_in']];assert h.evaluate(x,['nominal'])['feasible'];assert not h.evaluate([0]*34,['nominal'])['feasible'];assert not h.evaluate(x,SPEC['tasks']['stress'])['feasible']
 finally:h.close()
def test_forged_cost_rejected(tmp_path):
 c=json.loads((ROOT/'results/initial/nominal-419-multistart.json').read_text());c['cost']=1;p=tmp_path/'forged.json';p.write_text(json.dumps(c))
 with pytest.raises(AssertionError):check(p)
def test_wrong_network_hash_rejected(tmp_path):
 c=json.loads((ROOT/'results/initial/nominal-419-multistart.json').read_text());c['network_sha256']='0'*64;p=tmp_path/'forged.json';p.write_text(json.dumps(c))
 with pytest.raises(AssertionError):check(p)
