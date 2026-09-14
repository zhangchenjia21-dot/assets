"""从有界输入快照编译 BDP-01 r3；只写脚本所在目录，不访问存档或修改来源。"""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))

def emit(name, value):
    path = ROOT/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

def sha(name):
    return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()

b = read('inputs/BDP-01-r2.json')
parent = copy.deepcopy(b)
ib = read('inputs/interface-baselines-r2.json')
sb = read('inputs/external-service-interfaces-r2.json')
interfaces = ib['interfaces']
services = sb['services']
assert interfaces == b['interface_baselines']
assert services == b['external_service_interfaces']
lane = next(i for i in interfaces if i['interface_id']=='R2-IF-LANE-04')
threshold = next(i for i in interfaces if i['interface_id']=='R2-IF-THRESHOLD-1')
common = next(i for i in interfaces if i['interface_id']=='R2-IF-COMMON-EDGE')

# 用轴向折线与半宽1的闭合方形作Minkowski和。每个折点都保留完整2×2转角，
# 因方形包含半径1的圆，能给出连续2格水平扫掠证据，而非用相邻格数代替净宽。
spine = [[751,1637],[756,1637],[756,1635],[760,1635],[760,1634],[765,1634],[765,1633],[769,1633],[769,1632]]
rectangles = []
cells = set()
for a, z in zip(spine, spine[1:]):
    assert a[0]==z[0] or a[1]==z[1]
    rect = {'x':[min(a[0],z[0])-1,max(a[0],z[0])+1], 'z':[min(a[1],z[1])-1,max(a[1],z[1])+1]}
    rectangles.append(rect)
    cells.update((x,t) for x in range(*rect['x']) for t in range(*rect['z']))
original_lane = {tuple(c) for c in lane['local_geometry']['cells']}
original_common = {tuple(c) for c in common['local_geometry']['cells']}
parcel = {tuple(c) for c in b['spatial_envelope']['cells']}
assert cells <= original_lane | original_common
assert not cells & parcel
surface = read('evidence/局部地表事实.json')
facts = {tuple(r[:2]):r for r in surface['columns']}

# Y是行走顶面；折线标高是DESIGN_PROPOSAL，不伪装成已有铺装或Minecraft碰撞面。
# 端部对应原LANE-04控制点，中间保留门前Y132平台；不用统一削平整条前沿。
profile = [[750,131],[754,131],[755,132],[760,132],[762,133],[767,133],[768,134],[770,134]]
def height(x):
    for (left,low),(right,high) in zip(profile,profile[1:]):
        if left<=x<=right:
            return low+(high-low)*(x-left)/(right-left)
    raise ValueError('Outside local profile')

per_cell = []
for x,z in sorted(cells):
    h0,h1 = height(x),height(x+1)
    ground = facts[x,z][3]
    assert max(abs(h0-(ground+1)),abs(h1-(ground+1)))<=1
    per_cell.append({'x':x,'z':z,'observed_ground_block_y':ground,'observed_surface_y':ground+1,
                     'design_surface_corner_y':[h0,h1,h1,h0],
                     'corner_order':['x,z','x+1,z','x+1,z+1','x,z+1'],
                     'design_surface_center_y':height(x+0.5),
                     'protected_vertical_interval':[min(h0,h1),max(h0,h1)+3],
                     'public_source':'LANE-04' if (x,z) in original_lane else 'COMMON-EDGE'})

