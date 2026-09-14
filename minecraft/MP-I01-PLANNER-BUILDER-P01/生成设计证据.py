"""MP-I01独立设计产物生成。仅消费BDP-00/01与事实；不调用任何世界写入接口。"""
from pathlib import Path
import json,gzip,hashlib,math,shutil,datetime
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;A=R.parent;P=A/'MP-P05-NORTH-FRONTAGE-ENSEMBLE'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,v):
 p=R/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['sources','evidence','design','previews']:(R/n).mkdir(exist_ok=True)
(R/'.gitattributes').write_text('* -text\n',encoding='utf-8')
bdps=[b for b in load(P/'builder-design-packages.json') if b['id'] in ['BDP-00','BDP-01']];save('sources/handoff.json',bdps)
b=next(b for b in bdps if b['id']=='BDP-01');poly=b['spatial_envelope']
for name,p in [('CIV-001-Canon.md',A/'建筑师/world/civilizations/CIV-001/README.md'),('Architecture-Grammar.md',A/'建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md')]:shutil.copyfile(p,R/'sources'/name)
prov=load(P/'evidence/inherited-world-read-provenance.json');checks={}
for rel,expected in prov['source_and_snapshot_hashes'].items():
 current=sha(Path(prov['source_path'])/rel);assert current==expected['source_sha256'],'Stale source evidence'
 checks[rel]=current
save('evidence/source-check.json',{'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'world_writes':0,'source_path':prov['source_path'],'files':checks,'method':'read hashes, no Minecraft runtime','inherited_timestamp':prov['original_snapshot_utc']})
n=json.loads(gzip.decompress((P/'evidence/near-ground.json.gz').read_bytes()))
n['columns']=[c for c in n['columns'] if 749<=c['x']<=769 and 1622<=c['z']<=1637];n['bounds']=[749,1622,769,1637]
n['block_entities']=[e for e in n['block_entities'] if 749<=e['x']<=769 and 1622<=e['z']<=1637]
(R/'evidence/site-columns.json.gz').write_bytes(gzip.compress(json.dumps(n,separators=(',',':')).encode(),mtime=0));terrain={(c['x'],c['z']):c for c in n['columns']}
def inside(x,z):
 hit=False
 for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1]):
  if (b>z)!=(d>z) and x<(c-a)*(z-b)/(d-b)+a:hit=not hit
 return hit
parcel={(x,z) for x,z in terrain if inside(x+.5,z+.5)}
blocks={};tags={}
def put(x,y,z,s,tag):
 blocks[x,y,z]=s;tags[x,y,z]=tag
def box(x0,y0,z0,x1,y1,z1,s,tag):
 for x in range(x0,x1+1):
  for y in range(y0,y1+1):
   for z in range(z0,z1+1):put(x,y,z,s,tag)
def clear(x0,y0,z0,x1,y1,z1):box(x0,y0,z0,x1,y1,z1,'minecraft:air','intentional_void')
stone='minecraft:stone_bricks';timber='minecraft:stripped_spruce_log[axis=y]';wood='minecraft:spruce_planks';roof='minecraft:deepslate_tiles'
def shell(x0,z0,x1,z1,floor,top,tag):
 # 支承到当前地面下1格；空腔逐体积定义，后续开口再明确穿透。
 for x in range(x0,x1+1):
  for z in range(z0,z1+1):
   gy=terrain[x,z]['ground_y'];box(x,min(gy-1,floor-1),z,x,floor,z,stone,'foundation')
 clear(x0+1,floor+1,z0+1,x1-1,top,z1-1)
 for y in range(floor+1,top+1):
  for x in range(x0,x1+1):
   for z in range(z0,z1+1):
    if x in [x0,x1] or z in [z0,z1]:put(x,y,z,stone,tag)
