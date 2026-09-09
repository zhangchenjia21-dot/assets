"""读取已保存世界的体素导出，生成可复核透视与步行连通性证据。不是游戏截图。"""
from pathlib import Path
import numpy as np, json, sys, math, subprocess
from PIL import Image,ImageDraw,ImageFont
from collections import deque
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True)
scene=json.loads((R/'场景.json').read_text(encoding='utf8'));stage=sys.argv[1] if len(sys.argv)>1 else '3';actual='--plan' not in sys.argv
meta=json.loads((E/f'阶段{stage}-实存.json').read_text(encoding='utf8')) if actual else scene
V=np.fromfile(E/f'阶段{stage}-实存.bin',np.uint8).reshape(meta['size']) if actual else np.load(R/f'阶段{stage}.npy')
pal=meta['palette'];W,H,D=V.shape;Y0=63
basecolors={s.split('[')[0]:c for s,c in zip(scene['palette'],scene['colors'])}
colors=np.array([basecolors.get(s.split('[')[0],[125,125,125]) for s in pal],float)
air=np.array([s in ['minecraft:air','minecraft:cave_air','minecraft:void_air'] for s in pal]);solid=~air[V]
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
prefix=f'阶段{stage}-'+('实存' if actual else '设计')
def caption(im,title,sub):
 d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,64),fill=(20,28,31));d.text((18,7),title,font=font,fill='white');d.text((18,34),sub,font=small,fill=(200,211,213));return im
def view(name,eye,target,fov=65,res=(1000,640)):
 config={'volume':str(E/f'阶段{stage}-实存.bin'),'size':list(V.shape),'res':list(res),'eye':eye,'target':target,'fov':fov,'air':air.tolist(),'colors':colors.tolist(),'output':str(E/'临时透视.ppm')}
 if not actual:
  V.tofile(E/'临时设计.bin');config['volume']=str(E/'临时设计.bin')
 cfg=E/'临时视点.json';cfg.write_text(json.dumps(config),encoding='utf8')
 subprocess.run(['node',str(R/'体素透视.mjs'),str(cfg)],check=True)
 im=Image.open(E/'临时透视.ppm').copy();caption(im,f'T02 / {name} / '+('已保存世界读回' if actual else '施工前设计'),f'相机 XYZ {eye} → {target} · 软件体素透视；非游戏截图');im.save(E/f'{prefix}-{name}.png');print(name,flush=True);return
cams=[('01-西南全景',[22,137,209],[122,95,102],68),('02-东北俯瞰',[223,170,12],[129,99,105],64),('03-山脚入场',[25,66.6,194],[91,99,120],70),('04-门楼前',[57,77.6,156],[91,98,134],75),('05-上山转折',[99,90.6,134],[111,107,93],78),('06-教堂入口',[103,98.6,82],[133,104,81],82),('07-回廊西南',[122,96.6,120],[145,100,99],82),('08-教堂内殿',[112,98.6,81],[155,105,81],82),('09-生产台地',[138,84.6,155],[139,105,112],75),('10-泉台回望',[176,96.6,116],[138,103,112],80)]
cams.append(('11-庭心望教堂',[137,96.6,114],[132,107,85],85))
if stage=='1':cams=cams[:2]+[cams[2]]
if '--quick' in sys.argv:cams=cams[:2]
if '--no-views' in sys.argv:cams=[]
for name,eye,target,fov in cams:view(name,eye,target,fov,res=(900,576) if stage=='1' else (1100,700))
tops=(H-1)-np.argmax(solid[:,::-1,:],axis=1);topids=np.take_along_axis(V,tops[:,None,:],axis=1)[:,0,:]
arr=colors[topids].transpose(1,0,2).astype(np.uint8);im=Image.fromarray(arr).resize((960,880),Image.Resampling.NEAREST);dr=ImageDraw.Draw(im)
for r in scene['routes']:
 dr.line([(x*4,z*4) for x,y,z in r['cells']],fill=(232,204,104),width=2)
for x,z,name in [(113,81,'教堂'),(134,108,'回廊'),(104,71,'钟塔'),(85,133,'客舍'),(65,153,'门楼'),(139,165,'生产台地'),(172,109,'泉台')]:dr.text((x*4,z*4),name,font=small,fill='white',stroke_width=2,stroke_fill='black')
caption(im,'T02 / 顶视与路线','北为图上方；每格 4 像素；金线为设计路线中心，需配合连通性检查');im.save(E/f'{prefix}-平面.png')
for axis,coord in [('x',136),('z',108)]:
 cut=V[coord,:,:] if axis=='x' else V[:,:,coord].T
 img=colors[cut].astype(np.uint8)[::-1];im=Image.fromarray(img).resize((img.shape[1]*5,img.shape[0]*5),Image.Resampling.NEAREST)
 caption(im,f'T02 / 剖面 {axis.upper()}={coord}','来自保存体素；底边 Y63，顶边 Y166；每方块 5 像素');im.save(E/f'{prefix}-剖面{axis}.png')
if actual:
 # 主要路线允许一格台阶/跳步；禁止穿墙、飞行、水中移动。楼梯形状按保守整格包络。
 passable=np.array([air[i] or any(k in s for k in ['ladder','lantern','wheat']) for i,s in enumerate(pal)])[V]
 support=~passable;support[np.isin(V,[i for i,s in enumerate(pal) if 'water' in s.split('[')[0] or 'leaves' in s])]=False
 walk=np.zeros_like(solid);walk[:,1:-1,:]=support[:,:-2,:]&passable[:,1:-1,:]&passable[:,2:,:]
 start=(25,65-Y0,194);q=deque([start]);seen={start}
 while q:
  x,y,z=q.popleft()
  for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
   a,c=x+dx,z+dz
   if not(0<=a<W and 0<=c<D):continue
   for b in [y,y+1,y-1]:
    p=(a,b,c)
    if 0<b<H-1 and walk[p] and p not in seen:
     if b>y and not passable[x,y+2,z]:continue
     seen.add(p);q.append(p)
 points={'山脚':[25,65,194],'门楼':[67,77,153],'客舍':[88,83,137],'服务房':[82,87,117],'教堂内殿':[130,97,81],'回廊':[122,95,108],'庭心井':[136,95,105],'东厢':[160,95,107],'西厢':[113,95,108],'食堂':[127,91,129],'上种植台地':[130,83,151],'下种植台地':[142,79,165],'泉台':[176,95,116]}
 report={'method':'两格净空、可承重地面、相邻高差至多一格；允许跳步，未模拟游戏客户端物理','reachable_cells':len(seen),'destinations':{k:{'xyz':v,'reachable':(v[0],v[1]-Y0,v[2]) in seen} for k,v in points.items()}}
 (E/f'阶段{stage}-动线.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False),flush=True)
 (E/'观察点.json').write_text(json.dumps(cams,ensure_ascii=False,indent=2),encoding='utf8')
