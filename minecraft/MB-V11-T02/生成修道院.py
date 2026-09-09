"""T02 独立原创几何；输出 Canonical Blueprint，禁止直接写存档。"""
from pathlib import Path
import numpy as np, json, gzip, math, hashlib
ROOT=Path(__file__).parent
W,D,Y0,H=240,220,63,104
V=np.zeros((W,H,D),dtype=np.uint8); P=['minecraft:air']; colors=[[190,215,230]]
def mat(s,c):
 P.append('minecraft:'+s);colors.append(c);return len(P)-1
grass=mat('grass_block[snowy=false]',[106,125,67]);dirt=mat('dirt',[121,91, sixty:=60]);stone=mat('stone',[132,129,119]);rock=mat('andesite',[142,139,128]);rough=mat('cobblestone',[123,120,109]);brick=mat('stone_bricks',[157,151,133]);trim=mat('smooth_sandstone',[198,180,142]);roof=mat('terracotta',[150,85,61]);wood=mat('spruce_planks',[118,88, fifty:=50]);log=mat('oak_log[axis=y]',[101, eighty:=80,47]);leaves=mat('oak_leaves[distance=1,persistent=true,waterlogged=false]',[70,97, fifty]);pine=mat('spruce_leaves[distance=1,persistent=true,waterlogged=false]',[56,85,58]);path=mat('gravel',[165,152,128]);water=mat('water[level=0]',[ sixty,110,142]);slab=mat('stone_brick_slab[type=bottom,waterlogged=false]',[154,149,134]);fence=mat('oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]',[130,101,60]);light=mat('lantern[hanging=false,waterlogged=false]',[228,172,65]);farmland=mat('farmland[moisture=7]',[99, seventy:=70,42]);crop=mat('wheat[age=7]',[174,168,61]);hay=mat('hay_block[axis=y]',[186,157,52]);moss=mat('mossy_cobblestone',[110,118,85]);glass=mat('glass',[164,194,191]);stairs={d:mat(f'stone_brick_stairs[facing={d},half=bottom,shape=straight,waterlogged=false]',[154,149,134]) for d in ['east','west','north','south']}
def put(x,y,z,m):
 if 0<=x<W and Y0<=y<Y0+H and 0<=z<D: V[x,y-Y0,z]=m
def box(x1,y1,z1,x2,y2,z2,m):
 V[max(0,x1):min(W,x2+1),max(0,y1-Y0):min(H,y2-Y0+1),max(0,z1):min(D,z2+1)]=m
def ell(cx,cy,cz,rx,ry,rz,m,seed=0):
 for x in range(math.floor(cx-rx),math.ceil(cx+rx)+1):
  for z in range(math.floor(cz-rz),math.ceil(cz+rz)+1):
   for y in range(math.floor(cy-ry),math.ceil(cy+ry)+1):
    q=((x-cx)/rx)**2+((y-cy)/ry)**2+((z-cz)/rz)**2
    if q<1+0.10*math.sin(x*1.7+z*2.1+y+seed):put(x,y,z,m)
xx,zz=np.meshgrid(np.arange(W),np.arange(D),indexing='ij')
t=63+57*np.exp(-((xx-157)/58)**2-((zz-53)/49)**2)+23*np.exp(-((xx-118)/68)**2-((zz-112)/67)**2)+17*np.exp(-((xx-67)/35)**2-((zz-98)/59)**2)
edge=np.minimum.reduce([xx/20,(239-xx)/20,zz/18,(219-zz)/18,np.ones_like(xx)]).clip(0,1)
t=63+(t-63+2*np.sin(xx/8+zz/17)+1.8*np.sin(zz/8-xx/21))*edge
T=np.maximum(63,np.floor(t)).astype(int)
for x in range(W):
 for z in range(D):
  h=int(T[x,z]);box(x,63,z,x,h,z,stone)
  slope=abs(t[min(x+1,W-1),z]-t[max(0,x-1),z])+abs(t[x,min(z+1,D-1)]-t[x,max(0,z-1)])
  bare=h>116 or (slope>3.6 and z<110)
  box(x,h-1,z,x,h,z,rock if bare else dirt);put(x,h,z,rock if bare else grass)
