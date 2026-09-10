"""从实存导出检查路线、支承与连通几何；结果是工程观察，不是回归判定。"""
from pathlib import Path
import numpy as np,json,sys
from collections import deque
R=Path(__file__).parent;E=R/'证据';n=sys.argv[1];s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=json.loads((E/f'阶段{n}.json').read_text(encoding='utf8'));P=m['palette'];V=np.fromfile(E/f'阶段{n}.bin',np.uint8).reshape(m['size']);W,H,D=V.shape;y0=m['y0']
names=[p.split('[')[0].split(':')[1] for p in P];empty=np.array([a in ['air','cave_air','void_air','short_grass','fern','wheat','poppy','oxeye_daisy','torch'] for a in names]);passage=empty[V];support=np.array([not empty[i] and a!='water' and 'leaves' not in a and 'fence' not in a for i,a in enumerate(names)])[V]
walk=np.zeros_like(passage);walk[:,1:-1,:]=support[:,:-2,:]&passage[:,1:-1,:]&passage[:,2:,:];start=json.loads((R/'作业/01.json').read_text(encoding='utf8'))['spawn'];start=(start[0],start[1]-y0,start[2]);seen=np.zeros_like(walk);seen[start]=True;q=deque([start]);total=0
while q:
 x,y,z=q.popleft();total+=1
 for a,c in [(x+1,z),(x-1,z),(x,z+1),(x,z-1)]:
  if not(0<=a<W and 0<=c<D):continue
  for b in [y,y+1,y-1]:
   if 0<b<H-1 and walk[a,b,c] and not seen[a,b,c] and (b<=y or passage[x,y+2,z]):seen[a,b,c]=True;q.append((a,b,c))
dest={}
np.save(E/f'阶段{n}-步行mask.npy',seen)
for d in s['doors']:
 x,y,z=d['inside'];dest[d['name']]={'xyz':d['inside'],'reachable':bool(seen[x,y-y0,z])}
for name,(x,y,z) in {'桥中':(144,69,143),'庄园上层':(77,88,43),'磨坊上层':(170,73,89)}.items():dest[name]={'xyz':[x,y,z],'reachable':bool(seen[x,y-y0,z])}
roads={}
for r in s['routes']:
 bad=[]
 for x,y,z in r['cells']:
  if not(passage[x,y+1-y0,z] and passage[x,y+2-y0,z]):bad.append([x,y,z])
 roads[r['name']]={'samples':len(r['cells']),'blocked':bad}
footings={}
for name,x,z,X,Z,y,*_ in s['homes']+s['facilities']:
 footings[name]={'air_below_declared_floor':int(passage[x:X+1,y-1-y0,z:Z+1].sum())}
# 六邻域用于识别孤立体；对角接触的枝杈需人工区分，不将水、细草、火把纳入重型几何。
heavy=np.array([not empty[i] and a!='water' for i,a in enumerate(names)])[V];connected=np.zeros_like(heavy);connected[:,0,:]=heavy[:,0,:]
# 单调传播从土层出发，覆盖石体、墙、梁、木桩和树冠。
for iteration in range(250):
 oldcount=int(connected.sum());near=connected.copy()
 for axis in range(3):
  lo=[slice(None)]*3;hi=lo.copy();lo[axis]=slice(1,None);hi[axis]=slice(None,-1);near[tuple(lo)]|=connected[tuple(hi)];near[tuple(hi)]|=connected[tuple(lo)]
 connected|=near&heavy
 if int(connected.sum())==oldcount:break
orphans=np.argwhere(heavy&~connected);orphan_states={}
for p in np.unique(V[heavy&~connected]):orphan_states[P[int(p)]]=int((V[heavy&~connected]==p).sum())
rep={'method':'两格净空、实体支承、一格台阶或跳步；不模拟客户端物理。重型几何采用六邻域从底层传播，含树冠、石体、墙及桥。','reachable_cells':total,'destinations':dest,'routes':roads,'floor_contact':footings,'integrity':{'iterations':iteration+1,'unconnected_voxels':len(orphans),'states':orphan_states,'examples':[[int(x),int(y+y0),int(z)] for x,y,z in orphans[:60]]}}
(E/f'阶段{n}-几何检查.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'unreachable':[k for k,v in dest.items() if not v['reachable']],'blocked_routes':{k:len(v['blocked']) for k,v in roads.items() if v['blocked']},'unconnected_voxels':len(orphans),'orphan_states':orphan_states},ensure_ascii=False),flush=True)
