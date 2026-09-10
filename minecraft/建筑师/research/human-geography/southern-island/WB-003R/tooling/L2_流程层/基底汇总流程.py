"""复用地表缓存并汇总有限柱样本；所有经济解释留给研究报告。"""
import json,sqlite3
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
from L0_公理层.基底契约 import BOUNDS,SOIL,domains,ore_kind
from L1_器件层.缓存读取器 import load,distribution,distance
from L1_器件层.源快照保护器 import write_json
from L1_器件层.通达代理计算器 import crossing,corridors

def derive(out,cache):
    old=out.parent/'WB-002R-R1';a,m,states,biomes=load(old);dd=domains(a,m)
    def counts(values,lookup=None):
        keys,nums=np.unique(values,return_counts=True)
        result=Counter()
        # 多个block state可映射到同一方块名称，必须相加而非覆盖。
        for k,n in zip(keys,nums):result[lookup[int(k)] if lookup else str(int(k))]+=int(n)
        return dict(result)
    names={k:v['Name'] for k,v in states.items()};soil=np.isin(a['exposed_state'],[k for k,v in names.items() if v in SOIL]);flat=m['terrain_class']>0
    water=json.loads((old/'profile/internal-water.json').read_text(encoding='utf-8'));ids=sum([v['water_component_ids'] for v in water.values()],[])
    inland=distance(np.isin(m['water_component'],ids));shore=distance(m['shoreline']);sub={};materials={};access={}
    for key,mask in dd.items():
        proxy=mask&soil&flat;sample=mask&(a['trunk']>=0)
        sub[key]={'columns':int(mask.sum()),'elevation':distribution(a['exposed_y'][mask]),'flat_columns':int((mask&(m['terrain_class']==1)).sum()),'gentle_columns':int((mask&(m['terrain_class']==2)).sum()),'soil_lowrelief_columns':int(proxy.sum()),'soil_lowrelief_fraction':float(proxy.sum()/mask.sum()),'surface_biomes':counts(a['biome'][mask],biomes),'proxy_inland_water_manhattan_distance':distribution(inland[proxy]),'proxy_shore_manhattan_distance':distribution(shore[proxy])}
        materials[key]={'exposed_block_columns':counts(a['exposed_state'][mask],names),'vegetation_sample_columns':int(sample.sum()),'trunk_occupied_fraction':float(np.mean(a['trunk'][sample]>0)),'leaf_occupied_fraction':float(np.mean(a['leaf'][sample]>0))}
        access[key]={'land_within_16_of_internal_water':int((mask&(inland<=16)).sum()),'land_within_64_of_internal_water':int((mask&(inland<=64)).sum()),'shore_columns':int((mask&m['shoreline']).sum())}
    sensitivity=[]
    for xx in (480,640,800):
        for yy in (100,120,140):
            mask=m['east']&(a['x']<xx)&(a['exposed_y']<=yy)
            sensitivity.append({'x_lt':xx,'y_le':yy,'columns':int(mask.sum()),'soil_lowrelief_fraction':float((mask&soil&flat).sum()/mask.sum())})
    write_json(out/'profile/substrate-summary.json',{'bounds':BOUNDS,'mask_definitions':{'W':'R1 west','M':'R1 east AND x<640 AND exposed_y<=120','E':'R1 east AND x>=640 AND exposed_y>=140'},'unassigned_land_columns':int(((m['land_component']>0)&~(dd['W']|dd['M']|dd['E'])).sum()),'domains':sub,'middle_mask_sensitivity':sensitivity,'interpretation':'research masks, not political boundaries; soil-name AND R1 FLAT/GENTLE is morphology/material proxy, not fertility or yield; distances are geometric Manhattan, not paths'})
    db=sqlite3.connect((old/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True);wood={k:Counter() for k in dd};mixed=0
    chunk_masks={k:mask.reshape(mask.shape[0]//16,16,mask.shape[1]//16,16).sum(axis=(1,3))>=192 for k,mask in dd.items()}
    for cx,cz,name,n in db.execute('SELECT cx,cz,name,count FROM vegetation_palette'):
        assigned=[k for k,v in chunk_masks.items() if v[cz-BOUNDS[1]//16,cx-BOUNDS[0]//16]]
        if assigned:wood[assigned[0]][name]+=n
        else:mixed+=n
    db.close()
    for k in dd:materials[k]['sampled_vegetation_palette']=dict(wood[k])
    traces=json.loads((cache/'mineral-columns.json').read_text(encoding='utf-8'));minerals={};positives=[]
    for k in dd:
        sites=[s for s in traces if s['domain']==k];bands=[];near=Counter()
        for lo,hi in ((-60,-1),(0,59),(60,119),(120,179),(180,239),(240,300)):
            ores=Counter();present=Counter();total=solid=0;covered=0
            for s in sites:
                seen=set();covered+=int(s['surface_y']>=lo)
                for y in range(lo,min(hi,s['surface_y'])+1):
                    name=s['blocks'][y+60];total+=1;solid+=int(name not in ('minecraft:air','minecraft:cave_air','minecraft:water','minecraft:lava'))
                    ore=ore_kind(name)
                    if ore:ores[ore]+=1;seen.add(ore)
                present.update(seen)
            bands.append({'y_inclusive':[lo,hi],'columns_intersecting':covered,'sampled_blocks':total,'non_air_non_fluid_blocks':solid,'ore_blocks':dict(ores),'columns_with_ore':dict(present)})
        for s in sites:
            near.update(s['blocks'][-16:])
            for ore in ('coal','iron','copper','gold','redstone','lapis','diamond','emerald'):
                found=[i for i,n in enumerate(s['blocks']) if ore_kind(n)==ore]
                if found and not any(v['domain']==k and v['ore']==ore for v in positives):
                    i=found[0];positives.append({'domain':k,'sample_id':s['id'],'ore':ore,'x':s['x'],'y':i-60,'z':s['z'],'block':s['blocks'][i],'region':s['region'],'region_sha256':s['region_sha256']})
        minerals[k]={'columns':len(sites),'absolute_depth_bands':bands};materials[k]['sampled_top16_block_counts']=dict(near)
    write_json(out/'profile/material-profile.json',{'domains':materials,'mixed_or_unassigned_vegetation_block_observations':mixed,'vegetation_method':'R1 sampled plant palette assigned only when >=75% of chunk columns in mask; counts are sampled block observations, not tree inventory; top16 uses targeted columns only'})
    write_json(out/'profile/mineral-sample-profile.json',{'domains':minerals,'positive_witnesses':positives,'limitations':'absence only within sampled columns/depth; unequal vertical coverage; compare common Y bands, never infer regional density or reserves'})
    print('surface and minerals summarized',flush=True)
    cross,good=crossing(a,m)
    for k,mask in dd.items():access[k]['landing_proxy_shore_columns']=int((mask&good).sum())
    write_json(out/'profile/water-access-profile.json',{'domains':access,'method':'WATER_ACCESS_PROXY: geometric Manhattan distance to R1 enclosed surface water; LANDING_ACCESS_PROXY: 8 dry inward cardinal steps <=1 with relief16<=8; no freshwater, navigation or port claim'})
    write_json(out/'profile/crossing-profile.json',cross);print('crossings summarized',flush=True)
    paths=corridors(a,m,dd);write_json(out/'profile/movement-corridors.json',paths);print('corridors summarized',flush=True)
    rgb=np.zeros((*a['x'].shape,3),np.uint8);rgb[:]=(36,76,110);rgb[m['land_component']>0]=(110,110,100)
    for k,c in zip(dd,((120,180,90),(220,185,90),(160,130,110))):rgb[dd[k]]=c
    rgb[soil&flat&(dd['W']|dd['M']|dd['E'])]=(60,220,100)
    im=Image.fromarray(rgb).resize((1632,1056));draw=ImageDraw.Draw(im)
    def point(x,z):return ((x-BOUNDS[0])/2,(z-BOUNDS[1])/2)
    for p in paths['candidates']:
        draw.line([point(x,z) for x,z,y in p['path']],fill='magenta',width=3);x,z,_=p['path'][-1];draw.text(point(x,z),p['id'],fill='white')
    for p in cross['candidates']:
        if 'west' in p:draw.line([point(p[k]['x'],p[k]['z']) for k in ('west','east')],fill='cyan',width=3);draw.text(point(p['west']['x'],p['west']['z']),p['id'],fill='white')
    canvas=Image.new('RGB',(1632,1120),'black');canvas.paste(im,(0,64));draw=ImageDraw.Draw(canvas)
    draw.text((12,10),'WB-003R | N = -Z (up) | scale 2 blocks/pixel | X -800..2463, Z 1376..3487',fill='white');draw.text((12,32),'Green: soil+lowrelief | tan: M | brown: E | grey: unassigned | cyan: gap probes | magenta: cost paths',fill='white')
    canvas.save(out/'visual/substrate-access.png')
