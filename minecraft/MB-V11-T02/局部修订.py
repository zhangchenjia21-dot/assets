"""第二、三阶段实存审查后的有界修订：主路重铺、泉槽约束、东缘岩脚。"""
from pathlib import Path
import numpy as np,json,gzip,math
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];V=np.load(R/'阶段3.npy');before=V.copy();W,H,D=V.shape
def m(name):return next(i for i,p in enumerate(P) if p.split('[')[0]=='minecraft:'+name)
def put(x,y,z,p):V[x,y-63,z]=p
def box(x1,y1,z1,x2,y2,z2,p):V[x1:x2+1,y1-63:y2-62,z1:z2+1]=p
pts=[(25,64,194),(43,68,176),(61,76,153),(73,76,153),(85,82,150),(99,86,146),(99,94,110),(99,94,96),(100,96,82),(113,96,81)]
surface={};cells=[]
for i,(a,b) in enumerate(zip(pts,pts[1:])):
 x,y,z=a;X,Y,Z=b;dx,dz=X-x,Z-z;length=dx*dx+dz*dz
 for xx in range(min(x,X)-2,max(x,X)+3):
  for zz in range(min(z,Z)-2,max(z,Z)+3):
   t=max(0,min(1,((xx-x)*dx+(zz-z)*dz)/length));dist=(xx-x-t*dx)**2+(zz-z-t*dz)**2
   if dist<=5.1 and (xx,zz) not in surface or (dist<=5.1 and dist<surface[(xx,zz)][0]):surface[(xx,zz)]=(dist,round(y+(Y-y)*t),dx,dz)
 n=max(abs(dx),abs(dz))
 for j in range(n+1):cells.append([round(x+dx*j/n),round(y+(Y-y)*j/n),round(z+dz*j/n)])
for (x,z),(dist,y,dx,dz) in surface.items():
 box(x,y+1,z,x,y+4,z,0);box(x,max(63,y-3),z,x,y,z,m('cobblestone'));put(x,y,z,m('gravel'))
for (x,z),(dist,y,dx,dz) in surface.items():
 for ax,az,face in [(1,0,'west'),(-1,0,'east'),(0,1,'north'),(0,-1,'south')]:
  if (x+ax,z+az) in surface and surface[(x+ax,z+az)][1]==y-1:
   put(x,y,z,P.index(f'minecraft:stone_brick_stairs[facing={face},half=bottom,shape=straight,waterlogged=false]'));break
# 对角线中心采样的四舍五入可能与投影格标高差一格，记录实际铺面的标高。
cells=[[x,surface[(x,z)][1],z] for x,y,z in cells]
s['routes'][0]={'name':'登山主路（审查后重铺）','points':pts,'cells':cells}
# 原路径与建筑外墙相撞的短支线，改为入口平台，止于西厢既有门洞。
box(100,94,106,104,94,110,m('stone_bricks'));box(100,95,106,104,99,110,0)
# 封闭水槽的侧边与末端，旁边另保留干燥的站立点。
box(172,95,114,172,95,117,m('stone_bricks'));box(174,95,114,174,95,117,m('stone_bricks'));box(173,95,117,173,95,117,m('stone_bricks'))
box(175,94,114,177,94,118,m('stone_bricks'));box(175,95,114,177,98,118,0)
# 岩脚连接台地挡墙和原山坡；三组不同尺度碎岩，避免整面光滑墙直接落草地。
for cx,cz,rx,rz,hh in [(166,86,7,9,9),(172,97,6,8,6),(163,64,9,6,7)]:
 for x in range(cx-rx,cx+rx+1):
  for z in range(cz-rz,cz+rz+1):
   if x<=169 and z>=95:continue
   q=((x-cx)/rx)**2+((z-cz)/rz)**2
   if q<1:
    ids=V[x,:,z];non=np.flatnonzero(ids!=0);ground=int(non[-1])+63
    if int(ids[non[-1]]) not in [m('grass_block'),m('stone'),m('andesite'),m('dirt')]:continue
    if ground>130:continue
    height=int(hh*(1-q))
    if height:box(x,ground,z,x,min(146,ground+height),z,m('andesite'))
diff=V!=before;folder=R/'蓝图/04-主路与泉槽修订';folder.mkdir(exist_ok=True);phases=[];count=0
for x in range(0,W,32):
 for y in range(0,H,32):
  for z in range(0,D,32):
   coords=np.argwhere(diff[x:x+32,y:y+32,z:z+32])
   if not len(coords):continue
   blocks=[[int(a),int(b),int(c),int(V[x+a,y+b,z+c])] for a,b,c in coords]
   bp={'schema_version':1,'origin':{'x':x,'y':y+63,'z':z},'dimensions':{'x':min(32,W-x),'y':min(32,H-y),'z':min(32,D-z)},'palette':P,'blocks':blocks,'metadata':{'task':'MB-V11-T02','stage':'bounded-route-water-rock-revision'}}
   with gzip.open(folder/f'{x}_{y+63}_{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
   phases.append({'palette':P,'operations':[[x+a,y+63+b,z+c,x+a,y+63+b,z+c,p] for a,b,c,p in blocks]});count+=len(blocks)
(R/'作业/04.json').write_text(json.dumps({'world_path':s['world'],'phases':phases,'spawn':[25,65,194]},separators=(',',':')),encoding='utf8');np.save(R/'阶段4.npy',V)
(R/'场景.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8');print(count)
