"""本轮人工街区方案的序列化、逐列几何核对及制图。

几何统计只检验表达一致性，不以面积、连通或方块类别替代规划判断。
"""
from pathlib import Path
import json,gzip,hashlib,subprocess,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent; MC=R.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['maps','sources','evidence']:(R/name).mkdir(exist_ok=True)
if not (R/'sources/source-register.json').exists():
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=MC.parent,text=True).strip();register=[]
    def record(rel,authority,selection):
        register.append(dict(path=rel,revision=revision,sha256=sha(MC/rel),authority=authority,selection=selection))
    p='MP-P03-NORTH-ROCK-TERRACE/implementation-packages.json';record(p,'DESIGN_PROPOSAL','PACKAGE-01 only')
    write(R/'sources/parent-package.json',next(o for o in read(MC/p) if o['id']=='PACKAGE-01'))
    p='MP-P03-NORTH-ROCK-TERRACE/planning-data.json';record(p,'DESIGN_PROPOSAL','DISTRICT-01; ROUTE-01/02 interface; SPACE-01; FRONTAGE-01/02; no other districts')
    old=read(MC/p)
    write(R/'sources/parent-interfaces.json',dict(districts=[o for o in old['districts'] if o['id']=='DISTRICT-01'],routes=[o for o in old['routes'] if o['id'] in ['ROUTE-01','ROUTE-02']],spaces=[o for o in old['spaces'] if o['id']=='SPACE-01'],frontages=[o for o in old['frontages'] if o.get('district')=='DISTRICT-01']))
    for rel,out,auth in [('MP-P03M-NORTH-ROCK-TERRACE/assessment-data.json','supplemental-assessment.json','DESIGN_PROPOSAL'),('建筑师/world/civilizations/CIV-001/README.md','Canon入口.md','APPROVED_CANON')]:
        record(rel,auth,'User-authorized input');(R/'sources'/out).write_bytes((MC/rel).read_bytes())
    for rel in ['MP-P03M-NORTH-ROCK-TERRACE/evidence/surface.json.gz','MP-P03M-NORTH-ROCK-TERRACE/evidence/world-read-provenance.json','MP-P03M-NORTH-ROCK-TERRACE/evidence/shallow-void-columns.json']:
        record(rel,'OBSERVED / DERIVED','Pure factual evidence and provenance')
    skillrev=(R/'sources/skill-revision.txt').read_text().strip()
    for p in sorted((R/'sources/skill').rglob('*.md')):register.append(dict(path='skill/codex/minecraft-planner/'+p.relative_to(R/'sources/skill').as_posix(),revision=skillrev,sha256=sha(p),authority='SKILL_INSTRUCTION',local_copy=p.relative_to(R).as_posix()))
    write(R/'sources/source-register.json',register)
source=json.loads(gzip.decompress((R/'evidence/surface-crop.json.gz').read_bytes()))
near=json.loads(gzip.decompress((R/'evidence/near-ground.json.gz').read_bytes()))
x0,z0,x1,z1=source['bounds'];xs,zs=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(z0,z1+1)+.5)
shape=xs.shape;height=np.zeros(shape,int);surface=np.zeros(shape,int)
def family(s):
    b=s.split('[')[0].split(':')[-1]
    if b=='lava':return 4
    if b in ['grass_block','dirt','coarse_dirt','podzol','rooted_dirt']:return 1
    if b in ['sand','gravel','red_sand']:return 2
    if b in ['stone','granite','diorite','andesite','tuff','deepslate','basalt','smooth_basalt'] or b.endswith('_ore'):return 0
    return 5
for c in source['columns']:
    x,z,_,y,state,water,*_=c;height[z-z0,x-x0]=y;surface[z-z0,x-x0]=3 if water is not None else family(source['palette'][state])
