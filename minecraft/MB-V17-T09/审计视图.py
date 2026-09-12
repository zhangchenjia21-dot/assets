"""从保存关闭后的真实方块快照绘制审计视图；不代替客户端效果。"""
from pathlib import Path
import numpy as np,json,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;stage=sys.argv[1];m=json.loads((R/f'证据/{stage}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{stage}.u16',dtype='<u2').reshape(56,144,144);pal=m['palette'];font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
C=[]
for s in pal:
 s=s.split('[')[0]
 c=(161,157,139)
 for key,v in [('dirt',(120,102,74)),('grass',(104,124,74)),('gravel',(161,151,133)),('bricks',(151,94,69)),('stone_brick',(150,149,135)),('sandstone',(207,190,148)),('quartz',(230,227,212)),('terracotta',(162,103,75)),('diorite',(191,192,181)),('andesite',(135,141,135)),('oak',(137,107,66)),('water',(69,139,165)),('glass',(140,182,183)),('torch',(233,170,67)),('magma',(128,68,28))]:
  if key in s:c=v
 if s in ['minecraft:air','minecraft:cave_air','UNGENERATED']:c=(0,0,0)
 C.append(c)
C=np.array(C,float);air=np.array([s in ['minecraft:air','minecraft:cave_air','UNGENERATED'] for s in pal]);half=np.array(['_slab[' in s and 'type=bottom' in s for s in pal])
views=[('东北总貌',(143,87,2),(76,26,74)),('西南总貌',(7,78,141),(75,28,76)),('单色体量',(7,73,8),(76,28,76),True),('入口门槛',(82,20,14),(82,23,37)),('冷厅纵向',(66,21,61),(100,28,61)),('冷厅向暖室',(82,21,62),(82,24,90)),('热室穹顶',(82,23,99),(82,32,113)),('庭院柱廊',(31,20,73),(53,23,42)),('服务炉房',(130,19,108),(102,21,108)),('水箱与阶梯',(141,41,78),(117,27,51)),('更衣室',(65,21,36),(98,24,36)),('暖室回望',(82,23,85),(82,25,60))]
def render(name,eye,target,mono=False):
 w,h=(800,540) if stage in ['04-Repair','reload'] else (640,432);eye=np.array(eye,float);f=np.array(target,float)-eye;f/=np.linalg.norm(f);right=np.cross(f,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,f)
 gx,gy=np.meshgrid((np.arange(w)+.5-w/2)/w*1.5,(h/2-np.arange(h)-.5)/w*1.5);dirs=(f+gx[...,None]*right+gy[...,None]*up).reshape(-1,3);dirs/=np.linalg.norm(dirs,axis=1)[:,None];dirs=np.where(abs(dirs)<1e-9,1e-9,dirs)
 lo=np.array([0,10,0]);hi=np.array([144,66,144]);u=(lo-eye)/dirs;v=(hi-eye)/dirs;near=np.maximum(np.minimum(u,v).max(1),0);far=np.maximum(u,v).min(1);active=np.where(far>near)[0];d=dirs[active];t=near[active]+1e-6;p=eye+t[:,None]*d;cells=np.floor(p).astype(int);step=np.sign(d).astype(int);dt=abs(1/d);nxt=t[:,None]+(np.where(step>0,cells+1,cells)-p)/d;normal=np.zeros_like(cells);normal[:,1]=1;out=np.tile([188.,204.,212.],(w*h,1))
 for _ in range(480):
  valid=(cells>=lo).all(1)&(cells<hi).all(1)&(t<far[active]);active=active[valid];d=d[valid];t=t[valid];cells=cells[valid];step=step[valid];dt=dt[valid];nxt=nxt[valid];normal=normal[valid]
  if not len(active):break
  ids=A[cells[:,1]-10,cells[:,2],cells[:,0]];hit=~air[ids];mask=half[ids]
  if mask.any():
   a=cells[mask].astype(float);b=a+1;b[:,1]-=.5;uu=(a-eye)/d[mask];vv=(b-eye)/d[mask];hit[mask]=np.maximum(np.minimum(uu,vv).max(1),t[mask])<=np.maximum(uu,vv).min(1)+1e-6
  col=np.tile([180.,175.,162.],(hit.sum(),1)) if mono else C[ids[hit]].copy();light=.76+.15*normal[hit,1]-.08*normal[hit,2]+.05*normal[hit,0];out[active[hit]]=col*light[:,None]
  keep=~hit;active=active[keep];d=d[keep];t=t[keep];cells=cells[keep];step=step[keep];dt=dt[keep];nxt=nxt[keep];normal=normal[keep]
  if not len(active):break
  axis=nxt.argmin(1);rows=np.arange(len(active));t=nxt[rows,axis];cells[rows,axis]+=step[rows,axis];normal[:]=0;normal[rows,axis]=-step[rows,axis];nxt[rows,axis]+=dt[rows,axis]
 im=Image.fromarray(np.uint8(np.clip(out.reshape(h,w,3),0,255)));dr=ImageDraw.Draw(im);dr.rectangle((0,h-46,w,h),fill=(31,35,37));dr.text((8,h-44),f'T09 {stage} {name} | 实存体素渲染，非客户端截图',font=font,fill='white');dr.text((8,h-22),f'{tuple(map(float,eye))} → {target} | 方块模型/光照简化',font=font,fill='white');im.save(R/f'证据/{stage}-{name}.png');print(name,flush=True)
views.extend([('热池使用视角',(72,23,107),(84,22,116)),('冷池池阶',(69,21,61),(69,17,53)),('厕间入口',(30,20,36),(30,20,26))])
for i,v in enumerate(views):
 if len(sys.argv)==2 or str(i) in sys.argv[2:]:render(*v)
for name,data in [('纵剖X82',A[:,:,82]),('横剖Z61',A[:,61,:]),('热区剖Z108',A[:,108,:])]:
 im=Image.fromarray(np.uint8(C[data[::-1]])).resize((1008,392),Image.Resampling.NEAREST);im.save(R/f'证据/{stage}-{name}.png')
# 使用地坪上三格的水平切片，而非屋顶俯视，暴露实际房间与门洞。
im=Image.fromarray(np.uint8(C[A[12]])).resize((864,864),Image.Resampling.NEAREST);im.save(R/f'证据/{stage}-平面Y22.png')