shell(753,1628,758,1633,131,135,'workshop_wall')
shell(759,1626,766,1631,132,140,'main_wall')
box(760,136,1627,765,136,1630,wood,'upper_floor')
# 屋架和跨梁来自6格内部跨度，不让梁侵入首层3格净高。
box(759,136,1626,766,136,1626,'minecraft:stripped_spruce_log[axis=x]','floor_beam')
box(759,136,1631,766,136,1631,'minecraft:stripped_spruce_log[axis=x]','floor_beam')
for x in [759,766]:
 for z in [1626,1631]:box(x,137,z,x,140,z,timber,'upper_frame')
# 上层较轻填充；实墙区与对应窗口共同决定外观。
for x in range(760,766):
 for z in [1626,1631]:box(x,137,z,x,140,z,'minecraft:terracotta','upper_infill')
for z in range(1627,1631):
 for x in [759,766]:box(x,137,z,x,140,z,'minecraft:terracotta','upper_infill')
# 每个屋面自身有完整覆盖；低翼沿主屋西墙收边，没有悬空拼缝。
for x in range(759,767):
 for z in range(1626,1632):
  y=141+min(z-1626,1631-z);put(x,y,z,f'minecraft:deepslate_tile_stairs[facing={"south" if z<=1628 else "north"},half=bottom,shape=straight,waterlogged=false]','main_roof')
  if x in [759,766]:box(x,141,z,x,y-1,z,'minecraft:terracotta','gable')
for x in range(753,759):
 for z in range(1628,1634):
  y=136+min(z-1628,1633-z);put(x,y,z,f'minecraft:deepslate_tile_stairs[facing={"south" if z<=1630 else "north"},half=bottom,shape=straight,waterlogged=false]','work_roof')
  if x in [753,758]:box(x,136,z,x,y-1,z,stone,'work_gable')
box(760,140,1628,765,140,1628,'minecraft:stripped_spruce_log[axis=x]','roof_tie')
box(762,141,1628,762,142,1628,timber,'king_post')
box(754,135,1630,757,135,1630,'minecraft:stripped_spruce_log[axis=x]','work_tie')
box(755,136,1630,755,137,1630,timber,'work_king_post')
# 南向营业入口与家庭入口分别对接两条搜索段；门扇留在室内。
clear(755,132,1633,756,134,1633)
clear(763,133,1631,764,135,1631)
# 下翼至主屋一个高差：墙体全厚开口、户内短阶。
clear(758,132,1629,759,135,1630)
box(758,132,1629,758,132,1630,'minecraft:stone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]','internal_step')
# 家庭北门绕至私院；主入口至此无需穿过修理空间。
clear(760,133,1626,760,135,1626)
box(760,132,1625,761,132,1625,stone,'rear_landing')
# 单格宽直楼梯，逐步升四格；上层楼板沿整个楼梯切空。
clear(761,136,1627,764,139,1627)
for i,x in enumerate(range(761,765)):
 box(x,133,1627,x,133+i,1627,stone,'stair_support')
 box(x,133+i,1627,x,133+i,1627,'minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]','stair')
# 楼梯井南缘实栏，仅上层区域，首层通行保留。
box(761,137,1628,764,137,1628,'minecraft:spruce_fence[east=true,north=false,south=false,waterlogged=false,west=true]','guard')
# 概念栏杆会影响上层行走，留东端落脚与南排通道；后续保守验证按完整包络。
# 主要窗与地面楼层对齐。
for x in [761,764]:
 box(x,134,1626,x,134,1626,'minecraft:glass','window')
 box(x,138,1631,x,139,1631,'minecraft:glass','window')
for z in [1627,1630]:box(766,138,z,766,139,z,'minecraft:glass','window')
box(753,133,1630,753,134,1631,'minecraft:glass','work_window')
box(754,133,1628,755,134,1628,'minecraft:glass','work_window')
# 私院是现有地形上的连续户内余地：不复制Planner区域mask。
body=({(x,z) for x in range(753,759) for z in range(1628,1634)}|{(x,z) for x in range(759,767) for z in range(1626,1632)})-{(758,1633),(766,1631)}
yard={c for c in parcel if c not in body and (c[0]<=752 or c[1]<=1627)}
for x,z in yard:
 gy=terrain[x,z]['ground_y'];put(x,gy,z,'minecraft:andesite','yard_ground')
