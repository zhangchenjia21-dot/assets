"""独立标量NBT读取，与生产numpy palette解包/高度过滤交叉核验；不写世界。"""
import gzip,io,json,sqlite3,sys,zlib
from pathlib import Path
from contextlib import ExitStack
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tooling'));sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
import nbtlib
from L0_公理层.区域契约 import BOUNDS,AIR,WATER,ICE,PLANTS
from L1_器件层.源快照保护器 import ReadGuard,write_json

def value(data,bits,i):
    if data is None:return 0
    return (int(data[i//(64//bits)])&((1<<64)-1))>>((i%(64//bits))*bits)&((1<<bits)-1)

def read_nbt(world,cx,cz):
    p=world/'dimensions/minecraft/overworld/region'/f'r.{cx//32}.{cz//32}.mca'
    with p.open('rb') as f:
        f.seek(((cz%32)*32+cx%32)*4);location=int.from_bytes(f.read(4),'big');assert location
        f.seek((location>>8)*4096);length=int.from_bytes(f.read(4),'big');kind=f.read(1)[0];raw=f.read(length-1)
    if kind&128:raw=(p.parent/f'c.{cx}.{cz}.mcc').read_bytes()
    if kind&127==2:raw=zlib.decompress(raw)
    elif kind&127==1:raw=gzip.decompress(raw)
    elif kind&127!=3:raise ValueError('compression')
    d=nbtlib.File.parse(io.BytesIO(raw));assert (int(d['xPos']),int(d['zPos']))==(cx,cz)
    return d

def scalar(d,x,z):
    sections={int(s['Y']):s for s in d['sections']};low=int(d['yPos'])*16;high=(max(sections)+1)*16
    def block(y):
        s=sections.get(y//16)
        if s is None or 'block_states' not in s:return {'Name':'minecraft:air'}
        p=s['block_states'];n=len(p['palette']);i=(y%16)*256+(z%16)*16+x%16
        raw=p['palette'][value(p.get('data'),max(4,(n-1).bit_length()),i)]
        return {'Name':str(raw['Name']),**({'Properties':{str(k):str(v) for k,v in raw['Properties'].items()}} if 'Properties' in raw else {})}
    def filtered(n):return n in AIR or n in PLANTS or any(t in n for t in ('leaves','_log','_wood','fern','flower','vine','moss_carpet','sapling','azalea','mushroom','_roots'))
    # 从section上界反扫最高非空气，独立检查WORLD_SURFACE没有偏移或漏顶。
    y=high-1
    while block(y)['Name'] in AIR and y>=low:y-=1
    sy=y;top=block(y)
    while filtered(block(y)['Name']) and y>=low:y-=1
    gy=y;support=block(y);ice=support['Name'] in ICE
    if ice:
        while block(y)['Name'] in ICE and y>=low:y-=1
    wy=y if block(y)['Name'] in WATER else -32768;wb=-32768
    if wy!=-32768:
        while block(y)['Name'] in WATER and y>=low:y-=1
        wb=y+1
    def biome(y):
        p=sections[y//16]['biomes'];i=((y%16)//4)*16+(z%16//4)*4+x%16//4
        return str(p['palette'][value(p.get('data'),max(1,(len(p['palette'])-1).bit_length()),i)])
    veg=dict.fromkeys(('leaf','trunk','dry_ground_vegetation','other_vegetation'),0)
    for y in range(gy+1,sy+1):
        n=block(y)['Name']
        if 'leaves' in n:veg['leaf']+=1
        elif '_log' in n or '_wood' in n:veg['trunk']+=1
        elif n=='minecraft:dead_bush' or 'dry_grass' in n:veg['dry_ground_vegetation']+=1
        elif filtered(n) and n not in AIR:veg['other_vegetation']+=1
    return {'surface_y':sy,'exposed_y':gy,'water_y':wy,'water_bottom':wb,'surface_state':top,'exposed_state':support,'biome':biome(sy),'filtered_biome':biome(gy),'vegetation':veg}

def main(world):
    db=sqlite3.connect((ROOT/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
    m=np.load(ROOT/'raw-or-queryable/derived.npz');main=m['main_island'];rng=np.random.default_rng(2002);points={}
    def add(mask,label,count=35):
        coords=np.argwhere(mask)
        for i in rng.choice(len(coords),min(count,len(coords)),replace=False):
            z,x=map(int,coords[i]);points[(x+BOUNDS[0],z+BOUNDS[1])]=label
    add(main,'island_random',45);add(main&(m['relief32']>=8),'higher_relief');add(main&(m['terrain_class']==1),'lowland');add(m['shoreline'],'shore');add(main&(np.indices(main.shape)[1]<400),'western_lobes');add((m['water_component']>1),'internal_or_small_water');add((m['land_component']==2),'eastern_context')
    for x in (BOUNDS[0],BOUNDS[0]+1,BOUNDS[2]-1,BOUNDS[2]):
        for z in (BOUNDS[1],BOUNDS[1]+1,BOUNDS[3]-1,BOUNDS[3]):points[(x,z)]='corner_edge'
    for _ in range(40):points[(int(rng.integers(BOUNDS[0]//4,BOUNDS[2]//4))*4,int(rng.integers(BOUNDS[1]//4,BOUNDS[3]//4))*4)]='vegetation_grid'
    states={r['id']:json.loads(r['json']) for r in db.execute('SELECT * FROM states')};biomes={r['id']:r['name'] for r in db.execute('SELECT * FROM biomes')};chunks={};results=[]
    with ReadGuard(world):
        for (x,z),category in sorted(points.items()):
            key=(x//16,z//16)
            if key not in chunks:chunks[key]=read_nbt(world,*key)
            independent=scalar(chunks[key],x,z);row=dict(db.execute('SELECT * FROM samples WHERE x=? AND z=?',(x,z)).fetchone())
            observed={k:states[row[k]] if k.endswith('_state') else biomes[row[k]] if 'biome' in k else row[k] for k in independent if k!='vegetation'}
            assert all(observed[k]==v for k,v in independent.items() if k!='vegetation'),(x,z,observed,independent)
            if x%4==0 and z%4==0:
                v=dict(db.execute('SELECT * FROM vegetation WHERE x=? AND z=?',(x,z)).fetchone());assert all(v[k]==n for k,n in independent['vegetation'].items())
            results.append({'x':x,'z':z,'category':category,'independent':independent,'matches':True})
    db.close();write_json(ROOT/'validation/raw-column-crosscheck.json',{'status':'PASS','columns':len(results),'independent_chunks':len(chunks),'method':'scalar long-word palette extraction and top-down nonair scan; no production decoder imports','checks':results});print('independent raw columns PASS',len(results),flush=True)
if __name__=='__main__':main(Path(sys.argv[1]).resolve())
