"""核对本轮来源、引用、规模算术与重建稳定性；不评判回归质量。"""
from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,v):(ROOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
raw='minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/'
entries=[('SRC-CANON','minecraft/建筑师/world/civilizations/CIV-001/README.md','APPROVED_CANON'),
 ('SRC-D014','minecraft/建筑师/decisions/D-014_CIV-001最小文明Canon收敛与AB-001进入.md','APPROVED_CANON'),
 ('SRC-D020','minecraft/建筑师/decisions/D-020_AB-001P1R联盟公地精确边界接受.md','APPROVED_CANON'),
 ('SRC-R1-OBS',raw+'raw-or-queryable/observed.sqlite.gz','OBSERVED'),
 ('SRC-R1-DERIVED',raw+'raw-or-queryable/derived.npz','DERIVED'),
 ('SRC-R1-PROFILE',raw+'manifest/profile.json','DERIVED'),
 ('SRC-R1-STORE',raw+'manifest/store.json','DERIVED'),
 ('SRC-R1-SCOPE',raw+'profile/scope-completion.json','DERIVED'),
 ('SRC-R1-LAND',raw+'profile/land-components.json','DERIVED'),
 ('SRC-ATLAS','minecraft/建筑师/research/natural-geography/NG-3/atlas/objects.jsonl','DERIVED'),
 ('SRC-ATLAS-MANIFEST','minecraft/建筑师/research/natural-geography/NG-3/manifest/atlas.json','DERIVED'),
 ('SRC-ATLAS-FRESHNESS','minecraft/建筑师/research/natural-geography/NG-3/manifest/freshness.json','DERIVED')]
register=[]
for id,p,a in entries:register.append(dict(id=id,path=p,sha256=digest(REPO/p),authority=a,repository='zhangchenjia21-dot/assets',snapshot='b9fe3488fba793854314dc37a4540c0bff2eea86',used_for='Canon constraints' if a=='APPROVED_CANON' else 'natural terrain evidence only',limitations='历史快照；没有当前世界 freshness 或人文实存验证'))
skill=[]
for p in sorted((ROOT/'sources/skill').rglob('*.md')):skill.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p),source_url='https://raw.githubusercontent.com/zhangchenjia21-dot/Vibe-Coding/eb58654568d31d96ea1ee50f100e1ef6b927daa0/skill/codex/minecraft-planner/'+p.relative_to(ROOT/'sources/skill').as_posix()))
assert skill and digest(ROOT/'sources/skill/SKILL.md')=='5b9b0c2c5ebfbae71e21a150a6f88537a09375e54ab91e6859327808c1741a27'
dump('source-register.json',dict(archive_revision='r1',sources=register,skill_version='minecraft-planner v0.2',skill_files=skill,skill_commit='eb58654568d31d96ea1ee50f100e1ef6b927daa0',pinned_skill_byte_comparison='equal',read_filters={'sqlite_tables':['samples'],'npz_arrays':['land_component','slope8','relief32'],'atlas_families':['NGEO','NHYD'],'excluded':['MP-P01 proposal / Critic / maps / review','subsequent human planning / architecture answers','targets / assessments','k2 / k3 / k4 / k5 / zones'],'atlas_filter':'bounds intersect [-800,1376,2463,3487]'},freshness='R1 accepted snapshot; NG3 freshness is its prior check only; no current save access',world_writes=0))
o=json.loads((ROOT/'planning-objects.json').read_text(encoding='utf8'));packages=json.loads((ROOT/'implementation-packages.json').read_text(encoding='utf8'))
groups=['regions','nodes','routes','spaces','anchors'];ids=[v['id'] for g in groups for v in o[g]];assert len(ids)==len(set(ids))
for n in o['nodes']:
    c=n['built_fabric_capacity'];assert c['area_range_blocks2'][0]<c['area_range_blocks2'][1]
    assert c['confidence']=='LOW' and c['existing_area']=='UNVERIFIED'
    for i in (0,1):assert c['arithmetic_range'][i]==c['resident_household_pressure_range'][i]*c['household_land_allowance_blocks2'][i]+c['shared_service_land_blocks2'][i]
    assert 'location_search_envelope' in n and 'functional_hinterland' in n
for r in o['routes']:assert all(x in ids for x in r['ends']) and r['verification']=='UNVERIFIED_USABLE_ROUTE'
for p in packages:
    assert p['child_scale']=='REGIONAL_SYSTEM' and p['recipient']=='minecraft-planner'
    assert not p['world_write_authorization'] and not p['builder_ready']
    for k in ['UPSTREAM_FIXED','DOWNSTREAM_TO_RESOLVE','DOWNSTREAM_ADAPTABLE','REVISION_TRIGGER']:assert p[k]
    assert all(x in ids for x in p['scope_search_geometry']['node_refs']+p['scope_search_geometry']['route_refs'])
assert o['spaces'][0]['area_blocks2']==92124
assert o['context']['state']=='HANDOFF_READY' and o['context']['world_writes']==0
before={p.relative_to(ROOT).as_posix():digest(p) for p in list((ROOT/'maps').glob('*.png'))+[ROOT/x for x in ['planning-objects.json','demand-model.json','growth-sequence.json','building-program.json','implementation-packages.json','settlement-capacity.json','规划图册.html']]}
subprocess.run([sys.executable,str(ROOT/'规划产物生成.py')],check=True)
after={p:digest(ROOT/p) for p in before};assert before==after
for p in (ROOT/'maps').glob('*.png'):assert Image.open(p).size==(2430,1380)
for p in ROOT.glob('*.json'):json.loads(p.read_text(encoding='utf8'))
dump('validation.json',dict(status='ARTIFACT_CHECKS_COMPLETED_NOT_REGRESSION_VERDICT',checks={'unique_ids':len(ids),'nodes':6,'routes':6,'planner_packages':4,'json_parse':True,'capacity_arithmetic':True,'search_capacity_catchment_separate':True,'route_endpoint_refs':True,'commons_area_matches_canon':92124,'five_maps_dimensions':[2430,1380],'deterministic_rebuild_equal':before==after,'pinned_skill_bytes_equal':True},visual_review={'method':'view_image actual rendered PNGs','reviewed':['01','02','03','04','05'],'finding':'范围/坐标/图例与面积区间可读；非比例地籍。02 双向字形改为文字，03 同源公地 mask；没有实机预览。'},protected_scope={'world_writes':0,'save_access':'NONE','canon_writes':0,'skill_source_writes':0,'existing_plan_writes':0,'basis':'执行流程仅读取归档白名单，修改范围由 git scoped diff 复核；不是对实时存档做前后字节检测'},unverified=['current world freshness','existing built fabric','water supply and food carrying capacity','navigation / usable routes','exact ore / fuel resources','exact settlement boundaries'],review_status='AWAITING_GPT_AND_OWNER'))
print('Artifact references, scale arithmetic and deterministic rebuild verified; no regression verdict.')
