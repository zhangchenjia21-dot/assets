"""区分方案与实存，以通行、池底池壁、支承和状态对比作有限空间检查。"""
from pathlib import Path
from collections import deque
import numpy as np,json,sys
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True);s=json.loads((R/'场景.json').read_text(encoding='utf8'));n=sys.argv[1];design='--design' in sys.argv
m=s if design else json.loads((E/(n+'.json')).read_text(encoding='utf8'));P=m['palette'];V=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size']);W,H,D=V.shape
base=[p.split('[')[0] for p in P];free=np.array([p in ['minecraft:air','minecraft:cave_air','minecraft:fern','minecraft:red_tulip','minecraft:white_tulip','minecraft:orange_tulip','minecraft:cornflower'] for p in base]);A=free[V];solid=np.array([not free[i] and p!='minecraft:water' for i,p in enumerate(base)])[V];walk=np.zeros_like(A);walk[:,1:-1,:]=solid[:,:-2,:]&A[:,1:-1,:]&A[:,2:,:];seen=np.zeros_like(A);x,y,z=s['spawn'];start=(x,y-s['y0'],z);q=deque([start]);seen[start]=True
while q:
 x,y,z=q.popleft()
 for a,c in [(x-1,z),(x+1,z),(x,z-1),(x,z+1)]:
  if not(0<=a<W and 0<=c<D):continue
  for b in [y,y-1,y+1]:
   if 0<b<H-2 and walk[a,b,c] and not seen[a,b,c] and (b<=y or A[x,y+2,z]):seen[a,b,c]=True;q.append((a,b,c))
targets={name:bool(seen[x,y-s['y0'],z]) for name,x,y,z in s['targets']}
connected=np.zeros_like(solid);connected[:,0,:]=solid[:,0,:]
for k in range(400):
 old=int(connected.sum());near=connected.copy()
 for axis in range(3):
  a=[slice(None)]*3;b=a.copy();a[axis]=slice(1,None);b[axis]=slice(None,-1);near[tuple(a)]|=connected[tuple(b)];near[tuple(b)]|=connected[tuple(a)]
 connected|=near&solid
 if int(connected.sum())==old:break
orph=np.argwhere(solid&~connected);water=np.array([p=='minecraft:water' for p in base])[V];leaks=[];bed=[]
for x,y,z in np.argwhere(water):
 if y==0 or not(solid[x,y-1,z] or water[x,y-1,z]):bed.append([int(x),int(y+56),int(z)])
 for a,c in [(x-1,z),(x+1,z),(x,z-1),(x,z+1)]:
  if not(0<=a<W and 0<=c<D) or not(solid[a,y,c] or water[a,y,c]):leaks.append([int(x),int(y+56),int(z)]);break
rep={'source':'design' if design else 'saved chunks','targets':targets,'orphan_count':len(orph),'orphan_examples':[[int(x),int(y+56),int(z),P[int(V[x,y,z])]] for x,y,z in orph[:30]],'water':{'cells':int(water.sum()),'open_sides':leaks,'unsupported_bed':bed,'levels':sorted(set(int(y+56) for x,y,z in np.argwhere(water))),'fluid_update_stability':'unverified: current official executor has no fluid-update interface'},'method':'two-block clearance; one-block steps/jumps; approximate shape collision; six-neighbour structural connection'}
if not design:
 def norm(p):
  if '[' not in p:return p
  a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
 ids={p:i for i,p in enumerate(sorted(set(map(norm,P+s['palette']))))};a=np.array([ids[norm(p)] for p in P])[V];b=np.array([ids[norm(p)] for p in s['palette']])[np.load(R/f'阶段{n}.npy')];rep['different_cells']=int((a!=b).sum())
prefix=('设计' if design else '实存')+n;(E/(prefix+'-检查.json')).write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');np.save(E/(prefix+'-步行.npy'),seen);print(json.dumps(rep,ensure_ascii=True))
