"""T11 从房间、柱梁、屋面与接口生成 Core；不包含展示级 Finishing。"""
from pathlib import Path
import numpy as np,json,math
R=Path(__file__).resolve().parent;A=np.zeros((36,96,56),dtype=np.uint16);pal=['minecraft:air'];ids={pal[0]:0}
def pid(s):
 s=s if ':' in s else 'minecraft:'+s
 if s not in ids:ids[s]=len(pal);pal.append(s)
 return ids[s]
def box(x,y,z,X,Y,Z,s):
 if X<x or Y<y or Z<z:return
 assert 0<=x<=X<56 and 10<=y<=Y<46 and 0<=z<=Z<96
 A[y-10:Y-9,z:Z+1,x:X+1]=pid(s)
def p(x,y,z,s):box(x,y,z,x,y,z,s)
def stair(s,f):return s+'_stairs[facing='+f+',half=bottom,shape=straight,waterlogged=false]'
def slab(s):return s+'_slab[type=bottom,waterlogged=false]'
wood='dark_oak_planks';post='stripped_dark_oak_log[axis=y]';wall='white_terracotta';roof='deepslate_tiles'
def floor(x,z,X,Z,y=17,s=wood):box(x,15,z,X,y-1,Z,'stone_bricks');box(x,y,z,X,y,Z,s)
def shell(x,z,X,Z,b,t):
 box(x,b,z,X,t,z,wall);box(x,b,Z,X,t,Z,wall);box(x,b,z,x,t,Z,wall);box(X,b,z,X,t,Z,wall)
def frame(xs,zs,b,t):
 for x in xs:
  for z in zs:box(x,b,z,x,t,z,post)
 for z in zs:box(min(xs),t,z,max(xs),t,z,'stripped_dark_oak_log[axis=x]')
 for x in xs:box(x,t,min(zs),x,t,max(zs),'stripped_dark_oak_log[axis=z]')
def gable(x,z,X,Z,peak,eave):
 c=(z+Z)/2;r=(Z-z)/2
 for zz in range(z,Z+1):
  h=round(peak-(peak-eave)*abs(zz-c)/r);box(x,h-1,zz,X,h,zz,roof)
  for xx in [x+2,X-2]:box(xx,eave-1,zz,xx,h-2,zz,wall)
def portal(axis,fixed,a,b,lo,hi,depth=1):
 if axis=='z':box(a,lo,fixed,b,hi,fixed+depth-1,'air')
 else:box(fixed,lo,a,fixed+depth-1,hi,b,'air')
def export(name,prev):
 d=R/'蓝图'/name;d.mkdir(parents=True,exist_ok=True);files=[]
 for y in range(0,36,12):
  for z in range(0,96,24):
   for x in range(0,56,24):
    a=A[y:y+12,z:z+24,x:x+24];b=prev[y:y+12,z:z+24,x:x+24];yy,zz,xx=np.where(a!=b)
    if not len(xx):continue
    used=sorted(set(map(int,a[yy,zz,xx])));remap={v:i for i,v in enumerate(used)}
    bp={'schema_version':1,'origin':dict(x=x,y=y+10,z=z),'dimensions':dict(x=a.shape[2],y=a.shape[0],z=a.shape[1]),'palette':[pal[i] for i in used],'blocks':[[int(i),int(j),int(k),remap[int(v)]] for i,j,k,v in zip(xx,yy,zz,a[yy,zz,xx])],'metadata':{'name':'T11 '+name,'source_kind':'AI_ORIGINAL','content_omissions':[]}}
    f=f'{x}-{y+10}-{z}.json';(d/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f)
 (d/'清单.json').write_text(json.dumps({'files':files,'changed':int((A!=prev).sum())}),encoding='utf8');np.savez_compressed(R/(name+'.npz'),blocks=A,palette=pal);print(name,int((A!=prev).sum()))