corridor = {
    'baseline_id':'I02A2-PUBLIC-BDP01','revision':'r1','authority':'DESIGN_PROPOSAL',
    'scope':'BDP-01 frontage only: original LANE-04 control points (751,1637) to (769,1632)',
    'coordinate_semantic':'World X/Z; cells are complete unit squares, closed shared edges; Y is walking surface height.',
    'spine':spine,'sweep_kernel':{'metric':'L_INFINITY','half_width':1,'turns':'FULL_2_BY_2_SQUARE','caps':'SQUARE'},
    'protected_horizontal_geometry':{'type':'EXACT_UNION_OF_CLOSED_RECTANGLES','rectangles':rectangles,'cells':[list(c) for c in sorted(cells)]},
    'minimum_horizontal_clear':2,'minimum_vertical_clear':3,
    'continuous_width_proof':'For every point on the continuous spine, its closed [-1,1]^2 translate lies in the rectangle union. This contains the Euclidean radius-1 disk, including at every turn. This is a proposal clearance proof, not runtime movement.',
    'design_surface':{'type':'CONTINUOUS_PIECEWISE_LINEAR_HEIGHT_FIELD','formula':'Y=H(X), independent of Z; linearly interpolate profile breakpoints','profile_x_y':profile,'per_cell':per_cell,'authority':'DESIGN_PROPOSAL','native_translation':'A planning surface, not native block geometry. Detailed public steps/paving remain implementation authorship; any realization must retain minimum clear width/height and the fixed contact/port levels.'},
    'vertical_protection':'For each cell reserve [min(corner surface Y), max(corner surface Y)+3]. Only the declared walking surface/support may occupy below its local H(X); no door, roof, storage, railing or discharge may occupy the above-surface clearance.',
    'ports':[
        {'id':'WEST','point':[751,1637],'surface_y':131,'cap_square':{'x':[750,752],'z':[1636,1638]},'source':'r1 LANE-04 first original control point; observed surface131'},
        {'id':'EAST','point':[769,1632],'surface_y':134,'cap_square':{'x':[768,770],'z':[1631,1633]},'source':'r1 LANE-04 third original control point; observed surface134'}
    ],
    'threshold':{'private_cell':[757,1633],'shared_face':{'x':[757,758],'z':1634,'surface_y':132},'public_connection_axis':[[757.5,1634],[757.5,1635]],'connection_surface_y':132,'private_entry_clear_width':1,'public_through_clear_width':2,'semantic':'One-block private entrance opens directly onto the protected public strip; it does not reduce the continuous two-block through corridor. No private door is redesigned.'},
    'adjustment_envelope':{'horizontal_shift':0,'parcel_expansion':0,'private_contact_surface_delta':0,'port_surface_delta':0,'protected_surface_delta':0,'rule':'This revision fixes the continuous planning control surface and corridor. Builder may adjust only private doors, apron and internal rise within existing parcel; no public obstruction. Public realization must satisfy this baseline. Any incompatible local adjustment returns a new interface revision.'},
    'coordination':{'role':'PUBLIC-COORDINATOR','kind':'TASK_LOCAL_PLANNING_COORDINATION_ROLE','assigned_by':'MP-I02A2 task boundary','responsibility':'Own this public baseline, preserve port/threshold continuity, coordinate public detailed realization and accept minimal interface issues.','actual_institution_appointment_required_for_planning_freeze':False,'easement_approval_required_for_planning_freeze':False,'land_easement_world_write_resolve_before':'BEFORE_WORLD_WRITE'},
    'runtime_movement_verified':False,'world_write_authorization':False,
    'boundary_of_claim':'Local geometric continuity from threshold to both existing LANE-04 control points is specified. Does not certify construction, native movement, the rest of LANE-04, LANE-01/02 operations or actual land rights.'
}
emit('evidence/公共通行冻结基线.json',corridor)

for i in [lane,threshold]:
    i['interface_revision']='r3'
    i['status']='PLANNING_BASELINE_FIXED_DESIGN_PROPOSAL'
    i['supersedes']={'package':'MP-I02A','interface_id':i['interface_id'],'interface_revision':'r2'}
    i['coordination_owner']='PUBLIC-COORDINATOR / task-local planning coordination role'
    i['planning_coordination']=corridor['coordination']
    i['local_contact_control']={**corridor['threshold'],'continuous_route_status':'PLANNING_BASELINE_FIXED','baseline_ref':'evidence/公共通行冻结基线.json'}
    i['adjustment_envelope']=corridor['adjustment_envelope']
    i['resolve_before']='BEFORE_DESIGN_FREEZE'
    i['planning_interface_state']='CLOSED_AT_PLANNING_LEVEL'
    i['uncertainty']=['Minecraft runtime movement and detailed physical realization unverified; not a missing planning baseline.','Land / easement / world-write authorization remains BEFORE_WORLD_WRITE.']
    i['baseline_dependency']={'file':'evidence/公共通行冻结基线.json','revision':'r1','sha256':sha('evidence/公共通行冻结基线.json')}
lane['inherited_route_geometry']=lane['local_geometry']
lane['local_geometry']={**corridor['protected_horizontal_geometry'],'role':'PROTECTED_PUBLIC_CLEAR_ENVELOPE','spine':spine,'scope':corridor['scope'],'semantic':'r3 replaces only this BDP-01 frontage local clear path; full r1 route retained as lineage/context, not the active local clear proof.'}
lane['inherited_observed_section']={k:lane['height_or_section_baseline'][k] for k in ['authority','samples','fields','existing_surface_y_rule']}
lane['height_or_section_baseline']=corridor['design_surface']
lane['minimum_clear_requirement']={'horizontal_blocks':2,'vertical_blocks':3,'semantic':'Continuous Minkowski sweep, including turns and end caps; see exact rectangle union and per-cell protected volume.','status':'PLANNING_PROPOSAL_GEOMETRY_SPECIFIED_NOT_RUNTIME_CERTIFIED'}
threshold['inherited_observed_section']={k:threshold['height_or_section_baseline'][k] for k in ['per_column','fields']}
threshold['height_or_section_baseline']={'authority':'DESIGN_PROPOSAL','contact_surface_y':132,'public_surface_ref':'evidence/公共通行冻结基线.json','private_surface_rule':'Private adaptation belongs to Builder; shared face remains Y132.'}

