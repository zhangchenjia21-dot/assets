import os
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
C=Path(os.environ['MID_A_CACHE']);R=Path(os.environ['MID_A_REPO']);O=Path(os.environ['MID_A_OUTPUT']);V=O/'visual';V.mkdir(exist_ok=True)
a=np.load(C/'city-map.npz');obs=json.loads((O/'evidence/current-observation.json').read_text('utf-8'));states=obs['states']
x0,x1,z0,z1=89,435,1550,1860;sl=np.s_[z0-1453:z1-1453+1,0:x1-89+1];height=a['height'][sl];surf=a['surface'][sl];valid=height!=-32768;S=3;OX,OY=70,130;W,H=(x1-x0+1)*S,(z1-z0+1)*S
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
def xy(x,z):return (OX+(x-x0)*S,OY+(z-z0)*S)
def edge(m):
 q=np.pad(m,1);return m&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
base=np.full((*height.shape,3),[228,225,216],np.uint8)
for i,name in enumerate(states):
 color=(163,188,142) if name in ['minecraft:grass_block','minecraft:moss_block'] else (173,151,119) if name in ['minecraft:packed_mud','minecraft:coarse_dirt','minecraft:dirt','minecraft:rooted_dirt','minecraft:podzol'] else (134,180,200) if name=='minecraft:water' else (169,169,162)
 base[surf==i]=color