# 北侧家庭路径：在自家边界内形成132→131的分段平台。
for x,z in [(759,1625),(758,1625),(758,1626),(757,1626),(757,1627),(756,1627),(755,1627),(754,1627)]:
 if (x,z) in parcel:put(x,terrain[x,z]['ground_y'],z,'minecraft:andesite','rear_path')
put(758,132,1625,'minecraft:stone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]','rear_step')
put(754,131,1627,'minecraft:stone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]','rear_step')
put(758,132,1626,'minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]','rear_step')
for z in range(1629,1635):
 if (751,z) in parcel:put(751,terrain[751,z]['ground_y']+1,z,'minecraft:spruce_fence[east=false,north=true,south=true,waterlogged=false,west=false]','yard_boundary')
if (752,1634) in parcel:put(752,terrain[752,1634]['ground_y']+1,1634,'minecraft:spruce_fence[east=true,north=false,south=false,waterlogged=false,west=true]','yard_boundary')
# 户内门前落脚，不生成公共路线。实际公共对接仍缺handoff。
for x,z,y in [(755,1634,131),(756,1634,131),(763,1632,132),(764,1632,132)]:
 if (x,z) in parcel:put(x,y,z,stone,'threshold_landing')
# 基本使用位置作为独立设计家具体积；不是本轮Finishing。
furniture=[{'id':'WORKBENCH','bounds':[754,132,1629,755,132,1629],'use':'小件修理台','block':'minecraft:crafting_table'}, {'id':'TOOL','bounds':[757,132,1632,757,133,1632],'use':'工具/待修件','block':'minecraft:barrel'}, {'id':'COOK','bounds':[761,133,1630,761,133,1630],'use':'封闭灶具位置/需排烟','block':'minecraft:furnace'}, {'id':'FOOD','bounds':[762,133,1630,762,134,1630],'use':'洁净日需柜','block':'minecraft:barrel'}, {'id':'BED-A','bounds':[760,137,1630,761,137,1630],'use':'休息铺位A','block':'minecraft:red_wool'}, {'id':'BED-B','bounds':[763,137,1630,764,137,1630],'use':'休息铺位B','block':'minecraft:red_wool'}, {'id':'WASTE','bounds':[751,130,1633,751,131,1633],'use':'户内封闭污物暂存，去向待确认','block':'minecraft:barrel'}]
# 排烟有实体井道；灶具不是露天篝火，不假定火焰模拟。
# 以东墙一格厚的烟道实体表达排烟通路，不把它当可通行井筒。
box(766,133,1629,766,144,1629,stone,'flue')
for f in furniture:
 if f['id']=='COOK':f['bounds']=[765,133,1629,765,133,1629]
# 斜地界切去低翼东南角一列；相邻南墙仍闭合，入口不受影响。
for pos in list(blocks):
 if (pos[0],pos[2]) in [(758,1633),(766,1631)]:blocks.pop(pos);tags.pop(pos)
# 模型保留家具作为可开关图层，不挤进Core方块层。
for pos in list(blocks):
 if blocks[pos]=='minecraft:air':continue
 assert (pos[0],pos[2]) in parcel,f'outside parcel column {pos}'
