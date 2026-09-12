"""T09：依据房间、剖面、支承与明确门口生成增量 Canonical Blueprint。"""
from pathlib import Path
import numpy as np,json,math
R=Path(__file__).resolve().parent;A=np.zeros((56,144,144),dtype=np.uint16);pal=['minecraft:air'];ids={pal[0]:0}
def pid(s):
 s=s if ':' in s else 'minecraft:'+s
 if s not in ids:ids[s]=len(pal);pal.append(s)
 return ids[s]
def box(x,y,z,X,Y,Z,s):
 if X<x or Y<y or Z<z:return
 assert 0<=x<=X<144 and 10<=y<=Y<66 and 0<=z<=Z<144
 A[y-10:Y-9,z:Z+1,x:X+1]=pid(s)
def p(x,y,z,s):box(x,y,z,x,y,z,s)
def stairs(s,f):return s+'_stairs[facing='+f+',half=bottom,shape=straight,waterlogged=false]'
def slab(s):return s+'_slab[type=bottom,waterlogged=false]'
def export(name,prev):
 d=R/'蓝图'/name;d.mkdir(parents=True,exist_ok=True);files=[];total=0
 for y in range(0,56,14):
  for z in range(0,144,24):
   for x in range(0,144,24):
    a=A[y:y+14,z:z+24,x:x+24];b=prev[y:y+14,z:z+24,x:x+24];yy,zz,xx=np.where(a!=b)
    if not len(xx):continue
    used=sorted(set(map(int,a[yy,zz,xx])));remap={v:i for i,v in enumerate(used)}
    bp={'schema_version':1,'origin':dict(x=x,y=y+10,z=z),'dimensions':dict(x=a.shape[2],y=a.shape[0],z=a.shape[1]),'palette':[pal[i] for i in used],'blocks':[[int(i),int(j),int(k),remap[int(v)]] for i,j,k,v in zip(xx,yy,zz,a[yy,zz,xx])],'metadata':{'name':'T09 '+name,'source_kind':'AI_ORIGINAL','content_omissions':[]}}
    f=f'{x}-{y+10}-{z}.json';(d/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f);total+=len(xx)
 (d/'清单.json').write_text(json.dumps({'files':files,'changed':total}),encoding='utf8');np.savez_compressed(R/(name+'.npz'),blocks=A,palette=pal);print(name,total,flush=True)
brick='bricks';plaster='smooth_sandstone';stone='stone_bricks';marble='smooth_quartz';tile='terracotta'
box(0,10,0,143,14,143,'dirt');box(0,15,0,143,15,143,'grass_block[snowy=false]');old=A.copy()
# 地基依每个空间的实际地坪生成，不把全场抬成实体台地。
def floor(x,z,X,Z,y=18,s='smooth_sandstone'):
 box(x,15,z,X,y-1,Z,stone);box(x,y,z,X,y,Z,s)
def walls(x,z,X,Z,base,top):
 box(x,base,z,X,top,z+1,brick);box(x,base,Z-1,X,top,Z,brick);box(x,base,z,x+1,top,Z,brick);box(X-1,base,z,X,top,Z,brick)
def portal(axis,fixed,mid,width,base,spring,depth=2):
 r=width//2
 for u in range(-r,r+1):
  cap=spring+round(math.sqrt(max(0,r*r-u*u)))
  if axis=='z':box(mid+u,base,fixed,mid+u,cap,fixed+depth-1,'air')
  else:box(fixed,base,mid+u,fixed+depth-1,cap,mid+u,'air')
def barrel(x,z,X,Z,spring,rise):
 cz=(z+Z)/2;rz=(Z-z)/2
 for zz in range(z,Z+1):
  h=spring+round(rise*math.sqrt(max(0,1-((zz-cz)/rz)**2)))
  box(x,h,zz,X,h+1,zz,plaster);box(x,h+2,zz,X,h+2,zz,tile)
  for xx in [x,x+1,X-1,X]:box(xx,spring,zz,xx,h,zz,brick)
