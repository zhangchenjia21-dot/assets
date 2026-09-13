"""核对来源字节、规划引用和生成确定性；不把这些检查当语义质量裁判。"""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parent;REPO=R.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load(p):return json.loads((R/p).read_text(encoding='utf8'))
def dump(p,v):(R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
sources=[('SRC-CANON','minecraft/建筑师/world/civilizations/CIV-001/README.md','APPROVED_CANON','文明最低设定；不跟随后续建筑规划链接'),('SRC-PARENT','minecraft/MP-P01R-CIV001/implementation-packages.json','DESIGN_PROPOSAL','仅PACKAGE-03和必要node/route引用；抽取见sources/parent-package.json'),('SRC-OBS','minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/observed.sqlite.gz','OBSERVED','逐列地表、4格植被采样；非当前存档刷新'),('SRC-DERIVED','minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/derived.npz','DERIVED','只使用land_component、slope8、relief32自然数组'),('SRC-ATLAS','minecraft/建筑师/research/natural-geography/NG-3/atlas/objects.jsonl','DERIVED_WITH_MIXED_CONFIDENCE','只取相交NGEO/NHYD，未读取NSITE规划潜力；子集保留原lineage')]
reg=[]
for id,p,authority,use in sources:
 expected=subprocess.check_output(['git','-C',str(REPO),'show','aeded8d91e6af132a139cff5334a3a654d1c2806:'+p])
 assert hashlib.sha256(expected).hexdigest()==sha(REPO/p),p
 reg.append(dict(id=id,path=p,sha256=sha(REPO/p),repository='zhangchenjia21-dot/assets',revision='aeded8d91e6af132a139cff5334a3a654d1c2806',authority=authority,use=use))
for f in sorted((R/'sources/skill').rglob('*.md')):
 reg.append(dict(id='SRC-SKILL' if f.name=='SKILL.md' else 'SRC-REF-'+f.stem,path='skill/codex/minecraft-planner/'+f.relative_to(R/'sources/skill').as_posix(),sha256=sha(f),repository='zhangchenjia21-dot/Vibe-Coding',revision='886a8f3c4a06c9292080a0642636f31b90849a3b',authority='SKILL_INSTRUCTION',local_copy=f.relative_to(R).as_posix()))
dump('sources/source-register.json',reg)
plan=load('planning-data.json');packages=load('implementation-packages.json');nodes=plan['nodes'];ids={n['id'] for n in nodes};routes={q['id'] for q in plan['routes']}
assert len(ids)==4 and len(packages)==3
for n in nodes:
 c=n['built_fabric_capacity'];assert c['arithmetic_range']==c['area_range_blocks2'];assert abs(sum(n['profile']['surface_ratio'].values())-1)<.001
 assert n['profile']['land_columns']>c['area_range_blocks2'][1]
for q in plan['routes']:assert all(v in ids or v=='PARENT:NODE-04' for v in q['ends'])
for p in packages:
 assert p['child_scale']=='SETTLEMENT' and not p['world_write_authorization'] and not p['builder_ready']
 assert set(p['scope_node_refs'])<=ids and set(p['flow_refs'])<=routes
 for k in ['upstream_fixed','downstream_to_resolve','downstream_adaptable','revision_triggers','surface_specific_requirement']:assert p[k]
assert [sum(n['built_fabric_capacity']['area_range_blocks2'][i] for n in nodes[:2]) for i in range(2)]==[6000,14000]
assert plan['capacity_aggregation']['mutually_exclusive']==['NODE-03','NODE-04']
# 只重跑本轮生成脚本，对比确定性的JSON和PNG，不修改任何上游或世界。
files=[R/'planning-data.json',R/'implementation-packages.json',R/'evidence/candidate-profiles.json',*sorted((R/'maps').glob('*.png'))]
before={p.name:sha(p) for p in files}
subprocess.run([sys.executable,str(R/'规划产物生成.py')],check=True)
after={p.name:sha(p) for p in files};assert before==after
status=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain','-z','-uall'],encoding='utf8')
assert all(line[3:].startswith('minecraft/MP-P02R-EAST/') for line in status.split('\0') if line),status
dump('evidence/validation.json',dict(structural_checks='COMPLETED_NO_ASSERTION_FAILURE',deterministic_rebuild_files=len(files),unintended_rebuild_diff=0,north_capacity_arithmetic=[6000,14000],south_alternatives_not_summed=True,source_sha256_recorded=True,world_writes=0,world_verification='NOT_OPENED; no world API or save access used',semantic_quality='NOT_DETERMINED_BY_SCRIPT',live_route_water_substrate_fabric='UNVERIFIED',maps_visually_reviewed=['地形与区域交换关系','地表差异与候选规模','植被采样与开放地压力','候选区域同范围比较','关系线地形探针']))
dump('artifact-sha256.json',{p.relative_to(R).as_posix():sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='artifact-sha256.json'})
print('source, references, arithmetic, exclusive branches and deterministic rebuild verified')
