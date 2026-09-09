import json,sqlite3
from collections import Counter,defaultdict
import numpy as np
from L0_公理层.图册契约 import SCHEMA,ALGORITHM,BASE
from L1_器件层.图册存储器 import open_store,encode,mask_runs,geometry_summary,IdentityRegistry
from L1_器件层.源快照保护器 import write_json,digest

def build(out):
    """从已冻结候选、人工语义决策和NG-2成员索引汇编独立Atlas；不访问Minecraft。"""
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    fresh=read(out/'manifest/freshness.json')
    if fresh['geography_snapshot_status']!='CURRENT_MATCH':raise ValueError('freshness gate未通过')
    candidates=read(out/'atlas/numeric-candidates.json');decisions=read(out/'atlas/semantic-decisions.json');cal=read(out/'calibration/detector-rules.json')
    a=np.load(out/'raw-or-queryable/numeric-segmentation.npz');gx0,gz0=map(int,a['origin']);clip=[-6224,-6544,3807,3487]
    src=sqlite3.connect((out/'raw-or-queryable/input-cache/v1.sqlite').as_uri()+'?mode=ro',uri=True);src.row_factory=sqlite3.Row
    rows=[dict(r) for r in src.execute('SELECT * FROM cells ORDER BY gz,gx')];cells={(r['gx'],r['gz']):r for r in rows}
    ng2=out.parent/'NG-2';local={s:read(ng2/'assessments'/f'{s}.json') for s in ('SITE-002','SITE-005','SITE-015','SITE-014','SITE-017','SITE-019','SITE-003','SITE-011')}
    tmp=out/'raw-or-queryable/atlas-building.sqlite'
    if tmp.exists():raise ValueError('存在未完成汇编文件，不能覆盖')
    db=open_store(tmp);registry=IdentityRegistry(out/'atlas/id-registry.json');objects={};geometry={};cell_objects={};members=defaultdict(set)
    meta={'schema_version':SCHEMA,'algorithm':ALGORITHM,'execution_base':BASE,'status':'PROPOSED','geography_snapshot_status':'CURRENT_MATCH','freshness_checked_at':fresh['checked_at'],'world_coverage_bounds':clip,'coordinate_grid_bounds':[gx0*64,gz0*64,(gx0+a['height'].shape[1])*64-1,(gz0+a['height'].shape[0])*64-1],'world_writes':0,'targeted_refinement_count':0,'global_warnings':cal['global_warnings'],'known_unresolved_cells':{'land':int((a['land_units']==-1).sum()),'water':int((a['water_units']==-1).sum())},'relation_types':['adjacent_to','contains','part_of','connected_to','associated_with','overlaps'],'connected_to_policy':'No global real-water connection asserted from 64-block adjacency; connected_to may remain empty.'}
    for k,v in meta.items():db.execute('INSERT INTO meta VALUES (?,?)',(k,encode(v)))
    for rule in cal['rules']:db.execute('INSERT INTO calibration VALUES (?,?)',(rule['id'],encode(rule)))
    for r in rows:
        z,x=r['gz']-gz0,r['gx']-gx0
        db.execute('INSERT INTO cell_index VALUES (?,?,?,?,?,?,?,?,?,?)',(r['gx'],r['gz'],r['x'],r['z'],r['elevation'],r['water'],r['terrain'],r['geo_id'],int(a['land_units'][z,x]==-1),int(a['water_units'][z,x]==-1)))
    def lineage(id,kind,source,ref,role='evidence_only'):
        db.execute('INSERT OR IGNORE INTO lineage VALUES (?,?,?,?,?)',(id,kind,source,ref,role))
    def add(id,key,type,label,status,summary,runs,rep,semantics,boundary,topology,semantic,requires=True,geometry_id=None,extras=None):
        geometry_id=geometry_id or id
        if geometry_id not in geometry:
            geometry[geometry_id]=runs;db.executemany('INSERT INTO geometry_runs VALUES (?,?,?,?,?)',[(geometry_id,*r) for r in runs])
        registry.bind(id,key,runs)
        obj={'id':id,'family':id.split('-')[0],'type':type,'status':'PROPOSED','evidence_status':status,'machine_label':label,'summary':summary,'representative':{'x':int(rep[0]),'z':int(rep[1])},'geometry':dict(geometry_summary(runs),id=geometry_id,semantics=semantics),'confidence_semantics':'Qualitative evidence status at declared scale, not a probability or global detector accuracy','calibration_refs':[r['id'] for r in cal['rules']],'flow_direction':'unknown' if id.startswith('NHYD') else None,'uncertainty':{'boundary':boundary,'topology':topology,'semantic':semantic,'requires_refinement':requires}}
        if extras:obj.update(extras)
        objects[id]=obj
        db.execute('INSERT INTO atlas_objects VALUES (?,?,?,?,?,?,?,?)',(id,obj['family'],type,'PROPOSED',status,label,geometry_id,encode(obj)))
        db.execute('INSERT INTO uncertainty VALUES (?,?,?,?,?)',(id,boundary,topology,semantic,int(requires)))
        lineage(id,'algorithm',ALGORITHM,'tooling/L2_流程层/图册汇编流程.py','derived_by')
        # 索引只加速回溯；落点仍使用实际runs，不能用涉及cell就声称整格覆盖。
        for z0,z1,x0,x1 in runs:
            for gz in range(z0//64,z1//64+1):
                for gx in range(x0//64,x1//64+1):members[id].add((gx,gz))
        return obj
    def coarse_lineage(id,points):
        for gid in sorted({cells[p]['geo_id'] for p in points if p in cells and cells[p]['geo_id']}):lineage(id,'V1',gid,'../V1/survey/atlas/GEO.jsonl#'+gid)
        lineage(id,'V1_cells',id,'atlas_members WHERE object_id='+id,'member_index_to_V1_cells')
    def local_lineage(id,site):
        l=local[site];lineage(id,'NG-2',site,f'../NG-2/assessments/{site}.json','accepted_local_evidence');lineage(id,'V1',site,'../V1/survey/sites/SITE.jsonl#'+site)
        source=l['v1_source_object'];lineage(id,'V1',source,f'../V1/survey/atlas/{source.split("-")[0]}.jsonl#'+source)
    def water_runs(site):
        l=local[site];ar=np.load(ng2/'raw-or-queryable'/f'{site}-topology1.npz');label=l['water_topology']['primary_water']['component'];b=l['roi_bounds']
        return mask_runs(ar['water_labels']==label,(b[0],b[1]),1)
    island=local['SITE-003'];ia=np.load(ng2/'raw-or-queryable/SITE-003-topology1.npz');ib=island['roi_bounds'];island_runs=mask_runs(ia['land_labels']==island['water_topology']['primary_land']['component'],(ib[0],ib[1]),1)
    region_decisions={f'NGEO-C{r[0]:03d}':r for r in decisions['regions']}
    for c in candidates:
        family=c['candidate'].split('-')[0];number=int(c['candidate'][-3:]);id=f'{family}-{number:03d}'
        units=a['land_units' if family=='NGEO' else 'water_units'];mask=units==c['numeric_component'];zz,xx=np.where(mask);points={(int(x+gx0),int(z+gz0)) for z,x in zip(zz,xx)}
        runs=mask_runs(mask,(gx0*64,gz0*64),64,clip)
        for p in points:cell_objects[p]=id
        if family=='NGEO':
            _,label,type,status,summary=region_decisions[c['candidate']]
            if number==9:runs=island_runs
            obj=add(id,'region:'+c['candidate'],type,label,status,summary,runs,c['representative'],'actual_NG2_surface_land_columns' if number==9 else '64-block regional cell approximation clipped to surveyed full-world extent','1-block outer island outline' if number==9 else '64-block proxy + 320-block smoothing; not an exact terrain boundary; edge censored='+str(c['edge_censored']),'verified outer water ring only' if number==9 else 'coarse four-neighbor land continuity; narrow water breaks may be missed','current surface; anthropogenic origin uncertain; local calibration does not validate all members',number!=9,extras={'numeric_candidate':c['candidate'],'regional_metrics':{k:c[k] for k in ('cells','mean_elevation','min_elevation','max_elevation','mean_slope','mean_relief','top_biomes','edge_censored')},'boundary_evidence_status':'SUPPORTED' if number==9 else 'PROVISIONAL'})
            if number==9:local_lineage(id,'SITE-003')
        else:
            if number==15:
                runs=water_runs('SITE-019');l=local['SITE-019']
                obj=add(id,'water:NG2:SITE-019',l['refined_type'],'verified_branching_channel_reach','SUPPORTED','NG-2实测的开放分支水道与展宽段，替代V1封闭内陆水体解释。',runs,[1096,-1208],'actual_NG2_primary_water_component_columns','exact within ROI; north/south extent censored','four-neighbor real overlapping water intervals within ROI; continuation outside unknown','not a closed lake; no direction or drainage basin inferred',extras={'closure':'OPEN_AT_ROI','source_roi':l['roi_bounds']});local_lineage(id,'SITE-019')
            else:
                label='coarse_major_open_water_domain' if number==1 else f'coarse_water_patch_{number:03d}'
                obj=add(id,'water:'+c['candidate'],'coarse_surface_water_domain',label,'PROVISIONAL','真实水样本形成的64格候选水域；既不确认封闭湖体，也不保证全分量实际连通。',runs,c['representative'],'64-block sampled water>=0.6 cell approximation','shoreline uncertain at subcell scale; edge censored='+str(c['edge_censored']),'UNRESOLVED real connectivity, ice and narrow channels; sampled graph only','water biome context does not prove ocean/lake/river classification',extras={'closure':'unknown','numeric_candidate':c['candidate']})
            for p in sorted(points):
                for row in src.execute('SELECT m.id FROM members m JOIN objects o USING(id) WHERE m.gx=? AND m.gz=? AND o.family=?',(p[0],p[1],'HYD')):lineage(id,'V1',row[0],'../V1/survey/atlas/HYD.jsonl#'+row[0],'coarse_water_evidence_not_promoted')
        coarse_lineage(id,points)
    for id,site,label in [('NHYD-019','SITE-003','verified_island_surrounding_water'),('NHYD-020','SITE-011','verified_coastal_water_connection_context')]:
        l=local[site];runs=water_runs(site)
        # 水域代表点选真实run内点；SITE-003的SITE点在岛上，不能当作水域代表点。
        z0,z1,x0,x1=runs[len(runs)//2];rep=[(x0+x1)//2,z0]
        add(id,'water:NG2:'+site,'verified_surface_water_component',label,'SUPPORTED','NG-2 ROI内真实连通水面背景；不是整片海域或唯一海湾边界。',runs,rep,'actual_NG2_primary_water_component_columns','exact local columns; whole-waterbody boundary remains ROI-censored','real water intervals verified within ROI; global relation unresolved','no natural harbor, navigation or flow-direction inference',extras={'source_roi':l['roi_bounds'],'closure':'OPEN_AT_ROI'});local_lineage(id,site)
    feature_specs=[('NFEAT-001','SITE-002',[-5688,-1611]),('NFEAT-002','SITE-014',[-4792,-952]),('NFEAT-003','SITE-003',[-248,2056]),('NFEAT-004','SITE-011',[-312,-4024])]
    for id,site,rep in feature_specs:
        l=local[site];geom_id=None
        if site=='SITE-003':runs=island_runs;geom_id='NGEO-009';semantics='actual island land-column mask shared with NGEO-009'
        elif site=='SITE-014':
            ar=np.load(ng2/'raw-or-queryable/SITE-014-grid8.npz');b=l['roi_bounds'];runs=mask_runs(ar['low_slope_land'],(b[0],b[1]),8);semantics='NG2 8-block sampled low-slope tableland mask; not exact plateau boundary'
        else:runs=[(rep[1],rep[1],rep[0],rep[0])];semantics='observation anchor only; no feature-footprint containment claim'
        add(id,'feature:NG2:'+site,l['refined_type'],'local_'+l['refined_type'],'SUPPORTED',l['observed_evidence'][0],runs,rep,semantics,'see source footprint limitations; point means undefined areal boundary','local evidence only; no regional passage/harbor implication','; '.join(l['limitations']),site!='SITE-003',geom_id,{'source_roi':l['roi_bounds'],'long_term_value':'Preserves a reviewed discrete morphology and its limits, instead of promoting all V1 FEAT candidates.','requires_local_observation':True});local_lineage(id,site)
    for number,(site,l) in enumerate(local.items(),1):
        p=l['provenance']['representative_sample'];rep=[p['x'],p['z']];id=f'NSITE-{number:03d}'
        add(id,'site:NG2:'+site,l['refined_type'],'observation_'+site.lower().replace('-','_'),'SUPPORTED','已接受局部地形证据的再次观察入口；不指定建设用途。',[(rep[1],rep[1],rep[0],rep[0])],rep,'observation point only','no suitability footprint established','follow related local/global evidence limitations','; '.join(l['limitations']),True,extras={'planning_potential':'terrain_observation_only','requires_local_observation':True,'requires_world_write_authorization':True,'anthropogenic_contamination':'possible','source_verdict':l['verdict']});local_lineage(id,site)
    def relate(s,t,kind,status,evidence):
        if s!=t:db.execute('INSERT OR REPLACE INTO relations VALUES (?,?,?,?,?)',(s,t,kind,status,encode(evidence)))
    edges=Counter()
    for (gx,gz),id in cell_objects.items():
        for p in ((gx+1,gz),(gx,gz+1)):
            other=cell_objects.get(p)
            if other and other!=id:edges[tuple(sorted((id,other)))]+=1
    for (s,t),n in sorted(edges.items()):
        # NHYD-015已被实际成员替换；旧64格边不能再冒充新对象边界。
        if 'NHYD-015' in (s,t) or 'NGEO-009' in (s,t):kind='associated_with'
        else:kind='adjacent_to'
        for x,y in ((s,t),(t,s)):relate(x,y,kind,'PROVISIONAL',{'method':'V1 coarse-cell shared-edge context','shared_cell_edges':n,'not_real_water_connectivity':True})
    for id,obj in objects.items():
        if obj['family'] not in ('NFEAT','NSITE'):continue
        p=obj['representative'];near=cell_objects.get((p['x']//64,p['z']//64))
        if near:relate(id,near,'associated_with','PROVISIONAL',{'method':'anchor located in coarse regional context'})
        for water in ('NHYD-015','NHYD-019','NHYD-020'):
            runs=geometry[objects[water]['geometry']['id']]
            if any(x0<=p['x']<=x1 and z0<=p['z']<=z1 for z0,z1,x0,x1 in runs):
                relate(id,water,'part_of','SUPPORTED',{'method':'observation point is in actual NG2 water component, not whole feature containment'})
        refs=[r[0] for r in db.execute('SELECT source_id FROM lineage WHERE object_id=? AND source_kind=?',(id,'NG-2'))]
        if near:
            for site in refs:lineage(near,'NG-2',site,f'../NG-2/assessments/{site}.json','local_calibration_not_whole_region_validation')
    relate('NGEO-009','NFEAT-003','contains','SUPPORTED',{'method':'identical actual land geometry'});relate('NFEAT-003','NGEO-009','part_of','SUPPORTED',{'method':'identical actual land geometry'})
    for s,t in [('NGEO-009','NHYD-019'),('NHYD-019','NGEO-009')]:relate(s,t,'adjacent_to','SUPPORTED',{'method':'NG2 SITE-003 verified single outer water ring; inner ponds excluded'})
    for id in ('NHYD-015','NHYD-019','NHYD-020'):
        for other in sorted({cell_objects[p] for p in members[id] if p in cell_objects and cell_objects[p].startswith('NHYD') and cell_objects[p]!=id}):
            relate(id,other,'overlaps','PROVISIONAL',{'method':'local geometry shares coarse water cells; does not prove entire coarse domain connected'})
    for id,points in sorted(members.items()):db.executemany('INSERT INTO atlas_members VALUES (?,?,?,?)',[(id,gx,gz,'geometry_intersects_cell; use runs for point membership') for gx,gz in sorted(points)])
    registry.finish(db)
    # 每个对象至少一条历史证据；算法引用不能独自充当lineage。
    for id in objects:
        if not db.execute('SELECT 1 FROM lineage WHERE object_id=? AND source_kind IN (?,?)',(id,'V1','NG-2')).fetchone():raise ValueError('缺少历史证据: '+id)
    db.commit();integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
    if integrity!='ok':raise ValueError(integrity)
    exports=[]
    for id in sorted(objects):
        obj=objects[id];obj['lineage']=[dict(zip(('source_kind','source_id','ref','role'),r)) for r in db.execute('SELECT source_kind,source_id,ref,role FROM lineage WHERE object_id=? ORDER BY source_kind,source_id',(id,))];exports.append(obj)
    (out/'atlas/objects.jsonl').write_text(''.join(encode(o)+'\n' for o in exports),encoding='utf-8',newline='\n')
    (out/'atlas/relations.jsonl').write_text(''.join(encode(dict(zip(('source','target','kind','evidence_status','evidence'),r)))+'\n' for r in db.execute('SELECT * FROM relations ORDER BY source,target,kind')),encoding='utf-8',newline='\n')
    counts=dict(Counter(o['family'] for o in objects.values()));statuses=dict(Counter(o['evidence_status'] for o in objects.values()))
    report={'schema_version':SCHEMA,'execution_base':BASE,'counts':counts,'evidence_status_counts':statuses,'uncertainty_objects':sum(o['uncertainty']['requires_refinement'] for o in objects.values()),'unresolved_cells':meta['known_unresolved_cells'],'targeted_refinement':decisions['targeted_refinement'],'source_cache_not_published':True,'raw_ng2_columns_copied':0,'geometry_runs':db.execute('SELECT count(*) FROM geometry_runs').fetchone()[0],'integrity_check':integrity}
    db.close();src.close();tmp.replace(out/'raw-or-queryable/atlas.sqlite')
    write_json(out/'manifest/atlas.json',report);write_json(out/'manifest/store.json',{'path':'raw-or-queryable/atlas.sqlite','sha256':digest(out/'raw-or-queryable/atlas.sqlite'),'size':(out/'raw-or-queryable/atlas.sqlite').stat().st_size,'compression':'none; directly queryable, no archive round-trip required'})
    write_json(out/'targeted-refinement/decision.json',decisions['targeted_refinement']);print(json.dumps(report))