void=np.zeros(shape,bool);cover=np.full(shape,99);above=np.zeros(shape,int)
for c in near['columns']:
    states=[near['palette'][i].split('[')[0] for i in c['state_ids']];air=[-24+i for i,s in enumerate(states[:24]) if s in ['minecraft:air','minecraft:cave_air','minecraft:void_air']]
    j,i=c['z']-z0,c['x']-x0
    if air:void[j,i]=True;cover[j,i]=-max(air)
    above[j,i]=sum(s not in ['minecraft:air','minecraft:cave_air','minecraft:void_air'] for s in states[25:])
def polygon_mask(poly):
    m=np.zeros(shape,bool)
    for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1]):
        if b!=d:m^=((b>zs)!=(d>zs))&(xs<(c-a)*(zs-b)/(d-b)+a)
    return m
def line_mask(points,width):
    m=np.zeros(shape,bool)
    for (a,b),(c,d) in zip(points,points[1:]):
        t=np.clip(((xs-a)*(c-a)+(zs-b)*(d-b))/((c-a)**2+(d-b)**2),0,1)
        m|=(xs-a-t*(c-a))**2+(zs-b-t*(d-b))**2<=(width/2)**2
    return m
def area(poly):return abs(sum(a*d-c*b for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1])))/2
parent=read(R/'sources/parent-package.json');scope=parent['scope_geometry'];scope_mask=polygon_mask(scope)
parcels=[
 dict(id='PARCEL-01',block_ref='BLOCK-01',name='下肩修理与值守合院',polygon=[[750,1627],[765,1623],[768,1624],[768,1631],[760,1633],[751,1636]],frontage=[[751,1636],[760,1633],[768,1631]],households=1,why='西来货物最先需要小修理；较低肩部保留门前停留，生活小院嵌在后侧，较宽占地承担工作与工具暂存。',growth='GROWTH-02',access='SPACE-01 / LANE-04'),
 dict(id='PARCEL-02',block_ref='BLOCK-01',name='上沿复核与短宿合院',polygon=[[771,1625],[792,1628],[793,1633],[786,1636],[779,1630],[773,1630]],frontage=[[779,1630],[786,1636],[793,1633]],households=1,why='较高且临轻载出口，接单复核与值守短宿混合；不截断通往上台的东口。',growth='GROWTH-02',access='LANE-02 / LANE-04'),
 dict(id='PARCEL-03',block_ref='BLOCK-02',name='南沿收货家庭合院',polygon=[[757,1654],[775,1654],[776,1664],[758,1663]],frontage=[[757,1654],[775,1654]],households=1,why='面向卸载院，背后由小巷处理日常物品，前沿宽度保留多次小批卸货而非象征展示。',growth='GROWTH-02',access='SPACE-01 / LANE-03'),
 dict(id='PARCEL-04',block_ref='BLOCK-02',name='转角照看与轻修家庭',polygon=[[778,1653],[786,1649],[790,1653],[782,1663],[778,1664]],frontage=[[778,1653],[786,1649]],households=1,why='轮候院与背巷交会，照看共同库存并兼轻修；转角退出量大，不能用临街扩建封口。',growth='GROWTH-02',access='SPACE-01 / LANE-03'),
 dict(id='PARCEL-05',block_ref='BLOCK-03',name='共同体短储用地',polygon=[[787,1640],[794,1637],[794,1645],[791,1650],[788,1646]],frontage=[[787,1640],[788,1646],[791,1650]],households=0,why='已卸小批货再送短储；共同体持用抵制继承切分，不把它充当整个聚落的唯一粮仓。',growth='GROWTH-01',access='LANE-02 / LANE-03')
]
spaces=[dict(id='SPACE-01',name='卸载—复核共同院',polygon=[[750,1638],[760,1634],[774,1632],[779,1632],[785,1638],[786,1643],[780,1652],[761,1652],[753,1648]],controller='多共同体使用协议，待批准',use='西侧分批卸载，东侧轻载交付；院内通行与轮候分时，非驻养牲畜场',protection='沿院家庭不能圈占；最高峰溢出先错峰，不延伸到西南浅层异常边',growth='GROWTH-01'),dict(id='SPACE-02',name='南前沿共享门前带',polygon=[[757,1651],[776,1651],[783,1646],[786,1647],[786,1649],[778,1653],[778,1654],[757,1654]],controller='南侧两户使用地役，待批准',use='从公共院到家庭门前的步行、轻物交接；不计私人扩建地',protection='继承或分户后仍连续，不供牲畜长期站留',growth='GROWTH-02')]
lanes=[
 dict(id='LANE-01',name='西接卸载口',points=[[749,1647],[756,1645],[764,1642]],width=4,mode='PACK_CANDIDATE',why='只将到达货物送至首卸，保持相称回转与短等待；不以此宽度宣称驮畜已验证。',growth='GROWTH-01'),
 dict(id='LANE-02',name='东向轻载横通',points=[[778,1641],[787,1638],[796,1634]],width=3,mode='PEDESTRIAN_LIGHT_LOAD',why='从交割院通向父包ROUTE-02，侧门和停货不截断贯穿。',growth='GROWTH-01'),
 dict(id='LANE-03',name='南后巷与东侧接回',points=[[757,1664],[768,1665],[781,1666],[791,1654],[796,1644],[796,1634]],width=2,mode='PEDESTRIAN_SERVICE',why='前院交割繁忙时，家庭仍能从背侧进出和分时清运；窄边界不供重货与牲畜穿行。',growth='GROWTH-03'),
 dict(id='LANE-04',name='北前沿门前通行',points=[[751,1637],[760,1634],[769,1632],[778,1631],[786,1638]],width=2,mode='PEDESTRIAN',why='跨不同家庭门前的连续通行地役；不把院沿缝隙分配为私人可堵门廊。',growth='GROWTH-02')
]
objects=parcels+spaces+lanes;masks={}
for o in objects:
    m=polygon_mask(o['polygon']) if 'polygon' in o else line_mask(o['points'],o['width'])
    masks[o['id']]=m&scope_mask
    o.update(authority='DESIGN_PROPOSAL',geometry_semantics='PROVISIONAL_PARCEL_OR_SHARED_SPACE_NOT_BUILDING' if 'polygon' in o else 'PLANNING_LANE_ENVELOPE_NOT_ENGINEERED_ROAD',source_refs=['SRC-PARENT','SRC-FACT','SRC-CANON','SRC-ASSESSMENT'])
    vals=height[m&scope_mask]
    o['metrics']=dict(polygon_area=area(o['polygon']) if 'polygon' in o else None,cell_center_area=int((m&scope_mask).sum()),outside_scope_cells=int((m&~scope_mask).sum()),ground_y_range=[int(vals.min()),int(vals.max())],void24_columns=int((m&scope_mask&void).sum()),void16_columns=int((m&scope_mask&void&(cover<=16)).sum()),soil_columns=int((m&scope_mask&(surface==1)).sum()),above_ground_nonair_columns=int((m&scope_mask&(above>0)).sum()))
