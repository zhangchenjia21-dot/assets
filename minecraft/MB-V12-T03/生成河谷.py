"""独立 T03：只生成任务蓝图和作业，不直接访问游戏存档。"""
from pathlib import Path
import numpy as np,json,gzip,math
R=Path(__file__).parent; W=D=256;Y0=56;H=80
P=['minecraft:air'];C=[[178,205,221]]
def material(name,color):
 state='minecraft:'+name
 if state in P:return P.index(state)
 P.append(state);C.append(color);return len(P)-1
air=0;grass=material('grass_block[snowy=false]',[104,132,67]);dirt=material('dirt',[124,91,59]);stone=material('stone',[130,129,124]);chalk=material('calcite',[191,189,174]);gravel=material('gravel',[157,147,124]);mud=material('mud',[99,98,88]);coarse=material('coarse_dirt',[117,89,57]);cobble=material('cobblestone',[125,124,113]);moss=material('mossy_cobblestone',[116,124,94]);dress=material('sandstone',[196,179,137]);plaster=material('white_terracotta',[199,171,153]);clay=material('packed_mud',[140,108,76]);plank=material('oak_planks',[154,121,72]);spruce=material('spruce_planks',[119,88,53]);oak=material('oak_log[axis=y]',[106,83,52]);beam=material('stripped_oak_log[axis=x]',[151,119,71]);hay=material('hay_block[axis=y]',[180,159,64]);leaf=material('oak_leaves[distance=1,persistent=true,waterlogged=false]',[69,111,52]);darkleaf=material('dark_oak_leaves[distance=1,persistent=true,waterlogged=false]',[64,97,43]);water=material('water[level=0]',[ sixty:= sixty if False else 65,119,152]);farmland=material('farmland[moisture=7]',[106,78,45]);wheat=material('wheat[age=7]',[180,168,62]);short=material('short_grass',[95,132,61]);fern=material('fern',[64,119,54]);flower=material('oxeye_daisy',[218,215,163]);poppy=material('poppy',[172,60,42]);torch=material('torch',[226,172,74]);slab=material('oak_slab[type=bottom,waterlogged=false]',[154,121,72]);fence=material('oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]',[138,104,59]);roofstates={}
for name,color in [('bamboo',[180,155,76]),('spruce',[115, eighty:=85,50]),('cobbled_deepslate',[76,79, eighty])]:
 for face in ['north','south','east','west']:
  roofstates[name,face]=material(f'{name}_stairs[facing={face},half=bottom,shape=straight,waterlogged=false]',color)
V=np.zeros((W,H,D),np.uint8);V[:,:7,:]=dirt;V[:,7,:]=grass;initial=V.copy()
def put(x,y,z,p):
 if 0<=x<W and 0<=z<D and Y0<=y<Y0+H:V[x,y-Y0,z]=p
def box(x,y,z,X,Y,Z,p):
 V[max(0,x):min(W,X+1),max(0,y-Y0):min(H,Y-Y0+1),max(0,z):min(D,Z+1)]=p
def line(a,b,p,r=0):
 n=max(abs(b[i]-a[i]) for i in range(3))
 for j in range(n+1):
  x,y,z=[round(a[i]+(b[i]-a[i])*j/max(n,1)) for i in range(3)];box(x-r,y,z-r,x+r,y,z+r,p)
def crown(x,y,z,rx,ry,rz,p):
 for a in range(-rx,rx+1):
  for b in range(-ry,ry+1):
   for c in range(-rz,rz+1):
    if (a/rx)**2+(b/ry)**2+(c/rz)**2<1:put(x+a,y+b,z+c,p)
