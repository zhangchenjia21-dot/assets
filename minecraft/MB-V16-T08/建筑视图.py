"""实存体素透视及剖面；不作游戏光照或材质效果的替代证明。"""
from pathlib import Path
import numpy as np,json,math,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;stage=sys.argv[1];meta=json.loads((R/f'证据/{stage}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{stage}.u16',dtype='<u2').reshape(84,144,160);pal=meta['palette']
colors=[]
for v in pal:
 s=v.split('[')[0];c=(156,160,156)
 for key,rgb in [('stone_brick',(153,153,141)),('sandstone',(215,205,172)),('andesite',(141,148,142)),('deepslate',(57,69,76)),('dark_oak',(95,72,47)),('dirt',(117,93,64)),('grass',(105,133,70)),('gravel',(144,137,116)),('glass',(142,187,197)),('torch',(244,191,71)),('air',(0,0,0))]:
  if key in s and (key!='air' or s in ['minecraft:air','minecraft:cave_air','minecraft:void_air']):c=rgb
 colors.append(c)
C=np.array(colors,float);empty=np.array([v in ['minecraft:air','minecraft:cave_air','minecraft:void_air','UNGENERATED'] for v in pal]);slabs=np.array(['_slab[' in v and 'type=double' not in v for v in pal]);upper=np.array(['type=top' in v for v in pal]);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
def render(name,eye,target,mono=False,w=920,h=600):
 eye=np.array(eye,float);f=np.array(target,float)-eye;f/=np.linalg.norm(f);right=np.cross(f,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,f)
 xx,yy=np.meshgrid((np.arange(w)+.5-w/2)/w*1.45,(h/2-np.arange(h)-.5)/w*1.45);d=(f+xx[:,:,None]*right+yy[:,:,None]*up).reshape(-1,3);d/=np.linalg.norm(d,axis=1)[:,None]
 sky=np.tile([191.,204.,211.],(len(d),1));low=np.array([0,12,0]);high=np.array([160,96,144]);inv=1/np.where(abs(d)<1e-8,1e-8,d);ta=(low-eye)*inv;tb=(high-eye)*inv;near=np.maximum(np.minimum(ta,tb).max(axis=1),0);far=np.maximum(ta,tb).min(axis=1);active=np.where(near<far)[0];t=near[active]+1e-5;d=d[active];pos=eye+t[:,None]*d;cell=np.floor(pos).astype(int);step=np.sign(d).astype(int);delta=abs(1/d);nextt=t[:,None]+(np.where(step>0,cell+1,cell)-pos)/d;norm=np.zeros_like(cell);norm[:,1]=1
 for iteration in range(650):
  if not len(active):break
  valid=(cell[:,0]>=0)&(cell[:,0]<160)&(cell[:,1]>=12)&(cell[:,1]<96)&(cell[:,2]>=0)&(cell[:,2]<144)&(t<far[active]);active=active[valid];t=t[valid];d=d[valid];cell=cell[valid];step=step[valid];delta=delta[valid];nextt=nextt[valid];norm=norm[valid]
  if not len(active):break
  ids=A[cell[:,1]-12,cell[:,2],cell[:,0]];hit=~empty[ids];pos=eye+(t+1e-5)[:,None]*d
  # 半砖求局部盒体交点，避免把屋脊缝隙误画成实心方块。
  mask=slabs[ids]&hit
  if mask.any():
   mi=cell[mask].astype(float);ma=mi+1;mi[:,1]+=np.where(upper[ids[mask]],.5,0);ma[:,1]-=np.where(upper[ids[mask]],0,.5);aa=(mi-eye)/d[mask];bb=(ma-eye)/d[mask];nt=np.maximum(np.minimum(aa,bb).max(axis=1),t[mask]);ft=np.maximum(aa,bb).min(axis=1);good=nt<=ft+1e-5;hit[mask]=good;pos[mask]=eye+(nt+1e-5)[:,None]*d[mask]
  if hit.any():
   n=norm[hit];light=.75+.19*np.maximum(n[:,1],0)+.08*n[:,0]-.11*n[:,2];col=np.tile([175.,174.,164.],(int(hit.sum()),1)) if mono else C[ids[hit]].copy();col*=light[:,None]
   frac=pos[hit]-np.floor(pos[hit]);edge=((frac<.015)|(frac>.985)).sum(axis=1)>1;col[edge]*=.9
   sky[active[hit]]=col
  keep=~hit;active=active[keep];t=t[keep];d=d[keep];cell=cell[keep];step=step[keep];delta=delta[keep];nextt=nextt[keep];norm=norm[keep]
  if not len(active):break
  axis=nextt.argmin(axis=1);rows=np.arange(len(axis));t=nextt[rows,axis];cell[rows,axis]+=step[rows,axis];norm[:]=0;norm[rows,axis]=-step[rows,axis];nextt[rows,axis]+=delta[rows,axis]
 im=Image.fromarray(np.uint8(np.clip(sky.reshape(h,w,3),0,255)));dr=ImageDraw.Draw(im);dr.rectangle((0,h-48,w,h),fill=(28,32,34));dr.text((10,h-46),f'T08 {stage} · {name} · 实存体素审计渲染，非客户端截图',font=font,fill='white');dr.text((10,h-23),f'相机 {tuple(map(float,eye))} → {target}；光照/复杂方块形状简化',font=font,fill='white');im.save(R/f'证据/{stage}-{name}.png');print(name,flush=True)
views=[('西南体量',(4,85,141),(78,30,69)),('东北体量',(151,88,7),(78,31,63)),('单色轮廓',(8,73,13),(80,31,61),True),('西入口',(10,21,53),(37,30,56)),('中殿向东',(39,20,56),(116,35,56)),('侧廊柱列',(42,20,43),(83,30,49)),('交叉向北',(94,20,62),(95,38,23)),('回廊尺度',(46,20,114),(72,24,80)),('宿舍上层',(85,29,118),(86,30,97)),('东端外观',(150,25,67),(123,36,56))]
selected=sys.argv[2:]
for i,v in enumerate(views):
 if not selected or str(i) in selected:render(*v)
for label,section in [('纵剖Z56',A[:,56,:]),('横剖X61',A[:,:,61])]:
 im=Image.fromarray(np.uint8(C[section[::-1]])).resize((section.shape[1]*7,588),Image.Resampling.NEAREST);im.save(R/f'证据/{stage}-{label}.png')
