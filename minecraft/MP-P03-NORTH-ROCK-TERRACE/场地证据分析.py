"""本轮外围调查派生：坐标图、地表/浅层统计和现状定位，不生成规划答案。"""
from pathlib import Path
import json,sqlite3
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;C=R.parents[3]/'MP-P03-cache'
def dump(p,v):(R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
a=json.loads((C/'surface.json').read_text()); cols=np.array([[v if v is not None else -999 for v in row] for row in a['columns']]); h=cols[:,3].reshape(288,320);top=cols[:,2].reshape(288,320); st=cols[:,4].reshape(288,320);water=cols[:,5].reshape(288,320);leaf=cols[:,6].reshape(288,320);pal=a['palette'];names=[s.split('[')[0].split(':')[1] for s in pal]
classes=['ROCK','SOIL','SAND_GRAVEL','WATER','LAVA','OTHER'];lut=[]
for n in names:
 if n in ['grass_block','dirt','coarse_dirt','podzol']:v=1
 elif n in ['sand','gravel']:v=2
 elif n in ['water','kelp','kelp_plant']:v=3
 elif n=='lava':v=4
 elif n in ['stone','granite','tuff','smooth_basalt','coal_ore','iron_ore','copper_ore','lapis_ore']:v=0
 else:v=5
 lut.append(v)
s=np.array(lut)[st];s[water>-999]=3
np.savez_compressed(C/'terrain.npz',height=h,top=top,surface=s,state=st,water=water,leaf=leaf)
def profile(b):
 x,z,xx,zz=b;sl=(slice(z-1488,zz-1488+1),slice(x-640,xx-640+1));hh=h[sl];ss=s[sl]
 return {'bounds':b,'area':int(hh.size),'y_min_median_max':[int(hh.min()),float(np.median(hh)),int(hh.max())],'surface_counts':{k:int((ss==i).sum()) for i,k in enumerate(classes)},'leaf_columns':int((leaf[sl]>0).sum())}
dump('evidence/current-surface-summary.json',{'core':profile([704,1520,895,1711]),'context':profile([640,1488,959,1775]),'palette':pal,'classes':classes,'classification_note':'ROCK含可见矿石但非矿床；OTHER含苔藓、虫蚀石、陶瓦质等；WATER表示列上方观察到水而非饮水','substrate_samples':a['substrate_witnesses']})
features=[]
for v in cols:
 x,z,topY,y,idx,wy,*_=map(int,v);n=names[idx]
 if n in ['lava','magma_block','cobblestone','infested_cobblestone','mossy_cobblestone','cobweb']:
  features.append({'xz':[x,z],'y':y,'state':pal[idx],'meaning':'OBSERVED_MATERIAL_NOT_AUTHORED_ORIGIN'})
dump('evidence/surface-witnesses.json',features)
dump('evidence/fabric-witnesses.json',[dict(b,surface_y=int(h[b['z']-1488,b['x']-640]),depth_to_ground=int(h[b['z']-1488,b['x']-640])-b['y']) for b in a['block_entities'] if b['y']>=60])
tiles=[profile([x,z,x+15,z+15]) for z in range(1536,1697,16) for x in range(704,881,16)];dump('evidence/terrain-tiles16.json',tiles)
colors=np.array([[153,149,142],[153,178,112],[225,197,139],[92,162,190],[228,75,27],[168,129,175]],dtype=np.uint8)
gy,gx=np.gradient(h.astype(float));v=np.clip((h-60)/100,0,1);rgb=np.stack([95+140*v,140+95*v,110+120*v],2)*np.clip(.9-(gx+gy)*.1,.4,1.1)[:,:,None];rgb[s==3]=colors[3];rgb[s==4]=colors[4]
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
for title,arr in [('现场地形',np.uint8(np.clip(rgb,0,255))),('现场地表',colors[s])]:
 im=Image.new('RGB',(1420,1130),'#f5f1e8');im.paste(Image.fromarray(arr).resize((1120,1008),Image.Resampling.NEAREST),(85,65));d=ImageDraw.Draw(im);d.text((85,15),'MP-P03 '+title+' | 原存档纯只读、1格采样',font=font(26),fill='#233d42')
 for x in range(640,960,32):u=85+(x-640)*3.5;d.line((u,65,u,1073),fill='#b3b7a8');d.text((u,1076),str(x),font=font(17),fill='black')
 for z in range(1504,1776,32):vv=65+(z-1488)*3.5;d.line((85,vv,1205,vv),fill='#b3b7a8');d.text((15,vv),str(z),font=font(17),fill='black')
 d.rectangle((85+64*3.5,65+32*3.5,85+255*3.5,65+223*3.5),outline='#9c2842',width=3)
 for i,k in enumerate(classes):d.rectangle((1225,100+35*i,1245,120+35*i),fill=tuple(colors[i]));d.text((1250,100+35*i),k,font=font(15),fill='black')
 for z in range(1552,1697,16):
  for x in range(720,881,16):d.text((85+(x-640)*3.5,65+(z-1488)*3.5),str(h[z-1488,x-640]),font=font(13),fill='#233d42',stroke_width=1,stroke_fill='white')
 d.text((85,1105),'北↑ −Z，东→ +X；框=父包搜索窗；数字=地面Y；非饮水/矿床/规划图。',font=font(17),fill='#233d42');im.save(R/f'evidence/{title}.png')
print('current core',profile([704,1520,895,1711]));print('surface special',len(features))