# 首先建立冷厅承重边墙、三跨拱座与对应拱顶面。
floor(60,46,104,76);walls(60,46,104,76,19,30)
for a,b in [(62,75),(75,89),(89,102)]:
 for x in range(a,b+1):
  for z in range(48,75):
   u=(x-(a+b)/2)/((b-a)/2);v=(z-61)/13
   h=30+round(11*math.sqrt(max(0,1-min(u*u,v*v))))
   box(x,h,z,x,h+1,z,plaster);p(x,h+2,z,tile)
   if x in [62,102]:box(x,30,z,x,h,z,brick)
   if z in [48,74]:box(x,30,z,x,h,z,brick)
 # 拱脚和横向厚墩从基础立起，而非装饰贴在屋顶上。
 for x in [a,b]:
  for z in [48,73]:box(x-1,19,z-1,x+1,30,z+1,plaster)
# 边缘墙体搭接到屋面，不留两格墙厚后的半格漏缝。
for x in range(60,105):
 for z in [46,47,75,76]:box(x,30,z,x,31,z,brick)
# 北更衣房：低筒拱、柜席沿边，南侧两入口分散进入冷厅。
floor(60,26,104,46);walls(60,26,104,46,19,25);barrel(60,26,104,46,25,6)
# 暖室作为低颈，地坪抬高容纳独立热风层。
box(69,16,77,95,16,92,stone)
for x in range(71,95,3):
 for z in range(79,92,3):box(x,17,z,x,19,z,brick)
box(69,20,77,95,20,92,marble);walls(69,77,95,92,21,27);barrel(69,77,95,92,27,6)
# 南热室：圆形鼓座、厚墙和连续双层穹顶，明示径向支承。
cx,cz=82,108
for x in range(64,101):
 for z in range(90,127):
  r=math.hypot(x-cx,z-cz)
  if r<=17:
   p(x,16,z,stone);p(x,20,z,marble)
   if r>=14:box(x,17,z,x,31,z,brick)
   elif x%3==1 and z%3==1:box(x,17,z,x,19,z,brick)
   h=31+round(14*math.sqrt(max(0,1-(r/17)**2)))
   box(x,h,z,x,h+1,z,plaster);p(x,h+2,z,tile)
# 西运动庭院与三面柱廊：梁柱跨距决定屋面，中心露天。
floor(19,35,57,83,17,'sandstone');box(26,17,42,49,17,76,'sand')
for x,z,X,Z in [(19,35,57,41),(19,42,25,83),(26,77,57,83),(51,42,57,76)]:
 box(x,24,z,X,24,Z,'stripped_oak_log[axis=x]');box(x,25,z,X,25,Z,tile)
for x in range(21,58,6):
 for z in [39,79]:box(x,18,z,x,23,z,plaster);box(x-1,23,z,x+1,23,z,marble)
for z in range(45,77,6):
 for x in [23,53]:box(x,18,z,x,23,z,plaster);box(x,23,z-1,x,23,z+1,marble)
# 东侧庭院廊/更衣房接口和北入口独立门廊。
floor(54,29,60,76,18);box(54,25,29,60,25,76,tile)
for z in [30,42,54,66,75]:box(54,19,z,54,24,z,plaster)
floor(73,19,91,26,18);box(73,27,19,91,27,26,tile)
for x in [74,90]:box(x,19,20,x,26,20,plaster);box(x-1,26,19,x+1,26,21,marble)
# 厕间在公众边缘，入口绕开更衣与清水系统。
floor(19,20,38,33,17);walls(19,20,38,33,18,23);barrel(19,20,38,33,23,3)
# 后勤系统有自己的地面和入口：炉房在热区东侧，燃料院在更东侧。
floor(100,96,114,119,16,'stone_bricks');walls(100,96,114,119,17,23);barrel(100,96,114,119,23,4)
floor(105,75,114,95,16,'stone_bricks');box(105,23,75,114,23,95,tile)
floor(115,94,134,120,16,'gravel')
walls(115,94,134,120,17,19)
# 高位蓄水箱只以四墩和平台承托；梯/水路在 Meso 完成。
for x in [108,122]:
 for z in [39,59]:box(x,15,z,x+1,25,z+1,brick)
