"""MD-001U1 设计外围脚本：读取冻结证据，编译审阅模型；不提供存档写入入口。

几何单位为 block；建筑坐标为半开实体盒，场地 RLE 为包含端点的 block-column。
预览模型不是施工蓝图；碰撞检查只覆盖本脚本定义的保守设计包络。
"""
import json, gzip, hashlib, importlib.util, math
from pathlib import Path
from collections import Counter, deque
from datetime import datetime, timezone

OUT=Path(__file__).resolve().parents[1]
ROOT=next(p for p in OUT.parents if p.name=='建筑师')
PLAN=ROOT/'planning/CIV-001/MIDDLE/MD-001P'
S1=ROOT/'research/build-sites/CIV-001/MD-001S1'
CACHE=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001S1')
KIT=ROOT/'architecture/civilizations/CIV-001/kits/MIDDLE/v0.1'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cells(runs): return {(x,z) for z,l,r in runs for x in range(l,r+1)}
def rect(a,b,c,d): return {(x,z) for x in range(a,c+1) for z in range(b,d+1)}
def rle(points):
    out=[]
    for z in sorted({z for x,z in points}):
        xs=sorted(x for x,zz in points if zz==z);start=last=xs[0]
        for x in xs[1:]:
            if x!=last+1:out.append([z,start,last]);start=x
            last=x
        out.append([z,start,last])
    return out
def dilate(points,n):
    result=set(points)
    for _ in range(n): result|={(x+dx,z+dz) for x,z in result for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]}
    return result

def freshness():
    a=read(CACHE/'capture.json');records=[]
    for f in a['snapshot_files']:
        p=Path(a['world_path'])/f['world_relative'];s=p.stat()
        actual=sha(p)
        assert actual==f['sha256'] and s.st_size==f['size'] and s.st_mtime_ns==f['mtime_ns'], 'snapshot stale: '+str(p)
        assert sha(CACHE/'snapshot'/f['snapshot_name'])==actual
        records.append({**f,'matches_current':True})
    return {'checked_at_utc':datetime.now(timezone.utc).isoformat(),'source_capture_utc':a['snapshot_finished_at'],
            'world_name':a['world_name'],'data_version':a['data_version'],'files':records,'world_writes':0,
            'method':'read-only SHA256 + size + mtime comparison; no runtime launched',
            'scope':'five identity/session/local containers, not whole-save inventory'}

SURF={(p['x'],p['z']):p for p in json.load(gzip.open(CACHE/'surface.json.gz','rt',encoding='utf-8'))}
G1=cells(next(n for n in read(PLAN/'settlement-nodes.json')['nodes'] if n['id']=='G1')['envelope'])
LU=read(PLAN/'land-use.json');CLEAR=cells(LU['building_exclusion_overlays'][0]['geometry'])
ENVELOPE=rect(189,1695,237,1723)&G1-CLEAR
# 两级台地之间保留可达的缓坡和生活院；范围来自这组活动的相邻关系。
BUILDINGS=[
 {'id':'B1','name':'高台短仓与仓管住家','type':'short-storage-residence','bounds':[222,1697,234,1706],'floors':[68,73],'eave':77,'roof_axis':'x','pitch':0.5,'palette':'working-stone','phase':1,'doors':[[226,1706,68,3],[222,1701,68,2]],'program':['短存/交接/手推货物','仓管家庭、起居与寝区'],'cause':'干燥高台承重仓底；长脊顺装卸面，楼上不占地增加家庭生活'},
 {'id':'B2','name':'转角饮食与小旅舍','type':'inn-food','bounds':[202,1698,213,1707],'floors':[66,70,74],'eave':78,'roof_axis':'z','pitch':0.5,'palette':'lime-timber','phase':2,'doors':[[207,1707,66,2]],'program':['饮食/备餐/柜台','经营家庭起居、寝区','两组短住房与共用小厅'],'cause':'处于生活院转角，三层节约低地；窄向屋脊与仓库横脊相对'},
 {'id':'B3','name':'沿路日用品商住','type':'mixed-shop-house','bounds':[193,1713,205,1721],'floors':[66,70],'eave':74,'roof_axis':'x','pitch':0.5,'palette':'earth-timber','phase':1,'doors':[[199,1721,66,2],[199,1713,66,2]],'program':['铺面/日用品/内院家务','铺户家庭寝居'],'cause':'南向公共买卖、北向住家入口；不以商店营业开关控制居民通行'},
 {'id':'B4','name':'鞍具木器修理住屋','type':'repair-house','bounds':[190,1701,198,1708],'floors':[65,69],'eave':73,'roof_axis':'z','pitch':0.5,'palette':'repair-timber','phase':2,'doors':[[194,1708,65,2]],'program':['冷作修理/材料架','工匠家庭与学徒寝居'],'cause':'低台短进深，南面作业口；只修鞍具木器，无熔炉、锻造或明火工序'},
 {'id':'B5','name':'消息与照护小屋','type':'record-service','bounds':[220,1712,225,1719],'floors':[68],'eave':72,'roof_axis':'z','pitch':0.5,'palette':'working-stone','phase':3,'doors':[[220,1715,68,2]],'program':['问路/告示/小记录/短时照护'],'cause':'低檐尽端体量让住家与短仓之间留下视线；不是官署、查验处或收费点'}
]

