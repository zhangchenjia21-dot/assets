"""从已保存存档的读取快照渲染审计视图；无概念图、无生成式补绘。"""
from pathlib import Path
import numpy as np,json,sys,math,time
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;stage=sys.argv[1]
meta=json.loads((R/f'证据/{stage}-实存元数据.json').read_text());A=np.fromfile(R/f'证据/{stage}-实存方块.u16',dtype='<u2').reshape(meta['shape_yzx'])
pal=meta['palette'];colors=[]
for s in pal:
    s=s.split('[')[0]
    c=(187,145,93)
    for key,value in [('air',(0,0,0)),('sand',(212,180,120)),('sandstone',(208,172,115)),('cut_sandstone',(191,153,100)),('smooth_sandstone',(232,199,143)),('terracotta',(171,108,65)),('coarse_dirt',(135,110,69)),('packed_mud',(166,137,90)),('water',(55,142,152)),('leaves',(69,116,48)),('log',(117,91,56)),('wood',(113,87,51)),('planks',(163,123,73)),('slab',(194,159,105)),('fence',(128,100,61)),('grass',(99,126,55)),('fern',(88,118,46)),('dead_bush',(123,104,67)),('farmland',(102,79,48)),('wheat',(190,162,49)),('carrots',(69,126,35)),('hay',(172,144,50)),('white_wool',(232,218,180)),('brown_wool',(108,73,50)),('bricks',(157,84,61)),('torch',(248,190,76))]:
        if key in s:c=value
    if 'sandstone_slab' in s:c=(224,188,134)
    colors.append(c)
colors=np.array(colors,dtype=float);air=np.array([('air' in s or s=='UNGENERATED') for s in pal]);slabs=np.array([('slab[' in s and 'type=double' not in s) for s in pal]);tops=np.array(['type=top' in s for s in pal]);thin=np.array([any(k in s for k in ['short_grass','fern','wheat','carrots','dead_bush','torch']) for s in pal])
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
def render(name,eye,target,w=900,h=560,fov=65):
    eye=np.array(eye,dtype=float);f=np.array(target,dtype=float)-eye;f/=np.linalg.norm(f);right=np.cross(f,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,f)
    xx,yy=np.meshgrid((np.arange(w)+.5-w/2)/w*2*math.tan(math.radians(fov)/2),(h/2-np.arange(h)-.5)/w*2*math.tan(math.radians(fov)/2));dirs=(f+xx[:,:,None]*right+yy[:,:,None]*up).reshape(-1,3);dirs/=np.linalg.norm(dirs,axis=1)[:,None]
    n=len(dirs);sky=np.tile([183.,205.,212.],(n,1));sky+=np.clip(dirs[:,1,None],-.3,.7)*26
    lo=np.array([0.,12.,0.]);hi=np.array([288.,64.,240.]);inv=1/np.where(abs(dirs)<1e-9,1e-9,dirs)
    t1=(lo-eye)*inv;t2=(hi-eye)*inv;near=np.maximum(np.min(np.stack([t1,t2]),axis=0).max(axis=1),0);far=np.max(np.stack([t1,t2]),axis=0).min(axis=1)
    active=np.where(far>near)[0];t=near[active]+.0001;d=dirs[active];p=eye+t[:,None]*d;c=np.floor(p).astype(int);step=np.sign(d).astype(int);delta=abs(1/d);boundary=np.where(step>0,c+1,c);nextt=t[:,None]+(boundary-p)/d;normal=np.zeros_like(c);normal[:,1]=1
    # DDA 穿过空格；半砖按原生上下半格检查，其余复杂块使用格点占位审计。
    for _ in range(900):
        if not len(active):break
        valid=(c[:,0]>=0)&(c[:,0]<288)&(c[:,1]>=12)&(c[:,1]<64)&(c[:,2]>=0)&(c[:,2]<240)&(t<=far[active])
        active=active[valid];t=t[valid];d=d[valid];c=c[valid];step=step[valid];delta=delta[valid];nextt=nextt[valid];normal=normal[valid]
        if not len(active):break
        ids=A[c[:,1]-12,c[:,2],c[:,0]];hit=~air[ids]
        pos=eye+(t+.0002)[:,None]*d
        # 草本用稀疏交叉层替代整立方，避免遮住近地层；所有位置来自实存。
        grass=thin[ids];hit &= ~grass | (((pos[:,0]*7+pos[:,2]*11)%1)<.35)
        sh=slabs[ids];frac=pos[:,1]-c[:,1];hit &= ~sh | np.where(tops[ids],frac>=.5,frac<=.5)
        if hit.any():
            loc=c[hit];nn=normal[hit];col=colors[ids[hit]].copy();light=.73+.19*np.maximum(nn[:,1],0)+.13*nn[:,0]-.10*nn[:,2]
            posh=pos[hit];grain=((loc[:,0]*17+loc[:,1]*23+loc[:,2]*31)%13-6)*.75
            col*=light[:,None];col+=grain[:,None]
            # 格边帮助辨认尺度，非外部材质或虚构细节。
            frac=posh-np.floor(posh);edge=((frac<.024)|(frac>.976)).sum(axis=1)>1;col[edge]*=.88
            fog=np.minimum(.35,t[hit]/650);col=col*(1-fog[:,None])+np.array([203,197,169])*fog[:,None];sky[active[hit]]=col
        keep=~hit;active=active[keep];t=t[keep];d=d[keep];c=c[keep];step=step[keep];delta=delta[keep];nextt=nextt[keep];normal=normal[keep]
        if not len(active):break
        axis=nextt.argmin(axis=1);rows=np.arange(len(axis));t=nextt[rows,axis];c[rows,axis]+=step[rows,axis];normal[:]=0;normal[rows,axis]=-step[rows,axis];nextt[rows,axis]+=delta[rows,axis]
    im=Image.fromarray(np.uint8(np.clip(sky.reshape(h,w,3),0,255)));draw=ImageDraw.Draw(im);draw.rectangle((0,h-53,w,h),fill=(30,32,29));draw.text((12,h-49),f'T07 / {stage} / {name}   实际存档体素审计渲染（非客户端截图）',font=font,fill='white');draw.text((12,h-26),f'视点 {tuple(map(float,eye))} → {tuple(target)}；形状/光照简化，流体运行未验证',font=font,fill=(210,210,185));out=R/'证据'/f'{stage}-{name}.png';im.save(out);print(out,flush=True)
views=[('东南总览',(294,115,247),(137,20,114)),('西北总览',(18,95,18),(144,22,121)),('南来道路',(231,24,202),(175,30,135)),('门前抵达',(186,23,165),(177,29,135)),('院落回望',(177,23,105),(177,28,140)),('西侧水荫',(59,23,127),(115,25,106)),('田间步行',(98,23,194),(83,29,148)),('北脊剖望',(101,43,34),(132,20,134))]
selection=sys.argv[2:]
for i,v in enumerate(views):
    if not selection or str(i) in selection:render(*v)
# 平面和剖面是独立几何辅助，不能替代上述透视。
if not selection:
    solid=~air[A];height=np.argmax(solid[::-1],axis=0);ix=A.shape[0]-1-height;ids=A[ix,np.arange(240)[:,None],np.arange(288)[None,:]];img=Image.fromarray(np.uint8(colors[ids])).resize((1152,960),Image.Resampling.NEAREST);img.save(R/'证据'/f'{stage}-俯视.png')
    img=Image.fromarray(np.uint8(colors[A[:,108,:][::-1]])).resize((1152,208),Image.Resampling.NEAREST);img.save(R/'证据'/f'{stage}-剖面Z108.png')
