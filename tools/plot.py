from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'results/post-freeze.json').read_text())['candidates'];names=['stress-baseline.json','stress-419-perturb_repair.json','stress-719-perturb_repair.json'];data=[next(x for x in rows if x['certificate'].endswith(n)) for n in names];labels=['Inherited scenario baseline','Cheaper candidate A','Cheaper candidate B']
fig,axes=plt.subplots(1,2,figsize=(12,5));bars=axes[0].bar(labels,[x['cost']/1e6 for x in data],color=['#287797','#e2a642','#c47737']);axes[0].set_ylabel('Benchmark design cost (millions)');axes[0].set_ylim(0,8.5);axes[0].set_title('All satisfy the four optimization scenarios')
for b,x in zip(bars,data):axes[0].text(b.get_x()+b.get_width()/2,x['cost']/1e6+.12,f"{x['cost']/1e6:.3f}",ha='center')
bars=axes[1].bar(labels,[x['passed_scenarios'] for x in data],color=['#287797','#e2a642','#c47737']);axes[1].set_ylim(0,22);axes[1].set_ylabel('New scenarios passed (out of 20)');axes[1].set_title('Cost savings reduce unseen demand coverage')
for b,x in zip(bars,data):axes[1].text(b.get_x()+b.get_width()/2,x['passed_scenarios']+.3,str(x['passed_scenarios']),ha='center')
for ax in axes:ax.tick_params(axis='x',labelsize=9,rotation=12);ax.spines[['top','right']].set_visible(False)
fig.suptitle('Water-network pilot: a checked cost / scenario-coverage tradeoff');fig.tight_layout();fig.savefig(ROOT/'visuals/initial.png',dpi=150);fig.savefig(ROOT/'visuals/initial.svg')
