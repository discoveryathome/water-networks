"""Seeded task draw from discover/catalog.json, the same draw as `discover pick --offline` (Discovery@Home spec §7).

Suggestions, not reservations: check the Handoffs discussion for live claims before starting.
"""
from pathlib import Path
import argparse,hashlib,json,re,secrets
p=argparse.ArgumentParser();p.add_argument('--seed',help='32 hex digits; random if omitted');p.add_argument('--track');p.add_argument('--task');a=p.parse_args()
seed=(a.seed or secrets.token_hex(16)).lower()
if not re.fullmatch(r'[0-9a-f]{32}',seed):p.error('--seed must be exactly 32 hexadecimal digits')
draw=lambda label:int(hashlib.sha256(json.dumps([seed,label],separators=(',',':')).encode()).hexdigest(),16)
catalog=json.loads((Path(__file__).resolve().parents[1]/'discover/catalog.json').read_text());tracks=catalog['tracks']
if a.task:
 hits=[(t,c) for t in tracks for c in t['tasks'] if c['id']==a.task]
 if not hits:p.error(f'no card {a.task!r}')
 track,cards=hits[0][0],[hits[0][1]]
else:
 if a.track:
  track=next((t for t in tracks if t['id']==a.track),None)
  if not track:p.error(f'no track {a.track!r}')
 else:
  ticket=draw('track')%sum(t['weight'] for t in tracks)
  for track in tracks:
   ticket-=track['weight']
   if ticket<0:break
 pool,cards=list(track['tasks']),[]
 for i in range(min(3,len(pool))):cards.append(pool.pop(draw(f'card:{i}')%(1000*len(pool))//1000))
out=[{'task_id':c['id'],'question':c['question'],'method':c['methods'][draw(f"method:{c['id']}")%len(c['methods'])],'first_step':c['first_step'],'acceptance_gate':c['acceptance_gate']} for c in cards]
print(json.dumps({'seed':seed,'priority_revision':catalog['priority_revision'],'track':track['id'],'suggestions':out,'note':'Suggestions, not reservations. Check the Handoffs discussion for live claims and open handoffs first (docs/CONTRIBUTING.md, Claiming work).'},indent=2))
