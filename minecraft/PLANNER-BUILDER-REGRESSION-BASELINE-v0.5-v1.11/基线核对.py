"""只读核对Git归档与汇总记录；不运行原测试、不读取世界、不自动裁定语义质量。"""
from pathlib import Path
import argparse, hashlib, json, subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--assets',required=True)
parser.add_argument('--vibe',required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parent
index=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))
baseline=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
source=index['source_commit']; checks=[]
def git(repo,*args):
    return subprocess.check_output(['git','-C',repo,*args])
def blob(path):return git(args.assets,'show',source+':'+path)
def obj(path):return json.loads(blob('minecraft/'+path).decode('utf-8-sig'))
def check(name,value):
    checks.append({'name':name,'satisfied':bool(value)})
    if not value:raise AssertionError(name)
for item in index['files']:
    data=blob(item['path'])
    check('evidence SHA256: '+item['path'],hashlib.sha256(data).hexdigest()==item['sha256'])
    check('evidence blob: '+item['path'],git(args.assets,'rev-parse',source+':'+item['path']).decode().strip()==item['git_blob'])
check('15 existing reviews',sum(x['path'].endswith('/Independent Review.md') for x in index['files'])==15)
for v in index['tested_versions']:
    data=git(args.vibe,'show',v['source_commit']+':'+v['path'])
    check('fixed Skill/contract hash: '+v['name'],hashlib.sha256(data).hexdigest()==v['sha256_git_bytes'])
    check('current Skill/contract unchanged: '+v['name'],git(args.vibe,'show','HEAD:'+v['path'])==data)
for d,a,b,n in [('MP-P01R-CIV001','POLITY_TERRITORY','REGIONAL_SYSTEM',4),('MP-P02R-EAST','REGIONAL_SYSTEM','SETTLEMENT',3),('MP-P03-NORTH-ROCK-TERRACE','SETTLEMENT','DISTRICT',3),('MP-P04-WEST-APPROACH','DISTRICT','URBAN_ENSEMBLE',3)]:
    packages=obj(d+'/implementation-packages.json')
    check('recursive scale/recipient: '+d,len(packages)==n and all(p['parent_scale']==a and p['child_scale']==b and p['recipient']=='minecraft-planner' and not p['builder_ready'] and not p['world_write_authorization'] for p in packages))
failed=obj('MP-P05R-NORTH-FRONTAGE-ENSEMBLE/planning-data.json')
check('P05R failure retained as observed',failed['state']=='SCOPED' and failed['builder_ready'] is True and baseline['historical_failure_retained']['verdict']=='FAIL_MODEL_EXECUTION')
packages=obj('MP-P05R2-NORTH-FRONTAGE-ENSEMBLE/builder-design-packages.json')['packages']
p=next(x for x in packages if x['package_id']=='BDP-01')
check('P05R2 concrete handoff fields',p['package_revision']=='r1' and p['builder_handoff_readiness']=='CONCEPT_DESIGN_READY' and p['boundary_semantic']['horizontal']=='CELL_CENTER_MASK' and bool(p['interface_baselines']) and bool(p['external_service_interfaces']) and bool(p['dependencies']))
for d,revision,readiness in [('MP-I02A-INTERFACE-CLOSURE','r2','CONCEPT_DESIGN_READY'),('MP-I02A2-FREEZE-BASELINE','r3','DESIGN_FREEZE_READY')]:
    p=obj(d+'/BDP-01.json');lineage=obj(d+'/revision-lineage.json')
    check('revision/readiness: '+d,p['package_revision']==revision and p['builder_handoff_readiness']==readiness and lineage['downstream']['status']=='STALE_FOR_FIDELITY_REVIEW')
q=obj('MP-I02B-DESIGN-FREEZE/Builder-owned-closure.json');f=obj('MP-I02B-DESIGN-FREEZE/Planning-Fidelity-Gate.json');v=obj('MP-I02B-DESIGN-FREEZE/设计核验.json');w=obj('MP-I02B-DESIGN-FREEZE/雨水性能.json')
check('I02B legitimately unfrozen',q['design_ready'] is False and q['building_state']=='UNFROZEN_DESIGN_WITH_BLOCKERS')
check('I02B actual Fidelity issue',f['BDP_revision']=='r3' and f['result']=='UPSTREAM_PLANNING_ISSUE' and f['issue_id']=='MP-I02B-UPI-RAIN-01' and w['status']=='UPSTREAM_PLANNING_ISSUE')
check('I02B recorded static evidence',v['checks']['native_state_count']==564 and not v['checks']['outside_parcel'] and not v['checks']['public_clear_envelope_intrusions'] and v['checks']['private_yard_cells']==18 and v['checks']['threshold_top']==132 and sum(x['samples'] for x in v['checks']['route_results'])==806)
check('three status domains separated',baseline['core_regression_suite']=='PASS_WITH_NOTES' and not baseline['design_ready'] and not baseline['world_write_authorization'] and not baseline['production_construction_authorized'])
check('positive transition limit retained',baseline['positive_design_ready_transition']=='NOT_DEMONSTRATED')
check('no world writes',baseline['world_writes']==q['world_writes']==v['world_writes']==0)
report=(root/'总回归报告.md').read_text(encoding='utf-8')
check('mandatory report sections present',all(x in report for x in ['Tested Versions','Regression Scope','L0 → L4','Planning Fidelity','Builder Design Freeze behavior','Known limitations','Production usage recommendation','Stable baseline declaration']))
result={'validation_scope':'Read-only reconciliation of archived facts, source hashes and baseline metadata; NOT re-execution of original regression tests or semantic quality scoring','source_commit':source,'check_count':len(checks),'unsatisfied':0,'checks':checks,'world_writes':0,'runtime_started':False,'new_independent_review_performed':False,'core_verdict_basis':'Model synthesis of existing Independent Reviews, especially MP-I02B Final suite interpretation; not generated from check count'}
(root/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'checks':len(checks),'unsatisfied':0,'world_writes':0}))
