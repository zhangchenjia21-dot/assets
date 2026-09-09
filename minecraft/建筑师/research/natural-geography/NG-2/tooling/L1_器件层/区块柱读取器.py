"""按实际 4903 palette 解码真实柱；使用 numpy 批量解包而非高度插值。"""
import gzip
import io
import json
import zlib
from collections import OrderedDict
import numpy as np
import nbtlib
from L0_公理层.精查契约 import AIR,WATER,ICE,vegetation,artificial

def unpack(words,bits,count):
    if words is None:return np.zeros(count,dtype=np.int32)
    values=np.asarray(words,dtype=np.int64).view(np.uint64)
    i=np.arange(count,dtype=np.uint64);per=64//bits
    return ((values[i//per]>>((i%per)*np.uint64(bits)))&np.uint64((1<<bits)-1)).astype(np.int32)

class Reader:
    def __init__(self,world,db):
        self.world=world;self.db=db;self.cache=OrderedDict();self.states={};self.state_values=[];self.biomes={};self.biome_values=[]
        self.headers={};self.decoded=0
        for sid,raw in db.execute('SELECT id,json FROM states ORDER BY id'):
            self.states[raw]=sid;self.state_values.append(json.loads(raw))
        for bid,name in db.execute('SELECT id,name FROM biomes ORDER BY id'):
            self.biomes[name]=bid;self.biome_values.append(name)
    def state_id(self,state):
        obj={'Name':str(state['Name'])}
        if 'Properties' in state:obj['Properties']={str(k):str(v) for k,v in state['Properties'].items()}
        raw=json.dumps(obj,sort_keys=True,separators=(',',':'))
        if raw not in self.states:
            sid=len(self.state_values);self.states[raw]=sid;self.state_values.append(obj);self.db.execute('INSERT INTO states VALUES (?,?)',(sid,raw))
        return self.states[raw]
    def biome_id(self,name):
        name=str(name)
        if name not in self.biomes:
            self.biomes[name]=len(self.biome_values);self.biome_values.append(name);self.db.execute('INSERT INTO biomes VALUES (?,?)',(self.biomes[name],name))
        return self.biomes[name]
    def raw(self,cx,cz):
        path=self.world/'dimensions/minecraft/overworld/region'/f'r.{cx//32}.{cz//32}.mca'
        if path not in self.headers:
            with path.open('rb') as f:self.headers[path]=f.read(8192)
        i=(cz%32)*32+cx%32;loc=int.from_bytes(self.headers[path][4*i:4*i+4],'big')
        if not loc:raise ValueError(f'缺失区块 {cx},{cz}')
        with path.open('rb') as f:
            f.seek((loc>>8)*4096);n=int.from_bytes(f.read(4),'big');c=f.read(1)[0];raw=f.read(n-1)
        if c&128:raw=(path.parent/f'c.{cx}.{cz}.mcc').read_bytes()
        if c&127==2:raw=zlib.decompress(raw)
        elif c&127==1:raw=gzip.decompress(raw)
        elif c&127!=3:raise ValueError('未支持的压缩类型')
        d=nbtlib.File.parse(io.BytesIO(raw))
        if int(d['DataVersion'])!=4903 or str(d['Status'])!='minecraft:full' or (int(d['xPos']),int(d['zPos']))!=(cx,cz):raise ValueError('区块版本/状态/坐标不满足只读调查前提')
        return d,path,loc>>8
    def read(self,cx,cz):
        key=(cx,cz)
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        d,path,sector=self.raw(cx,cz);self.decoded+=1
        sections={int(s['Y']):s for s in d['sections']};low=int(d['yPos'])*16;high=(max(sections)+1)*16;bits=(high-low).bit_length()
        hm=d['Heightmaps']['WORLD_SURFACE']
        if len(hm)!=(256+64//bits-1)//(64//bits):raise ValueError('heightmap位数不符')
        sy=unpack(hm,bits,256)+low-1;floor=unpack(d['Heightmaps']['OCEAN_FLOOR'],bits,256)+low-1
        xs=np.arange(256)%16;zs=np.arange(256)//16;arrays={};biomearrays={}
        air=self.state_id({'Name':'minecraft:air'})
        def states_at(ys,active=None,previous=None):
            active=np.ones(256,dtype=bool) if active is None else active
            values=np.full(256,air,dtype=np.int32) if previous is None else previous.copy()
            values[active]=air
            for sec in np.unique((ys//16)[active]):
                select=(ys//16==sec)&active;s=sections.get(int(sec))
                if s is None or 'block_states' not in s:continue
                if sec not in arrays:
                    p=s['block_states'];pal=np.array([self.state_id(v) for v in p['palette']],dtype=np.int32)
                    arrays[sec]=pal[unpack(p.get('data'),max(4,(len(pal)-1).bit_length()),4096)]
                indices=(ys[select]%16)*256+zs[select]*16+xs[select];values[select]=arrays[sec][indices]
            return values
        top=states_at(sy);gy=sy.copy();support=top.copy()
        while True:
            names=[self.state_values[s]['Name'] for s in support];mask=np.array([vegetation(n) for n in names])&(gy>=low)
            if not mask.any():break
            gy[mask]-=1;support=states_at(gy,mask,support)
        names=[self.state_values[s]['Name'] for s in support]
        wy=gy.copy();ws=support.copy();covered=np.array([n in ICE for n in names])
        # 冰盖下的水必须实际读取。整块蓝冰/浮冰底下无水时不伪装成水面。
        probing=covered.copy()
        while probing.any():
            wy[probing]-=1;ws=states_at(wy,probing,ws)
            probing=covered & np.array([self.state_values[s]['Name'] in ICE for s in ws]) & (wy>=low)
        wet=np.array([self.state_values[s]['Name'] in WATER for s in ws]);wy[~wet]=-32768
        bottom=np.where(wet,wy,gy).copy();bed=bottom.copy();bs=ws.copy()
        active=wet.copy()
        while active.any():
            bed[active]-=1;bs=states_at(bed,active,bs)
            active=wet & np.array([self.state_values[s]['Name'] in WATER for s in bs]) & (bed>=low)
        bottom=np.where(wet,bed+1,-32768)
        biome=np.zeros(256,dtype=np.int32)
        for sec in np.unique(sy//16):
            select=sy//16==sec;p=sections[int(sec)]['biomes'];pal=np.array([self.biome_id(v) for v in p['palette']])
            values=pal[unpack(p.get('data'),max(1,(len(pal)-1).bit_length()),64)]
            indices=((sy[select]%16)//4)*16+(zs[select]//4)*4+xs[select]//4;biome[select]=values[indices]
        suspicious=np.array([artificial(self.state_values[int(a)]['Name']) or artificial(self.state_values[int(b)]['Name']) for a,b in zip(top,support)],dtype=np.int32)
        # 一行对应真实整数柱；water_y/bottom 哨兵 -32768 表示无已观测表层水区间。
        rows=np.column_stack((xs+cx*16,zs+cz*16,sy,gy,floor,wy,bottom,top,support,np.where(wet,ws,air),biome,covered.astype(int)&wet,suspicious)).astype(np.int32)
        entities=[{'id':str(e.get('id','unknown')),'x':int(e.get('x',0)),'y':int(e.get('y',0)),'z':int(e.get('z',0))} for e in d.get('block_entities',[])]
        self.db.execute('INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?,?,?)',(cx,cz,path.relative_to(self.world).as_posix(),sector,4903,'minecraft:full',json.dumps(entities)))
        self.cache[key]=rows
        if len(self.cache)>128:self.cache.popitem(last=False)
        return rows

def connect(path):
    import sqlite3
    db=sqlite3.connect(path)
    db.executescript('''
    PRAGMA user_version=1;
    CREATE TABLE IF NOT EXISTS states(id INTEGER PRIMARY KEY,json TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS biomes(id INTEGER PRIMARY KEY,name TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS chunks(cx INTEGER,cz INTEGER,region TEXT,sector INTEGER,data_version INTEGER,status TEXT,block_entities TEXT,PRIMARY KEY(cx,cz));
    CREATE TABLE IF NOT EXISTS samples(x INTEGER,z INTEGER,surface_y INTEGER,exposed_y INTEGER,ocean_floor_y INTEGER,water_y INTEGER,water_bottom INTEGER,surface_state INTEGER,exposed_state INTEGER,water_state INTEGER,biome INTEGER,ice_covered INTEGER,artificial_material INTEGER,PRIMARY KEY(x,z));
    CREATE TABLE IF NOT EXISTS target_samples(target TEXT,x INTEGER,z INTEGER,stage TEXT,PRIMARY KEY(target,x,z));
    CREATE TABLE IF NOT EXISTS targets(id TEXT PRIMARY KEY,json TEXT);
    CREATE TABLE IF NOT EXISTS assessments(target TEXT PRIMARY KEY,json TEXT);
    CREATE TABLE IF NOT EXISTS profiles(target TEXT,name TEXT,x INTEGER,z INTEGER,distance REAL,elevation INTEGER,water_y INTEGER,PRIMARY KEY(target,name,x,z));
    CREATE INDEX IF NOT EXISTS target_sample_lookup ON target_samples(target);
    ''')
    return db
