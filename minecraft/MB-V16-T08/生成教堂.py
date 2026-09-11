"""T08 原创 Canonical Blueprint；分阶段保留设计，脚本不直接写游戏文件。"""
from pathlib import Path
import numpy as np,json,math
R=Path(__file__).resolve().parent;A=np.zeros((84,144,160),dtype=np.uint16);pal=['minecraft:air'];ids={pal[0]:0}
def pid(s):
 s=s if ':' in s else 'minecraft:'+s
 if s not in ids:ids[s]=len(pal);pal.append(s)
 return ids[s]
def box(x,y,z,X,Y,Z,s):
 if X<x or Y<y or Z<z:return
 assert 0<=x<=X<160 and 12<=y<=Y<96 and 0<=z<=Z<144,(x,y,z,X,Y,Z)
 A[y-12:Y-11,z:Z+1,x:X+1]=pid(s)
def p(x,y,z,s):box(x,y,z,x,y,z,s)
def stair(s,face):return s.removesuffix('s')+'_stairs[facing='+face+',half=bottom,shape=straight,waterlogged=false]' if s.endswith('_tiles') else s+'_stairs[facing='+face+',half=bottom,shape=straight,waterlogged=false]'
def slab(s):return (s.removesuffix('s') if s.endswith('_tiles') else s)+'_slab[type=bottom,waterlogged=false]'
def line(a,b,s):
 prev=list(a)
 for t in np.linspace(0,1,max(abs(a[i]-b[i]) for i in range(3))*3+1):
  end=[round(a[i]+t*(b[i]-a[i])) for i in range(3)]
  for i in range(3):
   while prev[i]!=end[i]:prev[i]+=1 if end[i]>prev[i] else -1;p(*prev,s)
  p(*end,s)
def export(stage,old):
 d=R/'蓝图'/stage;d.mkdir(parents=True,exist_ok=True);files=[];n=0
 for y in range(0,84,16):
  for z in range(0,144,32):
   for x in range(0,160,32):
    a=A[y:y+16,z:z+32,x:x+32];b=old[y:y+16,z:z+32,x:x+32];yy,zz,xx=np.where(a!=b)
    if not len(xx):continue
    used=sorted(set(map(int,a[yy,zz,xx])));remap={v:i for i,v in enumerate(used)}
    bp={'schema_version':1,'origin':{'x':x,'y':y+12,'z':z},'dimensions':{'x':a.shape[2],'y':a.shape[0],'z':a.shape[1]},'palette':[pal[i] for i in used],'blocks':[[int(i),int(j),int(k),remap[int(v)]] for i,j,k,v in zip(xx,yy,zz,a[yy,zz,xx])],'metadata':{'name':'T08 '+stage,'source_kind':'AI_ORIGINAL','content_omissions':[]}}
    f=f'{x}-{y+12}-{z}.json';(d/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f);n+=len(xx)
 (d/'清单.json').write_text(json.dumps({'stage':stage,'files':files,'blocks':n}),encoding='utf8');np.savez_compressed(R/f'{stage}-方案.npz',blocks=A,palette=pal);print(stage,n,flush=True)

box(0,12,0,159,14,143,'dirt');box(0,15,0,159,15,143,'grass_block[snowy=false]');old=A.copy()
stone='stone_bricks';dress='smooth_sandstone';roof='deepslate_tiles'
def shell(x,z,w,d,h):
 box(x,16,z,x+w,17,z+d,'stone_bricks');box(x,18,z,x+w,h,z+d,stone);box(x+2,18,z+2,x+w-2,h,z+d-2,'air')
def gable_x(x1,x2,zmid,half,eave):
 for z in range(zmid-half,zmid+half+1):
  y=eave+half-abs(z-zmid)
  for x in [x1,x2]:box(x,eave,z,x,y-1,z,stone)
  box(x1-1,y,z,x2+1,y,z,slab(roof) if z==zmid else stair(roof,'south' if z<zmid else 'north'))
def gable_z(z1,z2,xmid,half,eave):
 for x in range(xmid-half,xmid+half+1):
  y=eave+half-abs(x-xmid)
  for z in [z1,z2]:box(x,eave,z,x,y-1,z,stone)
  box(x,y,z1-1,x,y,z2+1,slab(roof) if x==xmid else stair(roof,'east' if x<xmid else 'west'))
