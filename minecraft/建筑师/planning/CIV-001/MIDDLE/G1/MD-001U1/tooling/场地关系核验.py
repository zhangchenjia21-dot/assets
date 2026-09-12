"""对设计的场地关系作独立集合/剖面核验；不通过评分替模型决定设计。"""
import importlib.util,json,gzip,math,heapq
from pathlib import Path
from collections import deque
spec=importlib.util.spec_from_file_location('design',Path(__file__).with_name('街区设计编译.py'));d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
model=json.load(gzip.open(d.OUT/'design-model.json.gz','rt',encoding='utf8'));bs=d.read(d.OUT/'building-roles.json')['buildings']
cir=d.read(d.OUT/'circulation.json');foot=set().union(*(d.rect(*b['bounds']) for b in bs))
def component_sizes(points):
    left=set(points);sizes=[]
    while left:
        start=left.pop();q=deque([start]);n=1
        while q:
            x,z=q.popleft()
            for p in [(x+1,z),(x-1,z),(x,z+1),(x,z-1)]:
                if p in left:left.remove(p);q.append(p);n+=1
        sizes.append(n)
    return sorted(sizes,reverse=True)
def projection(v):return d.rect(math.floor(v['a'][0]),math.floor(v['a'][2]),math.ceil(v['b'][0])-1,math.ceil(v['b'][2])-1)
roofs=set().union(*(projection(v) for v in model['boxes'] if v['role'] in ['roof','canopy']))
above_conflicts=[];retained=[]
for x,z in sorted(d.ENVELOPE):
    for y,n in d.SURF[x,z]['above']:
        if 'leaves' not in n and '_log' not in n:continue
        clash=[v for v in model['boxes'] if v['a'][0]<x+1 and v['b'][0]>x and v['a'][2]<z+1 and v['b'][2]>z and v['a'][1]<y+1 and v['b'][1]>y]
        (above_conflicts if clash else retained).append([x,y,z,n])
clear=d.CLEAR;threshold=set().union(*(d.cells(z['geometry']) for z in d.LU['zones'] if z['code']==3))
g1=d.G1;exclude=set().union(*(d.cells(z['geometry']) for z in d.LU['zones'] if z['code']==2))
gaps=[]
for i,a in enumerate(bs):
    aa=d.rect(*a['bounds'])
    for b in bs[i+1:]:
        bb=d.rect(*b['bounds']);dist=min(abs(x-X)+abs(z-Z) for x,z in aa for X,Z in bb)-1
        gaps.append({'a':a['id'],'b':b['id'],'minimum_empty_columns_manhattan':dist})
# 排水提案限定在设计包络；端点仍是局部出水见证，不编造完整汇水区性能。
drains=[
 {'id':'D-L','points':[[211,64.5,1711],[200,64.5,1711],[200,62.5,1695]],'purpose':'生活院雨水沿西侧维护缝向北；格栅盖板跨过步行路线'},
 {'id':'D-H','points':[[230,66.5,1695],[200,62.5,1695]],'purpose':'高台屋面经北侧檐沟收集后沿北缘下送；不向生活院自由跌水'}]
for rt in drains:
    samples=[]
    for a,b in zip(rt['points'],rt['points'][1:]):
        n=int(abs(b[0]-a[0])+abs(b[2]-a[2]));assert n>0 and b[1]<=a[1]
        for t in range(n+1):samples.append([round(a[j]+(b[j]-a[j])*t/n,3) for j in range(3)])
    rt['centerline_samples']=samples
    rt['all_within_envelope']=all((round(x),round(z)) in d.ENVELOPE for x,y,z in samples)
    rt['footprint_crossings']=sum((round(x),round(z)) in foot for x,y,z in samples)
    assert rt['all_within_envelope'] and not rt['footprint_crossings']
d.write(d.OUT/'drainage-vegetation.json',{'status':'PROPOSED_ENGINEERING_DETAIL / NOT FLUID_VALIDATED','drains':drains,
 'outlet':{'point':[200,62.5,1695],'current_ground_y':d.SURF[200,1695]['ground_y'],'receiving_strip_bounds':[199,1695,201,1697],
           'condition':'local filter/maintenance strip only; hydraulic capacity and downstream receiving conditions require pre-build confirmation'},
 'dry_waste':'sealed removable containers at [190,1717]; no soakaway or discharge to stormwater',
 'vegetation_conflicting_with_design_solids':above_conflicts,'vegetation_not_intersecting_design_solids':retained,
 'vegetation_status':'no vegetation changed; intersecting fragments must be resolved by bounded future clearance/retention design; no tree-count inference',
 'clean_water':'delivered clean storage reserved at [211,1712]; source unknown; no well, spring, water-source block or drinking-water claim'})
# 主通行链仅作为读入上下文，不将其自动编译成道路。
paths=[p for rt in d.read(d.PLAN/'movement-network.json')['routes'][:2] for p in rt['path']]
connections=[]
for x,z in [(209,1723),(231,1714)]:
    nearest=min(paths,key=lambda p:abs(p[0]-x)+abs(p[1]-z));connections.append({'design_edge':[x,z],'nearest_R1_reference':nearest,'status':'context relation only; outside-envelope route not designed/cleared'})
d.write(d.OUT/'validation/spatial-relations.json',{'envelope_components':component_sizes(d.ENVELOPE),
 'unbuilt_columns_components':component_sizes(d.ENVELOPE-foot),'building_footprint_columns':len(foot),
 'roof_and_canopy_projection_columns':len(roofs),'roof_projection_coverage':len(roofs)/len(d.ENVELOPE),
 'footprint_overlap_clearance':len(foot&clear),'all_roof_overlap_clearance':len(roofs&clear),
 'all_roof_overlap_threshold':len(roofs&threshold),'all_roof_overlap_reserve':len(roofs&exclude),'all_roof_outside_G1':len(roofs-g1),
 'pairwise_spacing':gaps,'R1_connections':connections,
 'open_space_note':'one connected open system does not certify absence of every dead-end; B5 east maintenance strip is explicitly service-only, not an advertised public alley',
 'fire_and_daylight':'minimum wall gap3 at B4/B2 and eave gap1; no cross-alley timber bridge; maintained separation proposal, not fire-code or seasonal daylight simulation'})
assert len(component_sizes(d.ENVELOPE))==1
assert not roofs&clear and not roofs&threshold and not roofs&exclude and roofs<=g1
qa=d.read(d.OUT/'validation/design-qa.json')
assert not any(a['failures'] for a in qa['stairs']+qa['routes'])
print('spacing',gaps,'roof area',len(roofs),'tree conflicts',len(above_conflicts),'retained fragments',len(retained))