box(108,26,39,123,26,60,stone);walls(108,39,123,60,27,31)
# 明确门口贯穿接口；四个设计公共连接不靠绕行替代。
portal('z',25,82,6,19,23,3)
for x in [69,95]:portal('z',44,x,6,19,23,6)
portal('x',59,36,4,19,22,4);portal('x',59,61,6,19,24,4)
portal('z',74,82,6,19,24,5);portal('z',90,82,6,21,25,5)
portal('z',31,30,4,18,21,3)
portal('x',112,108,4,17,20,4);portal('x',132,107,4,17,19,3)
portal('z',94,109,4,17,20,4)
# 两级温区门槛与院廊浅阶是房间连接的一部分，提前纳入 Macro。
box(78,19,75,86,19,76,stairs('sandstone','south'));box(78,20,77,86,20,78,stairs('sandstone','south'))
box(56,18,58,59,18,64,stairs('sandstone','east'))
# 冷池和热池各自有底与环壁；Macro 建池，Meso 放水。
def pool(x,z,X,Z,bottom,surface):
 box(x,bottom,z,X,surface,Z,marble);box(x+1,bottom+1,z+1,X-1,surface,Z-1,'air')
pool(65,50,74,57,15,18);pool(90,66,100,73,15,18);pool(74,111,90,119,17,20)
export('01-Macro',old);old=A.copy()
# Gate 有界返工：陡拱壳在体素转译时加竖向接缝，厚鼓座承接穹顶。
for x in range(64,101):
 for z in range(90,127):
  r=math.hypot(x-82,z-108)
  if 14<=r<=17:
   h=31+round(14*math.sqrt(max(0,1-(r/17)**2)))
   box(x,31,z,x,h,z,brick)
for a,b in [(62,75),(75,89),(89,102)]:
 def cap(x,z):return 30+round(11*math.sqrt(max(0,1-min(((x-(a+b)/2)/((b-a)/2))**2,((z-61)/13)**2))))
 for x in range(a,b+1):
  for z in range(48,75):
   h=cap(x,z);n=min(cap(xx,zz) for xx,zz in [(max(a,x-1),z),(min(b,x+1),z),(x,max(48,z-1)),(x,min(74,z+1))])
   box(x,n+1,z,x,h,z,plaster)
# 西更衣门移到池旁实体步行带；旧洞按其墙层恢复。
box(66,19,44,72,26,48,brick);portal('z',44,79,4,19,23,6)
portal('x',112,108,4,17,20,5)
box(54,18,58,55,18,64,stairs('sandstone','east'))
# 两个画布边角区块此前未生成，显式初始化同一测试范围的地面。
old[:6,128:144,0:32]=0
export('01-GateRepair',old);old=A.copy()
# 采光来自窗带和圆热室侧窗，窗洞遵循可解释的半圆开口。
def window(axis,fixed,mid,width,bottom,spring,depth=2):
 r=width//2
 for u in range(-r,r+1):
  cap=spring+round(math.sqrt(max(0,r*r-u*u)))
  if axis=='z':box(mid+u,bottom,fixed,mid+u,cap,fixed+depth-1,'light_gray_stained_glass')
  else:box(fixed,bottom,mid+u,fixed+depth-1,cap,mid+u,'light_gray_stained_glass')