collisions=[]
for i,a in enumerate(parcels):
    for b in objects:
        if b['id']==a['id'] or (b in parcels and parcels.index(b)<i):continue
        n=int((masks[a['id']]&masks[b['id']]).sum())
        if n:collisions.append([a['id'],b['id'],n])
occupied=np.logical_or.reduce(list(masks.values()));private=np.logical_or.reduce([masks[o['id']] for o in parcels]);public=np.logical_or.reduce([masks[o['id']] for o in spaces+lanes])
summary=dict(scope_continuous_area=area(scope),scope_cell_center_area=int(scope_mask.sum()),parcel_area_including_shared_holding=int(private.sum()),public_area=int(public.sum()),union_area=int(occupied.sum()),unallocated_scope_area=int((scope_mask&~occupied).sum()),collisions=collisions,scope_void24_columns=int((void&scope_mask).sum()),occupied_void24_columns=int((void&occupied).sum()),scanned_columns=len(near['columns']),world_writes=0,cell_semantic='cell centers x+0.5,z+0.5; scope clips lane ends only; union avoids double-counting lanes inside commons')
write(R/'evidence/geometry-audit.json',summary)
plan=dict(id='MP-P04-WEST-APPROACH',revision='r1',scale='DISTRICT',authority='DESIGN_PROPOSAL',state='HANDOFF_READY',review_status='AWAITING_GPT_AND_OWNER',world_writes=0,world_write_authorization=False,builder_ready=False,parent='MP-P03-NORTH-ROCK-TERRACE / PACKAGE-01',supplement='MP-P03M-NORTH-ROCK-TERRACE / assessment-data',scope_polygon=scope,parcels=parcels,shared_spaces=spaces,lanes=lanes,area_ledger=summary)
blocks=[]
for bid,why in [('BLOCK-01','两家沿卸载院北侧形成混合前沿，后院在户用地内；不强造背街。'),('BLOCK-02','南侧收货与照看家庭组成较深合院，重复交割产生后巷通行需求。'),('BLOCK-03','共同持用的短储前沿不继承切分，连接轻载出口与后侧服务。')]:
    ps=[p for p in parcels if p['block_ref']==bid]
    blocks.append(dict(id=bid,type='PARCEL_GROUP_NOT_CLOSED_STREET_BLOCK',parcel_refs=[p['id'] for p in ps],geometry=dict(type='MULTIPOLYGON_MEMBERS',polygons=[p['polygon'] for p in ps]),why=why,authority='DESIGN_PROPOSAL'))
