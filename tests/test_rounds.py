from pathlib import Path
import sys,json,copy
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from rounds import *
@pytest.fixture
def old_design():return json.loads((ROOT/'rounds/r001/designs/cheaper.json').read_text())
@pytest.fixture
def challenge():return json.loads((ROOT/'rounds/r001/challenges/challenge-01.json').read_text())
def test_old_round_remains_valid(old_design):assert design_verdict(old_design)['verified']
def test_new_round_design():assert design_verdict(json.loads((ROOT/'rounds/r002/designs/design-1301.json').read_text()))['verified']
def test_verified_counterexample(challenge):assert challenge_verdict(challenge)['confirmed_shortfall_m']>=.005
@pytest.mark.parametrize('multipliers',[[1.2]*31,[1.]*30,[float('nan')]*31,[True]*31,[.9]*31])
def test_demand_envelope(multipliers):
 with pytest.raises(AssertionError):validate_demand(multipliers,read_round('r001'))
def test_duplicate_counterexample(challenge):
 with pytest.raises(AssertionError):challenge_verdict(challenge,[challenge])
def test_no_violation_is_not_a_challenge(challenge):
 challenge['multipliers']=[1.]*31
 with pytest.raises(AssertionError):challenge_verdict(challenge)
def test_round_change_rejected(old_design):
 old_design['round_id']='r002'
 with pytest.raises(AssertionError):design_verdict(old_design)
def test_unregistered_target(challenge):
 challenge['target_sha256']='0'*64
 with pytest.raises(AssertionError):challenge_verdict(challenge)
def test_cost_forgery(old_design):
 old_design['cost']-=1000
 with pytest.raises(AssertionError):design_verdict(old_design)
