"""独立解码规划 JSON，验证覆盖、几何/统计一致和前序证据封口；不调用生成器。"""
import json,hashlib,sqlite3,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[3]
CACHE=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001P-R1')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()
def write(name,d):(OUT/'validation'/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
doc=read(ROOT/'research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json');a=np.full((2112,3264),255,np.uint8)
for z,l,h,c in doc['runs']:a[z-1376,l+800:h+801]=c
m=a==2
def mask(runs):
    result=np.zeros(a.shape,bool)
    for z,l,h in runs:
        assert 1376<=z<=3487 and -800<=l<=h<=2463
        assert not result[z-1376,l+800:h+801].any();result[z-1376,l+800:h+801]=True
    assert m[result].all();return result
def partition(items):
    counts=np.zeros(a.shape,np.uint8)
    for item in items:
        q=mask(item['geometry']);assert int(q.sum())==item.get('area',item.get('terrain',{}).get('area'));counts+=q
    assert np.array_equal(counts,m.astype(np.uint8))
partition(read(OUT/'subareas.json')['subareas']);partition(read(OUT/'land-use.json')['zones']);partition(read(OUT/'human-use-intensity.json')['zones'])
nodes=read(OUT/'settlement-nodes.json')['nodes'];used=np.zeros(a.shape,bool)
for n in nodes:
    q=mask(n['envelope']);assert int(q.sum())==n['envelope_area'];assert not (q&used).any();used|=q
    x,z=n['point'];assert q[z-1376,x+800]
assert len(nodes)==5 and sum(n['rank']=='principal_hub' for n in nodes)==1
reserve=mask(next(z for z in read(OUT/'land-use.json')['zones'] if z['code']==2)['geometry']);assert not (used&reserve).any()
connector=np.zeros(a.shape,bool)
for z,l,h in read(ROOT/'research/build-sites/CIV-001/AB-001P1R/connector-geometry.json')['runs']:connector[z-1376,l+800:h+801]=True
g=next(n for n in nodes if n['id']=='G1');gm=mask(g['envelope'])
assert np.array_equal(used&connector,gm)
assert g['envelope_area']==7175 and gm[connector].sum()==7175
threshold=mask(next(z for z in read(OUT/'land-use.json')['zones'] if z['code']==3)['geometry'])
clear=mask(read(OUT/'land-use.json')['building_exclusion_overlays'][0]['geometry'])
assert not (gm&threshold).any() and int((gm&clear).sum())==1451
assert g['building_eligible_ceiling_columns']==int((gm&~clear).sum())
assert round(g['envelope_area']*.48)<=g['building_eligible_ceiling_columns']
seen=set(); todo=[tuple(g['point'])]
for x,z in todo:
    if (x,z) in seen:continue
    seen.add((x,z))
    for xx,zz in ((x-1,z),(x+1,z),(x,z-1),(x,z+1)):
        if gm[zz-1376,xx+800] and (xx,zz) not in seen:todo.append((xx,zz))
assert len(seen)==7175
db=sqlite3.connect((ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
network=read(OUT/'movement-network.json');nodepoints={n['id']:n['point'] for n in nodes};nodepoints.update({'I-C':[89,1750],'I-W1':[326,2326],**{i['id']:i['middle_point'] for i in network['east_interfaces']}})
for rt in network['routes']:
    p=np.array(rt['path']);assert (a[p[:,1]-1376,p[:,0]+800]==2).all();assert (abs(np.diff(p[:,:2],axis=0)).sum(axis=1)==1).all();assert int(abs(np.diff(p[:,2])).max())==rt['max_surface_step'];assert len(p)-1==rt['length_blocks'];assert p[0,:2].tolist()==nodepoints[rt['from']] and p[-1,:2].tolist()==nodepoints[rt['to']]
for x,z,yy in {tuple(point) for rt in network['routes'] for point in rt['path']}:assert db.execute('SELECT exposed_y FROM samples WHERE x=? AND z=?',(x,z)).fetchone()[0]==yy
db.close()
for it in network['east_interfaces']:
    x,z=it['middle_point'];xx,zz=it['east_point'];assert abs(x-xx)+abs(z-zz)==1 and a[z-1376,x+800]==2 and a[zz-1376,xx+800]==3
mp=read(OUT/'MASTERPLAN.json');assert mp['source_territory_revision']==154 and mp['middle_exact_area']==391002 and mp['world_write_authorized'] is False
intensity=read(OUT/'human-use-intensity.json');assert intensity['capacity'][0]['indicative_footprint_ratio'][0]>max(i['indicative_footprint_ratio'][0] for i in intensity['capacity'][1:])
for i in (0,1):assert abs(sum(c['footprint_capacity'][i] for c in intensity['capacity'])/391002-intensity['middle_indicative_territory_footprint_ratio'][i])<1e-10
maps=list((OUT/'visual').glob('*.png'));assert len(maps)==9
for p in maps:
    with Image.open(p) as im:assert im.width>=1400 and im.height>=1000;im.verify()
contract=read(OUT/'validation/map-contract.json');assert contract['pixels_per_block_x']==contract['pixels_per_block_z']==1
before=read(CACHE/'source-before.json');after={p.relative_to(ROOT).as_posix():sha(p) for folder in ('research','world','architecture','decisions') for p in (ROOT/folder).rglob('*') if p.is_file()};assert before==after
write('source-audit.json',{'status':'PASS','protected_files':len(before),'source_inventory_sha256':sha(CACHE/'source-before.json'),'research_world_canon_architecture_decisions_unchanged':True,'world_writes':0,'new_world_block_reads':0,'broad_rescan':0,'freshness':'accepted cache only, no claim of current save freshness'})
write('independent-geometry.json',{'status':'PASS','checks':['exact 391002-column subarea/landuse/intensity partitions','five disjoint settlement envelopes; G1 7175 columns connected','only G1 inside P1; threshold and terrain reserve excluded; through-clearance overlay enforced','eight Middle-only path segments; R1a/b reconstruct original R1; cached elevations independently queried','both East interfaces cross exact revision154 shared edges','D025 principal/secondary density gradient and capacity arithmetic','nine PNG maps with equal-scale contracts; visual inspection separate','506 predecessor source files unchanged'],'cross_domain_density_note':'West/East future built coverage is not measured or frozen; D025 ordering retained as next-plan constraint','world_writes':0})
print('independent planning geometry and source audit PASS')

# 固定 Git 基线作独立差分；修订范围之外的字典与逐列用途不能被顺带改写。
BASE='4e276890000ffb87219aaaf1e8c2ea09cc6a8624'; REPO=ROOT.parents[1]
def previous(name):
    return json.loads(subprocess.check_output(['git','show',f"{BASE}:{(OUT/name).relative_to(REPO).as_posix()}"],cwd=REPO))
assert read(OUT/'subareas.json')['subareas'][1:]==previous('subareas.json')['subareas'][1:]
assert read(OUT/'subareas.json')['subareas'][0]['geometry']==previous('subareas.json')['subareas'][0]['geometry']
assert nodes[:4]==previous('settlement-nodes.json')['nodes']
assert network['routes'][2:]==previous('movement-network.json')['routes'][1:]
assert network['routes'][0]['path']+network['routes'][1]['path'][1:]==previous('movement-network.json')['routes'][0]['path'][::-1]
assert network['east_interfaces']==previous('movement-network.json')['east_interfaces']
assert network['water_interfaces']==previous('movement-network.json')['water_interfaces']
for name in ('land-use.json','human-use-intensity.json'):
    for current in read(OUT/name)['zones']:
        prior=next((z for z in previous(name)['zones'] if z['id']==current['id']),None)
        old=mask(prior['geometry']) if prior else np.zeros(a.shape,bool)
        assert not ((mask(current['geometry'])^old)&~connector).any()
with sqlite3.connect((ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True) as db:
    heights=[db.execute('SELECT exposed_y FROM samples WHERE x=? AND z=?',(int(x)-800,int(z)+1376)).fetchone()[0] for z,x in zip(*np.where(gm))]
assert min(heights)==g['terrain']['elevation']['min'] and max(heights)==g['terrain']['elevation']['max'] and float(np.median(heights))==g['terrain']['elevation']['median']
derived=np.load(ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/derived.npz')
assert np.isfinite(derived['slope8'][gm]).all() and (derived['slope8'][gm]<=.25).all()
assert (derived['relief32'][gm]<=8).all() and (derived['step1'][gm]<=2).all()
assert not derived['shoreline'][gm].any()
assert sha(ROOT/'research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json')==mp['source_territory_sha256']
assert mp['first_build_recommendation']['node']=='G1' and mp['world_write_authorized'] is False
assert intensity['P1_threshold_footprint_ratio']==[0,0]
assert np.array_equal(threshold,connector & (np.indices(a.shape)[1]-800<130))
write('scope-delta.json',{'status':'PASS','base_commit':BASE,'unchanged':['revision154 source hash','Commons','P1 exact members','P2-P5 entire records','N1-N4 entire records','R2-R7','East interfaces','water interfaces','all land-use and intensity columns outside P1'],'G1_connected_columns':len(seen),'G1_clearance_columns':1451,'G1_cached_height_and_slope_independent_check':True,'R1_segments_reconstruct_original':True,'world_writes':0})
print('R1 independent scope / P1 geometry / cached terrain PASS')
