"""只从已接受缓存生成浏览器可用的紧凑mask与阅读底图；不扫描世界方块。"""
import sys,json,sqlite3,base64,io,hashlib
from pathlib import Path
from datetime import datetime,timezone
from contextlib import ExitStack
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
from 源快照保护器 import digest,write_json,fingerprint,ReadGuard
out=Path(__file__).resolve().parents[1];project=out.parents[1];cache=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/TT-001');r1=project/'research/human-geography/southern-island/WB-002R-R1';p1r=project/'research/build-sites/CIV-001/AB-001P1R';world=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师')
roots={'research':project/'research','world_canon':project/'world','architecture':project/'architecture'}
if sys.argv[1] in ('init','seal'):
    with ExitStack() as stack:
        for r in roots.values():stack.enter_context(ReadGuard(r))
        now={k:fingerprint(v) for k,v in roots.items()}
        if sys.argv[1]=='init':
            assert not (cache/'source-before.json').exists();write_json(cache/'source-before.json',now)
            expected=json.loads((r1/'profile/scope-completion.json').read_text(encoding='utf-8'))['relevant_region_hashes']
            write_json(out/'validation/freshness.json',{'status':'CACHED_EPOCH_ONLY','current_world_freshness':'NOT_VERIFIED_WORLD_IN_USE','reason':'initial read-only guard failed with sharing violation; task uses accepted immutable cache only, no retry or game manipulation','r1_relevant_regions':expected,'task_start_inventory_sha256':digest(cache/'source-before.json'),'checked_at':datetime.now(timezone.utc).isoformat(),'new_world_block_reads':0})
        else:
            before=json.loads((cache/'source-before.json').read_text(encoding='utf-8'));unchanged={k:before[k]==v for k,v in now.items()};assert all(unchanged.values());write_json(out/'validation/source-audit.json',{'status':'PASS','unchanged':unchanged,'world_writes':0,'new_world_block_reads':0,'checked_at':datetime.now(timezone.utc).isoformat()})
    print('source audit complete');sys.exit()
assert sys.argv[1]=='build'
w,h=3264,2112;bounds=[-800,1376,2463,3487]
with np.load(r1/'raw-or-queryable/derived.npz') as f:land=f['land_component']>0;shore=f['shoreline'];slope=f['slope8']
db=sqlite3.connect((r1/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
arr=np.asarray(db.execute('SELECT exposed_y,biome FROM samples ORDER BY z,x').fetchall(),np.int32).reshape(h,w,2);biomes=dict(db.execute('SELECT * FROM biomes'));db.close()
def png(a):
    b=io.BytesIO();Image.fromarray(a).save(b,format='PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
grey=np.clip(110+(arr[:,:,0]-62)*.42-np.nan_to_num(slope,nan=0)*30,55,235).astype(np.uint8);rgb=np.zeros((h,w,3),np.uint8);rgb[:]=(36,65,82)
rgb[land]=np.stack([grey[land]*.86,grey[land]*.94,grey[land]*.78],axis=1).astype(np.uint8);rgb[shore]=(185,210,199)
palette={};bio=np.zeros_like(rgb);bio[:]=(36,65,82)
for k,name in sorted(biomes.items()):
    seed=hashlib.sha256(name.encode()).digest();color=[75+v%125 for v in seed[:3]];palette[str(k)]={'name':name,'color':color};bio[land&(arr[:,:,1]==k)]=color
commons=json.loads((p1r/'commons-geometry.json').read_text(encoding='utf-8'))['runs'];connector=json.loads((p1r/'connector-geometry.json').read_text(encoding='utf-8'))['runs']
for runs,count in ((commons,92124),(connector,13661)):
    assert sum(e-s+1 for z,s,e in runs)==count
    assert all(land[z-bounds[1],s-bounds[0]:e-bounds[0]+1].all() for z,s,e in runs)
source_files=[r1/'raw-or-queryable/observed.sqlite',r1/'raw-or-queryable/derived.npz',p1r/'commons-geometry.json',p1r/'connector-geometry.json',project/'decisions/D-020_AB-001P1R联盟公地精确边界接受.md']
inputs=[{'path':p.relative_to(project).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size} for p in source_files];sourceid=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest()
data={'schema':'territory-base/1','id':sourceid,'bounds':bounds,'width':w,'height':h,'landCount':int(land.sum()),'landBits':base64.b64encode(np.packbits(land.ravel(),bitorder='little').tobytes()).decode(),'commons':commons,'connector':connector,'terrainImage':png(rgb),'biomeImage':png(bio),'biomeLegend':palette,'references':inputs,'freshness':json.loads((out/'validation/freshness.json').read_text(encoding='utf-8'))['status'],'acceptedBoundary':'D-020 / AB-001P1R @723f921; Commons92124; connector13661; cutX89','coordinateConvention':'block(x,z) occupies [x,x+1) by [z,z+1); horizontal runs inclusive'}
(out/'预加载/地理数据.js').write_text('window.TERRITORY_BASE='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
write_json(out/'预加载/manifest.json',{k:v for k,v in data.items() if k not in ('landBits','commons','connector','terrainImage','biomeImage','biomeLegend')})
print('preload generated',data['landCount'],(out/'预加载/地理数据.js').stat().st_size,'bytes')