for x in [68,82,96]:window('z',47,x,6,32,35,2);window('z',73,x,6,32,35,2)
window('x',101,61,10,27,33,4)
for x in [65,99]:window('z',26,x,4,21,24,2)
for x in [71,82,93]:
 for z in [98,120]:
  for xx in range(x-2,x+3):
   for zz in range(z-3,z+4):
    if 14<=math.hypot(xx-82,zz-108)<=17:box(xx,24,zz,xx,29,zz,'light_gray_stained_glass')
for z in [103,110]:
 for x in [66,98]:
  for xx in range(x-2,x+3):
   for zz in range(z-2,z+3):
    if 14<=math.hypot(xx-82,zz-108)<=17:box(xx,24,zz,xx,29,zz,'light_gray_stained_glass')
# 庭院柱梁的檐口和内缘承托明确重复跨间。
for x in range(21,58,6):
 for z in [39,79]:box(x-1,18,z-1,x+1,18,z+1,stone)
# 室内低侧墙面有抹灰，门口重新按原意清开，不随机切洞。
for z in [28,44]:box(62,19,z,102,22,z,plaster)
portal('z',44,79,4,19,23,6);portal('z',44,95,6,19,23,6)
for z in [49,73]:
 for a,b in [(64,72),(78,86),(92,100)]:box(a,19,z,b,22,z,plaster)
# 稳定单水位浴池，内设台阶，玩家无需跳坑退出。
for x,z,X,Z,b,s in [(65,50,74,57,15,17),(90,66,100,73,15,17),(74,111,90,119,17,19)]:
 box(x+1,b+1,z+1,X-1,s,Z-1,'water[level=0]')
 box(x+1,s,z+1,x+2,s,z+2,marble)
 box(x+1,s+1,z,x+2,s+1,z,stairs('quartz','south'))
# 公共供水箱与封闭陶管以同高度系统分支表达，不用开放悬空水片。
box(110,27,41,121,29,58,'water[level=0]')
for x in range(101,111):box(x,27,60,x,28,60,'cut_sandstone')
box(102,21,60,103,27,61,'cut_sandstone');p(102,20,61,'chiseled_sandstone')
for z in range(61,110):box(103,17,z,104,17,z,'cut_sandstone')
# 炉膛通过环墙低位炉口送热；热风空腔有独立检修端，不伪装公众楼层。
box(97,17,105,106,19,109,'bricks');box(97,17,106,109,18,108,'air')
box(106,17,106,109,17,108,'magma_block');box(106,18,105,110,21,105,brick)
box(99,21,106,101,38,108,brick);box(100,22,107,100,38,107,'air')
portal('x',104,85,4,17,20,3)
# 维护水箱的直跑阶梯沿东墙；独立落地，不穿越冷厅。
for x in [108,122]:
 box(x,15,49,x+1,25,50,brick)
 for mid in [44,54]:
  for z in range(mid-3,mid+5):
   bottom=21+round(math.sqrt(max(0,16-(z-mid)**2)))
   box(x,bottom,z,x+1,25,z,brick)
for z in [78,86,94]:box(113,17,z,114,22,z+1,brick)
floor(124,39,130,73,16,'gravel')
for i in range(15):
 z=71-i;box(125,17,z,128,16+i,z,stone);box(125,17+i,z,128,17+i,z,stairs('stone_brick','north'))
box(122,31,54,128,31,56,stone);portal('x',122,54,4,30,31,2)
# 前院与北侧短街段，小幅贴地阶梯接入门廊。
floor(53,13,111,18,16,'gravel');floor(70,17,94,19,17,'sandstone')
box(77,16,13,87,16,14,stairs('sandstone','south'))
box(77,17,17,87,17,18,stairs('sandstone','south'));box(77,18,19,87,18,20,stairs('sandstone','south'))
box(26,16,13,33,16,19,'gravel');box(27,17,19,33,17,20,stairs('sandstone','south'))
export('02-Meso',old);old=A.copy()
# 墙面内衬覆盖了三个阈限，按已设计的墙层深度恢复，不改空间组织。
portal('z',25,82,6,19,23,4)
portal('z',44,79,4,19,23,6);portal('z',44,95,6,19,23,6)
portal('z',73,82,6,19,24,6)
box(78,19,75,86,19,76,stairs('sandstone','south'));box(78,20,77,86,20,78,stairs('sandstone','south'))
export('02-JunctionRepair',old);old=A.copy()
# 材料沿构造分布：室内地面边饰、冷厅跨间线，非噪声混材。
for x in range(63,102):
 for z in range(49,74):
  if A[8,z,x]==pid(plaster) and (x in [75,89] or z in [59,63]):p(x,18,z,'polished_diorite')
