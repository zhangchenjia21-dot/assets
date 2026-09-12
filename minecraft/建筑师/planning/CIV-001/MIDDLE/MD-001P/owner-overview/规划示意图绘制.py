"""从已接受领土和规划 RLE 绘制面向 Owner 的说明图；不写世界或改动规划。"""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent; P=OUT.parent; ROOT=P.parents[3]
def read(p):return json.loads(p.read_text(encoding="utf-8"))
doc=read(ROOT/"research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json")
a=np.full((960,1600),255,np.uint8)
for z,l,r,c in doc["runs"]:
 if 1440<=z<2400 and r>=-400 and l<1200:a[z-1440,max(l+400,0):min(r+401,1600)]=c
rgb=np.full((960,1600,3),(211,229,232),np.uint8)
for c,col in [(0,(219,201,147)),(1,(205,213,191)),(2,(173,191,155)),(3,(199,198,185))]:rgb[a==c]=col
colors=[(174,195,148),(132,157,137),(211,181,109),(187,175,139),(222,117,67),(151,112,167),(72,149,154),(148,151,68)]
for zone,col in zip(read(P/"land-use.json")["zones"],colors):
 for z,l,r in zone["geometry"]:rgb[z-1440,l+400:r+401]=col
im=Image.new("RGB",(2240,1440),"#f7f4ec");im.paste(Image.fromarray(rgb),(50,175));d=ImageDraw.Draw(im)
def font(s):return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc",s)
def text(x,y,s,size=24,color="#293c38"):d.text((x,y),s,font=font(size),fill=color,spacing=10)
def pt(p):return (50+p[0]+400,175+p[1]-1440)
text(50,32,"中域 · 聚落与生活网络",48);text(52,101,"一个紧凑主镇，三个常住社区；以地形组织交换，以街院容纳生活。",26)
b=a==2;edge=b&(~np.roll(b,1,0)|~np.roll(b,-1,0)|~np.roll(b,1,1)|~np.roll(b,-1,1))
y,x=np.where(edge)
for yy,xx in zip(y,x):d.point((50+int(xx),175+int(yy)),fill="#485e3d")
net=read(P/"movement-network.json")
for r in net["routes"]:
 points=[pt(p) for p in r["path"]]
 for i in range(0,len(points)-1,14):d.line(points[i:i+9],fill="#247c90",width=4)
nodes=read(P/"settlement-nodes.json")["nodes"]
labels=[("N1 低地混合主镇",(545,250)),("N2 中台工匠社区",(925,490)),("N3 北高台交换镇",(1180,310)),("N4 内谷居民聚落",(970,760))]
for n,(label,loc),col in zip(nodes,labels,colors[4:]):
 q=pt(n["point"]);x,y=loc;w=int(d.textlength(label,font=font(25)))+32
 d.line((q,(x,y+25)),fill="#455e54",width=2);d.rounded_rectangle((x,y,x+w,y+49),radius=9,fill="#fffdf6",outline=col,width=3);text(x+15,y+7,label,25)
 d.ellipse((q[0]-8,q[1]-8,q[0]+8,q[1]+8),fill=col,outline="white",width=3)
text(95,585,"联盟公地",32);text(95,631,"保持独立，不纳入主镇扩张",20)
text(1380,760,"东域山地",30);text(1380,805,"仅显示邻接背景",20)
for it in [net["commons_interface"],*net["east_interfaces"]]:
 q=pt(it["middle_point"]);d.rectangle((q[0]-6,q[1]-6,q[0]+6,q[1]+6),fill="#293c38",outline="white",width=2)
q=pt([326,2326]);d.ellipse((q[0]-7,q[1]-7,q[0]+7,q[1]+7),fill="#247c90");text(q[0]+20,q[1]-15,"南岸条件性渡运点",23);text(q[0]+20,q[1]+25,"背岸陡，保留接口，不设新大镇",19)
text(65,190,"北 ↑   东 →",22);d.line((80,1090,180,1090),fill="#293c38",width=4);text(80,1100,"100 格",19)
text(1700,180,"四个节点，都有人生活",29)
cards=[("01  主镇 / 最高密度","市场 · 商住 · 仓院 · 轻作","旅宿与公共服务交织","窄巷、共享院落、上住下店"),("02  中台 / 工匠家庭","修造 · 轻加工 · 货物整备","粮食铺、日常供应与居民院落","顺台地生长，不削平成大院"),("03  北高台 / 对东交换","仓储 · 旅宿 · 畜力服务","东域货物与日用品在此交换","交换镇也是常住家庭社区"),("04  内谷 / 日常供给","居民 · 工具修理 · 小市场","食物供应与南路中继","保留谷壁与岸坡的自然间隙")]
for i,(head,*lines) in enumerate(cards):
 y=240+i*190;d.rounded_rectangle((1680,y,2190,y+170),radius=12,fill="white");d.rectangle((1680,y+12,1687,y+158),fill=colors[4+i]);text(1710,y+15,head,26)
 for j,line in enumerate(lines):text(1710,y+57+j*33,line,21)
d.rounded_rectangle((1680,1020,2190,1145),radius=12,fill="#f1dfc2");text(1705,1036,"首栋推荐：公共秤验与小仓院",25);text(1705,1080,"在 N1 内另做选址；此图不定建筑位置",20)
text(55,1170,"如何读这张图",29)
legend=[("混合聚落候选面",colors[4]),("生产性开放地",colors[0]),("地形与岸线保留",colors[1]),("连接带与通行预留",colors[2])]
for i,(s,c) in enumerate(legend):
 x=55+i*400;d.rectangle((x,1220,x+22,1242),fill=c);text(x+35,1215,s,22)
text(55,1266,"蓝色虚线 = 交通联系预留，尚非道路。深色小方块 = 跨域接口。聚落实际范围为不规则彩色面。",23)
text(55,1312,"整体更紧凑，不等于处处建满：保留林坡、排水、岸线、小生产与必要公共空间。",24)
text(55,1370,"MD-001P 待审核方案 · revision 154 · 等比例 1 px / block · world writes = 0 · 未进入建筑设计",20,"#67736a")
im.save(OUT/"中域规划示意图.png")
