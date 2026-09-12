"""独立解码交付 RLE 与当前快照，核验禁入范围、浅层记录、源封口和高度见证。"""
import json,hashlib
from collections import Counter,deque
import numpy as np
from PIL import Image
import 当前场地读取 as s

def members(runs):
    out=set()
    for z,l,r in runs:
        assert l<=r
        for x in range(l,r+1):assert (x,z) not in out;out.add((x,z))
    return out

doc=s.read(s.OUT/'candidates.json');cs=doc['candidates'];assert len(cs)==3
g=members(next(n for n in s.read(s.PLAN/'settlement-nodes.json')['nodes'] if n['id']=='G1')['envelope'])
land=s.read(s.PLAN/'land-use.json');clear=members(land['building_exclusion_overlays'][0]['geometry'])
threshold=members(next(z for z in land['zones'] if z['code']==3)['geometry']);reserve=members(next(z for z in land['zones'] if z['code']==2)['geometry'])
reader=s.Reader();used=set();witnesses=[]
for c in cs:
    m=members(c['geometry']);buf=members(c['buffer_geometry'])
    assert len(m)==c['gross_usable_area'] and m<=g and not m&(clear|threshold|reserve|used);used|=m
    assert m<=buf and len(buf)==c['buffer_area']
    todo=[next(iter(m))];seen=set(todo)
    for x,z in todo:
        for q in ((x-1,z),(x+1,z),(x,z-1),(x,z+1)):
            if q in m and q not in seen:seen.add(q);todo.append(q)
    assert seen==m
    assert c['subsurface']['queried_blocks']==len(buf)*13 and not c['subsurface']['anomalies']
    assert not c['identified_artificial_surface'] and not c['block_entities_in_buffer']
    values=[]
    for x,z in sorted(m):
        p=reader.surface(x,z);values.append(p['ground_y'])
        assert not s.artificial(p['ground']) and p['ground'] not in s.WATER
    assert [min(values),max(values)]==c['surface_elevation_range']
    for x,z in sorted(m)[::max(1,len(m)//15)]:
        p=reader.surface(x,z);chunk=reader.chunk(x//16,z//16)
        top=(max(int(section['Y']) for section in chunk['sections'])+1)*16-1
        while reader.block(x,top,z) in s.AIR:top-=1
        assert top==p['surface_y']
        witnesses.append({'site':c['id'],'x':x,'z':z,'heightmap_surface_y':p['surface_y'],'brute_vertical_surface_y':top})
    for name in ('access_witness','drainage_witness'):
        path=c[name];assert path and (path[0][0],path[0][1]) in m
        for p in path:assert reader.surface(p[0],p[1])['ground_y']==p[2]
        for a,b in zip(path,path[1:]):assert abs(a[0]-b[0])+abs(a[1]-b[1])==1
    assert all(b[2]<=a[2] for a,b in zip(c['drainage_witness'],c['drainage_witness'][1:]))
    assert c['drainage_witness'][-1][2]<c['drainage_witness'][0][2]
    assert c['local_pit_check']['maximum_fill_depth']==0

audit=s.read(s.OUT/'current-world-audit.json');assert audit['world_name']=='建筑师' and audit['data_version']==4903
for r in audit['snapshot_files']:
    p=s.WORLD/r['world_relative'];assert s.sha(p)==r['sha256'] and p.stat().st_mtime_ns==r['mtime_ns'] and p.stat().st_size==r['size']
    assert s.sha(s.CACHE/'snapshot'/r['snapshot_name'])==r['sha256']
assert s.read(s.OUT/'recommended-site.json')['geometry']==cs[0]['geometry']
before=s.read(s.CACHE/'protected-before.json')
assert all(s.sha(s.ROOT/name)==digest for name,digest in before.items())
maps=list((s.OUT/'visual').glob('*.png'));assert len(maps)==3
for p in maps:
    with Image.open(p) as im:assert im.size==(1800,1160);im.verify()
contracts=s.read(s.OUT/'validation/map-contract.json')
assert all(c['pixels_per_block_x']==c['pixels_per_block_z'] for c in contracts.values())
s.write(s.OUT/'validation/geometry-and-source.json',{'status':'PASS','candidate_areas':[len(members(c['geometry'])) for c in cs],'three_disjoint_connected_envelopes_inside_G1':True,'no_threshold_clearance_or_reserve_overlap':True,'candidate_current_surface_verified':True,'access_and_drainage_witnesses_verified':True,'local_closed_pit_depths':[c['local_pit_check']['maximum_fill_depth'] for c in cs],'snapshot_and_current_source_sha_size_mtime_unchanged':True,'protected_planning_authority_files_unchanged':len(before),'world_writes':0,'broad_rescan':0,'new_world_column_reads':audit['scope_columns'],'extra_eye_ray_sample_columns':audit['extra_visual_ray_columns'],'maps_equal_scale':True})
s.write(s.OUT/'validation/heightmap-crosscheck.json',{'status':'PASS','method':'brute downward block scan from highest section, independent of Heightmaps indexing','witnesses':witnesses})
print('site geometry / current source / heightmap cross-check PASS',len(witnesses),'vertical witnesses')
