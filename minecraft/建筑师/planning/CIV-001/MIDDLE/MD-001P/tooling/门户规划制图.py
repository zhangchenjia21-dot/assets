"""只读取当前规划数据和既有地形缓存，绘制 R1 全域及门户局部等比例图。"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[3]
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def font(s):return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',s)
X0,Z0=-400,1440
a=np.full((960,1600),255,np.uint8)
territory=json.loads((ROOT/'research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json').read_text(encoding='utf-8'))
for z,l,r,c in territory['runs']:
    if 1440<=z<2400 and l<1200 and r>=-400:a[z-1440,max(l+400,0):min(r+401,1600)]=c
def mask(runs):
    m=np.zeros(a.shape,bool)
    for z,l,r in runs:m[z-Z0,l-X0:r-X0+1]=True
    return m
sub=read('subareas.json')['subareas'];nodes=read('settlement-nodes.json')['nodes'];net=read('movement-network.json')
land=read('land-use.json');intensity=read('human-use-intensity.json');evidence=read('validation/gateway-evidence.json')
lu=np.zeros(a.shape,np.uint8);iv=np.zeros(a.shape,np.uint8);sa=np.zeros(a.shape,np.uint8)
for s in land['zones']:lu[mask(s['geometry'])]=s['code']
for s in intensity['zones']:iv[mask(s['geometry'])]=s['code']
for i,s in enumerate(sub,1):sa[mask(s['geometry'])]=i
pal=np.array([(210,227,231),(177,198,153),(130,153,137),(216,185,115),(170,178,143),(221,127,74),(162,125,177),(80,155,163),(158,160,80),(194,78,116)],np.uint8)
dp=np.array([(130,153,137),(177,198,153),(216,185,115),(214,125,106),(237,103,57)],np.uint8)
base=np.full((*a.shape,3),(210,227,231),np.uint8)
for c,col in [(0,(220,202,151)),(1,(207,215,191)),(2,(177,198,153)),(3,(199,199,187))]:base[a==c]=col
terrain=np.load('D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001P/terrain.npz')['y'][64:1024,400:2000]
value=np.clip((terrain-60)/130,0,1)
terrain_rgb=np.stack((91+value*124,163-value*67,133-value*58),axis=2).astype(np.uint8)
titles={'terrain-base':'地形底图','planning-subareas':'规划子区','settlement-hierarchy':'主镇与门户聚落层级','movement-exchange':'门户 → 主镇交换链','land-use-masterplan':'混合土地使用','human-use-density':'使用强度与密度','phasing-first-build':'分期与首栋推荐'}
nodecolors={n['id']:tuple(pal[5+i]) for i,n in enumerate(nodes)}
def text(d,xy,s,size=21,fill='#293d37'):d.text(xy,s,font=font(size),fill=fill,spacing=8)
def draw_map(rgb,title,kind):
    im=Image.new('RGB',(2180,1220),'#f6f3eb');im.paste(Image.fromarray(rgb),(50,145));d=ImageDraw.Draw(im)
    text(d,(50,22),'MD-001P-R1 · '+title,38);text(d,(50,80),'P1 不只是通道：G1 门户常住社区，与 N1 主镇互补',25)
    def pt(p):return 50+p[0]+400,145+p[1]-1440
    m=a==2;edge=m&(~np.roll(m,1,0)|~np.roll(m,-1,0)|~np.roll(m,1,1)|~np.roll(m,-1,1))
    for z,x in zip(*np.where(edge)):d.point((50+int(x),145+int(z)),fill='#50653e')
    if kind not in ('terrain-base','planning-subareas','human-use-density'):
        for r in net['routes']:
            pts=[pt(p) for p in r['path']]
            for i in range(0,len(pts)-1,14):d.line(pts[i:i+9],fill='#267b91',width=3)
    label_positions=[(790,280),(960,535),(1325,300),(960,780),(440,475)]
    for n,loc in zip(nodes,label_positions):
        p=pt(n['point']);label=n['id']+' '+('门户街市' if n['id']=='G1' else {'N1':'低地混合主镇','N2':'中台工匠社区','N3':'北高台交换镇','N4':'内谷居民聚落'}[n['id']]);w=int(d.textlength(label,font=font(22)))+24
        d.line((p,loc),fill='#3c5145',width=2);d.rounded_rectangle((*loc,loc[0]+w,loc[1]+42),radius=6,fill='white',outline=nodecolors[n['id']],width=2);text(d,(loc[0]+12,loc[1]+5),label,22)
        d.ellipse((p[0]-6,p[1]-6,p[0]+6,p[1]+6),fill=nodecolors[n['id']],outline='white',width=2)
    for it in [net['commons_interface'],*net['east_interfaces']]:
        p=pt(it['middle_point']);d.rectangle((p[0]-5,p[1]-5,p[0]+5,p[1]+5),fill='#263d34')
    text(d,(100,660),'联盟公地 · 不扩入',23);text(d,(1360,835),'东域背景',23)
    text(d,(1700,145),'G1 → N1 双节点',28)
    legends={
        'land-use-masterplan':[(s['name'],tuple(pal[s['code']])) for s in land['zones']],
        'human-use-density':[(s['name'],tuple(dp[s['code']])) for s in intensity['zones']],
        'planning-subareas':[(s['id']+' '+s['name'],tuple(pal[i+1])) for i,s in enumerate(sub)],
        'phasing-first-build':[('F0 审核；不自动启动 Site Gate','#78877b'),('F1 G1 共享周转与生活院',nodecolors['G1']),('F2 G1 + N1 逐院生长',nodecolors['N1']),('F3 N2 / N3 次级社区',nodecolors['N2']),('F4 N4 与条件性南岸',nodecolors['N4'])]
    }
    entries=legends.get(kind,[(n['id']+' '+n['name'],nodecolors[n['id']]) for n in nodes])
    for i,(label,col) in enumerate(entries):
        yy=205+i*52;d.rectangle((1700,yy+6,1717,yy+23),fill=col);text(d,(1730,yy),label,19)
    yy=740
    for line in ['G1：短交易、短仓、饮食旅宿','修理、日用品与经营家庭生活','N1：更完整市场、较大仓储','加工、公共生活与长期商业','阈值零建筑；穿行净空另保护','蓝虚线为预留，非现有道路','首栋仅推荐，不定建筑位置']:
        text(d,(1700,yy),line,20);yy+=40
    if kind=='terrain-base':text(d,(1700,665),'高程 Y60 绿 → Y190+ 棕',20)
    text(d,(70,165),'北 ↑  东 →',20);d.line((75,1060,175,1060),fill='#293d37',width=4);text(d,(75,1072),'100 blocks',18)
    text(d,(50,1145),'revision154 · 391,002 格中域 · 1 px/block · 待 GPT + Owner 审核 · world writes = 0',22)
    return im

for kind,title in titles.items():
    rgb=base.copy();m=a==2
    if kind=='terrain-base':rgb[m]=terrain_rgb[m]
    elif kind=='planning-subareas':rgb[m]=pal[sa[m]]
    elif kind=='human-use-density':rgb[m]=dp[iv[m]]
    else:
        rgb[m]=pal[lu[m]]
        if kind=='phasing-first-build':
            rgb[mask(nodes[2]['envelope'])]=pal[6]
    draw_map(rgb,title,kind).save(OUT/'visual'/(kind+'.png'))

# 门户局部图突出零建筑阈值与净空；同一 X/Z 比例，所有填色仍来自精确 RLE。
rgb=base.copy();rgb[a==2]=pal[lu[a==2]];clear=mask(land['building_exclusion_overlays'][0]['geometry'])
zz,xx=np.indices(a.shape);rgb[clear&((xx+zz)%8<2)]=(55,108,116)
im=Image.new('RGB',(1900,1220),'#f6f3eb');scale=2.5;ox,oy=70,160;wx,wz=70,1500
im.paste(Image.fromarray(rgb[60:440,470:850]).resize((950,950),Image.Resampling.NEAREST),(ox,oy));d=ImageDraw.Draw(im)
text(d,(55,25),'P1 门户街市与 N1 主镇 · 局部关系',38);text(d,(55,87),'真实规划轮廓 / 通行净空 / 常住生活分工',25)
def pt(p):return ox+(p[0]-wx)*scale,oy+(p[1]-wz)*scale
for r in net['routes'][:2]:
    pts=[pt(p) for p in r['path']]
    for i in range(0,len(pts)-1,10):d.line(pts[i:i+6],fill='#166b87',width=4)
for n in [nodes[0],nodes[-1]]:
    x,z=pt(n['point']);d.ellipse((x-9,z-9,x+9,z+9),fill='white',outline='#304434',width=2);text(d,(x+16,z-14),n['id'],26)
for x in [89,130,190,240,308,400]:text(d,(pt([x,1500])[0]-12,125),str(x),17)
for z in [1550,1650,1750,1850]:text(d,(5,pt([70,z])[1]),str(z),17)
text(d,(1080,175),'P1 共 13,661 格，分开安排',28)
for i,item in enumerate(evidence['parts']):
    text(d,(1080,235+i*54),f"{item['name']}：{item['area']:,} 格",23)
lines=['G1 7,175 格混合候选面（玫红）','35%–48% 意向建筑占地；含居民生活','斜线：穿行净空，建筑不得占用','阈值 X89–129：零建筑占地','G1 内净空 1,451 格，不扣成假空白','G1：短交易 / 短仓 / 饮食 / 修理','N1：较深市场 / 加工 / 公共服务','两节点日常互通，不连成封口建筑墙','首栋改荐 G1 共享周转与生活院','称量是自愿交易服务，不是关税查验','取水、排水、人工内容须未来局部复核']
for i,s in enumerate(lines):text(d,(1080,555+i*44),s,23)
d.line((95,1140,220,1140),fill='#293d37',width=4);text(d,(95,1155),'50 blocks · 北 ↑ 东 →',18)
text(d,(470,1150),'2.5 px/block · 节点锚点非建筑位置 · world writes = 0',22)
im.save(OUT/'visual/gateway-principal-detail.png')
contract={'pixel_size':[2180,1220],'map_origin_pixel':[50,145],'world_origin':[-400,1440],'map_extent_exclusive':[-400,1440,1200,2400],'pixels_per_block_x':1,'pixels_per_block_z':1,'all_middle_columns_included':True,'local_gateway':{'pixel_size':[1900,1220],'map_origin_pixel':[70,160],'world_origin':[70,1500],'extent_exclusive':[70,1500,450,1880],'pixels_per_block_x':2.5,'pixels_per_block_z':2.5},'symbols_not_footprints':True}
(OUT/'validation/map-contract.json').write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8',newline='\n')
print('R1 seven full maps + gateway detail complete')
