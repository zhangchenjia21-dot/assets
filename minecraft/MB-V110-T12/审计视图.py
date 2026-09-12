"""从保存关闭后的 T12 体素绘制透视/剖面；不是客户端截图。"""
from pathlib import Path
import numpy as np,json,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(36,96,56);pal=m['palette'];font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
C=[];models=[];air=[]
for v in pal:
 n=v.split('[')[0];c=(170,163,141)
 for k,rgb in [('dirt',(120,101,75)),('grass',(93,119,70)),('gravel',(146,144,129)),('mud',(129,105,82)),('stone',(139,143,141)),('dark_oak',(84,59,39)),('spruce',(123,90,57)),('oak',(122,88,50)),('stripped_dark_oak',(93,69,48)),('white_terracotta',(204,181,157)),('deepslate',(63,69,72)),('quartz',(226,224,211)),('sandstone',(211,196,156)),('bamboo',(186,173,100)),('birch',(203,191,143)),('green_terracotta',(101,112,60)),('blue_wool',(54,72,134)),('white_wool',(233,229,206)),('red_wool',(154,53,42)),('yellow_wool',(207,170,61)),('glass',(206,216,204)),('chest',(154,105,54)),('barrel',(126,91,51)),('furnace',(92,96,94)),('moss',(91,115,64)),('leaves',(65,103,51)),('candle',(240,216,167)),('lantern',(212,158,71)),('torch',(229,163,64)),('flower_pot',(153,88,58)),('black_terracotta',(63,45,37)),('water',(66,126,159))]:
  if k in n:c=rgb
 if 'dark_oak' in n:c=(84,59,39)
 if '_carpet' in n:c=(91,115,64) if 'moss' in n else (174,157,110) if 'yellow' in n else (58,67,108) if 'blue' in n else (154,53,42) if 'red' in n else (221,211,185)
 if 'azalea' in n:c=(65,103,51)
 if 'cauldron' in n:c=(87,91,88)
 empty=n in ['minecraft:air','minecraft:cave_air','UNGENERATED'];air.append(empty);C.append((0,0,0) if empty else c)
 b=[([0,0,0],[1,1,1])]
 if '_slab[' in v:b=[([0,.5 if 'type=top' in v else 0,0],[1,1 if 'type=top' in v else .5,1])]
 if '_stairs[' in v:
  lo=[0,.5,0];hi=[1,1,1]
  if 'facing=north' in v:hi[2]=.5
  if 'facing=south' in v:lo[2]=.5
  if 'facing=west' in v:hi[0]=.5
  if 'facing=east' in v:lo[0]=.5
  b=[([0,0,0],[1,.5,1]),(lo,hi)]
 if '_fence[' in v:
  b=[([.375,0,.375],[.625,1,.625])]
  if 'east=true' in v or 'west=true' in v:b.append(([0 if 'west=true' in v else .375,.4,.4375],[1 if 'east=true' in v else .625,.85,.5625]))
  if 'north=true' in v or 'south=true' in v:b.append(([.4375,.4,0 if 'north=true' in v else .375],[.5625,.85,1 if 'south=true' in v else .625]))
 if '_pane[' in v:b=[([0,0,.4375],[1,1,.5625])] if 'east=true' in v or 'west=true' in v else [([.4375,0,0],[.5625,1,1])]
 if '_trapdoor[' in v:
  if 'open=false' in v:b=[([0,.8125 if 'half=top' in v else 0,0],[1,1 if 'half=top' in v else .1875,1])]
  elif 'facing=north' in v:b=[([0,0,.8125],[1,1,1])]
  elif 'facing=south' in v:b=[([0,0,0],[1,1,.1875])]
  elif 'facing=east' in v:b=[([0,0,0],[.1875,1,1])]
  else:b=[([.8125,0,0],[1,1,1])]
 if ':chest[' in v:b=[([.0625,0,.0625],[.9375,.875,.9375])]
 if '_carpet' in v:b=[([0,0,0],[1,.0625,1])]
 if 'azalea' in v:b=[([0,.5,0],[1,1,1]),([.25,0,.25],[.75,.5,.75])]
 if 'flower_pot' in v:b=[([.3125,0,.3125],[.6875,.375,.6875])]
 if 'candle[' in v:b=[([.35,0,.35],[.65,.5,.65])]
 if ':torch' in v:b=[([.44,0,.44],[.56,.65,.56])]
 if 'lantern[' in v:b=[([.3,.1,.3],[.7,.8,.7])]
 models.append(b)
C=np.array(C,float);air=np.array(air);partial=np.array([b!=[([0,0,0],[1,1,1])] for b in models]);mins=np.zeros((len(pal),3,3));maxs=np.zeros_like(mins)
for i,b in enumerate(models):
 for j,(lo,hi) in enumerate(b):mins[i,j]=lo;maxs[i,j]=hi
