"""由本轮显式规划决定生成数据与坐标图；不以程序评分代替规划判断。"""
from pathlib import Path
import json, math, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent
C=R.parents[3]/'MP-P02R-cache'
A=np.load(C/'surface-natural.npz'); h=A['height']; land=A['land']; surf=A['surface']; veg=A['vegetation']; slope=A['slope']; relief=A['relief']
def dump(p,v): (R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def profile(b):
 x,z,xx,zz=b; sl=(slice(z-1456,zz-1456+1),slice(x-320,xx-320+1)); m=land[sl]==2; n=int(m.sum()); ss=surf[sl]
 vz,vx=np.mgrid[0:452,0:448]; vm=(vx*4+320>=x)&(vx*4+320<=xx)&(vz*4+1456>=z)&(vz*4+1456<=zz)&(land[::4,::4]==2)
 return dict(bounds=b,land_columns=n,y_p10_p50_p90=np.percentile(h[sl][m],[10,50,90]).tolist(),gentle_columns=int((m&(slope[sl]<=.15)&(relief[sl]<=10)).sum()),surface_ratio={k:round(float(((ss==i)&m).sum()/n),4) for i,k in enumerate(['NON_EAST_LAND','SOIL_SURFACE','ROCK_SURFACE','SAND_GRAVEL','TERRACOTTA_SURFACE','MUD_CLAY','SNOW_ICE','SURFACE_PLANT','OTHER_UNRESOLVED']) if i},vegetation_sample_count=int(vm.sum()),leaf_sample_presence_ratio=round(float((veg[:,:,0][vm]>0).mean()),4),artificial_flag_columns=int((A['artificial'][sl][m]>0).sum()),source_refs=['SRC-OBS','SRC-DERIVED'],authority='DERIVED',substrate='UNRESOLVED',existing_fabric='UNVERIFIED')
specs=[
 ('NODE-01','北岩台集散候选',[704,1520,895,1711],[800,1620],[3500,8000],[12,24],[100,150],[2300,4400],'北部共同体产品交割、修理及共享储备；承担吞吐不垄断东席','岩面占优且有较多缓地；优先比较少占草土的干式服务面，不能据此认定地基完整或有水','稀缺土面先保留调查；常住不随平岩面积膨胀；若供水/下山运输失败，服务随既有社区迁移或收缩','沿可用岩台分簇，生活嵌入服务前沿；排水与贴岩基础需调查','MP-P01R:NODE-05'),
 ('NODE-02','西肩常住支援候选',[512,1904,703,2095],[610,1990],[2500,6000],[18,36],[100,130],[700,1320],'地方家庭与共同体日常支援，向北交换但保有自治与地方祭祀','草土覆盖多、植被样本较多，但整体高于北部岩台且缓地破碎','不得把草土都铺成聚落；保留成片土面调查生产潜力，水与运输不足则下调居民压力','小簇贴台肩，居住与低扰动工作混合；开放土面不被连接成连续建成带','MP-P01R:NODE-05'),
 ('NODE-03','南部混合岩面条件候选',[1472,2480,1663,2671],[1570,2580],[3000,9000],[12,30],[120,180],[1560,3600],'仅在真实远端生产与持续供给成立后支持当地活动','岩面与陶瓦质表面交错，草土很少；北侧沿岸地形亦不能证明绕行可达','不设自给农业默认值；先季节服务，土层/饮水/资源/驮路任一失败可为0','碎片式服务与驻留，避免用填土大平台抹平地表差异','MP-P01R:NODE-06'),
 ('NODE-04','南部草土高地替代搜索',[1350,2672,1471,2863],[1410,2760],[3000,9000],[12,30],[120,180],[1560,3600],'NODE-03的替代位置而非第四座新聚落','草土与陶瓦质地表交错，比NODE-03整体更高；不能用绿色表面抵消运输成本','只有水、既有人文或真实生产优势足以补偿抬升成本时才替代；不能与NODE-03叠加容量','压缩对土面的占用；分簇适应既有地形，不预定完整农田环','MP-P01R:NODE-06')]
nodes=[]
for i,name,b,p,area,hh,allow,shared,role,ground,sensitivity,morph,parent in specs:
 nodes.append(dict(id=i,name=name,type='settlement_search_candidate',authority='DESIGN_PROPOSAL',parent_node=parent,location_search_envelope={'bounds':b,'representative_xz':p,'not_exact_site':True},built_fabric_capacity={'area_range_blocks2':area,'household_pressure':hh,'household_allowance_blocks2':allow,'shared_service_blocks2':shared,'arithmetic_range':[hh[0]*allow[0]+shared[0],hh[1]*allow[1]+shared[1]],'confidence':'LOW','inactive_area_blocks2':0,'existing_area':'UNVERIFIED','exclusions':['生产腹地','未建设公地','矿区与燃料林','节点间交通','全部搜索窗'],'semantic':'户用地含本地通行院落；shared只计不重复区域服务。为Minecraft压力假设，不是人口普查。'},role=role,surface_character_summary=ground,sensitivity=sensitivity,morphology=morph,functional_hinterland={'type':'RELATIONAL_NOT_POLYGON','description':'北部家庭—交割—中域接口' if i in ['NODE-01','NODE-02'] else '实际远端生产点—驻留支持—北部交换；有活动才启动'},profile=profile(b),source_refs=['SRC-CANON','SRC-PARENT','SRC-OBS','SRC-DERIVED'],alternative_to='NODE-03' if i=='NODE-04' else None))
routes=[
 dict(id='ROUTE-01',ends=['PARENT:NODE-04','NODE-01'],points=[[350,1600],[550,1620],[800,1620]],flow='粮食与日用物上山；山地产品下行；周期交割和急需修理',magnitude='初期按北部30–60户与间歇生产，非已知吨位',resistance='由低地升至裸岩缓台；需调查转折、装卸与排水；不默认车行',priority='先确认跨域接口'),
 dict(id='ROUTE-02',ends=['NODE-01','NODE-02'],points=[[800,1620],[680,1780],[610,1990]],flow='家庭日需、共同储备、维修与地方代表往返',magnitude='日常小量、定期集散；不将两端当可每日轻松往返',resistance='越过地表转换与台肩高差；绕坡通道调查先于聚落定址',priority='与两北部候选联合调查'),
 dict(id='ROUTE-03',ends=['NODE-02','NODE-03'],points=[[610,1990],[900,2150],[1230,2390],[1570,2580]],flow='远端生产工具/口粮补给及回程产品；条件性',magnitude='先季节小队；没有实测吞吐不得升级常年重货',resistance='穿越高地且遇岩土交错；图线只是关系穿越带。必须比较绕高地/分段储备，不证明鞍部',priority='远端启动前验证'),
 dict(id='ROUTE-04',ends=['NODE-02','NODE-04'],points=[[610,1990],[950,2260],[1230,2500],[1410,2760]],flow='ROUTE-03替代关系；与南部替代分支绑定',magnitude='与ROUTE-03互斥的容量情景',resistance='较高的草土高地意味着更多爬升；有本地水与生产优势才值得',priority='比较分支')]
for q in routes:
 q.update(authority='DESIGN_PROPOSAL',geometry_semantics='RELATION_WAYPOINTS_NOT_ALIGNMENT',usable_route='UNVERIFIED',source_refs=['SRC-PARENT','SRC-OBS','SRC-DERIVED'])
 # 沿关系线抽取地形只揭示风险，不生成导航或最优路线。
 samples=[];dist=0;prev=None
 for p1,p2 in zip(q['points'],q['points'][1:]):
  count=max(2,int(math.dist(p1,p2)/8)+1)
  for t in np.linspace(0,1,count):
   x,z=[int(round(a+(b-a)*t)) for a,b in zip(p1,p2)]
   if prev:dist+=math.dist(prev,(x,z))
   samples.append([round(dist,1),x,z,int(h[z-1456,x-320]),int(surf[z-1456,x-320])]);prev=(x,z)
 q['straight_relation_probe']={'length_blocks':round(dist,1),'y_range':[min(v[3] for v in samples),max(v[3] for v in samples)],'samples':samples,'not_route_feasibility':True}
demands=[]
for k,(d,why,users,mag,freq,stage,dep,ext,response) in enumerate([
 ('持续生活','常住与工艺活动不能仅靠矿产名义维持','家庭/驻留者','北部30–60户；南部0或12–30户','每日','各独立阶段','饮水、粮食、日常通行','污水与生活争地','户内储备与共用补给关系'),
 ('跨域交换','山地生产与西域低地供给互补','驮队/工匠/交割者','间歇批次，未测吨位','周期/季节','交换增长','中域接口与北部服务','拥堵/牲畜/物料损耗','共享交割与维修可嵌于社区'),
 ('共同治理','东席代表多个自治共同体','家庭代表/地方组织','多共同体轮换协商，人数未定','定期与争端发生时','稳定阶段','相互可达且非单方独占','中心垄断风险','共享议事/寄宿需求，不必独立行政城'),
 ('资源生产支持','富矿Canon需转为真实可服务生产','探查与工艺人员','未证矿种/储量/产出','条件性','资源成立后','资源、水、燃料、运输','烟尘/火/废水','前期维修；重冶炼需另证风水燃料'),
 ('地表延续与恢复','土面/植被占用不可视为无成本','本地使用者','范围待现状与权属调查','持续/轮替','全部','土层、植被更新、排水','侵蚀与过采','保留片状开放地与缓冲')],1):demands.append(dict(id=f'DEMAND-{k:02}',demand=d,why=why,users=users,magnitude=mag,frequency=freq,maturity=stage,dependencies=dep,externalities=ext,response=response,authority='PLANNING_ASSUMPTION'))
anchors=[dict(id='ANCHOR-01',role='ORIGIN_ANCHOR',scale='Regional',why='地方生活须依赖经验证的水与可持续生计；尚未定位',when='任何常住前',attracts='家庭与低扰动工作',repels='污染水源的活动',morphology='生活围绕真实可维持支点分簇',removal='两北节点容量可归零或移位'),dict(id='ANCHOR-02',role='GROWTH_ANCHOR',scale='Regional',why='跨域交割需要降低反复爬升与货损',when='稳定交换出现后',attracts='储备/维修/交割',repels='阻断装卸的连续建设',morphology='北岩台服务与西肩家庭协作而非单中心扩张',removal='NODE-01独立服务规模失去理由，迁回可服务社区'),dict(id='ANCHOR-03',role='STABILIZING_ANCHOR',scale='Regional',why='强地方自治与东席联合需协商与履约',when='多共同体持续联系',attracts='周期代表与公共互助',repels='唯一矿都垄断',morphology='多个生活中心与共享服务',removal='需回问Canon，不能靠空间优化取消自治'),dict(id='ANCHOR-04',role='GROWTH_ANCHOR',scale='Regional',why='远端若有真实生产，反复北返成本高',when='资源/供给/路成立后',attracts='季节支持，后可常住',repels='未经证据的大型矿城',morphology='NODE-03或04，条件性离散聚落',removal='ROUTE-03/04与南部容量删除')]
growth=[dict(id='GROWTH-01',driver='已有地方生活传统，实存未读取',response='以真实水与生计为基础的自治小共同体',new_constraint='已有权属、路线、祭祀不得清空',next_pressure='跨社区互助与剩余交换',independent_viability='只在水与生计成立处存在，不预支未来矿业'),dict(id='GROWTH-02',driver='交换频率增长',response='已有路与可装卸岩台附近嵌入共享服务',new_constraint='交割通行与稀缺土面保留',next_pressure='储备、纠纷与维修需求',independent_viability='仅服务北部家庭与交换，不依赖南部'),dict(id='GROWTH-03',driver='互助履约制度稳定',response='共享服务成熟，常住保持多中心',new_constraint='地方权属与服务准入',next_pressure='真实远端生产若出现则需延伸',independent_viability='成熟北部网络可永久止于此'),dict(id='GROWTH-04',driver='远端资源和供给确证',response='先季节驻留，再比较南部两个地表候选',new_constraint='长距离补给、恢复与退出责任',next_pressure='若压力不足则撤回季节状态',independent_viability='独立验算供应；不因总图画了节点强迫常住')]
spaces=[dict(id='SPACE-01',where='NODE-02草土斑块及NODE-01稀缺土面',controller='地方共同体，具体权属待调查',users='家庭与生产者',use='土层/生产潜力调查及潜在生产、排水空间',when='持续',why_unbuilt='不可逆占用前保留选择；不是已证耕地保护线'),dict(id='SPACE-02',where='NODE-01局部岩面',controller='参与交割的共同体协议',users='驮运和维修',use='临时卸载与周转',when='周期',why_unbuilt='保持通行和共享服务，非景观广场定形'),dict(id='SPACE-03',where='所有节点间未定址高地和植被斑块',controller='权属待查，不宣称无主地',users='当地利用者',use='现状延续、潜在恢复/采集与排水',when='长期',why_unbuilt='没有连续建成需求；植被更新与水源不明'),dict(id='SPACE-04',where='实际确认的饮水源周边，尚无坐标',controller='受益社区协定',users='居民',use='供水与卫生隔离',when='每日',why_unbuilt='生产污染不得侵入，缓冲范围随水流调查而定')]
programs=[dict(id=f'PROGRAM-{i:02}',demand_ref=d['id'],functions=d['response'],magnitude=d['magnitude'],adjacency=d['dependencies'],maturity=d['maturity'],externality=d['externalities'],delivery='SETTLEMENT Planner判断共享/嵌入/独立；不指定栋数、房间或立面') for i,d in enumerate(demands,1)]
kit=dict(shared_dna='成熟前现代石木工程；强地方自治与共享履约空间；不借魔法抹平供给',typology_skeletons=['混合家庭与低扰动工作','共享储备/维修/交割','可撤回季节驻留'],variation=['岩面需验证裂隙、排水、基础接触，少占土面','草土候选需查土深与植被权属，保持开放片连续性','陶瓦质表面不证明可制陶或承载，应独立查基底与冲刷','高差决定分簇与驮运/步行接口，不能套用平地统一组合'],forbidden=['整栋复制形成等距村落','指定block palette/屋顶/房间','草土=肥田、岩面=矿床','用万能石台抹平地表差异'])
plan=dict(id='MP-P02R-EAST',revision='r1',scale='REGIONAL_SYSTEM',state='HANDOFF_READY',state_meaning='可交SETTLEMENT Planner继续调查与规划；非实地可建、非回归或Owner验收结论',world_writes=0,builder_ready=False,parent='MP-P01R-CIV001:r1:PACKAGE-03',authority='DESIGN_PROPOSAL_PENDING_REVIEW',fabric_observation='EXISTING_FABRIC_UNVERIFIED',evolution='EXISTING_EVOLUTION',history_status='HYPOTHETICAL_CAUSAL_SEQUENCE_NOT_OBSERVED_HISTORY',nodes=nodes,routes=routes,demands=demands,anchors=anchors,growth=growth,commons=spaces,programs=programs,architecture_kit_requirements=kit,capacity_aggregation={'north':[6000,14000],'south_active':[3000,9000],'south_inactive':0,'total_north_only':[6000,14000],'total_with_one_south':[9000,23000],'mutually_exclusive':['NODE-03','NODE-04'],'not_carrying_capacity':True},branches=[{'id':'BRANCH-01','condition':'北部水/生计/通达成立，南部证据不足','result':'仅北部6k–14k；南部0'},{'id':'BRANCH-02','condition':'南部生产及NODE-03供给可行','result':'加3k–9k；NODE-04仅比较不建'},{'id':'BRANCH-03','condition':'NODE-04实际水/生计优势补偿高差且优于NODE-03','result':'南部迁为NODE-04；不叠加'},{'id':'BRANCH-00','condition':'北部角色无兼容水/路/生计位置','result':'保持无定址，报告PACKAGE-03 upstream planning issue'}])
dump('planning-data.json',plan)
packages=[]
for n in nodes[:3]:
 nid=n['id']; package=dict(id='PACKAGE-'+nid[-2:],parent_plan='MP-P02R-EAST',parent_revision='r1',parent_scale='REGIONAL_SYSTEM',child_scale='SETTLEMENT',recipient='minecraft-planner',authority='DESIGN_PROPOSAL_PENDING_REVIEW',scope_node_refs=[nid]+(['NODE-04'] if nid=='NODE-03' else []),why=n['role'],upstream_anchor_refs=['ANCHOR-01','ANCHOR-02','ANCHOR-03'] if nid!='NODE-03' else ['ANCHOR-04'],flow_refs=[q['id'] for q in routes if nid in q['ends']],upstream_fixed=['多个自治共同体，北部服务不独占东席','保持中域—北部—条件远端供给关系','搜索窗、建成容量、关系腹地三分；NODE-03/04互斥','保护待查土面与水源选择，不以绿色或裸岩直接定产能'],fixed_authority_note='Canon立即有效；本轮关系仅在本案被接受后约束下游，不升格World Canon',downstream_to_resolve=['先读取当前既有建筑/道路/土地权属，不按空白建设','逐候选检查稳定饮水、季节水量与污水方向','岩面裂隙/土深/陶瓦质基底/侵蚀；人工地表来源','植被逐地块覆盖、利用权与更新；土面生产可行性','连续驮路坡度、净空、转折、桥渡及装卸；不得以端点可达代替','实际资源地点与活动规模、燃料来源、粮食交换压力','建立聚落Anchor、历史继承、主通行与分区关系，再交L3'],downstream_adaptable=['在角色成立条件下迁移或拆分搜索位置','重新分配北部总容量，不能机械占满上限','本地catchment、内部层级与形态','南部季节化、取消或互斥替代'],capacity_hypothesis=n['built_fabric_capacity'],location_search_envelope=n['location_search_envelope'],functional_hinterland=n['functional_hinterland'],surface_evidence=n['profile'],surface_specific_requirement=n['sensitivity'],source_refs=n['source_refs'],cross_package_dependencies=[f'PACKAGE-{j:02}' for j in range(1,4) if j!=int(nid[-2:])],external_dependency='MP-P01R PACKAGE-02中域接口仅协调，无本轮设计权限',revision_triggers=['水/通达/既有权属使角色无兼容位置','容量显著超出范围或多个节点重复服务同一压力','具体资源与假设方向不符','保护地表后角色不可维持'],revision_protocol='先移位/拆分/季节化；仍不能满足关系则提最小受影响node/route/capacity证据，标UPSTREAM_PLANNING_ISSUE，父案revision后重跑Gate并标子包stale；不覆盖原父案',expected_outputs=['现状与地表证据','聚落Plan/关系与容量，非建筑设计','同坐标地图、machine-readable数据、L3交接包','供水/驮路/生计结论及未证边界'],world_write_authorization=False,builder_ready=False)
 packages.append(package)
dump('implementation-packages.json',packages)
dump('evidence/candidate-profiles.json',[{'id':n['id'],**n['profile']} for n in nodes])

# 坐标栅格只用于证据制图；面积符号为等面积示意，不是假精确聚落轮廓。
(R/'maps').mkdir(exist_ok=True)
F=lambda s:ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',s)
pal=np.array([[125,173,194],[158,181,109],[153,148,141],[220,198,148],[185,130,100],[127,113,98],[222,234,238],[82,136,82],[186,143,188]],dtype=np.uint8)
gy,gx=np.gradient(h.astype(float));v=np.clip((h-60)/240,0,1); terrain=np.stack([100+145*v,150+90*v,110+125*v],2)*np.clip(.85-(gx+gy)*.13,.35,1.15)[:,:,None];terrain[land!=2]=pal[0];terrain=np.uint8(np.clip(terrain,0,255))
cover=np.full((452,448,3),[224,217,199],dtype=np.uint8);cover[veg[:,:,0]>0]=[45,104,61];cover[land[::4,::4]!=2]=pal[0]
colors=['#b72a42','#5a3884','#bc6412','#08747a']
def dashed(d,p1,p2,color,width=2):
 length=math.dist(p1,p2)
 for t in np.arange(0,length,12):
  a=t/length;b=min(t+6,length)/length;d.line((p1[0]+(p2[0]-p1[0])*a,p1[1]+(p2[1]-p1[1])*a,p1[0]+(p2[0]-p1[0])*b,p1[1]+(p2[1]-p1[1])*b),fill=color,width=width)
for mode,arr,title in [('terrain',terrain,'地形与区域交换关系'),('surface',pal[surf],'地表差异与候选规模'),('cover',cover,'植被采样与开放地压力')]:
 im=Image.new('RGB',(1580,1090),'#f5f1e8');im.paste(Image.fromarray(arr).resize((896,904),Image.Resampling.NEAREST),(80,100));d=ImageDraw.Draw(im)
 def xy(p):return (80+(p[0]-320)/2,100+(p[1]-1456)/2)
 d.text((80,18),'MP-P02R | '+title+' | REGIONAL_SYSTEM',font=F(27),fill='#233a40');d.text((80,58),'X 向东 →   北 ↑（−Z）   1图素 = 2 blocks；候选与连线均为提案',font=F(18),fill='#33484a')
 for x in range(400,2100,200):u,_=xy((x,1456));d.line((u,100,u,1004),fill='#b7bbaa');d.text((u-15,1008),str(x),font=F(16),fill='black')
 for z in range(1600,3264,200):_,vv=xy((320,z));d.line((80,vv,976,vv),fill='#b7bbaa');d.text((10,vv),str(z),font=F(16),fill='black')
 for q in routes:
  pp=[xy(p) for p in q['points']]
  for a,b in zip(pp,pp[1:]):dashed(d,a,b,'#ac3651',3)
  d.text(pp[len(pp)//2],q['id'].replace('ROUTE-','R'),font=F(18),fill='#8e1537',stroke_width=2,stroke_fill='white')
 for n,col in zip(nodes,colors):
  b=n['location_search_envelope']['bounds'];p=xy(n['location_search_envelope']['representative_xz']);a=xy(b[:2]);bb=xy(b[2:]);d.rectangle((*a,*bb),outline=col,width=2)
  for area in n['built_fabric_capacity']['area_range_blocks2']:
   rad=math.sqrt(area/math.pi)/2;d.ellipse((p[0]-rad,p[1]-rad,p[0]+rad,p[1]+rad),outline=col,width=3)
  d.text((p[0]+8,p[1]+30),n['id'],font=F(18),fill=col,stroke_width=2,stroke_fill='white')
 d.text(xy((350,1600)),'中域接口',font=F(17),fill='#243a40',stroke_width=2,stroke_fill='white')
 y=105
 texts=['图例与阅读方法','细框：位置搜索窗，不是城界','双圆：下限/上限等面积符号','圆不表示真实圆形聚落或精确落位','虚线：双向交换关系，不是已通道路','腹地仅在数据中以服务关系表达','']
 if mode=='surface':
  for i,label in enumerate(['非东岛陆地掩膜/水面背景','草土表面','岩面（不证明矿床）','砂/砾','陶瓦质表面（不证明土层）','泥/黏土表面','雪/冰','表面植物','其它未决']):
   d.rectangle((1010,y,1031,y+16),fill=tuple(pal[i]));d.text((1040,y-3),label,font=F(17),fill='#233a40');y+=25
 elif mode=='terrain':texts+=['底图：exposed_y 派生地形晕渲','浅色总体较高，晕影提示坡折','全图高程约 Y60–300；非路线坡度图','剖面见关系线地形探针.png']
 else:texts+=['深绿：4格采样列发现树叶','米色：该采样列未发现树叶','非精确树冠范围；不证明森林产量','未画植被 ≠ 没有草木/使用权']
 for t in texts:d.text((1010,y),t,font=F(18),fill='#233a40');y+=27
 for n,col in zip(nodes,colors):
  d.text((1010,y),n['id']+' '+n['name'],font=F(18),fill=col);y+=27
  area=n['built_fabric_capacity']['area_range_blocks2'];d.text((1010,y),f'{area[0]:,}–{area[1]:,} blocks²；LOW',font=F(18),fill='#233a40');y+=30
 for t in ['南部03/04互斥，不相加；未启动为0','北部合计6k–14k；全部最多9k–23k','水/土深/实存/矿源/通达尚未验证','R1逐列快照；NG-3粗地理仅辅助','源版本 aeded8d / Skill 886a8f3','非当前游戏实时画面；world writes=0']:
  d.text((1010,y),t,font=F(17),fill='#233a40');y+=27
 d.line((80,1050,180,1050),fill='black',width=3);d.text((190,1037),'200 blocks  |  r1 · 待 GPT + Owner 审核',font=F(18),fill='#233a40')
 im.save(R/f'maps/{title}.png')

im=Image.new('RGB',(1450,1150),'#f5f1e8');d=ImageDraw.Draw(im);d.text((50,20),'候选区域：相同坐标范围的地形 / 地表 / 树叶采样比较',font=F(26),fill='#233a40')
for row,n in enumerate(nodes):
 b=n['profile']['bounds'];x,z,xx,zz=b;sl=(slice(z-1456,zz-1456+1),slice(x-320,xx-320+1)); yy=85+row*255
 for col,arr in enumerate([terrain[sl],pal[surf[sl]],np.repeat(np.repeat(cover,4,0),4,1)[sl]]):im.paste(Image.fromarray(arr).resize((235,235),Image.Resampling.NEAREST),(50+col*255,yy))
 p=n['profile'];s=p['surface_ratio'];lines=[n['id']+' '+n['name'],f'X{x}..{xx} / Z{z}..{zz}',f'Y p10/50/90 = '+str(p['y_p10_p50_p90']),f'草土 {s["SOIL_SURFACE"]:.1%} / 岩面 {s["ROCK_SURFACE"]:.1%}',f'陶瓦质 {s["TERRACOTTA_SURFACE"]:.1%} / 树叶样本 {p["leaf_sample_presence_ratio"]:.1%}',f'缓地列 {p["gentle_columns"]:,}；不等于可建容量','北部服务/家庭分担' if row<2 else '南部两个候选只能选择一个','比例为搜索窗内东岛陆地；非最终建成区']
 for j,t in enumerate(lines):d.text((830,yy+j*28),t,font=F(19),fill='#233a40')
d.text((50,1110),'上北右东；三列依次为地形/地表/树叶采样。色例同区域图；源R1，r1，非实时；world writes=0。',font=F(19),fill='#233a40');im.save(R/'maps/候选区域同范围比较.png')
im=Image.new('RGB',(1400,1040),'#f5f1e8');d=ImageDraw.Draw(im);d.text((55,20),'交换关系线地形探针（不是拟建道路纵断面）',font=F(28),fill='#233a40')
for i,q in enumerate(routes):
 y=95+i*225;ss=q['straight_relation_probe']['samples'];length=ss[-1][0];points=[(100+s[0]/length*1180,y+150-(s[3]-60)/240*145) for s in ss];d.line(points,fill='#3a6054',width=2);d.line((100,y+150,1280,y+150),fill='black');d.text((60,y-25),f'{q["id"]} | 直线折线长 {length:.0f} blocks | Y {q["straight_relation_probe"]["y_range"]}',font=F(19),fill='#233a40')
 for s in ss:d.rectangle((100+s[0]/length*1180,y+160,100+s[0]/length*1180+4,y+173),fill=tuple(pal[s[4]]))
 for yy in [60,180,300]:
  vv=y+150-(yy-60)/240*145;d.text((45,vv-10),str(yy),font=F(15),fill='#233a40')
 d.text((100,y+180),'0                      距离沿关系折线 →',font=F(16),fill='black');d.text((1230,y+180),str(round(length)),font=F(16),fill='black')
d.text((55,1000),'各栏同Y60–300；底部颜色为地表族。探针每约8格取样，不验证坡道、净空、连续通行或水源。',font=F(19),fill='#233a40');im.save(R/'maps/关系线地形探针.png')
print('generated',len(nodes),'nodes',len(packages),'packages')
