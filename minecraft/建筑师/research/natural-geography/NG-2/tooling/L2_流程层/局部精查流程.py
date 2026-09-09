import gzip
import hashlib
import json
import math
import random
import shutil
import sys
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import nbtlib
from L0_公理层.精查契约 import SCHEMA,BASE_COMMIT,TARGETS,AIR,WATER,ICE,vegetation
from L1_器件层.源文件保护器 import ReadGuard,fingerprint,write_json
from L1_器件层.区块柱读取器 import Reader,connect
from L1_器件层.局部指标计算器 import grid,metrics,topology,depression_test
from L1_器件层.局部图生成器 import render,detail_views

def targets_at(v1):
    return {o['id']:o for o in map(json.loads,(v1/'survey/sites/SITE.jsonl').read_text(encoding='utf-8').splitlines()) if o['id'] in TARGETS}

def persist(reader,db,target,cx,cz,indices,stage):
    rows=reader.read(cx,cz)[indices].tolist()
    db.executemany('INSERT OR IGNORE INTO samples VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',rows)
    db.executemany('INSERT OR IGNORE INTO target_samples VALUES (?,?,?,?)',[(target,r[0],r[1],stage) for r in rows])

def rectangle(reader,db,target,bounds,step,stage,commit=True):
    x0,z0,x1,z1=bounds;count=0
    for cz in range(z0//16,z1//16+1):
        for cx in range(x0//16,x1//16+1):
            xs=[x for x in range(max(x0,cx*16),min(x1,cx*16+15)+1) if (x-x0)%step==0]
            zs=[z for z in range(max(z0,cz*16),min(z1,cz*16+15)+1) if (z-z0)%step==0]
            indices=[(z%16)*16+x%16 for z in zs for x in xs]
            if indices:persist(reader,db,target,cx,cz,indices,stage);count+=len(indices)
        if commit and cz%32==0:db.commit()
    if commit:db.commit()
    return count

def profiles(reader,db,target,bounds,point):
    x0,z0,x1,z1=bounds;px,pz=point['x'],point['z']
    lines={'east-west':[(x,pz) for x in range(x0,x1+1)],'north-south':[(px,z) for z in range(z0,z1+1)]}
    lines['northwest-southeast']=[(px+d,pz+d) for d in range(max(x0-px,z0-pz),min(x1-px,z1-pz)+1)]
    lines['southwest-northeast']=[(px+d,pz-d) for d in range(max(x0-px,pz-z1),min(x1-px,pz-z0)+1)]
    for name,coords in lines.items():
        grouped=defaultdict(list)
        for x,z in coords:grouped[(x//16,z//16)].append((z%16)*16+x%16)
        for (cx,cz),indices in grouped.items():persist(reader,db,target,cx,cz,indices,'profile1')
        start=coords[0]
        for x,z in coords:
            y,wy=db.execute('SELECT exposed_y,water_y FROM samples WHERE x=? AND z=?',(x,z)).fetchone()
            db.execute('INSERT OR REPLACE INTO profiles VALUES (?,?,?,?,?,?,?)',(target,name,x,z,math.hypot(x-start[0],z-start[1]),y,wy))
    db.commit()

def independent_checks(reader,db,target):
    """纯 Python 单索引解码并从最高 Y 竖向下探，独立于批量 numpy 读取路径。"""
    rows=db.execute('SELECT s.* FROM samples s JOIN target_samples t USING(x,z) WHERE target=?',(target,)).fetchall()
    rng=random.Random(int(target[-3:])+4903);chosen=rng.sample(rows,min(12,len(rows)))
    water=[r for r in rows if r[5]!=-32768];ice=[r for r in rows if r[11]]
    chosen+=rng.sample(water,min(4,len(water)))+rng.sample(ice,min(2,len(ice)))
    chosen+=sorted(rows,key=lambda r:r[3])[:3]+sorted(rows,key=lambda r:r[3])[-3:]
    result=[]
    def value(container,index,minimum):
        pal=container['palette']
        if len(pal)==1:return pal[0]
        bits=max(minimum,(len(pal)-1).bit_length());per=64//bits;word=int(container['data'][index//per])&((1<<64)-1)
        return pal[(word>>((index%per)*bits))&((1<<bits)-1)]
    for row in chosen:
        x,z,sy,gy,floor,wy,wb,top,support,ws,bid,covered,suspicious=row;d,path,sector=reader.raw(x//16,z//16);ss={int(s['Y']):s for s in d['sections']};lo=int(d['yPos'])*16
        def block(y):
            s=ss.get(y//16)
            if s is None or 'block_states' not in s:return {'Name':'minecraft:air'}
            return value(s['block_states'],(y%16)*256+(z%16)*16+x%16,4)
        yy=(max(ss)+1)*16-1
        while yy>=lo and str(block(yy)['Name']) in AIR:yy-=1
        filtered=yy
        while filtered>=lo and vegetation(str(block(filtered)['Name'])):filtered-=1
        probe=filtered
        while probe>=lo and str(block(probe)['Name']) in ICE:probe-=1
        observed_water=probe if str(block(probe)['Name']) in WATER else -32768
        b=value(ss[yy//16]['biomes'],((yy%16)//4)*16+((z%16)//4)*4+(x%16)//4,1)
        water_ok=True
        if wy!=-32768:
            water_ok=all(str(block(y)['Name']) in WATER for y in range(wb,wy+1)) and str(block(wb-1)['Name']) not in WATER
        ok=yy==sy and filtered==gy and observed_water==wy and str(b)==reader.biome_values[bid] and str(block(sy)['Name'])==reader.state_values[top]['Name'] and str(block(gy)['Name'])==reader.state_values[support]['Name'] and water_ok
        result.append({'target':target,'x':x,'z':z,'region':path.relative_to(reader.world).as_posix(),'chunk':[x//16,z//16],'surface_y':sy,'vertical_scan_y':yy,'filtered_y':filtered,'water_top_independent':observed_water,'biome':str(b),'water_interval':[wb,wy] if wy!=-32768 else None,'water_block_interval_valid':water_ok,'pass':ok})
    if not all(r['pass'] for r in result):raise ValueError('独立柱解码验证失败')
    return result

def scan(world,out,only=None):
    v1=out.parent/'V1';configs=json.loads(json.dumps(TARGETS));targets=targets_at(v1)
    plan=out/'manifest/roi-plan.json'
    if plan.exists():configs=json.loads(plan.read_text(encoding='utf-8'))
    write_json(plan,configs)
    with ReadGuard(world),ReadGuard(v1):
        print('source and V1 read guards acquired',flush=True)
        before=fingerprint(world);old=out/'manifest/world-before.json'
        if old.exists() and before!=json.loads(old.read_text(encoding='utf-8')):raise ValueError('世界与本任务首轮指纹不同，不得拼接调查')
        write_json(old,before);vbefore=fingerprint(v1);vold=out/'manifest/v1-before.json'
        if vold.exists() and vbefore!=json.loads(vold.read_text(encoding='utf-8')):raise ValueError('V1与本任务首轮指纹不同')
        write_json(vold,vbefore)
        level=nbtlib.load(world/'level.dat')['Data']
        if str(level['LevelName'])!='建筑师' or int(level['DataVersion'])!=4903:raise ValueError('世界绑定不符')
        db=connect(out/'raw-or-queryable/refinement.sqlite');reader=Reader(world,db)
        checks=[];stats={}
        for target,config in configs.items():
            if only and target not in only:continue
            b=config['bounds'];p=targets[target]['representative'];print(f'{target}: initial 8-block ROI {b}',flush=True)
            base_count=rectangle(reader,db,target,b,8,'context8')
            a=grid(db,target,b,8);h=a['height'].astype(float);wet=a['water_top']!=-32768;dz,dx=np.gradient(h,8)
            change=np.zeros(wet.shape,bool);change[1:]|=wet[1:]!=wet[:-1];change[:-1]|=wet[1:]!=wet[:-1];change[:,1:]|=wet[:,1:]!=wet[:,:-1];change[:,:-1]|=wet[:,1:]!=wet[:,:-1]
            critical=(np.hypot(dx,dz)>=0.25)|change
            zz,xx=np.indices(critical.shape);critical|=((xx*8+b[0]-p['x'])**2+(zz*8+b[1]-p['z'])**2<=96**2)
            patches=sorted({((b[0]+int(x)*8)//16,(b[1]+int(z)*8)//16) for z,x in zip(*np.where(critical))})
            for pi,(cx,cz) in enumerate(patches):
                rectangle(reader,db,target,[max(b[0],cx*16),max(b[1],cz*16),min(b[2],cx*16+15),min(b[3],cz*16+15)],4,'adaptive4',False)
                if pi%64==0:db.commit()
            db.commit()
            print(f'{target}: {len(patches)} slope/shore/target patches refined to 4 blocks',flush=True)
            if config.get('topology'):
                print(f'{target}: exact column topology underway',flush=True);rectangle(reader,db,target,b,1,'topology1')
            for fine in config.get('fine1_bounds',[]):
                rectangle(reader,db,target,fine,1,'critical1')
            profiles(reader,db,target,b,p)
            config['resolution_levels']=[8,4,1];config['adaptive_rule']='8-block slope>=0.25 OR observed water transition OR target radius96 -> entire intersected 16x16 chunk at4; water targets full ROI at1; four cross profiles at1'
            config['refinement_patch_count']=len(patches);config['base_sample_count']=base_count
            write_json(out/'manifest'/f'{target}-adaptive-patches.json',{'patch_size':16,'spacing':4,'chunks':patches,'rule':config['adaptive_rule']})
            db.execute('INSERT OR REPLACE INTO targets VALUES (?,?)',(target,json.dumps({'config':config,'v1':targets[target]},ensure_ascii=False)));db.commit()
            result=metrics(db,target,config,p,out)
            if config.get('topology'):result['water_topology']=topology(db,target,config,p,out)
            else:result['water_topology']={'method':'8/4-block sample context only; no full ROI connectivity claim','flow_direction':'not inferred'}
            if config.get('fine1_bounds'):
                result['critical_depression_test']=depression_test(db,target,config['fine1_bounds'][0],p,out)
            stats[target]=result;write_json(out/'assessments'/f'{target}-metrics.json',result)
            checks.extend(independent_checks(reader,db,target));print(f'{target}: {result["samples"]} stored columns; crosscheck passed',flush=True)
            render(db,out,configs,targets)
        after=fingerprint(world);vafter=fingerprint(v1)
        write_json(out/'manifest/world-after.json',after);write_json(out/'manifest/v1-after.json',vafter)
        audit={'world_writes':0,'world_inventory_sha256_size_mtime_equal':before==after,'world_file_count':len(before),'world_bytes':sum(v['size'] for v in before.values()),'v1_inventory_sha256_size_mtime_equal':vbefore==vafter,'v1_file_count':len(vbefore),'protection':'GENERIC_READ / FILE_SHARE_READ for all original world and V1 files; no Minecraft process launched','in_game_visual_review':'BLOCKED_BY_SAFE_ENVIRONMENT'}
        write_json(out/'validation/world-write-audit.json',audit)
        if before!=after or vbefore!=vafter:raise ValueError('世界或V1发生变化')
        previous=out/'validation/column-crosschecks.json';old_checks=json.loads(previous.read_text(encoding='utf-8')) if previous.exists() else []
        new_ids={r['target'] for r in checks};write_json(previous,[r for r in old_checks if r['target'] not in new_ids]+checks)
        db.commit();integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
        write_json(out/'validation/database.json',{'integrity_check':integrity,'samples':db.execute('SELECT count(*) FROM samples').fetchone()[0],'chunks':db.execute('SELECT count(*) FROM chunks').fetchone()[0],'target_samples':db.execute('SELECT count(*) FROM target_samples').fetchone()[0]})
        manifest={'schema':SCHEMA,'base_commit':BASE_COMMIT,'world_path':str(world),'world_name':'建筑师','data_version':4903,'dimension':'minecraft:overworld','timestamp':datetime.now(timezone.utc).isoformat(),'targets':configs,'status':'implementation evidence collected; assessment pending','in_game_visual_review':'BLOCKED_BY_SAFE_ENVIRONMENT','reader':'read-only nbtlib 2.0.4 + numpy padded palette decoding; no game API','observed':'surface/blocks/biome/water intervals','derived':'vegetation-filtered surface, metrics and connectivity','source_file_manifest':'world-before.json','v1_manifest':'v1-before.json'}
        write_json(out/'manifest/survey.json',manifest)
        for id in configs:
            rows=[{'name':name,'x':x,'z':z,'distance':dist,'exposed_y':y,'water_y':None if wy==-32768 else wy} for name,x,z,dist,y,wy in db.execute('SELECT name,x,z,distance,elevation,water_y FROM profiles WHERE target=? ORDER BY name,distance',(id,))]
            write_json(out/'profiles'/f'{id}.json',rows)
        db.close();print('scan complete; world and V1 fingerprints unchanged',flush=True)

def views(out):
    db=connect(out/'raw-or-queryable/refinement.sqlite');configs=json.loads((out/'manifest/roi-plan.json').read_text(encoding='utf-8'));targets=targets_at(out.parent/'V1');render(db,out,configs,targets);detail_views(db,out,configs,targets);db.close()

def verify_all(world,out):
    """补充极端值与水/冰样本审计；不重采样、不修改 V1。"""
    v1=out.parent/'V1'
    with ReadGuard(world),ReadGuard(v1):
        before=fingerprint(world);vb=fingerprint(v1)
        if vb!=json.loads((out/'manifest/v1-before.json').read_text(encoding='utf-8')):raise ValueError('V1不再匹配本任务快照')
        if before!=json.loads((out/'manifest/world-before.json').read_text(encoding='utf-8')):raise ValueError('世界不再匹配本任务快照')
        db=connect(out/'raw-or-queryable/refinement.sqlite');reader=Reader(world,db);checks=[]
        for id in TARGETS:
            checks.extend(independent_checks(reader,db,id));print(id+' independent audit complete',flush=True)
        write_json(out/'validation/column-crosschecks.json',checks)
        after=fingerprint(world);va=fingerprint(v1)
        if before!=after or vb!=va:raise ValueError('验证期间源文件改变')
        write_json(out/'validation/final-read-audit.json',{'world_inventory_equal':before==after,'v1_inventory_equal':vb==va,'world_writes':0,'checked_columns':len(checks),'all_crosschecks_pass':all(r['pass'] for r in checks)})
        db.close()
