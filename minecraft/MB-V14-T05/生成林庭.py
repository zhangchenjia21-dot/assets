"""T05 原创林庭模型；只生成蓝图和作业，实际存档交由正式接口。"""
from pathlib import Path
import numpy as np,json,gzip,math,random
R=Path(__file__).parent;W=D=256;H=96;Y0=56;P=['minecraft:air'];C=[[177,203,207]]
def mat(n,c):
 n='minecraft:'+n
 if n in P:return P.index(n)
 P.append(n);C.append(c);return len(P)-1
stone=mat('stone',[121,129,119]);andesite=mat('andesite',[134,143,131]);mossrock=mat('mossy_cobblestone',[105,127,84]);dirt=mat('dirt',[111,80,52]);podzol=mat('podzol[snowy=false]',[104,82,48]);grass=mat('grass_block[snowy=false]',[100,128,63]);moss=mat('moss_block',[88,124,57]);coarse=mat('coarse_dirt',[127,99,61]);mud=mat('mud',[83,92,80]);water=mat('water[level=0]',[61,120,134]);root=mat('dark_oak_log[axis=y]',[72,58,41]);bark=mat('dark_oak_log[axis=z]',[79,61,40]);wood=mat('oak_planks',[162,131,82]);beam=mat('stripped_oak_log[axis=x]',[151,116,68]);leaf=mat('oak_leaves[distance=1,persistent=true,waterlogged=false]',[56,107,52]);leaf2=mat('dark_oak_leaves[distance=1,persistent=true,waterlogged=false]',[44,83,44]);leaf3=mat('azalea_leaves[distance=1,persistent=true,waterlogged=false]',[81,129,59]);fern=mat('fern',[65,119,52]);short=mat('short_grass',[100,145,59]);white=mat('lily_of_the_valley',[225,229,202]);purple=mat('allium',[155,105,183]);blue=mat('blue_orchid',[98,172,198]);glow=mat('shroomlight',[210,170,84]);fence=mat('oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]',[162,131,82]);slab=mat('oak_slab[type=bottom,waterlogged=false]',[162,131,82]);seed=mat('bookshelf',[122,116,69]);stairs={}
for f in ['north','south','east','west']:stairs[f]=mat(f'oak_stairs[facing={f},half=bottom,shape=straight,waterlogged=false]',[162,131,82])
V=np.zeros((W,H,D),np.uint8);T=np.zeros((W,D),np.int16);reserve=np.zeros((W,D),bool);routes=[];targets=[];trees=[];envelopes=[];rng=random.Random(514)
def put(x,y,z,p):
 if 0<=x<W and Y0<=y<Y0+H and 0<=z<D:V[x,y-Y0,z]=p
def box(x,y,z,X,Y,Z,p):
 assert 0<=x<=X<W and Y0<=y<=Y<Y0+H and 0<=z<=Z<D,(x,y,z,X,Y,Z)
 V[x:X+1,y-Y0:Y-Y0+1,z:Z+1]=p
def segment(a,b,p,r=0):
 n=max(abs(b[i]-a[i]) for i in range(3));prev=list(a)
 for k in range(n+1):
  q=[round(a[i]+(b[i]-a[i])*k/max(n,1)) for i in range(3)]
  for axis in range(3):
   prev[axis]=q[axis]
   for dx in range(-r,r+1):
    for dy in range(-r,r+1):
     for dz in range(-r,r+1):
      if dx*dx+dy*dy+dz*dz<=r*r+1:put(prev[0]+dx,prev[1]+dy,prev[2]+dz,p)
def ellipsoid(cx,cy,cz,rx,ry,rz,p,empty=False):
 for x in range(max(0,int(cx-rx)),min(W,int(cx+rx)+1)):
  for y in range(max(Y0,int(cy-ry)),min(Y0+H,int(cy+ry)+1)):
   for z in range(max(0,int(cz-rz)),min(D,int(cz+rz)+1)):
    if ((x-cx)/rx)**2+((y-cy)/ry)**2+((z-cz)/rz)**2<=1 and (not empty or V[x,y-Y0,z]==0):put(x,y,z,p)
