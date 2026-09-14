"""只编译 MP-I02A 局部修订；输入按 BDP-01 精确选择，绝不写回来源。"""
from pathlib import Path
import json, hashlib, copy

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / '发布/assets'
PLAN = ASSETS / 'minecraft/MP-P05R2-NORTH-FRONTAGE-ENSEMBLE'
BUILD = ROOT.parent / 'MP-I01R-PLANNER-BUILDER-P01'
records = []

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def emit(name, data):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def read(path, selector):
    records.append({'source': str(path), 'sha256': sha(path), 'selection': selector})
    return json.loads(path.read_text(encoding='utf-8-sig'))

bdp = next(x for x in read(PLAN/'builder-design-packages.json', 'packages[package_id=BDP-01]')['packages'] if x['package_id']=='BDP-01')
emit('inputs/BDP-01-r1.json', bdp)
old = copy.deepcopy(bdp)
ids = {x['interface_id'] for x in bdp['interface_baselines']}
sids = {x['service_id'] for x in bdp['external_service_interfaces']}
ibase = read(PLAN/'interface-baselines.json', sorted(ids))
services = read(PLAN/'external-service-interfaces.json', sorted(sids))
interfaces = [x for x in ibase['interfaces'] if x['interface_id'] in ids]
service_list = [x for x in services['services'] if x['service_id'] in sids]
assert interfaces == bdp['interface_baselines']
assert service_list == bdp['external_service_interfaces']
for dep in bdp['dependencies'][:2]:
    assert sha(PLAN/dep['file']) == dep['sha256']
emit('inputs/interface-baselines-r1.json', {'interfaces': interfaces})
emit('inputs/external-service-interfaces-r1.json', {'services': service_list})
handoff = read(PLAN/'handoff-register.json', 'public_coordination only')
emit('inputs/public-coordination-r1.json', handoff['public_coordination'])
issues = read(BUILD/'issues.json', 'whole authorized file')
emit('inputs/MP-I01R-issues.json', issues)
for name in ['handoff-consumption-record.md', '设计核验.json']:
    p = BUILD/name
    records.append({'source':str(p),'sha256':sha(p),'selection':'whole authorized file'})
    (ROOT/'inputs'/name).write_bytes(p.read_bytes())
for path, name in [
    (ASSETS/'minecraft/建筑师/world/civilizations/CIV-001/README.md', 'CIV-001-Canon.md'),
    (ASSETS/'minecraft/建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md', 'CIV-001-Architecture-Grammar.md')]:
    records.append({'source':str(path),'sha256':sha(path),'selection':'current approved Canon / Grammar; no transitive references followed'})
    (ROOT/'inputs'/name).write_bytes(path.read_bytes())

# 仅选门前连接块及其两侧衔接所需地表列；不打开存档，不使用浅层证据推断水文。
surface = read(PLAN/'evidence/地表采样.json', '753 <= x <= 761 and 1632 <= z <= 1638')
assert sha(PLAN/'evidence/地表采样.json') == next(d['sha256'] for d in bdp['dependencies'] if d['file']=='evidence/地表采样.json')
slice_rows = [r for r in surface['columns'] if 753<=r[0]<=761 and 1632<=r[1]<=1638]
emit('evidence/公共接口地表切片.json', {'authority':surface['authority'],'fields':surface['fields'],'palette':surface['palette'],'columns':slice_rows,'limitation':'Archived snapshot only; not a hydraulic model or continuous collision certification.'})