plan['blocks']=blocks
plan['frontages']=[dict(id='FRONTAGE-'+p['id'][-2:],parcel_ref=p['id'],points=p['frontage'],public_access=p['access'],meaning='门前交换/日常进入界面，不是建筑墙线',permission='使用地役需共同体及原权利人同意',authority='DESIGN_PROPOSAL') for p in parcels]
plan['source_refs']={'SRC-PARENT':'sources/parent-package.json + sources/parent-interfaces.json','SRC-FACT':'evidence/surface-crop.json.gz + evidence/near-ground.json.gz','SRC-CANON':'sources/Canon入口.md','SRC-ASSESSMENT':'sources/supplemental-assessment.json'}
plan['capacity']={'parent_households':[4,6],'selected_households':4,'parent_area_range':[1200,1600],'selected_union_area':summary['union_area'],'counting_rule':'cell-center union of parcels, shared court and lanes; blocks/frontages are overlay references not added area','five_six_households':'UNALLOCATED_CONDITIONAL: after supply and L4 habitable split test, may subdivide P01/P03 or redistribute inside same cap; no assumed extra buildable land','aggregate_parent_constraint':'Do not increase MP-P03 total3500–4600 by adopting MP-P03M settlement upper8000; parent coordination required','confidence':'LOW'}
plan['context']={'fabric_observation_state':'EXISTING_FABRIC_PARTIAL','evolution_logic':'EXISTING_EVOLUTION','maturity':'CONDITIONAL_TARGET_NOT_OBSERVED_HISTORY','coordinate_system':'Minecraft overworld X/Z, blocks; surface samples at integer columns; area evaluates cell center x+0.5,z+0.5','current_ownership':'UNKNOWN_TO_PLANNER','scope_note':'成熟文明内的候选街区；不得因未见地上房屋而认定空白土地'}
plan['conditions']=['供水与日需未证，常住分支不得启用施工','本地表面/净空扫描非实机驮运验证；西接路与东侧跨包续接未证','地块不是已批准地籍；现状与权属需确认','原浅16格空气带暂不分配建设；新17–24格空气不伪装地面缺口，P03与后巷保留基底复核条件','不擅用跨包水源、储备或污物终端容量']
plan['provisional_rights']={'commons':'参与共同体共管，反对沿院永久占用；非已批地方制度','parcels':'家庭用益及分户是假说，受既有权利调查约束','lanes':'L01/02公共交割与穿行，L03共享后巷，L04门前通行；关闭须保留等价通行','veto':'任何现有使用者冲突先局部移位；无法兼容才回报父包'}
plan['restrictions']=[{'id':'RESTRICTION-01','authority':'PARENT_PROPOSAL','geometry_ref':'evidence/near-ground-summary.json / minimum_cover<=16','rule':'不分配建设，不填洞、不默认地下室；本轮选用地块及通路与此类列无交集'}, {'id':'RESTRICTION-02','authority':'DESIGN_PROPOSAL','geometry_ref':'evidence/near-ground-summary.json / minimum_cover17..24','rule':'P03及L03所覆盖列只表达地块/通路候选，不分配建筑基础或重载；L4先调查拟用体积、局部移位或有界适应，再确认。不是整块地质禁建结论。'}, {'id':'RESTRICTION-03','authority':'DESIGN_PROPOSAL','geometry_ref':'evidence/near-ground-summary.json / block_entities','rule':'地下现存对象来源与权属未知，不推断成聚落，不授权改变'}]
for p in parcels:
    m=masks[p['id']];adj=np.zeros(shape,bool)
    adj[1:]|=public[:-1];adj[:-1]|=public[1:];adj[:,1:]|=public[:,:-1];adj[:,:-1]|=public[:,1:]
    p['metrics']['public_edge_adjacent_cells']=int((m&adj).sum())
    p['tenure']='PROPOSED_FAMILY_USE_NOT_CONFIRMED_TITLE' if p['households'] else 'PROPOSED_SHARED_HOLDING'
    p['rear_space_semantic']='家庭院落包含于地块内，确切房屋/院界由L4决定' if p['households'] else '装卸和门前通行不能侵入共享路带'
    p['ground_condition']='NO_AIR_OBSERVED_TO24_NOT_STABILITY_PROOF' if not p['metrics']['void24_columns'] else 'DEEPER_AIR_PRESENT; 基底复核前不得冻结房屋或地下室位置'
