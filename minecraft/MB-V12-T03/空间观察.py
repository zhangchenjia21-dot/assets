"""T03 的平面、剖面、透视及几何观察。实际证据仅使用保存区块的只读导出。"""
from pathlib import Path
import numpy as np,json,sys,subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True);n=sys.argv[1];design='--design' in sys.argv
s=json.loads((R/'场景.json').read_text(encoding='utf8'));meta=s if design else json.loads((E/f'阶段{n}.json').read_text(encoding='utf8'));P=meta['palette'];V=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/f'阶段{n}.bin',np.uint8).reshape(meta['size'])
lookup={p.split('[')[0]:c for p,c in zip(s['palette'],s['colors'])};C=np.array([lookup.get(p.split('[')[0],[135,125,100]) for p in P]);air=np.array([p in ['minecraft:air','minecraft:cave_air','minecraft:void_air'] for p in P]);y0=s['y0'];W,H,D=V.shape
prefix=('设计' if design else '实存')+n;font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
def title(im,label,details):
 d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,55),fill=(23,34,37));d.text((12,5),'T03 · '+prefix+' · '+label,font=font,fill='white');d.text((12,31),details,font=small,fill=(205,217,220));return im
views=[('西南谷地',[14,117,260],[125,73,122],74),('东岸俯瞰',[249,130,190],[108,76,118],73),('南侧进入',[66,77.6,190],[92,77,147], seventy:=72),('村中草地',[99,72.6,147],[74,84,121],78),('桥上看村',[144,70.6,143],[101,78,139],82),('桥上看水磨',[155,70.6,143],[166, seventy_b:=72,96],74),('教堂门前',[57,84.6,101],[60,89,88], eighty:=80),('河岸草甸',[124,67.6,185],[151,69,150],78),('长屋宅前',[92,74.6,157],[77,76,158],82),('磨坊水轮',[156,67.6,101],[162,68,91],80),('条田近景',[193, seventy_c:=73,203],[205,85,181],78),('北庄院',[106,81.6,67],[83,88,50],80)]
if '--quick' in sys.argv:views=views[:2]
if '--maps' in sys.argv:views=[]
if design:V.tofile(E/f'临时设计{n}.bin')
for label,eye,target,fov in views:
 if not design and eye[1]<110 and (E/f'阶段{n}-步行mask.npy').exists():
  reachable=np.load(E/f'阶段{n}-步行mask.npy');candidates=[]
  for xx in range(max(0,int(eye[0])-4),min(W,int(eye[0])+5)):
   for zz in range(max(0,int(eye[2])-4),min(D,int(eye[2])+5)):
    for yy in np.flatnonzero(reachable[xx,:,zz]):
     score=(xx-eye[0])**2+(zz-eye[2])**2+.35*(yy+y0+1.6-eye[1])**2;candidates.append((score,xx,float(yy+y0+1.6),zz))
  if candidates:
   _,xx,yy,zz=min(candidates);eye[:]=[xx,round(yy,2),zz]
 cfg={'volume':str(E/f'临时设计{n}.bin') if design else str(E/f'阶段{n}.bin'),'size':list(V.shape),'res':[1000,640],'eye':eye,'target':target,'y0':y0,'fov':fov,'palette':P,'colors':C.tolist(),'output':str(E/f'临时{n}.ppm')}
 cf=E/f'临时{n}.json';cf.write_text(json.dumps(cfg),encoding='utf8');subprocess.run(['node',str(R/'体素观察.mjs'),str(cf)],check=True)
 im=Image.open(E/f'临时{n}.ppm').copy();title(im,label,f'相机 {eye} → {target} | 软件几何透视，非游戏截图');im.save(E/f'{prefix}-{label}.png');print(label,flush=True)
surface=(H-1)-np.argmax((~air[V])[:,::-1,:],axis=1);ids=np.take_along_axis(V,surface[:,None,:],axis=1)[:,0,:];im=Image.fromarray(C[ids].astype(np.uint8).transpose(1,0,2)).resize((1024,1024),Image.Resampling.NEAREST)
d=ImageDraw.Draw(im)
for a in s['doors']:
 x,y,z=a['inside'];d.text((x*4,z*4),a['name'],font=small,fill='white',stroke_width=2,stroke_fill='black')
title(im,'平面','北在上，4像素/格；建筑标签为设计位置');im.save(E/f'{prefix}-平面.png')
for axis,k in [('z',143),('x',95)]:
 cut=V[:,:,k].T if axis=='z' else V[k,:,:];im=Image.fromarray(C[cut].astype(np.uint8)[::-1]).resize((cut.shape[1]*4,H*4),Image.Resampling.NEAREST);title(im,f'{axis.upper()}={k} 剖面',f'底部Y{y0} 顶部Y{y0+H-1}；4像素/格');im.save(E/f'{prefix}-剖面{axis}.png')
if not design:(E/f'阶段{n}-视点.json').write_text(json.dumps(views,ensure_ascii=False,indent=2),encoding='utf8')