for x in range(W):
 for z in range(D):
  # 浅盆、偏心土丘和泉沟决定地貌，起伏控制在林下尺度。
  west=10*math.exp(-((x-72)/44)**2-((z-94)/56)**2)
  north=13*math.exp(-((x-166)/57)**2-((z-48)/35)**2)
  east=7*math.exp(-((x-205)/34)**2-((z-132)/55)**2)
  swale=-3*math.exp(-((x-(122+12*math.sin(z/34)))/16)**2)*math.exp(-((z-156)/65)**2)
  pocket=1.3*math.sin(x/13+z/19)*math.sin(z/11)*min(1,(west+north+east)/8)
  edge=max(0,min(1,x/18,(255-x)/18,z/18,(255-z)/18));y=round(64+(west+north+east+swale+pocket)*edge);T[x,z]=max(62,y)
  box(x,56,z,x,int(T[x,z])-3,z,stone);box(x,int(T[x,z])-2,z,x,int(T[x,z])-1,z,dirt);put(x,int(T[x,z]),z,grass)
# 不规则泉池，北方来水从浅沟落入盆底；岸线保留土壤与碎石袋。
wet=np.zeros((W,D),bool)
for x in range(87,182):
 for z in range(99,192):
  theta=math.atan2(z-148,x-132);rr=1+.09*math.sin(theta*3)+.05*math.sin(theta*7)
  basin=((x-132)/25)**2+((z-148)/21)**2
  if basin<rr:
   h=int(T[x,z]);bottom=62 if basin<.6 else 63;box(x,bottom,z,x,max(h,66),z,0);put(x,bottom,z,mud);box(x,bottom+1,z,x,65,z,water);T[x,z]=bottom;wet[x,z]=True
def streamcenter(z):return round(148+12*math.sin((z-42)/31)) if z<129 else round(111+10*math.sin((z-174)/26))
for z in list(range(49,132))+list(range(169,239)):
 cx=streamcenter(z);level=72 if z<65 else 70 if z<83 else 68 if z<104 else 65 if z<184 else 64 if z<211 else 63
 for x in range(cx-3,cx+4):
  h=int(T[x,z]);box(x,level-2,z,x,max(h,level+1),z,0);put(x,level-2,z,andesite);box(x,level-1,z,x,level,z,water);T[x,z]=level-2;wet[x,z]=True
# 泉池北岸的根庭自然土肩，为祖树保留地基；不填平水面。
for x in range(127,147):
 for z in range(103,122):
  if (x-137)**2+(z-112)**2<95 and not wet[x,z]:
   h=int(T[x,z]);box(x,min(h,69),z,x,69,z,dirt);put(x,69,z,moss);T[x,z]=69
pathspec=[('入林径',[(87,232),(92,213),(100,196),(103,181),(109,174)]),('西岸巡林',[(109,174),(105,158),(108,139),(113,136),(115,132),(115,121)]),('种子室支径',[(105,158),(95,145),(94,133)]),('北根径',[(94,133),(91,138),(81,138),(79,127),(79,100),(104,91),(120,95),(128,99)]),('东岸径',[(109,174),(126,182),(151,183),(164,173),(168,155),(169,141),(162,125),(158,126),(158,125),(158,115)]),('归林径',[(164,173),(176,188),(164,207),(132,214),(112,208),(106,218),(92,219),(92,213)])]
pathcells=[]
for name,pts in pathspec:
 cells=[]
 for (x,z),(X,Z) in zip(pts,pts[1:]):
  n=max(abs(X-x),abs(Z-z))
  for k in range(n+1):
   a=round(x+(X-x)*k/n);c=round(z+(Z-z)*k/n);cells.append((a,c))
 for x,z in cells:reserve[max(0,x-5):min(W,x+6),max(0,z-5):min(D,z+6)]=True
 pathcells.append((name,cells))
