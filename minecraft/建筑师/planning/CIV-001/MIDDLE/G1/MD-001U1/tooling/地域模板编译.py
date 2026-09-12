"""把本轮设计参数与尚待验证的变化规则明确分开；不注册正式建成资产。"""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('design',Path(__file__).with_name('街区设计编译.py'));d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
P='PROPOSED';V='PREVIEW_VALIDATED'
def rule(id,subject,text,status=P,**kw):return dict(id=id,subject=subject,rule=text,status=status,**kw)
shared=[
 rule('C01','构造','石基承担地面接口；木柱梁/石墙形成真实支承链，填充墙不冒充悬空承重。'),
 rule('C02','材料','主结构、次结构、屋面、填充共2–4种主材料；罕见/高亮色仅在功能节点克制使用。'),
 rule('C03','形成过程','形态差异由用途、街路、地形与分期产生；不随机破损或复制均等地块。'),
 rule('C04','尺度','门窗对应实际活动和楼层；先检验入口、楼梯、落脚与支承，再做细节。'),
 rule('C05','文明语义','普通日常建筑不布满魔法装置；契约/消息用可达的小公共界面表达，不默认官署。')]
regional=[
 rule('R01','混合与密度','以独立商住/短仓/饮食体量共享街巷和院；楼上增加生活，不吞占公共通行。',V,evidence='MD-001U1:487/1310 footprint;1046 gross floor area'),
 rule('R02','台基','各栋依地面独立定标高；优先0–2格局部填补、0–1格局部切削，超过须另作场地设计。',V,observed_instance_ranges='B1 0;B2 0..2;B3 0..1;B4 0..1;B5 -1..0'),
 rule('R03','跨间','常用柱间3–5格；末跨2–3格可容入口/楼梯；梁柱同楼板与支承相交。',bay_range=[3,5],end_bay_range=[2,3]),
 rule('R04','层高','生活层楼面到楼面4格；短仓首层5格；拟扩范围4–5格，净高至少2.5格。',V,validated_floor_deltas=[4,5]),
 rule('R05','屋顶','长仓横脊，转角旅舍陡双坡，低公共屋可四坡；坡比取1:2或1:1，半格台阶翻译后重核封口。',families=['gable-long','gable-steep','hipped-low'],pitch_rise_run=[[1,2],[1,1]]),
 rule('R06','开口层级','家门宽1–2高2–3；商门2高3；仓门3高3–4；不能占柱脚或让高门切断上层梁。',V,validated_clear_portals='width2/3,height3; no installed door blockstate'),
 rule('R07','窗与立面','生活窗1–2宽、2高；短仓首层实墙优先；寝区需要朝外采光，楼梯孔对应区不机械开窗。'),
 rule('R08','街边','短退界0–2格用于门槛/雨棚；退界随实际路线弯折，不把所有住宅平行后退成草坪街。'),
 rule('R09','街巷','常用步行净带2格，驮运3格为拟定下限；新细节不得侵入全高净空。外部道路仍需现状检验。'),
 rule('R10','间距','本例最近墙面3格、屋檐间1格仅作为维护界面；公共主巷不使用这一最窄间隙。',V,evidence='B4-B2 measured wall gap3; eave gap1; no fire-code claim'),
 rule('R11','坡岸转换','岸侧先防潮和水源验证；低地用独立石脚；坡麓用短挡墙/错层，禁止统一巨台推平。'),
 rule('R12','院落','院是饮食、家务、短交接与通行的共享空间；装卸停泊独立于全天居民净带。'),
 rule('R13','排水','檐沟→落水位置→有连续坡向的盖沟/明沟→可维护收水处；污物另收运，禁止把雨水沟当污水渠。'),
 rule('R14','细部','招牌只挂在入口/转角，告示可站读；灯设在门槛、楼梯和作业处，不等距满街插火把。'),
 rule('R15','边墙','本轮独立屋，不使用共用承重墙。后续贴邻必须另给防火墙、分户排水、维修权与独立疏散设计。'),
 rule('R16','地域边界','Middle以转接和紧凑混用区别于West农牧展开、East山地工程；不能只换同一房屋的色板。')]
