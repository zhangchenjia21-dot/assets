"""把当前快照查询压缩为轻量审核包；推荐判断由本轮人工比较明确给出，不自动评分。"""
import gzip,json,hashlib
from collections import Counter,deque
import numpy as np
import 当前场地读取 as s
rows=json.load(gzip.open(s.CACHE/'surface.json.gz','rt',encoding='utf-8'));by={(p['x'],p['z']):p for p in rows}
candidates=s.read(s.CACHE/'candidate-analysis.json');content=s.read(s.CACHE/'content-analysis.json');delta=s.read(s.CACHE/'cache-delta.json')
g=s.mask(next(n for n in s.read(s.PLAN/'settlement-nodes.json')['nodes'] if n['id']=='G1')['envelope'])
reader=s.Reader();visual=[]
# 仅作地形与植被遮挡见证；站立眼高 1.62，不模拟尚未设计的建筑高度。
for c in candidates:
    x,z=c['study_anchor'];target=by[(x,z)]['ground_y']+1.62;source=[89,1750];source_y=by[tuple(source)]['ground_y']+1.62
    points=[];seen=set();blocked=[]
    for t in np.linspace(0,1,2*max(abs(x-source[0]),abs(z-source[1]))+1):
        xx=int(round(source[0]+(x-source[0])*t));zz=int(round(source[1]+(z-source[1])*t));yy=source_y+(target-source_y)*t
        if (xx,zz) in seen:continue
        seen.add((xx,zz));name=reader.block(xx,int(np.floor(yy)),zz)
        points.append([xx,zz,round(yy,3),name])
        if name not in s.AIR|s.PLANTS and not any(q in name for q in ('fern','flower','sapling')):blocked.append([xx,int(np.floor(yy)),zz,name])
    visual.append({'site':c['id'],'source_eye':[89,round(source_y,2),1750],'target_eye':[x,round(target,2),z],'method':'single standing-eye block-occlusion ray; not screenshot, building skyline or full viewshed','sample_columns':len(points),'blocked_samples':blocked,'ray':points})

notes={
'S1':{'terrain_adaptation':'Y66–67、总高差1格，适合顺地组织主体与院场；不需以全场削平为先决条件，具体基础未定。','access_loading_relation':'东南侧9步当前表层见证接入 R1b；装卸可退入 gross envelope 内，不能把净空当专属仓院。','resident_life_relation':'东南交换面与北/西住家生活面有分开组织的余地；保留共享院、储水和维护空间，入口位置尚未设计。','drainage_water_note':'北缘有不升高到更低地面的短见证；排水须保留岸线维护，不向岸边排污。饮用水未确认；沿通行联系运水、院内储水/消防作为待设计验证关系。','political_visual_risk':'位于 G1 东侧、远离 X89 阈值，较不易误读为边界官署；与 N1 相邻，必须保持次级门户尺度，不借 N1 地块扩容。','pros':['三者中候选面高差最小','较高缓台，局部向北排水方向清楚','9步联系在同一Y67上，居民/货物组织空间较完整'],'cons':['东界紧邻 G1/N1 分界，不可向东借地','缓冲内有树木和冠幅，后续入口须避让','饮水来源与深于12格的地下未确认'],'verdict':'RECOMMENDED / AWAITING GPT + OWNER REVIEW'},
'S2':{'terrain_adaptation':'Y63–65、总高差2格；局部台阶/错层适配的需求高于 S1，不应为物流而削成统一大坪。','access_loading_relation':'南侧9步接入 G1 中段；即时交接方便，但装卸停驻不得溢入最繁忙的穿行带。','resident_life_relation':'北侧可联系居民后勤与小供给；要隔开南侧短仓噪声与家庭日常通行。','drainage_water_note':'北缘通向Y62低地，存在非升高排水见证；低缘比 S1 更敏感，不应把低地当污水接收池。清洁供水待确认。','political_visual_risk':'接近门户中段，易读为街市服务；须避免正对穿行线的封闭控制入口。','pros':['居于 G1 中段，日用品和居民步行联系直接','保有586格研究容量','下方12格未检出空腔或水'],'cons':['高差2格且北缘接近Y62低地','更接近高频交接流线','缓冲内有一头牛，后续施工须另检查和保护实体'],'verdict':'VIABLE ALTERNATIVE / CONDITIONS OPEN'},
'S3':{'terrain_adaptation':'Y64–66、高差2格；南侧树木较多，需以避让和顺地关系处理，不能默认清空树木。','access_loading_relation':'北侧9步到主穿行；短仓可向北交接，不能把通行带当停牲口区。','resident_life_relation':'南侧生活面相对独立，适合经营家庭与小供给；需要保留后勤与树木维护间隙。','drainage_water_note':'沿西侧有24步非升高到更低地面的见证，较 S1/S2 长且经过平缓段；降雨汇流/地表维护更需设计复核，清洁取水不能由此推定。','political_visual_risk':'可表达路旁生活院，边界官署误读较低；不得以院墙横贯主路。','pros':['三者容量最大605格','货物北侧、生活南侧的组织潜力较清楚','浅层无空腔/水体见证'],'cons':['2格高差','缓冲内木干和冠幅最多','局部排水见证较长，平段多'],'verdict':'VIABLE ALTERNATIVE / CONDITIONS OPEN'}
}
for c in candidates:
    c.update(notes[c['id']]);c['world_write_authorized']=False
    c['existing_content_risk']='未检出规则所列人工材料或 block entity；不能证明自然材料未被玩家摆放。树木/实体记录须保留，不自动清除。'
    c['subsurface_risk']='候选+4格缓冲逐柱地面下12格未检出空气/水/熔岩/所列人工材料；更深和缓冲外未调查。'
    c['capacity_basis']='数百格不规则 gross envelope，为一个中等主体及必需共享院、装卸短停、居民入口、储水/消防与维护的容量研究；不固定比例、建筑矩形或功能分区。'
    c['visual_witness']=next(v for v in visual if v['site']==c['id'])
