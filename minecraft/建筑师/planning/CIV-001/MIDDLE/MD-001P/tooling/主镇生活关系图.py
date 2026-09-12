"""等比例局部图：只显示混合活动重心和关系，不绘制建筑/街道施工线。"""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parents[1]
nodes=json.loads((OUT/'settlement-nodes.json').read_text(encoding='utf-8'))['nodes'];n=nodes[0]
x0,z0,x1,z1=n['terrain']['bounds'];x0-=20;z0-=20;x1+=21;z1+=21;w,h=x1-x0,z1-z0
mask=np.zeros((h,w),np.uint8)
for z,l,r in n['envelope']:mask[z-z0,l-x0:r-x0+1]=1
rgb=np.full((h,w,3),(45,65,71),np.uint8);rgb[mask>0]=(206,126,95)
scale=min(3.,900/w,1000/h);ox,oz=50,70
im=Image.new('RGB',(1470,1200),(18,29,40));im.paste(Image.fromarray(rgb).resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST),(ox,oz));dr=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
dr.text((30,15),'N1 主镇混合生活结构 · 活动关系，不是建筑或道路设计',font=font,fill='white')
points={p['id']:(ox+(p['point'][0]-x0)*scale,oz+(p['point'][1]-z0)*scale) for p in n['activity_centres']}
for dest in ('A2','A3','A4'):
    a,b=np.array(points['A1']),np.array(points[dest])
    for t in np.arange(0,1,.10):
        q=a+(b-a)*t;r=a+(b-a)*min(t+.055,1);dr.line((*q,*r),fill='#b3dfea',width=2)
for p in n['activity_centres']:
    xx,zz=points[p['id']];dr.ellipse((xx-6,zz-6,xx+6,zz+6),fill='white');dr.text((xx+10,zz-22),p['id'],font=font,fill='white')
explain=['A1 日常市场、秤验、记录与协商','A2 共享仓院、装卸与车马寄存','A3 家庭生活、小供给、清洁储水预留','A4 轻修理、商住与旅宿混合','红面：N1 混合候选面，不是建成占地','虚线：功能联系，街线待局部规划','活动重心不是独占功能分区','上住下作/下店、共享院落、短巷','货物在院内停装，居民全天可通行','热工与生活冲突用院落/运营分隔','不可填平图内地形保留缺口','首栋推荐在 N1 内另做 Local Site Gate']
for i,t in enumerate(explain):dr.text((990,100+i*56),t,font=small,fill='white')
for x in range((x0//50+1)*50,x1,50):dr.text((ox+(x-x0)*scale,45),str(x),font=small,fill='white')
for z in range((z0//50+1)*50,z1,50):dr.text((5,oz+(z-z0)*scale),str(z),font=small,fill='white')
dr.line((60,1120,60+50*scale,1120),fill='white',width=3);dr.text((60,1140),'50 blocks · 北 ↑ 东 →',font=small,fill='white');dr.text((500,1120),'world writes = 0 · 未冻结地块、建筑尺寸或街道施工范围',font=small,fill='white')
im.save(OUT/'visual/principal-life-structure.png')
(OUT/'validation/principal-map-contract.json').write_text(json.dumps({'status':'PLANNING PROPOSAL','world_bounds_exclusive':[x0,z0,x1,z1],'origin_pixel':[ox,oz],'pixels_per_block_x':scale,'pixels_per_block_z':scale,'symbols_not_footprints':True},indent=2),encoding='utf-8',newline='\n')
