"""本轮原创宫苑 Canonical 分期蓝图；仅生成任务文件，不写 Minecraft。"""
from pathlib import Path
import math,json,gzip,numpy as np
R=Path(__file__).parent;W,H,D=224,64,320;Y0=56;P=[];C=[]
def mat(n,c):P.append('minecraft:'+n);C.append(c);return len(P)-1
air=mat('air',[186,210,220]);stone=mat('stone',[117,119,119]);dirt=mat('dirt',[112,83,56]);grass=mat('grass_block[snowy=false]',[101,137,66]);sand=mat('smooth_sandstone',[217,201,159]);quartz=mat('quartz_block',[232,228,211]);trim=mat('chiseled_sandstone',[196,177,135]);roof=mat('deepslate_tiles',[64,72,82]);glass=mat('light_blue_stained_glass',[124,172,186]);pave=mat('smooth_stone',[165,168,164]);gravel=mat('gravel',[166,158,136]);water=mat('water[level=0]',[66,125,159]);hedge=mat('oak_leaves[distance=1,persistent=true,waterlogged=false]',[59,94,44]);log=mat('oak_log[axis=y]',[103,77,47]);wood=mat('oak_planks',[162,124,77]);podzol=mat('podzol[snowy=false]',[110,89,60]);red=mat('red_tulip',[210,58,52]);white=mat('white_tulip',[239,233,207]);orange=mat('orange_tulip',[235,138,45]);blue=mat('cornflower',[77,107,202]);fern=mat('fern',[86,121,57]);pot=mat('terracotta',[162,98,70]);gold=mat('gold_block',[214,175,55]);slab=mat('smooth_sandstone_slab[type=bottom,waterlogged=false]',[214,201,167]);stairs={f:mat('smooth_sandstone_stairs[facing='+f+',half=bottom,shape=straight,waterlogged=false]',[220,205,168]) for f in ['north','south','east','west']}
V=np.zeros((W,H,D),np.uint8);V[:,:7,:]=dirt;V[:,7,:]=grass;before=V.copy();pools=[];buildings=[];targets=[];trees=[]
def box(x,y,z,X,Y,Z,p):
 if min(x,z)<0 or X>=W or Z>=D or y<Y0 or Y>=Y0+H:raise ValueError(('bounds',x,y,z,X,Y,Z))
 if x<=X and y<=Y and z<=Z:V[x:X+1,y-Y0:Y-Y0+1,z:Z+1]=p
def put(x,y,z,p):box(x,y,z,x,y,z,p)
def ground(z):return 68 if z<=96 else max(64,68-(z-96)) if z<104 else 64 if z<198 else max(62,64-(z-197))
for x in range(W):
 for z in range(D):
  h=ground(z) if 12<=x<=211 and 8<=z<=307 else 63
  box(x,56,z,x,h-2,z,stone);put(x,h-1,z,dirt);put(x,h,z,grass)
  if h<63:box(x,h+1,z,x,63,z,air)
# 规则式平台的低挡土墙与短阶有明确人工整地身份。
for z in range(8,97):
 for x in [12,211]:box(x,63,z,x,68,z,trim)
box(12,64,8,211,68,8,trim)
for z in [96,197]:box(13,ground(z)-2,z,210,ground(z),z,trim)
# 提前形成全部地面路基，不在后期穿透建筑。
def pathrect(x,z,X,Z,p=gravel):
 for zz in range(z,Z+1):box(x,ground(zz),zz,X,ground(zz),zz,p)
