"""只读捕获当前存档局部快照，再离线查询；无 Minecraft 加载、保存或写入接口。

NBT 4903 的 padded-long/palette 解码沿用已验证 V1 算法，本文件不导入其内部层。
完整 region 与逐列结果只写工程 Local Cache，Git 仅接收摘要和空间见证。
"""
import sys, json, gzip, zlib, io, hashlib, ctypes
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import numpy as np
sys.path.insert(0,'D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
import nbtlib

OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[3]
PLAN=ROOT/'planning/CIV-001/MIDDLE/MD-001P'
CACHE=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001S1')
WORLD=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师')
X0,Z0,W,H=80,1620,241,231
AIR={'minecraft:air','minecraft:cave_air','minecraft:void_air'}
WATER={'minecraft:water','minecraft:kelp','minecraft:kelp_plant','minecraft:seagrass','minecraft:tall_seagrass','minecraft:bubble_column'}
PLANTS={'minecraft:short_grass','minecraft:tall_grass','minecraft:short_dry_grass','minecraft:tall_dry_grass','minecraft:snow','minecraft:dead_bush','minecraft:sugar_cane','minecraft:bamboo','minecraft:cactus','minecraft:leaf_litter','minecraft:pink_petals','minecraft:lily_pad'}
def vegetation(n):return n in AIR|PLANTS or any(t in n for t in ('leaves','_log','_wood','fern','flower','vine','moss_carpet','sapling','azalea','mushroom','_roots'))
def artificial(n):return any(t in n for t in ('_planks','_stairs','_slab','_bricks','_door','_fence','glass','concrete','rail','torch','_sign','_carpet','redstone')) or n in {'minecraft:farmland','minecraft:dirt_path','minecraft:chest','minecraft:crafting_table','minecraft:barrel','minecraft:ladder','minecraft:lantern','minecraft:stone_bricks'}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def mask(runs):
    a=np.zeros((H,W),bool)
    for z,l,r in runs:
        if Z0<=z<Z0+H and l<X0+W and r>=X0:a[z-Z0,max(l-X0,0):min(r-X0+1,W)]=True
    return a
def rle(a):
    rows=[]
    for z,row in enumerate(a):
        cuts=np.r_[0,np.where(row[1:]!=row[:-1])[0]+1,W]
        for l,r in zip(cuts[:-1],cuts[1:]):
            if row[l]:rows.append([z+Z0,int(l)+X0,int(r)+X0-1])
    return rows
def dilate(a,n):
    a=a.copy()
    for _ in range(n):
        b=a.copy();a[1:]|=b[:-1];a[:-1]|=b[1:];a[:,1:]|=b[:,:-1];a[:,:-1]|=b[:,1:]
    return a
def packed(data,index,bits):return (int(data[index//(64//bits)])&((1<<64)-1))>>((index%(64//bits))*bits)&((1<<bits)-1)

class Reader:
    """只打开本地已捕获文件 rb；缺失/非完整/版本不符区块即失败，不以空气补齐。"""
    def __init__(self):self.chunks={};self.arrays={};self.files={};self.blocks=Counter()
    def chunk(self,cx,cz,kind='region'):
        key=(kind,cx,cz)
        if key in self.chunks:return self.chunks[key]
        name=f'{kind}-r.{cx//32}.{cz//32}.mca';path=CACHE/'snapshot'/name
        if not path.exists():
            if kind!='region':return None
            raise FileNotFoundError(name)
        if name not in self.files:self.files[name]=path.read_bytes()
        data=self.files[name];index=(cx%32)+(cz%32)*32
        location=int.from_bytes(data[index*4:index*4+4],'big');sector=location>>8
        if sector==0:
            if kind!='region':return None
            raise ValueError(f'missing chunk {cx},{cz}')
        pos=sector*4096;length=int.from_bytes(data[pos:pos+4],'big');compression=data[pos+4]
        payload=data[pos+5:pos+4+length]
        if compression&128:raise ValueError('external chunk requires explicit snapshot extension')
        if compression==2:payload=zlib.decompress(payload)
        elif compression==1:payload=gzip.decompress(payload)
        elif compression!=3:raise ValueError(f'unsupported compression {compression}')
        d=nbtlib.File.parse(io.BytesIO(payload));assert int(d['DataVersion'])==4903
        if kind=='region':
            assert (int(d['xPos']),int(d['zPos']))==(cx,cz) and str(d['Status'])=='minecraft:full'
        self.chunks[key]=d;return d
    def block(self,x,y,z):
        cx,cz=x//16,z//16;d=self.chunk(cx,cz);key=(cx,cz,y//16)
        if key not in self.arrays:
            section=next((s for s in d['sections'] if int(s['Y'])==y//16),None)
            if section is None or 'block_states' not in section:self.arrays[key]=(['minecraft:air'],None)
            else:
                b=section['block_states'];names=[str(s['Name']) for s in b['palette']]
                ids=np.zeros(4096,np.uint16) if len(names)==1 else np.array([packed(b['data'],i,max(4,(len(names)-1).bit_length())) for i in range(4096)],np.uint16)
                self.arrays[key]=(names,ids)
        names,ids=self.arrays[key];i=(y%16)*256+(z%16)*16+x%16
        return names[0] if ids is None else names[int(ids[i])]
    def surface(self,x,z):
        d=self.chunk(x//16,z//16);sections=d['sections'];low=int(d['yPos'])*16;high=(max(int(s['Y']) for s in sections)+1)*16
        bits=(high-low).bit_length();hm=d['Heightmaps']['WORLD_SURFACE'];assert len(hm)==(256+(64//bits)-1)//(64//bits)
        sy=packed(hm,(z%16)*16+x%16,bits)+low-1;gy=sy
        above=[]
        while gy>=low and vegetation(self.block(x,gy,z)):
            above.append([gy,self.block(x,gy,z)]);gy-=1
        return {'x':x,'z':z,'surface_y':sy,'ground_y':gy,'ground':self.block(x,gy,z),'top':self.block(x,sy,z),'above':above}

def capture():
    CACHE.mkdir(exist_ok=True);snapshot=CACHE/'snapshot'
    if snapshot.exists():raise FileExistsError('已有快照不得静默覆盖；复现应使用 surface 模式')
    g=mask(next(n for n in read(PLAN/'settlement-nodes.json')['nodes'] if n['id']=='G1')['envelope'])
    path=np.zeros(g.shape,bool)
    for rt in read(PLAN/'movement-network.json')['routes'][:2]:
        for x,z,_ in rt['path']:path[z-Z0,x-X0]=True
    scope=dilate(g,8)|dilate(path,2)
    chunks=sorted({((int(x)+X0)//16,(int(z)+Z0)//16) for z,x in zip(*np.where(scope))})
    regions=sorted({(cx//32,cz//32) for cx,cz in chunks})
    targets=[WORLD/'level.dat',WORLD/'session.lock']
    for kind in ('region','entities','poi'):
        for rx,rz in regions:
            p=WORLD/f'dimensions/minecraft/overworld/{kind}/r.{rx}.{rz}.mca'
            if p.exists():targets.append(p)
    api=ctypes.WinDLL('kernel32',use_last_error=True);api.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p];api.CreateFileW.restype=ctypes.c_void_p;api.CloseHandle.argtypes=[ctypes.c_void_p]
    handles=[];start=utc()
    try:
        for p in targets:
            h=api.CreateFileW(str(p),0x80000000,1,None,3,0,None)
            if h==ctypes.c_void_p(-1).value:raise OSError(ctypes.get_last_error(),'当前存档未能取得拒绝写入的只读共享句柄；须关闭存档后重试')
            handles.append(h)
        d=nbtlib.load(WORLD/'level.dat')['Data']
        if str(d['LevelName'])!='建筑师' or int(d['DataVersion'])!=4903:raise ValueError('CURRENT_WORLD_IDENTITY_NOT_CONFIRMED')
        snapshot.mkdir();records=[]
        for p in targets:
            data=p.read_bytes();name=p.name if p.parent==WORLD else p.parent.name+'-'+p.name
            (snapshot/name).write_bytes(data);st=p.stat();records.append({'world_relative':p.relative_to(WORLD).as_posix(),'snapshot_name':name,'size':len(data),'mtime_ns':st.st_mtime_ns,'sha256':hashlib.sha256(data).hexdigest()})
        assert all(sha(WORLD/r['world_relative'])==r['sha256'] for r in records)
        audit={'status':'CURRENT_WORLD_IDENTITY_CONFIRMED','world_name':str(d['LevelName']),'world_path':str(WORLD),'data_version':int(d['DataVersion']),'game_version':str(d['Version']['Name']),'last_played_epoch_ms':int(d['LastPlayed']),'singleplayer_uuid':[int(v) for v in d['singleplayer_uuid']],'identity_basis':'exact established survey path + current level.dat LevelName/version + current source hashes','read_started_at':start,'snapshot_finished_at':utc(),'snapshot_files':records,'scope_columns':int(scope.sum()),'scope_geometry':rle(scope),'scope_reason':'G1 envelope + eight-column local buffer; old R1 chain two-column transit context only','selected_chunks':chunks,'world_writes':0,'broad_rescan':0,'guard':'GENERIC_READ / FILE_SHARE_READ denies write/delete on identity, session.lock and selected containers during capture','limitations':['Save-level disk snapshot, not in-game screenshot','No Minecraft runtime launched; raw region is local-only']}
        write(OUT/'current-world-audit.json',audit);write(CACHE/'capture.json',audit)
    finally:
        for h in handles:api.CloseHandle(h)
    print('captured current world',len(chunks),'chunks',int(scope.sum()),'columns',flush=True)

def surface():
    audit=read(CACHE/'capture.json')
    for r in audit['snapshot_files']:assert sha(CACHE/'snapshot'/r['snapshot_name'])==r['sha256']
    r=Reader();scope=mask(audit['scope_geometry']);rows=[]
    for z,x in zip(*np.where(scope)):rows.append(r.surface(int(x)+X0,int(z)+Z0))
    with gzip.open(CACHE/'surface.json.gz','wt',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False,separators=(',',':'))
    write(CACHE/'surface-summary.json',{'columns':len(rows),'materials':dict(Counter(p['ground'] for p in rows)),'elevation':[min(p['ground_y'] for p in rows),max(p['ground_y'] for p in rows)],'decoded_chunks':len(r.chunks)})
    print(read(CACHE/'surface-summary.json'),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='capture':capture();surface()
    elif sys.argv[1]=='surface':surface()
    else:raise ValueError('expected capture or surface')