palette=sorted(set(blocks.values()));encoded=[[*p,palette.index(s),tags[p]] for p,s in sorted(blocks.items())]
save('design/voxel-design.json',{'format':'MP-I01 review model; NOT executable canonical construction blueprint','coordinate_system':'Minecraft absolute x,y,z; block volume [x,x+1] etc','world_writes':0,'scope':'BDP-01 / PARCEL-01','state':'DESIGN_REVIEW_READY_WITH_INTERFACE_HOLD','palette':palette,'blocks':encoded,'furniture_program_volumes':furniture,'parcel':poly,'anchor':[753,131,1628],'note':'air encodes intended excavation/portal, not world edits; no executable job produced'})
spaces=[{'id':'S-WORK','bounds':[754,132,1629,757,135,1632],'floor_top':132,'role':'小件接单/修理，4×4净包络'}, {'id':'S-LIVE','bounds':[760,133,1627,765,135,1630],'floor_top':133,'role':'6×4总体生活包络，楼梯/日需占用另扣'}, {'id':'S-SLEEP','bounds':[760,137,1627,765,140,1630],'floor_top':137,'role':'两人寝层，楼梯洞与栏杆另扣'}, {'id':'S-YARD','cells':sorted(yard),'role':'北/西折转家庭小院与户内路径，非公共后巷'}]
edges=[{'id':'E1','from':'TH-01','to':'S-WORK','portal':[755,132,1633],'width':2,'headroom':3,'sequence':'门前短停→较低修理间，公众止于此'}, {'id':'E2','from':'TH-02','to':'S-LIVE','portal':[763,133,1631],'width':2,'headroom':3,'sequence':'较高家庭门→生活间'}, {'id':'E3','from':'S-WORK','to':'S-LIVE','portal':[758,132,1629],'width':2,'rise':1,'sequence':'受控户内短阶；不是公共穿堂'}, {'id':'E4','from':'S-LIVE','to':'S-SLEEP','portal':[761,133,1627],'width':1,'rise':4,'sequence':'北侧单格宽直梯→东落脚→南侧寝层'}, {'id':'E5','from':'S-LIVE','to':'S-YARD','portal':[760,133,1626],'width':1,'sequence':'北门→分段后缘→西院，不穿修理间'}]
save('design/program-space-graph.json',{'users':{'households':1,'people':2,'authority':'BUILDER_DESIGN_ASSUMPTION'},'spaces':spaces,'edges':edges,'furniture':furniture,'important_separation':'营业/家庭分门；日需与封闭污物错时，不宣称外部终端已解决'})
# 方块到简单长方体模型：stairs用两盒，其余作为保守全块。仅用于设计审查。
def boxes(pos,s):
 x,y,z=pos
 if s=='minecraft:air':return []
 if '_stairs' in s:
  upper=(x+.5,y+.5,z,x+1,y+1,z+1)
  if 'facing=north' in s:upper=(x,y+.5,z,x+1,y+1,z+.5)
  if 'facing=south' in s:upper=(x,y+.5,z+.5,x+1,y+1,z+1)
  if 'facing=west' in s:upper=(x,y+.5,z,x+.5,y+1,z+1)
  return [(x,y,z,x+1,y+.5,z+1),upper]
 if 'fence' in s:
  if 'north=true' in s:return [(x+.375,y,z,x+.625,y+1.5,z+1)]
  return [(x,y,z+.375,x+1,y+1.5,z+.625)]
 return [(x,y,z,x+1,y+1,z+1)]
def col(s):
 if 'glass' in s:return (99,146,158)
 if 'deepslate' in s:return (67,76,83)
 if 'terracotta' in s:return (159,125,103)
 if 'spruce' in s:return (106,78,53)
 if s=='minecraft:air':return (240,240,240)
 return (157,156,143)
meshes=[]
for pos,s in blocks.items():
 for q in boxes(pos,s):meshes.append((q,col(s),tags[pos]))
