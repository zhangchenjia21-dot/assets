"""只有 rb 文件读取；Windows 共享模式在调查期间拒绝已有文件写入与删除。"""
import ctypes
import hashlib
import io
import json
import struct
import zlib
import gzip
from pathlib import Path
import nbtlib
from L0_公理层.地理契约 import packed, palette_value, AIR, WATER

class ReadGuard:
    def __init__(self, world):
        self.world = world
        self.handles = []
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateFileW.argtypes = [ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
        self.api.CreateFileW.restype = ctypes.c_void_p
        self.api.CloseHandle.argtypes = [ctypes.c_void_p]
    def __enter__(self):
        try:
            for p in sorted(self.world.rglob('*')):
                if p.is_file():
                    h = self.api.CreateFileW(str(p),0x80000000,1,None,3,0,None)
                    if h == ctypes.c_void_p(-1).value:
                        raise OSError(ctypes.get_last_error(), '无法取得只读共享句柄: '+str(p))
                    self.handles.append(h)
            return self
        except BaseException:
            self.__exit__(None,None,None)
            raise
    def __exit__(self,*args):
        for h in self.handles:
            self.api.CloseHandle(h)
        self.handles.clear()

def fingerprint(world):
    result = {}
    for p in sorted(world.rglob('*')):
        if p.is_file():
            with p.open('rb') as f:
                digest = hashlib.file_digest(f,'sha256').hexdigest()
            s = p.stat()
            result[p.relative_to(world).as_posix()] = {'size':s.st_size,'mtime_ns':s.st_mtime_ns,'sha256':digest}
    return result

def header(path):
    with path.open('rb') as f:
        raw = f.read(8192)
    # Chunky 边缘存在零字节占位；没有 location table 就不算生成区块。
    if not raw:
        return []
    if len(raw) != 8192:
        raise ValueError('region header truncated: '+str(path))
    rx,rz = map(int,path.stem.split('.')[1:])
    rows=[]
    for i in range(1024):
        loc = int.from_bytes(raw[i*4:i*4+4],'big')
        if loc:
            rows.append((rx*32+i%32,rz*32+i//32,loc>>8,loc&255,int.from_bytes(raw[4096+i*4:4100+i*4],'big')))
    return rows

def chunk(path, sector, cx, cz):
    with path.open('rb') as f:
        f.seek(sector*4096)
        count = int.from_bytes(f.read(4),'big')
        compression = f.read(1)[0]
        payload = f.read(count-1)
    if compression & 128:
        payload = (path.parent / f'c.{cx}.{cz}.mcc').read_bytes()
    kind = compression & 127
    if kind == 1:
        payload = gzip.decompress(payload)
    elif kind == 2:
        payload = zlib.decompress(payload)
    elif kind != 3:
        raise ValueError(f'unsupported compression {kind}')
    d = nbtlib.File.parse(io.BytesIO(payload))
    if int(d['DataVersion']) != 4903:
        raise ValueError('当前解码器仅验证 DataVersion 4903')
    if (int(d['xPos']),int(d['zPos'])) != (cx,cz):
        raise ValueError('chunk position mismatch')
    return d

def block(sections,x,y,z):
    s = sections.get(y//16)
    if s is None or 'block_states' not in s:
        return 'minecraft:air'
    return str(palette_value(s['block_states'],(y%16)*256+z*16+x,4)['Name'])

def columns(d, points=((8,8),(2,2),(14,2),(2,14),(14,14))):
    sections = {int(s['Y']):s for s in d['sections']}
    low = int(d['yPos'])*16
    high = (max(sections)+1)*16
    bits = (high-low).bit_length()
    hm = d['Heightmaps']
    if len(hm['WORLD_SURFACE']) != (256+(64//bits)-1)//(64//bits):
        raise ValueError('heightmap geometry mismatch')
    out=[]
    for x,z in points:
        y = packed(hm['WORLD_SURFACE'],z*16+x,bits)+low-1
        floor = packed(hm['OCEAN_FLOOR'],z*16+x,bits)+low-1
        motion = packed(hm['MOTION_BLOCKING_NO_LEAVES'],z*16+x,bits)+low-1
        top=block(sections,x,y,z)
        # WORLD_SURFACE 可包含树冠；独立下探只剥离显式植被，不假装能够识别所有人工建筑。
        ground=y
        while ground>=low:
            b=block(sections,x,ground,z)
            if b not in AIR and not any(t in b for t in ('leaves','_log','_wood','fern','flower','vine','moss_carpet')) and b not in ('minecraft:short_grass','minecraft:tall_grass','minecraft:short_dry_grass','minecraft:tall_dry_grass','minecraft:snow'):
                break
            ground-=1
        b=block(sections,x,ground,z)
        biome_y = max(low,min(high-1,y))
        sec=sections[biome_y//16]
        biome=str(palette_value(sec['biomes'],((biome_y%16)//4)*16+(z//4)*4+x//4,1))
        out.append({'x':int(d['xPos'])*16+x,'z':int(d['zPos'])*16+z,'surface_y':y,'ocean_floor_y':floor,'motion_no_leaves_y':motion,'exposed_y':ground,'surface_block':top,'exposed_block':b,'biome':biome,'water':int(b in WATER),'water_y':ground if b in WATER else None,'height_bits':bits,'min_y':low,'max_y':high-1})
    return out

def verify_column(d,sample):
    """验证不读取 heightmap：从最高 section 向下逐块寻找最高非空气。"""
    ss={int(s['Y']):s for s in d['sections']}
    x,z=sample['x']%16,sample['z']%16
    y=sample['max_y']
    while y>=sample['min_y'] and block(ss,x,y,z) in AIR:
        y-=1
    section=ss[y//16]
    # 独立展开 biome 的 packed longs，避免复用随机索引函数。
    cont=section['biomes']; pal=cont['palette']
    if len(pal)==1:
        bio=str(pal[0])
    else:
        bits=max(1,(len(pal)-1).bit_length()); expanded=[]
        for word in cont['data']:
            unsigned=int(word)&((1<<64)-1)
            expanded.extend((unsigned>>(j*bits))&((1<<bits)-1) for j in range(64//bits))
        bio=str(pal[expanded[((y%16)//4)*16+(z//4)*4+x//4]])
    # 原始 block palette 名称证明水体；不是 river biome 代理。
    exposed=block(ss,x,sample['exposed_y'],z)
    return {'x':sample['x'],'z':sample['z'],'height_expected':sample['surface_y'],'height_vertical_scan':y,'biome_expected':sample['biome'],'biome_expanded':bio,'water_block':exposed,'pass':y==sample['surface_y'] and bio==sample['biome'] and int(exposed in WATER)==sample['water']}
