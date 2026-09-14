"""从已哈希核验的历史缓存重算事实；阈值仅装配模型搜索提案。

不访问Minecraft世界、不自动选择聚落、不把图成本当交通时间。
独立输出目录保留封存；所有业务代码属于任务外围复现脚本。
"""
from pathlib import Path
import numpy as np,json,heapq,hashlib,sqlite3
from collections import deque
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--raw-cache',required=True,type=Path);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
PLAN=Path(__file__).resolve().parents[1];R=PLAN.parents[3]
C=args.output;C.mkdir(parents=True,exist_ok=True);raw=args.raw_cache
if C.resolve()==PLAN.resolve():raise ValueError('Refuse overwrite primary directory')
for name,expected in [('observed.sqlite','01d115d6c686cc6d59772cfc68e1cbd50a5816045eeaa7f48fa8a4a8d4a791b7'),('derived.npz','575861ecd5b791ffd0e0c32614c5dc63de7563de477ee963994103f44024beff')]:
 with (raw/name).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==expected
territory_path=R/'research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json'
territory=json.loads(territory_path.read_text('utf-8-sig'));assert territory['revision']==154
# 全部政治成员来自冻结RLE；表层只读区域背景矩形的历史缓存。
d=np.load(raw/'derived.npz');shape=d['whole_group'].shape
all_t=np.full(shape,-1,np.int8)
for z,lo,hi,k in territory['runs']:
 assert np.all(all_t[z-1376,lo+800:hi+801]==-1)
 all_t[z-1376,lo+800:hi+801]=k
assert [int(np.sum(all_t==k)) for k in range(6)]==[92124,575397,391002,1198158,0,0]
all_y=np.full(shape,-32768,np.int16);all_st=np.zeros(shape,np.int16)
conn=sqlite3.connect((raw/'observed.sqlite').as_uri()+'?mode=ro',uri=True)
for z in range(1400,2441):
 rows=np.array(conn.execute('select x,exposed_y,exposed_state from samples where z=? and x between -400 and 1280 order by x',(z,)).fetchall())
 all_y[z-1376,rows[:,0]+800]=rows[:,1];all_st[z-1376,rows[:,0]+800]=rows[:,2]
conn.close()
a={'territory':all_t,'height':all_y,'surface':all_st,'terrain':d['terrain_class']}
np.savez_compressed(C/'context-map.npz',**a)
# 裁至整个正式中域包围框；计算只读历史缓存，非重新扫描存档。
x0,z0,x1,z1=89,1453,1188,2382
sl=np.s_[z0-1376:z1-1376+1,x0+800:x1+801]
t=a['territory'][sl];m=t==2;y=a['height'][sl];tc=a['terrain'][sl]
slope=d['slope8'][sl];relief=d['relief32'][sl];step=d['step1'][sl]
elig=m&(tc>0);seen=np.zeros(m.shape,bool);components=[]
for z,x in zip(*np.where(elig)):
 if seen[z,x]:continue
 q=deque([(z,x)]);seen[z,x]=1;cells=[]
 while q:
  zz,xx=q.popleft();cells.append((zz,xx))
  for dz,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
   nz,nx=zz+dz,xx+dx
   if 0<=nz<m.shape[0] and 0<=nx<m.shape[1] and elig[nz,nx] and not seen[nz,nx]:seen[nz,nx]=1;q.append((nz,nx))
 components.append(cells)
components.sort(key=len,reverse=True)
patch=np.zeros(m.shape,np.int16)
for i,cells in enumerate(components[:5],1):
 zz,xx=np.array(cells).T;patch[zz,xx]=i
zz,xx=np.indices(m.shape);wx,wz=xx+x0,zz+z0
searches={
 'S-W':m&(y<=90)&(wx<=580)&(wz<=1850),
 'S-U':m&(wx>=680)&(wz<=1840)&(y>=100)&(y<=175),
 'S-T':m&(wx>=380)&(wx<=580)&(wz>=1720)&(wz<=1880)&(y>=125),
 'S-V':m&(wx>=370)&(wx<=510)&(wz>=1950)&(wz<=2160)&(y>=95)&(y<=155)}
surface=a['surface'][sl]
db=sqlite3.connect((raw/'observed.sqlite').as_uri()+'?mode=ro',uri=True)
states={i:json.loads(v)['Name'] for i,v in db.execute('select * from states')};db.close()
summary=[]
for name,sm in searches.items():
 zz,xx=np.where(sm);ids,counts=np.unique(surface[sm],return_counts=True)
 summary.append(dict(id=name,area=int(sm.sum()),bounds=[int(xx.min()+x0),int(zz.min()+z0),int(xx.max()+x0),int(zz.max()+z0)],y_p10_p50_p90=np.percentile(y[sm],[10,50,90]).tolist(),flat=int(np.sum(sm&(tc==1))),gentle=int(np.sum(sm&(tc==2))),surface_top=sorted([(states[int(i)],int(n)) for i,n in zip(ids,counts)],key=lambda a:-a[1])[:6]))