def pad(x1,z1,x2,z2,y):
 # 台地仅覆盖使用空间；外露挡墙与坡面有真实支承。
 for x in range(x1,x2+1):
  for z in range(z1,z2+1):
   h=int(T[x,z]);box(x,y+1,z,x,max(y+1,h+1),z,0);box(x,63,z,x,y,z,stone)
   if x in (x1,x2) or z in (z1,z2):box(x,max(64,min(h,y)-1),z,x,y,z,rough)
   put(x,y,z,path);T[x,z]=y
pad(104,69,165,94,96);pad(104,95,169,122,94);pad(119,123,156,137,90)
pad(76,126,100,145,82);pad(74,109,87,124,86);pad(61,148,74,158,76)
pad(115,147,146,156,82);pad(122,161,161,170,78)
pad(166,103,178,118,94)
def tree(x,z,height,r,kind,seed):
 y=int(T[x,z])+1
 box(x,y,z,x,y+height-4,z,log)
 for dx,dz,dy in [(-2,1,-3),(2,-1,-2),(1,2,-1)]:
  for k in range(1,4):put(x+round(dx*k/3),y+height-6+k,z+round(dz*k/3),log)
 if kind=='pine':
  ell(x-1,y+height-3,z,r,2.4,r*.8,pine,seed);ell(x+2,y+height-1,z+1,r*.7,2.1,r*.7,pine,seed+2)
 else:
  ell(x-1,y+height-4,z,r,4,r*.9,leaves,seed);ell(x+2,y+height-2,z+2,r*.67,3.2,r*.65,leaves,seed+4)
 return [x,y,z,height,r,kind]
