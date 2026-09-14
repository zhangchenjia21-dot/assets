"""仅编译设计审阅文件；输入固定在本目录，不加载世界、不裁定语义 Gate。"""
from pathlib import Path
import json, math, hashlib, collections

ROOT = Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def write(name, value):
    (ROOT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

old = read('inputs/concept-r1/设计体素.json')
bdp = read('inputs/r3/BDP-01.json')
site = read('inputs/场地事实切片.json')
public = read('inputs/r3/evidence/公共通行冻结基线.json')
blocks = {}
changes = []
def put(v, state, **extra):
    w = dict(v, state=state, **extra)
    blocks[(w['x'],w['y'],w['z'])] = w
    return w
for v in old['blocks']:
    role, shape = v['role'], v['shape']
    base = {'stone':'stone_bricks','wood':'spruce_planks','plaster':'calcite','roof':'deepslate_tiles','glass':'glass','metal':'iron_block','bed':'red_bed','water':'cauldron'}[v['material']]
    state = 'minecraft:'+base
    if shape == 'stair':
        base = 'deepslate_tile_stairs' if v['material']=='roof' else 'spruce_stairs' if v['material']=='wood' else 'stone_brick_stairs'
        state = f'minecraft:{base}[facing={v["facing"]},half=bottom,shape=straight,waterlogged=false]'
    elif shape == 'slab':
        base = 'deepslate_tile_slab' if v['material']=='roof' else 'stone_brick_slab' if v['material']=='stone' else 'spruce_slab'
        state = f'minecraft:{base}[type=bottom,waterlogged=false]'
    if role == 'sleeping_place':
        state = f'minecraft:red_bed[facing=south,occupied=false,part={"foot" if v["z"]==1627 else "head"}]'
    if role in ['batch_storage','food_storage','linen_storage','sealed_waste','clean_water_storage']:
        state = 'minecraft:barrel[facing=up,open=false]'
    if role in ['wash_basin','rain_reservation']:
        state = 'minecraft:cauldron'
    if role == 'repair_bench': state = 'minecraft:crafting_table'
    if role == 'small_vise': state = 'minecraft:anvil[facing=north]'
    if role == 'cooking_hearth': state = 'minecraft:furnace[facing=west,lit=false]'
    if role == 'post': state = 'minecraft:spruce_log[axis=y]'
    if role == 'roof_tie': state = 'minecraft:spruce_log[axis=z]'
    if role == 'stair_guard':
        state = 'minecraft:spruce_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]'
    put(v,state)
    if role == 'privacy_screen':
        put(dict(v,y=v['y']+1), 'minecraft:spruce_planks')

# 门的关闭状态是存储态；行走核验采用显式开门交互，不把闭门穿越当作可达。
doors = [(755,132,1631,'work_door'),(758,132,1631,'family_door'),(766,138,1627,'hygiene_door')]
for x,y,z,role in doors:
    for dy in [0,1]:
        put({'x':x,'y':y+dy,'z':z,'material':'wood','role':role,'shape':'door'},
            f'minecraft:spruce_door[facing=north,half={"lower" if dy==0 else "upper"},hinge={"right" if role=="hygiene_door" else "left"},open=false,powered=false]')
    changes.append({'component':role,'at':[x,y,z],'change':'two native door halves; inside original parcel; open for transit, close for privacy'})
    if role != 'hygiene_door':
        put({'x':x,'y':y+2,'z':z,'material':'stone','role':'door_head_closure','shape':'cube'},'minecraft:stone_bricks')
# 两处可开闭窗替代固定玻璃，提供起居与卫生通风；不把开窗当排烟性能证明。
for x,y,z,facing in [(765,135,1629,'north'),(767,139,1627,'west')]:
    put({'x':x,'y':y,'z':z,'material':'wood','role':'ventilation_shutter','shape':'trapdoor'},
        f'minecraft:spruce_trapdoor[facing={facing},half=bottom,open=true,powered=false,waterlogged=false]')
# 卫生区前界补薄屏，维持原有两格操作带和家庭上层通路。
for y in [138,139]:
    put({'x':765,'y':y,'z':1627,'material':'wood','role':'hygiene_front_screen','shape':'trapdoor'},
        'minecraft:spruce_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]')
changes += [
    {'component':'privacy_screen','change':'replace custom 0.2-wide screen by two-high full native planks in the same two columns'},
    {'component':'stair_guard','change':'replace custom 0.12-wide rail by open native south-facing trapdoor, north-edge thickness 3/16; upper passage remains 13/16 wide'},
    {'component':'chimney','change':'unchanged solid stone placeholder; explicitly NOT a functioning flue'},
    {'component':'rain','change':'dry native cauldrons are reservations only; zero certified design storage; performance alternatives separately evaluated'}]

def state_parts(v):
    s=v['state']; name=s.split('[')[0]; props={}
    if '[' in s:props=dict(p.split('=') for p in s.split('[')[1][:-1].split(','))
    return name,props

def boxes(v, doors_open=False):
    x,y,z=v['x'],v['y'],v['z']; name,p=state_parts(v)
    def box(a,b):return {'min':[x+a[0],y+a[1],z+a[2]],'max':[x+b[0],y+b[1],z+b[2]],'role':v['role'],'material':v['material'],'state':v['state']}
    if name.endswith('_stairs'):
        f=p['facing']; upper={'east':([.5,.5,0],[1,1,1]),'south':([0,.5,.5],[1,1,1]),'north':([0,.5,0],[1,1,.5])}[f]
        return [box([0,0,0],[1,.5,1]),box(*upper)]
    if name.endswith('_slab'):return [box([0,0,0],[1,.5,1])]
    if name.endswith('_trapdoor'):
        return [box(*{'south':([0,0,0],[1,1,3/16]),'north':([0,0,13/16],[1,1,1]),'west':([13/16,0,0],[1,1,1])}[p['facing']])]
    if name.endswith('_door'):
        return [box(*(([0,0,0],[3/16,1,1]) if p['hinge']=='left' else ([13/16,0,0],[1,1,1])))] if doors_open else [box([0,0,13/16],[1,1,1])]
    if name.endswith('_bed'):return [box([0,0,0],[1,9/16,1])]
    # 炉、桶、砧和盆采取整格外包络；不利用容器凹腔获得通行净空。
    return [box([0,0,0],[1,1,1])]

model = dict(old,format='MP-I02B native-state review candidate v1',revision='r2',
    predecessor='MP-I01R concept r1',consumed_bdp='BDP-01 r3',status='UNFROZEN_DESIGN_WITH_BLOCKERS',
    blocks=list(blocks.values()),design_occupancy={'residents':2,'households':1,'basis':'Builder design scenario, not actual population; repair operator included among residents; one temporary handover visitor on apron'},
    roof_and_services={'rain':'UNPROVED; no public discharge; see 雨水性能.json','flue':'SOLID_PLACEHOLDER_NOT_FUNCTIONAL','roof_top_y':144,'chimney_top_y':145})
write('设计体素.json',model)
write('设计修订.json',{'revision':'r2','preserved':['Architectural Intent','primary Plan/Section','Program and Space Graph','Massing','stone plinth and timber tectonic logic','routes','private yard','public threshold'],'bounded_changes':changes,'superseded':['r1 custom screen/rail geometry','r1 open doorways','r1 pending public interface coordination wording','r1 anticipated public rainwater receiver'],'not_superseded':'r1 conceptual functional flue and rain closure requirements remain unsatisfied; no construction authorization'})
bs=[b for v in blocks.values() for b in boxes(v,True)]
write('设计几何.json',{'authority':'static native-shape review; doors in interaction-open state','boxes':bs,'unverified':'no Minecraft registry/update/physics execution; dynamic trapdoor opening not claimed as a route action'})
mask=set(map(tuple,bdp['spatial_envelope']['cells']))
pub=set(map(tuple,public['protected_horizontal_geometry']['cells']))
ground={(c[0],c[1]):c[3] for c in site['columns']}
outside=[list(k) for k in blocks if (k[0],k[2]) not in mask]
intrusions=[]
for p in public['design_surface']['per_cell']:
    lo,hi=p['protected_vertical_interval']
    intrusions.extend([list(k) for k in blocks if k[0]==p['x'] and k[2]==p['z'] and k[1]<hi and k[1]+1>lo])
yard=[v for v in blocks.values() if v['role']=='yard_floor']
yard_above=[list(k) for k in blocks if any(v['x']==k[0] and v['z']==k[2] for v in yard) and k[1]>=131]

def intersects(a,b):return all(a['min'][i]<b['max'][i]-1e-7 and a['max'][i]>b['min'][i]+1e-7 for i in range(3))
route_results=[]
support_roles={'floor','shallow_plinth','upper_floor','private_landing','apron_floor','yard_floor','internal_stair','split_level_stair','yard_step','stair_support','stair_stringer'}
for route in model['routes']:
    hits=[]; samples=0; unsupported=0
    for a,b in zip(route['surface'],route['surface'][1:]):
        n=max(1,math.ceil(math.hypot(b[0]-a[0],b[1]-a[1])*16))
        for t in [i/n for i in range(n+1)]:
            x=a[0]+(b[0]-a[0])*t+.5; z=a[1]+(b[1]-a[1])*t+.5; nominal=a[2]+(b[2]-a[2])*t
            projection={'min':[x-.3,nominal-1,z-.3],'max':[x+.3,nominal+1.01,z+.3]}
            support=[p['max'][1] for p in bs if p['role'] in support_roles and intersects(projection,p)]
            if not support:unsupported+=1;continue
            foot=max(support)
            body={'min':[x-.3,foot+1e-6,z-.3],'max':[x+.3,foot+1.8,z+.3]}
            bad=[p['role'] for p in bs if intersects(body,p)]
            if bad:hits.append({'at':[round(x,4),round(foot,4),round(z,4)],'roles':sorted(set(bad))})
            samples+=1
    route_results.append({'route':route['id'],'samples':samples,'body_obstructions':len(hits),'unsupported':unsupported,'examples':hits[:8]})

contacts=[]; edits=[]; influence=set()
for k,v in blocks.items():
    x,y,z=k;g=ground[(x,z)]
    if y<=g:edits.append({'at':list(k),'observed_ground_y':g,'role':v['role']})
    if v['role'] in support_roles and (x,y-1,z) not in blocks and y<=g+1:
        contacts.append({'at':list(k),'ground_y':g,'role':v['role']})
        # 三格、2:1扩散仅是有界证据覆盖筛查；不是虚构承载力或实际应力影响截止面。
        for depth in range(1,4):
            radius=math.ceil(depth/2)
            for dx in range(-radius,radius+1):
                for dz in range(-radius,radius+1):influence.add((x+dx,y-depth,z+dz))
near={(c['x'],c['ground_y']+site['near_ground']['dy_range'][0]+i,c['z']):site['near_ground']['palette'][s] for c in site['near_ground']['columns'] for i,s in enumerate(c['state_ids'])}
missing=sorted(influence-set(near)); observed=collections.Counter(near[k] for k in influence if k in near)
write('地基影响核验.json',{'status':'PARTIAL_EVIDENCE_BLOCKER','actual_edit_cells_at_or_below_surface':edits,'below_surface_count':sum(e['at'][1]<e['observed_ground_y'] for e in edits),'ground_contacts':contacts,'contact_count':len(contacts),'screening_volume_cells':[list(k) for k in sorted(influence)],'screening_rule':'3 blocks below contact; 2 vertical to 1 horizontal spread, rounded conservatively. Coverage sensitivity only, not a verified load influence cutoff.','screening_unobserved_cells':[list(k) for k in missing],'screening_states':dict(observed),'known_artificial_locations':site['near_ground']['block_entities'],'direct_location_intersections':[x for x in site['near_ground']['block_entities'] if (x['x'],x['y'],x['z']) in influence],'minimum_gap':'Define/justify load influence depth and lateral extent for stepped masonry/timber + any water load; supply existing factual coverage of that volume and artificial structure extents where relevant. No whole-world/deep-clearance certificate demanded. Current shallow sample cannot establish bearing/joints or complete structure extent.','world_writes':0})
write('设计核验.json',{'test':'MP-I02B','revision':'r2','world_writes':0,'regression_verdict':'NOT_ASSIGNED','checks':{'native_state_count':len(blocks),'outside_parcel':outside,'public_clear_envelope_intrusions':intrusions,'private_yard_cells':len(yard),'yard_above_obstructions':yard_above,'threshold_top':blocks[(757,131,1633)]['y']+1,'required_threshold_top':132,'route_results':route_results},'limits':['Static 0.6 x 1.8 body envelope only, doors deliberately opened. Foot lifted to local supporting stair surface for headroom; not game stepping/jump simulation.','Runtime movement and native-state neighbor updates unverified.','Solid chimney is not a lumen. Roof collection, water balance and storage are not certified.']})

# 水量模型只作显式条件分析；不把自选降雨量提升为Site事实或批准设计事件。
roof_columns=set((v['x'],v['z']) for v in blocks.values() if v['role'] in ['house_roof','workshop_roof','chimney'])
rain={'status':'UPSTREAM_PLANNING_ISSUE','interface':'R2-S1-RAINWATER r3','catchment':{'roof_projection_cells':len(roof_columns),'parcel_cells':len(mask),'yard_exposed_cells':len(yard),'conversion':'Conditional 1 block = 1 m, runoff coefficient 1 for conservative screening; not measured site hydrology'},'existing_native_cauldrons':{'count':2,'certified_storage_m3':0,'reason':'Minecraft cauldron levels are not calibrated real cubic metres; roof runoff is not simulated by native rain'},'bounded_options':[
 {'id':'RW-A','geometry':'Existing two reservation columns (756,1625),(757,1625)','assumed_engineered_net_storage_m3':2,'status':'REJECTED_AS_PROOF','reason':'Even generously assuming 1 m3 per column does not create recovery or safe failure; original vessels have no gutter connection.'},
 {'id':'RW-B','geometry':'Above-ground sealed north strip X756..759 / Z1625 (four legal columns), maximum 2 m useful depth, independent support required','assumed_engineered_net_storage_m3':8,'status':'BOUNDED_ENVELOPE_STUDY_ONLY','reason':'8 m3 is optimistic net volume before wall/freeboard losses, not an installed tank. No verified recovery sink; additional water loads reopen U-GROUND. Roof branches and all exposed yard drainage remain to be collected.'},
 {'id':'RW-C','geometry':'Buried retention/infiltration or converted yard','status':'NOT_ADOPTED','reason':'Cannot assume rock infiltration or deep excavation safety. Taking the mandatory 18-cell yard or routing overflow across boundary violates fixed relations.'}],
 'sensitivity':[{'rain_mm':p,'roof_m3':round(len(roof_columns)*p/1000,3),'whole_parcel_m3':round(len(mask)*p/1000,3),'8m3_optimistic_remaining':round(8-len(mask)*p/1000,3)} for p in [10,25,50,100,200]],
 'balance':'S_next = S + precipitation * catchment - verified recovery. Verified guaranteed recovery lower bound is 0. For any finite storage, repeated positive rainfall exceeds capacity without a bounded cumulative event and a proved recovery/failure path.',
 'safe_failure':'Not demonstrated. Entry flood barrier would conflict with Y132 fixed contact / access; full yard enclosure without safe retained water depth and recovery does not establish safe occupancy.',
 'minimum_upstream_request':'Preserve r3 no-discharge baseline. Provide/accept a justified cumulative design-event and failure envelope plus a guaranteed parcel-local recovery mechanism compatible with current evidence; if impossible, planner must decide the smallest explicit R2-S1-RAINWATER interface revision. Builder does not propose or assume a public outfall.',
 'affected':['BDP-01','R2-S1-RAINWATER','MP-I02B candidate r2; any changed boundary/contact also requires explicit related interface revision'],
 'claim_limit':'Inability to prove under current evidence and bounded adaptations; not a mathematical claim that every possible parcel-local solution is impossible.'}
write('雨水性能.json',rain)
print(json.dumps({'native_blocks':len(blocks),'outside':len(outside),'public_intrusions':len(intrusions),'routes':route_results,'contact_count':len(contacts),'screening_missing':len(missing),'roof_cells':len(roof_columns)},ensure_ascii=False))
