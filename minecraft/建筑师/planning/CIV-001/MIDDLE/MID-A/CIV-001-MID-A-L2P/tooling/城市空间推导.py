import os
from pathlib import Path
from collections import deque,Counter
import json,numpy as np,hashlib
C=Path(os.environ['MID_A_CACHE']);R=Path(os.environ['MID_A_REPO']);P=R/'minecraft/建筑师';O=Path(os.environ['MID_A_OUTPUT'])
O.mkdir(parents=True,exist_ok=True)
def w(n,s):p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n',encoding='utf-8',newline='\n')
def j(n,v):w(n,json.dumps(v,ensure_ascii=False,indent=2))
a=np.load(C/'current.npz');obs=json.loads((C/'current-observation.json').read_text('utf-8'));old=np.load(Path(os.environ['MID_A_L1_CACHE'])/'regional-map.npz');shape=old['height'].shape
rows=a['rows'];sub=a['sub'];states=obs['states'];y=np.full(shape,-32768,np.int16);surface=np.full(shape,-1,np.int16);logs=np.zeros(shape,np.int16);leaves=logs.copy();z,x=np.indices(shape);x+=89;z+=1453
for xx,zz,top,gy,s,l,leaf in rows:y[zz-1453,xx-89]=gy;surface[zz-1453,xx-89]=s;logs[zz-1453,xx-89]=l;leaves[zz-1453,xx-89]=leaf
def dilate(mask,n):
 out=mask.copy()
 for _ in range(n):
  q=np.pad(out,1);out=q[1:-1,1:-1]|q[:-2,1:-1]|q[2:,1:-1]|q[1:-1,:-2]|q[1:-1,2:]
 return out
def connected(mask):
 seen=np.zeros(shape,bool);groups=[]
 for zz,xx in zip(*np.where(mask)):
  if seen[zz,xx]:continue
  q=deque([(zz,xx)]);seen[zz,xx]=1;cells=[]
  while q:
   zz,xx=q.popleft();cells.append((zz,xx))
   for dz,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
    nz,nx=zz+dz,xx+dx
    if 0<=nz<shape[0] and 0<=nx<shape[1] and mask[nz,nx] and not seen[nz,nx]:seen[nz,nx]=1;q.append((nz,nx))
  groups.append(cells)
 return sorted(groups,key=len,reverse=True)
def rle(mask):
 out=[]
 for zi,row in enumerate(mask):
  diff=np.diff(np.pad(row.astype(np.int8),(1,1)));out += [[zi+1453,int(lo)+89,int(hi)+89] for lo,hi in zip(np.where(diff==1)[0],np.where(diff==-1)[0]-1)]
 return out
city=a['C2_LINKED_CORE'].copy();groups=connected(city);city[:]=0
for zz,xx in groups[0]:city[zz,xx]=1
wet=np.zeros(shape,bool);void=wet.copy();anomaly=wet.copy()
for xx,yy,zz,si in sub:
 if not city[zz-1453,xx-89]:continue
 if yy<=y[zz-1453,xx-89]-2:
  name=states[si]
  if name in ['minecraft:air','minecraft:cave_air','minecraft:void_air']:void[zz-1453,xx-89]=1
  if name in ['minecraft:water','minecraft:lava']:wet[zz-1453,xx-89]=1
  if 'infested' in name or 'cobblestone' in name:anomaly[zz-1453,xx-89]=1
habitat=np.zeros(shape,bool)
for be in obs['block_entities']:
 xx,zz=be['x'],be['z']
 if be['y']>0:habitat[zz-1453,xx-89]=1
shore=np.zeros(shape,bool)
for state in ['minecraft:water']:shore|=surface==states.index(state)
# 保留面是L2公开空间/限制层，不是逐建筑可建性自动裁决。
reserved=city&(dilate(shore,5)|dilate(void|wet|anomaly,3)|dilate(habitat,5)|(y>70))
active=city&~reserved
# 片区是城市内部责任范围，所有范围均允许混合使用；阈值按接口/扩宽/服务后场关系裁定。
quarters={'Q-GATE':city&(x<=235),'Q-MARKET':city&(x>235)&(z<1730),'Q-YARDS':city&(x>235)&(z>=1730)}
summary=[]
for key in ['C1_GATEWAY','C2_LINKED_CORE','C3_NORTH_CORE']:
 mask=a[key];rr=rows[mask[rows[:,1]-1453,rows[:,0]-89]]
 summary.append(dict(id=key,area=int(mask.sum()),y_percentiles=np.percentile(rr[:,3],[0,10,50,90,100]).tolist(),surface_counts=dict(Counter(states[i] for i in rr[:,4])),log_blocks=int(rr[:,5].sum()),leaf_blocks=int(rr[:,6].sum()),connected_groups=[len(g) for g in connected(mask)],runs=rle(mask)))