for lane in lanes:
    lane['rights']='PROPOSED_EASEMENT_NOT_CONFIRMED'
    lane['usable_route']='UNVERIFIED'
    lane['width_semantic']='规划通行带名义宽度，非实机净宽认证；端头跨父边界部分另协调，不计本包'
write(R/'planning-data.json',plan)
# 保存每一条连续路带的逐格中心线剖面，另有完整近地体素供独立核查。
profiles=[]
for lane in lanes:
    rows=[];seen=set();distance=0
    for a,b in zip(lane['points'],lane['points'][1:]):
        length=math.dist(a,b)
        for k in range(math.ceil(length)+1):
            t=min(k/length,1);x=round(a[0]+t*(b[0]-a[0]));z=round(a[1]+t*(b[1]-a[1]));key=(x,z)
            if key in seen:continue
            seen.add(key);rows.append([round(distance+k,2),x,z,int(height[z-z0,x-x0]),int(above[z-z0,x-x0]),int(cover[z-z0,x-x0]) if void[z-z0,x-x0] else None])
        distance+=length
    profiles.append(dict(id=lane['id'],fields=['distance','x','z','ground_y','nonair_above_1_to_4','nearest_air_depth_within24_or_null'],samples=rows,max_adjacent_ground_step=max(abs(a[3]-b[3]) for a,b in zip(rows,rows[1:])),not_movement_verification=True))