# 主教堂：高中央船厅与低侧廊分体，从第一阶段即有屋顶身份。
shell(34,38,94,36,29)
box(34,30,48,128,43,64,stone);box(36,18,49,126,43,63,'air')
gable_x(34,128,56,9,44)
for z in list(range(37,48))+list(range(65,76)):
 y=29+(z-37 if z<48 else 75-z)//2
 box(33,y,z,129,y,z,slab(roof))
 # 側廊截面真实闭合，不形成屋顶下裸露长缝。
 for x in [34,128]:box(x,29,z,x,y,z,stone)
# 耳堂为贯通横向高空间；高屋面从交叉部向两臂延伸。
shell(86,22,18,68,43);gable_z(22,90,95,10,44)
box(87,18,39,103,43,73,'air')
# 重建交叉体开口后的两侧上墙及四个主要承柱。
for x in [86,103]:
 for z in [48,63]:box(x,18,z,x+1,43,z+1,dress)
# 高东端延伸、方形终止；圣坛适度抬一级。
box(110,18,49,126,18,63,'polished_andesite')
for z in [26,77]:shell(104,z,13,13,27);gable_x(104,117,z+6,7,28)
# 收小的交叉钟楼，封顶尖屋面；下方肋顶将独立于屋架。
box(87,44,48,103,59,64,stone);box(89,44,50,101,59,62,'air')
for i in range(9):
 box(86+i,60+i,47+i,104-i,60+i,65-i,slab(roof))
# 西前室有独立低山墙，入口不只是平墙开洞。
shell(24,49,10,14,27);gable_x(24,34,56,8,28)
box(24,18,53,35,24,59,'air')
# 回廊低屋面与开放草庭，北廊和教堂侧门相接。
for x,z,w,d in [(35,76,44,5),(35,81,5,36),(40,112,39,5),(74,81,5,31)]:
 box(x,16,z,x+w,17,z+d,'stone_bricks');box(x,23,z,x+w,23,z+d,'dark_oak_planks')
 for xx,zz in [(x,z),(x+w,z),(x,z+d),(x+w,z+d)]:box(xx,18,zz,xx,22,zz,stone)
 # 回廊瓦顶很低，不与教堂侧廊争高。
 box(x,24,z,x+w,24,z+d,slab(roof))
# 东翼宿舍：下层交通/库房、上层集体睡眠。参事堂另有较低的横向山墙。
shell(80,91,14,35,34);box(81,26,92,93,26,125,'dark_oak_planks');gable_z(91,126,87,8,35)
shell(94,95,21,14,27);gable_x(94,115,102,8,28)
# 门与连接在 Macro 有位置，细化后检查开口逻辑。
for b in [(45,18,73,48,21,77),(78,18,99,96,21,103),(85,18,88,89,21,93),(80,18,117,82,21,121)]:box(*b,'air')
export('01-Macro',old);old=A.copy()

def pointed_open(axis,fixed,mid,width,bottom,spring,rise,depth=1,fill='air'):
 # 两段圆弧近似尖拱，顶点集中；不用矩形洞贴三角装饰。
 r=width/2
 for u in range(-int(r),int(r)+1):
  cap=spring+round(rise*math.sqrt(max(0,1-(abs(u)/max(r,.1)))))
  for dd in range(depth):
   if axis=='x':box(fixed+dd,bottom,mid+u,fixed+dd,cap,mid+u,fill)
   else:box(mid+u,bottom,fixed+dd,mid+u,cap,fixed+dd,fill)
# 中殿侧拱廊，规律性来自跨间结构；唱诗席沿同一结构秩序。
bay_pairs=[(36,46),(46,56),(56,66),(66,76),(76,86),(104,114),(114,126)]
for x1,x2 in bay_pairs:
 mid=(x1+x2)//2
 for z in [48,64]:
  box(x1,18,z-1,x1+1,30,z+1,dress)
  pointed_open('z',z,mid,x2-x1-3,18,26,5,1)
  # 高窗单独在拱廊以上，面向天空而非侧廊阁楼。
  pointed_open('z',z,mid,4,35,39,3,1,'light_gray_stained_glass')
  box(x1,31,z,x1+1,43,z,dress)
# 侧廊外窗与西/东/耳堂主窗。
for mid in [41,51,61,71,81,111,121]:
 for z in [38,73]:pointed_open('z',z,mid,4,21,25,3,2,'light_gray_stained_glass')
