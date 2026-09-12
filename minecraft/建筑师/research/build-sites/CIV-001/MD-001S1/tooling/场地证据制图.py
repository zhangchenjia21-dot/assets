"""按当前快照表层和候选 RLE 绘制等比例坐标图；不渲染虚构建筑或设计平剖面。"""
import gzip,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import 当前场地读取 as s
rows=json.load(gzip.open(s.CACHE/'surface.json.gz','rt',encoding='utf-8'))
cs=s.read(s.OUT/'candidates.json')['candidates'];g=s.mask(next(n for n in s.read(s.PLAN/'settlement-nodes.json')['nodes'] if n['id']=='G1')['envelope'])
clear=s.mask(s.read(s.PLAN/'land-use.json')['building_exclusion_overlays'][0]['geometry'])
base=np.full((s.H,s.W,3),(223,225,221),np.uint8)
palette=[(146,191,151),(155,191,144),(169,191,137),(186,188,129),(205,181,118),(220,164,103),(229,145,90)]
trunks=[];leaves=[]
for p in rows:
    x,z=p['x']-s.X0,p['z']-s.Z0;base[z,x]=palette[max(0,min(6,p['ground_y']-62))]
    if not g[z,x]:base[z,x]=(base[z,x]*.55+100).astype(np.uint8)
    if p['ground'] in s.WATER:base[z,x]=(78,145,182)
    if any('_log' in b for yy,b in p['above']):trunks.append((p['x'],p['z']))
    if any('leaves' in b for yy,b in p['above']):leaves.append((p['x'],p['z']))
