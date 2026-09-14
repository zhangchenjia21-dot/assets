"""等比例区域表达；标签锚点仅用于排版，不是聚落选址。"""
from pathlib import Path
import argparse,json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
P=Path(__file__).resolve().parents[1];a.output.mkdir(parents=True,exist_ok=True)
f=lambda n:ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
ctx=np.load(a.cache/'context-map.npz');reg=np.load(a.cache/'regional-map.npz')
sl=np.s_[1400-1376:2441-1376,-400+800:1281+800]
t=ctx['territory'][sl];y=ctx['height'][sl].astype(float);tc=ctx['terrain'][sl]
W,H=1681,1041;OX,OY=70,145
rgb=np.full((H,W,3),[199,224,231],np.uint8)
for k,c in enumerate([[191,174,214],[201,210,178],[202,204,184],[198,194,185]]):rgb[t==k]=c
shade=np.clip((y-90)*.20,-12,27)
rgb=np.clip(rgb.astype(float)+np.where((t>=0)[...,None],shade[...,None],0),0,255).astype('uint8')
def edge(mask):
 q=np.pad(mask,1);return mask&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
def xy(x,z):return (OX+x+400,OY+z-1400)
colors={'S-W':(187,92,41),'S-U':(118,66,142),'S-T':(30,125,105),'S-V':(50,111,172)}
anchors={'A':(355,1660),'B':(920,1700),'T':(480,1810),'V':(440,2050),'C':(70,1740),'EN':(1130,1760),'ES':(680,2080),'X':(326,2326),'W':(276,2297)}
titles=['01 地形与地表条件','02 推荐区域聚落网络','03 主要流与通达关系','04 层级与近似搜索范围','05 建成集中与开放地逻辑','06 历史生长与路径依赖']
panels=[
 ['历史缓存 / 非当前实存调查','正式中域：391,002 blocks²','中位地表 Y=122','绿色：FLAT / GENTLE 派生分类','灰褐：其它或分类未知','底色明暗：缓存地表高程','西侧低地平缓组：40,631','东北高位平缓组：24,926','两组中位 Y 约 65 / 137','砂面、石面不能视为同种承载地','完整表层统计见 terrain JSON','局部供水 / 人工物仍待核实'],
 ['推荐：两个主要中心 + 两地方点','A 低地综合中心：主中心','吸收门户即时服务，不另复制一镇','B 高位交换中心：第二中心','山地侧交换 + 自身居民日常生活','T 台地：地方生活 / 分段整备','V 南谷：地方生活 / 条件性接近','框线与透明色是搜索范围','未确定中心落点或建成边界','政治访问不强制经过交易','不是每类功能各造一座镇','未来 L2 优先建议 MID-A'],
 ['虚线箭头 = 关系 / 方向假说','CA：共同访问与近界服务','AB：生活品上行 / 加工品下行','AT / TB：台地生活与接近比较','AV：谷地日常供给','BE / VE：东域北向与谷侧交换','VW：有条件 West 直接渡运','X03：实测几何水隙约 56.4 格','细灰线：weight=16 的图实验','不是道路 / 不含权利或净空证明','AB 组边缘间上升仍约 61 格','东域腹地、车行和季节均待证'],
 ['粗边：两个主要中心搜索区','细边：两个地方服务搜索区','S-W：73,566 格；Y50=66','S-U：102,027 格；Y50=137','S-T：32,001 格；Y50=152','S-V：27,513 格；Y50=132','搜索区 ≠ settlement envelope','没有选定镇心、地块或街道','connector 全部纳入低地比较','其地权 / 公共访问不能被吞没','小点可在后续证据下合并降级','全域未覆盖地面仍有区域角色'],
 ['工作建成量级 / LOW confidence','A：16,000–24,000 blocks²','B：10,000–16,000 blocks²','T：2,000–4,000 blocks²','V：1,000–3,000 blocks²','合计：29,000–47,000','占全域：7.42%–12.02%','含内部通行 / 工作共享空间','building footprint 尚未确定','色深只表达集中倾向，不是填充率','开放坡岸 / 生产 / 过渡地不推平','三域同口径密度仍待兄弟案验证'],
 ['历史假说 / 非 Minecraft 施工批次','G-A：地方居民生活与近邻协作','低地 / 高位 / 谷地可各自存在','G-B：重复交换强化低地综合服务','G-C：Commons 稳固后门户服务增长','公共访问与地方权利产生协商','G-D：山地交换增强高位第二中心','减少重复下山，水与燃料仍限量','G-E：成熟网络保留地方缓冲','季节、拥堵、地权可改变分工','不是所有小点由主城扩散生成','若条件不成立可退回单中心备选']]