write(R/'evidence/lane-profiles.json',profiles)
write(R/'evidence/near-ground-summary.json',dict(bounds=near['bounds'],column_count=len(near['columns']),void_columns=[dict(x=int(x0+i),z=int(z0+j),minimum_cover=int(cover[j,i])) for j,i in zip(*np.nonzero(void))],block_entities=near['block_entities'],source_unchanged=True))
F='C:/Windows/Fonts/msyh.ttc'
def font(n):return ImageFont.truetype(F,n)
basecolors=np.array([[174,174,164],[119,159,93],[213,183,127],[72,146,184],[239,69,28],[145,114,145]])
def draw_map(stage=None):
    im=Image.new('RGB',(1710,1120),'#f6f2e8');d=ImageDraw.Draw(im);scale=14;ox,oz=85,120;bx,bz=742,1618
    def xy(p):return (ox+(p[0]-bx)*scale,oz+(p[1]-bz)*scale)
    for z in range(1618,1672):
        for x in range(742,801):
            y=height[z-z0,x-x0];c=basecolors[surface[z-z0,x-x0]];c=np.clip(c*(.83+.015*(y-129)),0,255).astype(int)
            a,b=xy((x,z));d.rectangle((a,b,a+scale,b+scale),fill=tuple(c))
            if void[z-z0,x-x0] and cover[z-z0,x-x0]<=16:d.line((a,b,a+scale,b+scale),fill='#b51978',width=2)
    for z in range(1620,1671,5):
        a,b=xy((742,z));d.line((a,b,a+59*scale,b),fill='#c9c8bd');d.text((36,b-9),str(z),font=font(16),fill='#243c42')
    for x in range(745,801,5):
        a,b=xy((x,1618));d.line((a,b,a,b+54*scale),fill='#c9c8bd');d.text((a-17,b+54*scale+6),str(x),font=font(16),fill='#243c42')
    d.line([xy(p) for p in scope+[scope[0]]],fill='#563a54',width=4)
    active=lambda o:stage is None or o['growth'] in stage
    for o in spaces:
        if active(o):d.polygon([xy(p) for p in o['polygon']],fill='#e2cc8d',outline='#8b7139')
    for o in lanes:
        if active(o):d.line([xy(p) for p in o['points']],fill='#f8eed3',width=o['width']*scale,joint='curve');d.line([xy(p) for p in o['points']],fill='#967b49',width=2)
    for o in parcels:
        if active(o):
            d.polygon([xy(p) for p in o['polygon']],fill='#bcd0cf' if o['households'] else '#c9bad4',outline='#365c61')
            d.line([xy(p) for p in o['frontage']],fill='#be5636',width=6)
            center=np.mean(o['polygon'],axis=0);a,b=xy(center);d.text((a-17,b-12),o['id'].replace('PARCEL-','P'),font=font(22),fill='#193a40')
    # 观测层再次叠加，避免被地块填色遮蔽。深空气以点标而非地面洞口符号。
    for z in range(1618,1672):
        for x in range(742,801):
            a,b=xy((x,z));j,i=z-z0,x-x0
            if x<800 and height[j,i]!=height[j,i+1]:d.line((a+scale,b,a+scale,b+scale),fill='#a4ada4',width=1)
            if void[j,i]:
                if cover[j,i]<=16:d.line((a,b,a+scale,b+scale),fill='#b51978',width=2)
                else:d.ellipse((a+5,b+5,a+8,b+8),fill='#963b88')
    for x,z in [(750,1640),(760,1643),(770,1640),(780,1642),(790,1643),(790,1629)]:
        a,b=xy((x,z));d.text((a-14,b-10),str(height[z-z0,x-x0]),font=font(15),fill='#283b37')
    title='内部地块与共享通路' if stage is None else ('短时交割起因' if len(stage)==1 else '供给闭合后的常住前沿')
    d.text((65,22),'MP-P04｜西接坡交割与修理前沿 · '+title,font=font(29),fill='#203b43')
    d.text((65,69),'DISTRICT · ↑北 −Z / 东 +X · 字段坐标为地块草案，不是房屋墙线',font=font(20),fill='#203b43')
    panel=['紫边：父案约束范围','细阶线+数字：实测地面Y','洋红斜线 ≤16深；点 17–24深空气','蓝灰：混合家庭用地 P01–04','紫灰：共同短储 P05','金色：共同卸载院 SPACE-01','浅带：通行地役候选 L01–04','红边：主要前沿；不是连续封墙','','西卸载 → 院内复核 → 东轻载','南后巷：日常步行与分时清运','北合院自留后院，不造整圈道路','','数字是面积账本，不是可施工证明',f'地块+公地+通路并集：{summary["union_area"]} 格²',f'未分配范围：{summary["unallocated_scope_area"]} 格²','当前分支4户；5–6户需核分户容量','供水、驮运、权利、持续需求待证','','P03/后巷下较深空气需核基底','不整片铺平；不填未知空洞','图外西接路及东供水接口仍待协调']
    panel[5]='金色：共同院 S01 / 南门前带 S02'
    if stage is not None:
        panel[13]='以下为成熟分支账本，非本阶段规模'
        panel[16]='本阶段不设常住；成熟分支条件4户' if len(stage)==1 else '本阶段仅在供给等条件成立后驻4户'
    for label,p,g in [('L01',(753,1646),'GROWTH-01'),('L02',(791,1636),'GROWTH-01'),('L03',(788,1659),'GROWTH-03'),('L04',(764,1633),'GROWTH-02'),('S01',(769,1646),'GROWTH-01'),('S02',(768,1653),'GROWTH-02')]:
        if stage is None or g in stage:
            a,b=xy(p);d.text((a-14,b-10),label,font=font(15),fill='#784b2a')
    for i,t in enumerate(panel):d.text((970,120+i*32),t,font=font(19),fill='#203b43')
    a,b=xy((745,1671));d.line((a,b+60,a+140,b+60),fill='#203b43',width=4);d.text((a,b+70),'10 blocks',font=font(18),fill='#203b43')
    d.text((70,1020),'OBSERVED/DERIVED：2026-09-13来源快照；本轮24格浅层复核。其余线面均DESIGN_PROPOSAL。',font=font(19),fill='#203b43')
    d.text((70,1054),'world writes = 0；不会因几何连通、表面平缓或未见空气而认定真实可用、安全或有权施工。',font=font(19),fill='#203b43')
    return im