for zmid in [52,60]:pointed_open('x',127,zmid,4,25,38,4,2,'light_gray_stained_glass')
pointed_open('x',127,56,3,28,41,3,2,'light_gray_stained_glass')
for z in [22,89]:
 for xmid in [90,95,100]:pointed_open('z',z,xmid,3,27,38,4,2,'light_gray_stained_glass')
for zm in [52,56,60]:pointed_open('x',34,zm,2,35,40,3,2,'light_gray_stained_glass')
pointed_open('x',24,56,6,18,23,5,2)
# 尖拱门套厚度，由外宽内窄构成阴影。
for x in [22,23]:
 box(x,18,51,x,27,61,dress);pointed_open('x',x,56,8 if x==22 else 6,18,23,5)
for x,z in [(108,32),(108,83)]:pointed_open('x',104,z,4,18,22,3,2)
pointed_open('x',94,102,6,18,22,4,2)
# 十字交叉的四道承重尖拱贯通主空间，明确留存四角柱束。
for x in [86,103]:pointed_open('x',x,56,14,18,32,9,2)
for z in [48,63]:pointed_open('z',z,95,14,18,32,9,2)
# 四分肋拱：明确拱腹与屋架空腔，角部柱束接到肋脚。
def vault(x1,x2,z1,z2,spring,rise):
 cx=(x1+x2)/2;cz=(z1+z2)/2;rx=(x2-x1)/2;rz=(z2-z1)/2
 for x in range(x1,x2+1):
  for z in range(z1,z2+1):
   t=max(0,min(1,1-min(abs((x-cx)/rx),abs((z-cz)/rz))))
   y=spring+round(rise*math.sqrt(t));p(x,y,z,'smooth_sandstone')
 # 对角拱肋与横拱用正交体素接缝连接，避免仅角接触。
 for a,b in [((x1,z1),(x2,z2)),((x1,z2),(x2,z1)),((x1,z1),(x1,z2)),((x2,z1),(x2,z2))]:
  prev=None
  for t in np.linspace(0,1,80):
   x=round(a[0]+(b[0]-a[0])*t);z=round(a[1]+(b[1]-a[1])*t)
   y=spring+round(rise*math.sqrt(max(0,min(1,1-min(abs((x-cx)/rx),abs((z-cz)/rz))))))-1
   if prev:line(prev,(x,y,z),'polished_andesite')
   prev=(x,y,z)
for a,b in bay_pairs:vault(a,b,48,64,35,8)
vault(86,104,48,64,35,10)
for a,b in [(24,36),(36,48),(64,76),(76,88)]:vault(86,104,a,b,35,8)
# 柱脚、柱头与北侧外扶壁。半拱跨越侧廊，承压外墩落地。
for x in [36,46,56,66,76,86,104,114,126]:
 for z in [48,64]:
  box(x-1,18,z-1,x+1,19,z+1,'polished_andesite');box(x-1,29,z-1,x+1,30,z+1,dress)
 for z in [35,77]:
  box(x-1,16,z-1,x+1,29,z+1,stone);box(x,30,z,x,32,z,dress)
 for side in [-1,1]:
  for j in range(12):
   z=56+side*(9+j);y=40-round(8*math.sqrt(j/11));box(x,y,z,x,y+1,z,stone)
# 钟楼通风孔；仅检修阁楼，不冒称可游览楼层。
for x in [87,103]:pointed_open('x',x,56,5,52,55,3,1)
for z in [48,64]:pointed_open('z',z,95,5,52,55,3,1)
# 两层宿舍实际折返梯：宽三格、休息平台，逐段净空预留。
box(81,18,115,93,33,125,'air');box(81,26,115,83,26,125,'dark_oak_planks')
for i in range(5):
 box(84+i,18,121,84+i,17+i,124,stone);box(84+i,18+i,121,84+i,18+i,124,stair('stone_brick','east'))
box(89,22,119,92,22,124,'stone_bricks')
for i in range(4):
 box(88-i,18,116,88-i,22+i,118,stone);box(88-i,23+i,116,88-i,23+i,118,stair('stone_brick','west'))
box(81,26,116,84,26,118,'dark_oak_planks')
# 楼上宿舍北端留出夜间交通，只提供楼梯可达，不设置跨空门。
for z in [96,106,115]:
 for x in [80,94]:pointed_open('x',x,z,3,28,30,2,2,'light_gray_stained_glass')