zz,xx=np.indices(g.shape);base[clear&((zz+xx)%6<2)]=(55,133,165)
cols={'S1':'#bf5949','S2':'#8b65a7','S3':'#287e84'}
def font(n):return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
def text(d,p,t,size=22,color='#2e4038'):d.text(p,t,font=font(size),fill=color,spacing=8)
contracts={}
for kind,title,bounds,scale in [('current-world-site-base','G1 当前存档场地底图',[85,1674,251,1794],6),('candidate-comparison','三个候选 · 容量与生活关系',[85,1674,251,1794],6),('recommended-site-detail','推荐 S1 · 东侧高位缓台',[206,1678,248,1730],15)]:
    x0,z0,x1,z1=bounds;ox,oy=80,165
    im=Image.new('RGB',(1800,1160),'#f6f3eb');crop=base[z0-s.Z0:z1-s.Z0,x0-s.X0:x1-s.X0]
    im.paste(Image.fromarray(crop).resize(((x1-x0)*scale,(z1-z0)*scale),Image.Resampling.NEAREST),(ox,oy));d=ImageDraw.Draw(im)
    text(d,(55,24),'MD-001S1 · '+title,37);text(d,(55,89),'当前 建筑师 / 26.2 / DataVersion 4903 · 仅 Site Gate，未设计建筑',24)
    def pt(p):return ox+(p[0]-x0)*scale,oy+(p[1]-z0)*scale
    def outline(mask,color,width=2):
        for z,x in zip(*np.where(mask)):
            wx,wz=x+s.X0,z+s.Z0
            if not(x0<=wx<x1 and z0<=wz<z1):continue
            px,pz=pt((wx,wz))
            for dx,dz,line in [(0,-1,(px,pz,px+scale,pz)),(0,1,(px,pz+scale,px+scale,pz+scale)),(-1,0,(px,pz,px,pz+scale)),(1,0,(px+scale,pz,px+scale,pz+scale))]:
                if not mask[z+dz,x+dx]:d.line(line,fill=color,width=width)
    outline(g,'#506440',2)
    for x,z in leaves:
        if x0<=x<x1 and z0<=z<z1:
            px,pz=pt((x,z));d.rectangle((px,pz,px+scale-1,pz+scale-1),fill='#668b55')
    for x,z in trunks:
        if x0<=x<x1 and z0<=z<z1:
            px,pz=pt((x,z));d.rectangle((px,pz,px+scale-1,pz+scale-1),fill='#403d29')
    if kind!='current-world-site-base':
        for c in cs if kind=='candidate-comparison' else cs[:1]:
            m=s.mask(c['geometry']);outline(m,cols[c['id']],4)
            for x,z,yy in c['access_witness']:
                if x0<=x<x1 and z0<=z<z1:
                    px,pz=pt((x,z));d.ellipse((px,pz,px+scale-1,pz+scale-1),fill='#135c88')
            if kind=='candidate-comparison':
                px,pz=pt(c['study_anchor']);text(d,(px-22,pz-18),c['id'],27,cols[c['id']])
            else:
                for x,z,yy in c['drainage_witness']:
                    if x0<=x<x1 and z0<=z<z1:
                        px,pz=pt((x,z));d.ellipse((px,pz,px+scale-1,pz+scale-1),fill='#56358b')
    step=20 if scale==6 else 5
    for x in range((x0//step+1)*step,x1,step):text(d,(pt((x,z0))[0]-10,135),str(x),17)
    for z in range((z0//step+1)*step,z1,step):text(d,(10,pt((x0,z))[1]),str(z),17)
    lx=1140 if scale==6 else 780
    if kind=='recommended-site-detail':
        lines=['S1 推荐 · 570 格 gross envelope','边界 X216–240 / Z1684–1718','表层 Y66–67 · 总高差 1 格','红线是不规则 Site 包络，不是建筑','蓝点：9步接入现有规划通行链','紫点：向北更低地面的排水见证','深色树干、绿色冠幅保留为现状','候选与4格缓冲下方12格已读取','未检出空腔、水、明确人工材料','现状主通行线仍有树木，非成路','饮用水未确认；储水/消防待验证','不能向东借用 N1 土地','接受本 Gate 后才能另开设计任务']
    elif kind=='candidate-comparison':
        lines=['S1 东侧高位缓台 · 推荐','570 格 / Y66–67 / 局部高差1','接入同高通行见证；北向较低地','S2 北侧中段缓台 · 备选','586 格 / Y63–65 / 局部高差2','北低缘更敏感，缓冲内有牛','S3 南侧生活口袋 · 备选','605 格 / Y64–66 / 局部高差2','后侧生活空间较独立，排水见证长','三者均不占政治阈值或穿行净空','蓝点只标接近通行链的见证','候选含院落/后勤容量，非屋顶面积']
    else:
        lines=['读自本轮真实存档局部快照','G1 7,175 列全部核对','总表层查询 10,954 列','含G1八格缓冲与窄通行背景','地面 Y62 绿色 → Y68 棕橙','深绿冠幅 / 深褐树干','蓝色斜线：不可建造的穿行净空','灰白区域：未做本轮表层查询','旧缓存差异：1列 dirt→grass_block','没有把旧缓存当作当前存档','无玩家视角截图，机器坐标为依据']
    for i,line in enumerate(lines):text(d,(lx,185+i*51),line,22)
    if kind=='recommended-site-detail':
        for p in rows:
            if p['x']%4==0 and p['z']%4==0 and s.mask(cs[0]['geometry'])[p['z']-s.Z0,p['x']-s.X0]:text(d,pt((p['x'],p['z'])),str(p['ground_y']),13)
    d.line((85,1010,85+10*scale,1010),fill='#2e4038',width=4);text(d,(85,1028),'10 blocks · 北 ↑ 东 →',20)
    text(d,(430,1010),f'等比例 {scale} px/block · PNG 坐标可追踪 · 未冻结建筑位置、尺寸或平面',22)
    text(d,(55,1090),'world writes = 0 · 候选需 GPT + Owner 审核 · 图中蓝线/点不是道路施工设计',23)
    im.save(s.OUT/'visual'/(kind+'.png'));contracts[kind]={'pixel_size':[1800,1160],'world_bounds_exclusive':bounds,'origin_pixel':[ox,oy],'pixels_per_block_x':scale,'pixels_per_block_z':scale}
s.write(s.OUT/'validation/map-contract.json',contracts)
print('three current-world site maps complete')
