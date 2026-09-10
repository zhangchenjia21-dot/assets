"""T04 原创空间模型；仅生成任务蓝图，施工交给正式离线接口。"""
from pathlib import Path
import numpy as np,json,gzip,math
R=Path(__file__).parent;W=D=256;H=128;Y0=56
P=['minecraft:air'];C=[[173,199,208]]
def mat(s,c):
 s='minecraft:'+s
 if s in P:return P.index(s)
 P.append(s);C.append(c);return len(P)-1
stone=mat('stone',[128,130,126]);rock=mat('andesite',[137,139,135]);cobble=mat('cobblestone',[119,124,119]);brick=mat('stone_bricks',[147,151,144]);moss=mat('mossy_stone_bricks',[126,139,113]);dress=mat('polished_andesite',[165,168,161]);dirt=mat('dirt',[116,86,61]);grass=mat('grass_block[snowy=false]',[97,123,66]);coarse=mat('coarse_dirt',[120,95,65]);gravel=mat('gravel',[149,140,121]);wood=mat('spruce_planks',[115,84,53]);oak=mat('oak_log[axis=y]',[97,75,48]);beam=mat('stripped_oak_log[axis=x]',[139,105,68]);plaster=mat('white_terracotta',[184,156,136]);leaf=mat('oak_leaves[distance=1,persistent=true,waterlogged=false]',[67,104,50]);leaf2=mat('birch_leaves[distance=1,persistent=true,waterlogged=false]',[92,127,58]);leaf3=mat('dark_oak_leaves[distance=1,persistent=true,waterlogged=false]',[55,88,44]);fern=mat('fern',[75,116,49]);short=mat('short_grass',[105,140,65]);daisy=mat('oxeye_daisy',[213,213,169]);water=mat('water[level=0]',[63,110,132]);hay=mat('hay_block[axis=y]',[166,141,60]);torch=mat('torch',[225,167,55]);slab=mat('stone_brick_slab[type=bottom,waterlogged=false]',[147,151,144]);fence=mat('spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]',[115,84,53]);stairs={}
for material,color in [('stone_brick',[147,151,144]),('spruce',[115,84,53]),('cobbled_deepslate',[67,73,76])]:
 for f in ['north','south','east','west']:stairs[material,f]=mat(f'{material}_stairs[facing={f},half=bottom,shape=straight,waterlogged=false]',color)
V=np.zeros((W,H,D),np.uint8);T=np.zeros((W,D),np.int16);route=[];targets=[];trees=[];envelopes=[]
def box(x,y,z,X,Y,Z,p):
 assert 0<=x<=X<W and Y0<=y<=Y<Y0+H and 0<=z<=Z<D,(x,y,z,X,Y,Z)
 V[x:X+1,y-Y0:Y-Y0+1,z:Z+1]=p
def put(x,y,z,p):
 if 0<=x<W and Y0<=y<Y0+H and 0<=z<D:V[x,y-Y0,z]=p
def line(a,b,p,width=0):
 # 正交补接口让斜向枝杈、梁与墙体保持面连接。
 n=max(abs(b[i]-a[i]) for i in range(3));prev=a
 for k in range(n+1):
  q=tuple(round(a[i]+(b[i]-a[i])*k/max(n,1)) for i in range(3));cur=list(prev)
  for axis in range(3):
   cur[axis]=q[axis]
   for xx in range(cur[0]-width,cur[0]+width+1):
    for zz in range(cur[2]-width,cur[2]+width+1):put(xx,cur[1],zz,p)
  prev=q
def poly(x,z,pts):
 c=False;j=len(pts)-1
 for i,(a,b) in enumerate(pts):
  A,B=pts[j]
  if (b>z)!=(B>z) and x<(A-a)*(z-b)/(B-b)+a:c=not c
  j=i
 return c
for x in range(W):
 for z in range(D):
  center=132+5*math.sin(z/43);width=51 if x<center else 66
  broad=47.5*math.exp(-(abs(x-center)/width)**3.2-(abs(z-109)/102)**6)
  shoulder=8*math.exp(-((x-196)/47)**2-((z-73)/73)**2)
  edge=max(0,min(1,x/22,(255-x)/22,z/22,(255-z)/22))
  noise=(1.1*math.sin(x/11+z/18)+.8*math.sin(z/8-x/17))*min(1,broad/20)
  T[x,z]=round(63+(broad+shoulder+noise)*edge)
  y=int(T[x,z]);box(x,56,z,x,y,z,stone)
  if (abs(x-center)>width*.63 and broad>10) or (y>100 and math.sin(z/8+x/13)>1.4):
   for yy in range(max(64,y-4),y+1):put(x,yy,z,rock if yy%7<2 else stone)
  else:box(x,y-2,z,x,y-1,z,dirt);put(x,y,z,grass)
