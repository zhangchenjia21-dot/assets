"""外围归档检查：记录来源字节、复算交接引用与确定性；不作为规划语义判定器。"""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parent;REPO=R.parents[1];ENGINE=R.parents[3];C=ENGINE/'MP-P03-cache'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def load(p):return json.loads((R/p).read_text(encoding='utf8'))
def dump(p,v):(R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
revision='27db0c35fe8ef43244f8eda31559e8d9cc52f42d';skill=(R/'sources/skill-revision.txt').read_text(encoding='utf-8-sig').strip()
sources=[]
for id,p,authority,use in [('SRC-CANON','minecraft/建筑师/world/civilizations/CIV-001/README.md','APPROVED_CANON','只用批准的最低文明设定，不读取后续聚落答案'),('SRC-PARENT','minecraft/MP-P02R-EAST/implementation-packages.json','PARENT_PLANNING_PROPOSAL','仅PACKAGE-01'),('SRC-PARENT-REFS','minecraft/MP-P02R-EAST/planning-data.json','PARENT_PLANNING_PROPOSAL','仅NODE-01及父包ROUTE-01/02必要接口')]:
 raw=subprocess.check_output(['git','-C',str(REPO),'show',revision+':'+p]);assert hashlib.sha256(raw).hexdigest()==sha(REPO/p)
 sources.append(dict(id=id,repository='zhangchenjia21-dot/assets',revision=revision,path=p,sha256=sha(REPO/p),authority=authority,use=use))
for p in sorted((R/'sources/skill').rglob('*.md')):
 sources.append(dict(id='SRC-SKILL' if p.name=='SKILL.md' else 'SRC-REF-'+p.stem,repository='zhangchenjia21-dot/Vibe-Coding',revision=skill,path='skill/codex/minecraft-planner/'+p.relative_to(R/'sources/skill').as_posix(),sha256=sha(p),authority='SKILL_INSTRUCTION',local_copy=p.relative_to(R).as_posix()))
provenance=load('evidence/world-read-provenance.json');source=Path(provenance['source_path'])
assert provenance['source_before']==provenance['source_after'] and provenance['world_writes']==0
world_final={n:sha(source/n) for n in provenance['source_before']};assert world_final==provenance['source_before'],'SOURCE_CHANGED_SINCE_READ'
assert sha(C/'surface.json')==provenance['raw_sha256']
sources.append(dict(id='SRC-LIVE',authority='OBSERVED',world=provenance['world'],read_utc=provenance['read_utc'],fingerprint_ref='evidence/world-read-provenance.json',raw_cache_sha256=provenance['raw_sha256'],method='只读源文件→字节一致副本→既有RegionReader；未启动游戏',freshness='本轮文件快照，非玩家实时视角'))
for p in ['AI-Offline/L3_外交层/存档读取接口.mjs','AI-Offline/L1_器件层/存档区块读取器.mjs','AI-Offline/L1_器件层/存档元数据读取器.mjs']:
 sources.append(dict(id='SRC-READER-'+Path(p).stem,authority='TOOL_IMPLEMENTATION',path=str(ENGINE/p),sha256=sha(ENGINE/p),purpose='现有只读接口；未修改工具'))
dump('sources/source-register.json',sources)
plan=load('planning-data.json');packages=load('implementation-packages.json');ids={d['id'] for d in plan['districts']};pids={p['id'] for p in packages}
assert plan['scale']=='SETTLEMENT' and plan['world_writes']==0
assert [sum(d['area_range'][i] for d in plan['districts']) for i in (0,1)]==[3500,4600]
assert [sum(d['households'][i] for d in plan['districts']) for i in (0,1)]==[12,17]
for p in packages:
 assert p['child_scale']=='DISTRICT' and p['recipient']=='minecraft-planner' and p['scope_ref'] in ids
 assert set(p['cross_package_dependencies'])<=pids and p['id'] not in p['cross_package_dependencies']
 assert not p['world_write_authorization'] and not p['builder_ready']
 for k in ['upstream_fixed','downstream_to_resolve','downstream_adaptable','revision_triggers','expected_outputs']:assert p[k]
assert not load('evidence/route-frontage-overlap.json')
intersections=load('evidence/shallow-void-planning-intersections.json');assert all(i['void_column_overlap']==0 for i in intersections)
assert any(i.get('soil_column_overlap',0)>0 for i in intersections),'不能隐藏未决土面重叠'
files=[R/'planning-data.json',R/'implementation-packages.json',R/'evidence/planning-geometry-metrics.json',*sorted((R/'maps').glob('*.png'))]
before={p.name:sha(p) for p in files}
subprocess.run([sys.executable,str(R/'聚落规划生成.py')],check=True,stdout=subprocess.DEVNULL)
after={p.name:sha(p) for p in files};assert before==after
status=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain','-z','-uall'],encoding='utf8');assert all(s[3:].startswith('minecraft/MP-P03-NORTH-ROCK-TERRACE/') for s in status.split('\0') if s),status
size=sum(p.stat().st_size for p in R.rglob('*') if p.is_file());assert size<15*1024*1024
dump('evidence/validation.json',{'source_hashes_verified':True,'source_world_final_hashes':world_final,'world_writes':0,'world_hash_scope':'仅本轮读取的level.dat与两个region，非全存档逐文件审计','district_count':3,'capacity_sum':[3500,4600],'household_sum':[12,17],'route_frontage_overlap_columns':0,'known_shallow_void_overlap_columns':0,'rebuild_file_count':len(files),'rebuild_byte_diff':0,'bundle_bytes_before_final_manifest':size,'geometry_check_meaning':'仅检查提案表达的一致性，不证明通行、基底安全或规划质量','semantic_review':'AWAITING_GPT_AND_OWNER','unverified':['持续饮水质/量','实机连续移动','深部与完整地基','土地权属/旧路来源','食物/动物供给','污物终端'],'visual_review':'2张当前观察图、2张内部图、3张阶段图与1张剖面图人工检查'})
dump('artifact-sha256.json',{p.relative_to(R).as_posix():sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='artifact-sha256.json'})
print(json.dumps({'validation':'completed','rebuild_files':len(files),'rebuild_diff':0,'world_writes':0,'bundle_bytes':size}))
