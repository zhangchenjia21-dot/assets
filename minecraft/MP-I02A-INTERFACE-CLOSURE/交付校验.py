"""验证归档一致性与有限几何事实；不替代 GPT + Owner 的回归裁决。"""
from pathlib import Path
import hashlib, json, sys

R = Path(__file__).resolve().parent
def read(f):
    return json.loads((R/f).read_text(encoding='utf-8-sig'))
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

old=read('inputs/BDP-01-r1.json')
b=read('BDP-01.json')
ii=read('interface-baselines.json')['interfaces']
ss=read('external-service-interfaces.json')['services']
checks={}
checks['embedded_interfaces_match']=b['interface_baselines']==ii
checks['embedded_services_match']=b['external_service_interfaces']==ss
checks['dependency_hashes_match']=all(digest(R/d['file'])==d['sha256'] for d in b['dependencies'])
keys=['scope','why','design_context','planning_causal_context','spatial_envelope','boundary_semantic','required_adjacency','required_access','program_requirements','planner_fixed','builder_adaptable','historical_growth_stage','architecture_kit_requirements']
checks['unaffected_BDP_fields_unchanged']=all(b[k]==old[k] for k in keys)
checks['unaffected_interfaces_unchanged']=all(i==next(x for x in old['interface_baselines'] if x['interface_id']==i['interface_id']) for i in ii if i['interface_id'] not in ['R2-IF-LANE-04','R2-IF-THRESHOLD-1'])
checks['unaffected_services_unchanged']=all(s==next(x for x in old['external_service_interfaces'] if x['service_id']==s['service_id']) for s in ss if s['service_id']!='R2-S1-RAINWATER')
lane=next(i for i in ii if i['interface_id']=='R2-IF-LANE-04')
threshold=next(i for i in ii if i['interface_id']=='R2-IF-THRESHOLD-1')
patch={(x,z) for x in range(756,758) for z in range(1634,1636)}
parcel={tuple(c) for c in b['spatial_envelope']['cells']}
checks['patch_inside_existing_lane_mask']=patch <= {tuple(c) for c in lane['local_geometry']['cells']}
checks['patch_does_not_occupy_parcel']=not patch & parcel
checks['private_contact_inside_apron']=[757,1633] in threshold['local_geometry']['cells']
rows={tuple(row[:2]):row for row in read('evidence/公共接口地表切片.json')['columns']}
checks['five_contact_columns_observed_surface_132']=all(rows[c][3]+1==132 for c in patch|{(757,1633)})
checks['local_patch_minimum_dimensions']=758-756==2 and 1636-1634==2 and 135-132==3
checks['contact_face_shares_boundary']=threshold['local_contact_control']['shared_contact_face']=={'x':[757,758],'z':1634,'surface_y':132}
reg=read('closure-register.json')
checks['upstream_holds_remain_before_freeze']=all(next(i for i in reg['issues'] if i['id']==k)['status']=='UNRESOLVED' and next(i for i in reg['issues'] if i['id']==k)['resolve_before']=='BEFORE_DESIGN_FREEZE' for k in ['U-PUBLIC','U-RAINWATER'])
checks['other_issue_status_and_time_preserved']=all(all(i.get(k)==j.get(k) for k in ['status','resolve_before','owner']) for i in reg['issues'] if i['id'] not in ['U-PUBLIC','U-RAINWATER'] for j in read('inputs/MP-I01R-issues.json')['issues'] if i['id']==j['id'])
checks['no_false_readiness_or_authorization']=b['builder_handoff_readiness']=='CONCEPT_DESIGN_READY' and b['world_write_authorization'] is False and reg['regression_verdict']=='NOT_ASSIGNED'
checks['downstream_marked_stale']=b['downstream_design_status']['status']=='STALE_FOR_FIDELITY_REVIEW' and b['downstream_design_status']['original_design_modified'] is False
if '--verify-sources' in sys.argv:
    local=[r for r in read('source-provenance.json')['records'] if not r['source'].startswith('https:')]
    checks['registered_local_sources_unchanged']=all(digest(Path(r['source']))==r['sha256'] for r in local)
result={'test':'MP-I02A','check_scope':'artifact integrity and local patch geometry only','checks':checks,'checks_count':len(checks),'discrepancies':sum(not v for v in checks.values()),'regression_verdict':'NOT_ASSIGNED','world_writes':0,'not_verified':['continuous two-sided public tie-ins and turn clearance','rainwater quantitative capacity, recovery and overflow safety','Builder fidelity under r2','actual public appointment / rights / world execution']}
(R/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest={'test':'MP-I02A','revision':'r1','regression_verdict':'NOT_ASSIGNED','review_status':'AWAITING_GPT_AND_OWNER','world_writes':0,'files':[{'file':str(p.relative_to(R)).replace('\\','/'),'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifest.json']}
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
if result['discrepancies']:
    raise SystemExit(1)
