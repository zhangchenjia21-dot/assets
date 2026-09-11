"""T07 原创场景；只生成 Canonical Blueprint，不直接写 Minecraft 存档。"""
from pathlib import Path
import numpy as np, math, json
R=Path(__file__).resolve().parent
X,Z,Y0,NY=288,240,12,52
palette=['minecraft:air']; ids={palette[0]:0}
def pid(s):
    s=s if ':' in s else 'minecraft:'+s
    if s=='minecraft:oak_fence':s+='[east=false,north=false,south=false,waterlogged=false,west=false]'
    if s=='minecraft:grass_block':s+='[snowy=false]'
    if any(k in s for k in ['_slab[','_stairs[','_leaves[']) and 'waterlogged=' not in s:s=s[:-1]+',waterlogged=false]'
    if s not in ids: ids[s]=len(palette);palette.append(s)
    return ids[s]
A=np.zeros((NY,Z,X),dtype=np.uint16)
def box(x1,y1,z1,x2,y2,z2,s):
    if x2<x1 or y2<y1 or z2<z1:return
    assert 0<=x1<=x2<X and 0<=z1<=z2<Z and Y0<=y1<=y2<Y0+NY,(x1,y1,z1,x2,y2,z2)
    A[y1-Y0:y2-Y0+1,z1:z2+1,x1:x2+1]=pid(s)
def put(x,y,z,s):box(x,y,z,x,y,z,s)
def line(a,b,s,width=0):
    n=max(abs(b[i]-a[i]) for i in range(3))*2+1
    for t in np.linspace(0,1,n):
        x,y,z=[round(a[i]+(b[i]-a[i])*t) for i in range(3)]
        box(x-width,y,z-width,x+width,y,z+width,s)
def export(stage,old):
    out=R/'蓝图'/stage;out.mkdir(parents=True,exist_ok=True);files=[];count=0
    for y in range(0,NY,16):
      for z in range(0,Z,32):
       for x in range(0,X,32):
        sub=A[y:y+16,z:z+32,x:x+32];prev=old[y:y+16,z:z+32,x:x+32]
        yy,zz,xx=np.where(sub!=prev)
        if not len(xx):continue
        used=sorted(set(int(v) for v in sub[yy,zz,xx]));mapping={p:i for i,p in enumerate(used)}
        rows=[[int(a),int(b),int(c),mapping[int(d)]] for a,b,c,d in zip(xx,yy,zz,sub[yy,zz,xx])]
        bp={'schema_version':1,'origin':{'x':x,'y':y+Y0,'z':z},'dimensions':{'x':sub.shape[2],'y':sub.shape[0],'z':sub.shape[1]},'palette':[palette[i] for i in used],'blocks':rows,'metadata':{'name':'T07-'+stage,'source_kind':'AI_ORIGINAL','content_omissions':[]}}
        f=f'{x}-{y+Y0}-{z}.json';(out/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f);count+=len(rows)
    (out/'清单.json').write_text(json.dumps({'stage':stage,'files':files,'specified_blocks':count},ensure_ascii=False),encoding='utf8')
    np.savez_compressed(R/f'方案-{stage}.npz',blocks=A,palette=palette)
    print(stage,count,len(files),flush=True)

# 已创建画布为 y=15 沙面。核心砾质冲积缓坡自然连接北侧岩脊与外围沙地。
box(0,12,0,287,15,239,'sand');baseline=A.copy()
H=np.zeros((Z,X),dtype=int)
def smooth(v):return max(0,min(1,v))**2*(3-2*max(0,min(1,v)))
for z in range(Z):
 for x in range(X):
    core=min(smooth((x-18)/30),smooth((268-x)/28),smooth((z-35)/30),smooth((220-z)/25))
    h=15+5*core
    # 两段风蚀岩脊、鞍部和南向冲蚀沟；非同心等高台地。
    ridge=17*math.exp(-((x-85)/66)**4-((z-28-0.14*(x-80))/16)**2)
    ridge+=8*math.exp(-((x-179)/29)**2-((z-36)/18)**2)
    gully=7*math.exp(-((x-(116+0.42*(z-25)))/8)**2-((z-35)/29)**2)
    h+=max(0,ridge-gully)
    dune=5*math.exp(-((x-24-0.13*z)/18)**2-((z-168)/45)**2)+4*math.exp(-((x-250)/17)**2-((z-95)/44)**2)
    h+=dune
    edge=min(smooth(x/12),smooth((287-x)/12),smooth(z/10),smooth((239-z)/10));h=round(15+(h-15)*edge)
    H[z,x]=h
    if h>15:box(x,16,z,x,h,z,'sandstone')
    surf='sand'
    if 65<z<200 and 55<x<225:surf='coarse_dirt' if ((x-90)/53)**2+((z-132)/65)**2<1 else 'sandstone'
    if z<61 and h>24:surf='sandstone'
    put(x,h,z,surf)
    if surf=='sand' and h>16:put(x,h-1,z,'sand')