def observe():
    proof=freshness();write(OUT/'validation/source-freshness-before.json',proof)
    for b in BUILDINGS:
        x,z,X,Z=b['bounds'];ps=rect(x,z,X,Z);b['footprint_area']=len(ps)
        b['ground_y_range']=[min(SURF[p]['ground_y'] for p in ps),max(SURF[p]['ground_y'] for p in ps)]
        b['ground_floor_fill_range']=[b['floors'][0]-1-v for v in b['ground_y_range'][::-1]]
        assert ps<=ENVELOPE
        assert rect(x-1,z-1,X+1,Z+1)<=ENVELOPE, b['id']+' roof out of envelope'
    # 只扩读本微街区及四格缓冲的浅层，复用同一已验证快照，不重取整个 G1。
    scope=dilate(ENVELOPE,4);assert scope<=set(SURF)
    spec=importlib.util.spec_from_file_location('site_reader',S1/'tooling/当前场地读取.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);reader=m.Reader()
    counts=Counter();anomalies=[];above=Counter();trees=[]
    for x,z in sorted(scope):
        p=SURF[x,z]
        for y in range(p['ground_y']-12,p['ground_y']+1):
            n=reader.block(x,y,z);counts[n]+=1
            if n in m.AIR|m.WATER|{'minecraft:lava'} or m.artificial(n):anomalies.append([x,y,z,n])
        if (x,z) in ENVELOPE:
            for y,n in p['above']:
                if n not in m.AIR:above[n]+=1
                if '_log' in n:trees.append([x,y,z,n])
    write(OUT/'validation/local-context.json',{'lineage':'MD-001S1 capture; identical current source SHA256','surface_reused_columns':len(ENVELOPE),
        'subsurface_scope_rle':rle(scope),'subsurface_columns':len(scope),'depth_below_surface':12,'block_queries':len(scope)*13,
        'materials':dict(counts),'anomalies':anomalies,'above_ground_materials_in_envelope':dict(above),'log_blocks_in_envelope':trees,
        'reader_sha256':sha(S1/'tooling/当前场地读取.py'),'raw_cache':'LOCAL_ONLY: MD-001S1/snapshot and surface.json.gz',
        'limitations':['natural block placement provenance unknown','deep underground not surveyed','water source not confirmed','entities and POIs reuse MD-001S1 selected-chunk audit; recheck before build']})
    write(OUT/'site-envelope.json',{'schema':'civ-design-envelope/1','id':'MD-001U1-E1','status':'DESIGN_PROPOSAL','rle_inclusive':rle(ENVELOPE),
        'gross_columns':len(ENVELOPE),'G1_columns':len(G1),'geometry_rule':'G1 intersect X189..237,Z1695..1723 minus accepted through-clearance',
        'ground_y_range':[min(SURF[p]['ground_y'] for p in ENVELOPE),max(SURF[p]['ground_y'] for p in ENVELOPE)],
        'terrain_histogram':dict(Counter(SURF[p]['ground_y'] for p in ENVELOPE)),
        'clearance_overlap':len(ENVELOPE&CLEAR),'not_a_write_volume':True})
    write(OUT/'building-roles.json',{'coordinate_contract':'bounds=[xmin,zmin,xmax,zmax] inclusive; floors=finished walking surface Y','buildings':BUILDINGS})
    manifest=OUT/'validation/source-inputs.json'
    if manifest.exists():
        for item in read(manifest)['inputs']:assert sha(ROOT/item['path'])==item['sha256'], 'protected input changed: '+item['path']
    else:
        write(manifest,{'baseline_commit':'d06eb07b3725d11744c6715259823a7ef031c156','inputs':[
            {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for folder in [PLAN,S1,ROOT/'world',ROOT/'decisions'] for p in sorted(folder.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],
            'skill':{'url':'https://raw.githubusercontent.com/zhangchenjia21-dot/Vibe-Coding/main/skill/codex/minecraft-builder/SKILL.md','version':'1.10','sha256':sha(Path('D:/Games/Minecraft/AI工程/研究缓存/minecraft-builder-current-SKILL.md'))}})

# 设计盒按精确实体交集校验；颜色只用于审阅，非真实 Minecraft 纹理。
BOXES=[];ROUTES=[];OPENINGS=[];STAIRS=[]
COLORS={'stone':'#92938b','timber':'#574536','floor':'#9a7b50','lime':'#d7c8a5','earth':'#b9a080','roof':'#705343','darkroof':'#56544d','glass':'#749b9d','paving':'#b3aa91','rail':'#71563e','water':'#719ba0','sign':'#e2c288','hearth':'#514f48','grass':'#85966a','soil':'#9d9178'}
def box(a,b,mat,owner,role):
    if all(b[i]>a[i] for i in range(3)):BOXES.append({'a':list(a),'b':list(b),'material':mat,'owner':owner,'role':role})
def walkway(name,points,width=2,kind='resident'):
    # 显式线段插值；站立面每半格检查，不以终点 BFS 冒充路径验证。
    samples=[]
    for a,b in zip(points,points[1:]):
        n=max(1,math.ceil(math.dist(a,b)*2))
        samples.extend([[round(a[i]+(b[i]-a[i])*t/n,4) for i in range(3)] for t in range(n)])
    samples.append(points[-1]);ROUTES.append({'id':name,'kind':kind,'width':width,'points':points,'samples':samples})

def model():
    BOXES.clear();ROUTES.clear();OPENINGS.clear();STAIRS.clear()
    for b in BUILDINGS:
        x,z,X,Z=b['bounds'];X+=1;Z+=1;f=b['floors'][0];owner=b['id']
        bay={'B1':4,'B2':3,'B3':5,'B4':4,'B5':3}[owner];b['bay']=bay
        if owner=='B2':b['pitch']=1
        b['roof_family']='hipped' if owner=='B5' else 'gable'
        # 墙底和地坪从真实地面接起；不在整片台地下面铺统一巨台。
        for xx,zz in rect(x,z,X-1,Z-1):box((xx,SURF[xx,zz]['ground_y'],zz),(xx+1,f-1,zz+1),'stone',owner,'foundation')
        sx=x+2;sz=z+2
        for i,fy in enumerate(b['floors']):
            rise=(b['floors'][i+1]-fy) if i+1<len(b['floors']) else None
            hole=None if i==0 else (sx,sz,sx+b['floors'][i]-b['floors'][i-1],sz+2)
            for xx,zz in rect(x,z,X-1,Z-1):
                if hole and hole[0]<=xx<hole[2] and hole[1]<=zz<hole[3]:continue
                mat='stone' if owner=='B2' and 210<=xx<=212 and 1698<=zz<=1700 else 'floor'
                if i==0 and (xx in (x,X-1) or zz in (z,Z-1)):mat='stone'
                box((xx,fy-1,zz),(xx+1,fy,zz+1),mat,owner,'floor')
            ceil=b['floors'][i+1]-1 if rise else b['eave']
            # 门洞与窗洞先定义，再生成承重墙，不把洞藏在表皮后。
            openings=[]
            if i==0:
                for dx,dz,dy,w in b['doors']:
                    if dx==x:bounds=[x,fy,dz,x+1,fy+3,dz+w]
                    else:bounds=[dx,fy,dz,dx+w,fy+3,dz+1]
                    openings.append(bounds);OPENINGS.append({'owner':owner,'bounds':bounds,'kind':'door','clear_height':3})
            wallmat='stone' if i==0 else ('lime' if b['palette']=='lime-timber' else 'earth')
            windows=[]
            # 北面楼梯不设窗；开口位置对应可用活动带，重仓首层少窗。
            if i>0 or owner!='B1':
                for wx in range(x+2,X-2,bay):
                    for wz in [z,Z-1]:
                        if wz==z and sx<=wx<sx+5:continue
                        if owner=='B2' and wz==z and wx>=210:continue
                        windows.append([wx,fy+1,wz,wx+(2 if owner=='B3' else 1),fy+3,wz+1])
                if i>0:windows.append([X-1,fy+1,Z-4,X,fy+3,Z-2])
            for xx,zz in rect(x,z,X-1,Z-1):
                if xx not in (x,X-1) and zz not in (z,Z-1):continue
                for yy in range(fy,ceil):
                    if any(a<=xx<A and c<=zz<C and h<=yy<H for a,h,c,A,H,C in openings):continue
                    win=any(a<=xx<A and c<=zz<C and h<=yy<H for a,h,c,A,H,C in windows)
                    mat='glass' if win else ('timber' if (xx in (x,X-1) and zz in (z,Z-1)) or (i>0 and (xx-x)%bay==0) else wallmat)
                    if owner=='B2' and 210<=xx<=212 and zz==1698:mat='stone'
                    box((xx,yy,zz),(xx+1,yy+1,zz+1),mat,owner,'window' if win else 'wall')
            if rise:
                for k in range(rise*2):
                    top=fy+(k+1)*.5
                    box((sx+k*.5,fy,sz),(sx+(k+1)*.5,top,sz+2),'timber',owner,'stair')
                    for az,bz in [(sz-.2,sz),(sz+2,sz+2.2)]:box((sx+k*.5,top,az),(sx+(k+1)*.5,top+1,bz),'rail',owner,'stair-guard')
                for az,bz in [(sz-.2,sz),(sz+2,sz+2.2)]:box((sx,fy+rise,az),(sx+rise,fy+rise+1,bz),'rail',owner,'hole-guard')
                pts=[[sx-.5,fy,sz+1]]+[[sx+k*.5+.25,fy+(k+1)*.5,sz+1] for k in range(rise*2)]+[[sx+rise+.5,fy+rise,sz+1]]
                # 每一踏步顶面单独取样，净空不把台阶实体自身误判为障碍。
                STAIRS.append({'id':owner+'-'+str(i),'owner':owner,'samples':pts,'rise':rise,'width':2,'stair_hole':[sx,sz,sx+rise,sz+2]})
            # 南侧活动带不占楼梯前后落脚。家具是功能位置原型，并非成品室内装饰。
            if i==0 and owner=='B1':
                for xx in [x+2,X-3]:box((xx,fy,Z-4),(xx+1,fy+1,Z-2),'timber',owner,'storage-rack')
            elif i==0 and owner=='B2':
                box((X-3,fy,z+1),(X-1,fy+1,z+3),'hearth',owner,'enclosed-cook-zone')
                box((x+2,fy,Z-3),(x+4,fy+1,Z-2),'floor',owner,'meal-table')
            elif i==0 and owner=='B4':box((X-3,fy,Z-3),(X-1,fy+1,Z-2),'timber',owner,'cold-repair-bench')
            elif i==0 and owner=='B5':box((x+3,fy,z+2),(x+5,fy+1,z+3),'floor',owner,'record-desk')
            elif owner=='B2' and i==2:
                for bx in [203,209]:box((bx,fy,1705),(bx+2,fy+.5,1706),'earth',owner,'guest-sleep-platform')
                box((208,fy,1704),(209,fy+3,1707),'timber',owner,'guest-partition')
                for ax,bx in [(203,205),(207,208),(209,211)]:box((ax,fy,1704),(bx,fy+3,1704.25),'earth',owner,'guest-room-screen')
                walkway('B2-GUEST-WEST',[[208.5,fy,1701],[209.5,fy,1703],[206,fy,1703],[206,fy,1705.5]],.6,'interior')
                walkway('B2-GUEST-EAST',[[212.5,fy,1701],[212,fy,1703],[212,fy,1705.5]],.6,'interior')
            elif i>0:
                box((x+1,fy,Z-3),(x+3,fy+.5,Z-2),'earth',owner,'sleep-platform')
                # 厅→寝区的屏风不横断主步行带。
                box((x+4,fy,Z-3),(x+4.25,fy+2,Z-1),'timber',owner,'sleep-screen')
        # 屋面逐条半格坡，屋脊方向由长仓/转角旅舍功能决定。
        span=(Z-z if b['roof_axis']=='x' else X-x);mid=(z+Z)/2 if b['roof_axis']=='x' else (x+X)/2
        lo=z-1 if b['roof_axis']=='x' else x-1;hi=Z+1 if b['roof_axis']=='x' else X+1
        for k in range(lo,hi):
            if owner=='B5':continue
            ry=b['eave']+max(0,(span/2-abs(k+.5-mid))*b['pitch'])
            thickness=max(.5,b['pitch'])
            if b['roof_axis']=='x':box((x-1,ry,k),(X+1,ry+thickness,k+1),'darkroof' if owner=='B1' else 'roof',owner,'roof')
            else:box((k,ry,z-1),(k+1,ry+thickness,Z+1),'roof',owner,'roof')
            if lo<k<hi-1:
                if b['roof_axis']=='x':
                    for ex in [x,X-1]:box((ex,b['eave'],k),(ex+1,ry,k+1),'earth',owner,'gable')
                else:
                    for ez in [z,Z-1]:box((k,b['eave'],ez),(k+1,ry,ez+1),'earth',owner,'gable')
        # 顶层系梁在可用净高之上；它支承屋架，并非贴在立面的假梁。
        if owner=='B5':
            for xx,zz in rect(x-1,z-1,X,Z):
                ry=b['eave']+max(0,min(xx-x+.5,X-xx-.5,zz-z+.5,Z-zz-.5))*.5
                box((xx,ry,zz),(xx+1,ry+.5,zz+1),'darkroof',owner,'roof')
        for xx in range(x+2,X-1,bay):box((xx,b['eave']-.5,z),(xx+.5,b['eave'],Z),'timber',owner,'tie-beam')
        b['ridge_y']=max(v['b'][1] for v in BOXES if v['owner']==owner and v['role']=='roof')
        if owner in ['B1','B3']:
            ax=223 if owner=='B1' else 198;az=1707 if owner=='B1' else 1722;w=10 if owner=='B1' else 5;ay=72 if owner=='B1' else 69.5
            box((ax,ay,az),(ax+w,ay+.5,az+2),'roof',owner,'canopy')
            for px in [ax,ax+w-.5]:box((px,f,az+1.5),(px+.5,ay,az+2),'timber',owner,'canopy-post')
        if owner=='B2':box((211,67,1699),(212,84,1700),'stone',owner,'flue-reservation')
        # 下层门至楼梯、楼梯至上层活动带，分别为受约束的 expected edges。
        if len(b['floors'])>1:
            dx,dz,_,dw=b['doors'][0];doorx=dx+dw/2
            walkway(owner+'-ENTRY-STAIR',[[doorx,f,Z-.5],[doorx,f,Z-1.5],[sx-.5,f,Z-1.5],[sx-.5,f,sz+1]],.6,'interior')
            for i,fy in enumerate(b['floors'][1:]):
                rise=fy-b['floors'][i]
                walkway(owner+'-UPPER-'+str(i),[[sx+rise+.5,fy,sz+1],[X-1.5,fy,sz+1],[X-1.5,fy,Z-1.5],[X-3,fy,Z-1.5]],.6,'interior')
    # 所有室外面只是设计，且严格限于包络；默认保留原坡而非统一找平。
    occupied=set().union(*(rect(*b['bounds']) for b in BUILDINGS))
    for x,z in ENVELOPE-occupied:
        gy=SURF[x,z]['ground_y'];mat='soil' if 1708<=z<=1713 else 'grass'
        box((x,gy+.8,z),(x+1,gy+1,z+1),mat,'SPACE','ground-surface')
    # 生活与装卸有两条独立接入，居民不必经过仓门或关上的店铺。
    walkway('R-LIVING',[[209,66,1723],[209,66,1710],[215,66,1710],[218,68,1710],[221,68,1710]],2)
    walkway('R-CARGO',[[231,68,1714],[231,68,1709],[227,68,1709],[227,68,1706]],3,'pack-and-hand-cargo')
    walkway('R-B3-HOME',[[209,66,1711],[200,66,1711],[200,66,1714]],2)
    walkway('R-B2-FOOD',[[209,66,1710],[208,66,1709],[208,66,1706]],2)
    walkway('R-B4-REPAIR',[[200,66,1711],[195,65,1711],[195,65,1707]],2)
    walkway('R-B5-SERVICE',[[219,68,1710],[218,68,1716],[221,68,1716]],2)
    walkway('R-B1-RESIDENT',[[219,68,1710],[219,68,1702],[223.5,68,1702]],2)
    # 门前面和路线按拟定步行标高修正；坡段具体台阶以 profiles 保存，未写世界。
    for rt in ROUTES:
        for xx,fy,zz in rt['samples']:
            for x,z in rect(math.floor(xx-rt['width']/2),math.floor(zz-rt['width']/2),math.ceil(xx+rt['width']/2)-1,math.ceil(zz+rt['width']/2)-1):
                if (x,z) in ENVELOPE-occupied:box((x,min(SURF[x,z]['ground_y'],fy-.5),z),(x+1,fy,z+1),'paving','SPACE','route-design-surface')
    # 烟道预留穿越楼板/屋面时扣去重叠实体，不能把木楼板直接穿进烟道。
    cutter=([211,67,1699],[212,84,1700]);fixed=[]
    for v in BOXES:
        if v['owner']!='B2' or v['role']=='flue-reservation':fixed.append(v);continue
        lo=[max(v['a'][i],cutter[0][i]) for i in range(3)];hi=[min(v['b'][i],cutter[1][i]) for i in range(3)]
        if any(lo[i]>=hi[i] for i in range(3)):fixed.append(v);continue
        a=v['a'];b=v['b']
        for A,B in [(a,[lo[0],b[1],b[2]]),([hi[0],a[1],a[2]],b),
                    ([lo[0],a[1],a[2]],[hi[0],b[1],lo[2]]),([lo[0],a[1],hi[2]],[hi[0],b[1],b[2]]),
                    ([lo[0],a[1],lo[2]],[hi[0],lo[1],hi[2]]),([lo[0],hi[1],lo[2]],[hi[0],b[1],hi[2]])]:
            if all(B[i]>A[i] for i in range(3)):fixed.append({**v,'a':A,'b':B})
    BOXES[:]=fixed
    write(OUT/'circulation.json',{'routes':ROUTES,'stairs':STAIRS,'portals':OPENINGS,
        'main_approach':'R1a Commons -> G1 -> R1b N1 remains outside design; branches at south/east edges; no gateway over the route',
        'external_route_status':'RESERVATION NOT CLEARED ROAD; trunk [233,1729] remains a pre-build issue',
        'loading_bay':{'bounds':[228,1708,233,1711],'role':'two pack animals or hand-load stop; not cart certification'},
        'shared_court':{'bounds':[201,1709,216,1712],'role':'eating, household chores, water carrying, passing; movement lane stays clear'},
        'growth_interfaces':[[189,1711],[216,1723]],'water_service':{'clean_storage':[211,1712],'fire_storage':[224,1709],'dry_waste_collection':[190,1717],'source':'UNCONFIRMED'},
        'actual_minecraft_collision':'UNVERIFIED; design proxy only'})
    write(OUT/'phasing.json',{'status':'PROPOSED_NO_WRITE_AUTHORITY','phases':[
        {'id':0,'work':'water-source confirmation, new live-save read-only check, bounded footprint/vegetation/ground route compilation','stop':'no occupancy or writes on this packet'},
        {'id':1,'buildings':['B1','B3'],'work':'separate high short-store + lower shop-home, shared approach and water/fire service before occupation'},
        {'id':2,'buildings':['B2','B4'],'work':'need-driven inn and cold-repair infill, keep cross-court connection'},
        {'id':3,'buildings':['B5'],'work':'low service end-piece; remaining gaps remain open, not automatic infill'}]})
    write(OUT/'URBAN-ENSEMBLE.json',{'schema':'civ-urban-ensemble/0.1','status':'DESIGN_PREVIEW / AWAITING INDEPENDENT REVIEW','world_writes':0,
        'envelope':'site-envelope.json','gross_area':len(ENVELOPE),'footprint_area':sum(b['footprint_area'] for b in BUILDINGS),
        'coverage':sum(b['footprint_area'] for b in BUILDINGS)/len(ENVELOPE),'gross_floor_area':sum(b['footprint_area']*len(b['floors']) for b in BUILDINGS),
        'buildings':BUILDINGS,'model_contract':'design-model.json.gz: colored half-open solid boxes, not executable blockstates; Minecraft collision not certified',
        'sections':[{'id':'A-A','axis':'x','fixed_z':1703},{'id':'B-B','axis':'z','fixed_x':207}],
        'interpretive_growth':'The short-store and shop support immediate exchange; inn/repair grow around their shared court; low public room completes the slope end. This is design causality, not authored history Canon.'})
    with open(OUT/'design-model.json.gz','wb') as f:
        f.write(gzip.compress(json.dumps({'schema':'civ-design-solids/1','boxes':BOXES,'colors':COLORS},ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
    write(OUT/'building-roles.json',{'coordinate_contract':'bounds=[xmin,zmin,xmax,zmax] inclusive; floors=finished walking surface Y','buildings':BUILDINGS})

def verify():
    def hit(p,radius=.3):
        x,y,z=p
        return [v for v in BOXES if v['role'] not in ['ground-surface','route-design-surface'] and
                v['a'][0]<x+radius and v['b'][0]>x-radius and v['a'][2]<z+radius and v['b'][2]>z-radius and
                v['a'][1]<y+1.9 and v['b'][1]>y+.001]
    checks=[]
    for st in STAIRS:
        failures=[]
        for i,p in enumerate(st['samples']):
            # 玩家站在每一级顶面；避免把下一阶的 riser 当成同高度水平墙。
            hits=[v for v in hit(p,.2) if v['role']!='stair']
            if hits:failures.append({'sample':i,'point':p,'roles':sorted(set(v['role'] for v in hits))})
        checks.append({'id':st['id'],'sampled_treads_landings':len(st['samples']),'failures':failures})
    route_checks=[]
    for rt in ROUTES:
        failures=[]
        for i,p in enumerate(rt['samples']):
            hits=hit(p)
            if hits:failures.append({'sample':i,'point':p,'roles':sorted(set(v['role'] for v in hits))})
        route_checks.append({'id':rt['id'],'samples':len(rt['samples']),'failures':failures})
    # 逐体量投影包含屋檐，不用 footprint 独自证明未越界。
    illegal=[]
    for v in BOXES:
        proj=rect(math.floor(v['a'][0]),math.floor(v['a'][2]),math.ceil(v['b'][0])-1,math.ceil(v['b'][2])-1)
        if not proj<=ENVELOPE:illegal.append(v)
    write(OUT/'validation/design-qa.json',{'envelope_within_G1':ENVELOPE<=G1,'clearance_overlap':len(ENVELOPE&CLEAR),
        'all_design_projection_outside_columns':len(illegal),'stairs':checks,'routes':route_checks,
        'limitations':['checks use simplified solids, not Minecraft blockstate collisions','route centerline radius0.3; full pack-animal envelope not certified','no in-game walk-through / lighting / fluid updates'],
        'world_writes':0})
    assert not illegal
    print('envelope',len(ENVELOPE),'buildings',[(b['id'],b['ground_y_range'],b['footprint_area']) for b in BUILDINGS])
    print('stair failures',[(x['id'],len(x['failures'])) for x in checks]);print('route failures',[(x['id'],len(x['failures'])) for x in route_checks])

if __name__=='__main__':
    observe();model();verify()
