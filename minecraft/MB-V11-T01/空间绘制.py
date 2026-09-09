"""从阶段蓝图或存档回读绘制审计图；非游戏截图，方块采用简化材质和几何。"""
import json,sys,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
mode=sys.argv[1] if len(sys.argv)>1 else '1'
vox={}
if mode.isdigit():
    manifest=json.loads((ROOT/'阶段清单.json').read_text(encoding='utf8'))
    for stage in manifest['stages'][:int(mode)]:
        for file in stage['files']:
            b=json.loads((ROOT/file).read_text(encoding='utf8'));o=b['origin']
            for x,y,z,p in b['blocks']:vox[x+o['x'],y+o['y'],z+o['z']]=b['palette'][p]
else:
    for x,y,z,s in json.loads((ROOT/'存档回读方块.json').read_text(encoding='utf8')):vox[x,y,z]=s
# 超平坦的表面也参与遮挡，实际回读模式不补造方块。
if mode.isdigit():
    for z in range(-4,155):
        for x in range(-4,190):vox.setdefault((x,63,z),'minecraft:grass_block')
vox={p:s for p,s in vox.items() if s and not s.endswith(':air') and not s.endswith(':cave_air')}
palette={'grass_block':(102,129,66),'dirt':(116,94,66),'clay':(137,146,149),'water':(62,127,132),'stone':(148,149,139),'andesite':(130,139,136),'stone_bricks':(161,156,140),'smooth_stone':(183,179,159),'white_concrete':(231,227,207),'dark_oak_log':(81,62,48),'oak_log':(109,84,55),'dark_oak_planks':(101,76,52),'deepslate_tiles':(61,69,76),'polished_blackstone_bricks':(49,54,60),'oak_leaves':(68,107,54),'azalea_leaves':(72,119,69),'bamboo':(94,132,66),'dark_oak_fence':(91,69,48),'lily_pad':(79,126,64)}
palette['gravel']=(155,151,139)
palette['stone_brick_stairs']=(162,158,145)
def typ(s):return s.split(':')[-1].split('[')[0]
def shape(s):
    t=typ(s)
    if t=='bamboo':return (.38,0,.38,.62,1,.62)
    if 'fence' in t:return (.36,0,.36,.64,1.4,.64)
    if t=='lily_pad':return (.05,0,.05,.95,.05,.95)
    if t=='water':return (0,0,0,1,.9,1)
    return (0,0,0,1,1,1)
dirs=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
facepoints=[];colors=[];centers=[];normals=[]
for (x,y,z),s in vox.items():
    t=typ(s);a,b,c,d,e,f=shape(s)
    corners=np.array([[x+a,y+b,z+c],[x+d,y+b,z+c],[x+d,y+e,z+c],[x+a,y+e,z+c],[x+a,y+b,z+f],[x+d,y+b,z+f],[x+d,y+e,z+f],[x+a,y+e,z+f]])
    ids=[[1,5,6,2],[4,0,3,7],[3,2,6,7],[0,4,5,1],[5,4,7,6],[0,1,2,3]]
    for i,(dx,dy,dz) in enumerate(dirs):
        ns=vox.get((x+dx,y+dy,z+dz))
        if ns and shape(ns)==(0,0,0,1,1,1) and shape(s)==(0,0,0,1,1,1):continue
        if ns and t=='water' and typ(ns)=='water':continue
        p=corners[ids[i]];facepoints.append(p);centers.append(p.mean(axis=0));normals.append(dirs[i]);base=np.array(palette.get(t,(190,100,160)));shade=[.8,.68,1,.5,.85,.73][i];colors.append(tuple((base*shade).astype(int)))
faces=np.asarray(facepoints);centers=np.asarray(centers);normals=np.asarray(normals);colors=np.asarray(colors)
out=ROOT/'证据'/('阶段'+mode if mode.isdigit() else '最终');out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
def render(name,eye,target,fov=66):
    w,h=1400,900;eye=np.array(eye,float);forward=np.array(target,float)-eye;forward/=np.linalg.norm(forward);right=np.cross(forward,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,forward)
    idx=np.flatnonzero(np.sum(normals*(eye-centers),axis=1)>0)
    p=faces[idx]-eye;depth=p@forward;keep=np.all(depth>.15,axis=1);idx=idx[keep];p=p[keep];depth=depth[keep]
    scale=w/(2*math.tan(math.radians(fov/2)));px=w/2+(p@right)*scale/depth;py=h*.49-(p@up)*scale/depth
    keep=(px.max(axis=1)>0)&(px.min(axis=1)<w)&(py.max(axis=1)>0)&(py.min(axis=1)<h);idx=idx[keep];px=px[keep];py=py[keep];depth=depth[keep]
    image=Image.new('RGB',(w,h),(198,216,218));draw=ImageDraw.Draw(image)
    for j in np.argsort(-depth.mean(axis=1)):
        draw.polygon(list(zip(px[j],py[j])),fill=tuple(colors[idx[j]]))
    draw.rectangle((0,h-62,w,h),fill=(29,39,39));draw.text((18,h-55),name+' | '+('阶段蓝图预览' if mode.isdigit() else '实际存档回读 · 简化方块透视'),font=font,fill='white');draw.text((18,h-29),f'Camera {list(eye)}  Target {target}  FOV {fov}° | 非游戏截图；栅栏、竹叶与纹理简化',font=font,fill=(207,222,213));image.save(out/(name+'.png'))
views=[('01-整体鸟瞰',[228,185,238],[90,66,76],62),('02-入口藏露',[38,65.62,145],[38,66,128],72),('03-出院见水',[67,65.62,112],[109,67,76],70),('04-听荷厅北望',[105,66.62,111],[104,69,62],68),('05-登山回望',[57,78.62,52],[107,65,78],72),('06-曲桥看山',[132,67.62,56],[65,75,61],70),('07-东岸临水',[151,66.62,94],[102,69,79],72),('08-竹院',[156,69.62,39],[171,70,50],70),('11-山亭中心原视点',[57,78.62,47],[115,65,102],72)]
for v in views:render(*v)
image=Image.new('RGB',(1110,894),(238,236,220));draw=ImageDraw.Draw(image)
for z in range(149):
    for x in range(185):
        column=[(y,s) for (xx,y,zz),s in []]
        for y in range(104,55,-1):
            s=vox.get((x,y,z))
            if s:draw.rectangle((x*6,z*6,x*6+5,z*6+5),fill=palette.get(typ(s),(190,100,160)));break
image.save(out/'09-顶视.png')
image=Image.new('RGB',(1480,700),(219,231,229));draw=ImageDraw.Draw(image)
for j,z in enumerate([47,64,89,117]):
    base=j*175+150
    for x in range(185):
        for y in range(58,96):
            s=vox.get((x,y,z))
            if s:draw.rectangle((x*8,base-(y-58)*4,x*8+7,base-(y-58)*4+3),fill=palette.get(typ(s),(190,100,160)))
    draw.text((8,j*175+2),f'剖面 Z={z} | X 0–184 | Y 58–95（竖向比例放大）',font=font,fill=(30,40,35))
image.save(out/'10-四道剖面.png');print(str(out))