# 核心只需小规模找平，不额外抬高建筑。
box(137,16,71,216,20,146,'sandstone')

# 坎儿井末段，近水平微坡在格点尺度下简化；水池及农渠均封闭床岸。
box(88,18,29,92,21,94,'cut_sandstone');box(89,19,29,91,20,94,'air');box(89,19,29,91,19,94,'water[level=0]')
for z in [34,57,77]:
    h=max(int(H[z,90]),22)
    box(88,20,z-2,92,h,z+2,'sandstone');box(89,20,z-1,91,h,z+1,'air')
    box(88,h+1,z-2,92,h+1,z+2,'cut_sandstone');box(89,h+1,z-1,91,h+1,z+1,'oak_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]')
for z in range(85,132):
 for x in range(66,113):
    d=((x-90)/18)**2+((z-108)/22)**2
    if d<1.15:box(x,16,z,x,20,z,'sandstone')
    if d<1:box(x,17,z,x,19,z,'water[level=0]');put(x,20,z,'air')
# 分水干渠从池南端到田间，底岸连续；阀门关闭的末端不伪造水流。
box(88,18,127,92,20,190,'cut_sandstone');box(89,19,127,91,19,189,'water[level=0]');box(89,20,127,91,20,189,'air')
for z in [147,160,174,187]:
    box(58,18,z-1,112,20,z+1,'cut_sandstone');box(59,19,z,111,19,z,'water[level=0]');box(59,20,z,111,20,z,'air')
# 靠近水源的生活取水台与封闭式储水屋。
box(107,19,111,128,20,122,'cut_sandstone')
box(114,17,102,128,24,112,'sandstone');box(116,18,104,126,22,110,'air');box(116,18,104,126,19,110,'water[level=0]')
for y,r in [(25,7),(26,6),(27,5),(28,4),(29,2)]:
 for z in range(100,115):
  for x in range(114,129):
   if (x-121)**2+(z-107)**2<=r*r:put(x,y,z,'smooth_sandstone')
box(119,21,112,123,23,114,'sandstone');box(120,21,112,122,22,114,'air')
box(114,20,115,116,21,119,'cut_sandstone');put(115,21,117,'water[level=0]')

# 驿站四翼主量：南门、环廊与内院，先有结构再加分间。
box(139,20,74,214,20,141,'cut_sandstone')
for b in [(139,74,214,87),(139,88,151,128),(202,88,214,128),(139,129,214,141)]:
 x1,z1,x2,z2=b;box(x1,21,z1,x2,28,z2,'sandstone');box(x1+2,21,z1+2,x2-2,27,z2-2,'air')
box(152,20,88,201,20,128,'sand')
box(172,21,133,183,36,145,'cut_sandstone');box(175,21,132,180,29,145,'air')
# 北侧主伊万空腔与厚拱口。
box(170,21,84,184,32,94,'sandstone');box(173,21,86,181,29,94,'air')