# 跨界按所有四邻接共享边枚举；分组是比较责任，不挑一个固定山口。
full=a['territory'];fy=a['height'];edges=[]
for z,x in zip(*np.where(m)):
 for dz,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
  gz,gx=z+z0-1376+dz,x+x0+800+dx
  if full[gz,gx]==3:
   edges.append([int(x+x0),int(z+z0),int(gx-800),int(gz+1376),int(abs(int(y[z,x])-int(fy[gz,gx])))])
border=np.zeros(m.shape,bool)
for x,z,*_ in edges:border[z-z0,x-x0]=1
north=border&(wz<1850);south=border&(wz>=1850)
targets={'P2':patch==2,'P3':patch==3,'P4':patch==4,'E-N':north,'E-S':south,'X03':(wx==326)&(wz==2326)}
cost=1+2*np.where(np.isfinite(slope),slope,1)+relief/16+0.5*step
H,W=m.shape;fm=m.ravel();fc=cost.ravel();fy=y.ravel()
def paths(source,targets,weight):
 dist=np.full(H*W,np.inf);parent=np.full(H*W,-1,np.int32);q=[]
 for n in np.flatnonzero(source):dist[n]=0;heapq.heappush(q,(0.,int(n)))
 masks={k:v.ravel() for k,v in targets.items()};found={}
 while q and len(found)<len(masks):
  dv,n=heapq.heappop(q)
  if dv!=dist[n]:continue
  for name,mask in masks.items():
   if name not in found and mask[n]:found[name]=n
  z,x=divmod(n,W)
  for nxt in ([n-1] if x else [])+([n+1] if x<W-1 else [])+([n-W] if z else [])+([n+W] if z<H-1 else []):
   if not fm[nxt]:continue
   dh=int(fy[nxt])-int(fy[n]);nd=dv+(fc[n]+fc[nxt])/2+weight*dh*dh
   if nd<dist[nxt]:dist[nxt]=nd;parent[nxt]=n;heapq.heappush(q,(nd,nxt))
 result=[]
 for name,n in found.items():
  cells=[];end=n
  while n>=0:
   z,x=divmod(n,W);cells.append([int(x+x0),int(z+z0),int(fy[n])]);n=int(parent[n])
  cells.reverse();dy=np.diff([p[2] for p in cells]);result.append(dict(target=name,weight=weight,cost=float(dist[end]),length=len(cells)-1,ascent=int(dy[dy>0].sum()),descent=int(-dy[dy<0].sum()),max_step=int(np.abs(dy).max()) if len(dy) else 0,path=cells))
 return result
probes=[]
for weight in [4,16]:
 for source,label,ts in [(patch==1,'LOW',targets),(patch==2,'UPPER',{'E-N':north,'E-S':south}),(patch==4,'VALLEY',{'X03':targets['X03'],'E-S':south})]:
  for item in paths(source,ts,weight):item['source']=label;probes.append(item)
result=dict(bounds=[x0,z0,x1,z1],searches=summary,patches=[dict(id='PATCH-'+str(i),area=len(cells)) for i,cells in enumerate(components[:5],1)],boundary=dict(all_edges=len(edges),north_contact_columns=int(np.sum(north)),south_contact_columns=int(np.sum(south)),north_edges=sum(e[1]<1850 for e in edges),south_edges=sum(e[1]>=1850 for e in edges),edge_step_le1=sum(e[-1]<=1 for e in edges)),probes=probes,search_definition='S-W:Middle,Y<=90,X<=580,Z<=1850; S-U:Middle,X>=680,Z<=1840,100<=Y<=175; S-T:Middle,380<=X<=580,1720<=Z<=1880,Y>=125; S-V:Middle,370<=X<=510,1950<=Z<=2160,95<=Y<=155')
result['edge_witnesses']=edges
result['search_runs']={}
for name,sm in searches.items():
 runs=[]
 for z in range(H):
  padded=np.pad(sm[z].astype(np.int8),(1,1));edges2=np.diff(padded);starts=np.where(edges2==1)[0];ends=np.where(edges2==-1)[0]-1
  runs.extend([[int(z+z0),int(lo+x0),int(hi+x0)] for lo,hi in zip(starts,ends)])
 result['search_runs'][name]=runs
result['search_sensitivity']={}
for threshold in [80,90,100]: result['search_sensitivity']['west_height_'+str(threshold)]=int(np.sum(m&(y<=threshold)&(wx<=580)&(wz<=1850)))
for threshold in [670,680,690]: result['search_sensitivity']['upper_x_'+str(threshold)]=int(np.sum(m&(wx>=threshold)&(wz<=1840)&(y>=100)&(y<=175)))
(C/'regional-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
np.savez_compressed(C/'regional-map.npz',territory=t,height=y,terrain=tc,patch=patch,**searches)
print('Rebuilt cached regional facts and graph probes; world writes = 0')
