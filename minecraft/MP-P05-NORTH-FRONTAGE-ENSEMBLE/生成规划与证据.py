"""任务外围复现脚本：仅读取显式父包和事实证据，写入本归档；不加载或写入游戏。"""
from pathlib import Path
import json, gzip, hashlib, math, shutil, datetime
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'MP-P04-WEST-APPROACH'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,obj):
 p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(x,z,poly):
 hit=False
 for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1]):
  if (b>z)!=(d>z) and x<(c-a)*(z-b)/(d-b)+a:hit=not hit
 return hit
def distance(p,line):
 vals=[]
 for a,b in zip(line,line[1:]):
  dx,dz=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz)))
  vals.append(math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dz))
 return min(vals)
for d in ['sources','evidence','maps']: (ROOT/d).mkdir(exist_ok=True)
(ROOT/'.gitattributes').write_text('* -text\n',encoding='utf-8')
parent=read(PARENT/'planning-data.json')
parcels=[v for v in parent['parcels'] if v['id'] in ['PARCEL-01','PARCEL-02']]
lanes=[v for v in parent['lanes'] if v['id'] in ['LANE-02','LANE-04']]
spaces=[v for v in parent['shared_spaces'] if v['id']=='SPACE-01']
packages=read(PARENT/'implementation-packages.json')
save('sources/parent-extract.json',{'source_revision':'r1','authority':'DESIGN_PROPOSAL','packages':[p for p in packages if p['id']=='PACKAGE-01'], 'public_contract':[p for p in packages if p['id']=='PACKAGE-03'],'parcels':parcels,'lanes':lanes,'shared_spaces':spaces})
canon=ROOT.parent/'建筑师/world/civilizations/CIV-001/README.md'
shutil.copyfile(canon,ROOT/'sources/CIV-001-README.md')
for n in ['architecture-kit-requirements','planning-artifacts-and-maps','morphology-parcels-and-density','human-geography-kernels','surface-substrate-landcover','flows-externalities-and-demand','causal-growth-model','settlement-capacity-and-scale']:
 shutil.copyfile(PARENT/f'sources/skill/references/{n}.md',ROOT/f'sources/skill/references/{n}.md')
assert sha(ROOT/'sources/skill/SKILL.md')==sha(PARENT/'sources/skill/SKILL.md'),'Skill snapshot mismatch'
prov=read(PARENT/'evidence/world-read-provenance.json')
checks={}
for rel,expected in prov['source_and_snapshot_hashes'].items():
 src=Path(prov['source_path'])/rel;snap=Path(prov['read_snapshot'])/rel
 checks[rel]={'current':sha(src),'snapshot':sha(snap),'expected':expected['source_sha256']}
 assert len(set(checks[rel].values()))==1,'Evidence stale: stop generation'