modules=[
 ('M01','连续石脚/台基',{'width':[6,14],'depth':[7,13],'local_fill':[0,2],'local_cut':[0,1]},['terrain-column profile','ground floor Y'],['each wall/column has support','no strip of grass under a bearing wall'],['deep foundation below observed12 is unverified'],P),
 ('M02','两格直跑楼梯',{'width':[2,2],'rise':[4,5],'run':[4,5],'landing_length':[1,2],'tread_half_rise':0.5},['two floor elevations','reserved hole'],['hole covers run x2','clear ceiling volume over every tread and landing'],['trapdoor/beam over head envelope','no upper landing'],V),
 ('M03','家门/店门',{'clear_width':[2,2],'clear_height':[3,3],'wall_depth':[1,1]},['two continuous walking surfaces'],['opening through full wall','no canopy post in approach'],['door on a retained tree column without clearance resolution'],V),
 ('M04','短仓大门',{'clear_width':[3,3],'clear_height':[3,4],'wall_depth':[1,2]},['separate off-route unloading bay'],['lintel retains bearing','resident access independent of cargo door'],['forced customs or toll gate'],P),
 ('M05','生活窗',{'width':[1,2],'height':[2,2],'sill_above_floor':[1,1]},['room position','bay line'],['openings do not replace bearing posts'],['glass curtain wall','window over stair hole without review'],P),
 ('M06','短檐雨棚',{'depth':[1,2],'clear_height':[3,4],'projection_span':[4,10]},['door and route geometry'],['supported at margins','upper room egress not obstructed'],['post in cargo turning lane'],P),
 ('M07','门廊',{'width':[3,5],'depth':[2,3]},['entry sequence'],['one continuous door/landing route'],['fortified entrance across public road'],P),
 ('M08','小阳台',{'depth':[1,2],'width':[3,6],'rail_height':[1,1.5]},['upper room','street role'],['bearing beam/cantilever accounted','no overhanging neighbour parcel'],['heavy stone deck on unsupported timber skin'],P),
 ('M09','短拱廊',{'bays':[2,3],'clear_bay_width':[3,4],'height':[3,4]},['public frontage need'],['columns leave continuous2-wide path','independent structural spans'],['arcade merely square holes labelled pointed arches','road enclosure'],P),
 ('M10','院墙/小门',{'height':[1,2],'gate_width':[2,3]},['shared court boundary','public access rights'],['resident through-route stays open','drain outlet not blocked'],['all four sides sealed without outfall'],P),
 ('M11','服务院',{'clear_area':[24,72],'passage_width':[2,3]},['loading and waste destinations'],['standing loads separate from passing','maintenance access'],['mixed sewage and clean storage'],P),
 ('M12','转角/尽端',{'corner_recess':[0,2],'eave_projection':[0.5,1]},['street junction','neighbour roof geometry'],['corner sightline','no accidental inaccessible slit'],['mirror copy for its own sake'],P),
 ('M13','盖沟/坡阶',{'channel_width':[1,1],'cover_width':[1,2],'step_rise':[0.5,0.5]},['current terrain','local receiver'],['monotone invert','walkable crossing separate from water volume'],['source-water staircase without fluid update','polluted outfall'],P),
 ('M14','储水/消防/干污物位',{'clean_storage_area':[2,6],'fire_storage_area':[2,6],'dry_waste_area':[2,4]},['verified source and servicing plan'],['covered clean storage','separate sealed waste','no emergency lane storage'],['treat nearby water as confirmed potable'],P),
 ('M15','小招牌与告示',{'width':[1,2],'height':[1,2],'reading_clearance':[2,3]},['named activity and doorway'],['limited accent','standing reader outside route'],['inventing tax or border-control authority'],P)]
module_objs=[]
for id,name,ranges,inputs,inv,forbidden,status in modules:module_objs.append(dict(id=id,name=name,status=status,dimension_ranges_blocks=ranges,inputs=inputs,invariants=inv,incompatible=forbidden,
    preview_evidence='MD-001U1/validation/design-qa.json; chosen instances only, real collision UNVERIFIED' if status==V else None))
