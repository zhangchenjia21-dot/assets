"""独立集合/边集合核验分割；验证到主岛的路径只读R1拓扑，不规划道路。"""
import sys,json
from pathlib import Path
from collections import deque
import numpy as np
sys.dont_write_bytecode=True
from 源快照保护器 import digest,write_json
out=Path(__file__).resolve().parents[1];project=out.parents[3];p1=out.parent/'AB-001P1';r1=project/'research/human-geography/southern-island/WB-002R-R1';cache=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/AB-001P1R')
core=['commons-boundary.json','commons-geometry.json','connector-geometry.json','review/cross-sections.json','visual/commons-connector-boundary.png']
if len(sys.argv)>1 and sys.argv[1]=='snapshot':write_json(cache/'rebuild-before.json',{p:digest(out/p) for p in core});sys.exit(0)
def decode(file):
    obj=json.loads(file.read_text(encoding='utf-8'));cells=set()
    for z,s,e in obj['runs']:
        for x in range(s,e+1):assert (x,z) not in cells;cells.add((x,z))
    return obj,cells
source,A=decode(p1/'geometry/A-land-runs.json');co,C=decode(out/'commons-geometry.json');ne,N=decode(out/'connector-geometry.json')
assert C|N==A and not C&N and len(A)==105785 and len(C)==92124 and len(N)==13661
def boundary(cells):
    edges=set()
    for x,z in cells:
        for edge in ((x,z,x+1,z),(x,z+1,x+1,z+1),(x,z,x,z+1),(x+1,z,x+1,z+1)):
            if edge in edges:edges.remove(edge)
            else:edges.add(edge)
    return edges
for obj,cells in ((co,C),(ne,N)):
    unfolded=set()
    for x,z,u,v in obj['outline_segments']:
        assert (x==u) != (z==v)
        for offset in range((u-x) if z==v else (v-z)):
            edge=(x+offset,z,x+offset+1,z) if z==v else (x,z+offset,x,z+offset+1)
            assert edge not in unfolded;unfolded.add(edge)
    assert unfolded==boundary(cells)
    seen={next(iter(cells))};q=deque(seen)
    while q:
        x,z=q.popleft()
        for p in ((x-1,z),(x+1,z),(x,z-1),(x,z+1)):
            if p in cells and p not in seen:seen.add(p);q.append(p)
    assert seen==cells
# 仅在切口以东的父陆体寻路，禁止绕回Commons以伪证续接。
with np.load(r1/'raw-or-queryable/derived.npz') as f:labels=f['land_component']
start=min(p for p in N if p[0]==240);q=deque([start]);prev={start:None};goal=None
while q:
    x,z=q.popleft()
    if x==400:goal=(x,z);break
    for p in ((x-1,z),(x+1,z),(x,z-1),(x,z+1)):
        px,pz=p
        if 89<=px<=400 and 1453<=pz<=2050 and p not in prev and labels[pz-1376,px+800]==2:prev[p]=(x,z);q.append(p)
assert goal is not None
path=[]
while goal is not None:path.append(list(goal));goal=prev[goal]
path.reverse()
for x,z in path:assert x>=89 and (x,z) not in C and labels[z-1376,x+800]==2
write_json(out/'review/parent-continuation.json',{'purpose':'topological witness only, not access route or road','start_in_connector':path[0],'end_east_mainland':path[-1],'cardinal_steps':len(path)-1,'path_xz':path,'commons_never_entered':True,'source':'R1 derived.npz land_component=2'})
b=json.loads((out/'commons-boundary.json').read_text(encoding='utf-8'));seams=boundary(C)&boundary(N);assert len(seams)==48 and all(e[0]==e[2]==89 for e in seams)
before=json.loads((cache/'rebuild-before.json').read_text(encoding='utf-8'));assert all(digest(out/p)==h for p,h in before.items())
write_json(out/'validation/independent.json',{'status':'PASS','A_area':len(A),'commons_area':len(C),'connector_area':len(N),'union_disjoint_complete':True,'each_component_connected':True,'outline_exact_edge_symmetric_difference':True,'shared_cut_unit_edges':len(seams),'parent_connection_without_commons':True,'no_world_block_reads':True})
write_json(out/'validation/rebuild.json',{'status':'PASS','fresh_process_byte_identical':before,'source':'immutable AB-001P1 geometry + R1 caches','human_selected_cut':'Plane X89; testing does not replace independent interpretation review'})
print('independent partition, outline, parent path and rebuild PASS',flush=True)