for x in list(range(63,75))+list(range(90,102)):p(x,19,30,slab('smooth_quartz'))
for x in [62,102]:box(x,19,32,x,19,42,slab('smooth_quartz'))
for x in [64,72,80,88,96]:box(x,20,28,x+3,21,28,'chiseled_sandstone')
# 更衣与冷厅局部照明、暖室座席和热池边缘。
for x,z in [(63,34),(101,34),(64,60),(100,60),(71,83),(93,83),(72,105),(92,105)]:
 p(x,19 if z<77 else 21,z,'chiseled_sandstone')
 p(x,20 if z<77 else 22,z,'torch')
for x in [71,93]:box(x,21,81,x,21,88,slab('smooth_quartz'))
# 厕席与排水槽有明确服务身份；不把污水连到清水箱。
box(21,18,22,36,18,23,'smooth_quartz');box(21,18,29,36,18,30,'smooth_quartz')
for x in [23,27,31,35]:p(x,18,23,'air');p(x,18,29,'air')
box(20,16,22,37,16,30,'stone_bricks');box(21,17,25,36,17,26,'polished_andesite')
# 炉房燃料在后勤院，公众方向不置火；栏杆保护高位维护阶梯。
box(117,17,114,123,19,117,'oak_log[axis=x]')
for i in range(15):
 z=71-i
 for x in [124,129]:box(x,17,z,x,17+i,z,brick);p(x,18+i,z,'sandstone_wall[up=true,east=none,north=low,south=low,west=none,waterlogged=false]')
box(123,32,54,129,32,54,'sandstone_wall[up=true,east=low,north=none,south=none,west=low,waterlogged=false]')
# 前院低告示基座与运动场边坐凳，保持庭院中心净空。
box(92,18,18,94,19,19,'chiseled_sandstone')
for z in [47,59,71]:box(20,18,z,20,18,z+3,slab('sandstone'))
export('03-Micro',old)
old=A.copy()
# 最终使用关系收口：厕间/庭院地坪，后勤院到维护梯，三池出水台阶。
floor(27,33,33,35,17,'sandstone')
floor(125,73,129,94,16,'gravel');floor(134,104,139,110,16,'gravel')
box(139,16,104,139,16,110,stairs('stone_brick','west'))
for x,z,y in [(66,50,18),(91,66,18),(75,111,20)]:box(x,y,z,x+1,y,z,stairs('quartz','north'))
# 引水支线末段从北侧接入高位箱；封闭首端表示本场地之外的供水边界。
for z in [20,28,36]:box(114,15,z,117,26,z+1,brick)
for z in range(19,40):
 p(114,26,z,brick);p(117,26,z,brick)
box(114,27,18,117,30,40,stone);box(115,28,19,116,29,40,'water[level=0]')
box(114,31,18,117,31,40,tile)
# 陈设复核：移除入口上方柜块，侧凳在门口断开；厕席不封闭通道。
box(80,20,28,83,21,28,'air');portal('x',59,36,4,19,22,4)
box(28,18,29,32,18,30,'air');portal('z',93,127,4,17,20,3)
export('04-Repair',old)
(R/'调色板.json').write_text(json.dumps(pal,ensure_ascii=False),encoding='utf8')