trees=[]
def palm(x,z,h,lean,az):
    ground=int(H[z,x]);ground=20 if 50<x<135 and 80<z<195 else ground
    box(x,16,z,x,ground,z,'coarse_dirt')
    top=(x+lean,ground+h,z)
    line((x,ground+1,z),top,'jungle_log[axis=y]')
    put(*top,'jungle_wood[axis=y]')
    # 羽状叶由上扬中轴转为下垂，区别于球状阔叶树冠。
    for n in range(7):
        a=az+n*math.tau/7;length=5+(n%3)
        prev=top
        for j in range(1,length+1):
            end=(round(top[0]+j*math.cos(a)),round(top[1]+2*math.sin(math.pi*j/length)-j*0.38),round(top[2]+j*math.sin(a)))
            line(prev,end,'jungle_leaves[persistent=true,distance=1]');prev=end
            if 2<=j<length:
                for side in [-1,1]:
                    put(end[0]+round(math.cos(a+side*math.pi/2)),end[1],end[2]+round(math.sin(a+side*math.pi/2)),'jungle_leaves[persistent=true,distance=1]')
    trees.append({'x':x,'y':ground,'z':z,'height':h,'lean':lean,'azimuth':az})
for i,(x,z,h,l) in enumerate([(60,91,12,1),(68,82,14,-1),(77,75,11,1),(107,80,14,1),(119,88,11,-1),(56,111,13,1),(63,127,12,-1),(75,139,14,1),(105,135,12,-1),(122,139,13,1),(54,149,11,1),(67,153,13,-1),(79,162,12,1),(106,156,14,-1),(118,173,12,1),(72,179,14,1),(99,181,13,-1),(54,176,11,1),(130,157,12,1),(133,120,12,-1)]):palm(x,z,h,l,i*.63)
export('01-Macro',baseline);old=A.copy()

# Macro 实存审计修订：支渠岸壁曾截断干渠，池岸曾封住引水末端。
box(89,19,83,91,19,189,'water[level=0]');box(89,20,83,91,20,189,'air')
# 将北脊切成有支沟及裸岩肩的地貌，打断大范围连续等高层。
gullies=[[(41,18),(48,34),(58,51),(67,65)],[(115,15),(119,30),(132,48),(147,66)],[(163,20),(158,36),(169,54)]]
for z in range(13,67):
 for x in range(30,204):
    h=int(H[z,x]);dist=999
    for pts in gullies:
     for a,b in zip(pts,pts[1:]):
      vx,vz=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*vx+(z-a[1])*vz)/(vx*vx+vz*vz)))
      dist=min(dist,math.hypot(x-a[0]-t*vx,z-a[1]-t*vz))
    cut=round(max(0,5-dist)*max(0,h-19)/11)
    if cut and not 87<=x<=93:
      nh=max(18,h-cut);box(x,nh+1,z,x,h,z,'air');put(x,nh,z,'gravel' if nh<23 else 'cut_sandstone');H[z,x]=nh

# 南北厢房保留室内横向通路；东西翼客房从庭院拱廊进入。
for z in [89,99,109,119]:
    for west in [True,False]:
        x1,x2=(139,151) if west else (202,214)
        box(x1+1,21,z,x2-1,27,z,'sandstone')
        xdoor=150 if west else 203
        box(xdoor,21,z+3,xdoor+1,23,z+5,'air') if west else box(xdoor-1,21,z+3,xdoor,23,z+5,'air')
        # 内向浅拱廊柱列与压顶；拱下通行不碰客房围护。
        px=154 if west else 199
        box(min(px,xdoor),28,z,max(px,xdoor),28,z+9,'smooth_sandstone')
        box(px,21,z,px,26,z,'cut_sandstone')
        box(px,27,z,px,27,z+2,'smooth_sandstone')
        box(px,27,z+7,px,27,z+9,'smooth_sandstone')
        box(px,26,z+1,px,26,z+1,'smooth_sandstone')
        box(px,26,z+8,px,26,z+8,'smooth_sandstone')
        # 厚窗洞不穿入交通路径。
        outer=139 if west else 214
        box(outer,24,z+4,outer,25,z+5,'air')
for x in [141,151,161,188,198,208]:
    box(x,21,129,x,27,140,'sandstone')
    box(x+3,21,128,x+5,24,130,'air')
# 后部通长厩棚与端口，院内可绕主伊万从两端进入。
for x in [145,156,194,205]:box(x,21,85,x+3,24,88,'air')
for x in range(145,211,8):
    box(x,21,76,x,23,80,'oak_fence')
    box(x+1,21,76,x+4,21,76,'hay_block[axis=y]')