coordination = {
    'planning_author': 'MP-I02A / minecraft-planner v0.5',
    'planning_coordination_owner': 'PUBLIC-COORDINATOR',
    'planning_responsibility': '维护本户接触面、两侧公共路段连续净空与跨界服务责任；接收 Builder 的最小接口反馈。',
    'actual_assignment': handoff['public_coordination']['assignment'],
    'approval_record': None,
    'authority': 'DESIGN_PROPOSAL under MP-I02A task authorization; not actual appointment or easement approval',
    'builder_responsibility': '仅本户建筑、门前私侧停步和户内高差；不得替公共方修路或承诺受纳。',
    'rights_resolve_before': 'BEFORE_WORLD_WRITE'
}
contact = {
    'authority':'DESIGN_PROPOSAL supported by OBSERVED_SNAPSHOT',
    'private_contact_cell':[757,1633],
    'shared_contact_face':{'x':[757,758],'z':1634,'surface_y':132},
    'private_surface_y':132,
    'public_surface_y':132,
    'height_semantic':'Y132 为行走面，不是 ground block Y；来源 ground_y=131。',
    'public_connection_patch':{'x':[756,758],'z':[1634,1636],'surface_y':132,'clear_y':[132,135]},
    'patch_semantic':'闭合矩形边界定义连续设计表面和其上开放净空；四列只作本地接口控制，不把它当作整条公共路的通行证明。',
    'continuous_route_status':'UNRESOLVED_AT_BOTH_TIE_INS',
    'tie_in_faces':[{'x':756,'z':[1634,1636]},{'x':758,'z':[1634,1636]}],
    'tie_in_requirement':'公共方需连接至既有 LANE-04 局部走线；两侧转折及断面变化全程保持法向净宽 >=2、行走面以上净高 >=3。不得仅凭相邻 cells 连通认定闭合。'
}
for item in interfaces:
    if item['interface_id'] not in {'R2-IF-THRESHOLD-1','R2-IF-LANE-04'}:
        continue
    item['interface_revision']='r2'
    item['supersedes']={'plan':'MP-P05R2','interface_id':item['interface_id'],'interface_revision':'r1','scope':'BDP-01 contact only; remaining geometry inherited'}
    item['status']='DESIGN_PROPOSAL_PARTIAL_CLOSURE'
    item['planning_coordination']=coordination
    item['local_contact_control']=contact
    if item['interface_id']=='R2-IF-THRESHOLD-1':
        item['height_or_section_baseline']['rule']='本轮规划级固定 contact face Y132；不再允许该接触点任意±1。户内余高差仍由 Builder 消化，非批准建筑方案。'
        item['height_or_section_baseline']['preferred_contact_surface_y']=[132,132]
        item['adjustment_envelope']={
            'horizontal':'r2 固定 shared_contact_face；门、私侧落脚与阶梯可在原24列 apron 内调整，门扇全状态不得侵入公共净空。改接触面需接口再修订。',
            'vertical':'shared_contact_face Y132，允许偏移0；其余户内高差由 Builder 设计。',
            'public':'家庭 Builder 无公共面调整权；公共连接块外两侧 tie-in 尚未冻结。'
        }
        item['uncertainty']=['局部接触表面已编译为规划级提案；连续公共 tie-in 与公共协调确认仍未闭合。','确切门、步级和净空适配由 Builder 在新 revision 下核验。','真实土地/地役许可 BEFORE_WORLD_WRITE。']
    else:
        item['height_or_section_baseline']['local_override']='仅 local_contact_control 中四列行走面固定 Y132；其余 r1 观测断面不改成已冻结设计断面。'
        item['adjustment_envelope']['local_override']='四列连接块平面不外扩、行走面Y132偏移0；其余原调整范围只是候选权限，任何两侧连接修订须公共方记录新revision。'
        item['uncertainty']=['UNRESOLVED：四列连接块之外两侧连续净宽/转折/断面尚无闭合设计；不能外推为整条LANE-04已冻结。','规划责任已分配到PUBLIC-COORDINATOR角色；实际承接人与回签未提供。','真实通行地役许可保持BEFORE_WORLD_WRITE。']

