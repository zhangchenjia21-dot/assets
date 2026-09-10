"""对实际保存体素或明确标记的设计体素做通行、接口及完整性观察，不判定回归。"""
from pathlib import Path
import json,numpy as np,sys
from collections import deque
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True);n=sys.argv[1];design='--design' in sys.argv;s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=s if design else json.loads((E/(n+'.json')).read_text(encoding='utf8'));P=m['palette'];V=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size']);w,h,d=V.shape
free=np.array([any('minecraft:'+a==p for a in ['air','cave_air','fern','short_grass','lily_of_the_valley','allium','blue_orchid']) for p in P]);air=free[V];support=np.array([not free[i] and not any(k in p.split('[')[0] for k in ['water','leaves','fence']) for i,p in enumerate(P)])[V];walk=np.zeros_like(air);walk[:,1:-1,:]=support[:,:-2,:]&air[:,1:-1,:]&air[:,2:,:]
spawn=json.loads((R/'作业/01.json').read_text(encoding='utf8'))['spawn'];start=(spawn[0],spawn[1]-56,spawn[2]);seen=np.zeros_like(walk);seen[start]=True;q=deque([start])
while q:
 x,y,z=q.popleft()
 for a,c in [(x-1,z),(x+1,z),(x,z-1),(x,z+1)]:
  if not(0<=a<w and 0<=c<d):continue
  for b in [y,y-1,y+1]:
   if 0<b<h-2 and walk[a,b,c] and not seen[a,b,c] and (b<=y or air[x,y+2,z]):seen[a,b,c]=True;q.append((a,b,c))
targets={a:{'xyz':[x,y,z],'reachable':bool(seen[x,y-56,z])} for a,x,y,z in s['targets']};routes={r['name']:[p for p in r['cells'] if not seen[p[0],p[1]-56,p[2]]] for r in s['routes']}
heavy=np.array([not free[i] and p.split('[')[0]!='minecraft:water' for i,p in enumerate(P)])[V];connected=np.zeros_like(heavy);connected[:,0,:]=heavy[:,0,:]
for it in range(400):
 count=connected.sum();near=connected.copy()
 for axis in range(3):
  a=[slice(None)]*3;b=a.copy();a[axis]=slice(1,None);b[axis]=slice(None,-1);near[tuple(a)]|=connected[tuple(b)];near[tuple(b)]|=connected[tuple(a)]
 connected|=near&heavy
 if connected.sum()==count:break
mask=heavy&~connected;orph=np.argwhere(mask);rep={'source':'design' if design else 'saved chunks','method':'two-block clearance / one-block step or jump; six-neighbour heavy geometry, not client physics','targets':targets,'blocked_routes':routes,'orphans':len(orph),'orphan_states':{P[int(p)]:int((V[mask]==p).sum()) for p in np.unique(V[mask])},'orphan_examples':[[int(x),int(y+56),int(z)] for x,y,z in orph[:100]],'micro_solid_changes':s['micro_solid_changes']}
if not design:
 def norm(p):
  if '[' not in p:return p
  a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
 states=sorted(set(map(norm,P+s['palette'])));ids={p:i for i,p in enumerate(states)};actual=np.array([ids[norm(p)] for p in P])[V];expected=np.array([ids[norm(p)] for p in s['palette']])[np.load(R/f'阶段{n}.npy')];rep['different_cells']=int((actual!=expected).sum())
prefix=('设计' if design else '实存')+n;(E/(prefix+'-检查.json')).write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');np.save(E/(prefix+'-步行.npy'),seen);print(json.dumps({'unreachable':[a for a,b in targets.items() if not b['reachable']],'routes':{a:len(b) for a,b in routes.items() if b},'orphans':rep['orphans'],'orphan_states':rep['orphan_states'],'different_cells':rep.get('different_cells')},ensure_ascii=False))