typologies=[]
for id,name,width,depth,storeys,core,optional,terrain,bad in [
 ('T01','mixed-shop-house',[9,14],[8,12],[2,3],['street shop','independent home entrance','upper living','M02'],['M06','M08'],['lowland plinth','small split level'],['single shop door controls all homes']),
 ('T02','short-storage-residence',[11,15],[9,14],[2,2],['high clear ground store','cargo portal','home access','off-route handover'],['M04','M06','M11'],['dry lowland','independent terrace'],['bulk industrial warehouse in G1','home stair through locked cargo racks']),
 ('T03','repair-house',[8,12],[7,11],[1,2],['cold-work area','materials rack','home/learner space','service apron'],['M06','M11'],['small low plinth','edge terrace'],['hot metal process below timber bedrooms']),
 ('T04','inn-food',[10,14],[9,14],[2,3],['food room','separate cook/flue location','host family','guest floor','M02'],['M07','M08'],['street corner','terrace step'],['guest access through private sleeping area','timber touching flue']),
 ('T05','record-service',[6,9],[7,10],[1,2],['readable front room','record/help desk','short care place'],['M07','M15'],['low end piece','step terrace'],['dominant government/toll iconography']),
 ('T06','courtyard-service-compound',[12,24],[8,18],[0,0],['daily passage','water/fire access','shared activity','separate short unloading'],['M10','M11','M14'],['split court','covered crossing at swale'],['sealed basin','fill every gap','uniform four-side cloister by default'])]:
    typologies.append({'id':id,'name':name,'status':P,'required_core':core,'optional_modules':optional,
        'dimension_ranges_blocks':{'width':width,'depth':depth,'storeys':storeys},'proportion':'usually width/depth0.65..1.8; compound may bend with terrain, area is not a rectangular plot mandate',
        'variation_knobs':['function and load','plot edge','age/addition sequence','slope and entry Y','street corner or end','craft/status'],
        'terrain_adaptation':terrain,'incompatible':bad,'not_fixed_blueprint':True})
palettes=[
 {'id':'working-stone','status':P,'structure':['stone','cobblestone'],'upper_frame':['stripped_oak_log'],'infill':['mud_bricks'],'roof':['stone_brick_slab','stone_brick_stairs'],'accent':['oak_sign'],'use':'B1 working ground floor/B5 public plinth; heavy roof requires actual truss/support closure before build'},
 {'id':'lime-timber','status':P,'structure':['stone'],'upper_frame':['stripped_oak_log'],'infill':['smooth_sandstone'],'roof':['spruce_stairs','spruce_slab'],'accent':['oak_trapdoor'],'use':'B2 cared-for food/guest frontage'},
 {'id':'earth-timber','status':P,'structure':['cobblestone'],'upper_frame':['stripped_oak_log'],'infill':['packed_mud'],'roof':['dark_oak_stairs','dark_oak_slab'],'accent':['oak_sign'],'use':'B3 everyday retail-house; paired window where living activity needs light'},
 {'id':'repair-timber','status':P,'structure':['cobblestone'],'upper_frame':['stripped_acacia_log'],'infill':['mud_bricks'],'roof':['spruce_stairs','spruce_slab'],'accent':['oak_fence'],'use':'B4 economical cold-repair frontage; patches only where repair phase explains them'}]
variations=[rule('V01','功能','仓首层5格与3格门；住家层4格、2格门；不要仅换颜色。'),rule('V02','年代','后增雨棚、不同维护程度的填充墙可改变立面；结构柱仍连续。'),
 rule('V03','地块','转角短面可承担入口或次窗，末跨可缩；不得随机旋转脱离路。'),rule('V04','地形','在本例0–2填/0–1切之外的场地须重做剖面；不扩大台基套用。'),
 rule('V05','等级/工匠','常用房以土色，旅舍入口可浅色；装饰集中门梁，不把每栋换成不同文明。'),rule('V06','变化界限','一个组团至少由用途产生两种脊向、不同高度与入口等级；这是审阅提示，不是自动评分器。')]
d.write(d.KIT/'KIT.json',{'schema':'civ-architecture-kit/0.1','civilization':'CIV-001','region':'MIDDLE','version':'0.1','status':P,
    'shared_dna':shared,'regional_dna':regional,'maturity_ceiling':V,'source_design':'planning/CIV-001/MIDDLE/G1/MD-001U1',
    'compile_order':['Site Context','Program/Space Graph','Plan+Section+Sequence','Choose/fit typology and modules','Geometric/semantic Critic','Preview','GPT+Owner review'],
    'formal_asset_registration':False,'world_writes':0})
d.write(d.KIT/'modules.json',{'schema':'civ-modules/0.1','modules':module_objs})
d.write(d.KIT/'typologies.json',{'schema':'civ-typologies/0.1','typologies':typologies})
d.write(d.KIT/'palette-families.json',{'schema':'civ-palettes/0.1','families':palettes,'availability':'design choices, not proof of on-site stock or supply chain','prefix':'minecraft:','preview_colors':'schematic; palette textures not client-validated'})
d.write(d.KIT/'variation-rules.json',{'schema':'civ-variation-rules/0.1','rules':variations,'randomization_policy':'no stochastic noise or whole-building cloning'})
print('kit',len(shared)+len(regional),'rules',len(modules),'modules',len(typologies),'typologies')
