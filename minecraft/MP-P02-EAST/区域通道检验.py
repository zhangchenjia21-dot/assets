"""8 格阻力路径作为区域可比证据；不宣称实体可通行或最优工程道路。"""
from pathlib import Path
import heapq,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent;CACHE=ROOT.parents[3]/'MP-P02-cache';p=np.load(CACHE/'regional-natural.npz')
h=p['height'];land=p['land'];art=p['artificial'];H,W=h.shape
def avg(a):return a.reshape(H//8,8,W//8,8).mean((1,3))
ch=avg(h);dry=avg(land==2)==1;clear=avg(art==0)==1
coords={'INTERFACE-01':[350,1600],'NODE-01':[812,1636],'NODE-02':[620,1948],'NODE-03':[1652,2588],'NODE-04':[1188,1988],'ALT-01':[1284,2796]}
def nearest(pt):
 x,z=pt;cx=int((x-256)//8);cz=int((z-1440)//8)
 opts=[(math.dist((x,z),(256+xx*8+4,1440+zz*8+4)),zz,xx) for zz in range(max(0,cz-8),min(ch.shape[0],cz+9)) for xx in range(max(0,cx-8),min(ch.shape[1],cx+9)) if dry[zz,xx] and clear[zz,xx]]
 return min(opts)[1:]
def solve(start,goal,maxgrade):
 a=nearest(coords[start]);b=nearest(coords[goal]);dist={a:0.};prev={};q=[(0.,a)];visited=set()
 while q:
  cost,u=heapq.heappop(q)
  if u in visited:continue
  visited.add(u)
  if u==b:break
  z,x=u
  for dz,dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:
   zz,xx=z+dz,x+dx;v=(zz,xx)
   if not (0<=zz<ch.shape[0] and 0<=xx<ch.shape[1] and dry[v] and clear[v]):continue
   if dx and dz and not (dry[z,xx] and dry[zz,x] and clear[z,xx] and clear[zz,x]):continue
   length=8*math.hypot(dx,dz);grade=abs(float(ch[v]-ch[u]))/length
   if grade>maxgrade:continue
   ncost=cost+length*(1+12*grade*grade)
   if ncost<dist.get(v,float('inf')):dist[v]=ncost;prev[v]=u;heapq.heappush(q,(ncost,v))
 if b not in visited:return {'status':'NO_PATH_IN_THIS_MODEL','grade_cap':maxgrade,'not_proof_of_impossibility':True}
 totalcost=dist[b];cells=[b]
 while cells[-1]!=a:cells.append(prev[cells[-1]])
 cells.reverse();pts=[[256+x*8+4,1440+z*8+4] for z,x in cells];ys=[float(ch[c]) for c in cells]
 length=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]));up=sum(max(0,b-a) for a,b in zip(ys,ys[1:]));down=sum(max(0,a-b) for a,b in zip(ys,ys[1:]))
 # 回读线段每格以暴露聚合模型遗漏的陡阶、水孔与人工材质标记。
 fine=[]
 for a,b in zip(pts,pts[1:]):
  for t in np.linspace(0,1,max(abs(a[0]-b[0]),abs(a[1]-b[1]))+1):
   x=int(round(a[0]+(b[0]-a[0])*t));z=int(round(a[1]+(b[1]-a[1])*t));fine.append((x,z,int(h[z-1440,x-256]),int(land[z-1440,x-256]),int(art[z-1440,x-256])))
 return dict(status='DERIVED_CORRIDOR_ONLY',grade_cap=maxgrade,xz=pts,height_profile=ys,length_blocks=round(length),cumulative_ascent=round(up),cumulative_descent=round(down),height_range=[round(min(ys)),round(max(ys))],max_fine_surface_step=max(abs(b[2]-a[2]) for a,b in zip(fine,fine[1:])),fine_water_samples=sum(a[3]!=2 for a in fine),fine_artificial_samples=sum(a[4]>0 for a in fine),snapped_endpoints=[pts[0],pts[-1]],weighted_cost=round(totalcost),usable_route='UNVERIFIED')
pairs=[('CORRIDOR-01','INTERFACE-01','NODE-01'),('CORRIDOR-02','NODE-01','NODE-02'),('CORRIDOR-03','NODE-01','NODE-03'),('ALTERNATIVE-01','NODE-02','ALT-01')]
out=[]
for id,a,b in pairs:
 modes=[solve(a,b,g) for g in [.25,.5]];out.append(dict(id=id,from_id=a,to_id=b,models=modes,source='R1 exposed_y/land_component/artificial_material',authority='DERIVED'))
 print(id,[(m['status'],m.get('length_blocks'),m.get('cumulative_ascent'),m.get('max_fine_surface_step')) for m in modes])
(ROOT/'evidence/corridor-models.json').write_text(json.dumps(dict(method='Dijkstra on 8-block mean exposed_y; all64columns east land and no artificial flag; 8-neighbour, no diagonal water corner cutting; cost=length*(1+12*grade^2); grade caps .25/.5 are analysis assumptions',limitations='非历史原路、非驮畜/玩家碰撞模型，均值掩盖陡阶；路径仅供下层勘察。不存在路径也不证明工程不可行。',coordinates=coords,corridors=out),ensure_ascii=False,indent=2),encoding='utf8')
old_a=solve('NODE-01','NODE-04',.5);old_b=solve('NODE-04','NODE-03',.5);direct=out[2]['models'][1]
(ROOT/'evidence/direct-remote-comparison.json').write_text(json.dumps({'authority':'DERIVED','rejected_service_candidate_xz':coords['NODE-04'],'via_service_length':old_a['length_blocks']+old_b['length_blocks'],'direct_length':direct['length_blocks'],'extra_length':old_a['length_blocks']+old_b['length_blocks']-direct['length_blocks'],'decision':'固定暂歇点因绕行代价且无独立需求而撤销；不再列入主链','old_legs':[old_a,old_b],'direct_model_ref':'corridor-models.json#CORRIDOR-03/models/1'},ensure_ascii=False,indent=2),encoding='utf8')