meta=[]
for i,title in enumerate(titles):
 base=rgb.copy()
 if i==0:base[(t==2)&(tc>0)]=[112,165,110]
 for k,c in [(0,[117,80,155]),(1,[110,130,70]),(2,[38,50,57]),(3,[113,96,86])]:base[edge(t==k)]=c
 im=Image.new('RGB',(2310,1300),'#f6f3ea');im.paste(Image.fromarray(base),(OX,OY));d=ImageDraw.Draw(im)
 d.text((70,25),'CIV-001 Middle L1 | '+title,font=f(34),fill='#24333a')
 d.text((70,83),'同尺度 1 pixel = 1 block  ·  X 向右 / Z 向下  ·  revision154 接受边界  ·  world writes = 0',font=f(22),fill='#40535c')
 if i>0:
  layer=Image.new('RGBA',im.size);ld=ImageDraw.Draw(layer)
  for name,col in colors.items():
   sm=reg[name];rgba=np.zeros((*sm.shape,4),np.uint8);rgba[sm]=(*col,65 if i!=4 else (100 if name in ['S-W','S-U'] else 40));rgba[edge(sm)]=(*col,255)
   layer.alpha_composite(Image.fromarray(rgba),xy(89,1453))
   if i==3 and name in ['S-W','S-U']:
    # 仅加粗搜索边；仍不产生精确聚落边界。
    be=edge(sm);out=np.zeros_like(rgba);out[be]=(*col,255)
    for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:layer.alpha_composite(Image.fromarray(out),(xy(89,1453)[0]+dx,xy(89,1453)[1]+dz))
  im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB');d=ImageDraw.Draw(im)
 def tag(key,text):
  q=xy(*anchors[key]);box=d.textbbox(q,text,font=f(22));d.rectangle((box[0]-4,box[1]-3,box[2]+4,box[3]+3),fill='#fff9ed');d.text(q,text,font=f(22),fill='#273841')
 def arrow(fr,to,label,col='#b44635'):
  x,z=xy(*anchors[fr]);u,v=xy(*anchors[to]);dist=math.hypot(u-x,v-z)
  for start in range(0,int(dist),18):
   end=min(start+10,dist);d.line((x+(u-x)*start/dist,z+(v-z)*start/dist,x+(u-x)*end/dist,z+(v-z)*end/dist),fill=col,width=3)
  angle=math.atan2(v-z,u-x);d.polygon([(u,v),(u-14*math.cos(angle-.4),v-14*math.sin(angle-.4)),(u-14*math.cos(angle+.4),v-14*math.sin(angle+.4))],fill=col)
  q=((x+u)/2,(z+v)/2);d.text(q,label,font=f(19),fill=col,stroke_width=2,stroke_fill='#fff9ed')
 if i in [1,2,5]:
  if i==2:
   analysis=json.loads((P/'evidence/regional-analysis.json').read_text('utf-8'))
   for probe in analysis['probes']:
    if probe['weight']==16 and len(probe['path'])>1:d.line([xy(x,z) for x,z,_ in probe['path']],fill='#888888',width=1)
  for fr,to,label in [('C','A','CA'),('A','B','AB'),('A','T','AT'),('T','B','TB?'),('A','V','AV'),('B','EN','BE?'),('V','ES','VE?'),('V','X','VW?'),('X','W','X03?')]:arrow(fr,to,label)
 if i>0:
  for k,txt in [('A','A · S-W'),('B','B · S-U'),('T','T · S-T'),('V','V · S-V')]:tag(k,txt)
 for q,txt in [((-320,1830),'ALLIANCE COMMONS'),((-360,2100),'WEST'),((1040,2150),'EAST')]:d.text(xy(*q),txt,font=f(22),fill='#566270')
 # 接口逐格取政治相邻关系，不以说明文字的近似范围替代接受几何。
 iz=np.where((t[:,89+400]==2)&(t[:,88+400]==0))[0]
 for z in iz:d.line((*xy(89,int(z)+1400),*xy(89,int(z)+1401)),fill='#a2429a',width=4)
 d.text(xy(-180,1690),'X89 accepted interface',font=f(18),fill='#82357c')
 if i==0:
  for q,txt in [((230,1610),'低地：草地 / 砂面'),((790,1670),'高位：石 / 砂砾'),((390,1840),'小台地'),((460,2080),'南谷缓地')]:d.text(xy(*q),txt,font=f(22),fill='#2b5540',stroke_width=2,stroke_fill='#fff9ed')
 if i==5:
  for q,txt in [((165,1580),'G-A/B 地方生活 → 重复交换'),((95,1770),'G-C 门户服务增强'),((755,1600),'G-A/D 本地生活 → 山地交换强化'),((580,1870),'G-E 分段 / 地方缓冲'),((465,2110),'G-A/E 谷地自存与季节调整')]:d.text(xy(*q),txt,font=f(21),fill='#753425',stroke_width=2,stroke_fill='#fff9ed')
 for x in range(-400,1281,200):d.text((xy(x,1400)[0]-15,1192),str(x),font=f(17),fill='#40535c')
 for z in range(1400,2441,200):d.text((10,xy(-400,z)[1]),str(z),font=f(16),fill='#40535c')
 d.rectangle((OX,OY,OX+W,OY+H),outline='#66747a',width=2)
 d.text((1800,145),'阅读图例与限制',font=f(27),fill='#263a43')
 for j,line in enumerate(panels[i]):d.text((1800,200+49*j),line,font=f(20),fill='#344950')
 d.text((1800,850),'边界：accepted / 不修改领土',font=f(20),fill='#344950')
 d.text((1800,899),'地形：observed / derived cache',font=f(20),fill='#344950')
 d.text((1800,948),'色区：proposal SEARCH AREA',font=f(20),fill='#344950')
 d.text((1800,997),'箭头：relationship，不是路线',font=f(20),fill='#344950')
 d.line((1820,1100,2020,1100),fill='#344950',width=4);d.text((1820,1110),'200 blocks',font=f(20),fill='#344950')
 d.text((70,1230),'NOT_EXISTING_ROAD / NOT_BUILD_FOOTPRINT · 标签为排版锚点，不是聚落坐标 · 待 GPT + Owner 审核',font=f(23),fill='#833d31')
 name=f'{i+1:02d}.png';im.save(a.output/name)
 meta.append(dict(file=name,sha256=hashlib.sha256((a.output/name).read_bytes()).hexdigest(),world_bounds=[-400,1400,1280,2440],pixels_per_block=1,map_origin_px=[OX,OY],label_anchor_semantics='LAYOUT_ONLY_NOT_SITE',proposal_semantics='SEARCH_AREAS_AND_RELATIONSHIPS_ONLY'))
(a.output/'maps.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Rendered six equal-scale regional maps; no world access.')