save('evidence/current-source-check.json',{'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_path':prov['source_path'],'files':checks,'world_writes':0,'method':'File hashes only; no game, server, chunk generation or save API','limitation':'Only the three relevant files; not entire save or collision validation'})
shutil.copyfile(PARENT/'evidence/world-read-provenance.json',ROOT/'evidence/inherited-world-read-provenance.json')
surface=json.loads(gzip.decompress((PARENT/'evidence/surface-crop.json.gz').read_bytes()))
near=json.loads(gzip.decompress((PARENT/'evidence/near-ground.json.gz').read_bytes()))
bounds=[746,1620,799,1646]
def inbounds(x,z):return bounds[0]<=x<=bounds[2] and bounds[1]<=z<=bounds[3]
surface['columns']=[c for c in surface['columns'] if inbounds(c[0],c[1])]
surface['bounds']=bounds
surface['substrate_witnesses']=[]
surface['block_entities']=[b for b in surface.get('block_entities',[]) if inbounds(b['x'],b['z'])]
near['columns']=[c for c in near['columns'] if inbounds(c['x'],c['z'])];near['bounds']=bounds
near['block_entities']=[b for b in near['block_entities'] if inbounds(b['x'],b['z'])]
for name,obj in [('surface',surface),('near-ground',near)]:
 (ROOT/f'evidence/{name}.json.gz').write_bytes(gzip.compress(json.dumps(obj,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
cols={(c['x'],c['z']):c for c in near['columns']}
surf={(c[0],c[1]):c for c in surface['columns']}
air={i for i,s in enumerate(near['palette']) if s.split('[')[0] in ['minecraft:air','minecraft:cave_air','minecraft:void_air']}
zones=[];stats=[]
for i,p in enumerate(parcels,1):
 cells=[(x,z) for x,z in cols if inside(x+.5,z+.5,p['polygon'])]
 masks={'FRONT_THRESHOLD':[],'PRIVATE_YARD':[],'FLEX_BUILDING_SEARCH':[],'NARROW_SERVICE':[]}
 for x,z in cells:
  dist=distance((x+.5,z+.5),p['frontage'])
  if dist<=1.4:key='FRONT_THRESHOLD'
  elif (i==1 and x<755) or (i==2 and x>=789):key='PRIVATE_YARD'
  elif i==2 and x<778:key='NARROW_SERVICE'
  else:key='FLEX_BUILDING_SEARCH'
  masks[key].append([x,z])
 for role,mask in masks.items():
  if mask: zones.append({'id':f'Z{i}-{role}','parcel_ref':p['id'],'role':role,'cells':mask,'authority':'DESIGN_PROPOSAL','geometry_semantic':'ILLUSTRATIVE_RELATION_ALLOCATION_NOT_FOOTPRINT','adaptable':'可重分配；保留家庭开敞空间、门前停留不占公共通行及单户完整生活；建筑占地由Builder证明'})
 stat={'parcel':p['id'],'cell_count':len(cells),'ground_y_range':[min(cols[c]['ground_y'] for c in cells),max(cols[c]['ground_y'] for c in cells)],'surface':dict(Counter(surface['palette'][surf[c][4]] for c in cells)),'air_to24_columns':sum(any(k in air for k in cols[c]['state_ids'][:24]) for c in cells),'above4_nonair_columns':sum(any(k not in air for k in cols[c]['state_ids'][25:]) for c in cells),'zone_counts':{k:len(v) for k,v in masks.items()}}
 stats.append(stat)
save('evidence/parcel-analysis.json',{'authority':'DERIVED','sample_semantics':'integer world columns, polygon selection at x+.5/z+.5; ground_y is block Y, not walking elevation','stats':stats,'limitations':['No air observed to24 does not certify foundations','Surface rock does not prove resource yield','Deep block entities are not identified ownership','Actual movement and future building usable routes UNVERIFIED']})
thresholds=[{'id':'TH-01','parcel_ref':'PARCEL-01','search_line':[[755,1634.9],[759,1633.5]],'role':'修理交接/顾客到达；暂停在户内门前，不占LANE-04','route_ref':'LANE-04'}, {'id':'TH-02','parcel_ref':'PARCEL-01','search_line':[[762,1632.5],[766,1631.5]],'role':'家庭与日需进入；与脏修理分流或错时','route_ref':'LANE-04'}, {'id':'TH-03','parcel_ref':'PARCEL-02','search_line':[[783,1633.4],[786,1636]],'role':'复核与约定短宿到达；无通宵公共穿堂','route_ref':'LANE-04'}, {'id':'TH-04','parcel_ref':'PARCEL-02','search_line':[[788,1635.1],[791,1633.9]],'role':'家庭/洁净补给至东端内院；经公共接口协调接入东口','route_ref':'LANE-02 / LANE-04'}]
for t in thresholds:
 t.update(authority='DESIGN_PROPOSAL',geometry_semantic='ENTRY_SEARCH_SEGMENT_NOT_DOOR',height_rule='顺应所在门前地段，Builder选择精确门槛与步级；不得借台阶或门扇侵占通行',observed_nearest_ground_y=[cols[(round(x),round(z))]['ground_y'] for x,z in t['search_line']],access_status='RIGHTS_AND_MOVEMENT_UNVERIFIED')
relations=[{'from':'LANE-04','to':'TH-01','mode':'pedestrian / hand-carried repair item','rule':'院内完成停留；公共院首卸后才手提入户'}, {'from':'TH-01','to':'Z1-FLEX_BUILDING_SEARCH','mode':'customer/work','rule':'接单近门前；家庭私域不充作穿行道'}, {'from':'TH-02','to':'Z1-PRIVATE_YARD','mode':'household / clean supplies','rule':'户内受控通达，可由建筑内部边缘通过；不强制额外后巷'}, {'from':'TH-03','to':'Z2-FLEX_BUILDING_SEARCH','mode':'review / invited guest','rule':'来客不必穿越家庭院落；短宿与复核可错时共用'}, {'from':'TH-04','to':'Z2-PRIVATE_YARD','mode':'household / clean supplies','rule':'东端院内到达；不得转成封闭东口的装卸院'}, {'from':'Z2-NARROW_SERVICE','to':'Z2-FLEX_BUILDING_SEARCH','mode':'private service','rule':'窄尾仅候选储物/服务或开敞，不要求独立卧室'}, {'from':'Z1-PRIVATE_YARD','to':'Z2-PRIVATE_YARD','mode':'NONE','rule':'两户不依赖彼此家庭院落作为公共捷径；没有未经批准的共用后巷'}]
conditions=[{'id':'C-RIGHTS','state':'UNRESOLVED','resolve_before':'world write / permanent occupation','owner':'地方权利主体与公共接口协调者（角色提案，非已任命机构）','requirement':'核实两户用益、LANE-04连续地役及东口权利；没有许可不能以规划取代'}, {'id':'C-SUPPLY','state':'UNRESOLVED','resolve_before':'permanent residence / guest operation','owner':'父聚落供给接口','requirement':'确认水粮来源、搬运频次、洁净到货与污物终端；本包只容纳户内缓冲，不证明上游水源'}, {'id':'C-GROUND','state':'PARTIAL','resolve_before':'Builder foundation design freeze','owner':'Builder','requirement':'按真实拟用体积复核基底、地下既有物与保护，当前仅地表下24格抽取'}, {'id':'C-ACCESS','state':'UNVERIFIED','resolve_before':'Builder design acceptance','owner':'公共接口设计者+两户Builder','requirement':'协同门前净宽、步级、转弯、落脚面与东口；检验真实使用而非端点连通'}, {'id':'C-CAPACITY','state':'DESIGN_TEST_REQUIRED','resolve_before':'Builder design acceptance','owner':'Builder','requirement':'两户各自生活与院落独立成立；P02先检验附带1–2人约定短宿，拥挤时先缩服务频次而非挤生活或公共路；固定program仍无解则回报父层'}]
data={'id':'MP-P05-NORTH-FRONTAGE-ENSEMBLE','revision':'r1','scale':'URBAN_ENSEMBLE','authority':'DESIGN_PROPOSAL','state':'HANDOFF_READY','review_status':'AWAITING_GPT_AND_OWNER','world_writes':0,'world_write_authorization':False,'parent':'MP-P04-WEST-APPROACH / PACKAGE-01 r1','context':{'fabric_observation_state':'EXISTING_FABRIC_PARTIAL','evolution_logic':'EXISTING_EVOLUTION / local formation hypothesis','historical_maturity':'阶段假说，非批准史实'},'parcels':parcels,'external_public_interfaces':{'lanes':lanes,'spaces':spaces,'authority':'PARENT_PROPOSAL','accounting':'引用公共接口，不计新增私用地，不设计整个公共院'},'parcel_group':{'id':'GROUP-01','parcel_refs':['PARCEL-01','PARCEL-02'],'households':2,'accounted_columns':269,'continuous_polygon_area':273,'building_coverage':'不将地块面积当建筑面积；见各包设计试配','separate_from':'公共路带/院落背景'},'relationship_allocation':zones,'frontage_thresholds':thresholds,'relations':relations,'conditions':conditions,'source_refs':['SRC-PARENT','SRC-CANON','SRC-SURFACE','SRC-NEAR','SRC-SKILL']}
save('planning-data.json',data)
commonfixed=['保留两户独立生活与家庭开敞空间；不新增第三户','朝向父包门前公共接口，停留/门扇/服务不得消灭公共通行','不能把公共院或户间间隙私有化；不强迫借另一户私域通行','普通分段地形适应，不将组团与公共院重做为整片等高平台','不得擅动未知地下现状；权利与供给仍为条件']
adapt=['exact footprint within envelope','room arrangement / exact Plan and Section','floor count and floor heights','roof / facade / openings','structural and tectonic system','foundation / drainage / local threshold geometry','block palette and Minecraft translation','门位等价移位、关系分配mask重划，保留接口语义']
bps=[]
for i,p in enumerate(parcels,1):
 bps.append({'id':f'BDP-0{i}','recipient':'minecraft-builder','scale':'URBAN_ENSEMBLE','scope':p['id'],'why':p['why'],'upstream_anchors_flows':['SPACE-01西首卸 / LANE-04步行','LANE-02东轻载'],'spatial_envelope':p['polygon'],'envelope_semantic':'parcel not exact building footprint','required_adjacency':[r for r in relations if f'Z{i}-' in r['to'] or f'Z{i}-' in r['from']],'required_access':[t for t in thresholds if t['parcel_ref']==p['id']],'shared_space_service_relation':'公共部分仍属MP-P04 PACKAGE-03；两户共担门前通行协调，不增加共用后院','program_requirements':(['单户完整居住、做饭、休息、日需和污物暂存','门前接单、小件修理、工具短储与值守','家庭内院；不强制冶炼炉或大宗矿石堆场'] if i==1 else ['单户完整居住和独立家庭内院','手提小件/单据复核、值守','附带约定短宿先按1–2人设计试配，不是旅店；不足时回报而不挤占家庭空间','窄西尾不承担独立居室的刚性要求']),'capacity':{'households':1,'area_columns':p['metrics']['cell_center_area'],'built_footprint_test_range':([55,85] if i==1 else [45,70]),'range_authority':'PLANNING_ASSUMPTION / nonbinding design budget, not demonstrated floor area','priority':'公共通行、单户生活、院落先成立，再证明附带服务；不以提高户数消化投资'},'historical_growth_stage':'H2下肩日常修理稳定后形成两户经营；非实存年代','architecture_kit_requirements':{'state':'HYPOTHESIS','canon_family':'东域前现代石木/贴山适应能力；具体系统由Builder','capabilities':['混合工作生活边界','分段门前与受控私院','洁净补给和脏服务的分离或错时','裸岩基底适应与节制地形施工'],'variation':'P01较深修理户 / P02较浅复核户，不复制同屋'},'planner_fixed':commonfixed+(['修理接单面向西来首卸后的手提流'] if i==1 else ['复核面向东轻载联系，不能堵东口','家庭生活优先于短宿峰值；附带短宿不能扩张为公共旅店']),'builder_adaptable':adapt,'dependencies':['BDP-00接口联审',*[c['id'] for c in conditions]],'known_uncertainty':conditions,'implementation_note':'可直接开展Architecture Design；不得施工。房屋冻结前和公共接口共同复核','upstream_issue_protocol':{'trigger':'普通门位调整、分段落脚、服务错时、户内重排仍无法满足固定关系','return':['冲突约束','拟用体积/使用证据','有界适应尝试','最小父包决定'],'no_silent_change':['地块扩张','户数','封公共路','取消必需生活或全部既定服务']},'world_write_authorization':False})
bps.insert(0,{'id':'BDP-00','recipient':'minecraft-builder','scale':'URBAN_ENSEMBLE','scope':'两户门前接口联审，非公共院建设包','why':'共享前沿若分开定高程会将通路剩余空间吞掉','spatial_envelope_refs':['TH-01','TH-02','TH-03','TH-04','LANE-04','LANE-02接点'],'planner_fixed':['父包LANE-04名义2格步行、LANE-02名义3格轻载关系保留；真实净宽由设计验证','门前停留进入各自用地，公共通行连续','污物清运与洁净补给错时且封闭搬运；不是已验证卫生能力'],'builder_adaptable':adapt,'dependencies':['MP-P04 PACKAGE-03协调','C-RIGHTS','C-SUPPLY'],'program_requirements':['共同门前连续通行和各户受控入口','对公共接口提出最小门位/高程协商'],'historical_growth_stage':'不对应新历史建筑','implementation_note':'先协调后冻结两户设计；仅输出接口设计要求，不授权改公共包','known_uncertainty':conditions,'world_write_authorization':False})
save('builder-design-packages.json',bps)
save('growth-and-flows.json',{'authority':'PLANNING_ASSUMPTION / DESIGN_PROPOSAL','actors':[{'role':'修理经营户','interest':'靠近首卸获取小修理收入，同时保护家庭生活','burden':'本户局部适应与工具储备','veto':'土地权利人、共同通行者可拒绝占路'}, {'role':'复核值守户','interest':'东口日常轻载交往带来业务，少量约定过夜补收入','burden':'较浅地块需要限制服务规模','veto':'家庭成员及共同通行者'}, {'role':'公共接口协调者/地方权利人','interest':'首卸与轻载通路保持公共作用','authority':'角色提案，不虚构已成立委员会或地役许可','burden':'共同路面与清运/洁净到货协议'}],'historical_growth':[{'id':'H1','cause':'间歇交割需要临时修理，尚未证明常住供给','choice':'先日间服务和可撤离工具暂存','feedback':'若需求稳定才值得家庭迁入；不凭未来矿产吞吐建大工坊'}, {'id':'H2','cause':'日常需求和供给、用益协商成立时','choice':'两户形成；下肩修理、上沿复核，共同保留门前通行','feedback':'前沿价值上升，经营户有圈占动力，地役与户内停留抑制堵路'}, {'id':'H3','cause':'短宿或货流峰值上升','choice':'先预约/错时、限制停留，禁止把窄尾或公共路充卧铺','feedback':'长期超负荷回父层重新分配服务；不是必然扩张'}],'implementation_dependency':['证据/权利/供给条件确认','BDP-00与父公共接口共同协调','BDP-01 / BDP-02建筑设计与实尺度program证明','经另行授权才可能实施；本轮无施工'], 'flows':[{'flow':'小件修理','route':'公共院首卸→TH-01→修理','rhythm':'日间/到货脉冲','stock':'户内工具和少量待修件，不能扩成矿石库存','failure':'峰值暂停收件，不能占LANE-04'}, {'flow':'家庭水粮','route':'已协调来源→公共接口→TH-02/TH-04→户内缓冲','rhythm':'每日使用，补给频次待来源确认','stock':'日需缓冲位置由Builder留出，储量须按实际人数补给周期校核','failure':'缺供暂停常住/客宿，无本地井证据'}, {'flow':'来客复核与短宿','route':'东口/门前→TH-03→受控经营空间','rhythm':'约定到达；夜间非公共穿堂','stock':'小量行李不占家庭院或路线','failure':'拒绝超额/回父节点协调，不新增户数'}, {'flow':'污物/脏修理物','route':'户内封闭暂存→同前沿错时搬运→待确认合法终端','rhythm':'避开洁净补给与来客峰值','stock':'与洁净水粮分置','failure':'终端无着落不能视为常住条件已闭合'}]})
# 地图以真实逐列地表作底；色块是关系试配，不代表建筑设计。
fontpath='C:/Windows/Fonts/msyh.ttc'
def font(n):return ImageFont.truetype(fontpath,n)
colors={'FRONT_THRESHOLD':'#e8a466','PRIVATE_YARD':'#91bfa1','FLEX_BUILDING_SEARCH':'#adc0d4','NARROW_SERVICE':'#c4b0ce'}
im=Image.new('RGB',(2800,1900),'#f6f3eb');dr=ImageDraw.Draw(im)
dr.text((80,35),'MP-P05｜北侧两户混合前沿 · 关系规划 r1',font=font(48),fill='#243b40')
dr.text((80,105),'URBAN_ENSEMBLE · DESIGN_PROPOSAL · 世界写入 0 · 非建筑平面图',font=font(27),fill='#45585c')
S=43;ox=100;oy=255
def xy(p):return (ox+(p[0]-746)*S,oy+(p[1]-1620)*S)
for (x,z),c in cols.items():
 y=c['ground_y'];v=max(120,min(234,228-(y-128)*10));px,pz=xy((x,z));dr.rectangle((px,pz,px+S,pz+S),fill=(v,min(245,v+8),min(245,v+5)))
for sp in spaces:dr.polygon([xy(p) for p in sp['polygon']],fill='#dbd1ad')
for zone in zones:
 for x,z in zone['cells']:
  a,b=xy((x,z));dr.rectangle((a,b,a+S,b+S),fill=colors[zone['role']])
for x in range(750,800,5):
 px,pz=xy((x,1620));dr.line((px,oy,px,oy+27*S),fill='#c0c1b8',width=1);dr.text((px-22,oy-43),str(x),font=font(22),fill='#344347')
for z in range(1620,1647,5):
 px,pz=xy((746,z));dr.line((ox,pz,ox+54*S,pz),fill='#c0c1b8',width=1);dr.text((12,pz-15),str(z),font=font(22),fill='#344347')
for (x,z),c in cols.items():
 if x%3==0 and z%3==0:
  a,b=xy((x+.15,z+.2));dr.text((a,b),str(c['ground_y']),font=font(16),fill='#626e66')
for p in parcels:dr.line([xy(q) for q in p['polygon']+[p['polygon'][0]]],fill='#293d4d',width=5)
for lane in lanes:
 dr.line([xy(q) for q in lane['points']],fill='#eee7cf',width=int(lane['width']*S),joint='curve')
 dr.line([xy(q) for q in lane['points']],fill='#7d683b',width=4,joint='curve')
for i,t in enumerate(thresholds,1):
 dr.line([xy(q) for q in t['search_line']],fill='#b14536',width=9)
 a,b=xy(t['search_line'][0]);dr.ellipse((a-21,b-22,a+21,b+22),fill='#fff8ed',outline='#b14536',width=3);dr.text((a-10,b-18),str(i),font=font(23),fill='#b14536')
labels=[((756,1626),'P01｜修理 + 一户生活'),((779,1623),'P02｜复核 + 一户生活'),((751,1641),'SPACE-01 公共首卸院（仅上下文）'),((780,1643),'LANE-02 → 东轻载出口'),((759,1636),'LANE-04 连续步行地役（待确认）')]
for p,t in labels:
 a,b=xy(p);bb=dr.textbbox((a,b),t,font=font(23));dr.rectangle((bb[0]-5,bb[1]-4,bb[2]+5,bb[3]+4),fill='#fffaf0');dr.text((a,b),t,font=font(23),fill='#263b45')
dr.text((2480,230),'N ↑\n-Z',font=font(36),fill='#243b40')
# 公共院超出当前事实裁剪边界，不让背景多边形覆盖图例。
dr.rectangle((0,oy+27*S+1,2800,1900),fill='#f6f3eb')
for route in [[[763,1632],[763,1628],[753,1630]],[[789,1634],[790,1631]],[[784,1633],[783,1630]]]:
 for a,b in zip(route,route[1:]):
  pa,pb=xy(a),xy(b)
  for k in range(0,20,2):dr.line((pa[0]+(pb[0]-pa[0])*k/20,pa[1]+(pb[1]-pa[1])*k/20,pa[0]+(pb[0]-pa[0])*(k+1)/20,pa[1]+(pb[1]-pa[1])*(k+1)/20),fill='#485652',width=4)
 a,b=xy(route[-1]);dr.ellipse((a-7,b-7,a+7,b+7),fill='#485652')
legend=[('FLEX_BUILDING_SEARCH','建筑搜索区'),('PRIVATE_YARD','家庭开敞空间'),('FRONT_THRESHOLD','户内门前缓冲'),('NARROW_SERVICE','窄尾服务/留空')]
for j,(k,t) in enumerate(legend):
 y=1490+j*58;dr.rectangle((100,y,138,y+32),fill=colors[k]);dr.text((155,y-4),t,font=font(27),fill='#344347')
dr.text((670,1480),'色块为可调整关系试配；虚线为户内关系，不是精确通道。\n1 修理接单  2 家庭/洁净日需  3 复核/约定短宿  4 家庭东院\n两户共 269 地表列；公共空间另属父包，不并入私用面积。\n底图数字 = 实测地表方块 Y；道路为父规划，非现状道路。\n当前证据：2026-09-13调查，2026-09-14原文件哈希复核。',font=font(28),fill='#344347',spacing=14)
dr.line((100,1800,100+5*S,1800),fill='#263b45',width=5);dr.text((100,1820),'5 blocks · 等比例 X/Z',font=font(24),fill='#344347')
dr.text((750,1820),'裸岩地表 / 下24格无空气观测 ≠ 基础安全、通行或权属认证',font=font(27),fill='#7a4d40')
im.save(ROOT/'maps/01-组团关系与真实地形.png')
# 现状地形剖面保留原Y，仅描述接口，不生成拟建建筑剖面。
im=Image.new('RGB',(2800,1700),'#f6f3eb');dr=ImageDraw.Draw(im)
dr.text((90,45),'门前与基底证据｜现状剖面，非建筑 Section',font=font(47),fill='#243b40')
dr.text((90,120),'横纵比例一致 · 地表方块顶面 = ground_y + 1 · 门槛与楼层高程未设计',font=font(28),fill='#45585c')
profiles=[]
for j,z in enumerate([1630,1634]):
 top=260+j*615;unit=43;base=top+480
 samples=[]
 for x in range(749,796):
  gy=cols[(x,z)]['ground_y'];px=120+(x-749)*unit;py=base-(gy+1-125)*unit
  dr.rectangle((px,py,px+unit,base),fill='#a7aaa1');dr.line((px,py,px+unit,py),fill='#394b48',width=5);samples.append([x,z,gy])
  if x%5==0:dr.text((px,base+18),str(x),font=font(22),fill='#394b48')
 for y in range(126,138,2):
  py=base-(y-125)*unit;dr.line((110,py,2160,py),fill='#c4c7bf',width=1);dr.text((45,py-16),str(y),font=font(22),fill='#394b48')
 dr.text((2220,top+10),f'Z = {z}\n西低 → 东高\n\n分段入口适应\n不锁定楼层\n不抹平整个前沿',font=font(30),fill='#394b48',spacing=15)
 profiles.append({'z':z,'samples':samples,'semantic':'OBSERVED GROUND PROFILE, not architecture or movement'})
dr.text((100,1550),'X749–795 / Z1630、1634 · 见规划图同坐标 · 无浅空气不等于承载力已验证',font=font(28),fill='#7a4d40')
im.save(ROOT/'maps/02-现状地形与门前高差.png');save('evidence/sections.json',profiles)
# 验证仅证明资料与几何账本；质量Gate单独由规划推理记录。
sets=[{(x,z) for x,z in cols if inside(x+.5,z+.5,p['polygon'])} for p in parcels]
zonecells=[tuple(c) for q in zones for c in q['cells']]
lane_overlap={l['id']:sum(distance((x+.5,z+.5),l['points'])<l['width']/2 for x,z in sets[0]|sets[1]) for l in lanes}
validation={'world_writes':0,'parcel_counts':[len(s) for s in sets],'parcel_overlap':len(sets[0]&sets[1]),'zone_partition_unique':len(zonecells)==len(set(zonecells))==269,'parent_parcel_geometry_unchanged':True,'public_lane_envelope_overlap_columns':lane_overlap,'note':'如父规划路带与私用列交叠，通行优先；关系mask不是可封闭建筑面','missing_surface_columns':len(set(cols)-set(surf)),'building_design': 'NOT_PERFORMED','collision_and_usable_route':'UNVERIFIED','foundation_stability':'UNVERIFIED','rights':'UNRESOLVED','data_checks_not_quality_proof':True}
assert [len(s) for s in sets]==[151,118] and not sets[0]&sets[1] and validation['zone_partition_unique']
save('validation.json',validation)
register=[]
for id,path,auth,use in [('SRC-PARENT',PARENT/'implementation-packages.json','DESIGN_PROPOSAL','PACKAGE-01 and direct PACKAGE-03 interface only'),('SRC-PARCELS',PARENT/'planning-data.json','DESIGN_PROPOSAL','P01/P02 L02/L04 SPACE01 only'),('SRC-CANON',canon,'APPROVED_CANON','CIV001 minimal canon; no architecture answer links followed'),('SRC-SURFACE',PARENT/'evidence/surface-crop.json.gz','OBSERVED','factual cropped surface'),('SRC-NEAR',PARENT/'evidence/near-ground.json.gz','OBSERVED','factual shallow read'),('SRC-SKILL',ROOT/'sources/skill/SKILL.md','OWNER_CONSTRAINT','v0.4 workflow')]:
 register.append({'id':id,'path':str(path),'sha256':sha(path),'authority':auth,'used_for':use})
save('sources/source-register.json',{'skill_commit':(ROOT/'sources/skill-revision.txt').read_text().strip(),'sources':register,'isolation_note':'未读取独立审核内容。一次父包JSON深度1输出连带出现PACKAGE-02摘要，未作设计依据；归档和实际几何只取PACKAGE-01及公共接口。远端FF仅报告新增review文件名，未打开内容。','freshness':'Source hashes match inherited readonly snapshot; not a new simulation'})
print(json.dumps({'stats':stats,'validation':validation},ensure_ascii=False,indent=2))
