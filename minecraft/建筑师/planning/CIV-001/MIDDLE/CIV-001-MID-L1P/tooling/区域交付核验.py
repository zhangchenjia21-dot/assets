"""独立核验范围、见证和递归契约；不评判规划语义是否已获接受。"""
from pathlib import Path
import argparse,json,hashlib
from collections import deque
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--cache',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
P=Path(__file__).resolve().parents[1]
read=lambda x:json.loads(x.read_text('utf-8'))
e=read(P/'evidence/regional-analysis.json');rebuilt=read(a.cache/'regional-analysis.json');assert e==rebuilt,'Independent rebuild differs'
r=np.load(a.cache/'regional-map.npz');t=r['territory'];y=r['height'];m=t==2;tc=r['terrain'];patch=r['patch']
assert int(m.sum())==391002
assert [int(np.sum(m&(tc==k))) for k in [1,2,0]]==[38040,41013,311949]
assert float(np.median(y[m]))==122
seen=np.zeros(m.shape,bool);sizes=[]
for z,x in zip(*np.where(m)):
 if seen[z,x]:continue
 q=deque([(z,x)]);seen[z,x]=1;n=0
 while q:
  z1,x1=q.popleft();n+=1
  for dz,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
   zn,xn=z1+dz,x1+dx
   if 0<=zn<m.shape[0] and 0<=xn<m.shape[1] and m[zn,xn] and not seen[zn,xn]:seen[zn,xn]=1;q.append((zn,xn))
 sizes.append(n)
assert max(sizes)==390995 and sum(sizes)-max(sizes)==7
cover=np.zeros(m.shape,np.int8)
for s in e['searches']:
 mask=np.zeros(m.shape,bool)
 for z,x0,x1 in e['search_runs'][s['id']]:mask[z-1453,x0-89:x1-88]=1
 assert np.array_equal(mask,r[s['id']]) and not np.any(mask&~m)
 assert int(mask.sum())==s['area'];cover+=mask
assert cover.max()==1
ctx=np.load(a.cache/'context-map.npz');ct=ctx['territory'];cy=ctx['height'];edges=e['edge_witnesses'];assert len(edges)==len({tuple(v[:4]) for v in edges})==1438
for x,z,u,v,dy in edges:
 assert abs(x-u)+abs(z-v)==1 and ct[z-1376,x+800]==2 and ct[v-1376,u+800]==3
 assert abs(int(cy[z-1376,x+800])-int(cy[v-1376,u+800]))==dy
assert sum(v[4]<=1 for v in edges)==1278
contacts={tuple(v[:2]) for v in edges}
for pr in e['probes']:
 path=pr['path'];assert pr['length']==len(path)-1
 for x,z,h in path:assert m[z-1453,x-89] and y[z-1453,x-89]==h
 for u,v in zip(path,path[1:]):assert abs(u[0]-v[0])+abs(u[1]-v[1])==1
 dy=np.diff([v[2] for v in path]);assert pr['ascent']==int(dy[dy>0].sum()) and pr['descent']==int(-dy[dy<0].sum())
 assert pr['max_step']==(int(np.abs(dy).max()) if len(dy) else 0)
 x,z,h=path[0];assert patch[z-1453,x-89]=={'LOW':1,'UPPER':2,'VALLEY':4}[pr['source']]
 x,z,h=path[-1];target=pr['target']
 if target.startswith('P'):assert patch[z-1453,x-89]==int(target[1:])
 elif target=='X03':assert (x,z)==(326,2326)
 else:assert (x,z) in contacts and ((z<1850)==(target=='E-N'))
nodes=read(P/'SETTLEMENT-HIERARCHY.json')['nodes'];assert len(nodes)==4
assert [sum(n['area'][i] for n in nodes) for i in [0,1]]==[29000,47000]
for n in nodes:
 pkg=read(P/('handoff/L2-'+n['id']+'.json'))
 assert pkg['world_write_authorization'] is False and pkg['execution_authorization'] is False
 for k in ['DOWNSTREAM_TO_RESOLVE','DOWNSTREAM_ADAPTABLE','revision_triggers','expected_outputs']:assert pkg[k]
for v in read(P/'visual/maps.json'):
 assert hashlib.sha256((P/'visual'/v['file']).read_bytes()).hexdigest()==v['sha256']
 assert v['pixels_per_block']==1
res=dict(status='MECHANICAL_CHECKS_PASSED_NOT_PLANNING_ACCEPTANCE',independent_rebuild_equal=True,middle_area=int(m.sum()),middle_component_sizes=sorted(sizes,reverse=True),search_area=sum(s['area'] for s in e['searches']),outside_search=int(np.sum(m&(cover==0))),search_overlap=0,boundary=e['boundary'],path_witnesses_checked=len(e['probes']),path_limit='Continuity/height/start/target checked; not an independent optimality proof. Deterministic recomputation agrees.',search_sensitivity=e['search_sensitivity'],built_fabric_range=[29000,47000],territory_fraction=[29000/391002,47000/391002],handoff_count=4,map_count=6,world_reads=0,world_writes=0,builder_calls=0,L2_execution=False)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(res,ensure_ascii=False))