pathrect(77,12,147,40);pathrect(104,9,120,76,pave);pathrect(18,74,206,95,pave)
pathrect(106,96,118,307);pathrect(14,101,210,107);pathrect(14,174,210,180);pathrect(14,192,210,197);pathrect(14,296,210,302)
for x in [16,72,148,204]:pathrect(x,101,x+5,301)
for z in range(97,101):box(104,ground(z),z,120,ground(z),z,stairs['north'])
for z in [198,199]:box(104,ground(z),z,120,ground(z),z,stairs['north'])
def pool(name,x,z,X,Z,floor,shape='rect'):
 cells=[];cx=(x+X)/2;cz=(z+Z)/2;rx=(X-x)/2;rz=(Z-z)/2
 for a in range(x,X+1):
  for c in range(z,Z+1):
   inside=True if shape=='rect' else ((a-cx)/rx)**2+((c-cz)/rz)**2<=1
   if inside:cells.append((a,c))
 S=set(cells)
 for a,c in cells:
  edge=any((a+dx,c+dz) not in S for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)])
  box(a,floor-2,c,a,floor,c,trim)
  if not edge:put(a,floor-1,c,water);put(a,floor,c,air)
 pools.append({'name':name,'bounds':[x,floor-2,z,X,floor,Z],'level':floor-1})
pool('平台西镜池',80,79,99,90,68);pool('平台东镜池',125,79,144,90,68)
pool('轴线圆池',99,179,125,191,64,'oval');pool('远端镜渠',103,213,121,288,62)
# 骨架绿墙：高围合园室与内侧隐蔽入口；不阻挡主轴。
for x,X in [(24,67),(157,200)]:
 for z in range(203,263):
  box(x,63,z,x+2,67,z,hedge);box(X-2,63,z,X,67,z,hedge)
 for z in [203,260]:box(x,63,z,X,67,z+2,hedge)
 # 内侧两个入口形成贯通环路，而非盲巷。
 inner=X-1 if x<100 else x+1
 for z in [214,250]:box(inner-2,63,z-2,inner+2,67,z+2,air)