box(0,10,0,55,14,95,'dirt');box(0,15,0,55,15,95,'grass_block[snowy=false]');prev=np.zeros_like(A)
# 北侧短街与清晰地界，院地不被抬为巨大台地。
floor(7,10,47,16,16,'gravel');box(8,16,10,46,16,10,stair('stone_brick','south'))
floor(13,18,31,33);floor(32,18,37,87,16,'packed_mud')
shell(13,18,37,33,18,27);frame([13,19,25,31,37],[18,26,33],18,22)
box(14,23,19,30,23,32,wood);box(14,18,19,30,21,32,'air')
# 梁仍在楼板下；前店不因楼板清空失去必要柱。
frame([13,19,31,37],[18,26,33],18,22)
box(31,17,19,31,22,32,wall);portal('x',31,20,24,18,21)
box(14,18,27,30,21,27,wall);portal('z',27,17,21,18,21);portal('z',27,24,29,18,22)
box(22,24,19,22,27,32,wall);portal('x',22,27,29,24,26)
gable(11,16,39,35,33,27)
# 前店楼梯与目标楼层在 Core 就成立。
box(25,23,24,28,23,30,'air')
for i in range(6):
 z=25+i;box(25,18,z,28,17+i,z,wood);box(25,18+i,z,28,18+i,z,stair('dark_oak','south'))
