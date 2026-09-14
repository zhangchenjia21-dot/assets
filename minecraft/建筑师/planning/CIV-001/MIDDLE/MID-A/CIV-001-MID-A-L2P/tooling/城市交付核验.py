"""机械检查不会替代规划独立审核；只核验守恒、成员、当前见证与权限。"""
from pathlib import Path
from collections import deque
import json,hashlib,os
import numpy as np
P=Path(__file__).resolve().parents[1];C=Path(os.environ['MID_A_CACHE']);R=Path(os.environ['MID_A_REPO'])
read=lambda n:json.loads((P/n).read_text('utf-8'))
g=read('evidence/settlement-geometry.json');obs=read('evidence/current-observation.json');a=np.load(C/'current.npz');cm=np.load(C/'city-map.npz');rows=a['rows'];sub=a['sub']
assert obs['before']==obs['after'] and obs['world_writes']==0
for name,fp in obs['before'].items():assert hashlib.sha256((C/'snapshot'/name).read_bytes()).hexdigest()==fp['sha256']
def points(runs):
 result=set()
 for z,x0,x1 in runs:
  assert x0<=x1
  for x in range(x0,x1+1):assert (x,z) not in result;result.add((x,z))
 return result
city=points(g['city_runs']);assert len(city)==29175
terr=json.loads((R/'minecraft/建筑师/research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json').read_text('utf-8'))
middle={(x,z) for z,x0,x1,k in terr['runs'] if k==2 for x in range(x0,x1+1)};assert city<=middle
seen={next(iter(city))};q=deque(seen)
while q:
 x,z=q.popleft()
 for v in [(x+1,z),(x-1,z),(x,z+1),(x,z-1)]:
  if v in city and v not in seen:seen.add(v);q.append(v)
assert seen==city
cover=set()
for d in g['districts']:
 p=points(d['runs']);assert len(p)==d['area'] and not p&cover;cover|=p
assert cover==city
reserve=points(next(v for v in g['reserves'] if v['id']=='public_non_roof_reserve')['runs']);assert reserve<=city and len(reserve)==7058
assert len(city-reserve)==22117
sr={(int(x),int(z)):(int(h),int(si)) for x,z,top,h,si,l,ll in rows};assert len(sr)==47704 and city<=set(sr)
volumes={}
for x,y,z,si in sub:
 if (int(x),int(z)) in city:volumes.setdefault((int(x),int(z)),set()).add(int(y))
assert set(volumes)==city
for p,levels in volumes.items():assert levels==set(range(sr[p][0]-12,sr[p][0]+1))
for p in read('evidence/access-probes.json')['probes']:
 assert p['reached'];path=p['path'];assert len(path)-1==p['length']
 for x,z,h in path:
  assert (x,z) in city and sr[(x,z)][0]==h and not cm['void'][z-1453,x-89] and not cm['wet'][z-1453,x-89] and cm['logs'][z-1453,x-89]==0
 for u,v in zip(path,path[1:]):assert abs(u[0]-v[0])+abs(u[1]-v[1])==1 and abs(u[2]-v[2])<=1
den=read('DENSITY-LAND-USE.json');assert den['working_built_fabric']==22117 and den['non_roof_reserve']==7058
for d in g['districts']:
 pkg=read('handoff/L3-'+d['id']+'.json');assert pkg['child_scale']=='DISTRICT' and pkg['world_write_authorization'] is False and pkg['L3_execution_authorized'] is False
 assert pkg['capacity']['city_area']==d['area'] and pkg['capacity']['working_built_fabric']==d['working_fabric_area']
for v in read('visual/maps.json'):assert hashlib.sha256((P/'visual'/v['file']).read_bytes()).hexdigest()==v['sha256'] and v['pixels_per_block']==3
out=dict(status='MECHANICAL_CHECKS_PASSED_NOT_INDEPENDENT_PLANNING_ACCEPTANCE',city_area=29175,city_components=1,political_overreach=0,district_partition_overlap=0,non_roof_reserve=7058,working_fabric=22117,surface_columns=47704,selected_city_shallow_columns=len(volumes),selected_city_shallow_voxels=29175*13,total_shallow_voxels=len(sub),snapshot_hashes_match=True,heightmap_independent_checks=obs['heightmap_independent_checks'],current_access_witnesses=3,maps=6,L3_packages=3,world_writes=0,world_loads=0,Builder_calls=0,L3_executed=False,limits=['Five isolated single-column nonreserved pieces are not standalone buildable parcels; capacities remain upper working hypotheses','No real road/collision/tenure or potable water proof','Underlying NBT containers include unqueried context; analysis bounded to mask and selected chunks'])
outpath=Path(os.environ.get('MID_A_CHECK_OUTPUT',str(P/'validation/mechanical-checks.json')));outpath.parent.mkdir(parents=True,exist_ok=True);outpath.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,ensure_ascii=False))