# 回廊庭院侧尖拱列与立柱。
for x in range(41,74,7):
 for z in [81,112]:
  box(x,18,z,x,22,z,dress);box(x,22,z,x+6,22,z,dress);p(x+1,21,z,dress);p(x+5,21,z,dress)
for z in range(83,110,7):
 for x in [40,74]:
  box(x,18,z,x,22,z,dress);box(x,22,z,x,22,z+6,dress);p(x,21,z+1,dress);p(x,21,z+5,dress)
export('02-Meso',old);old=A.copy()
# Meso 实存复核修订：折返平台补齐正交连接，耳堂厚墙贯通小礼拜堂。
box(89,22,116,92,22,118,'stone_bricks')
for z in [32,83]:pointed_open('x',103,z,4,18,22,3,3)
# 入口浅阶与地表只服务建筑；不扩建区域景观。
box(3,15,53,21,15,59,'gravel');box(20,16,52,21,16,60,stair('stone_brick','east'));box(22,17,51,23,17,61,stair('stone_brick','east'))
box(31,15,75,34,15,119,'gravel');box(34,16,115,35,16,118,stair('stone_brick','east'))
box(41,16,82,73,16,111,'dirt');box(41,17,82,73,17,111,'grass_block[snowy=false]')
box(40,17,95,74,17,98,'gravel');box(55,17,81,58,17,112,'gravel')
for x in range(38,85):
 for z in range(40,74):
  if A[5,z,x]==pid('stone_bricks') and (z in [55,56,57] or x%10==6):p(x,17,z,'polished_andesite')
# 简约唱诗座和圣坛明确方向，座列不封堵中央通路。
for x in range(105,118,3):
 for z in [51,61]:p(x,19,z,stair('dark_oak','south' if z==51 else 'north'))
box(122,19,54,124,19,58,'smooth_sandstone');box(123,20,55,123,20,57,slab('smooth_sandstone'))
# 圣坛浅阶在平抬地坪西缘，入口始终畅通。
box(109,18,50,109,18,62,stair('stone_brick','east'))
for x in [39,49,59,69,79]:
 for z in [40,72]:box(x,18,z,x+3,18,z,slab('dark_oak'))
for z in [95,99,103,107,111]:box(89,27,z,92,27,z,'dark_oak_slab[type=bottom,waterlogged=false]')
# 墙脚与檐口在物理构造位置变化，不随机撒材质。
for z in [38,74]:box(34,18,z,85,18,z,'andesite')
for z in [48,64]:
 for a,b in [(34,85),(105,128)]:box(a,44,z,b,44,z,slab('smooth_sandstone'))
for x in [34,128]:
 for z in [38,48,64,74]:box(x,18,z,x,29,z,dress)
# 简约照明使用常规火把；不是用发光填满空间掩盖窗和剖面。
for x,z in [(38,46),(58,46),(78,46),(107,46),(38,66),(58,66),(78,66),(108,67),(83,110),(91,115)]:
 box(x,18,z,x,19,z,'polished_andesite');p(x,20,z,'torch')
for x,z in [(43,84),(67,108)]:p(x,18,z,'short_grass')
export('03-Micro',old)
old=A.copy()
# 屋面交接复核：清除低屋面穿入高空间的瓦片，保留外部泛水接缝。
for x1,x2,z1,z2 in [(88,102,24,88),(82,92,93,124)]:
 for y in range(28,35):
  for z in range(z1,z2+1):
   for x in range(x1,x2+1):
    if 'deepslate' in pal[A[y-12,z,x]]:p(x,y,z,'air')
for y in range(28,35):
 for z in range(93,125):
  if 'deepslate' in pal[A[y-12,z,93]]:p(93,y,z,stone)
for z in [96,106,115]:pointed_open('x',93,z,3,28,30,2,2,'light_gray_stained_glass')
# 侧廊半砖坡面下加连续瓦基层，消除半格的透天空缝。
for z in list(range(37,48))+list(range(65,76)):
 y=29+(z-37 if z<48 else 75-z)//2
 for x1,x2 in [(33,85),(105,129)]:box(x1,y-1,z,x2,y-1,z,roof)
for x in [105,108]:
 for z in [51,61]:p(x,18,z,'dark_oak_planks')
export('04-Repair',old)
(R/'调色板.json').write_text(json.dumps(pal),encoding='utf8')
