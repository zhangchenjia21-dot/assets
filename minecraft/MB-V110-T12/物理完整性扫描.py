"""T12 全 Scope 接触与连续包络审计；原生静态形状不等于真实移动实测。"""
from pathlib import Path
import json,numpy as np,math,ast
R=Path(__file__).resolve().parent
import sys
s=sys.argv[1];meta=json.loads((R/f'证据/{s}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(36,96,56);pal=meta['palette'];shapes=json.loads((R/'证据/原生碰撞形状.json').read_text(encoding='utf8'))['shapes']
def state(x,y,z):return pal[A[y-10,z,x]] if 0<=x<56 and 10<=y<46 and 0<=z<96 else 'OUTSIDE'
def boxes(x,y,z):
 v=state(x,y,z)
 if v=='OUTSIDE':return []
 assert v in shapes,v
 return [(x+a,y+b,z+c,x+d,y+e,z+f) for a,b,c,d,e,f in shapes[v]]
def overlap(a,b):return all(a[i]<b[i+3]-1e-7 and a[i+3]>b[i]+1e-7 for i in range(3))
def nearby(bounds):
 for y in range(max(10,math.floor(bounds[1])-1),min(45,math.floor(bounds[4]))+1):
  for z in range(max(0,math.floor(bounds[2])),min(95,math.floor(bounds[5]))+1):
   for x in range(max(0,math.floor(bounds[0])),min(55,math.floor(bounds[3]))+1):
    for b in boxes(x,y,z):yield (x,y,z),b
def body_conflicts(x,y,z):
 body=(x-.3,y+.001,z-.3,x+.3,y+1.8,z+.3)
 return sorted(set(at for at,b in nearby(body) if overlap(body,b)))
def swept_conflicts(p,q):
 # 按先升后移 / 先移后降的保守正交扫掠，覆盖样点之间而非仅看端点。
 x,y,z=p;X,Y,Z=q;regions=[]
 if Y>y:
  regions.append((x-.3,y+.001,z-.3,x+.3,Y+1.8,z+.3))
  regions.append((min(x,X)-.3,Y+.001,min(z,Z)-.3,max(x,X)+.3,Y+1.8,max(z,Z)+.3))
 else:
  regions.append((min(x,X)-.3,y+.001,min(z,Z)-.3,max(x,X)+.3,y+1.8,max(z,Z)+.3))
  regions.append((X-.3,Y+.001,Z-.3,X+.3,y+1.8,Z+.3))
 return sorted({at for region in regions for at,b in nearby(region) if overlap(region,b)})
def travel(name,points):
 # 0.1 格沿整段检查；步升上限 0.6，不接受跳跃越梁/绕行终点。
 foot=points[0][1];trace=[];conflicts=set();steps=[];last=points[0]
 for p,q in zip(points,points[1:]):
  dist=max(abs(q[0]-p[0]),abs(q[2]-p[2]));n=max(1,math.ceil(dist/.1))
  for t in np.linspace(0,1,n+1):
   x=p[0]+(q[0]-p[0])*float(t);z=p[2]+(q[2]-p[2])*float(t);search=(x-.3,foot-.65,z-.3,x+.3,foot+.6,z+.3)
   support=[b[4] for _,b in nearby(search) if b[0]<x+.3-1e-7 and b[3]>x-.3+1e-7 and b[2]<z+.3-1e-7 and b[5]>z-.3+1e-7 and foot-.6-1e-7<=b[4]<=foot+.6+1e-7]
   if not support:steps.append({'at':[round(x,3),round(foot,3),round(z,3)],'reason':'no support within normal step band'});continue
   new=max(support);hits=sorted(set(body_conflicts(x,new,z)+swept_conflicts(last,[x,new,z])));conflicts.update(hits);foot=new;last=[x,new,z]
   trace.append({'feet':[round(x,3),round(foot,3),round(z,3)],'collisions':[list(c) for c in hits]})
 return {'name':name,'start':points[0],'end':points[-1],'sample_count':len(trace),'static_envelope_clear':not conflicts and not steps and abs(foot-points[-1][1])<=.063,'collision_cells':[{'at':list(c),'state':state(*c)} for c in sorted(conflicts)],'unsupported_samples':steps,'end_height':foot,'trace':trace,'movement_status':'UNVERIFIED - no real player step/collision walk-through'}
# 从 Builder 已声明的关系读取节点，不复用其 endpoint 判定结论。
tree=ast.parse((R/'旧模型对照.py').read_text(encoding='utf8'));edges=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='E' for t in n.targets))
routes=[]
for name,a,b,_ in edges:
 p=[a[0]+.5,a[1],a[2]+.5];q=[b[0]+.5,b[1],b[2]+.5]
 if name=='二层至伙计区':points=[p,[23.5,24,31.5],[23.5,24,28.5],q]
 elif name=='厨房至后路':points=[p,[33.5,17,58.5],q]
 elif a[0]!=b[0] and a[2]!=b[2]:points=[p,[p[0],p[1],q[2]],q]
 else:points=[p,q]
 routes.append(travel(name,points))