views=[('街上接近',(8,18.62,8),(25,22,23)),('正面中景',(25,18.62,9),(25,22,23)),('东北总貌',(53,51,2),(26,23,48)),('后庭总貌',(3,40,91),(25,22,51)),('前店',(23,19.62,20),(18,20,26)),('账房验货',(18,19.62,30),(27,20,29)),('通り庭',(34,18.62,22),(34,21,49)),('中庭取合',(20,18.62,38),(28,20,39)),('家庭起居',(27,19.62,47),(18,20,49)),('座敷望庭',(23,19.62,57),(23,20,71)),('厨房挑空',(34,18.62,44),(35,23,53)),('二层伙计',(26,25.62,31),(17,26,23)),('后庭缘侧',(21,18.62,71),(23,20,59)),('仓库',(32,19.62,79),(27,20,84)),('服务后路',(33,18.62,62),(35,19,74))]
views += [('中庭仰视',(20,18.62,38),(17,25,34)),('伙计室内',(19,25.62,30),(16,24.7,22)),('厨房使用',(34,18.62,48),(36,18,53)),('座敷室内',(21,19.62,60),(28,19.5,56))]
views += [('东墙脚',(35.2,18.62,21),(37,17.4,28)),('街门脚',(26,18.62,14),(24,16.8,17.5)),('仓库台阶脚',(29,18.62,73),(30,16.8,76)),('楼梯上行',(27.5,19.62,24.4),(27.5,24,30.5)),('楼梯顶部',(27.5,25.62,31.5),(26,21,26)),('东南边界',(41,18.62,67),(38,18,72))]
def render(name,eye,target):
 w,h=(640,420);eye=np.array(eye,float);f=np.array(target)-eye;f/=np.linalg.norm(f);right=np.cross(f,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,f)
 gx,gy=np.meshgrid((np.arange(w)+.5-w/2)/w*1.5,(h/2-np.arange(h)-.5)/w*1.5);dirs=(f+gx[...,None]*right+gy[...,None]*up).reshape(-1,3);dirs/=np.linalg.norm(dirs,axis=1)[:,None];dirs=np.where(abs(dirs)<1e-9,1e-9,dirs)
 lo=np.array([0,10,0]);hi=np.array([56,46,96]);u=(lo-eye)/dirs;v=(hi-eye)/dirs;near=np.maximum(np.minimum(u,v).max(1),0);far=np.maximum(u,v).min(1);active=np.where(far>near)[0];d=dirs[active];t=near[active]+1e-6;cells=np.floor(eye+t[:,None]*d).astype(int);step=np.sign(d).astype(int);dt=abs(1/d);nxt=t[:,None]+(np.where(step>0,cells+1,cells)-(eye+t[:,None]*d))/d;normal=np.zeros_like(cells);normal[:,1]=1;out=np.tile([187.,203.,211.],(w*h,1))
 for _ in range(300):
  valid=(cells>=lo).all(1)&(cells<hi).all(1)&(t<far[active]);active=active[valid];d=d[valid];t=t[valid];cells=cells[valid];step=step[valid];dt=dt[valid];nxt=nxt[valid];normal=normal[valid]
  if not len(active):break
  ids=A[cells[:,1]-10,cells[:,2],cells[:,0]];hit=~air[ids];mask=hit&partial[ids]
  if mask.any():
   ii=ids[mask];cc=cells[mask];dd=d[mask];hh=np.zeros(len(ii),bool)
   for j in range(3):
    uu=(cc+mins[ii,j]-eye)/dd;vv=(cc+maxs[ii,j]-eye)/dd;hh|=(maxs[ii,j]>mins[ii,j]).all(1)&(np.maximum(np.minimum(uu,vv).max(1),t[mask])<=np.minimum(np.maximum(uu,vv).min(1),nxt[mask].min(1))+1e-8)
   hit[mask]=hh
  light=.77+.15*normal[hit,1]-.08*normal[hit,2]+.04*normal[hit,0];out[active[hit]]=C[ids[hit]]*light[:,None];keep=~hit;active=active[keep];d=d[keep];t=t[keep];cells=cells[keep];step=step[keep];dt=dt[keep];nxt=nxt[keep];normal=normal[keep]
  if not len(active):break
  axis=nxt.argmin(1);rows=np.arange(len(active));t=nxt[rows,axis];cells[rows,axis]+=step[rows,axis];normal[:]=0;normal[rows,axis]=-step[rows,axis];nxt[rows,axis]+=dt[rows,axis]
 im=Image.fromarray(np.uint8(np.clip(out.reshape(h,w,3),0,255)));dr=ImageDraw.Draw(im);dr.rectangle((0,h-44,w,h),fill=(28,32,33));dr.text((7,h-42),f'T12 {s} {name}｜实存体素渲染，非客户端截图',font=font,fill='white');dr.text((7,h-21),f'{tuple(map(float,eye))} → {target}｜形状与光照简化',font=font,fill='white');im.save(R/f'证据/{s}-{name}.png');print(name,flush=True)
for i,v in enumerate(views):
 if len(sys.argv)==2 or str(i) in sys.argv[2:]:render(*v)
for name,data in [('纵剖X27',A[:,:,27]),('通庭剖X34',A[:,:,34]),('前店剖Z26',A[:,26,:]),('底层平面Y19',A[9]),('二层平面Y25',A[15])]:
 if '平面' not in name:data=data[::-1]
 im=Image.fromarray(np.uint8(C[data]));im.resize((data.shape[1]*8,data.shape[0]*8),Image.Resampling.NEAREST).save(R/f'证据/{s}-{name}.png')