reserve[82:105,100:135]=True;reserve[150:181,128:159]=True;reserve[113:163,90:135]=True;reserve[155:181,163:181]=True
def tree(x,z,h,r,kind=0,elder=False):
 y=int(T[x,z]);trees.append({'xyz':[x,y,z],'height':h,'radius':r,'kind':kind,'elder':elder})
 thick=3 if elder else 1 if h>22 else 0
 segment((x,y+1,z),(x-1,y+h-13,z+1),root,thick)
 # 弯曲分叉与多高程树冠，每个冠团都有连续木枝连接。
 for j in range(6 if elder else 3):
  angle=j*2.399+kind*.8;reach=r*(.7 if elder else .55);cx=x+round(math.cos(angle)*reach);cz=z+round(math.sin(angle)*reach);cy=y+h-6-(j%3)*3
  segment((x,y+h-17,z),(cx,cy-2,cz),root,1 if elder else 0)
  ellipsoid(cx,cy,cz,r*.61,7 if elder else max(4,r*.62),r*.55,[leaf,leaf2,leaf3][(kind+j//2)%3],True)
 for angle in [0,.9,2.1,3.2,4.4,5.4]:
  reach=17 if elder else 4;xx=x+round(reach*math.cos(angle));zz=z+round(reach*math.sin(angle));yy=int(T[xx,zz])+1
  segment((x,y+5,z),(xx,yy,zz),root,1 if elder else 0)
tree(137,112,48,29,0,True)
# 树群按场地边缘与开口组织；低枝和根不进入预留地面交通。
centers=[(42,48),(54,80),(39,113),(56,151),(48,188),(70,211),(196,49),(212,79),(205,109),(213,148),(204,189),(179,216),(109,47),(147,32)]
for i,(cx,cz) in enumerate(centers):
 for j in range(4):
  x=cx+rng.randint(-12,12);z=cz+rng.randint(-13,13)
  if not(15<x<241 and 15<z<241) or reserve[x,z] or wet[x,z] or any((x-t['xyz'][0])**2+(z-t['xyz'][2])**2<64 for t in trees):continue
  tree(x,z,rng.randint(20,32),rng.randint(9,14),(i+j)%3)
def save(n,old):
 np.save(R/f'阶段{n}.npy',V);mask=V!=old;folder=R/f'蓝图/{n}';folder.mkdir(parents=True,exist_ok=True);ph=[];count=0
 for x in range(0,W,32):
  for y in range(0,H,32):
   for z in range(0,D,32):
    q=np.argwhere(mask[x:x+32,y:y+32,z:z+32])
    if not len(q):continue
    b=[[int(a),int(c),int(d),int(V[x+a,y+c,z+d])] for a,c,d in q];count+=len(b);bp={'schema_version':1,'origin':{'x':x,'y':y+56,'z':z},'dimensions':{'x':32,'y':32,'z':32},'palette':P.copy(),'blocks':b}
    with gzip.open(folder/f'{x}-{y}-{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
    ops=[]
    for a in range(32):
     for d in range(32):
      c=0
      while c<32:
       if not mask[x+a,y+c,z+d]:c+=1;continue
       start=c;p=int(V[x+a,y+c,z+d]);c+=1
       while c<32 and mask[x+a,y+c,z+d] and V[x+a,y+c,z+d]==p:c+=1
       ops.append([x+a,y+start+56,z+d,x+a,y+c-1+56,z+d,p])
    ph.append({'palette':P.copy(),'operations':ops})
 job={'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V14-T05-森林圣所','phases':ph}
 if n=='01':job.update(create={'type':'superflat','seed':2026091005,'generator_options':{'biome':'minecraft:forest','layers':[{'block':'minecraft:bedrock','height':1},{'block':'minecraft:dirt','height':126},{'block':'minecraft:grass_block','height':1}],'structure_overrides':[],'features':False,'lakes':False}},spawn=[87,int(T[87,232])+1,232])
 (R/'作业').mkdir(exist_ok=True);(R/f'作业/{n}.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8');print(n,count,flush=True);return V.copy()
initial=np.zeros_like(V);initial[:,:7,:]=dirt;initial[:,7,:]=grass;before=save('01',initial)
# 地面路线先合并共享接口，再一次生成路面，避免相邻路径互相覆盖。
roadmask=np.zeros_like(reserve);earth=[];plan={};planned=[]
for name,cells in pathcells:
 heights=[max(int(T[x,z]),67) if wet[x-1:x+2,z-1:z+2].any() else int(T[x,z]) for x,z in cells]
 for k in range(1,len(heights)):heights[k]=max(heights[k-1]-1,heights[k])
 for k in range(len(heights)-2,-1,-1):heights[k]=max(heights[k+1]-1,heights[k])
 for (x,z),y in zip(cells,heights):
  for dx,dz in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
   key=(x+dx,z+dz);score=dx*dx+dz*dz
   if key not in plan or score<plan[key][0]:plan[key]=(score,y)
 planned.append((name,cells))
for (a,c),(_,y) in plan.items():
 h=int(T[a,c]);roadmask[a,c]=True
 if wet[a,c]:
  put(a,y,c,wood)
  if c%6==0 and h+1<=y-1:box(a,h+1,c,a,y-1,c,root)
 else:
  earth.append(abs(y-h))
  if h<y:box(a,h+1,c,a,y,c,dirt)
  elif h>y:box(a,y+1,c,a,h,c,0)
  put(a,y,c,coarse)
 for yy in [y+1,y+2]:
  if V[a,yy-56,c] not in [0,water]:raise RuntimeError(('route collision',a,yy,c,P[int(V[a,yy-56,c])]))
for name,cells in planned:routes.append({'name':name,'cells':[[x,plan[x,z][1]+1,z] for x,z in cells]})
# 祖树环廊：活根柱承重，外围栏杆留三处入口，内侧可看主干与树根。
for x in range(113,162):
 for z in range(88,137):
  d=math.hypot(x-137,z-112)
  if 16<=d<=20:put(x,75,z,wood)
  if 19<=d<=20 and not(116<x<125 and 119<z<127) and not(155<x<161 and 108<z<117) and not(123<x<132 and 94<z<102):put(x,76,z,fence)
for angle in [0,.8,1.7,2.5,3.3,4.2,5.2]:
 x=137+round(18*math.cos(angle));z=112+round(18*math.sin(angle));h=int(T[x,z]);segment((x,h+1,z),(x,74,z),root,1);segment((x,74,z),(137,71,112),root)
def steps(x,z,y,n,face,width=3):
 dx,dz={'north':(0,-1),'south':(0,1),'east':(1,0),'west':(-1,0)}[face]
 for i in range(n):
  for k in range(width):
   a=x+i*dx+(k if dz else 0);c=z+i*dz+(k if dx else 0);yy=y+i;h=int(T[a,c]);box(a,min(h,yy),c,a,yy,c,root);put(a,yy,c,stairs[face]);box(a,yy+1,c,a,yy+3,c,0)
steps(115,131,65,11,'north');box(115,75,120,123,75,122,wood);box(115,76,120,123,78,122,0)
steps(157,125,65,11,'north');box(155,75,114,159,75,116,wood);box(155,76,114,159,78,116,0)
targets += [['西根廊',121,76,113],['东根廊',155,76,112],['北根廊',137,76,94],['南根廊',137,76,130]]
# 泉池听水台以根桥进入，桥面下为水，根弧与岸基连接。
box(106,67,151,120,67,153,wood);box(118,67,146,124,67,157,wood)
for z in [151,153]:segment((106,65,z),(115,66,z),root);segment((115,66,z),(124,63,z),root)
targets.append(['听水台',122,68,151])
# 倒木种子室：半圆筒形外壳与两道突出树节，而非矩形墙面。
floor=70
for x in range(85,104):
 for z in range(104,132):
  if 87<=x<=101:
   h=int(T[x,z]);box(x,min(h,floor),z,x,floor,z,mossrock)
  for y in range(71,82):
   d=((x-94)/9)**2+((y-71)/10)**2
   if .65<d<=1:put(x,y,z,bark)
for z in [104,105,130,131]:
 for x in range(87,102):
  for y in range(71,80):
   if ((x-94)/9)**2+((y-71)/10)**2<=1:put(x,y,z,beam)
box(89,70,105,100,70,130,wood);box(92,71,129,96,75,131,0)
for z in [112,122]:box(85,73,z,87,75,z+2,0)
for z in [111,123]:
 for x in range(84,105):
  yy=71+round(10*math.sqrt(max(0,1-((x-94)/10)**2)))
  if x>84:segment((x-1,prevy,z),(x,yy,z),root)
  else:put(x,yy,z,root)
  prevy=yy
for z in [108,116,124]:box(99,71,z,100,73,z+2,seed)
targets.append(['种子室',94,71,127]);envelopes.append({'name':'种子室','bounds':[84,69,103,105,83,132]})
# 议庭：叶片壳覆盖弯曲肋骨，三边开放；石脚仅位于柱根潮湿位置。
cx,cz=169,142;fy=68
for x in range(156,182):
 for z in range(131,155):
  if ((x-cx)/13)**2+((z-cz)/12)**2<1:
   h=int(T[x,z]);box(x,min(h,fy),z,x,fy,z,mossrock);put(x,fy,z,wood)
for z in [132,141,151]:
 pts=[(157,69,z),(159,76,z),(168,83,z),(177,78,z),(180,69,z)]
 for a,b in zip(pts,pts[1:]):segment(a,b,root,1)
for x in range(157,181):
 y=round(74+8*math.sin((x-157)/23*math.pi))
 for z in range(132,153):
  if ((x-169)/13)**2+((z-142)/14)**2<1.2:
   if V[x,y-56,z]==0:put(x,y,z,moss)
   if V[x,y-1-56,z]==0:put(x,y-1,z,leaf2)
for x,z in [(158,133),(179,133),(158,151),(179,151)]:box(x,68,z,x,71,z,mossrock)
box(166,67,154,172,67,156,wood)
targets.append(['叶棚议庭',169,69,147]);envelopes.append({'name':'议庭','bounds':[155,67,130,183,85,156]})
# 南入口的两根活木相拱，尺度低于祖树并依附地脚。
for x,sign in [(87,1),(98,-1)]:
 y=int(T[x,212]);segment((x,y+1,212),(x+sign*2,y+7,212),root,1);segment((x+sign*2,y+7,212),(93,y+9,212),root,1)
ellipsoid(93,76,212,7,3,3,leaf3,True)
targets += [['幼林圃',165,int(T[165,173])+1,173],['入口',92,int(T[92,214])+1,214],['泉池西岸',105,int(T[105,158])+1,158]]
# 环廊梯和开放议庭属于明确的通路接口，登记实际脚点高度。
for route in routes:
 for p in route['cells']:
  x,y,z=p;choices=[]
  for yy in range(max(57,y-2),min(90,y+13)):
   if V[x,yy-1-56,z]!=0 and V[x,yy-56,z]==0 and V[x,yy+1-56,z]==0:choices.append(yy)
  if choices:p[1]=min(choices,key=lambda yy:abs(yy-y))
before=save('02',before);structure=V.copy()
# 地表与花群按林下、湿岸、向光开口与人工圃地分布，植被不进入交通和建筑。
flowerpatches=[(158,172,10,7,white),(174,176,8,5,purple),(156,158,6,9,blue),(106,143,5,8,white),(83,193,8,10,purple)]
for x in range(8,248):
 for z in range(8,248):
  if roadmask[x,z] or wet[x,z] or (84<x<106 and 102<z<134) or (154<x<184 and 129<z<157) or (114<x<162 and 88<z<138):continue
  h=int(T[x,z]);p=int(V[x,h-56,z])
  if p!=grass or V[x,h+1-56,z]!=0:continue
  near=min((x-t['xyz'][0])**2+(z-t['xyz'][2])**2 for t in trees);q=(math.sin(x/9+z/13)+math.cos(z/15-x/23));grain=((x*73856093)^(z*19349663))%1009/1009
  if near<280:
   put(x,h,z,podzol if near<95 else moss if q>.5 else grass)
   if grain<.48:put(x,h+1,z,fern)
   if grain<.032 and q>.2:
    put(x,h+1,z,leaf3)
    if grain<.014 and V[x,h+2-56,z]==0:put(x,h+2,z,leaf3)
  elif grain<.58 and q>-.9:put(x,h+1,z,short)
  for a,c,rx,rz,flower in flowerpatches:
   d=((x-a)/rx)**2+((z-c)/rz)**2
   if d<1 and grain<.4*(1-d)+.08:put(x,h+1,z,flower)
# 有根接地的幼树及育苗床边，留出两格以上间隙。
for x,z in [(155,174),(168,179),(176,171),(171,166)]:
 h=int(T[x,z]);segment((x,h+1,z),(x,h+4,z),root);ellipsoid(x,h+5,z,2,2,2,leaf3,True)
for x,y,z in [(120,74,121),(156,74,116),(100,74,107),(158,73,133),(178,73,151)]:put(x,y,z,glow)
# 根廊栏杆状态依邻接生成；所有新方块均能被运行时原生解析。
for x,y,z in np.argwhere(V==fence):
 props={}
 for d,dx,dz in [('east',1,0),('north',0,-1),('south',0,1),('west',-1,0)]:props[d]='true' if 'fence' in P[int(V[x+dx,y,z+dz])] else 'false'
 p=mat('oak_fence['+','.join(k+'='+v for k,v in sorted({**props,'waterlogged':'false'}.items()))+']',[162,131,82]);V[x,y,z]=p
save('03',before)
changes=[]
for x,y,z in np.argwhere((V!=structure)&(structure!=0)):
 a=P[int(structure[x,y,z])];b=P[int(V[x,y,z])]
 if not any(k in a for k in ['grass_block','fence']):changes.append([int(x),int(y+56),int(z),a,b])
(R/'场景.json').write_text(json.dumps({'world':'MB-V14-T05-森林圣所','size':[W,H,D],'y0':56,'palette':P,'colors':C,'routes':routes,'targets':targets,'trees':trees,'envelopes':envelopes,'path_earthwork_max':max(earth),'path_earthwork_mean':float(np.mean(earth)),'micro_solid_changes':changes},ensure_ascii=False,indent=2),encoding='utf8');print('trees',len(trees),'pathmax',max(earth),'micro',changes,flush=True)
