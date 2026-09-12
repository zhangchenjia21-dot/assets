"""核对指定空间边、门槛、池体约束和完整性，不输出建筑审美结论。"""
from pathlib import Path
from collections import deque
import numpy as np,json,sys
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(56,144,144);pal=m['palette']
air=np.array([v in ['minecraft:air','minecraft:cave_air','UNGENERATED'] or v.startswith('minecraft:torch') for v in pal])[A];water=np.array([v.startswith('minecraft:water[') for v in pal])[A];solid=~air&~water
walk=np.zeros_like(air);walk[1:-1]=solid[:-2]&air[1:-1]&air[2:]
def edge(a,b,rect):
 loX,hiX,loZ,hiZ=rect;q=deque([tuple(a)]);seen={tuple(a)}
 while q:
  x,y,z=q.popleft()
  if [x,y,z]==b:return {'reachable_via_expected_portal':True,'visited':len(seen)}
  for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
   xx,zz=x+dx,z+dz
   if not(loX<=xx<=hiX and loZ<=zz<=hiZ):continue
   for dy in [-1,0,1]:
    yy=y+dy;p=(xx,yy,zz)
    if not(11<=yy<65) or not walk[yy-10,zz,xx] or p in seen:continue
    if dy:
     sx,sy,sz=(xx,yy-1,zz) if dy>0 else (x,y-1,z);state=pal[A[sy-10,sz,sx]]
     direction={'east':(1,0),'west':(-1,0),'south':(0,1),'north':(0,-1)}
     if '_stairs[' not in state or not any('facing='+f in state and dx*d[0]+dz*d[1]==dy for f,d in direction.items()):continue
    seen.add(p);q.append(p)
 return {'reachable_via_expected_portal':False,'visited':len(seen)}
E=[('北路至门廊',[82,16,11],[82,19,23],[77,87,11,23]),('门廊至更衣',[82,19,23],[82,19,35],[78,86,23,35]),('更衣至冷厅西门',[69,19,40],[69,19,60],[66,72,40,61]),('更衣至冷厅东门',[95,19,40],[95,19,61],[92,98,40,62]),('更衣至西廊',[65,19,36],[56,19,36],[55,66,33,39]),('庭院至冷厅',[49,18,61],[65,19,61],[48,66,58,64]),('冷厅至暖室',[82,19,70],[82,21,84],[78,86,69,85]),('暖室至热室',[82,21,85],[82,21,104],[78,86,84,105]),('服务院至炉房',[124,17,108],[108,17,112],[106,125,103,114]),('炉房至检修廊',[109,17,100],[109,17,84],[106,112,83,101]),('维护梯至水箱平台',[126,17,73],[126,32,55],[124,130,54,74])]
if s!='01-Macro':E[2]=('更衣至冷厅西门',[79,19,40],[79,19,60],[77,81,40,61])
E.extend([('庭院至厕间',[30,18,37],[30,18,27],[27,33,26,38]),('服务街至院门',[141,16,107],[125,17,107],[124,141,104,110]),('服务院至维护梯脚',[127,17,100],[127,17,73],[125,129,72,101])])
out={'stage':s,'edges':{name:{'from':a,'to':b,'restricted_xz':r,**edge(a,b,r)} for name,a,b,r in E},'method':'Restricted expected portal corridor, 2-cell clearance, level walking or correctly oriented stairs. No global detour accepted.'}
seen=np.zeros_like(solid);seen[0]=solid[0];q=deque((0,z,x) for z in range(144) for x in range(144) if solid[0,z,x])
while q:
 y,z,x=q.popleft()
 for dy,dz,dx in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
  yy,zz,xx=y+dy,z+dz,x+dx
  if 0<=yy<56 and 0<=zz<144 and 0<=xx<144 and solid[yy,zz,xx] and not seen[yy,zz,xx]:seen[yy,zz,xx]=True;q.append((yy,zz,xx))
orphan=np.argwhere(solid&~seen);out['orphan_cells']=len(orphan);out['orphan_examples']=[[int(x),int(y+10),int(z),pal[A[y,z,x]]] for y,z,x in orphan[:15]]
leaks=[]
for y,z,x in np.argwhere(water):
 for dy,dz,dx in [(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
  if air[y+dy,z+dz,x+dx]:leaks.append([int(x),int(y+10),int(z)])
out['water']={'cells':int(water.sum()),'side_or_bottom_open_to_air':len(leaks),'examples':leaks[:10],'fluid_update_stability':'unverified; no controlled fluid tick available','logic':'separate contained pools and cistern; no open stepped sources'}
f=R/((('04-Repair' if (R/'04-Repair.npz').exists() else '03-Micro') if s=='reload' else s)+'.npz')
if f.exists():
 e=np.load(f)
 def norm(v):
  if '[' not in v:return v
  a,b=v.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
 allpal=sorted(set(map(norm,pal))|set(map(norm,e['palette'])));ix={v:i for i,v in enumerate(allpal)};act=np.array([ix[norm(v)] for v in pal])[A];exp=np.array([ix[norm(v)] for v in e['palette']])[e['blocks']];out['compared_cells']=int(A.size);out['plan_differences']=int((act!=exp).sum())
(R/f'证据/{s}-核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=True))
