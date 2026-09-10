"""读取实存导出并记录真实相机；设计预览单独标记，不混为存档证据。"""
from pathlib import Path
import numpy as np,json,sys,subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True);n=sys.argv[1];design='--design' in sys.argv;s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=s if design else json.loads((E/(n+'.json')).read_text(encoding='utf8'));v=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size']);P=m['palette'];lut={p.split('[')[0]:c for p,c in zip(s['palette'],s['colors'])};C=np.array([lut[p.split('[')[0]] for p in P]);prefix=('设计' if design else '实存')+n
views=[['东南远望',[241,151,253],[131,112,135],66],['西崖鸟瞰',[38,162,123],[135,112,121],72],['北脊回望',[160,154,37],[133,119,112],72],['接近山路',[179,92.6,216],[135,118,169],75],['跨壕入门',[135,110.6,191],[135,115,171],75],['外院',[136,110.6,164],[133,119,139],82],['内院',[138,113.6,130],[125,124,100],80],['厅堂门前',[140,113.6,122],[150,119,117],78],['主塔门前',[124,113.6,113],[124,120,99],76],['内墙回望',[108,125.6,124],[140,116,154],80],['主塔顶',[130,145.6,107],[144,136,158],80],['坡脚林缘',[62,78,178],[111,119,136],76]]
if '--quick' in sys.argv:views=views[:3]
if design:v.tofile(E/'临时设计.bin')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
def label(im,title,txt):
 d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,57),fill=(24,31,37));d.text((12,5),'T04 '+prefix+' · '+title,font=font,fill='white');d.text((12,32),txt,font=small,fill=(218,220,218));return im
for name,eye,target,fov in views:
 # 只对近地视点校准到附近实际可达脚点，不把鸟瞰标为步行视角。
 mask=E/(prefix+'-步行.npy')
 if mask.exists() and name not in ['东南远望','西崖鸟瞰','北脊回望']:
  a=np.load(mask);points=[]
  for x in range(max(0,int(eye[0])-3),min(256,int(eye[0])+4)):
   for z in range(max(0,int(eye[2])-3),min(256,int(eye[2])+4)):
    for y in np.flatnonzero(a[x,:,z]):points.append(((x-eye[0])**2+(z-eye[2])**2+(y+57.6-eye[1])**2,x,y+57.6,z))
  if points:
   _,x,y,z=min(points);eye[:]=[x,round(float(y),2),z]
 cfg={'volume':str(E/'临时设计.bin') if design else str(E/(n+'.bin')),'size':m['size'],'palette':P,'colors':C.tolist(),'y0':56,'res':[1100,720],'eye':eye,'target':target,'fov':fov,'output':str(E/'临时.ppm')};(E/'临时.json').write_text(json.dumps(cfg),encoding='utf8');subprocess.run(['node',str(R/'透视体素.mjs'),str(E/'临时.json')],check=True)
 im=Image.open(E/'临时.ppm').copy();label(im,name,f'{eye} → {target} | 保存区块软件几何观察，非客户端截图' if not design else '设计预览，尚非实存证据');im.save(E/(prefix+'-'+name+'.png'));print(name,flush=True)
nonair=np.array([p not in ['minecraft:air','minecraft:cave_air'] for p in P]);height=127-np.argmax(nonair[v][:,::-1,:],axis=1);ids=np.take_along_axis(v,height[:,None,:],axis=1)[:,0,:];im=Image.fromarray(C[ids].astype(np.uint8).transpose(1,0,2)).resize((1024,1024));label(im,'平面','北在上；4像素/格').save(E/(prefix+'-平面.png'))
for axis,k in [('x',135),('z',120)]:
 cut=v[k,:,:] if axis=='x' else v[:,:,k].T;im=Image.fromarray(C[cut].astype(np.uint8)[::-1]).resize((1024,512));label(im,axis+'='+str(k)+' 剖面','Y56—183；4像素/格').save(E/(prefix+'-剖面'+axis+'.png'))
(E/(prefix+'-视点.json')).write_text(json.dumps(views,ensure_ascii=False,indent=2),encoding='utf8')
