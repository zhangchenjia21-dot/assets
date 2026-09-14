import os
"""有界磁盘快照与只读解码。仅写任务缓存，绝不加载Minecraft或修改NBT。

NBT的4903填充long算法据World-Survey已验证算法独立实现；任务外围脚本无跨模块内部导入。
"""
from pathlib import Path
import sys,ctypes,hashlib,json,io,zlib,gzip,shutil
from datetime import datetime,timezone
from collections import Counter
import numpy as np
sys.path.insert(0,str(Path(os.environ['MID_A_CACHE'])/'deps'));import nbtlib
C=Path(os.environ['MID_A_CACHE']);world=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师')
assert world.resolve() not in C.resolve().parents
if not (C/'current-observation.json').exists() and '--capture' not in sys.argv:raise ValueError('Snapshot missing: reproduction refuses fresh capture without explicit --capture')
old=np.load(Path(os.environ['MID_A_L1_CACHE'])/'regional-map.npz');z,x=np.indices(old['height'].shape);x+=89;z+=1453
# 三个候选只由接受的S-W地形与门户/内部交换需求提出，非旧城镇轮廓。
defs={'C1_GATEWAY':(270,1640,1845),'C2_LINKED_CORE':(365,1640,1845),'C3_NORTH_CORE':(420,1570,1845)}
candidates={n:old['S-W']&(x<=xm)&(z>=zmin)&(z<=zmax)&(old['height']<=75) for n,(xm,zmin,zmax) in defs.items()}
union=np.logical_or.reduce(list(candidates.values()));mask=union.copy()
for dz in range(-8,9):
 for dx in range(-8,9):
  if abs(dx)+abs(dz)<=8:
   srcz=slice(max(0,-dz),min(mask.shape[0],mask.shape[0]-dz));srcx=slice(max(0,-dx),min(mask.shape[1],mask.shape[1]-dx))
   dstz=slice(max(0,dz),min(mask.shape[0],mask.shape[0]+dz));dstx=slice(max(0,dx),min(mask.shape[1],mask.shape[1]+dx));mask[dstz,dstx]|=union[srcz,srcx]
