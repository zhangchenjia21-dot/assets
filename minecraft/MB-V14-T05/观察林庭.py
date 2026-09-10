"""生成标记来源的空间观察，实际模式完全依赖保存区块。"""
from pathlib import Path
import numpy as np,json,sys,subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).parent;E=R/'证据';E.mkdir(exist_ok=True);n=sys.argv[1];design='--design' in sys.argv;s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=s if design else json.loads((E/(n+'.json')).read_text(encoding='utf8'));v=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size']);P=m['palette'];lut={p.split('[')[0]:c for p,c in zip(s['palette'],s['colors'])};C=np.array([lut[p.split('[')[0]] for p in P]);prefix=('设计' if design else '实存')+n
views=[['林庭东南',[225,124,214],[134,82,131],74],['林冠北侧',[195,129,61],[134,88,128],76],['林庭西侧',[58,111,143],[138,85,124],78],['入林门',[92,67,224],[99,74,199],76],['泉池初见',[107,69,165],[137,88,112],80],['听水台',[122,69.6,151],[137,88,112],80],['祖树根廊',[121,77.6,120],[137,87,112],82],['议庭入口',[169,70.6,157],[169,76,140],78],['倒木种子室',[94,72.6,138],[94,76,120],80],['幼林圃',[164,69,185],[165,71,173],80],['林下回望',[74,68,185],[111,81,151],78],['北泉岸',[165,75,98],[152,70,103],78]]
if '--quick' in sys.argv:views=views[:3]
if '--only' in sys.argv:views=[a for a in views if a[0]==sys.argv[sys.argv.index('--only')+1]]
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
def title(im,name,txt):
 d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,57),fill=(22,37,30));d.text((12,5),'T05 '+prefix+' · '+name,font=font,fill='white');d.text((12,32),txt,font=small,fill=(220,230,222));return im
if design:v.tofile(E/'临时设计.bin')
for name,eye,target,fov in views:
 mask=E/(prefix+'-步行.npy')
 if mask.exists() and name not in ['林庭东南','林冠北侧','林庭西侧']:
  a=np.load(mask);pts=[]
  for x in range(max(0,int(eye[0])-3),min(256,int(eye[0])+4)):
   for z in range(max(0,int(eye[2])-3),min(256,int(eye[2])+4)):
    for y in np.flatnonzero(a[x,:,z]):pts.append(((x-eye[0])**2+(z-eye[2])**2+(y+57.6-eye[1])**2,x,float(y+57.6),z))
  if pts:_,x,y,z=min(pts);eye[:]=[x,round(y,2),z]
 cfg={'volume':str(E/'临时设计.bin') if design else str(E/(n+'.bin')),'size':m['size'],'palette':P,'colors':C.tolist(),'eye':eye,'target':target,'fov':fov,'res':[1100,720],'output':str(E/'临时.ppm')};(E/'临时.json').write_text(json.dumps(cfg),encoding='utf8');subprocess.run(['node',str(R/'体素透视.mjs'),str(E/'临时.json')],check=True);im=Image.open(E/'临时.ppm').copy();title(im,name,f'{eye} → {target} | 软件几何观察，非客户端截图' if not design else '仅设计模型，非实存证据').save(E/(prefix+'-'+name+'.png'));print(name,flush=True)
nonair=np.array([p not in ['minecraft:air','minecraft:cave_air'] for p in P]);height=95-np.argmax(nonair[v][:,::-1,:],axis=1);ids=np.take_along_axis(v,height[:,None,:],axis=1)[:,0,:];im=Image.fromarray(C[ids].astype(np.uint8).transpose(1,0,2)).resize((1024,1024));title(im,'平面','北在上；4像素/格').save(E/(prefix+'-平面.png'))
for axis,k in [('x',137),('z',148)]:
 cut=v[k,:,:] if axis=='x' else v[:,:,k].T;im=Image.fromarray(C[cut].astype(np.uint8)[::-1]).resize((1024,384));title(im,axis+'='+str(k)+' 剖面','Y56—151；4像素/格').save(E/(prefix+'-剖面'+axis+'.png'))
vp=E/(prefix+'-视点.json');record=json.loads(vp.read_text(encoding='utf8')) if '--only' in sys.argv and vp.exists() else [];record={a[0]:a for a in record+views};vp.write_text(json.dumps(list(record.values()),ensure_ascii=False,indent=2),encoding='utf8')
