"""核验交付一致性；不以计数或布尔规则替模型作规划语义裁决。"""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,v:(R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v=load('设计体素.json');q=load('设计核验.json');b=load('inputs/r3/BDP-01.json');c=load('Builder-owned-closure.json');f=load('Planning-Fidelity-Gate.json')
checks=[]
def check(name,ok):
    checks.append({'check':name,'satisfied':bool(ok)})
    if not ok:raise AssertionError(name)
check('r3 selected',b['package_id']=='BDP-01' and b['package_revision']=='r3')
for d in b['dependencies']:check('dependency hash '+d['file'],sha(R/'inputs/r3'/d['file'])==d['sha256'])
keys={(x['x'],x['y'],x['z']):x for x in v['blocks']}
check('unique native cells',len(keys)==len(v['blocks']))
check('all native state namespace explicit',all(x['state'].startswith('minecraft:') for x in v['blocks']))
for k,x in keys.items():
    s=x['state']
    if ':spruce_door[' in s and 'half=lower' in s:
        check('paired door '+str(k),keys.get((k[0],k[1]+1,k[2]),{}).get('state')==s.replace('half=lower','half=upper'))
    if ':red_bed[' in s and 'part=foot' in s:
        check('paired bed '+str(k),keys.get((k[0],k[1],k[2]+1),{}).get('state')==s.replace('part=foot','part=head'))
check('parcel containment',not q['checks']['outside_parcel'])
check('public clear volume',not q['checks']['public_clear_envelope_intrusions'])
check('18-cell open yard',q['checks']['private_yard_cells']==18 and not q['checks']['yard_above_obstructions'])
check('r3 threshold 132',q['checks']['threshold_top']==q['checks']['required_threshold_top']==132)
check('six static routes clear',len(q['checks']['route_results'])==6 and all(not x['body_obstructions'] and not x['unsupported'] for x in q['checks']['route_results']))
check('not DESIGN_READY',v['status']=='UNFROZEN_DESIGN_WITH_BLOCKERS' and not c['design_ready'])
check('no suite verdict',v['regression_verdict']=='NOT_ASSIGNED' and c['regression_verdict']=='NOT_ASSIGNED')
check('all five conditions recorded',set(x['id'] for x in c['conditions'])=={'U-GROUND','U-HABITABILITY','B-TRANSLATION','B-RAINWATER-PERFORMANCE','B-PLANNING-FIDELITY'})
check('fidelity rechecked r3',f['BDP_revision']=='r3' and f['result']=='UPSTREAM_PLANNING_ISSUE')
check('original resolve_before retained',all(any(y['id']==x['id'] and y['resolve_before']==x['resolve_before'] for y in load('remaining-uncertainty.json')['conditions']) for x in b['known_uncertainty']))
for x in load('revision-currentness.json')['sources']:
    if not x['source'].startswith('https:') and Path(x['source']).exists():check('source unchanged '+x['source'],sha(Path(x['source']))==x['sha256'])
# 在同一输出路径重编译后比较语义产物哈希；图像单独重画，字体环境记录在制图脚本。
names=['设计体素.json','设计几何.json','设计修订.json','地基影响核验.json','雨水性能.json','设计核验.json']
before={n:sha(R/n) for n in names}
subprocess.run([sys.executable,str(R/'冻结候选编译.py')],check=True,capture_output=True)
check('deterministic design rebuild',all(before[n]==sha(R/n) for n in names))
write('validation.json',{'task':'MP-I02B','delivery_validation':'CHECKS_SATISFIED','checks':checks,'rebuild':before,'world_writes':0,'runtime_started':False,'perceptual_review':'Author viewed all 7 final PNGs: plan, section and massing preserved; chimney and water omissions explicitly marked. Not independent review.','architecture_review':'Two single-purpose evidence scripts plus delivery checker; no production module architecture added, no cross-module internals imported. Chinese filenames/comments. Source snapshots kept immutable.','not_certified':['DESIGN_READY','ground capacity','functional flue','rainwater performance','Minecraft runtime collision','whole skill regression']})
files=[p for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts]
write('manifest.json',{'algorithm':'SHA256','files':[{'path':str(p.relative_to(R)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)],'world_writes':0,'state':'UNFROZEN_DESIGN_WITH_BLOCKERS'})
print(json.dumps({'delivery_checks':len(checks),'failures':0,'manifest_files':len(files),'design_ready':False}))