rain = next(s for s in services if s['service_id']=='R2-S1-RAINWATER')
rain_id=rain['service_id']
rain.clear()
rain.update({
    'service_id':rain_id,'service_revision':'r3','service_type':'RAINWATER','status':'PLANNING_INTERFACE_CLOSED_BUILDER_PERFORMANCE_OPEN',
    'supersedes':{'package':'MP-I02A','service_revision':'r2'},
    'cross_boundary_discharge':'FORBIDDEN_UNLESS_FUTURE_INTERFACE_REVISION',
    'public_receiving_obligation':'NONE',
    'builder_responsibility':'DESIGN_AND_PROVE_PARCEL_LOCAL_CLOSED_STRATEGY',
    'resolve_before':'BEFORE_DESIGN_FREEZE',
    'interface_location_or_ref':{'parcel':'BDP-01.json#spatial_envelope','boundary_semantic':'CELL_CENTER_MASK as inherited; full occupied columns, no edge tolerance','threshold':'R2-IF-THRESHOLD-1 r3 is access and no-discharge boundary only; NOT an outfall'},
    'upstream_or_downstream_owner':'BDP-01 Builder owns parcel-local design and proof; PUBLIC-COORDINATOR owns the public no-discharge boundary only.',
    'neighbor_or_public_responsibility':'No receiving, conveyance, overflow or clearing commitment; no public outfall dependency.',
    'allowed_local_adjustment':'Within original parcel, preserving household program, independent yard, foundation protections and public corridor. Exact roof/gutter/pipe/retention layout remains Builder authorship.',
    'builder_to_prove':['Define justified design-event and failure assumptions; Planner supplies no invented rain or infiltration data.','Demonstrate collection, retention, recovery and safe failure within parcel; finite dry containers alone are not proof.','Demonstrate no boundary discharge or public/neighbor harm; no unproven external collection operation or assumed rock infiltration.'],
    'engineering_condition_id':'B-RAINWATER-PERFORMANCE',
    'return_protocol':'If the parcel-local strategy cannot be proved without violating fixed program/boundaries, return a new UPSTREAM_PLANNING_ISSUE with attempted bounded adaptations and minimum requested interface revision. Never silently create an outfall.',
    'planning_interface_state':'CLOSED_AT_PLANNING_LEVEL','performance_state':'UNRESOLVED_BUILDER_RESPONSIBILITY',
    'world_write_authorization':False
})
emit('interface-baselines.json',{'revision':'r3','revision_package':'MP-I02A2-r1','source_plan_revision':'MP-P05R2-r1','authority':'DESIGN_PROPOSAL','scope':'BDP-01 only','interfaces':interfaces})
emit('external-service-interfaces.json',{'revision':'r3','revision_package':'MP-I02A2-r1','source_plan_revision':'MP-P05R2-r1','scope':'BDP-01 only','services':services})

reg=read('inputs/closure-register-r1.json')
remaining=[i for i in reg['issues'] if i['id'] not in ['U-PUBLIC','U-RAINWATER']]
for i in remaining:
    i.pop('handling_in_MP_I02A',None)
    i['handling_in_MP_I02A2']='UNRESOLVED_STATUS_PRESERVED; outside planning-interface closure scope'