rain = next(s for s in service_list if s['service_id']=='R2-S1-RAINWATER')
rain.update({
    'service_revision':'r2',
    'supersedes':{'service_id':'R2-S1-RAINWATER','revision':'r1','revision_semantic':'r1 inherited from external-service-interfaces container'},
    'status':'UNRESOLVED_WITH_BOUNDED_LOCAL_OPTION',
    'builder_responsibility':'RESERVE_INTERFACE_ONLY',
    'upstream_or_downstream_owner':'PUBLIC-COORDINATOR：跨 parcel 受纳边界、接口位置/标高及责任协调；户内收集与留存由 BDP-01 Builder 设计、拟议住户运行。',
    'neighbor_or_public_responsibility':'没有当前受纳承诺。若采用跨界方案，公共方提供局部受纳对象、位置/标高、设计事件/峰值/容量和下游责任；本户不得把邻户、公路、共同院当作默认受纳地。',
    'interface_location_or_ref':'interface-baselines.json#R2-IF-THRESHOLD-1 (access/boundary reference only; NOT an outfall)',
    'local_requirement':'本户保持收集/调蓄预留；允许研究不跨界的闭合 local strategy，但两只干容器只证明预留，不证明容量、溢流安全或清空能力。',
    'allowed_local_adjustment':'仅原 R2-P1 cells 内；不得占用独立家庭院、必要生活空间或公共净空，不预设地下渗排、公共管道或无限容器。',
    'conditional_local_strategy':{
        'permission':'允许 Builder 设计比较与提交定量闭合证据；当前不是 FULL_SCOPE_OWNER 或已获批准的闭合系统。',
        'current_reservation_only':True,
        'responsibility_after_verified_selection':'FULL_SCOPE_OWNER limited to parcel-local collection/retention; public receiving obligation remains NONE',
        'selection_requires_new_service_revision':True,
        'quantitative_minimum':['明确有来源的设计降雨事件、历时及连续事件/恢复时间假设；不得由地表岩石臆测渗透。','明确全部屋面/汇水面和外来流入边界，核算有效入流、有效储量、初始占用及余量。','明确在设计事件与超设计事件/堵塞/满储失效时水的去向，证明不危害公共通行、邻户、基础及生活空间；不能把越界溢流称为闭合。','明确可持续清空/再利用能力、责任与中断条件；不得借尚未证实的清运服务闭合质量平衡。'],
        'planner_boundary':'Planner 固定是否跨界、责任与所需性能证据；不指定 gutter/pipe/cistern/foundation 的尺寸、构件和布局。'
    },
    'receiving_location':None,'receiving_elevation':None,'receiving_capacity':None,
    'retention_responsibility':{'design':'BDP-01 Builder','operation':'proposed household operator; actual commitment unverified','cross_parcel_receiving':'NONE_COMMITTED'},
    'resolve_before':'BEFORE_DESIGN_FREEZE',
    'uncertainty':'受纳方案或经定量核验的闭合本地方案均未具备，保留 U-RAINWATER HOLD；真实土地/地役许可另保持 BEFORE_WORLD_WRITE。'
})
emit('interface-baselines.json', {'revision':'r2','source_plan_revision':'MP-P05R2-r1','revision_package':'MP-I02A-r1','authority':'DESIGN_PROPOSAL / AWAITING_GPT_AND_OWNER','scope':'BDP-01 direct interfaces only','interfaces':interfaces})
emit('external-service-interfaces.json', {'revision':'r2','source_plan_revision':'MP-P05R2-r1','scope':'BDP-01 services only','services':service_list})

register = copy.deepcopy(issues)
register.update(test='MP-I02A',revision='r1',package_revision='r2',design_state='STALE_FOR_FIDELITY_REVIEW',review_status='AWAITING_GPT_AND_OWNER')
for issue in register['issues']:
    if issue['id']=='U-PUBLIC':
        issue.update(status='UNRESOLVED',dependency_revision='r2',closed_subconditions=['规划级接触面Y132、四列公共连接块及其3格净高要求已具体化。','本地adjustment envelope及Planner/Builder/公共角色责任已明确。'],minimum_missing_evidence=['两侧tie-in连续2格法向净宽、3格净高与标高衔接的局部几何/section证明。','PUBLIC-COORDINATOR规划责任承接/回签记录；不要求此时伪造真实地役许可。'],closure_limit='四列连接块只完成局部设计控制，未证明两侧公共通行连续性。')
    elif issue['id']=='U-RAINWATER':
        issue.update(status='UNRESOLVED',dependency_revision='r2',closed_subconditions=['跨parcel责任与不可默认排放边界明确。','允许有条件研究闭合local strategy；当前仍只预留。'],minimum_missing_evidence=['外部路径：局部受纳点/标高/容量设计依据及责任承接。','或本地路径：有来源的设计事件、入流/有效储量/恢复质量平衡、超限失效安全证据及责任确认。'],closure_limit='两个路径任选其一充分闭合后才能消除冻结前雨水HOLD；本轮没有量化数据。')
    else:
        issue['handling_in_MP_I02A']='OUT_OF_SCOPE_UNCHANGED; no closure asserted'
register['stop_rule']='Deliver MP-I02A revision package then stop for GPT + Owner; regression verdict NOT_ASSIGNED.'
emit('closure-register.json', register)

