"""复算水面分量、浅层见证与规划带叠置；这些几何/物质检查不裁定规划语义。"""
from pathlib import Path
import json,collections
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;C=R.parents[3]/'MP-P03-cache'
def dump(p,v):(R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
a=np.load(C/'terrain.npz');h=a['height'];w=a['water'];mask=w>-999;seen=set();out=[]
for z,x in zip(*np.where(mask)):
 if (z,x) in seen:continue
 stack=[(z,x)];seen.add((z,x));c=[]
 while stack:
  zz,xx=stack.pop();c.append((zz,xx))
  for nz,nx in [(zz-1,xx),(zz+1,xx),(zz,xx-1),(zz,xx+1)]:
   if 0<=nz<288 and 0<=nx<320 and mask[nz,nx] and (nz,nx) not in seen:seen.add((nz,nx));stack.append((nz,nx))
 if len(c)<4:continue
 zs,xs=map(np.array,zip(*c));out.append({'area_columns':len(c),'bounds':[int(xs.min()+640),int(zs.min()+1488),int(xs.max()+640),int(zs.max()+1488)],'water_y_values':np.unique(w[zs,xs]).tolist(),'edge_censored':bool((zs==0).any() or(zs==287).any()or(xs==0).any()or(xs==319).any()),'meaning':'二维相邻含水列，不证明三维水流、饮用、水量或池塘'})
dump('evidence/water-components.json',out)
raw=json.loads((C/'surface.json').read_text(encoding='utf8'));p=json.loads((R/'planning-data.json').read_text(encoding='utf8'))
def pm(poly):
 im=Image.new('1',(320,288));ImageDraw.Draw(im).polygon([(x-640,z-1488) for x,z in poly],fill=1);return np.array(im)
out=[]
for d in p['districts']:
 m=pm(d['polygon']);wit=[v for v in raw['substrate_witnesses'] if m[v['z']-1488,v['x']-640]];cnt=collections.Counter(raw['palette'][i] for v in wit for i in v['state_ids']);out.append({'district':d['id'],'witness_count':len(wit),'blocks':dict(cnt),'meaning':'8格离散13层见证，不能证明柱间无空洞'})
dump('evidence/district-substrate-witnesses.json',out)
issues=[]
for q in p['routes']:
 im=Image.new('1',(320,288));ImageDraw.Draw(im).line([(x-640,z-1488) for x,z in q['points']],fill=1,width=q['width_range'][0]);m=np.array(im)
 for f in p['frontages']:
  overlap=m&pm(f['polygon'])
  if overlap.any():issues.append({'route':q['id'],'frontage':f['id'],'overlap_columns':int(overlap.sum())})
dump('evidence/route-frontage-overlap.json',issues)
voids=json.loads((R/'evidence/shallow-void-columns.json').read_text(encoding='utf8'))['void_columns'];vm=np.zeros((288,320),dtype=bool)
for v in voids:vm[v['z']-1488,v['x']-640]=True
intersections=[]
for f in p['frontages']+p['spaces']:
 m=pm(f['polygon']);intersections.append({'id':f['id'],'void_column_overlap':int((m&vm).sum()),'soil_column_overlap':int((m&(a['surface']==1)).sum())})
for q in p['routes']:
 im=Image.new('1',(320,288));ImageDraw.Draw(im).line([(x-640,z-1488) for x,z in q['points']],fill=1,width=q['width_range'][0]);intersections.append({'id':q['id'],'void_column_overlap':int((np.array(im)&vm).sum())})
dump('evidence/shallow-void-planning-intersections.json',intersections)
print('substrate',out);print('route/frontage raster overlaps',issues)
print('void/frontage intersections',intersections)
