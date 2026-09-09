import hashlib
import json
from collections import Counter
from PIL import Image,ImageDraw,ImageFont

PALETTE={'water':(40,105,181),'plains_candidate':(151,190,99),'hills_candidate':(124,149,79),'highlands_candidate':(171,154,113),'mountains_candidate':(139,126,119),'plateau_candidate':(222,180,109),'valley_candidate':(207,219,134),'wetlands_candidate':(63,129,121)}

def color(text):
    d=hashlib.sha256(text.encode()).digest()
    return tuple(65+v%160 for v in d[:3])

def render(db,out):
    """所有图片从 SQLite 重建，北为 -Z，右为 +X；黑色是未采样/未知。"""
    cells=[dict(zip(('gx','gz','elevation','water','biome','terrain','geo_id'),r)) for r in db.execute('SELECT gx,gz,elevation,water,biome,terrain,geo_id FROM cells')]
    xmin=min(c['gx'] for c in cells);xmax=max(c['gx'] for c in cells)
    zmin=min(c['gz'] for c in cells);zmax=max(c['gz'] for c in cells)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    width=xmax-xmin+1;height=zmax-zmin+1
    scale=max(1,min(4,1300//max(width,height)))
    objects=[{'id':id,'family':f,'type':t,**json.loads(d)} for id,f,t,d in db.execute('SELECT id,family,type,details FROM objects WHERE active=1')]
    def decorate(im,title,legend):
        im=im.resize((width*scale,height*scale),Image.Resampling.NEAREST)
        canvas=Image.new('RGB',(max(im.width,850),im.height+150),(25,29,34));canvas.paste(im,(0,75))
        draw=ImageDraw.Draw(canvas);draw.text((12,8),title,fill='white',font=font)
        draw.text((12,30),f'X [{xmin*64}, {xmax*64+63}]  Z [{zmin*64}, {zmax*64+63}] | North (-Z) up | grid 64 blocks',fill='white',font=small)
        draw.text((12,49),'Observed samples / algorithmic candidates; black = unknown. Source: raw/geography.sqlite',fill='white',font=small)
        for i,line in enumerate(legend):draw.text((12,im.height+80+i*16),line,fill='white',font=small)
        return canvas
    heights=[c['elevation'] for c in cells];low=min(heights);high=max(heights)
    for kind in ('heightmap','biome-overview','water-map','terrain-region-map','GEO-labeled-map','SITE-overview-map'):
        im=Image.new('RGB',(width,height))
        for c in cells:
            if kind=='heightmap':
                a=(c['elevation']-low)/max(1,high-low);rgb=(int(30+220*a),int(70+170*a),int(80+155*a))
            elif kind=='biome-overview':rgb=color(c['biome'])
            elif kind=='water-map':rgb=(30,105,int(140+115*c['water'])) if c['water'] else (165,158,124)
            elif kind=='GEO-labeled-map':rgb=color(c['geo_id'])
            else:rgb=PALETTE[c['terrain']]
            im.putpixel((c['gx']-xmin,c['gz']-zmin),rgb)
        legend=[f'Elevation (vegetation-filtered sample mean): {low:.1f} to {high:.1f} blocks'] if kind=='heightmap' else ['Full legend and thresholds: reports/map-legends.json; all feature labels are provisional.']
        canvas=decorate(im,kind,legend);draw=ImageDraw.Draw(canvas)
        if kind in ('terrain-region-map','SITE-overview-map'):
            for i,(name,rgb) in enumerate(PALETTE.items()):
                lx=im.width*scale+14;ly=85+i*40
                draw.rectangle((lx,ly,lx+12,ly+12),fill=rgb)
                draw.text((lx,ly+15),name.replace('_candidate',''),fill='white',font=small)
        if kind in ('GEO-labeled-map','SITE-overview-map'):
            os=sorted([o for o in objects if o['family']==('GEO' if kind=='GEO-labeled-map' else 'SITE')],key=lambda o:-o['sample_cells'])
            for o in os[:35]:
                r=o['representative'];px=(r['x']/64-xmin)*scale;py=(r['z']/64-zmin)*scale+75
                draw.ellipse((px-3,py-3,px+3,py+3),fill='yellow',outline='black')
                draw.text((px+4,py),o['id'],fill='white',stroke_width=1,stroke_fill='black',font=small)
        canvas.save(out/'visual'/f'{kind}.png')
    chunks=list(db.execute('SELECT c.cx,c.cz,s.status FROM chunks c LEFT JOIN chunk_status s USING(cx,cz)'))
    cx0=min(r[0] for r in chunks);cx1=max(r[0] for r in chunks);cz0=min(r[1] for r in chunks);cz1=max(r[1] for r in chunks)
    im=Image.new('RGB',(cx1-cx0+1,cz1-cz0+1))
    status_colors={'minecraft:full':(74,174,115),'minecraft:biomes':(226,181,73),'minecraft:structure_starts':(127,102,154),'minecraft:carvers':(222,131,61),'minecraft:initialize_light':(72,185,201)}
    for x,z,status in chunks:im.putpixel((x-cx0,z-cz0),status_colors.get(status,(220,75,70)))
    canvas=Image.new('RGB',(max(850,im.width),im.height+65),(25,29,34));canvas.paste(im,(0,65));draw=ImageDraw.Draw(canvas)
    draw.text((10,8),f'Generated chunk headers | 1 pixel = 1 chunk | X chunks [{cx0},{cx1}] Z [{cz0},{cz1}]',fill='white',font=small)
    draw.text((10,29),'Green=full | yellow=biomes | purple=structure_starts | orange=carvers | cyan=initialize_light',fill='white',font=small)
    draw.text((10,46),'All chunk statuses audited. Black=absent. Partially generated chunks are not terrain survey coverage.',fill='white',font=small)
    canvas.save(out/'visual'/'generated-chunk-coverage.png')
    legends={'terrain':{k:list(v) for k,v in PALETTE.items()},'biomes':{c['biome']:color(c['biome']) for c in cells},'geo_label_limit':35,'water':'blue intensity represents fraction of 5 sampled columns, not water depth','height_range':[low,high]}
    (out/'reports'/'map-legends.json').write_text(json.dumps(legends,indent=2),encoding='utf-8')

def report(db,out):
    m=json.loads(db.execute("SELECT value FROM meta WHERE key='manifest'").fetchone()[0])
    objects=[{'schema_version':m['schema_version'],'id':id,'family':f,'type':t,'evidence_level':level,'confidence':conf,**json.loads(d)} for id,f,t,level,conf,d in db.execute('SELECT id,family,type,evidence_level,confidence,details FROM objects WHERE active=1')]
    for family,directory in [('GEO','atlas'),('HYD','atlas'),('FEAT','atlas'),('SITE','sites')]:
        (out/directory/f'{family}.jsonl').write_text(''.join(json.dumps(o,ensure_ascii=False)+'\n' for o in objects if o['family']==family),encoding='utf-8')
    (out/'atlas'/'adjacency.jsonl').write_text(''.join(json.dumps({'a':a,'b':b,'shared_cell_edges':n})+'\n' for a,b,n in db.execute('SELECT * FROM adjacency')),encoding='utf-8')
    counts=Counter(o['family'] for o in objects)
    distribution=list(db.execute('SELECT terrain,count(*),round(avg(elevation),1) FROM cells GROUP BY terrain ORDER BY count(*) DESC'))
    cov=m['coverage']
    coverage_text=f"完整生成方块范围：{cov.get('full_block_bounds','尚未完成状态审计')}；完整生成分量：{cov.get('full_components',[])}；区块状态统计：{cov.get('all_chunk_status_counts',{})}。Header 范围 {cov['block_bounds']} 不等于完成地形范围。"
    lines=['# 自然地理初步探查 V1',f"状态：{m['status']}；world writes = 0（全存档前后 SHA256/大小/修改时间与文件清单一致）。",f"存档：`{m['world_path']}`。Minecraft {m['minecraft']}，DataVersion {m['data_version']}。",coverage_text,f"已采样 {m['sampled_chunks']} 个区块、{m['sample_columns']} 根柱，64 格网格；每个单元采样区块内五柱。",f'对象数量：{dict(counts)}。GEO 是连通地形单元，不是命名山脉或行政区；小型碎片也保留。','## 地形统计（采样单元）']
    lines += [f'- {t}: {n} 单元，平均高度 {h}' for t,n,h in distribution]
    mountains=sorted([o for o in objects if o['family']=='GEO' and o['type']=='mountains_candidate'],key=lambda o:-o['sample_cells'])[:2]
    major_water=sorted([o for o in objects if o['family']=='HYD' and o['type']=='ocean_connected_water_candidate'],key=lambda o:-o['sample_cells'])[:1]
    lines += ['## 大尺度骨架']
    for o in mountains+major_water:
        lines.append(f"- {o['id']}：{o['type']}，范围 {o['bounds']}，估计覆盖 {o['estimated_area_blocks2']/1000000:.2f} 百万方块平方，样本平均高度 {o['elevation']['mean']:.1f}。")
    lines += ['## 下一步代表性观察地点']
    focus=[]
    for kind in ('mountains_candidate','plains_candidate','broad_valley_candidate','mountain_pass_candidate','island_candidate','coastal_bay_candidate','plateau_candidate','inland_water_body_candidate'):
        candidate=next((o for o in objects if o['family']=='SITE' and o['type']==kind),None)
        if candidate:focus.append(candidate)
    lines += [f"- {o['id']} / {o['source_object']}：{o['type']}，X={o['representative']['x']}，Y≈{o['representative']['y']}，Z={o['representative']['z']}，置信度 {o['confidence']}。" for o in focus]
    lines += ['## 已知限制']+[f'- {x}' for x in m['limitations']]
    lines += ['下一阶段建议：先针对山地、谷地、平原和水岸候选做 4–8 格局部只读精查，并在安全观察环境中复核；本轮停止，不进入文明设定或建筑规划。','工具分层：L0 编码契约；L1 文件读取/存储/推导/地图；L2 调查流程；L3 命令公开边界。无跨模块内部调用。']
    (out/'reports'/'summary.md').write_text('\n\n'.join(lines),encoding='utf-8')
    mapping={'mountains / mountain chains':['mountains_candidate'],'highlands':['highlands_candidate'],'hills':['hills_candidate'],'plateaus':['plateau_candidate'],'plains':['plains_candidate'],'broad valleys':['broad_valley_candidate'],'narrow valleys':['narrow_valley_candidate'],'coastline':['coastline_candidate'],'major inland water':['inland_water_body_candidate'],'islands':['island_candidate'],'peninsulas':['peninsula_tip_candidate'],'wetlands':['wetlands_candidate'],'escarpments / cliffs':['escarpment_candidate'],'passes / corridors':['mountain_pass_candidate'],'ocean / sea':['ocean_connected_water_candidate'],'river-like systems':['river_like_water_candidate'],'river valleys':['river_valley_candidate'],'confluences':['confluence_uncertain'],'narrow crossings':['narrow_crossing_candidate'],'coastal bays':['coastal_bay_candidate'],'natural harbors':[],'waterfalls / dramatic water transitions':[]}
    assessment=[]
    for requirement,types in mapping.items():
        matches=[o for o in objects if o['type'] in types and o['family']!='SITE']
        assessment.append({'requirement':requirement,'status':'provisional_candidates' if matches else 'uncertain_not_established','count':len(matches),'object_ids':[o['id'] for o in matches],'limitation':'Coarse sampled morphology only; not field-verified. No candidates does not prove absence.' if types else '64-block sampling does not establish depth, navigability, current or falling-water continuity; no positive assertion.'})
    (out/'atlas'/'detector-assessment.json').write_text(json.dumps(assessment,ensure_ascii=False,indent=2),encoding='utf-8')
