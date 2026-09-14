"""从最终审阅碰撞盒直接绘制平面、剖面和轴测，不使用生成图冒充证据。"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text(encoding='utf-8-sig'))
m=read('设计体素.json');bs=read('设计几何.json')['boxes'];p=read('inputs/r3/evidence/公共通行冻结基线.json');b=read('inputs/r3/BDP-01.json');s=read('inputs/场地事实切片.json')
font='C:/Windows/Fonts/msyh.ttc'
F=lambda n:ImageFont.truetype(font,n)
colors=m['palette'];bg='#f5f0e7'
def canvas(title):
    im=Image.new('RGB',(1400,1000),bg);d=ImageDraw.Draw(im);d.text((38,24),title,font=F(30),fill='#243b3c');return im,d
def footer(d):
    d.text((38,942),'MP-I02B · candidate r2 · BDP-01 r3 · 未冻结 / 待 GPT + Owner 审核 · world writes = 0',font=F(20),fill='#243b3c')
def plan(y,title,name):
    im,d=canvas(title);k=49;X=lambda x:170+(x-750)*k;Z=lambda z:90+(z-1623)*k
    for x,z in b['spatial_envelope']['cells']:d.rectangle((X(x),Z(z),X(x+1),Z(z+1)),fill='#e1dccf',outline='#bdb7aa')
    for x,z in p['protected_horizontal_geometry']['cells']:d.rectangle((X(x),Z(z),X(x+1),Z(z+1)),fill='#bbd5dd',outline='#92b8c5')
    for v in m['blocks']:
        if v['role']=='yard_floor':d.rectangle((X(v['x']),Z(v['z']),X(v['x']+1),Z(v['z']+1)),fill='#a0b697')
    for v in bs:
        a,c=v['min'],v['max']
        if a[1]<=y<c[1]:d.rectangle((X(a[0]),Z(a[2]),X(c[0]),Z(c[2])),fill=colors[v['material']],outline='#443e35')
    for route in m['routes']:
        points=[(X(v[0]+.5),Z(v[1]+.5)) for v in route['surface'] if abs(v[2]-y)<1.2]
        if len(points)>1:d.line(points,fill='#c34025' if route['id']=='R-WORK' else '#287c9c',width=3)
    for x in range(750,771,2):d.text((X(x),65),str(x),font=F(16),fill='#243b3c')
    for z in range(1623,1639,2):d.text((110,Z(z)),str(z),font=F(16),fill='#243b3c')
    d.text((1170,160),'北 ↑\n格网 1 block\n\n蓝底：公共净空\n绿底：18格私院\n红线：工作流\n蓝线：家庭流\n\n门按打开状态\n显示碰撞盒',font=F(18),fill='#243b3c')
    d.text((170,860),f'切片 Y={y}。烟道仍为未闭合实体占位；两容器无雨水性能认证。',font=F(20),fill='#7b3828');footer(d);im.save(R/name)
def section(z,title,name):
    im,d=canvas(title);X=lambda x:130+(x-750)*58;Y=lambda y:855-(y-128)*41
    for c in s['columns']:
        if c[1]==int(z):d.rectangle((X(c[0]),Y(c[3]+1),X(c[0]+1),855),fill='#c8c1b0')
    for v in bs:
        a,c=v['min'],v['max']
        if a[2]<=z<c[2]:d.rectangle((X(a[0]),Y(c[1]),X(c[0]),Y(a[1])),fill=colors[v['material']],outline='#443e35')
    for y in [131,132,134,138,140,144,145]:d.line((110,Y(y),1235,Y(y)),fill='#b5b4a7');d.text((50,Y(y)-19),str(y),font=F(18),fill='#243b3c')
    d.text((130,880),f'剖切 Z={z}；灰底为地表快照。未将浅层筛查提升为承载认证。',font=F(20),fill='#243b3c');footer(d);im.save(R/name)
def iso(cut,name):
    im,d=canvas('剖切轴测 · 保留原平剖面与家庭独立路线' if cut else '体量轴测 · 低作坊 / 高住屋 / 私院')
    project=lambda a:(670+(a[0]-760)*40-(a[2]-1630)*32,630+(a[0]-760)*15+(a[2]-1630)*18-(a[1]-130)*38)
    faces=[]
    for v in bs:
        a,c=v['min'],v['max'];x,y,z=a;u,h,w=c
        if cut and h>138:continue
        for pts,shade in [([(x,h,z),(u,h,z),(u,h,w),(x,h,w)],1),([(x,y,w),(u,y,w),(u,h,w),(x,h,w)],.85),([(u,y,z),(u,y,w),(u,h,w),(u,h,z)],.68)]:
            col=colors[v['material']];rgb=tuple(int(int(col[i:i+2],16)*shade) for i in [1,3,5]);faces.append((sum(q[0]+q[2]+q[1]*.05 for q in pts)/4,pts,rgb))
    for _,pts,col in sorted(faces,key=lambda a:a[0]):d.polygon([project(q) for q in pts],fill=col,outline='#343f3a')
    d.text((38,880),'图示包含未闭合烟道 / 雨水占位，不能据视觉完整宣告 DESIGN_READY。',font=F(21),fill='#7b3828');footer(d);im.save(R/name)
plan(132.25,'低肩作坊 / 独立家庭廊 / r3公共接口','平面-作坊.png')
plan(134.25,'住屋首层 · 起居炊食 / 内楼梯','平面-下层.png')
plan(138.25,'住屋上层 · 两床设计容量 / 屏隔卫生','平面-上层.png')
section(1628.5,'横剖面 · 私院131 → 作坊132 → 住屋134 / 138','剖面-家庭.png')
section(1625.5,'楼梯剖面 · 四级双半踏面 / 顶部落脚','剖面-楼梯.png')
iso(False,'体量轴测.png');iso(True,'剖切轴测.png')
names=['体量轴测.png','平面-作坊.png','平面-下层.png','平面-上层.png','剖面-家庭.png','剖面-楼梯.png','剖切轴测.png']
(R/'设计预览.html').write_text('<!doctype html><meta charset="utf-8"><title>MP-I02B freeze candidate r2</title><style>body{margin:32px;background:#243b3c;color:#f5f0e7;font:18px sans-serif}img{width:100%;max-width:1400px}a{color:#dbba7d}</style><h1>MP-I02B · 未冻结候选 r2</h1><p>BDP-01 r3。门与护栏已细化；地基、烟道/居住环境和雨水性能仍有 blocker。world writes = 0。</p><p><a href="Completion-Report.md">Completion Report</a></p>'+''.join('<h2>'+n+'</h2><img src="'+n+'">' for n in names),encoding='utf-8')
print('7 review drawings generated from final geometry')