s.write(s.OUT/'candidates.json',{'schema':'local-site-candidates/1','status':'AWAITING GPT + OWNER REVIEW','source_territory_revision':154,'candidate_count':3,'candidates':candidates,'screening_rejections':s.read(s.CACHE/'screening-rejections.json'),'world_writes':0})
rec=candidates[0]
s.write(s.OUT/'recommended-site.json',{'schema':'local-site-recommendation/1','status':'RECOMMENDED / SITE ACCEPTANCE PENDING GPT + OWNER','id':'S1','name':rec['name'],'geometry':rec['geometry'],'bounds':rec['bounds'],'gross_usable_area':rec['gross_usable_area'],'surface_elevation_range':rec['surface_elevation_range'],'source_snapshot':'current-world-audit.json','why':rec['pros'],'planning_anchor_is_not_building_coordinate':True,'first_build_type':'G1 共享周转与生活院','architecture_footprint_frozen':False,'world_write_authorized':False,'conditions_before_design_or_build':['GPT + Owner accept this Site Gate before Architecture Design task','verify potable source or actual clean-water delivery/storage solution','resolve canopy/root/animal protection and separated goods/resident circulation','verify foundation volume, drainage and deeper underground if future design exceeds 12-block audit','refresh current state before any future world-write authorization']})
grows=[p for p in rows if g[p['z']-s.Z0,p['x']-s.X0]]
surface={'status':'CURRENT SAVE OBSERVED','observed_scope_columns':len(rows),'G1_columns':len(grows),'G1_ground_y_range':[min(p['ground_y'] for p in grows),max(p['ground_y'] for p in grows)],'G1_materials':dict(Counter(p['ground'] for p in grows)),'ground_definition':'WORLD_SURFACE downward stripping explicit vegetation; trunks are separately inventoried and avoided, not declared removable','candidate_profiles':[{k:c[k] for k in ('id','gross_usable_area','surface_elevation_range','median_ground_y','relief','adjacent_max_step','adjacent_mean_step','ground_materials')} for c in candidates],'cache_comparison':delta,'witness_columns':[{'x':p['x'],'z':p['z'],'surface_y':p['surface_y'],'ground_y':p['ground_y'],'ground':p['ground'],'top':p['top']} for p in grows[::137]],'local_raw':'surface.json.gz retained Local-only'}
s.write(s.OUT/'surface-terrain.json',surface)
s.write(s.OUT/'existing-content-audit.json',{'status':'READ COMPLETE / PROVENANCE LIMITS','scope':'67 selected terrain/entity/POI chunks; candidate buffers precisely filtered','candidate_buffers':[{k:c[k] for k in ('id','buffer_area','above_buffer_palette','identified_artificial_surface','block_entities_in_buffer','entities_in_buffer')} for c in candidates],'block_entities':content['block_entities'],'poi_records':content['poi_records'],'structure_starts':content['structure_starts'],'entity_summary':dict(Counter(e['id'] for e in content['entities'])),'deep_item_note':'item entities elsewhere in scope at negative Y are outside shallow candidate volume; not treated as a mine or player structure','natural_material_provenance':'grass/dirt/packed_mud/stone/logs may be world-generated or placed; material-only query cannot establish actor/history','world_writes':0})
s.write(s.OUT/'subsurface-audit.json',{'status':'CURRENT SNAPSHOT SHALLOW READ COMPLETE','depth_below_ground':12,'buffer_blocks':4,'candidate_audits':[{'id':c['id'],'buffer_geometry':c['buffer_geometry'],**c['subsurface']} for c in candidates],'not_claimed':['No deep cave survey','No engineering bearing capacity certification','No proof of absence of natural-material player structure','No mine/resource district inference'],'world_writes':0})
pathpts=[p for r in s.read(s.PLAN/'movement-network.json')['routes'][:2] for p in r['path']]
logs=[[x,z] for x,z,_ in pathpts if any('_log' in n for yy,n in by[(x,z)]['above'])]
leaves=sum(any('leaves' in n and yy<=by[(x,z)]['ground_y']+2 for yy,n in by[(x,z)]['above']) for x,z,_ in pathpts)
s.write(s.OUT/'access-drainage-audit.json',{'status':'LOCAL RELATION WITNESSES / NOT ROAD DESIGN','candidate_access':[{'id':c['id'],'path':c['access_witness'],'steps':c['access_steps'],'role':c['access_loading_relation']} for c in candidates],'drainage':[{'id':c['id'],'non_rising_witness':c['drainage_witness'],'local_pit_check':c['local_pit_check'],'note':c['drainage_water_note']} for c in candidates],'main_corridor_current_obstructions':{'trunk_columns':logs,'low_leaf_columns_in_stored_path_sequence':leaves,'meaning':'Planning clearance is not a cleared existing road; do not promise cart access; future design must retain circulation and address vegetation under separate authorization'},'potable_water':'NOT CONFIRMED; nearby water not assumed potable; supply via corridor and safe storage/fire reserve is a planning possibility, not an installed system','drainage_limit':'local non-rising path to lower terrain only; not rainfall simulation or a sewage outlet design','world_writes':0})
audit=s.read(s.CACHE/'capture.json');uid=audit.pop('singleplayer_uuid',None)
if uid is not None:audit['singleplayer_uuid_sha256']=hashlib.sha256(json.dumps(uid).encode()).hexdigest()
audit['cache_comparison']={k:v for k,v in delta.items() if k!='changes'};audit['cache_change_details']=delta['changes'];audit['extra_visual_ray_columns']=len({tuple(p[:2]) for v in visual for p in v['ray']});audit['visual_ray_columns_outside_surface_scope']=len({tuple(p[:2]) for v in visual for p in v['ray']}-set(by));audit['extra_visual_ray_reason']='standing-eye occlusion from Commons interface to three sites, queried only exact rays from same current region snapshot'
audit['source_files_unchanged_at_final_check']=all(s.sha(s.WORLD/r['world_relative'])==r['sha256'] for r in audit['snapshot_files']);assert audit['source_files_unchanged_at_final_check']
audit['final_source_check_at']=s.utc();s.write(s.OUT/'current-world-audit.json',audit)
s.write(s.CACHE/'visual-rays.json',visual)
print('lightweight site evidence complete; recommended S1',rec['gross_usable_area'],'columns; visual blockers',[(v['site'],len(v['blocked_samples'])) for v in visual])