# 明确的桶拱屋顶：南北翼横向长拱，东西翼分间低拱。
for x in range(140,214):
 for z in range(75,86):
    y=28+round(3*math.sqrt(max(0,1-((z-80)/5.5)**2)))
    box(x,28,z,x,y,z,'terracotta')
for x1,x2 in [(140,151),(202,213)]:
 for x in range(x1,x2+1):
    y=28+round(2*math.sqrt(max(0,1-((x-(x1+x2)/2)/6)**2)))
    box(x,28,88,x,y,128,'terracotta')
for x1,x2 in [(140,171),(184,213)]:
    box(x1,28,130,x2,28,140,'terracotta')
    box(x1,29,140,x2,29,141,'smooth_sandstone_slab[type=bottom]')
# 门楼阶梯尖拱，上部开口两侧实墙；检验主入口始终 6 格宽。
box(175,21,128,180,29,145,'air')
for y,w in [(30,6),(31,4),(32,2)]:
    x=178-w//2;box(x,y,133,x+w-1,y,145,'air')
box(171,37,132,184,37,146,'smooth_sandstone_slab[type=bottom]')
for x in [171,184]:box(x,21,132,x,36,146,'smooth_sandstone')
for y in [24,29,34]:
    box(173,y,145,174,y+1,145,'chiseled_sandstone');box(181,y,145,182,y+1,145,'chiseled_sandstone')
for x in range(139,215,10):
    for z in [73,142]:box(x,21,z,x+1,26,z,'cut_sandstone')
# 从院中沿南翼外侧登上屋面，避免在客房隔墙内穿梯。
for i in range(8):
    if i:box(156+i,21,123,156+i,20+i,126,'sandstone')
    box(156+i,21+i,123,156+i,21+i,126,'sandstone_stairs[facing=east,half=bottom,shape=straight]')
box(164,28,123,167,28,132,'terracotta')

def road(points,width):
    for a,b in zip(points,points[1:]):
      n=max(abs(a[0]-b[0]),abs(a[1]-b[1]))*2+1
      for t in np.linspace(0,1,n):
       x,z=[round(a[i]+(b[i]-a[i])*t) for i in range(2)]
       for dz in range(-width,width+1):
        for dx in range(-width,width+1):
         if dx*dx+dz*dz>(width+.5)**2:continue
         xx,zz=x+dx,z+dz;h=int(H[zz,xx]);put(xx,h,zz,'packed_mud')
    # 无全包络清空，避免后施工道路切割建筑或树冠。
road([(256,231),(232,205),(214,175),(192,158),(178,149)],3)
road([(192,158),(223,155),(250,149),(279,144)],3)
road([(177,149),(166,153),(155,174),(132,181)],2)
road([(166,153),(143,139),(121,124),(109,119)],2)
road([(129,179),(115,184),(97,197),(72,195),(58,182)],2)
road([(66,133),(56,120),(53,96),(63,72),(73,61)],1)
# 门槛与院内主线固定标高，保留主入口；院中自由卸货空间。
box(175,20,129,180,20,150,'cut_sandstone')
box(173,20,93,181,20,129,'packed_mud')
box(155,20,104,198,20,110,'packed_mud')

def house(x,z,w,d,h,doorx):
    box(x,20,z,x+w,20,z+d,'cut_sandstone');box(x,21,z,x+w,20+h,z+d,'sandstone')
    box(x+1,21,z+1,x+w-1,19+h,z+d-1,'air');box(x,20+h,z,x+w,20+h,z+d,'terracotta')
    box(doorx,21,z+d,doorx+2,23,z+d,'air')
    for xx in [x,x+w]:box(xx,21,z,xx,20+h,z,'cut_sandstone')
    box(x,21+h,z,x+w,21+h,z,'sandstone_slab[type=bottom]')