def channel(z):return 137+17*math.sin(z/48)+7*math.sin(z/21)
T=np.zeros((W,D),int)
for x in range(W):
 for z in range(D):
  d=abs(x-channel(z));w=6+1.2*math.sin(z/17);riverY=65 if z<75 else 62
  h=64+min(20,max(0,d-8)*.145)+17*math.exp(-((x-23)/32)**2-((z-99)/137)**2)+26*math.exp(-((x-232)/29)**2-((z-129)/120)**2)+1.2*math.sin(z/23+x/31)
  h=max(riverY+1,round(h))
  if d<w:h=riverY-3+int(d/w)
  T[x,z]=h;box(x,56,z,x,h,z,stone);box(x,h-2,z,x,h,z,dirt);put(x,h,z,grass)
  if d<w:
   put(x,h,z,gravel if d>w*.6 else mud);box(x,h+1,z,x,riverY,z,water)
  elif d<w+2.8:put(x,h,z,gravel if z%11<7 else mud)
  elif h>92 and x>220:put(x,h,z,chalk if h%5<2 else stone)
  elif d<14 and z>160:put(x,h,z,coarse if math.sin(x*.23+z*.12)>0.3 else grass)
# 木堰保留低槽，磨坊引水沿东岸接回下游，不形成装饰性的孤立池塘。
for z in range(59,101):
 cx=round(159+(z-59)*.018)
 for x in range(cx-2,cx+3):
  h=65 if z<88 else max(62,65-(z-87)//4);box(x,h+1,z,x,max(h+1,int(T[x,z])),z,0);box(x,h-2,z,x,h-1,z,cobble)
  if abs(x-cx)==2:put(x,h,z,cobble)
  else:put(x,h,z,water)
for x in range(round(channel(74))-7,161):
 box(x,63,73,x,64,75,oak)
 if x>round(channel(74))+5:box(x,64,59,x,65,61,water)
for x in range(round(channel(101)),161):box(x,60,100,x,61,102,gravel);box(x,62,100,x,62,102,water)
homes=[('长屋A',72,153,90,163,72,'long'),('农舍B',99,168,111,178,69,'cottage'),('长屋C',62,128,75,141,74,'cross'),('农舍D',94,115,104,125,70,'cottage'),('厅屋E',82,82,102,94,75,'hall'),('农舍F',107,68,118,81,72,'cross'),('佃户G',51,156,63,167,77,'cottage'),('东岸H',173,153,188,164,70,'hall'),('东岸I',178,116,190,128,72,'cottage'),('佃户J',66,104,76,112,77,'cottage')]
facilities=[('教堂',48,83,78,94,82),('庄园',73,39,96,60,81),('谷仓',101,42,119,53,77),('水磨',163,84,178,98,67),('铁匠',108,148,119,158,68)]
def platform(x,z,X,Z,y):
 box(x,56,z,X,y-1,Z,stone);box(x,y,z,X,y,Z,coarse)
 for a in range(x,X+1):
  for c in range(z,Z+1):box(a,y+1,c,a,max(y+1,int(T[a,c])+1),c,0);T[a,c]=y
 for a,c in [(a,z) for a in range(x,X+1)]+[(a,Z) for a in range(x,X+1)]+[(x,c) for c in range(z,Z+1)]+[(X,c) for c in range(z,Z+1)]:
  # 台地侧面保留明确的石脚；以后建筑基础继续向下接入。
  box(a,y-2,c,a,y-1,c,cobble)
for name,x,z,X,Z,y,*rest in homes+facilities:platform(x-1,z-1,X+1,Z+1,y)
trees=[]
for i,(x,z,h,r) in enumerate([(20,60,15,6),(31,75,18,7),(16,91,13,6),(33,103,16,7),(22,123,18,8),(37,137,13,6),(18,154,16,7),(36,179,14,6),(14,192,18,8),(222,69,16,7),(232,88,19,8),(216,109,13,6),(231,130,17,7),(216,146,15,7),(238,159,18,8),(225,174,13,6),(212,196,16,8),(197,209,13,6),(129,111,10,5),(122,176,12,6),(153,205,11,6),(120,217,10,5),(158,28,12,6),(175,39,15,7)]):
 y=int(T[x,z])+1;line((x,y,z),(x+1,y+h-4,z),oak)
 for dx,dz,dh in [(-3,2,-2),(3,-1,0),(1,3,-3)]:
  line((x,y+h-7,z),(x+dx,y+h+dh-3,z+dz),oak);crown(x+dx,y+h+dh-2,z+dz,r-2,3,r-2,leaf if i%3 else darkleaf)
 crown(x,y+h-4,z,r,4,r-1,leaf if i%3 else darkleaf);trees.append([x,y,z,h,r])
# 参考橡树只复用木质和叶冠，去掉原平地基底；这是任务变体，不晋升入库。
ref=json.loads((R.parent/'AI-Blueprints/references/derived/REF-0049/normalized/normalized-blueprint.json').read_text(encoding='utf8'))
selected=[row for row in ref['blocks'] if any(t in ref['palette'][row[3]] for t in ['_log','_wood','_leaves'])]
lo=[min(row[a] for row in selected) for a in range(3)];hi=[max(row[a] for row in selected) for a in range(3)]
for x,y,z,p in selected:
 state=ref['palette'][p].replace('minecraft:','').replace('persistent=false','persistent=true');idx=material(state,[64,97,43] if 'leaves' in state else [96,74,44]);put(x-(lo[0]+hi[0])//2+86,y-lo[1]+71,z-(lo[2]+hi[2])//2+144,idx)
def save(n,name,before):
 folder=R/'蓝图'/f'{n:02d}-{name}';folder.mkdir(parents=True,exist_ok=True);phases=[];changed=V!=before;count=0
 for x in range(0,W,32):
  for y in range(0,H,32):
   for z in range(0,D,32):
    pts=np.argwhere(changed[x:x+32,y:y+32,z:z+32])
    if not len(pts):continue
    blocks=[[int(a),int(b),int(c),int(V[x+a,y+b,z+c])] for a,b,c in pts];count+=len(blocks)
    bp={'schema_version':1,'origin':{'x':x,'y':y+Y0,'z':z},'dimensions':{'x':min(32,W-x),'y':min(32,H-y),'z':min(32,D-z)},'palette':P,'blocks':blocks,'metadata':{'task':'MB-V12-T03','stage':name}}
    with gzip.open(folder/f'{x}_{y}_{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
    # 从 canonical 的同列相邻单元合并批写，不生成第二套建筑数据。
    ops=[];rows=sorted(blocks,key=lambda r:(r[0],r[2],r[1]));i=0
    while i<len(rows):
     a,b,c,p=rows[i];end=b;i+=1
     while i<len(rows) and rows[i]==[a,end+1,c,p]:end+=1;i+=1
     ops.append([x+a,y+Y0+b,z+c,x+a,y+Y0+end,z+c,p])
    phases.append({'palette':P.copy(),'operations':ops})
 job={'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落','phases':phases,'spawn':[32, int(T[32,214])+1,214]}
 if n==1:job['create']={'type':'superflat','seed':2026091003,'generator_options':{'biome':'minecraft:plains','layers':[{'block':'minecraft:bedrock','height':1},{'block':'minecraft:dirt','height':126},{'block':'minecraft:grass_block','height':1}],'structure_overrides':[]}}
 (R/'作业').mkdir(exist_ok=True);(R/'作业'/f'{n:02d}.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8');np.save(R/f'阶段{n}.npy',V);print(n,name,count,flush=True);return V.copy()
before=save(1,'河谷台地林冠',initial)
# 建筑构件函数只复用施工机制，组合由用途决定。
def shell(x,z,X,Z,y,h,wall=plaster):
 box(x,56,z,X,y,Z,cobble);box(x,y+1,z,X,y+h,Z,wall);box(x+1,y+1,z+1,X-1,y+h,Z-1,0);box(x+1,y,z+1,X-1,y,Z-1,plank)
 for a in range(x,X+1,5):box(a,y+1,z,a,y+h,z,oak);box(a,y+1,Z,a,y+h,Z,oak)
 for c in range(z,Z+1,5):box(x,y+1,c,x,y+h,c,oak);box(X,y+1,c,X,y+h,c,oak)
 box(x,y+h,z,X,y+h,z,beam);box(x,y+h,Z,X,y+h,Z,beam)
def roof(x,z,X,Z,y,kind='bamboo',axis='x'):
 if axis=='x':
  mid=(z+Z)/2
  for c in range(z-1,Z+2):
   rise=min(c-z+1,Z+1-c);yy=y+rise;box(x-1,yy,c,X+1,yy,c,roofstates[kind,'south' if c<mid else 'north'])
   if z<=c<=Z:box(x,y,c,x,yy-1,c,plaster);box(X,y,c,X,yy-1,c,plaster)
 else:
  mid=(x+X)/2
  for a in range(x-1,X+2):
   rise=min(a-x+1,X+1-a);yy=y+rise;box(a,yy,z-1,a,yy,Z+1,roofstates[kind,'east' if a<mid else 'west'])
   if x<=a<=X:box(a,y,z,a,yy-1,z,plaster);box(a,y,Z,a,yy-1,Z,plaster)
def door(x,z,y,axis='z',width=2):
 if axis=='z':box(x,y+1,z,x+width-1,y+3,z,0)
 else:box(x,y+1,z,x,y+3,z+width-1,0)
doors=[]
for i,(name,x,z,X,Z,y,typ) in enumerate(homes):
 if typ=='long':
  shell(x,z,X,Z,y,4,clay);roof(x,z,X,Z,y+5);door(X,z+4,y,'x');door(x,z+4,y,'x');box(x+6,y+1,z+1,x+6,y+1,Z-1,fence);door(x+6,z+4,y,'x');entry=[X+1,y+1,z+4]
 elif typ=='hall':
  shell(x,z,X,Z,y,5);roof(x,z,X,Z,y+6,'spruce');door(x+5,Z,y);entry=[x+5,y+1,Z+1]
  box(x+2,y+1,z+2,x+3,y+1,z+3,cobble)
  # 小型开敞附棚与高厅形成非对称工作界面。
  for a in [x,X]:box(a,y+1,Z+3,a,y+3,Z+3,oak)
  box(x,y+4,Z+1,X,y+4,Z+3,slab)
 else:
  shell(x,z,X,Z,y,4,clay if i%2 else plaster);roof(x,z,X,Z,y+5,axis='z' if typ=='cross' else 'x');door(X,z+4,y,'x');entry=[X+1,y+1,z+4]
 for a in [x+3,X-3]:box(a,y+2,z,a,y+3,z,0)
 doors.append({'name':name,'xyz':entry,'inside':[x+2,y+1,z+3]})
# 教堂：石砌长方形殿堂、较小圣坛与短钟塔；不沿用民居木框。
shell(48,83,69,94,82,8,cobble);roof(48,83,69,94,91,'cobbled_deepslate');shell(70,86,78,92,82,6,cobble);roof(70,86,78,92,89,'cobbled_deepslate');box(69,83,87,70,88,90,0)
box(46,56,84,51,101,91,cobble);box(47,83,85,50,100,90,0);box(46,102,84,51,102,91,dress);box(48,103,86,49,104,89,cobble);door(51,87,82,'x');door(46,87,82,'x')
for x in [55,61,66]:box(x,85,83,x,88,83,0);box(x,85,94,x,88,94,0)
door(57,94,82);doors.append({'name':'教堂','xyz':[57,83,95],'inside':[58,83,90]})
# 庄园：开敞厅堂与横向太阳间形成等级体量，楼梯接上层。
shell(73,46,96,60,81,6);roof(73,46,96,60,88,'spruce');shell(73,39,82,47,81,11);roof(73,39,82,47,93,'spruce','z');box(74,87,40,81,87,46,plank);door(86,60,81);box(76,82,46,79,85,47,0)
for i in range(7):box(75,81+i,48-i,76,81+i,48-i,roofstates['spruce','north']);box(75,82+i,48-i,76,84+i,48-i,0)
doors.append({'name':'庄园','xyz':[86,82,61],'inside':[86,82,55]})
# 谷仓：通透木构和对向打谷入口。
shell(101,42,119,53,77,6,spruce);roof(101,42,119,53,84,'bamboo');box(108,78,42,112,82,42,0);box(108,78,53,112,82,53,0);box(103,78,44,105,79,48,hay);doors.append({'name':'谷仓','xyz':[110,78,54],'inside':[110,78,48]})
# 磨坊：石制湿部、木上层、外部上粮阶和静态水轮。
shell(163,84,178,98,67,9,cobble);box(164,72,85,177,72,97,plank);roof(163,84,178,98,77,'spruce','z');door(178,94,67,'x');door(178,87,72,'x');box(174,73,85,177,75,85,plaster)
for i in range(6):box(179,67+i,94-i,180,67+i,94-i,roofstates['spruce','north'])
for angle in range(360):
 a=math.radians(angle);put(160,66+round(4*math.cos(a)),91+round(4*math.sin(a)),spruce)
line((159,66,91),(165,66,91),beam)
for dy,dz in [(4,0),(-4,0),(0,4),(0,-4),(3,3),(-3,-3),(3,-3),(-3,3)]:line((160,66,91),(160,66+dy,91+dz),oak)
doors.append({'name':'水磨','xyz':[179,68,94],'inside':[171,68,94]})
# 铁匠作坊：半开敞工作棚与实体炉墙，和住宅轮廓不同。
box(108,56,148,119,68,158,cobble);box(108,69,148,119,72,148,cobble);box(108,69,148,108,72,158,cobble)
for x,z in [(119,148),(119,158),(108,158)]:box(x,69,z,x,72,z,oak)
roof(108,148,119,158,73,'spruce');box(109,69,149,111, seventyfour:=74,151,cobble);box(110,75,150,110,78,150,cobble);doors.append({'name':'铁匠棚','xyz':[118,69,159],'inside':[115,69,153]})
# 桥跨河连接两岸，木桩和横梁承担有意悬跨。
box(123,68,141,165,68,145,plank)
for x in [124,136,151,164]:
 for z in [141,145]:box(x,58,z,x,69,z,oak)
for x in range(123,166):put(x,69,141,fence);put(x,69,145,fence)
routes=[]
def road(name,pts,width=3):
 surf={};cells=[]
 for a,b in zip(pts,pts[1:]):
  x,y,z=a;X,Y,Z=b;dx,dz=X-x,Z-z;ll=dx*dx+dz*dz
  for xx in range(min(x,X)-width,max(x,X)+width+1):
   for zz in range(min(z,Z)-width,max(z,Z)+width+1):
    if not(0<=xx<W and 0<=zz<D):continue
    t=max(0,min(1,((xx-x)*dx+(zz-z)*dz)/max(ll,1)));dist=(xx-x-t*dx)**2+(zz-z-t*dz)**2
    if dist<=(width/2)**2 and ((xx,zz) not in surf or dist<surf[xx,zz][0]):surf[xx,zz]=(dist,round(y+(Y-y)*t))
  n=max(abs(dx),abs(dz),1)
  for k in range(n+1):cells.append([round(x+dx*k/n),round(y+(Y-y)*k/n),round(z+dz*k/n)])
 for (x,z),(dist,y) in surf.items():
  box(x,y+1,z,x,y+3,z,0);box(x,56,z,x,y-1,z,stone);put(x,y,z,gravel if name!='桥面' else plank)
 routes.append({'name':name,'cells':[[x,surf[x,z][1],z] for x,y,z in cells]})
road('村道',[(32,int(T[32,214]),214),(66,75,190),(92,71,161),(98,70,142),(84,74,124),(92,75,103),(113,72,92),(123,71, sixty_z:=60)],5)
road('教区道',[(84,74,124),(60,80,107),(57,82,95)],3)
road('北庄道',[(113,72,92),(120,75, sixty_a:=65),(110,77,54),(98,79,63),(86,81,61)],3)
road('桥西道',[(98,70,142),(114,68,143),(123,68,143)],4)
road('东岸道',[(165,68,143),(173,69,137),(179,72,132),(194,72,124),(191,70,157)],4)
road('磨坊道',[(179,72,132),(190,69,106),(179,67,94)],3)
# 各户门口接入最近的公共路线，尽量沿宅前方向；不穿越住宅院落。
connections=[([(91,72,157),(92,71,161)],'A'),([(112,69,172),(115,69,166),(100,71,160)],'B'),([(76,74,132),(81,74,132),(84,74,124)],'C'),([(105,70,119),(110,71,121),(105,70,136),(98,70,142)],'D'),([(87,75,95),(92,75,103)],'E'),([(119,72,72),(123,72,72)],'F'),([(64,77,160),(69,76,170),(79,73,172)],'G'),([(178,70,165),(191,70,165),(191,70,157)],'H'),([(191,72,120),(194,72,124)],'I'),([(77,77,108),(84,76,111)],'J'),([(118,68,159),(120,68,155),(114,68,143)],'forge')]
for pts,name in connections:road('宅前'+name,pts,3)
before=save(2,'住居公共生产与交通',before)
# 地表采用有因果的分区：耕作缓坡、可淹草甸、林下腐殖、宅前踩踏。
for x in range(4,252):
 for z in range(4,252):
  h=int(T[x,z]);ground=int(V[x,h-Y0,z]);d=abs(x-channel(z))
  if ground!=grass or V[x,h+1-Y0,z]!=0:continue
  forest=(x<40 and 50<z<203) or (x>207 and 45<z<207)
  field=(x<57 and z>184) or (x>184 and z>178) or (33<x<64 and 17<z<57)
  patch=math.sin(x/8+z/21)+math.cos(z/13-x/23)
  grain=((x*73856093)^(z*19349663))%1009/1009
  if field:
   band=(x+round(3*math.sin(z/28)))%12
   if band<9 and z%29 not in [0,1]:put(x,h,z,farmland);put(x,h+1,z,wheat)
   elif band<11:put(x,h,z,coarse)
  elif forest:
   if math.sin(x*.22+z*.12)>-.2:put(x,h,z,coarse)
   if patch>.15 and grain<.4:put(x,h+1,z,fern)
  elif d<24:
   if patch>-.4 and grain<.45:put(x,h+1,z,short)
   if patch>1 and grain<.04:put(x,h+1,z,flower)
  elif patch>.7 and grain<.2:put(x,h+1,z,short)
  if field and patch>.8 and grain<.16 and (x%12)>9:put(x,h+1,z,poppy)
# 公共井、教区围界、小型菜圃与羊栏，为空地提供真实使用内容。
box(100,70,137,104,71,141,cobble);box(101,71,138,103,71,140,water)
for z in range(81,98):put(44,int(T[44,z])+1,z,moss)
for x in range(48,79,5):box(x,83,79,x,83,80,dress)
for x,z,X,Z,y in [(77,164,87,169,72),(97,107,105,112,71),(177,168,185,173,70)]:
 box(x,56,z,X,y,Z,dirt)
 for a in range(x,X+1):
  for c in range(z,Z+1):put(a,y,c,farmland);put(a,y+1,c,wheat)
for x in range(58,78):
 for z in [174,184]:put(x,int(T[x,z])+1,z,fence)
for z in range(174,185):
 for x in [58,77]:put(x,int(T[x,z])+1,z,fence)
for name,x,z,X,Z,y,*rest in homes:put(x+2,y+1,z+2,torch)
for x,y,z in np.argwhere(V==fence):
 props={}
 for direction,dx,dz in [('east',1,0),('north',0,-1),('south',0,1),('west',-1,0)]:
  props[direction]='true' if 0<=x+dx<W and 0<=z+dz<D and 'oak_fence' in P[int(V[x+dx,y,z+dz])] else 'false'
 state='oak_fence['+','.join(k+'='+v for k,v in sorted({**props,'waterlogged':'false'}.items()))+']';V[x,y,z]=material(state,[138,104,59])
before=save(3,'农业地表与生活细节',before)
(R/'场景.json').write_text(json.dumps({'size':[W,H,D],'y0':Y0,'palette':P,'colors':C,'homes':homes,'facilities':facilities,'doors':doors,'routes':routes,'trees':trees,'world':'MB-V12-T03-河谷村落','reference_reuse':'REF-0049 woody-and-canopy fragment at 86,71,144'},ensure_ascii=False,indent=2),encoding='utf8')
print('蓝图生成完成')
