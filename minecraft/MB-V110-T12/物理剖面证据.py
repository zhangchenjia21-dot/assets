"""把实存的原生静态碰撞形状和身体包络并列绘出，不冒充游戏截图。"""
from pathlib import Path
import json,numpy as np,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(36,96,56);pal=m['palette'];shapes=json.loads((R/'证据/原生碰撞形状.json').read_text(encoding='utf8'))['shapes'];font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
for name,x,z0,z1,y0,y1 in [('东墙支承',37,16,35,14,25),('入口台阶',24,12,23,14,24),('仓库入口',30,71,82,14,25),('楼梯中线',27,23,33,16,29),('楼梯西侧',25,23,33,16,29)]:
 scale=42;w=(z1-z0+1)*scale+80;h=(y1-y0+1)*scale+100;im=Image.new('RGB',(w,h),'#faf8f1');d=ImageDraw.Draw(im)
 def pt(z,y):return (55+(z-z0)*scale,45+(y1+1-y)*scale)
 for y in range(y0,y1+1):
  for z in range(z0,z1+1):
   v=pal[A[y-10,z,x]];c='#a38763' if 'oak' in v or 'spruce' in v else '#bcae96' if 'terracotta' in v else '#858b89'
   for a,b,c0,e,f,g in shapes[v]:
    if a<=.5<e:d.rectangle((*pt(z+c0,y+f),*pt(z+g,y+b)),fill=c)
 for y in range(y0,y1+2):
  d.line((pt(z0,y),pt(z1+1,y)),fill='#d5d2c9',width=1);d.text((5,pt(z0,y)[1]-8),str(y),font=font,fill='black')
 for z in range(z0,z1+2):d.line((pt(z,y0),pt(z,y1+1)),fill='#d5d2c9',width=1);d.text((pt(z,y0)[0],h-47),str(z),font=font,fill='black')
 initial=json.loads((R/'证据/baseline-物理扫描.json').read_text(encoding='utf8'))
 for gap in initial['closure_candidates']:
  X,Y,Z=gap['gap']
  if X==x and z0<=Z<=z1 and y0<=Y<=y1:d.rectangle((*pt(Z,Y+1),*pt(Z+1,Y)),outline='#d94d32',width=3)
 if '楼梯' in name:
  lane=next(r for r in initial['stair_lanes'] if r['name']==f'stair lane ({x}, 18, 25)');points=[t for t in lane['trace'] if t['collisions']]
  for t in points[::max(1,len(points)//3)]:
   _,Y,Z=t['feet'];d.rectangle((*pt(Z-.3,Y+1.8),*pt(Z+.3,Y)),outline='#d94d32',width=3)
 d.text((12,10),f'T12 {s} {name} X={x}｜原生静态碰撞剖面，非客户端截图',font=font,fill='black');d.text((12,h-24),'红框：初始缺口或同位置身体包络；Y 竖轴 / Z 横轴；不证明真实移动',font=font,fill='#a83222')
 im.save(R/f'证据/{s}-剖面-{name}.png')