# 管理/维修组合与带敞棚工院，尺度形态不同于主驿站。
house(137,161,13,13,6,142)
box(137,21,175,137,24,181,'stripped_jungle_log[axis=y]');box(150,21,175,150,24,181,'stripped_jungle_log[axis=y]')
box(137,25,175,150,25,181,'jungle_slab[type=bottom]')
house(116,186,17,11,5,122)
# 烤炉为厚小拱，不是同一住宅模板缩放。
box(126,21,181,131,23,185,'bricks');box(127,24,182,130,24,184,'bricks');box(128,21,185,129,22,185,'air');box(127,25,182,127,27,182,'bricks')
# 南门前市集三片不同长度的张布荫棚，杆与横梁明确。
for x,z,w,d in [(156,162,10,6),(167,179,13,5),(192,170,11,7)]:
    for xx in [x,x+w]:
      for zz in [z,z+d]:box(xx,21,zz,xx,25,zz,'oak_fence')
    for xx in range(x,x+w+1):
      yy=26+(1 if 2<xx-x<w-2 else 0)
      box(xx,yy,z,xx,yy,z+d,'white_wool' if xx%5 else 'brown_wool')
    box(x,25,z,x+w,25,z,'stripped_jungle_log[axis=x]');box(x,25,z+d,x+w,25,z+d,'stripped_jungle_log[axis=x]')
    box(x+2,21,z+1,x+w-2,21,z+1,'jungle_planks')
# 外驮畜饮水槽与拴系围场，与上游生活水池独立，人工搬水补充。
box(213,20,168,227,21,174,'cut_sandstone');box(215,21,169,225,21,172,'water[level=0]')
for z in [180,195]:box(205,21,z,229,21,z,'oak_fence')
box(229,21,180,229,21,195,'oak_fence');box(205,21,185,205,21,195,'oak_fence')
box(224,21,190,227,22,193,'hay_block[axis=y]')
# 灌溉畦块：窄水渠分配、可跨越的桥板和作物，不改树干。
for z1,z2 in [(149,158),(162,172),(176,185)]:
 for x1,x2 in [(59,85),(95,111)]:
  for z in range(z1,z2+1):
   for x in range(x1,x2+1):
    if A[21-Y0,z,x]==0:
      put(x,20,z,'farmland[moisture=7]')
      if (x-x1)%4!=3:put(x,21,z,'wheat[age=7]' if z1!=162 else 'carrots[age=7]')
for z in [142,167,193]:box(87,20,z,93,20,z+2,'jungle_slab[type=top]')
# 宽畦中补一条薄支渠，让耕作格到灌水不超过四格。
for z in [153,167,181]:
    box(58,18,z,112,18,z,'cut_sandstone');box(59,19,z,111,19,z,'water[level=0]');box(59,20,z,111,21,z,'air')
    box(59,20,z-1,111,20,z-1,'cut_sandstone');box(59,20,z+1,111,20,z+1,'cut_sandstone')
    box(59,21,z-1,111,21,z-1,'air');box(59,21,z+1,111,21,z+1,'air')
box(89,19,127,91,19,189,'water[level=0]')
for z in [142,167,193]:box(87,20,z,93,20,z+2,'jungle_slab[type=top]')
# 支渠从树根下侧通过；保留根盘和原来的低段树干，不以清理作物破坏树木。
for t in trees:
    x,z=t['x'],t['z'];put(x,20,z,'coarse_dirt')
    for y in range(21,24):put(x,y,z,'jungle_log[axis=y]')
export('02-Meso',old);old=A.copy()

# 地表遵从使用与湿度，避免全图撒花。枯灌木用于外围，草本只在水岸。
for z in range(14,228):
 for x in range(14,276):
    h=int(H[z,x]);v=(x*71+z*113+x*z*7)%103
    if A[h+1-Y0,z,x]!=0:continue
    if (x<48 or x>241 or z<64) and v==0 and A[h-Y0,z,x] in [pid('sand'),pid('sandstone')]:put(x,h+1,z,'dead_bush')
    d=((x-90)/18)**2+((z-108)/22)**2
    if 1.17<d<1.55 and x<106 and v<48 and A[20-Y0,z,x]==pid('coarse_dirt'):
      put(x,20,z,'grass_block');put(x,21,z,'short_grass' if v%3 else 'fern')
