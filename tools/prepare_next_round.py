"""Write a proposed next round without modifying any accepted round or index."""
from pathlib import Path
import sys,json,argparse,copy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from rounds import *
p=argparse.ArgumentParser();p.add_argument('--parent',required=True);p.add_argument('--next-id',required=True);p.add_argument('--out',required=True);p.add_argument('challenges',nargs='+');a=p.parse_args();assert re.fullmatch(r'r[0-9]{3,6}',a.next_id);parent=read_round(a.parent);assert not (ROOT/'rounds'/a.next_id).exists();out=(ROOT/a.out).resolve();assert out.is_relative_to(ROOT) and not out.exists();out.mkdir(parents=True);accepted=[];checks=[]
for file in a.challenges:
 c=json.loads(Path(file).read_text());assert c['round_id']==a.parent;checks.append(challenge_verdict(c,accepted));accepted.append(c)
proposal=copy.deepcopy(parent);proposal['parent_round_sha256']=digest(parent);proposal['round_id']=a.next_id;proposal['scenarios'] += [{'id':f'challenge-{digest(c)[:12]}','multipliers':c['multipliers'],'origin_sha256':digest(c)} for c in accepted]
(out/'proposed-round.json').write_text(json.dumps(proposal,indent=2)+'\n');(out/'challenge-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('Proposal prepared; maintainer review, baseline feasibility, and index publication are required before activation.')
