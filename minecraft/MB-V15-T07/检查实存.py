"""独立读取阶段实存快照，分开验证静态水体与近似玩家通行。"""
import numpy as np,json,sys
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存元数据.json').read_text());A=np.fromfile(R/f'证据/{s}-实存方块.u16',dtype='<u2').reshape(m['shape_yzx']);p=m['palette']
water=np.array(['water[' in v for v in p])[A];air=np.array(['air' in v or v=='UNGENERATED' for v in p])[A]
breaches=[];ys,zs,xs=np.where(water)
for y,z,x in zip(ys,zs,xs):
 for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
  if 0<=x+dx<288 and 0<=z+dz<240 and air[y,z+dz,x+dx]:breaches.append([int(x),int(y+12),int(z)])
bedless=[]
for y,z,x in zip(ys,zs,xs):
 if y>0 and air[y-1,z,x]:bedless.append([int(x),int(y+12),int(z)])
visited=np.zeros_like(water);components=[]
for y,z,x in zip(ys,zs,xs):
 if visited[y,z,x]:continue
 q=deque([(int(y),int(z),int(x))]);visited[y,z,x]=True;n=0;lo=[x,y+12,z];hi=lo.copy()
 while q:
  yy,zz,xx=q.popleft();n+=1
  for i,v in enumerate([xx,yy+12,zz]):lo[i]=min(lo[i],v);hi[i]=max(hi[i],v)
  for dy,dz,dx in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
   a,b,c=yy+dy,zz+dz,xx+dx
   if 0<=a<52 and 0<=b<240 and 0<=c<288 and water[a,b,c] and not visited[a,b,c]:visited[a,b,c]=True;q.append((a,b,c))
 components.append({'blocks':n,'min':list(map(int,lo)),'max':list(map(int,hi))})
passable=np.array([any(k in v for k in ['air','short_grass','fern','wheat','carrots','dead_bush','torch']) for v in p])[A]
support=~(passable|water|np.array([any(k in v for k in ['leaves','fence','trapdoor']) for v in p])[A])
walk=np.zeros_like(passable);walk[1:-1]=support[:-2]&passable[1:-1]&passable[2:]
seen=np.zeros_like(walk);q=deque();start=(9,218,243)
for y in range(1,50):
 if walk[y,start[1],start[2]]:q.append((y,start[1],start[2]));seen[y,start[1],start[2]]=True;break
while q:
 y,z,x=q.popleft()
 for dz,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
  xx,zz=x+dx,z+dz
  if not(0<=xx<288 and 0<=zz<240):continue
  for dy in [-1,0,1]:
   yy=y+dy
   if 0<yy<51 and walk[yy,zz,xx] and not seen[yy,zz,xx]:seen[yy,zz,xx]=True;q.append((yy,zz,xx))
targets={'南来道路':(231,20,202),'门前':(178,21,149),'主门':(177,21,139),'院心':(177,21,108),'北厩棚':(158,21,80),'西客房':(145,21,105),'东客房':(207,21,115),'取水台':(118,21,118),'市集':(162,21,166),'工院':(143,21,176),'田间桥':(90,21,168),'屋面':(166,29,134)}
checks={name:{'position':v,'reachable':bool(seen[v[1]-12,v[2],v[0]])} for name,v in targets.items()}
result={'stage':s,'source':'saved-world readback','water':{'blocks':len(xs),'levels':sorted(set(int(y+12) for y in ys)),'lateral_air_breaches':len(breaches),'breach_examples':breaches[:20],'bed_air_gaps':len(bedless),'components':components,'fluid_update_stability':'unverified'},'routes':checks,'route_method':'2-block clearance, cardinal move, one-block height step; voxel approximation, not client playthrough','reachable_cells':int(seen.sum())}
(R/f'证据/{s}-空间检查.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False),flush=True)
