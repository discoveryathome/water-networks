from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from rounds import *
index=json.loads((ROOT/'rounds/index.json').read_text());reports=[]
for round_id,metadata in index['rounds'].items():
 r=read_round(round_id);assert digest(r)==metadata['digest'],'Changed frozen round'
 for p in sorted((ROOT/'rounds'/round_id/'designs').glob('*.json')):reports.append({'path':str(p.relative_to(ROOT)),**design_verdict(json.loads(p.read_text()))})
 previous=[]
 for p in sorted((ROOT/'rounds'/round_id/'challenges').glob('*.json')):
  c=json.loads(p.read_text());reports.append({'path':str(p.relative_to(ROOT)),**challenge_verdict(c,previous)});previous.append(c)
print(json.dumps({'verified':True,'registered_certificates':len(reports),'rounds':list(index['rounds']),'checks':reports},indent=2))
