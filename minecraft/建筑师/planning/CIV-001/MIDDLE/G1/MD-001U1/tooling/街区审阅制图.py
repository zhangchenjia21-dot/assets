"""从同一设计实体生成等比例平剖面与离线斜视；不使用生成式图像代替几何证据。"""
import math,json,gzip,importlib.util
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageColor
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('design',HERE/'街区设计编译.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
OUT=d.OUT;VIS=OUT/'visual';VIS.mkdir(exist_ok=True)
DATA=d.read(OUT/'URBAN-ENSEMBLE.json');B=DATA['buildings'];CIRC=d.read(OUT/'circulation.json')
MODEL=json.load(gzip.open(OUT/'design-model.json.gz','rt',encoding='utf8'));BOX=MODEL['boxes'];COLORS=MODEL['colors']
FONT='C:/Windows/Fonts/msyh.ttc'
def font(s):return ImageFont.truetype(FONT,s)
def txt(dr,xy,t,size=20,fill='#263932'):dr.text(xy,t,font=font(size),fill=fill)
PALETTE=['#b8804b','#c7b58e','#a76a50','#85917a','#a99a76']
def page(title,sub,w=1600,h=1100):
    im=Image.new('RGB',(w,h),'#f4f0e6');dr=ImageDraw.Draw(im)
    txt(dr,(42,23),title,32);txt(dr,(44,72),sub,18,'#59645b');return im,dr
def save(im,name):im.save(VIS/name,optimize=True)

def plan(mode='plan'):
    titles={'plan':'G1 门户微街区｜总平面与生活/货物流线','roof':'屋顶与天际线｜高仓、三层旅舍、低檐服务屋','phasing':'分期生长｜短仓与商住先成立，沿院落补足生活'}
    im,dr=page(titles[mode],'北 ↑  /  1 格 = 1 block-column；平面 X/Z 同比例。设计提案，非现状建筑。')
    sc=17;ox=75;oz=146;x0=185;z0=1690
    def p(x,z):return (ox+(x-x0)*sc,oz+(z-z0)*sc)
    def r(a,b,c,e,fill,outline=None,width=1):dr.rectangle((*p(a,b),*p(c,e)),fill=fill,outline=outline,width=width)
    for (x,z),v in d.SURF.items():
        if 185<=x<=241 and 1690<=z<=1730:
            y=v['ground_y'];col=(154+(y-62)*9,169+(y-62)*6,124+(y-62)*7)
            if (x,z) not in d.ENVELOPE:col=(224,224,208)
            if (x,z) in d.CLEAR:col=(227,189,121)
            r(x,z,x+1,z+1,col)
    for x,z in d.ENVELOPE:
        for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
            if (x+dx,z+dz) not in d.ENVELOPE:
                a,b=(p(x+1,z),p(x+1,z+1)) if dx==1 else (p(x,z),p(x,z+1)) if dx==-1 else (p(x,z+1),p(x+1,z+1)) if dz==1 else (p(x,z),p(x+1,z))
                dr.line([a,b],fill='#294d43',width=3)
    for b,col in zip(B,PALETTE):
        x,z,X,Z=b['bounds'];X+=1;Z+=1
        if mode=='phasing':col={1:'#be784b',2:'#87a58d',3:'#b3a4bb'}[b['phase']]
        r(x,z,X,Z,col,'#463d34',2)
        if mode=='roof':
            if b['roof_axis']=='x':dr.line([p(x-1,(z+Z)/2),p(X+1,(z+Z)/2)],fill='#51372d',width=4)
            else:dr.line([p((x+X)/2,z-1),p((x+X)/2,Z+1)],fill='#51372d',width=4)
        else:
            for dx,dz,dy,w in b['doors']:
                if dx==x:r(dx,dz,dx+1,dz+w,'#eee7c9')
                else:r(dx,dz,dx+w,dz+1,'#eee7c9')
        txt(dr,p(x+1,z+1),b['id']+(' / F'+str(b['phase']) if mode=='phasing' else ''),19,'#fff9ec')
        txt(dr,p(x+1,z+3),str(len(b['floors']))+'层',16,'#fff9ec')
    if mode=='plan':
        for rt in CIRC['routes']:
            if rt['kind']=='interior':continue
            pts=[p(x,z) for x,y,z in rt['points']];col='#9a422e' if rt['kind']=='pack-and-hand-cargo' else '#305f79'
            dr.line(pts,fill=col,width=4)
            for pp in [pts[0],pts[-1]]:dr.ellipse((pp[0]-3,pp[1]-3,pp[0]+3,pp[1]+3),fill=col)
        for a,col in [([201,1709,216,1712],'#d2bc8d'),([228,1708,233,1711],'#d49c75')]:
            dr.rectangle((*p(a[0],a[1]),*p(a[2]+1,a[3]+1)),outline=col,width=3)
        for x,z,label in [(211,1712,'水'),(224,1709,'消'),(190,1717,'污')]:
            dr.ellipse((*p(x-.5,z-.5),*p(x+.8,z+.8)),fill='#ebe8d4',outline='#334b46');txt(dr,p(x-.4,z-.5),label,15)
        # 剖切位置与第二张图严格对应。
        for a,b,lab in [(p(188,1703),p(238,1703),'A-A'),(p(207,1694),p(207,1728),'B-B')]:
            dr.line([a,b],fill='#635679',width=1);txt(dr,a,lab,16,'#493b60')
    # 当前树干位置，不将待处理内容从事实图上擦掉。
    for v in d.read(OUT/'validation/local-context.json')['log_blocks_in_envelope']:
        x,y,z,_=v;xx,zz=p(x+.5,z+.5);dr.ellipse((xx-3,zz-3,xx+3,zz+3),fill='#963f40')
    for x in range(190,241,10):txt(dr,p(x,1731),str(x),16)
    for z in range(1690,1731,10):txt(dr,(8,p(185,z)[1]),str(z),15)
    dr.line([p(187,1735),p(197,1735)],fill='#263932',width=5);txt(dr,p(187,1736),'10 blocks',18)
    tx=1100;yy=155
    for b in B:
        txt(dr,(tx,yy),b['id']+' '+b['name'],22);yy+=34
        txt(dr,(tx,yy),'地坪 '+str(b['floors'])+' / 脊 '+str(round(b['ridge_y'],2)),16);yy+=31
        txt(dr,(tx,yy),str(b['footprint_area'])+' 格主体占地',16);yy+=49
    for line in ['包络 1,310 格 · 主体 487 格','覆盖率 37.18% · 地上毛楼面 1,046 格','黄带：accepted through-clearance','红点：当前木干（块位，不是株数）','水源未确认；水/消/污为设施预留点','R1 通行链位于南侧，向东北续接 N1','主路尚有树木，不宣称已清通','world writes = 0']:
        txt(dr,(tx,yy),line,17);yy+=29
    save(im,{'plan':'01-top-plan.png','roof':'04-roof-skyline.png','phasing':'05-growth-phases.png'}[mode])

def sections():
    im,dr=page('关键剖面｜各台地独立落地，楼层与楼梯同步校核','X/Y 或 Z/Y 均为 1:1；绿色线为现状地面；剖切实体来自同一 design-model。')
    for row,(axis,fixed,lo,hi,title) in enumerate([('x',1703,187,239,'A-A  Z=1703｜修理住屋 — 旅舍 — 高台短仓'),('z',207,1693,1727,'B-B  X=207｜三层旅舍楼梯 — 生活院 — 南侧接口')]):
        sx=16;ox=80;oy=565+row*475
        def p(a,y):return (ox+(a-lo)*sx,oy-(y-60)*sx)
        txt(dr,(55,120+row*475),title,24)
        for y in range(60,85,5):dr.line([p(lo,y),p(hi,y)],fill='#dbd8ca');txt(dr,(30,p(lo,y)[1]),str(y),15)
        for k in range(lo,hi):
            key=(k,fixed) if axis=='x' else (fixed,k)
            if key in d.SURF:
                gy=d.SURF[key]['ground_y']+1;dr.line([p(k,gy),p(k+1,gy)],fill='#7a875e',width=3)
        for v in BOX:
            i=2 if axis=='x' else 0;j=0 if axis=='x' else 2
            if v['a'][i]<=fixed+.5<v['b'][i] and v['b'][j]>lo and v['a'][j]<hi:
                a=p(v['a'][j],v['b'][1]);b=p(v['b'][j],v['a'][1]);dr.rectangle((*a,*b),fill=COLORS[v['material']])
        for b in B:
            x,z,X,Z=b['bounds'];a=x if axis=='x' else z;c=X if axis=='x' else Z
            if (z<=fixed<=Z if axis=='x' else x<=fixed<=X):txt(dr,p((a+c)/2,b['ridge_y']+1),b['id'],19)
        dr.line([(1050,oy-80),(1210,oy-80)],fill='#304a40',width=4);txt(dr,(1050,oy-65),'10 blocks / H=V',16)
    save(im,'02-sections.png')

def floorplans():
    im,dr=page('各栋使用平面｜独立入口、楼梯孔与起居带','同一比例 15 px / block；暖色＝活动区原型，深色＝墙/梁/梯；门洞留白。',1600,1280)
    for j,b in enumerate(B):
        x,z,X,Z=b['bounds'];scale=15;ox=45+j*305
        txt(dr,(ox,123),b['id']+' '+b['type'],17)
        for level,fy in enumerate(b['floors']):
            oy=180+level*315
            def p(xx,zz):return (ox+(xx-x)*scale,oy+(zz-z)*scale)
            txt(dr,(ox,oy-28),'地坪 Y'+str(fy),18)
            dr.rectangle((*p(x,z),*p(X+1,Z+1)),fill='#e4d6b8',outline='#4d5147',width=2)
            for v in BOX:
                if v['owner']!=b['id'] or v['role'] in ['roof','gable','tie-beam','canopy','canopy-post']:continue
                if v['a'][1]<=fy+1.5<v['b'][1]:
                    dr.rectangle((*p(v['a'][0],v['a'][2]),*p(v['b'][0],v['b'][2])),fill=COLORS[v['material']])
            for rt in CIRC['routes']:
                if rt['id'].startswith(b['id']) and rt['points'][0][1]==fy:dr.line([p(a,c) for a,y,c in rt['points']],fill='#416b87',width=2)
            for st in CIRC['stairs']:
                if st['owner']==b['id'] and st['samples'][0][1]==fy:
                    dr.line([p(a,c) for a,y,c in st['samples']],fill='#914f3c',width=3)
            program=b['program'][level]
            for i in range(0,len(program),15):txt(dr,(ox,oy+190+(i//15)*24),program[i:i+15],16)
    txt(dr,(45,1175),'楼梯样本检查≠真实客户端碰撞验证。每个上层有独立检验的梯口→活动带路径；屏风仅划分寝区，不封死起居。',19)
    save(im,'03-floor-plans.png')

def render(boxes,eye,target,size=(1500,1000),margin=65,title='',scale_override=None):
    im,dr=page(title,'离线设计斜视 · 简化材料与光照 · 非 Minecraft 截图 · 非施工完成证明',*size)
    if size[0]<800:
        im=Image.new('RGB',size,'#f4f0e6');dr=ImageDraw.Draw(im)
        txt(dr,(20,20),title,21);txt(dr,(20,58),'离线几何原型 · 未建成 / 未注册',15)
    forward=np.array(target,dtype=float)-np.array(eye);forward/=np.linalg.norm(forward)
    right=np.cross(forward,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,forward)
    def project(v):return np.array([np.dot(v,right),-np.dot(v,up),np.dot(v,forward)])
    faces=[]
    for v in boxes:
        x,y,z=v['a'];X,Y,Z=v['b'];color=np.array(ImageColor.getrgb(COLORS[v['material']]))
        fs=[([(x,Y,z),(X,Y,z),(X,Y,Z),(x,Y,Z)],[0,1,0],1.10),
            ([(x,y,z),(X,y,z),(X,Y,z),(x,Y,z)],[0,0,-1],.83),
            ([(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],[0,0,1],.88),
            ([(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)],[-1,0,0],.72),
            ([(X,y,z),(X,y,Z),(X,Y,Z),(X,Y,z)],[1,0,0],.96)]
        for verts,n,shade in fs:
            if np.dot(n,forward)>=-.001:continue
            pp=[project(q) for q in verts];faces.append((sum(q[2] for q in pp)/4,pp,tuple(np.clip(color*shade,0,255).astype(int))))
    points=np.array([p for _,ps,c in faces for p in ps]);mn=points[:,:2].min(axis=0);mx=points[:,:2].max(axis=0)
    scale=min((size[0]-2*margin)/(mx[0]-mn[0]),(size[1]-170)/(mx[1]-mn[1])) if scale_override is None else scale_override
    off=np.array([(size[0]-(mx[0]-mn[0])*scale)/2,140])
    # 逐像素深度缓冲，避免长屋面在画家排序中被短山墙错误覆盖。
    rgb=np.array(im);depth=np.full((size[1],size[0]),np.inf)
    for dep,ps,c in faces:
        pp=[np.r_[((q[:2]-mn)*scale+off),q[2]] for q in ps]
        for ia,ib,ic in [(0,1,2),(0,2,3)]:
            a,b,e=pp[ia],pp[ib],pp[ic]
            l=max(0,math.floor(min(a[0],b[0],e[0])));r=min(size[0]-1,math.ceil(max(a[0],b[0],e[0])))
            t=max(110,math.floor(min(a[1],b[1],e[1])));bot=min(size[1]-1,math.ceil(max(a[1],b[1],e[1])))
            if l>r or t>bot:continue
            xx,yy=np.meshgrid(np.arange(l,r+1)+.5,np.arange(t,bot+1)+.5)
            den=(b[1]-e[1])*(a[0]-e[0])+(e[0]-b[0])*(a[1]-e[1])
            if abs(den)<1e-8:continue
            u=((b[1]-e[1])*(xx-e[0])+(e[0]-b[0])*(yy-e[1]))/den
            v=((e[1]-a[1])*(xx-e[0])+(a[0]-e[0])*(yy-e[1]))/den;w=1-u-v
            zz=u*a[2]+v*b[2]+w*e[2];old=depth[t:bot+1,l:r+1]
            keep=(u>=-1e-6)&(v>=-1e-6)&(w>=-1e-6)&(zz<old-1e-5)
            old[keep]=zz[keep];rgb[t:bot+1,l:r+1][keep]=c
    im=Image.fromarray(rgb)
    return im

def views():
    context=[]
    for (x,z),s in d.SURF.items():
        if 185<=x<=241 and 1692<=z<=1728:
            y=s['ground_y']+1
            for b in B:
                xx,zz,X,Z=b['bounds']
                if xx<=x<=X and zz<=z<=Z:y=min(s['ground_y'],b['floors'][0]-1)
            context.append({'a':[x,60,z],'b':[x+1,y,z+1],'material':'soil' if (x,z) in d.CLEAR else 'grass'})
    for i,(eye,title) in enumerate([([173,95,1744],'西南到达｜南侧全天通行，商住向共享院开后门'),([251,91,1733],'东南装卸｜高台短仓与低檐消息屋分立'),([183,90,1673],'西北回望｜低台修理、三层旅舍与高仓错落')],1):
        im=render(BOX+context,eye,[212,69,1710],title=title);save(im,f'06-oblique-{i}.png')
    # 切开旅舍南半部，露出三层楼梯和起居带，补足外壳预览看不到的空间。
    cut=[]
    for v in BOX:
        if v['owner']!='B2':continue
        if v['role'] in ['roof','gable','tie-beam']:continue
        if v['a'][2]>=1705:continue
        q=dict(v);q['b']=list(v['b']);q['b'][2]=min(q['b'][2],1705);cut.append(q)
    save(render(cut,[220,85,1725],[207,70,1702],title='旅舍剖透视｜三层直跑楼梯与逐层开洞'),'06-oblique-4-cutaway.png')
    im,dr=page('Middle Kit v0.1｜同一构造传统，不同用途与地形','原型均来自本轮设计模型；材料为审阅色，不是建成、已接受或已注册资产。',1600,1150)
    for i,b in enumerate(B):
        x,z,X,Z=b['bounds'];tile=render([v for v in BOX if v['owner']==b['id']],[x-20,90,Z+25],[(x+X)/2,70,(z+Z)/2],size=(500,460),title=b['id']+' '+b['type'])
        im.paste(tile,((i%3)*525+12,(i//3)*475+130))
    txt(dr,(1100,670),'参数保留用途因果',24)
    for j,t in enumerate(['基座依真实地面独立找平','结构跨间 3–5 格为提案','店门 / 仓门 / 家门分级','楼梯宽 2，顶孔随层差变化','屋脊随作业面与转角改变','材料变化来自构件与维修','每次场地适配后重新核验']):txt(dr,(1080,715+j*35),t,19)
    save(im,'07-kit-overview.png')

if __name__=='__main__':
    for mode in ['plan','roof','phasing']:plan(mode)
    sections();floorplans();views()