qstats=[]
for k,mask in quarters.items():qstats.append(dict(id=k,area=int(mask.sum()),non_roof_reserve=int(np.sum(mask&reserved)),working_fabric_area=int(np.sum(mask&active)),runs=rle(mask)))
critical=[]
for name,mask in [('shallow_void_columns',void),('shallow_water_columns',wet),('habitat',habitat),('public_non_roof_reserve',reserved)]:critical.append(dict(id=name,area=int(mask.sum()),runs=rle(mask)))
jj=dict(schema='mid-a-settlement-geometry/1',authority='DESIGN_PROPOSAL_WITH_CURRENT_EVIDENCE',bounds=[89,1453,1188,2382],selected='C2_LINKED_CORE',candidate_summaries=summary,city_area=int(city.sum()),city_runs=rle(city),city_components=[len(g) for g in groups],districts=qstats,reserves=critical,active_fabric_area=int(active.sum()),meaning='Inclusive [z,x0,x1] block-column membership. Exact proposed settlement edge, NOT building permission. Quarter edges are planning responsibility seams adaptable with reciprocal agreement; not political lines.',world_writes=0)
j('evidence/settlement-geometry.json',jj)
# 当前完整表层轻量RLE，支持审核新世界观测；浅层全量保留本地，只交付异常逐体素见证。
surf_runs=[]
for zz in range(1570-8,1845+9):
 rr=sorted((v for v in rows if v[1]==zz),key=lambda v:v[0]);run=None
 for xx,_,top,gy,si,l,leaf in rr:
  val=[int(gy),int(si),int(l),int(leaf)]
  if run and int(xx)==run[2]+1 and val==run[3:]:run[2]=int(xx)
  else:
   if run:surf_runs.append(run)
   run=[int(zz),int(xx),int(xx),*val]
 if run:surf_runs.append(run)
(C/'current-surface-runs.json').write_text(json.dumps(dict(schema='surface-runs/1',states=states,runs=surf_runs)),encoding='utf-8')
witnesses=rows[(rows[:,0]%16==0)&(rows[:,1]%16==0)].tolist()
for si in range(len(states)):
 witnesses.extend(rows[rows[:,4]==si][:3].tolist())
j('evidence/surface-witnesses.json',dict(schema='stratified-surface-witnesses/1',fields=['x','z','world_surface_y','exposed_y','state_index','stripped_logs','stripped_leaves'],states=states,design='16-grid plus first three columns per exposed material; not full observation',rows=witnesses))
special=[]
for xx,yy,zz,si in sub:
 if states[si] in ['minecraft:air','minecraft:cave_air','minecraft:water','minecraft:lava'] or 'infested' in states[si]:special.append([int(xx),int(yy),int(zz),states[si]])
(C/'shallow-exceptions.json').write_text(json.dumps(special),encoding='utf-8')
selected=[]
for state in sorted({v[3] for v in special}):
 group=[v for v in special if v[3]==state]; selected.extend(group[::max(1,len(group)//30)][:40])
j('evidence/shallow-exceptions.json',dict(observed_voxels=len(sub),protocol=obs['shallow_sampling'],type_counts=dict(Counter(v[3] for v in special)),stratified_exceptions=selected,complete_columns_geometry='settlement-geometry.json#/reserves',not_full_foundation_clearance=True))
obs['flagged_surface_type_counts']=dict(Counter(v[3] for v in obs.pop('flagged_surface')));obs['flag_classifier_note']='Whitelist exceptions are NOT automatically artificial: podzol/terracotta/flowers/pumpkins can be natural. Bee habitat and deep chest/spawner are separately preserved.'
obs['delta_interpretation']='Different explicit vegetation stripping can change exposed_y; this histogram is NOT all world changes. Earlier same-filter pass differed in only four columns, no author attribution.';obs['surface_height_delta_to_L1_cache']=dict(Counter(str(v) for v in rows[:,3]-old['height'][rows[:,1]-1453,rows[:,0]-89]));j('evidence/current-observation.json',obs)
np.savez_compressed(C/'city-map.npz',height=y,surface=surface,logs=logs,leaves=leaves,city=city,reserved=reserved,active=active,void=void,wet=wet,**quarters,**{k:a[k] for k in a.files if k.startswith('C')})
print(json.dumps({k:jj[k] for k in ['city_area','city_components','active_fabric_area']},ensure_ascii=False));print([(q['id'],q['area'],q['non_roof_reserve'],q['working_fabric_area']) for q in qstats]);print([(c['id'],c['area']) for c in critical])