points=[(int(xx),int(zz)) for zz,xx in zip(z[mask],x[mask])];chunks=sorted({(xx//16,zz//16) for xx,zz in points})
dim=world/'dimensions/minecraft/overworld';regions={(cx//32,cz//32) for cx,cz in chunks}
files=[world/'level.dat',world/'session.lock'];absent=[]
for rx,rz in sorted(regions):
 for folder in ['region','entities','poi']:
  p=dim/folder/f'r.{rx}.{rz}.mca'
  if p.exists():files.append(p)
  else:absent.append(p.relative_to(world).as_posix())
if (C/'current-observation.json').exists():
 # 重放的缺失容器与文件清单绑定旧epoch，不受今天源目录增删影响。
 prior_manifest=json.loads((C/'current-observation.json').read_text('utf-8'))
 files=[world/name for name in prior_manifest['before']];absent=prior_manifest['absent_containers']
api=ctypes.WinDLL('kernel32',use_last_error=True);api.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p];api.CreateFileW.restype=ctypes.c_void_p;api.CloseHandle.argtypes=[ctypes.c_void_p]
stamp=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(p):return dict(sha256=sha(p),size=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns)
snap=C/'snapshot';replay=(C/'current-observation.json').exists()
if replay:
 prior=json.loads((C/'current-observation.json').read_text('utf-8'));before=prior['before'];after=prior['after'];start=prior['snapshot_start_utc'];end=prior['snapshot_end_utc']
 for name,value in before.items():assert sha(snap/name)==value['sha256']
else:
 assert not snap.exists(),'Do not overwrite snapshot';snap.mkdir();handles=[];start=stamp()
 try:
  for p in files:
   h=api.CreateFileW(str(p),0x80000000,1,None,3,0,None)
   if h==ctypes.c_void_p(-1).value:raise OSError(ctypes.get_last_error(),'Read share lock failed '+str(p))
   handles.append(h)
  before={p.relative_to(world).as_posix():fingerprint(p) for p in files}
  for p in files:
   q=snap/p.relative_to(world);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(q)==before[p.relative_to(world).as_posix()]['sha256']
  after={p.relative_to(world).as_posix():fingerprint(p) for p in files};assert before==after
  assert not any((world/p).exists() for p in absent)
 finally:
  for h in handles:api.CloseHandle(h)
 end=stamp()
identity=nbtlib.load(snap/'level.dat')['Data'];assert str(identity['LevelName'])=='建筑师' and int(identity['DataVersion'])==4903
def packed(arr,i,bits):return (int(arr[i//(64//bits)])&((1<<64)-1))>>((i%(64//bits))*bits)&((1<<bits)-1)
def loadchunk(folder,cx,cz):
 path=snap/'dimensions/minecraft/overworld'/folder/f'r.{cx//32}.{cz//32}.mca'
 if not path.exists():return None
 with path.open('rb') as f:
  f.seek(((cz%32)*32+cx%32)*4);loc=int.from_bytes(f.read(4),'big')
  if not loc:return None
  f.seek((loc>>8)*4096);length=int.from_bytes(f.read(4),'big');kind=f.read(1)[0];b=f.read(length-1)
 if kind&128:raise ValueError('External chunk requires separately locked snapshot; stop')
 if kind==2:b=zlib.decompress(b)
 elif kind==1:b=gzip.decompress(b)
 elif kind!=3:raise ValueError('Unsupported compression')
 return nbtlib.File.parse(io.BytesIO(b))
def expand(cont,n,minimum):
 pal=cont['palette'];bits=max(minimum,(len(pal)-1).bit_length())
 return np.zeros(n,np.int16) if len(pal)==1 else np.array([packed(cont['data'],i,bits) for i in range(n)],np.int16)
air={'minecraft:air','minecraft:cave_air','minecraft:void_air'}
plant=lambda s:any(v in s for v in ['leaves','_log','_wood','flower','fern','vine','moss_carpet','grass','sapling','bush']) and s not in ['minecraft:grass_block'] or s in {'minecraft:snow','minecraft:poppy','minecraft:dandelion','minecraft:oxeye_daisy','minecraft:azure_bluet','minecraft:sugar_cane','minecraft:glow_lichen'}
natural={'air','cave_air','void_air','stone','dirt','grass_block','coarse_dirt','rooted_dirt','sand','red_sand','sandstone','red_sandstone','gravel','clay','granite','diorite','andesite','tuff','calcite','deepslate','bedrock','water','lava','packed_mud','mud','moss_block','snow','snow_block'}
state_list=[];state_index={}
def sid(s):
 if s not in state_index:state_index[s]=len(state_list);state_list.append(s)
 return state_index[s]
rows=[];sub=[];flags=[];blockents=[];entities=[];pois=[];verify=[];bychunk={k:[] for k in chunks}
for xx,zz in points:bychunk[(xx//16,zz//16)].append((xx,zz))
for ix,(cx,cz) in enumerate(chunks):
 d=loadchunk('region',cx,cz);assert d is not None and int(d['DataVersion'])==4903 and (int(d['xPos']),int(d['zPos']))==(cx,cz)
 sections={int(s['Y']):s for s in d['sections']};decoded={sy:(expand(s['block_states'],4096,4),[str(v['Name']) for v in s['block_states']['palette']]) for sy,s in sections.items() if 'block_states' in s}
 def block(xx,yy,zz):
  if yy//16 not in decoded:return 'minecraft:air'
  arr,pal=decoded[yy//16];return pal[int(arr[(yy%16)*256+(zz%16)*16+xx%16])]
 low=int(d['yPos'])*16;high=(max(sections)+1)*16;bits=(high-low).bit_length();hm=d['Heightmaps']['WORLD_SURFACE']
 for xx,zz in bychunk[(cx,cz)]:
  top=packed(hm,(zz%16)*16+xx%16,bits)+low-1;gy=top;logs=leaves=0
  while gy>=low:
   s=block(xx,gy,zz)
   if s not in air and not plant(s):break
   logs+=int('_log' in s or '_wood' in s);leaves+=int('leaves' in s);gy-=1
  ground=block(xx,gy,zz);rows.append([xx,zz,top,gy,sid(ground),logs,leaves])
  # 固定8格格点浅层探查 + 所有异常地表；不是完整基础清障证明。
  suspect=ground.split(':')[-1] not in natural and '_ore' not in ground and not plant(ground)
  if suspect:flags.append([xx,gy,zz,ground])
  if candidates['C2_LINKED_CORE'][zz-1453,xx-89] or (xx%8==0 and zz%8==0) or suspect:
   for yy in range(gy-12,gy+1):sub.append([xx,yy,zz,sid(block(xx,yy,zz))])
  if xx%32==0 and zz%32==0:
   actual=high-1
   while block(xx,actual,zz) in air and actual>=low:actual-=1
   assert actual==top;verify.append([xx,zz,top,actual])
 for v in d.get('block_entities',[]):
  xx,zz=int(v['x']),int(v['z'])
  if (xx,zz) in bychunk[(cx,cz)]:blockents.append(dict(x=xx,y=int(v['y']),z=zz,id=str(v['id'])))
 en=loadchunk('entities',cx,cz)
 if en:
  for v in en.get('Entities',[]):entities.append(dict(id=str(v['id']),pos=[float(q) for q in v['Pos']]))
 po=loadchunk('poi',cx,cz)
 if po:
  for sy,s in po.get('Sections',{}).items():
   for v in s.get('Records',[]):pois.append(dict(section=str(sy),type=str(v['type']),pos=[int(q) for q in v['pos']]))
 if ix%30==0:print('decoded',ix,'/',len(chunks),flush=True)
np.savez_compressed(C/'current.npz',rows=np.array(rows,np.int32),sub=np.array(sub,np.int32),**candidates)
result=dict(schema='bounded-current-observation/1',snapshot_start_utc=start,snapshot_end_utc=end,world=str(world),identity=dict(LevelName=str(identity['LevelName']),DataVersion=int(identity['DataVersion'])),before=before,after=after,absent_containers=absent,source_bytes_unchanged=True,world_writes=0,world_loads=0,broad_rescan=False,candidate_definitions=defs,candidate_source='Accepted L1 S-W; cached Y<=75; candidate cutoffs are planning hypotheses, not natural/legal boundaries',surface_columns=len(rows),selected_chunks=len(chunks),shallow_voxels=len(sub),shallow_sampling='All C2 columns ground through ground-12; elsewhere 8-grid plus flagged surface columns; same immutable snapshot',heightmap_independent_checks=len(verify),states=state_list,flagged_surface=flags,block_entities=blockents,entities_in_selected_chunks=entities,poi_in_selected_chunks=pois,limits=['Natural-looking player blocks cannot be identified by material','No deep underground or complete hydrology/groundwater verification','Entities refer to snapshot time','Snapshot file containers include unused chunk context; only selected columns decoded','Snapshot copy Local-only'])
(C/'current-observation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('COMPLETE',len(rows),len(sub),len(flags),flush=True)
