"""MP-P01R 原创 L0 提案及真实坐标制图；数值均保留证据或假设身份。"""
from pathlib import Path
import json, math, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
CACHE=ROOT.parents[3]/'MP-P01R-cache'
P=np.load(CACHE/'natural.npz'); H=P['height']; L=P['land']; S=P['slope']; R=P['relief']
def dump(name,v): (ROOT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
sources=['SRC-CANON','SRC-R1-OBS','SRC-R1-DERIVED']
nodes=[]
def node(i,name,center,radius,area,hh,unit,shared,role,shape,driver,catch,stage,condition):
    x,z=center; a=(slice(max(0,z-1376-radius),min(2112,z-1376+radius+1)),slice(max(0,x+800-radius),min(3264,x+800+radius+1)))
    land=L[a]>0
    n=dict(id=f'NODE-{i:02d}',name=name,type='settlement_search_candidate',scale='POLITY_TERRITORY',authority='DESIGN_PROPOSAL',source_refs=sources,
      location_search_envelope=dict(type='bbox_search_only',bounds=[x-radius,z-radius,x+radius,z+radius],representative_xz=center,not_exact_site=True),
      built_fabric_capacity=dict(area_range_blocks2=area,confidence='LOW',status='TARGET_MATURITY_HYPOTHESIS_NOT_OBSERVED',morphology=shape,resident_household_pressure_range=hh,
        household_land_allowance_blocks2=unit,shared_service_land_blocks2=shared,arithmetic_range=[hh[0]*unit[0]+shared[0],hh[1]*unit[1]+shared[1]],
        calculation_note='户压力×含日常通行院落的户均用地+不重复计入的区域/政治服务空间；向外取整。系 Minecraft 规模敏感性模型，不是人口普查、地块标准或通用密度常数。',
        exclusions=['完整农牧腹地','矿场与燃料林','公地未建设保留地','搜索范围内其它未建地'],drivers=driver,
        sensitivity=condition,existing_area='UNVERIFIED'),
      role=role,functional_hinterland=dict(type='RELATIONAL_NOT_POLYGON',description=catch),historical_stage=stage,
      terrain_witness=dict(search_land_columns=int(land.sum()),elevation_p10_p50_p90=np.percentile(H[a][land],[10,50,90]).round(1).tolist(),slope8_le_0125_columns=int((land&(S[a]<=.125)).sum()),relief32_le_8_columns=int((land&(R[a]<=8)).sum()),
        note='完整方形搜索窗的自然统计，可能含多个陆地成员；低坡数不是可建筑面积，未减水源保护、现有实存或地籍。'),
      uncertainty=['精确位置及实存未调查','饮水与排污未验证','面积不冻结为城界',condition])
    nodes.append(n)
node(1,'西域主市场候选',[-350,2150],180,[20000,38000],[90,140],[150,190],[6000,11000],
 dict(population='联盟主要常住集中候选',economic='低岛生产汇集、普通手工业和交换',political='西席多个地方权力的市场协调节点，不独占西席',network='岛内集散',symbolic='地方契约'),
 '沿既有可用通路集聚的院落型混合市镇，生产地留在外围', ['西岛连续低平地','农牧与市场 Canon','多个地方共同体定期交换'], '西岛中南部生产共同体；北臂日常服务由 NODE-02 分担，三域货物流经中域而非全国日常赴此', 'GROWTH-02','若实际供给或人口不足，缩小到区间下限甚至退为周期市场，不强凑区域城镇。')
node(2,'北臂集货候选',[-200,1550],130,[5000,10000],[20,35],[150,190],[1500,3000],
 dict(population='少量常住与周边农户',economic='北臂产品与渡运候候补集货',political='地方自治',network='分担绕 C 形陆路的末端负担',symbolic='地方航渡祭祀可附着'),
 '小规模院落簇，不把整个北臂岸线建满',['C 形低岛绕行距离','北臂土地连续但面积有限'],'西岛北臂；与主市场重叠的是季节货运而非独占行政区','GROWTH-01','北侧航渡失败时保留地方收集功能，取消区域渡运容量。')
node(3,'联盟公地活动核心候选',[-140,1800],120,[10000,20000],[20,40],[110,160],[7800,13000],
 dict(population='低常住、会议期高访客',economic='公共事务服务，不作矿货必经仓场',political='三席共同政治中心，极高',network='三域到达的公共终点',symbolic='共同誓约与祭典'),
 '有限常住服务簇与共享活动空地；建成量不等于整个公地面积',['已批准共同领土','跨域争端与公共工程协调','强地方自治限制常设中央扩张'],'政治服务覆盖三域；日常生计依赖周边，行政影响不等于吞并中域','GROWTH-03','会议峰值未定；规模超过 20000 或改变非商业主导关系需重新评估，公地全域产权不因核心面积缩小。')
node(4,'中域北侧转运候选',[350,1600],150,[12000,24000],[45,80],[110,160],[6500,11000],
 dict(population='中等常住与旅商',economic='水陆/坡麓转换、储运及维修',political='中席地方城镇之一',network='跨域重货关键，吞吐重要性高于居民规模',symbolic='守约交割'),
 '低地口袋内较紧凑混合前沿，装卸服务与居民共存但分流',['东岛北西侧低地口袋','低地向山地陡升','中域 Canon'], '西域集货—东域北部生产之间；公地只分享人员通达，不垄断货流','GROWTH-02','岸线不是已证港口；若船岸或水源不成立，沿中域低地迁移或分成两节点，并回算容量。')
node(5,'东域北部共同体集散候选',[750,1780],240,[6000,14000],[30,60],[100,150],[3000,5000],
 dict(population='多个山地居民簇的服务集中',economic='山地产品汇集与维修，矿业取决于具体资源确认',political='东席多共同体协商之一，不是唯一矿都',network='山地驮运与下山链',symbolic='地方祖先/山地传统'),
 '不连续台地簇，总建成面积小于地理扩散范围',['富矿山地 Canon 而非矿脉测量','北侧中域接近性','大高差使持续上坡运输昂贵'], '北部山地共同体与实际矿源；服务范围随山路和水源调整','GROWTH-01','找不到稳定水源或可服务资源时缩为季节节点；不得用矿产 Canon 指定这里必有矿。')
node(6,'东南生产共同体条件候选',[1590,2750],240,[3000,9000],[12,30],[120,180],[1500,3200],
 dict(population='低常住或季节驻留',economic='远端生产的就近支持，有资源才成立',political='地方共同体自理，东席间接代表',network='远端分支，不能假设高吞吐干线已通',symbolic='地方性'),
 '离散小台地簇，禁止单一大圆形矿城',['东岛南北延伸明显','远端活动若存在，日常全赴北部代价高'], '东南山地实际资源点；本轮不划矿权和边疆国界','GROWTH-04','这是条件分支：资源/饮水/通道任一失败则不设常住聚落，容量可为 0；图上范围仅表示启动分支的规模。')

routes=[]
def route(i,ends,points,mode,flow,magnitude,frequency,stage,why):
    # 沿概念折线只读取样；显示地形代价，不把折线升级为可通行路径。
    sample=[]
    for (x,z),(xx,zz) in zip(points,points[1:]):
        steps=max(abs(xx-x),abs(zz-z))
        for t in np.linspace(0,1,steps+1):
            a=int(round(x+(xx-x)*t));b=int(round(z+(zz-z)*t));sample.append((a,b,int(H[b-1376,a+800]),int(L[b-1376,a+800])))
    heights=[p[2] for p in sample if p[3]>0]
    routes.append(dict(id=f'ROUTE-{i:02d}',authority='DESIGN_PROPOSAL',source_refs=sources,ends=ends,geometry=dict(type='conceptual_corridor_centerline',xz=points,search_halfwidth_blocks=80 if mode=='land_lowland' else 140,not_engineered_route=True),mode=mode,flow=flow,magnitude=magnitude,frequency=frequency,historical_stage=stage,why=why,
      verification='UNVERIFIED_USABLE_ROUTE',witness=dict(samples=len(sample),water_samples=sum(p[3]==0 for p in sample),land_y_range=[min(heights),max(heights)]),
      uncertainty='折线只表达流向和调查带；水深、碰撞、渡点、净空、坡道、权属与全程安全均待 L1。山地线路可大幅改线。'))
route(1,['NODE-02','NODE-01'],[[-200,1550],[-440,1660],[-530,1850],[-470,2020],[-350,2150]],'land_lowland','粮食、牲畜、地方交换与消息','MEDIUM','日常局部/周期跨片','GROWTH-02','绕西侧连续陆地承接沿途生产，不把海湾拉成直线陆路')
route(2,['NODE-01','NODE-03'],[[-350,2150],[-410,1930],[-390,1830],[-290,1810],[-140,1800]],'land_and_crossing','西席代表、公共事务人员及少量保障物资','LOW freight / HIGH event','会议/争端/祭典时集中','GROWTH-03','公地需西域公共到达；此线不要求矿货穿越政治中心')
route(3,['NODE-03','NODE-04'],[[-140,1800],[0,1760],[88,1750],[200,1730],[350,1600]],'land_lowland','代表、服务补给、消息','MEDIUM event','周期','GROWTH-03','利用已批准 connector 保持公地与中域接续，不把政治界线作实体障碍')
route(4,['NODE-02','NODE-04'],[[-200,1550],[-30,1560],[170,1530],[350,1600]],'conditional_water_transfer','粮食向东；工具/金属与旅客向西','REGIONAL if navigable','周期/季节','GROWTH-02','北端跨水候选避开公地货流；水面连通不证明航渡工程成立')
route(5,['NODE-04','NODE-05'],[[350,1600],[430,1580],[550,1680],[750,1780]],'mountain_search','食物与工具上山、减量后产品下山','REGIONAL / pack freight','周期','GROWTH-02','北侧低地到山地服务关系，不能把山顶直线视作道路')
route(6,['NODE-05','NODE-06'],[[750,1780],[1000,1800],[1140,2000],[1400,2300],[1660,2480],[1590,2750]],'conditional_mixed_terrain_search','远端资源/人员，必要时分段缓存','LOW until evidence','季节；条件启动','GROWTH-04','概念线采样含显著水段；调查绕湾/分段转运替代而非声称已通纯陆路。没有经济可行替代则取消远端常住分支。')

regions=[dict(id='REGION-01',authority='APPROVED_CANON',name='西域',geometry={'source':'SRC-R1-DERIVED','predicate':'land_component == 1','semantics':'自然成员作为 Canon 西域空间基础，不包揽周围海权'},role='人口、低平生产、市场',nodes=['NODE-01','NODE-02']),
 dict(id='REGION-02',authority='APPROVED_CANON',name='中域',geometry={'type':'UNRESOLVED_TRANSITION','description':'东岛西部低地/坡麓及 Commons 东侧 connector；无自然唯一三分硬边界'},role='跨岛与山地转运',nodes=['NODE-04']),
 dict(id='REGION-03',authority='APPROVED_CANON',name='东域',geometry={'type':'UNRESOLVED_TRANSITION','description':'东岛山地核心；不以某条等高线自动划政治边界'},role='矿业、石工与多个地方共同体',nodes=['NODE-05','NODE-06'])]
commons=((L==2)&(np.arange(-800,2464)[None,:]<=88))
assert commons.sum()==92124
space=dict(id='SPACE-01',authority='APPROVED_CANON',name='Alliance Commons',area_blocks2=92124,geometry={'type':'source_membership_plus_approved_cut','predicate':'land_component==2 AND x<=88','note':'仅对此 R1 快照复现 A 西侧主体；重算面积与 Canon 相等','political_interface':{'x':89,'z_range':[1726,1774]}},control='三域共同所有',users='代表、申请者、共同仪式参与者与服务者',use='共同治理、公共会集与通达',when='周期活动与低量常设服务',why_not_built_over='公有土地并非待售城镇地块；保障公共使用、岸缘与下一层查证的地形/生态保留空间',capacity_node='NODE-03')
growth=[dict(id='GROWTH-01',authority='PLANNING_ASSUMPTION',driver='当地生计与山地少量资源利用',response='分散农牧共同体和有水有资源的山地共同体独立成立；北臂收集与北山服务角色逐步出现',new_constraint='地方土地与可用山路形成惯性',next_pressure='交换季节盈余与互缺物资',viable_without_future='不依赖未来议会与跨域高吞吐；没有足够生计的远端点不设'),
 dict(id='GROWTH-02',authority='PLANNING_ASSUMPTION',driver='重复跨水和山地交换的损耗',response='西域市场集中部分交换，中域分段存储，已有路线强化',new_constraint='岸线、转运持有人和地方权利限制后续改线',next_pressure='跨域纠纷与公共工程协商',viable_without_future='即使无正式联盟，交换仍可通过地方契约运转'),
 dict(id='GROWTH-03',authority='PLANNING_ASSUMPTION',driver='共享工程与争端超过双边协商能力',response='已批准公地承担政治终点；三方访问加强，货运主链仍在地方',new_constraint='公地共同所有与 connector 地方归属长期约束',next_pressure='维持可达、公平使用和缓冲能力',viable_without_future='有限常设机构即可工作，不依赖远端扩张'),
 dict(id='GROWTH-04',authority='PLANNING_ASSUMPTION',driver='仅在资源、饮水、运输证明后出现远端盈余',response='东南小共同体及分段支线可强化；否则保持季节/未设',new_constraint='更长补给链、燃料和侵蚀负担',next_pressure='可能收缩或改用沿岸路线；不保证持续增长',viable_without_future='依赖已证明的当期活动，不依据未来矿都预建')]
anchors=[]
for i,n in enumerate(nodes):
    anchors.append(dict(id=f'ANCHOR-{i+1:02d}',node=n['id'],authority='DESIGN_PROPOSAL',scale='Territorial',role='STABILIZING_ANCHOR' if i==2 else ('ORIGIN_ANCHOR' if i in (1,4) else 'GROWTH_ANCHOR'),why=n['built_fabric_capacity']['drivers'],when=n['historical_stage'],attracts=n['role']['economic'],repels='与其主要使用冲突的重烟、污染或阻断公共通达',morphological_effect=n['built_fabric_capacity']['morphology'],removal_effect=['西域集散分散回地方，主市场容量退缩','北臂改为更长岛内集货路，北渡货流消失','议会常设服务和三方公共访问需求失去理由；商业节点不必同时消失','跨水与山路需重新配对，双端缓存和容量重估','北山产品缺少集散压力，山路与中域容量降级','取消 ROUTE-06 和东南常住容量，其余链仍可运行'][i]))
demands=[]
for i,(why,users,mag,freq,deps,external,response) in enumerate([
 ('农牧产品季节集中、日常需求分散','西域共同体及工匠','户群至跨共同体','日常+收获季',['REGION-01','NODE-01','NODE-02'],'牲畜拥挤、存储损耗','地方保留粮食与就地日常服务，剩余才进入市场'),
 ('海与坡之间载具及负载变化','运输者、旅商、生产者','区域重货，未有吨位','周期',['NODE-02','NODE-04','NODE-05'],'堆货占地、火险、停航滞留','分段转运与混合服务，不把仓储等同整个城镇'),
 ('富矿山地需要常规劳动、燃料与食物','多个山地共同体','分散/资源未定位','日常+季节',['REGION-03'],'污染、耗林、边坡侵蚀','就近减量加工的可行性比较；保护饮水，矿源不实则撤节点'),
 ('跨域争端和共同工程','三席、申请者、地方代表','政治高、常住低、活动峰值高','周期/事件',['SPACE-01','NODE-03'],'会期拥堵、地方垄断到达','公共到达与共享活动空间；日常小量服务可嵌入'),
 ('风险不能用低普及魔法消除','岛民、矿工、渡运者','战略保障但低常态流','恶劣天气/事故',['ROUTE-01','ROUTE-04','ROUTE-05'],'运力挤兑与储备腐损','各端分散缓冲、备用访问；拒绝虚构已通航冗余'),
 ('地方自治、祭祀和常规照护','居民与旅人','日常地方强、联盟弱','日常+节令',['REGION-01','REGION-02','REGION-03'],'静养/烟火冲突','服务嵌入地方聚落，不强制逐镇独立纪念建筑')]):
    demands.append(dict(id=f'DEMAND-{i+1:02d}',authority='DESIGN_PROPOSAL',why=why,users=users,magnitude=mag,frequency=freq,maturity='MATURE_WORKING_HYPOTHESIS',spatial_dependencies=deps,externalities=external,possible_spatial_response=response,priority='ANCHOR_CORE' if i<4 else 'ESSENTIAL_SUPPORT'))
programs=[dict(id=f'PROGRAM-{i+1:02d}',source_demand=d['id'],required_functions=d['possible_spatial_response'],magnitude=d['magnitude'],implementation_options='shared / embedded 优先；专用机构须由下层 throughput 证明',adjacency=d['spatial_dependencies'],maturity=d['maturity'],externality=d['externalities'],uncertainty='无单体数量或房间指标；L1 先分配聚落功能') for i,d in enumerate(demands)]
packages=[]
for i,(name,ns,rs,fixed,resolve,adapt,trigger) in enumerate([
 ('西域生产—市场系统',['NODE-01','NODE-02'],['ROUTE-01','ROUTE-04'],['低平生产不能被集中建成区耗尽','主市场与地方日常服务分工；不使全岛每天远行'],['人口/食物水量、实际农地与实存权属','北渡可行性和现有道路','分散村落的数量与容量'],['主市场在搜索逻辑内迁移','地方节点合并/拆分与容量分布'],['生产及进口无法支持户压力','主市场因实存无法承载且无附近替代']),
 ('中域与跨水接口系统',['NODE-04'],['ROUTE-04','ROUTE-05','ROUTE-03'],['西—中—东产品/人员转换','不强迫主要矿货穿越公地','connector 属中域且需公共访问关系'],['水深岸坡航渡风浪与两端装卸','饮水、地面净空和上山路线','实际混合实存与服务容量'],['渡点组合和分段缓存','单中心或双转换节点','岸陆连接精确走向'],['无跨水方式能支持假设流量','上山供给链中断或容量降一数量级']),
 ('东域山地共同体系统',['NODE-05','NODE-06'],['ROUTE-05','ROUTE-06'],['多个共同体而非单一矿都','富矿是区域 Canon 不定位矿脉','远端节点条件启动'],['真实可服务资源、水源、燃料更新','驮运路线与台地可用面积','当地实存与山地食物来源'],['节点在资源/台地调查后迁移','远端保持季节性或撤销','碎片化服务网络及容量'],['没有持续供给的北山活动支点','通达/水源与区域角色无可兼容位置']),
 ('联盟公地与三域公共访问接口',['NODE-03'],['ROUTE-02','ROUTE-03'],['SPACE-01 全部 92124 格²共同所有，不缩小产权','X89 政治界面不是物理割裂','政治重要性不等于最大常住城镇'],['已批准 A 及公地边界实地复核','三域公平到达与会议峰值','实存、饮水、可用公共地与低量常设需求'],['活动核心位置及服务形态','低密服务的分布与非建设空间用途'],['公地内无法支持必要公共访问','需要改变公地或地方归属才能成立'])]):
    packages.append(dict(id=f'PACKAGE-{i+1:02d}',name=name,parent_plan='MP-P01R-CIV001',parent_revision='r1',parent_scale='POLITY_TERRITORY',child_scale='REGIONAL_SYSTEM',recipient='minecraft-planner',authority='DESIGN_PROPOSAL_PENDING_REVIEW',scope_search_geometry={'node_refs':ns,'route_refs':rs,'not_child_boundary':True},why=name,upstream_anchors=[a['id'] for a in anchors if a['node'] in ns],upstream_flows=rs,
      UPSTREAM_FIXED=fixed,conditional_authority_note='Canon/Owner 约束立即有效；本轮关系仅在父案获接受后成为下层 fixed，不自动成为 Canon。',DOWNSTREAM_TO_RESOLVE=['EXISTING_FABRIC_UNVERIFIED：先调查现有人文实存']+resolve,DOWNSTREAM_ADAPTABLE=adapt,
      capacity_hypothesis=[{'node':n['id'],'location_search_envelope':n['location_search_envelope'],'built_fabric_capacity':n['built_fabric_capacity'],'functional_hinterland':n['functional_hinterland']} for n in nodes if n['id'] in ns],source_refs=sources,
      uncertainty='容量 LOW；水/实存/可通行性未验证；图上符号不是地籍',cross_package_dependencies=[f'PACKAGE-{j:02d}' for j in range(1,5) if j!=i+1],REVISION_TRIGGER=trigger,
      revision_protocol='先在适配范围内修订；无解则报 UPSTREAM_PLANNING_ISSUE，引用新证据及最小受影响 node/route/capacity；父案加 revision，仅更新受影响链并重跑 Gates，关联 child 标记 stale。',
      expected_outputs=['刷新自然及实存证据','L1 settlement network / catchment / capacity 三分对象','跨包接口可行性','L2 Planner 包','坐标规划图和 machine-readable objects'],world_write_authorization=False,builder_ready=False))
context=dict(plan_id='MP-P01R-CIV001',revision='r1',previous_revision=None,skill='minecraft-planner v0.2',scale='POLITY_TERRITORY',state='HANDOFF_READY',review_status='AWAITING_GPT_AND_OWNER',fabric_observation_state='EXISTING_FABRIC_UNVERIFIED',evolution_logic='EXISTING_EVOLUTION',maturity_state='MATURE_WORKING_HYPOTHESIS',world_writes=0,coordinate_system='Minecraft Overworld X east / Z south; block units; bounds inclusive',bounds=[-800,1376,2463,3487],context_note='历史阶段均为重构假设，无年表 Canon；当前实存未读，不代表空白。没有继承任何旧规划的节点/规模/线路。')
dump('planning-objects.json',dict(context=context,regions=regions,nodes=nodes,routes=routes,spaces=[space],anchors=anchors,source_refs=sources))
dump('demand-model.json',demands);dump('growth-sequence.json',growth);dump('building-program.json',programs);dump('implementation-packages.json',packages)
dump('settlement-capacity.json',dict(semantics='非现存面积、非通用密度、非人口事实、非建设授权',nodes=[dict(id=n['id'],capacity=n['built_fabric_capacity']) for n in nodes],rural_reserve_hypothesis={'west_distributed_households':[40,70],'built_fabric_range_blocks2':[6000,14000],'not_fixed_village_count':True,'location':'REGION-01 既有生产联系；不得依据本图自动新增村庄'},food_balance='UNRESOLVED；不把低坡面积当良田或默许地图外无限输入',sum_main_nodes_range_blocks2=[sum(n['built_fabric_capacity']['area_range_blocks2'][j] for n in nodes) for j in (0,1)]))

# 输出统一真实比例地图：透明圆是面积符号，不是覆盖该地的精确边界。
(ROOT/'maps').mkdir(exist_ok=True)
fontpath='C:/Windows/Fonts/msyh.ttc'
def f(n): return ImageFont.truetype(fontpath,n)
scale=.5; ox=85; oy=120
def xy(p):return(ox+(p[0]+800)*scale,oy+(p[1]-1376)*scale)
base=Image.open(ROOT/'evidence/自然底图.png').crop((80,70,1712,1126))
colors=['#9a4f24','#b98829','#774599','#126c86','#b34e46','#8e405d']
def dashed(d,box,color,width=2):
    x,y,xx,yy=box
    for a,b in [((x,y),(xx,y)),((xx,y),(xx,yy)),((xx,yy),(x,yy)),((x,yy),(x,y))]:
        length=math.dist(a,b)
        for t in range(0,int(length),13):
            q=min(t+7,length);d.line((a[0]+(b[0]-a[0])*t/length,a[1]+(b[1]-a[1])*t/length,a[0]+(b[0]-a[0])*q/length,a[1]+(b[1]-a[1])*q/length),fill=color,width=width)
def linearrow(d,pts,color,width=4):
    ps=[xy(p) for p in pts];d.line(ps,fill=color,width=width)
    a,b=ps[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);d.polygon([b,(b[0]-12*math.cos(ang-.45),b[1]-12*math.sin(ang-.45)),(b[0]-12*math.cos(ang+.45),b[1]-12*math.sin(ang+.45))],fill=color)
titles=['01 领土与地形约束','02 交换流与条件通道','03 聚落规模：搜索 ≠ 建成 ≠ 腹地','04 服务腹地：关系而非城界','05 因果生长：重构假设而非已知历史']
filenames=[]
for mode,title in enumerate(titles):
    im=Image.new('RGB',(2430,1380),'#f5f1e8');im.paste(base,(ox,oy));d=ImageDraw.Draw(im)
    d.text((85,20),'MP-P01R · CIV-001  /  '+title,font=f(30),fill='#213638')
    d.text((85,66),'L0 POLITY_TERRITORY  |  r1 · 提案待审  |  world writes = 0  |  北 ↑ (-Z)',font=f(21),fill='#435459')
    for x in range(-800,2464,400):
        u,v=xy((x,1376));d.line((u,oy,u,oy+1056),fill='#d8ded0');d.text((u-20,oy+1060),str(x),font=f(17),fill='#35494b')
    for z in range(1400,3488,400):
        u,v=xy((-800,z));d.line((ox,v,ox+1632,v),fill='#d8ded0');d.text((6,v-10),str(z),font=f(17),fill='#35494b')
    # 同源公地成员掩膜；严禁用视觉椭圆代替 Canon 边界。
    mask=Image.fromarray(np.uint8(commons)*255).resize((1632,1056),Image.Resampling.NEAREST)
    tint=Image.new('RGB',base.size,'#c4a5d8');im.paste(Image.blend(base,tint,.48),(ox,oy),mask);d=ImageDraw.Draw(im)
    a=xy((89,1726));b=xy((89,1774));d.line([a,b],fill='#6f287b',width=4)
    if mode==0:
        for p,label in [((-430,2330),'西域：连续低地生产基础'),((430,1460),'中域：岸—陆—坡麓过渡'),((1090,2170),'东域：多共同体山地核心'),((1040,3010),'远端活动取决于资源与补给；不预定全面开发')]:
            d.text(xy(p),label,font=f(21),fill='#35494b',stroke_width=2,stroke_fill='#f5f1e8')
    if mode in (1,4):
        for r in routes:
            color={'GROWTH-02':'#ae602c','GROWTH-03':'#774599','GROWTH-04':'#817971'}[r['historical_stage']] if mode==4 else ('#287790' if 'water' in r['mode'] or 'crossing' in r['mode'] else '#b46334')
            linearrow(d,r['geometry']['xz'],color,3 if 'conditional' in r['mode'] else 4)
            p=r['geometry']['xz'][len(r['geometry']['xz'])//2];q=xy(p);d.text((q[0]+6,q[1]+9),r['id'].replace('ROUTE-','R'),font=f(19),fill=color,stroke_width=2,stroke_fill='#f5f1e8')
    if mode==3:
        for a,b in [([-530,2220],[-350,2150]),([50,2210],[-350,2150]),([-430,1590],[-200,1550]),([1100,1690],[750,1780]),([1870,2740],[1590,2750]),([600,1550],[350,1600])]:
            linearrow(d,[a,b],'#70906e',3)
        d.text(xy((1150,3200)),'腹地依赖实际资源、路程与地方权利\n无已证边界，不按圆形半径分割',font=f(20),fill='#435747')
    for i,n in enumerate(nodes):
        u,v=xy(n['location_search_envelope']['representative_xz']);c=colors[i];lo,hi=n['built_fabric_capacity']['area_range_blocks2']
        if mode==2:
            b=n['location_search_envelope']['bounds'];a=xy(b[:2]);bb=xy(b[2:]);dashed(d,(*a,*bb),'#75858c')
            rlo=math.sqrt(lo/math.pi)*scale;rhi=math.sqrt(hi/math.pi)*scale
            overlay=Image.new('RGBA',im.size,(0,0,0,0));od=ImageDraw.Draw(overlay);rgb=tuple(int(c[k:k+2],16) for k in (1,3,5))
            od.ellipse((u-rhi,v-rhi,u+rhi,v+rhi),fill=rgb+(45,),outline=rgb+(255,),width=2)
            od.ellipse((u-rlo,v-rlo,u+rlo,v+rlo),fill=rgb+(95,))
            im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(im)
        else:
            rad=math.sqrt((lo+hi)/2/math.pi)*scale*.5
            d.ellipse((u-rad,v-rad,u+rad,v+rad),fill=c,outline='white',width=2)
        d.text((u+8,v-28),'N'+str(i+1).zfill(2),font=f(22),fill=c,stroke_width=2,stroke_fill='white')
    panel=1770; y=125
    legend=[['自然：绿低地 → 褐高地；蓝为水域','Canonical：紫色为公地精确成员','西域 = 西岛自然成员','中—东是过渡关系，不画虚假国界','富矿是区域 Canon，不是已测矿脉','节点均为本轮搜索候选，非现存城镇'],
      ['R01 岛内集货与地方交换','R02 西域—公地公共访问','R03 connector 公共接续','R04 北侧跨水：粮食 / 工具与人员双向','R05 分段上山：粮食 / 山地产品双向','R06 远端条件支线，尚非已通道路'],
      ['虚线框 = 选址搜索窗，不是城界','彩色内圆 = 建成面积下限等面积符号','浅色外环 = 上限，不是实际建筑轮廓','圆按地图比例；山地会碎片化','腹地另见图 04，不包含在圆中','全部容量置信度 LOW；N06 可为 0'],
      ['绿色箭头 = 地方服务/供给关系','不表示耕地已开发或资源已定位','政治服务：公地覆盖三域','经济服务：分段、交叠、季节性','蓝海域不等于已证航道','不划独占圆形 catchment'],
      ['G1 地方生计 / 山地共同体','G2 交换强化 → 市场、转运、山路','G3 共同治理 → 公地访问链','G4 远端条件强化，允许不发生','棕线 G2；紫线 G3；灰线 G4','既有遗存未读；无臆造旧路/年表']][mode]
    for t in legend:d.text((panel,y),t,font=f(22),fill='#35494b');y+=37
    y+=30
    for i,n in enumerate(nodes):
        lo,hi=n['built_fabric_capacity']['area_range_blocks2'];d.text((panel,y),f"N{i+1:02d}  {n['name']}",font=f(21),fill=colors[i]);y+=32
        d.text((panel,y),f'{lo/1000:g}–{hi/1000:g} 千格²  ·  LOW'+(' / 条件' if i==5 else ''),font=f(21),fill='#35494b');y+=49
    d.text((panel,y+5),'面积含内部街巷、院落和共享服务地。\n不含完整农地、矿场、燃料林或外部腹地。\n人口、饮水、粮食和通行能力仍需 L1。',font=f(19),fill='#536465',spacing=8)
    d.line((85,1245,335,1245),fill='#213638',width=4);d.text((85,1257),'500 blocks · 坐标单位为格',font=f(20),fill='#35494b')
    d.text((600,1220),'底图：WB-002R-R1 逐列 exposed_y / land_component；调查 base bc96aa5\nNG-3 仅作宏观 Atlas 参照；无本轮 live freshness 结论。X [-800,2463], Z [1376,3487]\n公地 = 原始东岛陆地 ∩ X≤88；本轮关系/面积/线路均不授权施工。',font=f(19),fill='#526569',spacing=8)
    filename=title.split(' ')[0]+'.png';im.save(ROOT/'maps'/filename);filenames.append(filename)
html='''<!doctype html><meta charset="utf-8"><title>MP-P01R CIV-001 规划图册</title><style>body{margin:24px;background:#f5f1e8;color:#243b40;font:18px system-ui}button{padding:10px;margin:4px}img{width:100%;max-width:2430px}table{border-collapse:collapse}td,th{border:1px solid #aaa;padding:10px}a{color:#176b80}</style><h1>南部岛屿群人类三域联盟 · MP-P01R</h1><p>L0 独立提案 · HANDOFF_READY / 待 GPT + Owner 审核 · world writes = 0</p><p>点是候选位置；搜索框不是城界；规模圆是等面积符号；腹地是服务关系。点击图册切换，原图可新窗口放大。</p>'''
for name,filename in zip(titles,filenames):html+=f'<button onclick="document.getElementById(\'map\').src=\'maps/{filename}\';document.getElementById(\'full\').href=\'maps/{filename}\'">{name}</button>'
html+='<p><a id="full" href="maps/01.png" target="_blank">打开当前原始大图</a> · <a href="国家级规划方案.md">完整规划逻辑</a> · <a href="implementation-packages.json">L1 交接包</a></p><img id="map" src="maps/01.png"><table><tr><th>候选</th><th>坐标 X,Z</th><th>建成规模假设</th><th>形态</th></tr>'
for n in nodes:html+=f"<tr><td>{n['id']} {n['name']}</td><td>{n['location_search_envelope']['representative_xz']}</td><td>{n['built_fabric_capacity']['area_range_blocks2']} 格² / LOW</td><td>{n['built_fabric_capacity']['morphology']}</td></tr>"
html+='</table><p>无现存建筑面积或粮食自给认证；节点 06 为条件分支，可为 0。精确场地、饮水、港航、实存和承载量必须在 L1 重查。禁止直接交 Builder 施工。</p>'
(ROOT/'规划图册.html').write_text(html,encoding='utf-8')
print('Generated',len(nodes),'nodes,',len(routes),'corridors,',len(packages),'L1 packages,',len(filenames),'maps')