# 取合部与开敞中庭各自有边界；通り庭贯穿东侧。
floor(13,34,15,64);floor(24,34,31,43);floor(16,34,23,42,16,'gravel')
shell(24,34,31,43,18,23);frame([24,31],[34,43],18,23)
portal('z',33,25,29,18,21,2);portal('z',43,25,29,18,21,2);portal('x',24,37,40,18,21)
box(23,17,37,23,17,40,stair('dark_oak','east'));box(16,17,37,16,17,40,stair('dark_oak','west'))
for x in range(22,33):box(x,24+(x-22)//5,33,x,25+(x-22)//5,44,roof)
# 后部两段居住空间与可见柱梁。
floor(13,44,31,63);shell(13,44,31,63,18,23);frame([13,22,31],[44,52,63],18,23)
box(14,18,52,30,22,52,wall);portal('z',52,19,24,18,21);portal('z',44,25,29,18,21)
portal('x',31,46,49,18,21);portal('z',63,17,27,18,22)
gable(11,42,33,65,30,24)
# 厨房保持挑空，侧屋面与主屋搭接；高处排烟光口由 Core 定义。
box(37,17,34,37,26,61,wall);frame([31,37],[35,43,51,59],17,25)
for x in range(31,40):box(x,29-(x-31)//3,33,x,30-(x-31)//3,62,roof)
box(33,28,48,36,32,52,wall);box(34,28,49,35,32,51,'air');box(32,33,47,37,33,53,roof)
portal('x',33,49,51,30,31);portal('x',36,49,51,30,31)
# 西侧缘侧、柱与低檐随庭院成为串联路线。
for z in [34,42,50,58,64]:box(13,18,z,13,23,z,post)
box(12,24,33,15,24,64,roof)
floor(13,64,31,65);floor(13,66,31,74,16,'gravel')
box(17,17,65,27,17,65,stair('dark_oak','north'))
box(13,16,68,18,16,73,'moss_block');box(26,16,69,30,16,73,'moss_block')
# 独立仓库与厕间，通过东后勤带接近。
floor(23,77,37,87);shell(23,77,37,87,18,24);frame([23,37],[77,87],18,24)
portal('z',77,30,33,18,21);box(29,17,76,34,17,76,stair('stone_brick','south'));gable(21,75,39,89,29,24)
floor(34,64,38,71,16,'stone_bricks');shell(34,64,38,71,17,21);portal('x',34,66,68,17,20);gable(33,63,39,72,23,21)
box(12,16,18,12,20,88,wall);box(39,16,18,39,20,88,wall);box(12,16,88,39,20,88,wall)
portal('z',18,22,26,18,21);box(22,17,17,26,17,18,stair('dark_oak','south'));portal('z',18,33,36,17,21)
# 东土间与后勤路连续，所有横梁保留足够净空。
portal('z',33,32,36,17,22);portal('z',61,32,36,17,22)
export('01-Macro',prev)
prev=A.copy()
# 实存检查发现的三处高差/接地接口，仍在 Core 阶段修复。
floor(33,17,36,17,16,'packed_mud')
box(31,17,20,31,17,24,stair('dark_oak','west'));box(31,17,46,31,17,49,stair('dark_oak','west'))
for x in [18,25]:box(x,18,52,x,23,52,post)
export('02-CoreRepair',prev)
prev=A.copy()
frame([13,19,31,37],[18,26,33],24,27)
fence='dark_oak_fence[east=false,north=false,south=false,west=false,waterlogged=false]'
paperEW='white_stained_glass_pane[east=true,north=false,south=false,west=true,waterlogged=false]'
paperNS='white_stained_glass_pane[east=false,north=true,south=true,west=false,waterlogged=false]'
# 外部格子与低二层通气窗属于建筑身份及采光系统。
for a,b in [(14,18),(20,21),(28,30)]:
 box(a,19,18,b,21,18,fence);box(a,18,18,b,18,18,wood)
for a,b in [(14,18),(24,29)]:box(a,25,18,b,26,18,'birch_fence[east=false,north=false,south=false,west=false,waterlogged=false]')
for x in [21,27]:box(x,18,18,x,22,18,post)
for a,b in [(14,16),(22,23),(29,30)]:box(a,18,27,b,21,27,paperEW)
for a,b in [(14,17),(26,30)]:box(a,18,52,b,21,52,paperEW)
box(24,19,35,24,21,36,paperNS);box(24,19,41,24,21,42,paperNS)
box(13,19,46,13,21,50,paperNS);box(13,19,55,13,21,61,paperNS)
for z in [39,40,41,54,55,56]:p(37,21,z,fence);p(37,22,z,fence)
box(24,21,77,26,22,77,paperEW);box(35,21,77,36,22,77,paperEW)
# 既有屋面上层转为瓦阶，保留下层连续木望板，避免漏缝。
for x,z,X,Z,peak,eave in [(11,16,39,35,33,27),(11,42,33,65,30,24),(21,75,39,89,29,24),(33,63,39,72,23,21)]:
 c=(z+Z)/2;r=(Z-z)/2
 for zz in range(z,Z+1):
  h=round(peak-(peak-eave)*abs(zz-c)/r)
  for xx in range(x,X+1):
   if A[h-10,zz,xx]==pid(roof) and A[h-9,zz,xx]==pid('air'):
    p(xx,h,zz,stair('deepslate_tile','south' if zz<c else 'north'))
    if A[h-11,zz,xx]==pid(roof):p(xx,h-1,zz,wood)
for x in range(12,40):
 if A[24,26,x]==pid('air'):p(x,34,26,slab('deepslate_tile'))
# 卧层梯井围护保留落脚位置；护栏不能封楼梯顶端。
for z in range(24,31):
 for x in [24,29]:p(x,24,z,fence)
for x in range(24,30):p(x,24,23,fence)
export('03-Meso',prev)
prev=A.copy()
# 可使用的基础设施和最低功能照明，不摆展示性货物/家具。
for z in [50,52]:p(36,17,z,'polished_andesite')
p(36,17,51,'furnace[facing=west,lit=false]');p(36,17,55,'water_cauldron[level=3]')
box(27,16,69,29,17,71,'stone_bricks');p(28,17,70,'water[level=0]')
box(35,16,66,37,16,70,wood);p(36,16,69,'oak_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]')
for x,y,z in [(17,21,26),(29,21,33),(21,22,52),(34,24,51),(18,26,26)]:p(x,y,z,'lantern[hanging=true,waterlogged=false]')
export('04-Base',prev)
