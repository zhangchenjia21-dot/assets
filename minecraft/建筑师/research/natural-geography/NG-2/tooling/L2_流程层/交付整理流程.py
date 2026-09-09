"""汇编人工解释与可追溯事实、校验引用；不从阈值自动决定地貌verdict。"""
import json,hashlib
from collections import Counter
from datetime import datetime,timezone
import numpy as np
from L1_器件层.区块柱读取器 import connect
from L1_器件层.源文件保护器 import write_json

def finalize(out):
    db=connect(out/'raw-or-queryable/refinement.sqlite')
    authored=json.loads((out/'assessments/interpretations.json').read_text(encoding='utf-8'))
    targets={id:json.loads(raw) for id,raw in db.execute('SELECT id,json FROM targets')}
    required={'target_id','v1_type','v1_source_object','roi_bounds','sampling_method','resolution_levels','observed_evidence','refined_metrics','water_topology','anthropogenic_contamination','verdict','refined_type','confidence','limitations','provenance'}
    checks=[];summary=[]
    for id,t in targets.items():
        m=json.loads((out/'assessments'/f'{id}-metrics.json').read_text(encoding='utf-8'));v=t['v1'];cfg=t['config'];p=v['representative'];b=cfg['bounds']
        a=dict(authored[id]);a.update({'target_id':id,'v1_type':v['type'],'v1_source_object':v['source_object'],'roi_bounds':b,'sampling_method':{'initial':'8-block actual grid','adaptive':'4-block entire chunks around slope>=0.25, water transition, or target radius96','critical':'full 1-block water ROI' if cfg.get('topology') else '1-block saddle core and profiles' if cfg.get('fine1_bounds') else '1-block profiles','stored_columns':m['samples'],'first_insert_stage_counts':m['stage_new_sample_counts'],'roi_reason':cfg['reason']},'resolution_levels':[8,4,1]})
        a['refined_metrics']={'source':f'assessments/{id}-metrics.json','sha256':hashlib.sha256((out/'assessments'/f'{id}-metrics.json').read_bytes()).hexdigest(),'observed_extrema_xyz':m['observed_extrema'],'grid8_elevation':m['grid8_elevation'],'grid8_slope_rise_run':m['grid8_slope_rise_run'],'low_slope_land':m['low_slope_land'],'target_elevation_band':m['target_elevation_band'],'high_terrain_200':m['high_terrain_200'],'profiles':m['profiles']}
        a['water_topology']=m['water_topology']
        a['anthropogenic_contamination']='possible'
        entities=m['material_context']['near_surface_or_waystone_entities']
        a['anthropogenic_evidence']={'candidate_material_columns':m['artificial_material_samples'],'near_surface_or_waystone_entity_counts':dict(Counter(e['id'] for e in entities)),'details':f'assessments/{id}-metrics.json#/material_context','interpretation':'Observed Waystones and candidate materials have unresolved generated/player origin. No evidence here establishes landscape-scale grading; local interventions cannot be excluded. Retain all surfaces and lower origin confidence rather than infer pristine terrain.','material_origin_context':'validation/worldgen-material-context.json','limitations':'Material checks cover requested surface columns; entity inventory covers decoded chunks. Natural-material edits and unobserved small structures can be missed.'}
        regions=[r[0] for r in db.execute('SELECT DISTINCT c.region FROM chunks c JOIN (SELECT DISTINCT (x >> 4) cx,(z >> 4) cz FROM target_samples WHERE target=?) t USING(cx,cz) ORDER BY c.region',(id,))]
        chunk_count=db.execute('SELECT count(*) FROM (SELECT DISTINCT (x >> 4),(z >> 4) FROM target_samples WHERE target=?)',(id,)).fetchone()[0]
        sample=db.execute('SELECT s.* FROM samples s JOIN target_samples t USING(x,z) WHERE t.target=? AND x=? AND z=?',(id,p['x'],p['z'])).fetchone()
        a['provenance']={'base_commit':'4b9b1f7e600708ff67e1ef2f844a9d3de0ba2242','world_snapshot':'manifest/world-before.json','v1_snapshot':'manifest/v1-before.json','v1_site_record':'../V1/survey/sites/SITE.jsonl#'+id,'queryable_store':'raw-or-queryable/refinement.sqlite (restore archive first)','sample_trace':'target_samples(target,x,z) -> samples(x,z) -> chunks(x>>4,z>>4) -> region path -> world-before SHA256','decoded_chunks':chunk_count,'regions':regions,'representative_sample':dict(zip(['x','z','surface_y','exposed_y','ocean_floor_y','water_y','water_bottom','surface_state','exposed_state','water_state','biome','ice_covered','artificial_material'],sample)),'interpretation_authority':'human-readable model assessment; not a threshold-generated verdict, not World Canon','in_game_visual_review':'BLOCKED_BY_SAFE_ENVIRONMENT'}
        if id=='SITE-002':
            c=m['critical_depression_test'];a['refined_metrics']['saddle']={k:c[k] for k in ('bounds','resolution','target_height','edge_escape_minimax','low_components')}
            a['refined_metrics']['saddle']['terrain_step_crossings']={name:{k:v for k,v in route.items() if k!='path'} for name,route in c['terrain_step_crossings'].items()}
            points=[]
            for dx,dz in [(-64,0),(64,0),(0,-64),(0,64)]:
                x,z=p['x']+dx,p['z']+dz;y=db.execute('SELECT exposed_y FROM samples WHERE x=? AND z=?',(x,z)).fetchone()[0];points.append([x,y,z])
            a['refined_metrics']['saddle']['orthogonal_64_block_samples_xyz']=points
            route=c['terrain_step_crossings']['east-west']['path'];entity_coords={(e['x'],e['z']) for e in entities}
            a['refined_metrics']['saddle']['route_intersects_observed_near_surface_entities']=[q for q in route if (q['x'],q['z']) in entity_coords]
        if id=='SITE-005':
            grid=np.load(out/'raw-or-queryable'/f'{id}-grid8.npz');sections=[]
            for z in [-5760,-5496,-5248]:
                y=grid['height'][(z-b[1])//8];mask=(y>=65)&(y<=130)&(grid['water_top'][(z-b[1])//8]==-32768);ix=(p['x']-b[0])//8;left=right=ix
                while left>0 and mask[left-1]:left-=1
                while right+1<len(mask) and mask[right+1]:right+=1
                sections.append({'z':z,'x_bounds':[b[0]+left*8,b[0]+right*8+7],'sampled_band_width_blocks':(right-left+1)*8,'target_column_qualifies':bool(mask[ix])})
            a['refined_metrics']['apron_sections']={'method':'8-block contiguous dry height65..130 band containing target X; this is NOT valley floor width','sections':sections,'valley_floor_width':None,'reason':'opposed valley walls not established'}
        if id=='SITE-011':
            t1=np.load(out/'raw-or-queryable/SITE-011-topology1.npz');label=m['water_topology']['primary_water']['component'];anchor=[64,-4200]
            anchor_label=int(t1['water_labels'][anchor[1]-b[1],anchor[0]-b[0]])
            if anchor_label!=label:raise ValueError('海域验证锚点与目标水体不连通')
            rect=[0,-4464,176,-4145];mask=t1['water_labels'][rect[1]-b[1]:rect[3]-b[1]+1,rect[0]-b[0]:rect[2]-b[0]+1]==label
            a['refined_metrics']['opening_evidence']={'open_water_anchor_xz':anchor,'same_real_water_component':True,'open_water_test_rectangle':rect,'fraction_in_target_water_component':float(mask.mean()),'sections':m['water_sections'],'direction_interpretation':'broad southwest opening and narrower northeast connection; not a unique mathematically fixed mouth'}
        if id=='SITE-019':a['refined_metrics']['water_sections']=m['water_sections']
        assert required<=set(a) and a['verdict'] in {'CONFIRMED','RECLASSIFIED','REJECTED','INSUFFICIENT'}
        assert a['anthropogenic_contamination'] in {'none','possible','likely','confirmed'}
        write_json(out/'assessments'/f'{id}.json',a)
        db.execute('INSERT OR REPLACE INTO assessments VALUES (?,?)',(id,json.dumps(a,ensure_ascii=False)))
        arrays=np.load(out/'raw-or-queryable'/f'{id}-grid8.npz')
        assert arrays['height'].shape==((b[3]-b[1])//8+1,(b[2]-b[0])//8+1)
        assert int(arrays['height'][(p['z']-b[1])//8,(p['x']-b[0])//8])==sample[3]
        if cfg.get('topology'):assert m['samples']==(b[2]-b[0]+1)*(b[3]-b[1]+1)
        checks.append({'target':id,'required_fields':True,'source_sample_present':True,'bounds_and_orientation_array_check':True,'topology_complete':True if cfg.get('topology') else 'not a full-topology target','profiles':len(m['profiles'])})
        summary.append({'target':id,'source':v['source_object'],'verdict':a['verdict'],'refined_type':a['refined_type'],'columns':m['samples']})
    db.commit()
    integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
    dangling=db.execute('SELECT count(*) FROM target_samples t LEFT JOIN samples s USING(x,z) WHERE s.x IS NULL').fetchone()[0]
    orphan=db.execute('SELECT count(*) FROM samples s LEFT JOIN chunks c ON c.cx=(s.x >> 4) AND c.cz=(s.z >> 4) WHERE c.cx IS NULL').fetchone()[0]
    dictionary_missing=db.execute('SELECT count(*) FROM samples s LEFT JOIN states a ON s.surface_state=a.id LEFT JOIN states e ON s.exposed_state=e.id LEFT JOIN states w ON s.water_state=w.id LEFT JOIN biomes b ON s.biome=b.id WHERE a.id IS NULL OR e.id IS NULL OR w.id IS NULL OR b.id IS NULL').fetchone()[0]
    assert integrity=='ok' and dangling==orphan==dictionary_missing==0
    write_json(out/'validation/delivery-checks.json',{'integrity_check':integrity,'dangling_target_samples':dangling,'missing_chunk_provenance':orphan,'missing_material_or_biome_dictionary':dictionary_missing,'assessment_count':len(checks),'target_checks':checks,'samples':db.execute('SELECT count(*) FROM samples').fetchone()[0],'target_samples':db.execute('SELECT count(*) FROM target_samples').fetchone()[0],'chunks':db.execute('SELECT count(*) FROM chunks').fetchone()[0]})
    manifest=json.loads((out/'manifest/survey.json').read_text(encoding='utf-8'));manifest.update({'status':'implementation completed / awaiting independent review','targets':{id:t['config'] for id,t in targets.items()},'delivery_timestamp':datetime.now(timezone.utc).isoformat(),'assessment_summary':summary});write_json(out/'manifest/survey.json',manifest)
    db.close();print(json.dumps(summary,ensure_ascii=True))
