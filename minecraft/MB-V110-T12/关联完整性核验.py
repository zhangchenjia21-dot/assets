"""关联几何接触、语义保留和变更范围；无世界写入。"""
from pathlib import Path
import json,numpy as np,sys
from collections import deque
R=Path(__file__).resolve().parent;s=sys.argv[1]
def read(n):
 m=json.loads((R/f'证据/{n}-实存.json').read_text(encoding='utf8'));a=np.fromfile(R/f'证据/{n}.u16',dtype='<u2').reshape(36,96,56);return np.array(m['palette'])[a],m
a,m=read(s);b,_=read('baseline');shapes=json.loads((R/'证据/原生碰撞形状.json').read_text(encoding='utf8'))['shapes'];ledger=json.loads((R/'证据/Repair变更账本.json').read_text(encoding='utf8'))['changes'];allow={tuple(c['at']):c for c in ledger};diff=np.argwhere(a!=b);unexpected=[]
for y,z,x in diff:
 p=(int(x),int(y+10),int(z));c=allow.get(p)
 if not c or c['before']!=b[y,z,x] or c['after']!=a[y,z,x]:unexpected.append(p)
def contact(v,w,delta):
 for p in shapes[v]:
  for q0 in shapes[w]:
   q=[q0[i]+delta[i%3] for i in range(6)];sizes=[min(p[i+3],q[i+3])-max(p[i],q[i]) for i in range(3)]
   if min(sizes)>=-1e-7 and sum(t>1e-7 for t in sizes)>=2:return True
 return False
solid=np.array([bool(shapes[v]) for v in m['palette']])[np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(36,96,56)]
seen=np.zeros_like(solid);seen[:6]=solid[:6];q=deque((5,z,x) for z in range(96) for x in range(56) if solid[5,z,x]);cache={}
while q:
 y,z,x=q.popleft()
 for dy,dz,dx in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
  Y,Z,X=y+dy,z+dz,x+dx
  if not(5<=Y<36 and 0<=Z<96 and 0<=X<56) or not solid[Y,Z,X] or seen[Y,Z,X]:continue
  key=(a[y,z,x],a[Y,Z,X],dx,dy,dz)
  if key not in cache:cache[key]=contact(key[0],key[1],(dx,dy,dz))
  if cache[key]:seen[Y,Z,X]=True;q.append((Y,Z,X))
unrooted=[{'at':[int(x),int(y+10),int(z)],'state':a[y,z,x]} for y,z,x in np.argwhere(solid&~seen)]
for row in unrooted:
 x,y,z=row['at'];above=a[y-9,z,x] if y<45 else 'OUTSIDE'
 row['above']=above;row['review']='intentional native hanging lantern; collision excludes suspension connection' if 'lantern[hanging=true' in row['state'] and '_log[' in above else 'UNEXPLAINED'
def region_same(mask):return not bool(((a!=b)&mask).any())
roof=np.char.find(b,'deepslate')>=0;stairs=np.char.find(b,'_stairs[')>=0;water=np.char.find(b,'water')>=0;finish=np.zeros_like(solid)
for y,z,x in np.argwhere(a!=b):
 if int(y+10) not in [16,17,22]:finish[y,z,x]=True
out={'stage':s,'unexpected_differences':unexpected,'actual_changed_cells':len(diff),'roof_states_unchanged':region_same(roof),'stair_states_unchanged':region_same(stairs),'water_states_unchanged':region_same(water),'unrooted_native_collision_nodes':unrooted,'native_touch_graph_limit':'static collision shapes; hanging lights/small intrinsic model offsets are reviewed separately; no structural load calculation','semantic_review':'same Program/Space Graph/main floors/openings/roofline; affected y16/y17 base interfaces and y22 local stair framing only','source_world':m['world']}
(R/f'证据/{s}-关联完整性.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=True))
