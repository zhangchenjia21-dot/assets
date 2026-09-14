"""核对版本、责任分离与连续几何；不产生回归或 Planning Fidelity 裁决。"""
from pathlib import Path
import hashlib,json,sys

R=Path(__file__).resolve().parent
def read(n): return json.loads((R/n).read_text(encoding='utf-8-sig'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(n,d): (R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

b=read('BDP-01.json'); old=read('inputs/BDP-01-r2.json')
c=read('evidence/公共通行冻结基线.json')
ii=read('interface-baselines.json')['interfaces']; ss=read('external-service-interfaces.json')['services']
oldii=old['interface_baselines']; oldss=old['external_service_interfaces']
checks={}
checks['embedded_interfaces_match']=ii==b['interface_baselines']
checks['embedded_services_match']=ss==b['external_service_interfaces']
checks['dependency_hashes_match']=all(digest(R/d['file'])==d['sha256'] for d in b['dependencies'])
checks['baseline_hashes_match']=all(digest(R/i['baseline_dependency']['file'])==i['baseline_dependency']['sha256'] for i in ii if 'baseline_dependency' in i)
keys=['scope','why','design_context','planning_causal_context','spatial_envelope','boundary_semantic','program_requirements','planner_fixed','builder_adaptable','required_access','required_adjacency','architecture_kit_requirements']
checks['causality_program_parcel_preserved']=all(b[k]==old[k] for k in keys)
checks['unaffected_interfaces_preserved']=all(i==next(o for o in oldii if o['interface_id']==i['interface_id']) for i in ii if i['interface_id'] not in ['R2-IF-LANE-04','R2-IF-THRESHOLD-1'])
checks['unaffected_services_preserved']=all(s==next(o for o in oldss if o['service_id']==s['service_id']) for s in ss if s['service_id']!='R2-S1-RAINWATER')

rects=c['protected_horizontal_geometry']['rectangles']; points=c['spine']
exact_rects=[{'x':[min(a[0],z[0])-1,max(a[0],z[0])+1],'z':[min(a[1],z[1])-1,max(a[1],z[1])+1]} for a,z in zip(points,points[1:])]
checks['exact_square_minkowski_sweep']=rects==exact_rects and all(a[0]==z[0] or a[1]==z[1] for a,z in zip(points,points[1:]))
checks['all_turns_have_full_2x2_overlap']=all(min(a['x'][1],z['x'][1])-max(a['x'][0],z['x'][0])>=2 and min(a['z'][1],z['z'][1])-max(a['z'][0],z['z'][0])>=2 for a,z in zip(rects,rects[1:]))
cells={(x,z) for r in rects for x in range(*r['x']) for z in range(*r['z'])}
checks['exact_full_cell_union']=cells=={tuple(v) for v in c['protected_horizontal_geometry']['cells']} and len(cells)==50
pub={tuple(v) for i in oldii if i['interface_id'] in ['R2-IF-LANE-04','R2-IF-COMMON-EDGE'] for v in i['local_geometry']['cells']}
parcel={tuple(v) for v in b['spatial_envelope']['cells']}
checks['within_inherited_public_masks']=cells<=pub
checks['no_private_parcel_overlap']=not cells&parcel
checks['old_four_cell_patch_retained']={(756,1634),(756,1635),(757,1634),(757,1635)}<=cells
checks['threshold_opens_directly_onto_corridor']=(757,1633) in parcel and (757,1634) in cells and c['threshold']['shared_face']=={'x':[757,758],'z':1634,'surface_y':132}
checks['ports_match_original_control_points']=points[0]==[751,1637] and points[-1]==[769,1632]

per=c['design_surface']['per_cell']; pc={(r['x'],r['z']):r for r in per}
checks['every_cell_has_explicit_surface']=set(pc)==cells
checks['shared_cell_edges_are_continuous']=all((x+1,z) not in pc or r['design_surface_corner_y'][1]==pc[x+1,z]['design_surface_corner_y'][0] for (x,z),r in pc.items()) and all((x,z+1) not in pc or r['design_surface_corner_y'][2:]==[pc[x,z+1]['design_surface_corner_y'][1],pc[x,z+1]['design_surface_corner_y'][0]] for (x,z),r in pc.items())
checks['vertical_clearance_at_least_3_everywhere']=all(r['protected_vertical_interval'][1]-max(r['design_surface_corner_y'])>=3 for r in per)
facts={tuple(r[:2]):r for r in read('evidence/局部地表事实.json')['columns']}
checks['observed_values_not_invented']=all(r['observed_ground_block_y']==facts[r['x'],r['z']][3] and r['observed_surface_y']==facts[r['x'],r['z']][3]+1 for r in per)
checks['proposed_surface_within_original_plus_minus_1']=all(abs(h-r['observed_surface_y'])<=1 for r in per for h in r['design_surface_corner_y'])
checks['contact_surface_132']=pc[757,1634]['design_surface_corner_y']==[132]*4 and facts[757,1633][3]+1==132
checks['port_levels_match_observation']=all(p['surface_y']==facts[tuple(p['point'])][3]+1 for p in c['ports'])

rain=next(s for s in ss if s['service_id']=='R2-S1-RAINWATER')
checks['exact_rainwater_responsibility_boundary']=rain['cross_boundary_discharge']=='FORBIDDEN_UNLESS_FUTURE_INTERFACE_REVISION' and rain['public_receiving_obligation']=='NONE' and rain['builder_responsibility']=='DESIGN_AND_PROVE_PARCEL_LOCAL_CLOSED_STRATEGY' and rain['resolve_before']=='BEFORE_DESIGN_FREEZE'
checks['no_reservation_only_or_conditional_old_choice']=all(k not in rain for k in ['conditional_local_strategy','receiving_location','receiving_capacity']) and rain['builder_responsibility']!='RESERVE_INTERFACE_ONLY'
checks['no_actual_appointment_as_planning_prerequisite']=c['coordination']['actual_institution_appointment_required_for_planning_freeze'] is False and c['coordination']['easement_approval_required_for_planning_freeze'] is False
reg=read('closure-register.json')
checks['two_planning_holds_closed_only_at_planning_level']={i['id'] for i in reg['planning_interface_closures']}=={'U-PUBLIC','U-RAINWATER'} and all(i['status']=='CLOSED_AT_PLANNING_LEVEL' for i in reg['planning_interface_closures']) and reg['planning_holds']==[]
checks['rainwater_engineering_still_before_freeze']=any(i['id']=='B-RAINWATER-PERFORMANCE' and i['status']=='UNRESOLVED' and i['resolve_before']=='BEFORE_DESIGN_FREEZE' for i in reg['remaining_conditions'])
oldissues=read('inputs/closure-register-r1.json')['issues']
checks['other_conditions_keep_status_and_timing']=all(any(n['id']==i['id'] and all(n[k]==i[k] for k in ['owner','status','resolve_before']) for n in reg['remaining_conditions']) for i in oldissues if i['id'] not in ['U-PUBLIC','U-RAINWATER'])
checks['fidelity_unassigned_and_design_stale']=b['downstream_design_status']['status']=='STALE_FOR_FIDELITY_REVIEW' and b['downstream_design_status']['building_design_ready'] is False and any(i['id']=='B-PLANNING-FIDELITY' and i['status']=='NOT_RECHECKED' for i in reg['remaining_conditions'])
checks['readiness_separate_from_verdict']=b['builder_handoff_readiness']=='DESIGN_FREEZE_READY' and reg['regression_verdict']=='NOT_ASSIGNED' and b['world_write_authorization'] is False and c['runtime_movement_verified'] is False

if '--verify-sources' in sys.argv:
    records=[r for r in read('provenance.json')['records'] if not r['source'].startswith('https:')]
    checks['registered_local_sources_unchanged']=all(digest(Path(r['source']))==r['sha256'] for r in records)
result={'test':'MP-I02A2','scope':'Artifact and analytic planning-geometry checks only; not runtime or engineering certification','checks':checks,'checks_count':len(checks),'discrepancies':sum(not v for v in checks.values()),'public_cells':len(cells),'world_writes':0,'regression_verdict':'NOT_ASSIGNED','limitations':['No Minecraft movement/native collision verification.','No hydraulic, foundation or habitability proof; Builder conditions stay open.','No real land/easement/world-write permission asserted.','No Planning Fidelity Gate verdict.']}
emit('validation.json',result)
emit('manifest.json',{'test':'MP-I02A2','revision':'r1','world_writes':0,'regression_verdict':'NOT_ASSIGNED','files':[{'file':p.relative_to(R).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts]})
print(json.dumps(result,ensure_ascii=False))
if result['discrepancies']: raise SystemExit(1)
