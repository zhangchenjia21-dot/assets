"""核对 T11 指定局部连接、实体支承及设计读回，不给出建筑质量结论。"""
from pathlib import Path
from collections import deque
import numpy as np,json,sys
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(36,96,56);pal=m['palette']
air=np.array([v in ['minecraft:air','minecraft:cave_air','UNGENERATED'] or v.startswith('minecraft:torch') or 'candle[' in v for v in pal])[A];solid=~air;walk=np.zeros_like(air);walk[1:-1]=solid[:-2]&air[1:-1]&air[2:]
def edge(a,b,r):
 q=deque([tuple(a)]);seen={tuple(a)}
 while q:
  x,y,z=q.popleft()
  if [x,y,z]==b:return True
  for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
   X,Z=x+dx,z+dz
   if not(r[0]<=X<=r[1] and r[2]<=Z<=r[3]):continue
   for dy in [-1,0,1]:
    Y=y+dy;p=(X,Y,Z)
    if not(11<=Y<45) or not walk[Y-10,Z,X] or p in seen:continue
    if dy:
     sx,sy,sz=(X,Y-1,Z) if dy>0 else (x,y-1,z);state=pal[A[sy-10,sz,sx]];direction={'east':(1,0),'west':(-1,0),'south':(0,1),'north':(0,-1)}
     if '_stairs[' not in state or not any('facing='+f in state and dx*d[0]+dz*d[1]==dy for f,d in direction.items()):continue
    seen.add(p);q.append(p)
 return False
E=[('街至店',[24,17,14],[24,18,22],[22,26,14,23]),('街至土间',[34,17,14],[34,17,23],[33,36,14,24]),('店至账房',[18,18,24],[18,18,30],[17,21,23,31]),('账房至取合',[27,18,32],[27,18,38],[25,29,31,39]),('取合至起居',[27,18,39],[27,18,48],[25,29,38,49]),('店至土间',[29,18,22],[34,17,22],[28,35,20,24]),('土间至厨房',[34,17,22],[34,17,49],[32,36,21,50]),('起居至土间',[28,18,47],[34,17,47],[27,35,46,49]),('取合至中庭',[26,18,38],[20,17,38],[19,27,37,40]),('中庭至西缘侧',[20,17,38],[14,18,38],[13,21,37,40]),('起居至座敷',[21,18,49],[21,18,58],[19,24,48,59]),('座敷至后庭',[23,18,60],[23,17,69],[17,27,59,70]),('后路至厕间',[33,17,66],[36,17,67],[32,37,65,69]),('服务路至仓库',[33,17,73],[32,18,81],[30,35,72,82]),('账房梯至二层',[27,18,24],[27,24,31],[25,28,24,31]),('二层至伙计区',[27,24,31],[17,24,28],[14,29,27,32]),('厨房至后路',[34,17,58],[33,17,73],[32,36,57,74])]
out={'stage':s,'edges':{n:{'from':a,'to':b,'restricted_xz':r,'expected_edge':edge(a,b,r)} for n,a,b,r in E}}
seen=np.zeros_like(solid);seen[0]=solid[0];q=deque((0,z,x) for z in range(96) for x in range(56) if solid[0,z,x])
while q:
 y,z,x=q.popleft()
 for dy,dz,dx in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
  Y,Z,X=y+dy,z+dz,x+dx
  if 0<=Y<36 and 0<=Z<96 and 0<=X<56 and solid[Y,Z,X] and not seen[Y,Z,X]:seen[Y,Z,X]=True;q.append((Y,Z,X))
bad=np.argwhere(solid&~seen);out['orphan_cells']=len(bad);out['orphan_examples']=[[int(x),int(y+10),int(z)] for y,z,x in bad[:16]]
def norm(v):
 if '[' not in v:return v
 a,b=v.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
f=R/(s+'.npz')
if f.exists():
 d=np.load(f);actual=np.array(list(map(norm,pal)))[A];expected=np.array(list(map(norm,d['palette'])))[d['blocks']];out['plan_differences']=int((actual!=expected).sum())
(R/f'证据/{s}-核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'stage':s,'failed_edges':[k for k,v in out['edges'].items() if not v['expected_edge']],'orphan_cells':out['orphan_cells'],'plan_differences':out.get('plan_differences')},ensure_ascii=True))
