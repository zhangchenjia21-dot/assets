"""读取目标体素，检查通行、六邻域完整性与精确目标状态；不判断回归结论。"""
from pathlib import Path
import numpy as np,json,sys
from collections import deque
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True);n=sys.argv[1];design='--design' in sys.argv;s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=s if design else json.loads((E/(n+'.json')).read_text(encoding='utf8'));P=m['palette'];v=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size']);w,h,d=v.shape
names=[p.split('[')[0].split(':')[1] for p in P];free=np.array([p in ['air','cave_air','short_grass','fern','oxeye_daisy','torch'] for p in names]);air=free[v];solid=np.array([not free[i] and p!='water' and 'leaves' not in p and 'fence' not in p for i,p in enumerate(names)])[v];walk=np.zeros_like(air);walk[:,1:-1,:]=solid[:,:-2,:]&air[:,1:-1,:]&air[:,2:,:]
seen=np.zeros_like(walk);start=(224,65-56,246);q=deque([start]);seen[start]=True
while q:
 x,y,z=q.popleft()
 for a,c in [(x+1,z),(x-1,z),(x,z+1),(x,z-1)]:
  if not(0<=a<w and 0<=c<d):continue
  for b in [y,y-1,y+1]:
   if 0<b<h-2 and walk[a,b,c] and not seen[a,b,c] and (b<=y or air[x,y+2,z]):seen[a,b,c]=True;q.append((a,b,c))
dest={a:{'xyz':[x,y,z],'reachable':bool(seen[x,y-56,z])} for a,x,y,z in s['targets']};routes={r['name']:[p for p in r['cells'] if not seen[p[0],p[1]-56,p[2]]] for r in s['routes']}
heavy=np.array([not free[i] and p!='water' for i,p in enumerate(names)])[v];connected=np.zeros_like(heavy);connected[:,0,:]=heavy[:,0,:]
for it in range(400):
 cnt=connected.sum();near=connected.copy()
 for axis in range(3):
  a=[slice(None)]*3;b=a.copy();a[axis]=slice(1,None);b[axis]=slice(None,-1);near[tuple(a)]|=connected[tuple(b)];near[tuple(b)]|=connected[tuple(a)]
 connected|=near&heavy
 if connected.sum()==cnt:break
orph=np.argwhere(heavy&~connected);states={P[int(p)]:int((v[heavy&~connected]==p).sum()) for p in np.unique(v[heavy&~connected])};rep={'source':'design' if design else 'saved chunks','method':'two-block clearance, adjacent one-block step/jump; six-neighbour heavy geometry; not client physics','destinations':dest,'routes':routes,'orphan_count':len(orph),'orphan_states':states,'orphan_examples':[[int(x),int(y+56),int(z)] for x,y,z in orph[:80]],'micro_previous_solid_changes':s['micro_previous_solid_changes']}
if not design:
 def norm(p):
  if '[' not in p:return p
  a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
 states2=sorted(set(map(norm,P+s['palette'])));ids={p:i for i,p in enumerate(states2)};expected=np.array([ids[norm(p)] for p in s['palette']])[np.load(R/f'阶段{n}.npy')];actual=np.array([ids[norm(p)] for p in P])[v];rep['different_cells']=int((expected!=actual).sum())
prefix=('设计' if design else '实存')+n;(E/(prefix+'-检查.json')).write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');np.save(E/(prefix+'-步行.npy'),seen);print(json.dumps({'unreachable':[a for a,b in dest.items() if not b['reachable']],'blocked_routes':{a:len(b) for a,b in routes.items() if b},'orphan_count':len(orph),'orphan_states':rep['orphan_states'],'different_cells':rep.get('different_cells')},ensure_ascii=False))