base=np.clip(base.astype(float)+np.where(valid,np.clip(height.astype(float)-66,-7,14),0)[...,None],0,255).astype(np.uint8)
titles=['01 三个城市范围候选','02 当前地面与浅层限制','03 Anchor 与历史生长','04 主要通达与公共生活','05 城市内部片区形成','06 全城密度与保障空间']
panels=[['C1 门户为核：19,623 格','C2 连续内城：29,175 格（推荐）','C3 更向北展：39,890 格','C1：接口与长存/日常需求竞争','C2：繁华门户 + 稍东综合核心','C3：线路/供水拉长，需求未证','边界是候选，不是历史城墙','北/东为成熟期规划收束','岸侧/高差限制外扩','本轮不把整片 S-W 都城市化'],['刷新：47,704 表层柱 / 226 区块','C2 每柱浅读至地表下 12 格','红：浅层空腔 572 列','蓝：浅层水 797 列','黄：蜂巢所在列 / 调查缓冲','点：剥离树干列，不是清树授权','浅层水不能证明饮用水源','深层箱 / 刷怪笼保留，不挖掘','灰底：未在本轮刷新','快照 2026-09-14 13:30 UTC'],['H0 地方家庭 / 近邻交换','H1 反复交换 → 市场稳定','H2 Commons → 门户繁荣','H3 分户 / 定居 → 门面 / 上层密集','H4 拥堵 / 火水 → 后场分化','门户是强 Anchor，不是另一城','主市场稍东获得分流余地','早期井址未证，不编造水源','方框是活动集中搜索提示','历史是假说，不是施工批次'],['M-GM：门户 与 内城市场','M-IN：内城 与 北东区域接近','M-SERVICE：货物 / 维护后场','M-LIFE：居民持续回家关系','M-REGIONAL：区域输入关系','PS-G：近界让行 / 短停','PS-M：日常市场 / 协商照护','PS-S：后场轮用 / 维护','线为关系，不是道路中心线','车行、地役、季节仍待证'],['三片属于同一座 MID-A 城市','Q-GATE 门户街市：12,786 格','Q-MARKET 内城生活：10,617 格','Q-YARDS 混合后场：5,772 格','每片都有住户 / 交易 / 服务','线是责任 seam，不是用途隔离','片界可协商调整，不照线铺路','后場来自拥堵/污物/装卸需求','市场公地由公共使用约定维持','不划精确街坊 / 地块 / 建筑'],['整城：29,175 格','工作建成空间：22,117 格','非屋顶保留层：7,058 格','屋顶目标整城约 50%–57%','门户片：48%–55%','内城片：60%–67%','后场片：36%–43%','比例分母是各片完整面积','高密来自连续 / 混用 / 上层','联盟最高密度需未来同口径对照']]
colors={'C1_GATEWAY':(40,140,150),'C2_LINKED_CORE':(175,70,50),'C3_NORTH_CORE':(130,80,175),'Q-GATE':(204,133,70),'Q-MARKET':(170,80,87),'Q-YARDS':(92,132,159)}
meta=[]
for i,title in enumerate(titles):
 b=base.copy()
 if i in [4,5]:
  for k in ['Q-GATE','Q-MARKET','Q-YARDS']:
   m=a[k][sl];b[m]=(b[m].astype(float)*.3+np.array(colors[k])*.7).astype(np.uint8)
 if i in [1,5]:
  m=a['reserved'][sl];b[m]=(b[m].astype(float)*.3+np.array([205,202,167])*.7).astype(np.uint8)
 if i==1:
  b[a['void'][sl]]=[205,52,49];b[a['wet'][sl]]=[40,75,200];b[(a['logs'][sl]>0)]=[36,85,45]
 if i==0:
  for k in ['C3_NORTH_CORE','C2_LINKED_CORE','C1_GATEWAY']:b[edge(a[k][sl])]=colors[k]
 else:b[edge(a['city'][sl])]=[103,40,30]
 im=Image.new('RGB',(1720,1160),'#f8f5eb');im.paste(Image.fromarray(b).resize((W,H),Image.Resampling.NEAREST),(OX,OY));d=ImageDraw.Draw(im)
 d.text((70,22),'MID-A L2 | '+title,font=font(32),fill='#293a40');d.text((70,77),'1 block = 3 pixels · X 向右 / Z 向下 · 城市提案 / 非建筑设计 · world writes = 0',font=font(22),fill='#4a5c61')
 def label(pos,text,color='#563a32'):
  d.text(xy(*pos),text,font=font(20),fill=color,stroke_width=2,stroke_fill='#fff9ec')
 def box(bounds,text,col):
  lo,hi,zn,zs=bounds; zz,xx=np.indices(height.shape); mask=a['city'][sl]&(xx+x0>=lo)&(xx+x0<=hi)&(zz+z0>=zn)&(zz+z0<=zs)
  for rz,rx in zip(*np.where(edge(mask))):d.rectangle((OX+int(rx)*S,OY+int(rz)*S,OX+int(rx)*S+2,OY+int(rz)*S+2),fill=col)
  label((lo,zn-9),text,col)
 def arrow(points,col):
  pts=[xy(x,z) for x,z in points]
  for (x,z),(u,v) in zip(pts,pts[1:]):
   dist=math.hypot(u-x,v-z)
   for st in range(0,int(dist),18):
    en=min(st+10,dist);d.line((x+(u-x)*st/dist,z+(v-z)*st/dist,x+(u-x)*en/dist,z+(v-z)*en/dist),fill=col,width=3)
  (x,z),(u,v)=pts[-2:];th=math.atan2(v-z,u-x);d.polygon([(u,v),(u-14*math.cos(th-.4),v-14*math.sin(th-.4)),(u-14*math.cos(th+.4),v-14*math.sin(th+.4))],fill=col)
 if i==0:
  for pos,text,key in [((102,1800),'C1 门户核','C1_GATEWAY'),((287,1810),'C2 推荐','C2_LINKED_CORE'),((355,1570),'C3 北展','C3_NORTH_CORE')]:label(pos,text,'#%02x%02x%02x'%colors[key])
 if i==1:
  box([326,336,1646,1656],'蜂巢保留','#8f731a');label((103,1780),'深层箱 / 刷怪笼 ↓ Y-51');label((280,1780),'岸/浅层风险 → 留空间')
 if i==2:
  box([150,225,1695,1770],'H2 门户繁华','#a25131');box([260,320,1660,1720],'H0/H1 综合核心','#964047');box([250,320,1730,1790],'H4 服务后场','#44667b');label((245,1628),'H3 连续填充 / 分户与共享')
 if i==3:
  rel=json.loads((O/'MOVEMENT-PUBLIC-SPACE-SKELETON.json').read_text('utf-8'))['relations']
  for k,r in enumerate(rel):arrow(r['geometry'],['#a64438','#704678','#466a88','#37826c','#806641'][k])
  for pos,text in [((125,1740),'PS-G'),((275,1675),'PS-M'),((255,1780),'PS-S'),((325,1615),'北东区域关系')]:label(pos,text)
 if i in [4,5]:
  for pos,text in [((135,1720),'Q-GATE 门户'),((263,1680),'Q-MARKET 内城'),((250,1770),'Q-YARDS 后场')]:label(pos,text)
  if i==5:label((282,1820),'斜坡 / 水洞维护，不填满')
 # 直接以revision154已接受X89相邻边绘制；只显示本城一侧。
 context=np.load(Path(os.environ['MID_A_L1_CACHE'])/'context-map.npz')['territory'];zs=np.where((context[:,889]==2)&(context[:,888]==0))[0]+1376
 for zz in zs:d.line((*xy(89,int(zz)),*xy(89,int(zz)+1)),fill='#7938a0',width=5)
 label((95,1650),'X89 · Commons在西侧','#7938a0')
 for xx in range(100,436,50):d.text((xy(xx,z0)[0]-14,1075),str(xx),font=font(17),fill='#4a5c61')
 for zz in range(1550,1861,50):d.text((10,xy(x0,zz)[1]),str(zz),font=font(16),fill='#4a5c61')
 d.rectangle((OX,OY,OX+W,OY+H),outline='#53666d',width=2)
 for n,text in enumerate(panels[i]):d.text((1160,145+n*55),text,font=font(21),fill='#344b55')
 d.text((1160,755),'实线边：精确城市提案成员',font=font(21),fill='#344b55');d.text((1160,805),'虚线：关系 / 非现有道路',font=font(21),fill='#344b55');d.text((1160,855),'框/片界：L2规划 / 非建筑范围',font=font(21),fill='#344b55')
 d.line((1180,970,1330,970),fill='#344b55',width=4);d.text((1180,985),'50 blocks',font=font(20),fill='#344b55')
 d.text((70,1120),'NOT_BUILD_FOOTPRINT / NOT_EXISTING_ROAD · 院落、街坊、建筑与精确道路留给后续授权尺度',font=font(21),fill='#8a4133')
 name=f'{i+1:02d}.png';im.save(V/name);meta.append(dict(file=name,sha256=hashlib.sha256((V/name).read_bytes()).hexdigest(),world_bounds=[x0,z0,x1,z1],pixels_per_block=S,map_origin=[OX,OY],coordinate_semantic='Minecraft block-column X/Z; proposal not construction'))
(V/'maps.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Six city maps rendered')