# 修剪树列与绿墙背景：主路径侧列种植有历史园艺原因。
def tree(x,z,h,kind):
 y=ground(z);box(x,y+1,z,x,y+h,z,log)
 for yy in range(y+4,y+h+3):
  r=2 if kind=='column' else max(1,4-abs(yy-(y+h-1))//2)
  for a in range(x-r,x+r+1):
   for c in range(z-r,z+r+1):
    if abs(a-x)+abs(c-z)<=r+2 and V[a,yy-Y0,c]==air:put(a,yy,c,hedge)
 trees.append([x,y,z,h,kind])
for x in [20,203]:
 for i,z in enumerate(range(108,294,16)):tree(x,z,10+(i%3),'column')
for x in [30,44,58,165,179,193]:
 for z in [209,256]:tree(x,z,11+(x%3),'crown')
# 宫殿壳体，中央亭突出，前庭翼部尺度较低。
def shell(name,x,z,X,Z,floor,walltop):
 box(x,floor-2,z,X,floor,Z,trim);box(x,floor+1,z,X,walltop,Z,sand);box(x+1,floor+1,z+1,X-1,walltop-1,Z-1,air)
 if walltop-floor>=14:box(x+1,floor+10,z+1,X-1,floor+10,Z-1,wood)
 for a in range(x-1,X+2):
  for c in range(z-1,Z+2):
   d=min(a-(x-1),(X+1)-a,c-(z-1),(Z+1)-c);yy=walltop+1+round(2*min(d,3)+max(0,d-3)*.5)
   box(a,yy-1,c,a,yy+1,c,roof)
 buildings.append({'name':name,'bounds':[x,floor,z,X,walltop+12,Z],'floor':floor,'top':walltop})
shell('宫殿主体',60,42,164,68,68,84);shell('中央亭',99,37,125,73,68,87);shell('西翼',60,16,73,41,68,78);shell('东翼',151,16,164,41,68,78)
def save(n):
 global before
 folder=R/'蓝图'/n;folder.mkdir(parents=True,exist_ok=True);phases=[];mask=V!=before;total=int(mask.sum())
 for x in range(0,W,32):
  for y in range(0,H,32):
   for z in range(0,D,32):
    sub=mask[x:x+32,y:y+32,z:z+32];q=np.argwhere(sub)
    if not len(q):continue
    blocks=[[int(a),int(b),int(c),int(V[x+a,y+b,z+c])] for a,b,c in q]
    bp={'schema_version':1,'origin':{'x':x,'y':y+Y0,'z':z},'dimensions':{'x':min(32,W-x),'y':32,'z':min(32,D-z)},'palette':P,'blocks':blocks}
    (folder/f'{x}-{y}-{z}.json.gz').write_bytes(gzip.compress(json.dumps(bp,separators=(',',':')).encode(),mtime=0))
    ops=[]
    for a in range(sub.shape[0]):
     for c in range(sub.shape[2]):
      b=0
      while b<sub.shape[1]:
       if not sub[a,b,c]:b+=1;continue
       end=b;p=int(V[x+a,y+b,z+c])
       while end+1<sub.shape[1] and sub[a,end+1,c] and V[x+a,y+end+1,z+c]==p:end+=1
       ops.append([x+a,y+b+Y0,z+c,x+a,y+end+Y0,z+c,p]);b=end+1
    phases.append({'palette':P.copy(),'operations':ops})
 job={'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T06-规则宫苑','phases':phases}
 if n=='01':job.update(create={'type':'superflat','seed':2026091106,'generator_options':{'biome':'minecraft:plains','layers':[{'block':'minecraft:bedrock','height':1},{'block':'minecraft:dirt','height':126},{'block':'minecraft:grass_block','height':1}],'structure_overrides':[],'features':False,'lakes':False}},spawn=[112,69,12])
 (R/'作业').mkdir(exist_ok=True);(R/'作业'/f'{n}.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8');np.save(R/f'阶段{n}.npy',V);before=V.copy();print(n,total,flush=True)
save('01')
# Meso 建筑立面：分层墙脚、窗套、柱式与出檐；统一材料对应构造。
for b in buildings:
 x,y,z,X,_,Z=b['bounds'];t=b['top']
 for yy in [y+1,t,t+1]:box(x-1,yy,z-1,X+1,yy,z-1,quartz);box(x-1,yy,Z+1,X+1,yy,Z+1,quartz)
 for a in range(x+3,X-1,7):
  for c in [z,Z]:
   for yy in [y+3]+([y+12] if t-y>=14 else []):
    if yy+3>t:continue
    box(a-1,yy-1,c,a+2,yy+4,c,trim);box(a,yy,c,a+1,yy+3,c,glass);box(a-1,yy-1,c-1 if c==z else c+1,a+2,yy-1,c-1 if c==z else c+1,slab)
 for a in [x,X]:
  for c in [z,Z]:box(a,y+2,c,a,t,c,quartz)
# 贯通的中央通厅，内部上层连接主翼；只开登记入口。
box(107,69,36,117,75,74,air);box(107,68,36,117,68,74,pave)
for x in [98,125]:box(x,79,47,x+1,83,61,air)
# 中央亭主楼梯，十级与顶层平台相连，楼板开口仅在楼梯包络。
for k in range(10):
 z=46+k;box(102,69+k,z,105,86,z,air);box(102,68,z,105,68+k,z,sand);box(102,69+k,z,105,69+k,z,stairs['south'])
box(102,78,56,106,78,58,wood)
# 宫殿南立面的附壁柱/柱廊与三角山花，强调轴心。
for x in [100,104,120,124]:box(x,69,74,x,84,74,quartz);box(x-1,69,74,x+1,69,75,trim);box(x-1,84,74,x+1,84,75,quartz)
box(99,85,74,125,85,75,quartz)
for yy in range(86,92):
 inset=(yy-86)*2;box(100+inset,yy,74,124-inset,yy,75,quartz)
put(112,92,74,gold)
# 前翼入口与屋内基本可达，不提供不可达封闭楼层。
for x in [73,151]:box(x,69,28,x,73,32,air)
# 支路进入两个园室。
for z in [214,250]:pathrect(64,z-2,77,z+2);pathrect(148,z-2,160,z+2)
for x,X in [(28,63),(161,196)]:box(x,62,207,X,62,258,gravel)
pool('西林丛圆池',35,224,56,245,62,'oval')
for x,z in [(45,217),(45,252)]:box(x-6,63,z,x+6,63,z,slab)
# 东林丛为绿剧场：椭圆草心与两侧短座阶，中央不放第二个同型池。
for x in range(165,194):
 for z in range(219,248):
  q=((x-179)/14)**2+((z-233)/13)**2
  if q<1:put(x,62,z,grass)
for z in [217,215]:box(167,62,z,191,63 if z==217 else 64,z,sand)
# 西附属橘园式屋：单层长窗厅；东园丁房更小，非同体量模板重复。
shell('橘园厅',27,113,59,129,64,74)
for x in range(30,58,6):box(x,66,130,x+2,72,130,quartz);box(x,66,129,x+2,71,129,glass)
box(41,65,128,45,69,130,air);pathrect(40,130,46,173)
shell('园丁房',175,115,194,127,64,71);box(182,65,127,186,68,127,air);pathrect(180,128,187,174)
for x in [178,188]:box(x,66,115,x+2,68,115,glass)
# 通行脚点覆盖轴线、两侧环道、附属屋、隐蔽园室及上层。
targets=[['前庭',112,69,25],['通厅',112,69,55],['宫殿上层',112,79,61],['观园平台',112,69,91],['花坛十字路',112,65,145],['圆池西侧',95,65,185],['西水园',60,63,234],['东绿剧场',179,63,234],['橘园厅',44,65,122],['园丁房',184,65,122],['镜渠终端',112,63,299]]
save('02')
# 四组低篱刺绣花坛：卷曲边界、中心圆纹与成片花带。
for x0 in [81,131]:
 for z0 in [122,156]:
  for x in range(x0-16,x0+17):
   for z in range(z0-13,z0+14):
    if 72<=x<=77 or 148<=x<=153:continue
    u=(x-x0)/15;v=(z-z0)/12;q=u*u+v*v
    if abs(u)<=1 and abs(v)<=1:
     put(x,64,z,gravel)
     curve=abs(q-.55)<.095 or (abs(u)<.07 and abs(v)<.85)
     rim=abs(u)>.92 or abs(v)>.91
     if curve or rim:put(x,65,z,hedge)
     elif q<.9 and q>.14:put(x,64,z,dirt);put(x,65,z,white if z0==122 and x0==81 else red if z0==122 else blue if x0==81 else orange)
# 盆栽庭院与功能花带，保留行走道。
for x in [30,36,50,56]:
 for z in [139,151,163]:
  box(x-1,65,z-1,x+1,65,z+1,pot);box(x,66,z,x,67,z,log)
  box(x-1,68,z-1,x+1,69,z+1,hedge)
for x in [31,54,177,191]:
 for z in range(135,166):
  put(x,64,z,dirt);put(x,65,z,white if x<100 else orange)
# 林丛外缘的林下地表；只在现有草地且有净空处添加，保护前序系统。
for x in range(14,211):
 for z in range(201,296):
  if min(abs(x-20),abs(x-203))<7:
   if V[x,62-Y0,z]==grass:put(x,62,z,podzol)
   if V[x,63-Y0,z]==air and V[x,62-Y0,z]==podzol and (x*7+z*11)%5==0:put(x,63,z,fern)
# 平台矮石栏及间隔花瓶柱，轴向和两侧步阶保持开口。
for x in range(18,207):
 if 103<=x<=121 or 70<=x<=78 or 148<=x<=156:continue
 put(x,69,95,slab)
 if x%9==0:box(x,69,95,x,70,95,quartz);put(x,71,95,pot)
# 主轴圆池中央石雕为有支承几何，非假水柱。
box(111,62,184,113,65,186,trim);box(112,66,185,112,69,185,quartz);put(112,70,185,gold)
save('03')
(R/'场景.json').write_text(json.dumps({'world':'MB-V15-T06-规则宫苑','size':[W,H,D],'y0':Y0,'palette':P,'colors':C,'targets':targets,'pools':pools,'buildings':buildings,'trees':trees,'spawn':[112,69,12]},ensure_ascii=False,indent=2),encoding='utf8')
