"""T11 阶段蓝图；仅生成文件，世界写入仍经公开离线接口。"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parent
stage=sys.argv[1];source=sys.argv[2]
m=json.loads((R/f'证据/{source}-实存.json').read_text(encoding='utf8'))
A=np.fromfile(R/f'证据/{source}.u16',dtype='<u2').reshape(36,96,56).copy();pal=list(m['palette']);ids={v:i for i,v in enumerate(pal)};before=A.copy();ledger=[]
def pid(v):
 v=v if ':' in v else 'minecraft:'+v
 if v not in ids:ids[v]=len(pal);pal.append(v)
 return ids[v]
def box(x,y,z,X,Y,Z,v,why,permission='Allowed'):
 assert 0<=x<=X<56 and 10<=y<=Y<46 and 0<=z<=Z<96
 for yy in range(y,Y+1):
  for zz in range(z,Z+1):
   for xx in range(x,X+1):
    old=pal[A[yy-10,zz,xx]];new=pid(v)
    if A[yy-10,zz,xx]!=new:ledger.append({'at':[xx,yy,zz],'before':old,'after':pal[new],'reason':why,'permission':permission});A[yy-10,zz,xx]=new
def p(x,y,z,v,why,permission='Allowed'):box(x,y,z,x,y,z,v,why,permission)
def slab(v='dark_oak',top=False):return v+'_slab[type='+('top' if top else 'bottom')+',waterlogged=false]'
def chest(x,y,z,face,why):p(x,y,z,'chest[facing='+face+',type=single,waterlogged=false]',why)
def barrel(x,y,z,why):p(x,y,z,'barrel[facing=up,open=false]',why)
def table(x,y,z,X,Z,why):box(x,y,z,X,y,Z,'spruce_planks',why)
def mat(x,z,X,Z,y=17):
 box(x,y,z,X,y,Z,'bamboo_mosaic','洁净席面，保留楼板体积与标高')
 for zz in range(z,Z+1,4):box(x,y,zz,X,y,zz,'birch_planks','席面分缝与边缘')
def lamp(x,y,z,hanging,why):p(x,y,z,'lantern[hanging='+str(hanging).lower()+',waterlogged=false]',why)
if stage=='05-Functional':
 table(14,18,22,20,23,'前店看样与丈量台，避开中央迎客线')
 for x,c in [(14,'blue'),(16,'white'),(18,'red')]:box(x,19,22,x+1,19,22,c+'_wool','受台面支承的三类样布')
 box(14,18,20,16,18,20,'spruce_planks','靠格子侧的备货柜')
 chest(15,19,20,'south','原生空容器，可存经营物品')
 table(14,18,30,16,31,'账房低案');chest(14,18,29,'east','账房文书存放')
 p(15,19,31,'white_carpet','账案纸面转译')
 table(29,18,37,30,40,'取合部检布包装台，主路在西侧')
 box(29,19,38,30,19,39,'white_carpet','摊平检视的未染布');barrel(30,18,41,'包装材料收储')
 mat(15,46,29,50);mat(15,54,29,61)
 table(15,18,47,17,49,'家庭低桌');p(16,19,48,'flower_pot','日常桌上容器转译')
 for x,z in [(14,47),(14,49),(18,47),(18,49)]:p(x,18,z,'blue_carpet','用餐座垫')
 table(29,18,57,30,60,'后座敷靠墙陈列台，中央保持空场')
 p(30,19,58,'flower_pot','安静陈设');p(30,19,60,'white_carpet','收置书卷转译')
 for z in [45,59]:barrel(36,17,z,'厨房备料容器，避开通道')
 table(36,17,46,36,48,'厨房备餐台');p(36,18,47,'flower_pot','备餐小器皿')
 mat(14,20,20,25,23)
 for x in [14,18]:
  box(x,24,21,x+1,24,24,'white_carpet','伙计可收叠铺盖；非原生床')
  box(x,24,21,x+1,24,21,'blue_carpet','铺盖头缘')
 chest(14,24,29,'east','伙计个人储物');chest(20,24,29,'west','伙计共同储物')
 for x in [24,35]:
  for z in [79,85]:box(x,18,z,x,21,z,'spruce_planks','仓储货架竖向承托')
  for y in [18,20]:table(x,y,80,x,84,'仓储层板沿墙组织')
  for z,c in [(80,'blue'),(83,'white')]:p(x,19,z,c+'_wool','架上布包');p(x,21,z,'white_wool','架上包裹')
 chest(27,18,84,'east','库内原生空储物箱');chest(34,18,80,'west','库内原生空储物箱')
 p(28,18,85,'spruce_planks','灯台支承');lamp(28,19,85,False,'库内工作灯，避开箱盖')
elif stage=='06-Architectural':
 # 只处理现有实心面或加附着细构，不挖门、不改屋面。
 for x in list(range(14,19))+[20,28,29,30]:p(x,18,18,slab('spruce',True),'格子下槛局部细分，开口语义不变','Restricted')
 for z in range(45,63):
  if pal[A[8,z,31]]=='minecraft:white_terracotta':p(31,18,z,'dark_oak_planks','居住侧土壁木踢脚')
 for z in range(34,62):
  if pal[A[7,z,37]]=='minecraft:white_terracotta':p(37,17,z,'stone_bricks','土间外墙防潮墙脚')
 for z in range(78,87):
  for x in [23,37]:
   if pal[A[8,z,x]]=='minecraft:white_terracotta':p(x,18,z,'stone_bricks','库墙落地石脚')
 for x in range(13,32):
  for z in [64,65]:
   if pal[A[7,z,x]]=='minecraft:dark_oak_planks':p(x,17,z,'spruce_planks','缘侧清洁木面，保留几何')
 for x in [14,18]:
  for y in range(22,27):
   if pal[A[y-10,17,x]]=='minecraft:air':p(x,y,17,'dark_oak_fence[east=false,north=false,south=false,west=false,waterlogged=false]','布幌吊杆接到现有檐底')
 for x in [14,15,16,17,18]:p(x,21,17,'blue_wool','檐下悬挂布幌；主门不遮挡')
elif stage=='07-Environmental':
 for x,z in [(22,14),(23,14),(24,14),(25,14),(26,14),(24,15),(25,15)]:p(x,16,z,'andesite','门前高频踩踏，保留街面标高')
 for z in [21,22,23,46,47,48,54,55,56,72,73]:p(34,16,z,'mud_bricks','土间受踏实的干燥维护带')
 for z in [50,51,52]:
  for y in [18,19,20]:
   if pal[A[y-10,z,37]]=='minecraft:white_terracotta':p(37,y,z,'brown_terracotta','灶旁局部烟熏，强度受火源限制')
 for x,z in [(13,68),(14,68),(13,69),(17,71),(18,71),(18,72),(30,72)]:p(x,17,z,'azalea','既有苔地中的低灌木，不增加结构树')
 for x,z in [(15,69),(16,69),(16,70),(29,73)]:p(x,17,z,'moss_carpet','庭地低密度苔边')
 for x,z in [(17,34),(18,34),(19,34),(17,35)]:p(x,16,z,'moss_block','小庭背阴地表，保持标高')
 for x,z in [(13,70),(13,71),(30,73)]:p(x,16,z,'mossy_stone_bricks','院墙接地潮湿点')
elif stage=='08-Composition':
 p(29,18,36,'spruce_planks','验货灯台');lamp(29,19,36,False,'庭边验货工作灯')
 p(16,18,31,'spruce_planks','账案灯座');lamp(16,19,31,False,'账目集中照明')
 p(29,18,61,'spruce_planks','座敷单处行灯支座');lamp(29,19,61,False,'夜间后间识别；实际照度待客户端')
 # 只取前台一处暖光，货物色彩仍是焦点。
 lamp(20,19,23,False,'售布台末端照明')
elif stage=='09-Restraint':
 # 本分支须在上一阶段实际视图审查后才执行。
 p(30,19,60,'air','删去座敷重复书卷点，让单处器皿与留白成立')
 box(18,19,22,19,19,22,'red_carpet','整块红布在前店中景抢眼，压低为台上摊开的样布')
else:raise ValueError(stage)
d=R/'蓝图'/stage;d.mkdir(parents=True,exist_ok=True);files=[]
for y in range(0,36,12):
 for z in range(0,96,24):
  for x in range(0,56,24):
   a=A[y:y+12,z:z+24,x:x+24];b=before[y:y+12,z:z+24,x:x+24];yy,zz,xx=np.where(a!=b)
   if not len(xx):continue
   used=sorted(set(map(int,a[yy,zz,xx])));remap={v:i for i,v in enumerate(used)}
   bp={'schema_version':1,'origin':dict(x=x,y=y+10,z=z),'dimensions':dict(x=a.shape[2],y=a.shape[0],z=a.shape[1]),'palette':[pal[i] for i in used],'blocks':[[int(i),int(j),int(k),remap[int(v)]] for i,j,k,v in zip(xx,yy,zz,a[yy,zz,xx])],'metadata':{'name':'T11 '+stage,'source_kind':'AI_ORIGINAL','content_omissions':['容器默认空；铺盖非原生床；道具为方块转译']}}
   f=f'{x}-{y+10}-{z}.json';(d/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f)
(d/'清单.json').write_text(json.dumps({'files':files,'changed':int((A!=before).sum())}),encoding='utf8');np.savez_compressed(R/(stage+'.npz'),blocks=A,palette=pal)
(R/f'证据/{stage}-变更账本.json').write_text(json.dumps({'source':source,'stage':stage,'changes':ledger},ensure_ascii=False,indent=2),encoding='utf8');print(stage,len(ledger))