# 干壕切穿南鞍部；两端随坡面收束，不设置无因果水壕。
for x in range(102,173):
 for z in range(183,191):
  h=int(T[x,z]);depth=round(7*min(1,(x-101)/10,(173-x)/10));box(x,h-depth+1,z,x,h,z,0);T[x,z]=h-depth;put(x,h-depth,z,rock)
upper=[(107,141),(103,111),(109,82),(139,73),(165,87),(168,118),(160,141)]
lower=[(110,144),(159,144),(170,163),(157,177),(116,177),(106,161)]
# 主院为脊顶范围内有限整平；记录填挖量，避免整块空心平台。
earth=[]
for name,pts,fy in [('内院',upper,111),('外院',lower,108)]:
 dif=[]
 for x in range(100,172):
  for z in range(70,180):
   if poly(x,z,pts):
    h=int(T[x,z]);dif.append(fy-h)
    if h<fy:box(x,h+1,z,x,fy,z,stone)
    elif h>fy:box(x,fy+1,z,x,h,z,0)
    put(x,fy,z,gravel if (x//5+z//7)%4 else coarse);T[x,z]=fy
 earth.append({'name':name,'cells':len(dif),'max_fill':max(dif),'max_cut':-min(dif),'mean_abs':float(np.mean(np.abs(dif)))})
def road(name,pts,width=4):
 cells={}
 for a,b in zip(pts,pts[1:]):
  x,y,z=a;X,Y,Z=b;n=max(abs(X-x),abs(Z-z));dx=X-x;dz=Z-z;ll=dx*dx+dz*dz
  for xx in range(min(x,X)-width,max(x,X)+width+1):
   for zz in range(min(z,Z)-width,max(z,Z)+width+1):
    t=max(0,min(1,((xx-x)*dx+(zz-z)*dz)/ll));d=(xx-x-dx*t)**2+(zz-z-dz*t)**2
    if d<=(width/2)**2 and ((xx,zz) not in cells or d<cells[xx,zz][0]):cells[xx,zz]=(d,round(y+(Y-y)*t))
 for (x,z),(_,y) in cells.items():
  if not(0<=x<W and 0<=z<D):continue
  old=int(T[x,z]);box(x,min(old,y),z,x,y,z,stone) if old<=y else None
  put(x,y,z,gravel)
  if old>y:box(x,y+1,z,x,old,z,0)
  T[x,z]=y
 samples=[]
 for a,b in zip(pts,pts[1:]):
  n=max(abs(b[0]-a[0]),abs(b[2]-a[2]))
  for k in range(n+1):
   x=round(a[0]+(b[0]-a[0])*k/n);z=round(a[2]+(b[2]-a[2])*k/n);samples.append([x,cells[x,z][1]+1,z])
 route.append({'name':name,'cells':samples})
road('登山接近',[(224,64,246),(211,69,229),(194,78,216),(174,90,216),(154,100,206),(136,108,194)],5)
road('外院至内门',[(135,108,179),(135,108,156),(133,111,143),(133,111,134)],4)
# 干壕木桥；桥台与坡面接口明确，桥面不填成土堤。
box(133,108,178,137,108,194,wood)
for z in [181,192]:box(132,int(T[132,z])+1,z,138,107,z,cobble)
for x in [133,137]:
 for z in range(179,195):put(x,109,z,fence)
route.append({'name':'壕桥','cells':[[135,109,z] for z in range(178,195)]})
def tree(x,z,h,r,variant):
 y=int(T[x,z]);trees.append([x,y,z,h,r,variant]);line((x,y+1,z),(x,y+h-3,z),oak)
 crowns=[(x,y+h-2,z,r,3),(x-r//2,y+h-4,z+2,r-1,3),(x+3,y+h-5,z-r//2,r-1,3)]
 for cx,cy,cz,rr,ry in crowns:
  line((x,y+h-6,z),(cx,cy,cz),oak)
  for a in range(cx-rr,cx+rr+1):
   for b in range(cy-ry,cy+ry+1):
    for c in range(cz-rr,cz+rr+1):
     if ((a-cx)/rr)**2+((b-cy)/ry)**2+((c-cz)/(rr*.83))**2<1 and 0<=a<W and 0<=c<D and V[a,b-Y0,c]==0:put(a,b,c,[leaf,leaf2,leaf3][variant])
for x,z,h,r,k in [(42,69,17,7,0),(50,76,14,6,2),(37,84,20,7,0),(53,97,16,7,0),(43,111,14,6,2),(34,126,18,8,0),(49,137,15,7,1),(58,157,18,7,0),(43,161,13,6,2),(53,179,16,6,0),(68,193,14,6,1),(77,206,18,7,0),(59,209,12,5,2),(73,224,15,6,0),(191,46,20,8,0),(205,54,15,7,2),(216,70,18,7,0),(209,86,14,6,1),(222,98,17,7,0),(201,111,18,8,0),(216,124,13,6,2),(230,143,18,7,0),(211,151,15,7,1),(233,163,14,6,0),(224,180,17,7,0),(195,179,12,5,2),(172,33,16,7,0),(151,22,14,6,1),(112,24,17,7,0),(95,39,13,6,2)]:tree(x,z,h,r,k)
def save(n,old):
 np.save(R/f'阶段{n}.npy',V);mask=V!=old;folder=R/f'蓝图/{n}';folder.mkdir(parents=True,exist_ok=True);ph=[];count=0
 for x in range(0,W,32):
  for y in range(0,H,32):
   for z in range(0,D,32):
    q=np.argwhere(mask[x:x+32,y:y+32,z:z+32])
    if not len(q):continue
    blocks=[[int(a),int(b),int(c),int(V[x+a,y+b,z+c])] for a,b,c in q];count+=len(blocks)
    bp={'schema_version':1,'origin':{'x':x,'y':y+Y0,'z':z},'dimensions':{'x':32,'y':32,'z':32},'palette':P.copy(),'blocks':blocks}
    with gzip.open(folder/f'{x}-{y}-{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
    # 同列等状态连续段批量化，操作逐格等价由执行前检查核实。
    ops=[]
    for a in range(32):
     for c in range(32):
      b=0
      while b<32:
       if not mask[x+a,y+b,z+c]:b+=1;continue
       start=b;p=int(V[x+a,y+b,z+c]);b+=1
       while b<32 and mask[x+a,y+b,z+c] and V[x+a,y+b,z+c]==p:b+=1
       ops.append([x+a,y+start+Y0,z+c,x+a,y+b-1+Y0,z+c,p])
    ph.append({'palette':P.copy(),'operations':ops})
 job={'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V13-T04-山脊城堡','phases':ph}
 if n=='01':job.update(create={'type':'superflat','seed':2026091004,'generator_options':{'biome':'minecraft:plains','layers':[{'block':'minecraft:bedrock','height':1},{'block':'minecraft:dirt','height':126},{'block':'minecraft:grass_block','height':1}],'structure_overrides':[],'features':False,'lakes':False}},spawn=[224,65,246])
 (R/'作业').mkdir(exist_ok=True);(R/f'作业/{n}.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8');print(n,count,flush=True);return V.copy()
initial=np.zeros_like(V);initial[:,:7,:]=dirt;initial[:,7,:]=grass
before=save('01',initial)
def footing(x,z,X,Z,y):
 for a in range(x,X+1):
  for c in range(z,Z+1):
   h=int(T[a,c]);box(a,min(h,y),c,a,y,c,cobble)
def shell(name,x,z,X,Z,y,h,wall=brick):
 footing(x,z,X,Z,y);box(x,y+1,z,X,y+h,Z,wall);box(x+2,y+1,z+2,X-2,y+h,Z-2,0);box(x+1,y,z+1,X-1,y,Z-1,wood)
 envelopes.append({'name':name,'bounds':[x,y,z,X,y+h,Z]})
def door(x,y,z,axis='z',width=3,height=4):
 if axis=='z':box(x,y,z,x+width-1,y+height-1,z+1,0)
 else:box(x,y,z,x+1,y+height-1,z+width-1,0)
def roof(x,z,X,Z,y):
 for xx in range(x-1,X+2):
  yy=y+min(xx-x+1,X+1-xx);face='east' if xx<(x+X)/2 else 'west';box(xx,yy,z-1,xx,yy,Z+1,stairs['cobbled_deepslate',face])
  if x<=xx<=X:
   if yy>y:box(xx,y,z,xx,yy-1,z,brick);box(xx,y,Z,xx,yy-1,Z,brick)
def wall(pts,ground,walk):
 for a,b in zip(pts,pts[1:]+pts[:1]):
  n=max(abs(b[0]-a[0]),abs(b[1]-a[1]))
  for k in range(n+1):
   x=round(a[0]+(b[0]-a[0])*k/n);z=round(a[1]+(b[1]-a[1])*k/n)
   for dx in [-1,0,1]:
    for dz in [-1,0,1]:
     xx,zz=x+dx,z+dz;h=int(T[xx,zz]);box(xx,min(h,ground),zz,xx,walk,zz,brick if (xx+zz)%13 else cobble)
   # 两侧胸墙中留连续两格以上的走道；垛口按防御构件节奏排列。
   if k%5<2:box(x,walk+1,z,x,walk+2,z,brick)
def tower(cx,cz,r,y,top):
 for x in range(cx-r,cx+r+1):
  for z in range(cz-r,cz+r+1):
   d=(x-cx)**2+(z-cz)**2
   if d<=r*r:
    h=int(T[x,z]);box(x,min(h,y),z,x,y,z,cobble)
    if d>(r-2)**2:box(x,y+1,z,x,top+1,z,brick)
    else:box(x,y+1,z,x,top-1,z,0)
    put(x,top,z,brick)
    if (r-1)**2<d and (x+z)%4<2:put(x,top+2,z,brick)
def stairrun(x,z,y,count,face='north',width=3,material='stone_brick'):
 dx,dz={'north':(0,-1),'south':(0,1),'east':(1,0),'west':(-1,0)}[face]
 for i in range(count):
  for k in range(width):
   a=x+dx*i+(k if dz else 0);c=z+dz*i+(k if dx else 0);yy=y+i
   put(a,yy-1,c,brick);put(a,yy,c,stairs[material,face]);box(a,yy+1,c,a,yy+3,c,0)
wall(lower,108,117);wall(upper,111,123)
for x,z in [(108,112),(113,83),(162,90),(165,124)]:tower(x,z,6,111,123)
# 门楼双塔与拱洞共用厚壳体，入口是预先定义的开口。
for cx in [124,145]:tower(cx,176,5,108,119)
shell('外门楼',128,173,141,180,108,11);door(133,109,173);door(133,109,179);box(130,109,173,138,113,180,0);box(130,116,174,139,116,179,wood)
box(130,117,174,139,119,179,0);box(128,120,173,141,120,180,brick)
for x in range(128,142,3):box(x,121,173,x+1,122,173,brick);box(x,121,180,x+1,122,180,brick)
shell('内门',127,138,140,144,111,11);box(131,112,138,135,116,145,0);box(127,123,138,140,123,144,brick)
for x in range(127,141,3):box(x,124,144,x+1,125,144,brick)
# 两院墙顶上下道，不用梯子替代全部交通。
stairrun(163,162,109,9,'north');box(163,117,153,167,117,154,brick);box(163,118,153,167,120,154,0)
stairrun(111,135,112,12,'north');box(106,123,123,113,123,124,brick);box(106,124,123,113,126,124,0)
# 主塔旧核心，多层木楼板与折返梯，外观矩形并有墙角加厚。
shell('主塔',114,86,135,108,111,31)
for x in [114,133]:
 for z in [86,106]:box(x,112,z,x+2,143,z+2,dress)
for y in [119,127,135,143]:box(116,y,88,133,y,106,wood)
for y in [116,124,132,140]:
 for x in [120,129]:box(x,y,86,x+1,y+2,87,0);box(x,y,107,x+1,y+2,108,0)
door(123,112,107);targets.append(['主塔入口',124,112,105])
for j,y in enumerate([112,120,128,136]):
 x=117 if j%2==0 else 121;z=102 if j%2==0 else 95;face='north' if j%2==0 else 'south';stairrun(x,z,y,8,face,3,'spruce')
 if j%2==0:box(117,y+7,94,123,y+7,94,wood);box(117,y+8,94,123,y+10,94,0)
 else:box(117,y+7,103,123,y+7,104,wood);box(117,y+8,103,123,y+10,104,0)
for x in range(114,136):
 for z in [86,108]:put(x,144,z,brick);put(x,145,z,brick) if x%4<2 else None
for z in range(87,108):
 for x in [114,135]:put(x,144,z,brick);put(x,145,z,brick) if z%4<2 else None
targets += [[f'主塔层{y}',127,y+1,101] for y in [119,127,135,143]]
# 厅堂与小礼拜堂保留不同体量与窗洞语言。
shell('厅堂',145,104,161,133,111,11);roof(145,104,161,133,123);door(145,112,120,'x');targets.append(['厅堂',148,112,121])
for z in [110,117,127]:
 box(145,116,z,146,120,z+1,0);box(160,116,z,161,120,z+1,0)
for z in [105,112,120,131]:box(144,112,z,144,116,z,cobble);put(144,117,z,stairs['stone_brick','east'])
shell('礼拜堂',137,84,149,98,111,8);roof(137,84,149,98,120);door(139,112,97);box(141,114,84,145,117,85,0);targets.append(['礼拜堂',141,112,95])
# 服务建筑以木构与低屋面表达用途；马厩开放的是院内一侧。
shell('马厩',110,149,122,166,108,5,plaster);roof(110,149,122,166,114)
for z in [151,156,161]:door(121,109,z,'x',3,4)
targets.append(['马厩',119,109,158])
shell('厨房',149,150,161,165,108,6);roof(149,150,161,165,115);door(149,109,155,'x');box(157,109,159,159,124,161,brick);targets.append(['厨房',151,109,156])
box(128,111,117,133,113,122,cobble);box(129,112,118,132,113,121,water)
targets += [['外院',136,109,164],['内院',137,112,128],['内墙步道',107,124,123],['外墙步道',164,118,154],['外门通道',134,109,176],['内门通道',133,112,140]]
# 穿塔的墙顶入口按步道标高预留；保留外侧女墙。
for cx,cz in [(108,112),(113,83),(162,90),(165,124)]:
 for x in range(cx-6,cx+7):
  for z in range(cz-6,cz+7):
   if (x-cx)**2+(z-cz)**2<=25:box(x,124,z,x,126,z,0)
# 记录完整结构状态，后续微细节禁止无意改动。
struct=V.copy();before=save('02',before)
protected=V!=0
for x in range(3,253):
 for z in range(3,253):
  h=int(T[x,z]);p=int(V[x,h-Y0,z]);above=int(V[x,h+1-Y0,z]);noise=math.sin(x/9+z/19)+math.cos(z/11-x/21);grain=((x*73856093)^(z*19349663))%1009/1009
  if p!=grass or above!=0:continue
  wooded=any((x-a)**2+(z-c)**2<(r+5)**2 for a,b,c,hh,r,k in trees)
  nearcastle=(95<x<180 and 67<z<198)
  if wooded:
   if noise>-.9:put(x,h,z,coarse)
   if grain<.62:put(x,h+1,z,fern if noise>.0 else short)
   # 林下灌丛必须根接地，并避开道路、城墙与已有树。
   if grain<.035 and noise>.3:
    for dx,dz in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
     a,c=x+dx,z+dz;yy=int(T[a,c])+1
     if V[a,yy-Y0,c]==0 and V[a,yy-Y0-1,c] in [grass,coarse,dirt]:put(a,yy,c,leaf3)
  elif not nearcastle and grain<.58 and noise>-.6:put(x,h+1,z,short)
  elif nearcastle and grain<.09 and noise>0:put(x,h+1,z,short)
  if not wooded and not nearcastle and noise>1.35 and grain<.025:put(x,h+1,z,daisy)
for x,z in [(113,152),(113,161)]:box(x,109,z,x+2,110,z+2,hay)
for x,y,z in [(126,112,105),(147,112,130),(151,109,163),(137,109,171)]:put(x,y,z,torch)
# 栏杆连接状态按实际邻接烘焙。
for x,y,z in np.argwhere(V==fence):
 props={}
 for d,dx,dz in [('east',1,0),('north',0,-1),('south',0,1),('west',-1,0)]:props[d]='true' if 'fence' in P[int(V[x+dx,y,z+dz])] else 'false'
 p=mat('spruce_fence['+','.join(k+'='+v for k,v in sorted({**props,'waterlogged':'false'}.items()))+']',[115,84,53]);V[x,y,z]=p
before=save('03',before)
changes=np.argwhere((V!=struct)&(struct!=0));allowed=[]
for x,y,z in changes:
 a=P[int(struct[x,y,z])];b=P[int(V[x,y,z])]
 if 'grass_block' not in a and 'fence' not in a:allowed.append([int(x),int(y+56),int(z),a,b])
(R/'场景.json').write_text(json.dumps({'world':'MB-V13-T04-山脊城堡','size':[W,H,D],'y0':Y0,'palette':P,'colors':C,'targets':targets,'routes':route,'trees':trees,'envelopes':envelopes,'earthworks':earth,'micro_previous_solid_changes':allowed},ensure_ascii=False,indent=2),encoding='utf8')
print('earth',earth,'unexpected micro replacements',len(allowed),flush=True)