trees=[]
for i,(x,z,h,r,k) in enumerate([(29,166,14,7,'pine'),(38,153,17,8,'pine'),(23,146,13,6,'oak'),(47,141,16,7,'pine'),(34,129,12,7,'oak'),(48,119,15,8,'oak'),(25,117,16,7,'pine'),(64,113,12,6,'oak'),(57,99,17,8,'pine'),(38,97,14,7,'oak'),(51,81,15,7,'pine'),(65,70,12,6,'oak'),(188,92,12,6,'pine'),(200,108,16,8,'pine'),(190,126,15,8,'oak'),(210,137,13,7,'oak'),(188,153,16,8,'pine'),(172,178,13,6,'oak'),(160,190,17,8,'pine'),(147,181,12,6,'oak'),(96,177,13,7,'oak'),(80,187,16,8,'pine'),(66,178,12,6,'oak')]):trees.append(tree(x,z,h,r,k,i))
def save_stage(n,name,prev):
 folder=ROOT/'蓝图'/f'{n:02d}-{name}';folder.mkdir(parents=True,exist_ok=True)
 diff=V!=prev;phases=[];count=0;tilecount=0
 for x in range(0,W,32):
  for y in range(0,H,32):
   for z in range(0,D,32):
    dv=diff[x:x+32,y:y+32,z:z+32]; pts=np.argwhere(dv)
    if not len(pts):continue
    blocks=[[int(a),int(b),int(c),int(V[x+a,y+b,z+c])] for a,b,c in pts]
    bp={'schema_version':1,'origin':{'x':x,'y':y+Y0,'z':z},'dimensions':{'x':min(32,W-x),'y':min(32,H-y),'z':min(32,D-z)},'palette':P,'blocks':blocks,'metadata':{'task':'MB-V11-T02','stage':name}}
    with gzip.open(folder/f'{x}_{y+Y0}_{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
    ops=[]
    # 按同一列的连续方块合并；每条操作与 canonical 单元一一对应。
    for a in range(dv.shape[0]):
     for c in range(dv.shape[2]):
      b=0
      while b<dv.shape[1]:
       if not dv[a,b,c]:b+=1;continue
       e=b;m=int(V[x+a,y+b,z+c])
       while e+1<dv.shape[1] and dv[a,e+1,c] and V[x+a,y+e+1,z+c]==m:e+=1
       ops.append([x+a,Y0+y+b,z+c,x+a,Y0+y+e,z+c,m]);b=e+1
    phases.append({'palette':P,'operations':ops});count+=len(blocks);tilecount+=1
 job={'world_path':WORLD,'phases':phases,'spawn':[25,65,194]}
 if n==1:job['create']={'type':'superflat','seed':2026090902,'generator_options':{'biome':'minecraft:plains','layers':[{'block':'minecraft:bedrock','height':1},{'block':'minecraft:dirt','height':126},{'block':'minecraft:grass_block','height':1}],'structure_overrides':[]}}
 (ROOT/'作业').mkdir(exist_ok=True);(ROOT/'作业'/f'{n:02d}.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8')
 np.save(ROOT/f'阶段{n}.npy',V)
 print(name,count,'voxels',tilecount,'tiles',flush=True)
 return V.copy()
WORLD='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V11-T02-山地修道院'
base=np.zeros_like(V);base[:,0,:]=grass
prev=save_stage(1,'山体台地与结构植被',base)
routes=[]
def route(name,points,width=3):
 cells=[]
 for a,b in zip(points,points[1:]):
  x,y,z=a;X,Y,Z=b;n=max(abs(X-x),abs(Z-z));last=None
  for i in range(n+1):
   q=i/n;cx,cy,cz=round(x+(X-x)*q),round(y+(Y-y)*q),round(z+(Z-z)*q)
   box(cx-width//2,cy+1,cz-width//2,cx+width//2,cy+4,cz+width//2,0)
   for dx in range(-width//2+1,width//2+1):
    for dz in range(-width//2+1,width//2+1):
     box(cx+dx,max(63,min(int(T[cx+dx,cz+dz]),cy)-1),cz+dz,cx+dx,cy,cz+dz,rough);put(cx+dx,cy,cz+dz,path)
   if last and cy>last[1]:
    facing=('east' if cx>last[0] else 'west') if cx!=last[0] else ('south' if cz>last[2] else 'north')
    box(cx-1,cy,cz-1,cx+1,cy,cz+1,stairs[facing])
   last=(cx,cy,cz);cells.append(last)
 routes.append({'name':name,'points':points,'cells':cells})
route('登山主路',[(25,64,194),(43,68,176),(61,76,153),(73,76,153),(82,82,150),(99,86,146),(99,94,110),(110,96,98),(113,96,82)],5)
route('客舍支路',[(82,82,150),(88,82,144),(88,82,137)],3)
route('服务支路',[(99,90,127),(91,88,124),(82,86,124),(82,86,117)],3)
route('生产台地',[(99,86,146),(109,86,150),(115,82,151),(132,82,151),(139,78,164),(150,78,165)],3)
route('东侧泉台',[(149,94,117),(158,94,120),(173,94,115)],3)
def hall(x1,z1,x2,z2,y,h,axis='x'):
 box(x1,y,z1,x2,y,z2,brick);box(x1,y+1,z1,x2,y+h,z2,brick);box(x1+1,y+1,z1+1,x2-1,y+h,z2-1,0)
 # 连续石基、墙带和开敞木屋架；山墙随屋面收分。
 box(x1,y+h,z1,x2,y+h,z2,trim)
 if axis=='x':
  mid=(z1+z2)//2
  for z in range(z1-1,z2+2):
   ry=y+h+1+(min(z-z1+1,z2+1-z)//2)
   box(x1-1,ry,z,x2+1,ry,z,roof)
   if z1<=z<=z2:
    box(x1,y+h+1,z,x1,ry-1,z,brick);box(x2,y+h+1,z,x2,ry-1,z,brick)
  for x in range(x1+4,x2,7):box(x,y+h-1,z1+1,x,y+h-1,z2-1,wood)
 else:
  for x in range(x1-1,x2+2):
   ry=y+h+1+(min(x-x1+1,x2+1-x)//2);box(x,ry,z1-1,x,ry,z2+1,roof)
   if x1<=x<=x2:box(x,y+h+1,z1,x,ry-1,z1,brick);box(x,y+h+1,z2,x,ry-1,z2,brick)
  for z in range(z1+4,z2,7):box(x1+1,y+h-1,z,x2-1,y+h-1,z,wood)
def arch_x(x,z,y,w=3,h=4,depth=1):
 for dz in range(-w//2+1,w//2+1):
  top=y+h-(1 if abs(dz)==w//2 else 0);box(x,y+1,z+dz,x+depth-1,top,z+dz,0)
def arch_z(x,z,y,w=3,h=4,depth=1):
 for dx in range(-w//2+1,w//2+1):
  top=y+h-(1 if abs(dx)==w//2 else 0);box(x+dx,y+1,z,x+dx,top,z+depth-1,0)
# 三廊式教堂：低侧廊、高中央殿、东端弧形后殿。
hall(108,72,156,90,96,10,'x')
hall(108,77,155,85,96,18,'x')
for x in range(114,153,7):
 arch_z(x,77,96,5,10);arch_z(x,85,96,5,10)
 for z in [72,90]:arch_z(x,z,102,1,3)
 for z in [77,85]:arch_z(x,z,108,1,3)
arch_x(108,81,96,5,7,2)
for x in range(155,164):
 for z in range(76,87):
  d=((x-155)/8)**2+((z-81)/5)**2
  if d<=1:
   box(x,96,z,x,108,z,brick);box(x,97,z,x,107,z,0)
   if d>.60:box(x,97,z,x,108,z,brick)
   put(x,109+int((1-d)*4),z,roof)
arch_x(155,81,96,5,8,2)
arch_z(124,90,96,3,5);box(123,95,91,125,95,95,brick);box(123,96,91,125,96,92,stairs['north'])
# 钟塔在西北，外部两段楼梯和内部梯子均提供上达路径。
box(102,96,70,109,127,77,brick);box(103,97,71,108,127,76,0)
for yy in [105,114,123]:
 box(101,yy,69,110,yy,78,trim)
 for xx in [104,107]:arch_z(xx,70,yy,1,3);arch_z(xx,77,yy,1,3)
 for zz in [72,75]:arch_x(102,zz,yy,1,3);arch_x(109,zz,yy,1,3)
box(102,128,70,109,128,77,roof);box(104,129,72,107,129,75,roof)
arch_z(105,77,96,3,4)
ladder=mat('ladder[facing=south,waterlogged=false]',[163,126,66]);box(104,97,71,104,127,71,ladder);box(103,126,72,108,126,76,wood);box(104,126,72,104,127,72,0)
# 回廊是宗教生活的有意规则中心，与外部顺坡格局有区别。
box(120,94,95,153,94,122,brick)
box(125,94,100,148,94,117,grass)
for x in range(121,154):
 for z in range(95,123):
  if x<=124 or x>=149 or z<=99 or z>=118:
   edgeDist=min(x-120,153-x,z-95,122-z)
   put(x,102-max(0,edgeDist//2),z,roof)
for x in range(124,150,5):
 for z in [99,118]:box(x,95,z,x,99,z,trim)
for z in range(99,119,5):
 for x in [124,149]:box(x,95,z,x,99,z,trim)
for x in range(124,150):
 for z in [99,118]:put(x,100,z,trim)
for z in range(99,119):
 for x in [124,149]:put(x,100,z,trim)
# 拱肩填在柱旁，使回廊有连续拱洞而非单纯柱棚。
for x in range(124,149,5):
 for z in [99,118]:put(x+1,99,z,trim);put(x+4,99,z,trim)
for z in range(99,118,5):
 for x in [124,149]:put(x,99,z+1,trim);put(x,99,z+4,trim)
hall(154,95,168,119,94,10,'z');hall(105,100,119,126,94,8,'z');hall(120,124,154,136,90,9,'x')
arch_x(154,107,94,3,5);arch_x(119,108,94,3,5);arch_x(105,108,94,3,5)
arch_z(127,124,90,3,5)
for i in range(5):box(126,94-i,119+i,128,94-i,119+i,stairs['north']);box(126,95-i,119+i,128,99-i,119+i,0)
for x in range(126,152,6):arch_z(x,136,93,1,3)
for z in range(100,118,6):arch_x(168,z,97,1,3)
for z in range(104,125,6):arch_x(105,z,97,1,3)
hall(78,128,97,142,82,7,'x');arch_z(88,142,82,3,4)
hall(75,110,86,121,86,6,'x');arch_z(82,121,86,3,4)
hall(62,149,72,157,76,6,'x');arch_x(62,153,76,5,5);arch_x(72,153,76,5,5)
# 防护墙沿台地边缘，不做对称城堡围墙。
for x in range(109,156):box(x,91,137,x,92,137,rough)
for z in range(96,123):box(170,94,z,170,96,z,rough)
for z in range(96,101):box(104,95,z,104,97,z,rough)
for x in range(106,120):
 if not 110<=x<=116:box(x,96,95,x,98,95,rough)
prev=save_stage(2,'建筑交通与水工',prev)
# 泉台：集水池靠上坡，饮水池和种植地沿下降方向组织。
box(171,94,106,177,95,113,brick);box(172,95,107,176,95,112,water)
box(175,96,105,177,99,106,rough);put(176,97,106,water)
box(172,94,114,174,94,116,brick);box(173,95,114,173,95,116,water)
# 回廊雨水井和四条短步道。
box(135,94,100,137,94,117,path);box(125,94,108,148,94,110,path)
box(134,95,107,138,95,111,trim);box(135,95,108,137,95,110,water)
# 日常劳作空间保持小尺度、有界种植。
for a,b,c,d,y in [(116,148,127,155,82),(133,148,145,155,82),(123,162,137,169,78),(145,162,160,169,78)]:
 box(a,y,b,c,y,d,farmland)
 for x in range(a,c+1):
  for z in range(b,d+1):
   if z==b+3:put(x,y,z,water)
   else:put(x,y+1,z,crop)
for x,z in [(120,155),(135,158),(153,155)]:tree(x,z,7,3,'oak',x)
box(76,87,113,78,88,114,hay)
# 建筑外部扶壁、台阶、照明均服从既定动线。
for x in [112,122,132,142,152]:
 for z in [71,91]:box(x,96,z,x+1,102,z,rough);put(x,103,z,slab)
for x,z,y in [(110,80,97),(110,84,97),(124,97,95),(149,107,95),(88,140,83),(107,107,95),(127,125,91),(66,151,77),(160,119,95)]:put(x,y,z,light)
for z in range(99,118):
 if z not in [105,106,107,108,109]:put(178,95,z,fence)
# 林下斑块只落在缓坡草面，避开建筑、路、生产区。
for x in range(17,219):
 for z in range(35,203):
  y=int(T[x,z]);m=int(V[x,y-Y0,z])
  if m==grass and (x<70 or x>181 or z>179) and math.sin(x*.36+z*.13)+math.sin(z*.29-x*.09)>1.6:
   if (x*19+z*13)%7<3:put(x,y+1,z,leaves)
prev=save_stage(3,'门窗水池与地被',prev)
(ROOT/'场景.json').write_text(json.dumps({'size':[W,H,D],'y0':Y0,'palette':P,'colors':colors,'routes':routes,'trees':trees,'world':WORLD},ensure_ascii=False,indent=2),encoding='utf8')
print('完成生成',flush=True)
