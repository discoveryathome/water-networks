from pathlib import Path
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from rounds import design_verdict,challenge_verdict,read_round
p=argparse.ArgumentParser();p.add_argument('submission');a=p.parse_args();f=Path(a.submission);assert f.stat().st_size<=100000,'Submission too large';c=json.loads(f.read_text())
if c.get('type')=='design':v=design_verdict(c)
elif c.get('type')=='challenge':
 read_round(c['round_id']);archive=[]
 for q in (ROOT/'rounds'/c['round_id']/'challenges').glob('*.json'):
  old=json.loads(q.read_text())
  if old!=c:archive.append(old)
 v=challenge_verdict(c,archive)
else:raise ValueError('Expected design or challenge submission')
print(json.dumps(v,indent=2))