ground=[]
for (x,z),c in terrain.items():ground.append(((x,c['ground_y']-2,z,x+1,c['ground_y']+1,z+1),(117,128,110),'terrain'))
font=lambda s:ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',s)
def render(name,az,el,cut=False):
 im=Image.new('RGB',(2600,1900),'#f5f1e8');d=ImageDraw.Draw(im);a=math.radians(az);e=math.radians(el);faces=[]
 def project(p):
  x,y,z=p[0]-759,p[1]-132,p[2]-1630
  u=x*math.cos(a)-z*math.sin(a);dep=x*math.sin(a)+z*math.cos(a)
  return (1250+u*70,1120+(dep*math.sin(e)-y*math.cos(e))*70,dep*math.cos(e)+y*math.sin(e))
 for q,c,t in ground+meshes:
  if cut and (q[1]>=136 or (t=='main_wall' and q[2]>=1631) or (t=='workshop_wall' and q[2]>=1633)):continue
  x,y,z,X,Y,Z=q;v=[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z),(x,Y,z),(X,Y,z),(X,Y,Z),(x,Y,Z)]
  for idx,light in [([4,5,6,7],1.12),([0,1,5,4],.7),([1,2,6,5],.88),([2,3,7,6],.94),([3,0,4,7],.78)]:
   pts=[project(v[i]) for i in idx];faces.append((sum(p[2] for p in pts)/4,[(p[0],p[1]) for p in pts],tuple(min(255,int(k*light)) for k in c)))
 for _,p,c in sorted(faces,key=lambda f:f[0]):d.polygon(p,fill=c,outline=tuple(max(0,k-18) for k in c))
 d.rectangle((0,0,2600,155),fill='#f5f1e8');d.text((65,28),name,font=font(43),fill='#26383d');d.text((65,90),'MP-I01 · Builder自主设计 · 软件体素预览，非Minecraft截图 · world writes = 0',font=font(26),fill='#43575c')
 d.rectangle((0,1790,2600,1900),fill='#f5f1e8');d.text((65,1810),'低修理翼 + 高生活主屋 / 单格直梯 / 分门进户 / 北西家庭院 / 不含公共道路设计',font=font(29),fill='#43575c')
 im.save(R/f'previews/{name}.png')
render('01-南西侧体量与入口',-35,28)
render('02-北侧家庭院与高差',145,28)
render('03-首层切开空间',-25,58,True)
# 真坐标切层平面；家具和楼梯井显式区分。
im=Image.new('RGB',(2800,1800),'#f5f1e8');d=ImageDraw.Draw(im)
d.text((70,35),'MP-I01｜Plan · 使用与动线分层',font=font(46),fill='#26383d')
for k,(y,title) in enumerate([(133,'首层：工作低一格 / 家庭高一格'),(137,'上层：两人寝层 / 楼梯井与落脚')]):
 ox=100+k*1380;oy=280;sc=61
 def xy(x,z):return(ox+(x-750)*sc,oy+(z-1623)*sc)
 for x,z in parcel:
  px,pz=xy(x,z);d.rectangle((px,pz,px+sc,pz+sc),fill='#dce1d1')
 for (x,by,z),s in blocks.items():
  if by==y and s!='minecraft:air':
   px,pz=xy(x,z);d.rectangle((px,pz,px+sc,pz+sc),fill=col(s),outline='#686c63')
 if k==1:
  for x in range(761,765):
   for z in [1627]:
    px,pz=xy(x,z);d.rectangle((px,pz,px+sc,pz+sc),fill='#e7d0a2');d.line((px,pz,px+sc,pz+sc),fill='#8e784c',width=2)
 for f in furniture:
  x,fy,z,X,Y,Z=f['bounds']
  if (k==0 and fy<136) or (k==1 and fy>=136):
   px,pz=xy(x,z);qx,qz=xy(X+1,Z+1);d.rectangle((px,pz,qx,qz),fill='#be8d70',outline='#523f30',width=2)
 for x in range(750,769,3):px,pz=xy(x,1623);d.text((px,oy-35),str(x),font=font(20),fill='#34464a')
 for z in range(1623,1637,3):px,pz=xy(750,z);d.text((ox-72,pz),str(z),font=font(19),fill='#34464a')
 d.line([xy(*p) for p in poly+[poly[0]]],fill='#345550',width=4)
 d.text((ox,175),title,font=font(29),fill='#34464a')
 d.text((ox,1200),('营业：TH-01 → 低修理间\n家庭：TH-02 → 生活间 → 北门私院\n受控短阶连接两个室内地坪' if k==0 else '寝层地坪顶 Y137；楼梯占北侧单格宽带\n两铺沿南侧；东落脚转入寝层\n梯井栏杆与铺位之间须保留一格通行'),font=font(29),fill='#34464a',spacing=14)
