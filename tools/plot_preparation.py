"""Render post-freeze sampled evidence; no simulation or round changes."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'results/ticktock/summary.json').read_text())['fresh_evaluation'][:4]
labels=['Earlier baseline','Earlier cheaper','Revised control','Revised search']
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(10,5.8));fig.subplots_adjust(left=.20,right=.77,bottom=.21,top=.82)
for i,r in enumerate(rows):
 ax.scatter(r['worst_pressure_m'],i,color='#167a79' if r['passed']==128 else '#bc6140',s=95,zorder=3)
 ax.text(1.02,i,f"{r['cost']/1e6:.3f}m · {r['passed']}/128",transform=ax.get_yaxis_transform(),va='center')
ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.axvline(30,color='#9b4e38',ls='--');ax.set_xlim(29.55,30.30);ax.set_xlabel('Lowest pressure across 128 fresh sampled demands (m)')
fig.suptitle('Water networks: design → challenge → revised design',x=.06,ha='left',fontsize=17,fontweight='bold')
fig.text(.06,.88,'Three verified counterexamples fed a revised seven-scenario design round.',fontsize=11)
fig.text(.785,.84,'Cost · samples passed',fontsize=10)
fig.text(.06,.055,'New envelope: node demand ×[1.0, 1.2], weighted total ≤1.105. Required pressure: 30 m.\nOne author-run rehearsal. Sampled coverage is not a worst-case robustness certificate.',fontsize=10,color='#4b5563')
for suffix in ['png','svg']:fig.savefig(ROOT/f'visuals/preparation.{suffix}',dpi=160,facecolor='white')
