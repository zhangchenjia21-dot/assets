"""本轮显式空间决定的可复现数据/地图生成；几何计算验证表达，不替代因果判断。"""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;REPO=R.parents[1];C=R.parents[3]/'MP-P03-cache';a=np.load(C/'terrain.npz');h=a['height'];surf=a['surface'];leaf=a['leaf']
def dump(p,v):(R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
parent=json.loads((REPO/'minecraft/MP-P02R-EAST/implementation-packages.json').read_text(encoding='utf8'))[0]
pdata=json.loads((REPO/'minecraft/MP-P02R-EAST/planning-data.json').read_text(encoding='utf8'))
dump('sources/parent-package.json',{'package':parent,'node':[n for n in pdata['nodes'] if n['id']=='NODE-01'][0],'routes':[q for q in pdata['routes'] if q['id'] in parent['flow_refs']],'authority':'PARENT_PLANNING_PROPOSAL_NOT_CANON'})
def area(poly):return abs(sum(x*z2-x2*z for (x,z),(x2,z2) in zip(poly,poly[1:]+poly[:1])))/2
def mask(poly):
 im=Image.new('1',(320,288));ImageDraw.Draw(im).polygon([(x-640,z-1488) for x,z in poly],fill=1);return np.array(im,dtype=bool)
def metrics(poly):
 m=mask(poly);ss=surf[m];hs=h[m];return {'polygon_area_blocks2':area(poly),'sample_columns_including_edge':int(m.sum()),'ground_y_min_median_max':[int(hs.min()),float(np.median(hs)),int(hs.max())],'surface_ratios':{k:round(float((ss==i).mean()),4) for i,k in enumerate(['rock','soil','sand_gravel','water','lava','other'])},'leaf_columns':int((leaf[m]>0).sum()),'meaning':'当前表面统计，不是基底承载或已可建面积'}
districts=[
 dict(id='DISTRICT-01',name='西接坡交割与修理前沿',polygon=[[748,1625],[765,1620],[794,1626],[798,1648],[782,1668],[755,1666],[748,1646]],area_range=[1200,1600],households=[4,6],why='货物从西南方向爬升到台面后需要卸载、复核与修理；照看者就近居住，不让重货穿过全聚落',morphology='短段混合前沿面向进场与卸载空地；背侧接家庭小院；砂砾斜带处让出通行',frontage='面向ROUTE-01和SPACE-01；修理与居住共享前后进出但分时卸货',density='局部中等，入口留宽；向西随坡增大停止',phase='GROWTH-01'),
 dict(id='DISTRICT-02',name='内台共享储备与守约前沿',polygon=[[795,1588],[815,1585],[835,1595],[839,1617],[831,1642],[809,1646],[797,1635]],area_range=[1500,2000],households=[5,7],why='交割形成持续保管和可信交易需求；抬离入口拥堵但仍靠近驮运卸载，家庭与值守共同维持储备',morphology='围绕两个相连公共空地形成折段前沿；共享服务抗分割，家庭使用可逐渐细分',frontage='面向SPACE-02/03与ROUTE-02；公共入口不与后侧服务抢同一门口',density='核心较连续，院落与横向通路打断；不是封闭仓储园区',phase='GROWTH-02'),
 dict(id='DISTRICT-03',name='东上台寄宿与日常混合簇',polygon=[[840,1583],[862,1579],[877,1591],[879,1613],[869,1630],[845,1624],[839,1606]],area_range=[800,1000],households=[3,4],why='周期代表和商旅需要停留；较高而缓的岩台靠近共享服务，又能减少入口牲畜干扰',morphology='断续前沿与共享生活院交替；不占满岩台、不把它变成纯住宅区',frontage='朝向ROUTE-02/03与生活共同院，保留后侧通行',density='核心一侧稍紧，东缘断续；不得跨砂砾带持续扩张',phase='GROWTH-03')]
for d in districts:d.update(authority='DESIGN_PROPOSAL',metrics=metrics(d['polygon']),geometry_semantics='APPROXIMATE_DISTRICT_RELATION_ENVELOPE_NOT_PARCELS',source_refs=['SRC-LIVE','SRC-PARENT','SRC-CANON'])
routes=[
 dict(id='ROUTE-01',name='西南接近与首段驮运',points=[[704,1660],[730,1658],[749,1650],[761,1644],[776,1641]],width_range=[4,6],flow='驮队、货物、入口访客',origins=['上游中域/西肩接口方向'],destinations=['SPACE-01'],why='先到较低西肩卸载，不让整队重货横穿生活簇',stage='GROWTH-01',priority='FREIGHT_PRIMARY'),
 dict(id='ROUTE-02',name='内台共享脊线通行',points=[[776,1641],[790,1635],[802,1628],[819,1621],[827,1614],[837,1612],[852,1610]],width_range=[3,5],flow='短距搬运、步行、居民、代表',origins=['SPACE-01'],destinations=['SPACE-02','SPACE-03','SPACE-04'],why='沿台面逐渐升高，连接公共空地；入口卸载后减小运输强度',stage='GROWTH-02',priority='MIXED_PRIMARY'),
 dict(id='ROUTE-03',name='前沿后侧服务回路',points=[[790,1635],[798,1608],[804,1597],[820,1600]],width_range=[2,3],flow='住户、轻载、值守；不承诺车行',origins=['DISTRICT-01'],destinations=['DISTRICT-02'],why='成熟前沿增加门前停留，后侧需要不穿公共交易场的日常通行；不追求闭合格网',stage='GROWTH-03',priority='PEDESTRIAN_SERVICE'),
 dict(id='ROUTE-04',name='东缘污物搬离预留',points=[[866,1618],[876,1624],[887,1630]],width_range=[2,3],flow='密闭污物与清扫搬运，非明沟',origins=['DISTRICT-03'],destinations=['接口待定'],why='与洁净储备交接分开，但终端处置未证，不可排向岩台下水面',stage='GROWTH-03',priority='CONDITIONAL_SERVICE')]
for q in routes:
 ss=[];dist=0;prev=None
 for p1,p2 in zip(q['points'],q['points'][1:]):
  for t in np.linspace(0,1,max(2,int(math.dist(p1,p2))+1)):
   x,z=[round(a+(b-a)*t) for a,b in zip(p1,p2)];p=(x,z)
   if p==prev:continue
   if prev:dist+=math.dist(p,prev)
   ss.append([round(dist,2),x,z,int(h[z-1488,x-640]),int(surf[z-1488,x-640])]);prev=p
 q.update(authority='DESIGN_PROPOSAL',geometry_semantics='SETTLEMENT_ALIGNMENT_PROPOSAL_ADAPTABLE_AT_DISTRICT',existing_road=False,usable_route='UNVERIFIED_PHYSICAL_MOVEMENT',profile=ss,length_blocks=round(dist,1),height_range=[min(s[3] for s in ss),max(s[3] for s in ss)],max_sampled_step=max(abs(ss[i][3]-ss[i-1][3]) for i in range(1,len(ss))),source_refs=['SRC-LIVE'])
spaces=[
 dict(id='SPACE-01',name='首段卸载与轮候共同地',polygon=[[760,1635],[775,1631],[785,1639],[779,1650],[763,1651]],controller='参与交割的地方共同体协定（提案）',users='驮队、接货家庭、修理者',use='分批卸载与短时轮候；牲畜不进入上台生活院',when='交割日密集，平日保留通行',why_unbuilt='服务准入公约和首段卸载；不能被沿街继承分割'),
 dict(id='SPACE-02',name='守约交接与公共停留',polygon=[[801,1617],[814,1612],[823,1616],[821,1628],[805,1633],[798,1628]],controller='多个共同体共同保管、地方自治不移交',users='居民、交割人、代表',use='核验、分配、日常交易；议事可借共享室内空间',when='日常/周期协商',why_unbuilt='让前沿不阻塞横向步行，不作为唯一东席首都广场'),
 dict(id='SPACE-03',name='洁净接水与储备服务院',polygon=[[813,1597],[823,1595],[831,1603],[826,1610],[816,1608]],controller='受益家庭与保管者',users='居民、运水者',use='封闭容器接收、储备维护；未来集雨贮存需另证',when='每日/补给时',why_unbuilt='维护通道与卫生分隔；不是声称已有泉井'),
 dict(id='SPACE-04',name='东上台日常共同院',polygon=[[848,1605],[861,1604],[868,1608],[865,1616],[852,1620],[845,1614]],controller='周边使用者共同承担清扫',users='家庭、寄宿者、地方仪式参与者',use='日常工作与停留；不常态装卸重货',when='每日',why_unbuilt='家庭/寄宿的共享空间和日照通行需求')]
for s in spaces:s.update(authority='DESIGN_PROPOSAL',metrics=metrics(s['polygon']))
# 前沿带仅表示聚合的潜在建设与前后关系，绝非单栋footprint或固定地块。
bands=[
 ('FRONTAGE-01','DISTRICT-01',[[751,1629],[762,1625],[779,1628],[775,1632],[760,1637],[752,1637]],'朝卸载场，混合维修/门前交易/值守家庭'),
 ('FRONTAGE-02','DISTRICT-01',[[758,1654],[777,1653],[787,1648],[791,1655],[779,1663],[758,1662]],'背接小院，前接轮候场；禁止连续封住出口'),
 ('FRONTAGE-03','DISTRICT-02',[[797,1589],[814,1588],[823,1591],[817,1593],[804,1594],[797,1594]],'后側通行与共享储备值守'),
 ('FRONTAGE-04','DISTRICT-02',[[828,1602],[833,1601],[835,1608],[831,1610],[827,1609]],'共享保管与寄居混合，不沿院周边闭合'),
 ('FRONTAGE-05','DISTRICT-02',[[805,1635],[821,1630],[830,1627],[831,1637],[815,1642],[809,1641]],'面向交接空地，货物留短途搬运'),
 ('FRONTAGE-07','DISTRICT-03',[[871,1606],[876,1608],[876,1614],[870,1619],[868,1615],[870,1610]],'向内院形成断续前沿；后侧留维护'),
 ('FRONTAGE-08','DISTRICT-03',[[843,1618],[851,1623],[860,1621],[861,1626],[853,1626],[844,1623]],'较短生活前沿，留通向内台的缺口')]
frontages=[dict(id=i,district=d,polygon=p,why=w,area_blocks2=area(p),authority='DESIGN_PROPOSAL',semantics='AGGREGATE_FRONTAGE_BAND_NOT_BUILDING_FOOTPRINT',metrics=metrics(p)) for i,d,p,w in bands]
constraints=[
 dict(id='CONSTRAINT-01',name='北缘陡坡与热源观察带',polygon=[[704,1520],[895,1520],[895,1572],[847,1566],[815,1570],[750,1575],[704,1560]],why='北缘坡折、现存熔岩；无需求支付其交通与安全代价',rule='本案无建设分配，实际安全退界由更细调查确定'),
 dict(id='CONSTRAINT-02',name='南部陷落与水面接近未证',polygon=[[817,1675],[844,1671],[872,1682],[878,1715],[853,1770],[815,1770],[801,1730]],why='高台向下急降，观察到下方水面但水质/来源/可持续量未知',rule='不画引水渠、不把就近水面作已证水源，不向下排污'),
 dict(id='CONSTRAINT-03',name='东侧砂砾带暂停扩张',polygon=[[879,1580],[895,1572],[901,1617],[888,1644],[878,1636]],why='砂砾带和坡折使统一扩张失去理由，先核查基底与冲刷',rule='停在当前簇，不填平为第二排均匀街区')]
for c in constraints:c.update(authority='DESIGN_PROPOSAL_ON_OBSERVED',geometry_semantics='INVESTIGATION_HOLD_NOT_STATUTORY_BOUNDARY')
demands=[
 dict(id='DEMAND-01',driver='低地产品与北部共同体交换',users='驮队、保管者、工艺家庭',magnitude='假设每次6–12头驮兽、1–2小队；不是实测货运量',frequency='周期交易/季节更密',maturity='GROWTH-01',dependencies=['ROUTE-01','SPACE-01'],externality='牲畜/噪声/堵塞',response='首段分批卸载；后续轻载'),
 dict(id='DEMAND-02',driver='日常家庭和值守维持服务',users='12–17户压力，17户以上需再证',magnitude='居住与工作嵌合，常住规模LOW',frequency='每日',maturity='GROWTH-02',dependencies=['SPACE-03','ROUTE-03'],externality='水/卫生/日需输入',response='小簇与共享院，水未闭合前不批准常住实施'),
 dict(id='DEMAND-03',driver='交割产生保管和履约',users='多共同体代理人、住户',magnitude='北部服务非唯一东席行政中心',frequency='交割日/协商时',maturity='GROWTH-02',dependencies=['SPACE-02'],externality='准入被单方垄断',response='共享保管和可借用议事空间'),
 dict(id='DEMAND-04',driver='周期访客停留',users='商旅、代表、短期帮工',magnitude='假设8–16短期访客，不转为常住人口',frequency='间歇',maturity='GROWTH-03',dependencies=['SPACE-04','ROUTE-02'],externality='生活拥挤/火/污物',response='混合寄宿与日常共同院，不单独规划旅馆区'),
 dict(id='DEMAND-05',driver='供水与清洁是持久生活前提',users='居民和访客',magnitude='仅供给压力假设：按60–90居民+最多16客、20–30L/人日约1.2–3.18m³/日；动物另计',frequency='每日',maturity='任何常住前',dependencies=['SPACE-03'],externality='饮水污染/搬运负担',response='洁净接水和密闭储存接口；量源不足则减员/日间站分支，不能靠水面像池塘通过Gate')]
for d in demands:d['authority']='PLANNING_ASSUMPTION'
anchors=[dict(id='ANCHOR-01',scale='Settlement',role='ORIGIN_ANCHOR',why='可分批交割的台面与西侧供给关系',when='GROWTH-01',attracts='照看、修理、短时交换',repels='连续重货穿生活院',consequence='西端公共轮候与混合前沿先形成',removal='无交换则缩为小服务点，内部主轴与储备需求消失'),dict(id='ANCHOR-02',scale='Settlement',role='STABILIZING_ANCHOR',why='共同体可信保管与共享准入',when='GROWTH-02',attracts='值守家庭与公共停留',repels='单方圈占公共场',consequence='内台共享储备不按家庭继承零碎分割',removal='公共前沿/保管规模需重算，不能留空壳中心'),dict(id='ANCHOR-03',scale='Settlement',role='CONDITIONAL_SUPPORT_ANCHOR',why='持续可饮用供给未确认，决定能否常住',when='常住分支前',attracts='家庭与寄宿',repels='污物与明排水',consequence='洁净接口与住户压力成对限制',removal='完整常住分支停用，改为小规模日间交换或上报父包')]
growth=[dict(id='GROWTH-01',driver='阶段性货物交割',response='西接坡短时轮候与修理，参与者从已有社区来',constraint='卸载场与通路先稳定，不能被后续沿街占满',next='值守和共享保管需求',independent_viability='自带可饮水并当天返回；未预支完整常住'),dict(id='GROWTH-02',driver='保管频率增加且生活供给成立',response='内台储备与照看家庭逐步嵌入',constraint='洁净接收和公共准入约定，土面斑块不当填充地',next='访客寄宿/密集前沿后侧通行',independent_viability='仅在供水和日需已证的常住分支成立'),dict(id='GROWTH-03',driver='周期访客形成停留压力',response='东上台混合生活簇与后侧轻载回路',constraint='砂砾/北坡/南陷限制扩展，不建立完整环城',next='超过17户优先回父包重分配而非填满岩台',independent_viability='可永久停在较小规模，不假设未来矿都')]
programs=[dict(id='PROGRAM-'+d['id'][-2:],demand_ref=d['id'],functions=d['response'],magnitude=d['magnitude'],adjacency_refs=d['dependencies'],maturity=d['maturity'],externality=d['externality'],sharing='DISTRICT确定共享/嵌入/独立；不指定栋数或房间') for d in demands]
kit={'shared_dna':'成熟石木工程、自治协商与共享履约，东域贴台面分段发展','requirements':['断续混合前沿可接院与轻载背路','基础接触与岩面排水需回应逐点基底，不默认地下室','共享储备维护与洁净输入不穿污物出口','对砂砾转换和土面小斑块可退让，不用巨平台抹平','共同语言允许不同院、转折与服务密度'],'forbidden':['整栋Blueprint复制','统一地块网格','指定roof/palette/窗型','借魔法取消供水']}
plan={'id':'MP-P03-NORTH-ROCK-TERRACE','revision':'r1','scale':'SETTLEMENT','state':'HANDOFF_READY','state_scope':'conditional planning handoff, not permanent settlement feasibility or authorization','parent':'MP-P02R-EAST:r1:PACKAGE-01','authority':'DESIGN_PROPOSAL_PENDING_REVIEW','world_writes':0,'fabric_observation':'EXISTING_FABRIC_PARTIAL','evolution':'EXISTING_EVOLUTION / hypothetical sequence, current authored fabric not established','districts':districts,'routes':routes,'spaces':spaces,'frontages':frontages,'constraints':constraints,'demands':demands,'anchors':anchors,'growth':growth,'programs':programs,'architecture_kit_requirements':kit,'capacity':{'built_fabric_range_blocks2':[3500,4600],'parent_range':[3500,8000],'district_sum':[3500,4600],'gross_envelopes_area':sum(area(d['polygon']) for d in districts),'permanent_households':[12,17],'household_allocation_note':'district max raw 6+7+4=17; min 4+5+3=12','shared_spaces_and_routes':'included in gross built fabric pressure; not added again','frontage_band_area':sum(area(f['polygon']) for f in frontages),'confidence':'LOW','excluded':['外部供水链','上游接近路','生产腹地','土面保留和高风险外缘'],'active_branch':'BRANCH-01 conditional resident scenario; implementation hold'},'branches':[{'id':'BRANCH-01','condition':'可持续饮水、日需、连接和土地使用可解决','form':'图示3500–4600格²混合聚落；12–17户','implementation':'HOLD_UNTIL_EVIDENCE'},{'id':'BRANCH-02','condition':'可短时交割，但常住饮水或日需不成立','form':'只保留首段交割和可撤回日间服务，不实施02/03生活簇；常住0','area_pressure_blocks2':[400,1000],'implementation':'需要回报父包角色/容量变化，不擅改父案'},{'id':'BRANCH-03','condition':'接近/权属/供水约束使任何角色均无兼容位置','form':'UPSTREAM_PLANNING_ISSUE；停止定址'}]}
dump('planning-data.json',plan)
plan['capacity']['calculation']='12–17户×100格²本地生活工作用地 + 2300–2900格²不重复共享服务/场院/通行 = 3500–4600格²；规模假说非面积标准'
plan['retired_objects']=[{'id':'FRONTAGE-06','reason':'浅层空气与接近条件使北段扩张缺乏必要性，撤回而非填洞','replacement':None}]
plan['capacity']['revision_reason']='浅层空隙复核后减少东上台前沿，父包3500–8000缩为3500–4600，不扩大占地补齐上限'
dump('planning-data.json',plan)
packages=[]
for d in districts:
 packages.append(dict(id='PACKAGE-'+d['id'][-2:],parent_plan=plan['id'],parent_revision='r1',parent_scale='SETTLEMENT',child_scale='DISTRICT',recipient='minecraft-planner',scope_ref=d['id'],scope_geometry=d['polygon'],authority='PARENT_PROPOSAL_NOT_CANON',why=d['why'],upstream_fixed=['公共交割由西侧先卸载、内部逐步轻载','共享院与横向通路不得被前沿封闭','多共同体共享不等于唯一东席中心','北坡/南陷/砂砾边缘不以总图理由自动填平','常住分支以供水/日需成立为前提','保持本轮浅层空气带暂不分配建设，不能默认填洞或建地下室'],downstream_to_resolve=['确认本簇实际人工痕迹/权属/旧路，不能按新地清空','逐前沿与院检查基底、空洞、排水；本轮已有8格13层初查和核心逐柱16层复核，深部/结构稳定仍未证','细化block/parcel/frontage演变和共享院面积，不将示意带当楼体','连续步行/驮运坡度、转折、净空；按profile定位问题','供水来源、搬运或收集量、贮存和密闭污物终端，跨包共同闭合'],downstream_adaptable=['本簇内移位/拆分前沿与调整小院','支巷、地块和边界细化','总3500–4600范围内跨包协商容量，不各自取上限扩大总量','若常住分支不成立，按BRANCH-02回退并报告上游'],capacity_hypothesis={'area_range_blocks2':d['area_range'],'households':d['households'],'includes':'共享场院与本地通行在总压力内，不另加'},cross_package_dependencies=['PACKAGE-'+x['id'][-2:] for x in districts if x['id']!=d['id']],source_refs=['SRC-LIVE','SRC-PARENT','SRC-CANON','SRC-SKILL'],revision_triggers=['稳定饮水无法支持12户','入口需要大规模重整才能服务','现存保护对象冲突不可局部避让','扣除公共通行与土面后需求无法容纳'],revision_protocol='最小受影响district/route/capacity先局部调整；若破坏供给/共享关系则回退本案Gate，提交上游问题并标关联包stale，不覆盖父案',expected_outputs=['DISTRICT因果规划','block/parcel/巷道/前沿及阶段图','可追溯JSON和L4交接包','供水/通行/现状未决与修订账本'],world_write_authorization=False,builder_ready=False))
dump('implementation-packages.json',packages)
dump('evidence/planning-geometry-metrics.json',{'districts':[{k:d[k] for k in ['id','metrics']} for d in districts],'frontages':[{k:f[k] for k in ['id','metrics']} for f in frontages],'spaces':[{k:s[k] for k in ['id','metrics']} for s in spaces],'route_profiles':[{k:q[k] for k in ['id','profile','max_sampled_step','length_blocks','height_range']} for q in routes]})

# Owner图：具体展示前沿带、共有院、主通行和后侧通行；保留地表可见而非功能色块。
(R/'maps').mkdir(exist_ok=True)
F=lambda n:ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
colors=np.array([[153,149,142],[153,178,112],[225,197,139],[92,162,190],[228,75,27],[168,129,175]],dtype=np.uint8)
gy,gx=np.gradient(h.astype(float));v=np.clip((h-60)/100,0,1);rgb=np.stack([95+140*v,140+95*v,110+120*v],2)*np.clip(.9-(gx+gy)*.1,.4,1.1)[:,:,None];rgb[surf==3]=colors[3];rgb[surf==4]=colors[4];rgb=np.uint8(np.clip(rgb,0,255))
def dash(d,pts,color,width=2):
 for a,b in zip(pts,pts[1:]):
  L=math.dist(a,b)
  for t in np.arange(0,L,13):
   aa=t/L;bb=min(t+7,L)/L;d.line((a[0]+(b[0]-a[0])*aa,a[1]+(b[1]-a[1])*aa,a[0]+(b[0]-a[0])*bb,a[1]+(b[1]-a[1])*bb),fill=color,width=width)
def map_image(mode='structure',stage=None):
 b=[728,1568,895,1687];scale=6;w=168*scale;hh=120*scale;im=Image.new('RGB',(1590,930),'#f5f1e8');base=rgb if mode=='terrain' else colors[surf];im.paste(Image.fromarray(base[80:200,88:256]).resize((w,hh),Image.Resampling.NEAREST),(70,110));d=ImageDraw.Draw(im)
 xy=lambda p:(70+(p[0]-728)*scale,110+(p[1]-1568)*scale)
 title={'structure':'聚落内部结构与地表','terrain':'聚落内部结构与地形','growth':'假说生长阶段'}[mode]
 d.text((70,22),'MP-P03 | '+title+(' '+stage if stage else '')+' | SETTLEMENT',font=F(28),fill='#223b42');d.text((70,67),'北↑（−Z） 东→（+X） | 框 X728..895 Z1568..1687 | 1格=6px',font=F(18),fill='#223b42')
 for x in range(736,896,16):u,_=xy((x,1568));d.line((u,110,u,830),fill='#c0bbae');d.text((u-15,840),str(x),font=F(16),fill='black')
 for z in range(1584,1688,16):_,vv=xy((728,z));d.line((70,vv,1078,vv),fill='#c0bbae');d.text((10,vv),str(z),font=F(16),fill='black')
 included=[dd for dd in districts if not stage or dd['phase']<=stage]
 for vv in json.loads((R/'evidence/shallow-void-columns.json').read_text(encoding='utf8'))['void_columns']:
  u,vp=xy((vv['x'],vv['z']))
  if 70<=u<1078 and 110<=vp<830:d.rectangle((u,vp,u+5,vp+5),fill='#ae528e')
 for c in constraints:
  pp=[xy(p) for p in c['polygon']]; # 仅在图内绘制适用暂停区线段，防止越界污染图例。
  pp=[p for p in pp if 70<=p[0]<=1078 and 110<=p[1]<=830]
  if len(pp)>1:dash(d,pp,'#a54839',3)
 for dd in included:
  pp=[xy(p) for p in dd['polygon']];dash(d,pp+[pp[0]],'#3a394b',2)
 for q in routes:
  if stage and q['stage']>stage:continue
  pp=[xy(p) for p in (q['points'][:4] if stage=='GROWTH-02' and q['id']=='ROUTE-02' else q['points'])]
  # 裁切路段放在独立图层，西侧图外接近不会写到坐标标签上。
  layer=Image.new('RGBA',im.size);ld=ImageDraw.Draw(layer);ld.line(pp,fill='#faf0cf',width=int(q['width_range'][0]*scale),joint='curve');ld.line(pp,fill='#9b653f',width=2)
  im.paste(layer.crop((70,110,1078,830)),(70,110),layer.crop((70,110,1078,830)));d=ImageDraw.Draw(im)
 for sp in spaces:
  if stage=='GROWTH-01' and sp['id']!='SPACE-01':continue
  if stage=='GROWTH-02' and sp['id']=='SPACE-04':continue
  pp=[xy(p) for p in sp['polygon']];d.polygon(pp,fill='#f5e5ad',outline='#805f2c');center=tuple(sum(v[i] for v in pp)/len(pp) for i in (0,1));d.text((center[0]-16,center[1]-10),'S'+sp['id'][-2:],font=F(18),fill='#614821')
 for f in frontages:
  if f['district'] not in [dd['id'] for dd in included]:continue
  d.polygon([xy(p) for p in f['polygon']],fill='#665b52',outline='#302e2a')
 # 前沿的朝向只标关系短线，不假装画出每户大门。
 for p1,p2 in [([769,1630],[772,1637]),([813,1637],[813,1628]),([872,1607],[866,1608])]:
  if stage and stage!='GROWTH-03':continue
  d.line([xy(p1),xy(p2)],fill='white',width=3)
 for dd in included:
  p=xy(dd['polygon'][0]);d.text((p[0],p[1]-25),dd['id'].replace('DISTRICT-','D'),font=F(19),fill='#231f35',stroke_width=2,stroke_fill='white')
 for q in routes:
  if stage and q['stage']>stage:continue
  p=xy([795,1605] if q['id']=='ROUTE-03' else q['points'][len(q['points'])//2]);d.text((max(75,p[0]),p[1]+12),q['id'].replace('ROUTE-','R'),font=F(18),fill='#6c3420',stroke_width=2,stroke_fill='white')
 y=115
 if stage:
  caption={'GROWTH-01':'阶段01：日间交割，常住0','GROWTH-02':'阶段02：供水成立后才常住','GROWTH-03':'阶段03：寄宿增长，不预支扩张'}[stage]
  d.text((70,860),caption+'；形态为历史假说，不是实存分期。',font=F(17),fill='#713747')
 lines=['内部形态：有条件常住分支','深灰：聚合前沿带，非单栋轮廓','米黄：主通行 / 共有场院','虚线：街区关系范围，非地籍','紫色：地面下16格内观察到空气','底色：真实表面；砂砾不是现存路','D01 西接坡：先卸载、修理与生活','D02 内台：保管、守约、值守混合','D03 东上台：寄宿与日常工作混合','','S01 首段轮候 / 驮队止步分批','S02 公共交接 / 不独占东席','S03 洁净接水 / 未证泉井','S04 日常共同院 / 轻载生活','','R01 西侧接近  R02 内台主通行','R03 后侧轻载  R04 污物搬离待证','','总建成压力 3,500–4,600格²','12–17户；供水未闭合前不实施','北缘陡坡/熔岩、南陷、东砂砾限扩','岩面≠矿床，土面≠肥田','源：建筑师只读快照 / world writes=0','v0.3 / r1；F06撤回、背路不跨空隙']
 for line in lines:d.text((1110,y),line,font=F(17),fill='#223b42');y+=29
 d.line((70,890,190,890),fill='black',width=4);d.text((205,878),'20 blocks；图形可由DISTRICT调整，不能直接交Builder。',font=F(19),fill='#223b42')
 return im
for mode,name in [('structure','01-内部结构与地表'),('terrain','02-内部结构与地形')]:map_image(mode).save(R/f'maps/{name}.png')
for i in range(1,4):map_image('growth',f'GROWTH-{i:02}').save(R/f'maps/生长阶段-{i:02}.png')
# 三条通行剖面；同横向比例与真实Y，未实现的路径不画成建成坡道。
im=Image.new('RGB',(1350,1000),'#f5f1e8');d=ImageDraw.Draw(im);d.text((60,20),'MP-P03 | 内部主通行与后侧通行的现状地形剖面',font=F(26),fill='#223b42')
for i,q in enumerate(routes[:3]):
 y=100+i*275;d.text((60,y-20),f'{q["id"]} {q["name"]}  长{q["length_blocks"]}格 / 最大采样跳变{q["max_sampled_step"]}格',font=F(20),fill='#223b42')
 for yy in [115,125,135,145]:
  sy=y+190-(yy-115)*5;d.line((100,sy,1250,sy),fill='#d0caba');d.text((55,sy-10),str(yy),font=F(17),fill='black')
 pp=[(100+s[0]*7,y+190-(s[3]-115)*5) for s in q['profile']];d.line(pp,fill='#3d6157',width=3)
 for s in q['profile']:d.rectangle((100+s[0]*7,y+205,104+s[0]*7,y+218),fill=tuple(colors[s[4]]))
 d.text((100,y+230),'0                    距离沿提案线（同尺度：1格=7px）',font=F(17),fill='#223b42')
d.text((60,955),'一格位置采样仅显示地形；坡道、台阶、驮兽净空和连续可用性尚未实现或实机验证。',font=F(19),fill='#223b42');im.save(R/'maps/03-主要通行地形剖面.png')
print('districts',[(d['id'],d['metrics']) for d in districts]);print('routes',[(q['id'],q['max_sampled_step']) for q in routes]);print('capacity',plan['capacity'])