bdp['package_revision']='r2'
bdp['source_plan_revision']='MP-P05R2-r1'
bdp['revision_package']='MP-I02A-r1'
bdp['builder_handoff_readiness']='CONCEPT_DESIGN_READY'
bdp['readiness_reason']='本户接触面及责任边界已局部具体化；连续公共tie-in与雨水性能/受纳证据仍缺，不足以Architecture Design Freeze。此为接口完整度说明，不是回归裁决。'
bdp['interface_baselines']=interfaces
bdp['external_service_interfaces']=service_list
bdp['interface_revisions']={i['interface_id']:i['interface_revision'] for i in interfaces}
bdp['external_service_revisions']={s['service_id']:s.get('service_revision','r1') for s in service_list}
bdp['known_uncertainty']=register['issues']
bdp['source_dependencies_inherited']=old['dependencies']
bdp['dependencies']=[{'file':f,'revision':'r2' if f in ['interface-baselines.json','external-service-interfaces.json'] else 'r1','sha256':sha(ROOT/f)} for f in ['interface-baselines.json','external-service-interfaces.json','closure-register.json','evidence/公共接口地表切片.json']]
bdp['source_refs']=['source-provenance.json','inputs/BDP-01-r1.json','inputs/CIV-001-Canon.md','inputs/CIV-001-Architecture-Grammar.md']
bdp['downstream_design_status']={'design':'MP-I01R / BDP-01 concept r1','status':'STALE_FOR_FIDELITY_REVIEW','reason':'THRESHOLD-1 / LANE-04 / RAINWATER revisions r1 -> r2','original_design_modified':False,'recheck':'Builder must consume r2 and recheck affected fidelity after interface HOLD closure; no automatic redesign authorized here.'}
emit('BDP-01.json',bdp)
lineage={'revision_package':'MP-I02A-r1','parent':'MP-P05R2-r1 / BDP-01-r1','package_revision':'r2','scope':'BDP-01 only; not global replacement of MP-P05R2','interface_changes':[{'id':i,'from':'r1','to':'r2'} for i in ['R2-IF-THRESHOLD-1','R2-IF-LANE-04','R2-S1-RAINWATER']],'unchanged_interfaces':[i for i in sorted(ids|sids) if i not in ['R2-IF-THRESHOLD-1','R2-IF-LANE-04','R2-S1-RAINWATER']],'downstream':bdp['downstream_design_status'],'other_consumers':'未读取其它BDP或设计。共享LANE-04的其它消费者须在采用本BDP-01局部overlay前由公共协调方识别；本包不覆盖其r1。','regression_verdict':'NOT_ASSIGNED','world_writes':0}
emit('revision-lineage.json',lineage)
for name in ['Planner-SKILL.md','planner-builder-contract.md','planner-builder-handoff.md']:
    records.append({'source':'https://github.com/zhangchenjia21-dot/Vibe-Coding/blob/fc6371361685e2eeaefdef5a513f21dbe64c6696/skill/codex/'+({'Planner-SKILL.md':'minecraft-planner/SKILL.md','planner-builder-contract.md':'shared/minecraft-planner-builder-contract.md','planner-builder-handoff.md':'minecraft-planner/references/planner-builder-handoff.md'}[name]),'sha256':sha(ROOT/'inputs'/name),'snapshot':'inputs/'+name})
emit('source-provenance.json',{'test':'MP-I02A','date':'2026-09-14','planner':'0.5','shared_contract':'1.0','remote_HEAD_verified':'fc6371361685e2eeaefdef5a513f21dbe64c6696','records':records,'other_read_log':['AI工程/ARCHITECTURE.md and assets/AGENTS.md for workspace boundaries','MP-I01R inputs/来源与读取记录.json solely to locate current Skill and Canon; historical design answers not followed','MP-I01R 设计几何.json parsed only keys, count and first two floor boxes to inspect format; no full architecture consumed or copied','Memory registry keyword lookup returned no task-specific source; no historical rollout read','Directory names listed for locating allowed inputs; no Independent Review contents opened'],'excluded_content_read':[],'selection_policy':'Containers parsed by tools; only BDP-01 and its exact direct interface IDs exposed/copied. No BDP-02 selected.','authority':'Observed snapshot supports elevations; local controls are DESIGN_PROPOSAL, neither Canon change nor permission.','world_writes':0,'world_write_authorization':False,'regression_verdict':'NOT_ASSIGNED'})
print('Compiled MP-I02A; BDP-01 r2; U-PUBLIC and U-RAINWATER remain UNRESOLVED; no regression verdict.')
