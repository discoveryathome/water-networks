"""Bounded search primitives; evaluations and failures are retained in the trace."""
import json
class Budget(Exception):pass
class Search:
 def __init__(self,h,scenarios,budget,trace):self.h=h;self.scenarios=scenarios;self.budget=budget;self.trace=trace;self.calls=0;self.best=None;self.bestx=None
 def eval(self,x):
  if self.calls>=self.budget:raise Budget
  v=self.h.evaluate(x,self.scenarios);self.calls+=1;improved=v['feasible'] and (self.best is None or v['cost']<self.best['cost'])
  if improved:self.best=v;self.bestx=x.copy()
  self.trace.write(json.dumps({'call':self.calls,'indices':x,'cost':v['cost'],'violation':v['violation'],'feasible':v['feasible'],'solver_ok':v['solver_ok'],'minimum_pressure':min(s['minimum_pressure_m'] for s in v['scenarios']),'incumbent_improved':improved})+'\n');return v
 def repair(self,x):
  x=x.copy();v=self.eval(x)
  for _ in range(170):
   if v['feasible']:return x,v
   options=[]
   for i in range(34):
    if x[i]==5:continue
    q=x.copy();q[i]+=1;w=self.eval(q)
    if w['solver_ok'] and w['violation']<v['violation']:options.append(((v['violation']-w['violation'])/(w['cost']-v['cost']),q,w))
   if not options:return x,v
   _,x,v=max(options,key=lambda z:z[0])
  return x,v
 def descend(self,x,rng):
  x=x.copy();v=self.eval(x)
  if not v['feasible']:return x,v
  for _ in range(2):
   changed=False;order=list(range(34));rng.shuffle(order)
   for i in order:
    for level in range(x[i]):
     q=x.copy();q[i]=level;w=self.eval(q)
     if w['feasible']:x=q;v=w;changed=True;break
   if not changed:break
  return x,v