d.text((70,1550),'棕：使用体积，不代表已精修家具；黄斜线：梯井 / 台阶；灰：墙与构造；绿：家庭外部空间\nX向右 / Z向下，北向上；方格1block。图为概念体素切层，实际碰撞仍UNVERIFIED。',font=font(30),fill='#34464a',spacing=15)
im.save(R/'previews/04-双层平面.png')
# 设计剖面沿单格直梯与主屋屋面，表达楼层、净高及支承。
im=Image.new('RGB',(2400,1700),'#f5f1e8');d=ImageDraw.Draw(im);sc=75
def xy(x,y):return(150+(x-751)*sc,1450-(y-128)*sc)
for (x,y,z),s in blocks.items():
 if z==1627 and s!='minecraft:air':
  for a,b,c,A,B,C in boxes((x,y,z),s):
   px,py=xy(a,B);qx,qy=xy(A,b);d.rectangle((px,py,qx,qy),fill=col(s),outline='#5e625a')
for y in range(130,145,2):
 px,py=xy(751,y);d.line((100,py,1650,py),fill='#d2d0c6');d.text((30,py-17),f'Y{y}',font=font(24),fill='#34464a')
d.text((70,30),'Section A｜Z1627 · 主屋直梯与楼层',font=font(44),fill='#26383d')
d.text((1720,330),'地坪顶 Y133\n寝层顶面 Y137\n四格升高 / 单格梯宽\n\n梯井贯穿楼板\n主屋屋脊顶 Y144\n屋顶未用薄单片\n\n屋架 / 石基 / 木楼层\n实际碰撞未验证',font=font(28),fill='#34464a',spacing=15)
d.text((70,1570),'X/Y等比例 · 方块体积剖面，不是结构计算 · 开洞/支承/净空仍需在实施阶段复核',font=font(27),fill='#34464a')
im.save(R/'previews/05-楼梯设计剖面.png')
# 导出可独立旋转的通用OBJ；它不是新的资产registry或施工格式。
lines=['# MP-I01 review mesh, absolute world coordinates, no world-write authorization'];idx=1
for q,c,t in meshes:
 x,y,z,X,Y,Z=q;v=[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z),(x,Y,z),(X,Y,z),(X,Y,Z),(x,Y,Z)]
 lines+=['v '+' '.join(map(str,p)) for p in v]
 for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:lines.append('f '+' '.join(str(idx+i) for i in f))
 idx+=8
(R/'design/review-model.obj').write_text('\n'.join(lines)+'\n',encoding='utf-8')
save('evidence/design-checks.json',{'world_writes':0,'all_design_columns_inside_parent_column_mask':True,'households':1,'people_design_assumption':2,'gross_footprint':82,'interior_envelopes':{'workshop':16,'main_each_level_before_stair_and_furniture':24},'public_lane_geometry':'MISSING_FROM_HANDOFF','external_interface_gate':'HOLD','collision':'UNVERIFIED','architectural_state':'DESIGN_REVIEW_READY_WITH_INTERFACE_HOLD','palette_count':len(palette),'model_blocks_including_air':len(blocks),'excavation':'design air only; not applied','world_read':'hash checks and inherited factual crop only'})
save('sources/source-register.json',{'skill_commit':'0e4cfe2d8bfc66b724c38cd80c5bf59bcd9940ca','read_sources':[{'path':str(p),'sha256':sha(p),'use':u} for p,u in [(P/'builder-design-packages.json','Only BDP-00/01 selected'),(P/'evidence/near-ground.json.gz','Factual site states only'),(P/'evidence/inherited-world-read-provenance.json','Factual source lineage'),(R/'sources/CIV-001-Canon.md','Approved Canon'),(R/'sources/Architecture-Grammar.md','Approved grammar'),(R/'sources/skill/SKILL.md','Current v1.10')]],'forbidden_files_read_this_task':[],'context_isolation':'Previous conversation contains Planner results; none are used as additional design authority. No Planning Packet/Critic/Review or upstream plans opened.'})
print('Generated design',len(blocks),'voxel records; footprint82; world writes0')