# 浅色墙脚、窗框、屋面雨口及局部修补；材料按构造分配。
for z in range(75,141):
 for x in [139,214]:
    put(x,21,z,'cut_sandstone')
for x in range(143,213,10):
    box(x,29,74,x+1,29,74,'sandstone_slab[type=bottom]')
for z in [94,104,114,124]:
    for x in [139,214]:
        for dz in [-1,2]:box(x,24,z+dz,x,25,z+dz,'smooth_sandstone')
        box(x,26,z-1,x,26,z+2,'smooth_sandstone_slab[type=bottom]')
# 货物、干草、坐席和低层照明，在已验证的使用空间内。
for x,z in [(158,96),(193,117),(145,177),(171,180),(197,171),(207,80)]:
    box(x,21,z,x+2,22,z+1,'hay_block[axis=y]')
for x,z in [(160,122),(186,122),(158,90),(191,90)]:box(x,21,z,x+3,21,z,'smooth_sandstone_slab[type=bottom]')
for x,z in [(174,147),(182,147),(154,95),(199,115),(143,158),(125,123),(116,182)]:
    box(x,21,z,x,23,z,'oak_fence');put(x,24,z,'torch')
export('03-Micro',old)
old=A.copy()
# 实存六邻接检查发现倾斜树干、羽叶步进及棚布折高只有角接触。
# 对原有同一条线做正交接缝补齐，不以删除树冠掩盖断裂。
def line(a,b,s,width=0):
    n=max(abs(b[i]-a[i]) for i in range(3))*2+1;prev=list(a)
    for t in np.linspace(0,1,n):
        end=[round(a[i]+(b[i]-a[i])*t) for i in range(3)]
        for axis in range(3):
            while prev[axis]!=end[axis]:
                prev[axis]+=1 if end[axis]>prev[axis] else -1
                put(*prev,s)
        put(*end,s)
original_trees=list(trees);trees=[]
for t in original_trees:palm(t['x'],t['z'],t['height'],t['lean'],t['azimuth'])
# 羽片侧支也用边连接，避免仅在角上接触主叶轴。
for t in trees:
    top=(t['x']+t['lean'],t['y']+t['height'],t['z'])
    for n in range(7):
      a=t['azimuth']+n*math.tau/7;length=5+n%3
      for j in range(2,length):
        end=(round(top[0]+j*math.cos(a)),round(top[1]+2*math.sin(math.pi*j/length)-j*.38),round(top[2]+j*math.sin(a)))
        for side in [-1,1]:
          tip=(end[0]+round(math.cos(a+side*math.pi/2)),end[1],end[2]+round(math.sin(a+side*math.pi/2)))
          line(end,tip,'jungle_leaves[persistent=true,distance=1]')
for x,z,w,d in [(156,162,10,6),(167,179,13,5),(192,170,11,7)]:
    box(x,26,z+d//2,x+w,26,z+d//2,'stripped_jungle_log[axis=x]')
# 栏杆原生连接状态按现场相邻支承烘焙，单根荫棚柱不生成横向虚接。
fences=np.where(np.isin(A,[i for i,s in enumerate(palette) if s.startswith('minecraft:oak_fence[')]))
for y,z,x in zip(*fences):
    props={}
    for name,dx,dz in [('east',1,0),('north',0,-1),('south',0,1),('west',-1,0)]:
      neighbor=palette[A[y,z+dz,x+dx]].split('[')[0]
      props[name]='true' if neighbor not in ['minecraft:air','minecraft:water','minecraft:torch'] else 'false'
    put(int(x),int(y+Y0),int(z),'oak_fence['+','.join(k+'='+v for k,v in props.items())+',waterlogged=false]')
export('04-Repair',old)
old=A.copy()
# 复种树干时根盘填土截住两处暗渠；只恢复根盘下一格水道，保留上部根盘。
for x,z in [(67,153),(99,181)]:put(x,19,z,'water[level=0]')
export('05-Water',old)
(R/'树木候选.json').write_text(json.dumps(trees,indent=2),encoding='utf8')
(R/'调色板.json').write_text(json.dumps(palette,indent=2),encoding='utf8')
np.save(R/'设计地面.npy',H)
