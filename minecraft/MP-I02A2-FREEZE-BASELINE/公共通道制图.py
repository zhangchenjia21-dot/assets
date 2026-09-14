"""按发布的坐标与section生成审核图；不绘制或修改建筑设计。"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parent
c=json.loads((R/'evidence/公共通行冻结基线.json').read_text(encoding='utf-8'))
b=json.loads((R/'BDP-01.json').read_text(encoding='utf-8'))
im=Image.new('RGB',(1500,1040),'#f7f5ef'); d=ImageDraw.Draw(im)
font='C:/Windows/Fonts/msyh.ttc'
def text(x,y,s,size=22,color='#273b40'):
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color)
text(45,24,'MP-I02A2 · 公共通行冻结基线',32)
text(45,71,'DESIGN_PROPOSAL  |  50 公共列  |  最小净宽 2 / 净高 3  |  world writes = 0',21)
S=48; ox=80; oy=150
def xy(x,z): return (ox+(x-750)*S,oy+(z-1629)*S)
for x,z in b['spatial_envelope']['cells']:
    if 750<=x<770 and 1629<=z<1639:
        a=xy(x,z); e=xy(x+1,z+1); d.rectangle([a,e],fill='#e6d8bb')
for p in c['design_surface']['per_cell']:
    x,z=p['x'],p['z']; col='#97cdbb' if p['public_source']=='LANE-04' else '#efc67f'
    d.rectangle([xy(x,z),xy(x+1,z+1)],fill=col)
for x in range(750,771):
    d.line([xy(x,1629),xy(x,1639)],fill='#c3c8c4',width=1)
    if x%2==0: text(xy(x,1629)[0]-17,121,str(x),15)
for z in range(1629,1640):
    d.line([xy(750,z),xy(770,z)],fill='#c3c8c4',width=1)
    text(20,xy(750,z)[1]-10,str(z),15)
d.line([xy(*p) for p in c['spine']],fill='#246757',width=4)
for p in c['spine']:
    x,z=xy(*p); d.ellipse((x-4,z-4,x+4,z+4),fill='#246757')
d.line([xy(757,1634),xy(758,1634)],fill='#bb4b3c',width=7)
for p in c['ports']:
    x,z=xy(*p['point']); d.ellipse((x-7,z-7,x+7,z+7),outline='#203f48',width=3)
text(1100,150,'范围与来源',25)
for y,color,s in [(205,'#97cdbb','36列 · 原LANE-04'),(250,'#efc67f','14列 · 原共同院'),(295,'#e6d8bb','BDP-01私域 · 不侵入')]:
    d.rectangle((1100,y,1123,y+23),fill=color); text(1135,y-2,s,19)
text(1100,350,'红线：私侧入口 Y132',20)
text(1100,391,'转角：完整 2×2 扫掠',20)
text(1100,432,'端点：原路控制点',20)
text(1100,473,'西端 Y131 / 东端 Y134',19)
text(1100,527,'规划关系已局部固定',21)
text(1100,561,'非 runtime movement 证明',17)
text(45,653,'连续设计断面：Y = H(X)，Z方向等高；每列四角值详见JSON',23)
px=lambda x:80+(x-750)*48
py=lambda y:928-(y-131)*36
profile=c['design_surface']['profile_x_y']
poly=[(px(x),py(y)) for x,y in profile]+[(px(x),py(y+3)) for x,y in reversed(profile)]
d.polygon(poly,fill='#dcebe4')
for y in range(131,138):
    d.line([(80,py(y)),(1040,py(y))],fill='#c7d0c9',width=1); text(27,py(y)-12,str(y),17)
d.line([(px(x),py(y)) for x,y in profile],fill='#246757',width=4)
d.line([(px(x),py(y+3)) for x,y in profile],fill='#629a86',width=2)
text(450,850,'门前 Y132 平台',18)
text(1100,710,'至少 3 格净高',23)
text(1100,755,'地表适应 ≤ ±1 格',21)
text(1100,800,'不指定铺装/台阶构造',19)
text(1100,845,'Builder设计仍待核验',20)
for x in range(750,771,2): text(px(x)-17,944,str(x),15)
text(45,993,'雨水：禁止跨界 / 公共受纳义务 NONE / Builder 须在冻结前设计并证明户内闭合策略。回归裁决 NOT_ASSIGNED。',18)
im.save(R/'公共通道与断面.png')
print('Rendered coordinate-based public plan and section.')
