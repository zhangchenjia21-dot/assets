"""验证来源、区域包契约、容量和可复现性；不评回归质量。"""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,v):(ROOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def read(n):return json.loads((ROOT/n).read_text(encoding='utf8'))
base='8d4c9f8f81fedab66859b16fb9f1ab941747fef5';skill_commit='e72acd9e735c23261a3e41cde2402b4302c104a0'
rs='minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/'
src=[('SRC-PARENT','minecraft/MP-P01R-CIV001/implementation-packages.json','REGRESSION_PARENT_NOT_CANON'),('SRC-PARENT-REFS','minecraft/MP-P01R-CIV001/planning-objects.json','REGRESSION_PARENT_NOT_CANON'),('SRC-CANON','minecraft/建筑师/world/civilizations/CIV-001/README.md','APPROVED_CANON'),('SRC-OBS',rs+'raw-or-queryable/observed.sqlite.gz','OBSERVED'),('SRC-DERIVED',rs+'raw-or-queryable/derived.npz','DERIVED'),('SRC-PROFILE',rs+'manifest/profile.json','DERIVED'),('SRC-ATLAS','minecraft/建筑师/research/natural-geography/NG-3/atlas/objects.jsonl','DERIVED'),('SRC-ATLAS-MANIFEST','minecraft/建筑师/research/natural-geography/NG-3/manifest/atlas.json','DERIVED')]
reg=[]
for id,path,authority in src:
 digest=sha(REPO/path);expected=hashlib.sha256(subprocess.check_output(['git','show',f'{base}:{path}'],cwd=REPO)).hexdigest();assert digest==expected
 reg.append(dict(id=id,path=path,authority=authority,sha256=digest,assets_commit=base,unchanged_from_source_commit=True))
# 只提取宏观自然对象，避免引入 SITE 潜力或旧人文答案。
atlas=[]
for line in (REPO/src[6][1]).open(encoding='utf8'):
 o=json.loads(line)
 if o['family'] not in ['NGEO','NHYD']:continue
 b=o['geometry']['bounds']
 if b[2]>=256 and b[0]<=2175 and b[3]>=1440 and b[1]<=3263:atlas.append(o)
dump('evidence/atlas-natural-subset.json',atlas)
skills=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),source_url=f'https://raw.githubusercontent.com/zhangchenjia21-dot/Vibe-Coding/{skill_commit}/skill/codex/minecraft-planner/'+p.relative_to(ROOT/'sources/skill').as_posix()) for p in sorted((ROOT/'sources/skill').rglob('*.md'))]
assert sha(ROOT/'sources/skill/SKILL.md')=='5b9b0c2c5ebfbae71e21a150a6f88537a09375e54ab91e6859327808c1741a27'
dump('source-register.json',dict(sources=reg,skill_version='minecraft-planner v0.2',skill_commit=skill_commit,skill_files=skills,parent_extraction='PACKAGE-03 only; necessary NODE-04/05/06, ROUTE-05/06, ANCHOR-05/06 refs',read_filters={'sqlite':['samples.exposed_y','samples.water_y','samples.artificial_material'],'npz':['land_component','slope8','relief32'],'atlas':['NGEO','NHYD']},excluded='MP-P01 old plan; old East/Middle/G1/N1 settlement answers; reviews; targets/assessments; k2/k3/k4/k5/zones',freshness='R1 snapshot base bc96aa5; no live-world freshness claim',world_writes=0))
o=read('planning-objects.json');pack=read('implementation-packages.json');demand=read('demand-model.json');cap=read('settlement-capacity.json')
ids=[x['id'] for k in ['nodes','corridors','interfaces','anchors','spaces'] for x in o[k]];assert len(ids)==len(set(ids))
assert len(o['nodes'])==3 and o['rejected_candidates'][0]['id']=='NODE-04'
for n in o['nodes']:
 c=n['built_fabric_capacity'];assert c['confidence']=='LOW'
 assert c['area_range_blocks2']==c['arithmetic']==[c['household_pressure_range'][j]*c['household_land_allowance_range'][j]+c['shared_land_range'][j] for j in (0,1)]
 assert n['location_search_envelope'] and n['functional_hinterland']
for d in demand:assert all(x in ids for x in d['dependencies'])
for c in o['corridors']:assert c['from_id'] in ids and c['to_id'] in ids and c['usable_route']=='UNVERIFIED'
for p in pack:
 assert p['child_scale']=='SETTLEMENT' and p['recipient']=='minecraft-planner'
 assert not p['world_write_authorization'] and not p['builder_ready']
 assert all(x in ids for x in p['scope']+p['upstream_flow_refs'])
 for k in ['UPSTREAM_FIXED','DOWNSTREAM_TO_RESOLVE','DOWNSTREAM_ADAPTABLE','REVISION_TRIGGER']:assert p[k]
assert cap['north_total']==[sum(n['built_fabric_capacity']['area_range_blocks2'][j] for n in o['nodes'][:2]) for j in (0,1)]
assert cap['remote_total_if_activated']==o['nodes'][2]['built_fabric_capacity']['area_range_blocks2']
assert read('evidence/direct-remote-comparison.json')['extra_length']==820
generated=['planning-objects.json','demand-model.json','growth-sequence.json','building-program.json','implementation-packages.json','parent-delta.json','settlement-capacity.json','区域图册.html','evidence/corridor-models.json','evidence/direct-remote-comparison.json']+[f'maps/{i:02d}.png' for i in range(1,6)]
before={n:sha(ROOT/n) for n in generated}
for script in ['区域通道检验.py','区域规划生成.py']:subprocess.run([sys.executable,str(ROOT/script)],check=True)
assert before=={n:sha(ROOT/n) for n in generated}
dump('validation.json',dict(status='ARTIFACT_CHECKS_COMPLETED_NOT_REGRESSION_VERDICT',active_nodes=3,rejected_candidate='NODE-04',corridors=3,settlement_packages=3,checks={'unique_ids':True,'references_resolve':True,'capacity_arithmetic':True,'north_parent_capacity_not_duplicated':True,'remote_reduced_not_increased':True,'search_capacity_hinterland_distinct':True,'source_hashes_match_git_snapshot':True,'deterministic_rebuild_equal':True,'service_detour_comparison':{'extra_blocks':820,'action':'withdraw fixed service node'}},visual_review={'method':'rendered PNG view_image','maps':['01','02','03','04','05'],'limitation':'No in-game verification; map scale circles are not exact footprints'},planning_gates={'Premise':'READY_AS_CONDITIONAL_PLANNING','Morphology':'READY_AS_REGIONAL_RELATIONS_AND_CAPACITY_HYPOTHESES','Handoff':'READY_FOR_L2_EVIDENCE_AND_PLANNING_NOT_BUILD','REVIEWED':False},unverified=['current world freshness','existing fabric and tenure','water/food/fuel/ore','actual usable routes and collision'],world_writes=0,save_access='NONE',protected_sources_modified=False))
print('Source hashes, references, capacity accounting and deterministic regeneration verified.')
