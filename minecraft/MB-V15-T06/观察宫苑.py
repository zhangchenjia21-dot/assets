"""标注源数据与相机的总览、玩家高度透视、平面和剖面。"""
from pathlib import Path
import json,sys,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).parent;E=R/'证据';n=sys.argv[1];design='--design' in sys.argv;s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=s if design else json.loads((E/(n+'.json')).read_text(encoding='utf8'));P=m['palette'];v=np.load(R/f'阶段{n}.npy') if design else np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size']);colors={p.split('[')[0]:c for p,c in zip(s['palette'],s['colors'])};C=np.array([colors[p.split('[')[0]] for p in P]);prefix=('设计' if design else '实存')+n
views=[['全苑东南',[212,124,296],[109,73,157],65],['宫殿西南',[24,102,149],[111,78,65],71],['园室与镜渠',[213,106,297],[116,68,230],75],['前庭到达',[112,70.6,18],[112,79,52],72],['观园平台',[112,70.6,92],[112,64,210],78],['花坛步道',[110,66.6,122],[82,65.5,122],76],['花坛回望',[112,66.6,171],[112,80,56],70],['西水园',[61,64.6,235],[42,65,235],77],['绿剧场',[180,64.6,249],[178,65,220],77],['橘园花庭',[44,66.6,164],[44,71,122],76],['镜渠终端',[112,64.6,300],[112,77,61],65],['宫殿通厅',[112,70.6,51],[112,72,78],76],['宫殿上层',[112,80.6,65],[104,80,55],76]]
views.append(['橘园入口近景',[44,66.6,134],[44,66,121],76])
if '--quick' in sys.argv:views=views[:3]
if '--only' in sys.argv:views=[a for a in views if a[0]==sys.argv[sys.argv.index('--only')+1]]
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13)
def label(im,name,subtitle):
 d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,55),fill=(35,40,46));d.text((10,4),'T06 '+prefix+' · '+name,font=font,fill='white');d.text((10,30),subtitle,font=small,fill=(222,229,235));return im
if design:v.tofile(E/'临时设计.bin')
for name,eye,target,fov in views:
 cfg={'volume':str(E/'临时设计.bin') if design else str(E/(n+'.bin')),'size':m['size'],'palette':P,'colors':C.tolist(),'eye':eye,'target':target,'fov':fov,'res':[1050,700],'output':str(E/'临时.ppm')};(E/'临时.json').write_text(json.dumps(cfg),encoding='utf8');subprocess.run(['node',str(R/'体素观察.mjs'),str(E/'临时.json')],check=True);im=Image.open(E/'临时.ppm').copy();label(im,name,f'{eye} → {target} | 软件几何透视，非客户端截图' if not design else '仅设计模型，非实存证据').save(E/(prefix+'-'+name+'.png'));print(name,flush=True)
height=v.shape[1]-1-np.argmax(v[:,::-1,:]!=P.index('minecraft:air'),axis=1);ids=np.take_along_axis(v,height[:,None,:],axis=1)[:,0,:];im=Image.fromarray(C[ids].astype(np.uint8).transpose(1,0,2)).resize((672,960));label(im,'平面','北在上；X0—223 / Z0—319').save(E/(prefix+'-平面.png'))
for axis,k in [('x',112),('z',55)]:
 cut=v[k,:,:] if axis=='x' else v[:,:,k].T;im=Image.fromarray(C[cut].astype(np.uint8)[::-1]).resize((1120,320));label(im,axis+'='+str(k)+' 剖面','Y56—119；切面中未切中的支承需结合三维透视').save(E/(prefix+'-剖面'+axis+'.png'))
vp=E/(prefix+'-视点.json');prior=json.loads(vp.read_text(encoding='utf8')) if '--only' in sys.argv and vp.exists() else [];vp.write_text(json.dumps(list({a[0]:a for a in prior+views}.values()),ensure_ascii=False,indent=2),encoding='utf8')