routes.append(travel('库门左侧踏面横向使用',[[30.5,17.5,76.15],[29.5,17.5,76.15]]))
routes.append(travel('库门右侧踏面横向使用',[[33.5,17.5,76.15],[34.5,17.5,76.15]]))
# 所有同类竖向交通：逐个楼梯串按原生朝向追踪，不只检查声明的中心线。
stairs=[];visited=set()
for y,z,x in np.argwhere(np.array(['_stairs[' in v and 'half=bottom' in v for v in pal])[A]):
 y=int(y+10);x=int(x);z=int(z);v=state(x,y,z);dx,dz=next(d for f,d in [('east',(1,0)),('west',(-1,0)),('south',(0,1)),('north',(0,-1))] if 'facing='+f in v)
 if 'deepslate_tile_stairs' in v or y>24 or (x,y,z) in visited:continue
 if state(x-dx,y-1,z-dz)==v or state(x-dx,y,z-dz)==v:continue
 chain=[];X,Y,Z=x,y,z
 while state(X,Y,Z)==v:
  chain.append((X,Y,Z));visited.add((X,Y,Z));X+=dx;Z+=dz
  if state(X,Y+1,Z)==v:Y+=1
 if not chain:continue
 a=chain[0];b=chain[-1];result=travel('stair lane '+str(a),[[a[0]+.5-dx,a[1],a[2]+.5-dz],[b[0]+.5+dx,b[1]+1,b[2]+.5+dz]])
 if a[2]==76 and a[0] in [29,34]:result['classification']='apron lateral end, not a through-wall route';result['excluded_from_through_route_gate']=True
 stairs.append(result)
# 全部低层墙、柱、框架扫描。高处檐梁/屋脊不是应直接落地的墙脚。
gaps=[];scanned=0;reveals=[]
for z in range(10,90):
 for x in range(7,48):
  for y in range(16,25):
   v=state(x,y,z);upper=state(x,y+1,z)
   wall=('terracotta' in v or '_log[axis=y]' in v) and ('terracotta' in upper or '_log[axis=y]' in upper)
   if not wall:continue
   below=state(x,y-1,z)
   if below==v or 'terracotta' in below or '_log[axis=y]' in below:continue
   scanned+=1
   if below=='minecraft:air' and y<=19:gaps.append({'standing_element':[x,y,z],'gap':[x,y-1,z],'state':v,'below_gap':state(x,y-2,z),'classification':'REQUIRES_INTENT_REVIEW'})
   elif '_slab[' in below and 'type=bottom' in below:gaps.append({'standing_element':[x,y,z],'gap':[x,y-1,z],'state':v,'classification':'PARTIAL_CONTACT_REVIEW'})
  v=state(x,18,z)
  if '_slab[' in v and 'type=top' in v:reveals.append({'at':[x,18,z],'state':v,'classification':'upper slab underside; determine intended sill/reveal from Builder contract'})
for y,z,x in np.argwhere(np.array(['_stairs[' in v and 'deepslate' not in v for v in pal])[A]):
 y=int(y+10);x=int(x);z=int(z)
 if y<=18 and state(x,y-1,z)=='minecraft:air':gaps.append({'standing_element':[x,y,z],'gap':[x,y-1,z],'state':state(x,y,z),'below_gap':state(x,y-2,z),'classification':'STAIR_SUPPORT_REVIEW'})
# 其它小物和边界：凡在低层的原生碰撞实体底部不接触下表面，列出供语义审查。
loose=[]
for y,z,x in np.argwhere(A!=0):
 y=int(y+10);x=int(x);z=int(z);v=state(x,y,z)
 if y<16 or y>25 or not any(k in v for k in ['chest[','flower_pot','azalea','lantern[','_fence[']):continue
 if 'hanging=true' in v:continue
 bb=boxes(x,y,z)
 if not bb:continue
 low=min(b[1] for b in bb);under=boxes(x,y-1,z)
 if not any(b[1]<=low+1e-6 and b[4]>=low-1e-6 for b in under):loose.append({'at':[x,y,z],'state':v,'base':low,'classification':'support or lateral suspension review'})
out={'stage':s,'scope_bounds':[[7,10,10],[47,45,89]],'method':'native state collision boxes + 0.6 x 1.8 body; support sampling <=0.1 blocks plus conservative continuous step/horizontal swept AABBs between samples; step band 0.6; not actual Minecraft movement','wall_bases_examined':scanned,'closure_candidates':gaps,'intentional_reveal_review':reveals,'small_support_review':loose,'routes':routes,'stair_lanes':stairs,'gate':'INITIAL REVIEW REQUIRED' if gaps or any(not r['static_envelope_clear'] and not r.get('excluded_from_through_route_gate') for r in routes+stairs) else 'UNVERIFIED','movement_clearance':'UNVERIFIED'}
(R/f'证据/{s}-物理扫描.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'stage':s,'wall_bases':scanned,'closure_candidate_count':len(gaps),'routes_with_static_conflicts':[{k:r[k] for k in ['name','collision_cells','end_height']} for r in routes if not r['static_envelope_clear']],'stair_lanes_checked':len(stairs),'stair_conflicts':[{k:r[k] for k in ['name','collision_cells','static_envelope_clear']} for r in stairs if not r['static_envelope_clear']],'small_support_review':loose},ensure_ascii=True))