draw_map().save(R/'maps/街区地块与通行.png')
draw_map(['GROWTH-01']).save(R/'maps/阶段01-交割起因.png')
draw_map(['GROWTH-01','GROWTH-02']).save(R/'maps/阶段02-条件常住.png')
im=Image.new('RGB',(1500,1060),'#f6f2e8');d=ImageDraw.Draw(im)
d.text((65,25),'MP-P04｜通路纵断面与地块高度关系',font=font(30),fill='#203b43')
d.text((65,76),'真实逐列地面；曲线未经过拟建路面整形。横轴沿候选线距离，纵轴为Y。',font=font(21),fill='#203b43')
for n,profile in enumerate(profiles):
    left,top=95,165+n*195;rows=profile['samples'];length=rows[-1][0];lo=min(r[3] for r in rows)-1;hi=max(r[3] for r in rows)+1
    pts=[(left+row[0]*11,top+130-(row[3]-lo)*18) for row in rows]
    d.text((left,top-35),f'{profile["id"]} · 最大相邻采样高差 {profile["max_adjacent_ground_step"]} 格',font=font(21),fill='#203b43')
    for yy in range(lo,hi+1):
        py=top+130-(yy-lo)*18;d.line((left,py,left+max(length,15)*11,py),fill='#d3d3c6');d.text((left-42,py-10),str(yy),font=font(15),fill='#203b43')
    d.line(pts,fill='#486861',width=3)
    for row,p in zip(rows,pts):
        if row[5] is not None:d.ellipse((p[0]-3,p[1]-3,p[0]+3,p[1]+3),fill='#a63880')
    d.text((left,top+144),f'0 → {length:.0f} blocks',font=font(17),fill='#203b43')
for i,t in enumerate(['P01：Y129–133，低肩分段接口','P02：Y133–136，轻载上沿','P03：Y133–135，深空气待核','P04：Y134–135，转角保留出口','P05：Y135–136，小批短储','','不统一削平到一个标高。','局部步级/门槛/路基由L4与Builder核定。','驮畜转弯、错车、实际脚下碰撞未证。','两端接续和地役权仍需跨包确认。','洋红点：路带下24格内有空气。','不是该点路面缺口或已证塌陷。']):d.text((890,190+i*40),t,font=font(19),fill='#203b43')
d.text((65,1010),'world writes = 0 · evidence/lane-profiles.json + near-ground.json.gz · 不以断面替代实际可用路线验证',font=font(18),fill='#203b43')
im.save(R/'maps/通路与高差剖面.png')
print(json.dumps(dict(summary=summary,objects=[dict(id=o['id'],metrics=o['metrics']) for o in objects]),ensure_ascii=False))