reg={
    'test':'MP-I02A2','revision':'r1','package':'BDP-01','package_revision':'r3',
    'authority':'DESIGN_PROPOSAL','regression_verdict':'NOT_ASSIGNED','review_status':'AWAITING_GPT_AND_OWNER','world_writes':0,
    'planning_interface_closures':[
        {'id':'U-PUBLIC','status':'CLOSED_AT_PLANNING_LEVEL','resolve_before':'BEFORE_DESIGN_FREEZE','evidence':'evidence/公共通行冻结基线.json','basis':'50-cell exact public sweep, connected turns and fixed local continuous per-cell design surface. Task-local coordination role is sufficient under Owner task boundary.','residual':'Runtime/detail implementation and real rights remain outside this planning closure.'},
        {'id':'U-RAINWATER','status':'CLOSED_AT_PLANNING_LEVEL','resolve_before':'BEFORE_DESIGN_FREEZE','evidence':'external-service-interfaces.json#R2-S1-RAINWATER','basis':'No cross-boundary discharge and no public receiving obligation; Builder owns parcel-local closed design/proof.','residual':'B-RAINWATER-PERFORMANCE remains open; no hydraulic success is asserted.'}
    ],
    'remaining_conditions':remaining+[
        {'id':'B-RAINWATER-PERFORMANCE','origin_issue':'U-RAINWATER','status':'UNRESOLVED','owner':'BDP-01 Builder','resolve_before':'BEFORE_DESIGN_FREEZE','minimum_closure':'Design and prove parcel-local collection/retention/recovery/safe failure; or return new UPSTREAM_PLANNING_ISSUE if infeasible.','engineering_scope':'Not a Planner receiving-interface HOLD.'},
        {'id':'B-PLANNING-FIDELITY','status':'NOT_RECHECKED','owner':'BDP-01 Builder','resolve_before':'BEFORE_DESIGN_FREEZE','minimum_closure':'Consume BDP-01 r3 and prove design fidelity to revised public and rainwater baselines; no gate result assigned by Planner.'}
    ],
    'planning_holds':[],
    'builder_design_state':'STALE_FOR_FIDELITY_REVIEW; NOT DESIGN_READY',
    'stop_rule':'Stop after archive and delivery; GPT + Owner review; no regression PASS/FAIL.'
}
emit('closure-register.json',reg)

b['package_revision']='r3'
b['revision_package']='MP-I02A2-r1'
b['builder_handoff_readiness']='DESIGN_FREEZE_READY'
b['readiness_reason']='Planner planning-interface baseline is locally resolvable under MP-I02A2 authority. Builder may attempt freeze only after its own ground, habitability, translation, parcel-local rainwater performance and Planning Fidelity conditions. This is not building DESIGN_READY or a regression verdict.'
b['interface_baselines']=interfaces
b['external_service_interfaces']=services
b['interface_revisions']={i['interface_id']:i['interface_revision'] for i in interfaces}
b['external_service_revisions']={s['service_id']:s.get('service_revision','r1') for s in services}
b['known_uncertainty']=reg['remaining_conditions']
b['planning_interface_closures']=reg['planning_interface_closures']
b['planning_role_semantics']=corridor['coordination']
b['interface_interpretation_precedence']='Active r3 local geometry/section replaces r2 local contact control. inherited_* fields and input snapshots are provenance only. PUBLIC-COORDINATOR means task-local planning role for this handoff; historic actual-appointment wording in unchanged r1 objects is not a planning freeze prerequisite. Real rights remain BEFORE_WORLD_WRITE.'
b['shared_space_service_relations']='Common/public masks remain protected. Use r3 public baseline and no-discharge rainwater contract. Non-rainwater service reservations and their existing timing remain unchanged.'
b['downstream_design_status']={'design':'MP-I01R / BDP-01 concept r1','status':'STALE_FOR_FIDELITY_REVIEW','reason':'Consumed r1; MP-I02A r2 and MP-I02A2 r3 require new fidelity check. No design changes in this task.','original_design_modified':False,'building_design_ready':False,'builder_next_step':'Close remaining design conditions and run its own Planning Fidelity Gate against r3.'}
b['dependencies']=[{'file':f,'sha256':sha(f),'revision':'r3' if f in ['interface-baselines.json','external-service-interfaces.json'] else 'r1'} for f in ['interface-baselines.json','external-service-interfaces.json','closure-register.json','evidence/公共通行冻结基线.json','evidence/局部地表事实.json']]
b['source_refs']=['provenance.json','inputs/BDP-01-r2.json','inputs/CIV-001-Canon.md','inputs/CIV-001-Architecture-Grammar.md']
emit('BDP-01.json',b)
emit('revision-lineage.json',{
    'revision_package':'MP-I02A2-r1','parent_package':'MP-I02A / BDP-01 r2','source_plan_revision':'MP-P05R2-r1','package_revision':'r3',
    'source_parent_revision_lineage_sha256':sha('inputs/revision-lineage-r1.json'),
    'changed_objects':[{'id':s,'from':'r2','to':'r3'} for s in ['BDP-01','R2-IF-LANE-04','R2-IF-THRESHOLD-1','R2-S1-RAINWATER']],
    'unchanged_objects':[i['interface_id'] for i in interfaces if i not in [lane,threshold]]+[s['service_id'] for s in services if s!=rain],
    'new_baseline':'I02A2-PUBLIC-BDP01 r1',
    'application_scope':'BDP-01 local overlay only; not a replacement of MP-P05R2, other packages or other designs.',
    'downstream':b['downstream_design_status'],
    'world_write_authorization':False,'regression_verdict':'NOT_ASSIGNED'
})
print('Compiled BDP-01 r3; planning interfaces closed; Builder conditions remain open; verdict NOT_ASSIGNED.')
