"""所有类别均为阈值派生候选；连通性仅是 64 格采样网格连通性。"""
import json
import math
from collections import Counter,defaultdict
from statistics import mean,pstdev
from L0_公理层.地理契约 import neighbors,STEP

def components(points):
    remaining=set(points)
    groups=[]
    while remaining:
        start=min(remaining); remaining.remove(start); stack=[start]; group=[]
        while stack:
            p=stack.pop();group.append(p)
            for q in neighbors(p):
                if q in remaining:
                    remaining.remove(q);stack.append(q)
        groups.append(group)
    return groups

def derive_cells(db):
    grouped=defaultdict(list)
    for x,z,raw in db.execute('SELECT x,z,observed FROM samples'):
        grouped[(x//STEP,z//STEP)].append(json.loads(raw))
    cells={}
    for p,ss in grouped.items():
        center=next(s for s in ss if s['x']%16==8 and s['z']%16==8)
        yy=[s['exposed_y'] for s in ss]
        water=mean(s['water'] for s in ss)
        cells[p]={'gx':p[0],'gz':p[1],'x':center['x'],'z':center['z'],'elevation':mean(yy),'water':water,'biome':Counter(s['biome'] for s in ss).most_common(1)[0][0],'roughness':pstdev(yy),'observed':ss}
    for p,c in cells.items():
        nearby=[cells[(p[0]+dx,p[1]+dz)]['elevation'] for dx in range(-3,4) for dz in range(-3,4) if (p[0]+dx,p[1]+dz) in cells]
        edge=[abs(c['elevation']-cells[q]['elevation'])/STEP for q in neighbors(p) if q in cells]
        c['slope']=max(edge,default=0);c['relief']=max(nearby)-min(nearby)
        c['relative_elevation']=c['elevation']-mean(nearby)
        if c['water']>=0.6:t='water'
        elif 'swamp' in c['biome'] or 'marsh' in c['biome']:t='wetlands_candidate'
        elif c['elevation']>=150 and c['relief']>=65:t='mountains_candidate'
        elif c['elevation']>=120 and c['slope']<0.12 and c['roughness']<3:t='plateau_candidate'
        elif c['relative_elevation']<=-18 and c['relief']>=45:t='valley_candidate'
        elif c['elevation']>=120:t='highlands_candidate'
        elif c['slope']<=0.12 and c['relief']<=30 and c['roughness']<=3:t='plains_candidate'
        else:t='hills_candidate'
        c['terrain']=t
    db.execute('DELETE FROM cells')
    db.executemany('INSERT INTO cells VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',[(p[0],p[1],c['x'],c['z'],c['elevation'],c['water'],c['biome'],c['slope'],c['relief'],c['roughness'],c['terrain'],None,json.dumps(c['observed'])) for p,c in cells.items()])
    return cells

class Atlas:
    def __init__(self,db,cells):
        self.db=db;self.cells=cells;self.current=[];self.used=set()
        self.old={row[0]:(row[1],row[2],set()) for row in db.execute('SELECT id,family,type FROM objects')}
        for id,x,z in db.execute('SELECT id,gx,gz FROM members'):
            if id in self.old:self.old[id][2].add((x,z))
        self.next={f:1+max([int(id.split('-')[1]) for id in self.old if id.startswith(f+'-')],default=0) for f in ('GEO','HYD','FEAT','SITE')}
        db.execute('UPDATE objects SET active=0')
        db.execute('DELETE FROM adjacency')
    def add(self,family,kind,points,confidence,extra=None):
        ps=set(points)
        # 增量通过同类成员重叠保持 ID；拆分/合并记录旧对象，绝不回收号码。
        candidates=[(len(ps&old[2])/max(len(ps|old[2]),1),id) for id,old in self.old.items() if old[:2]==(family,kind) and id not in self.used]
        best=max(candidates,default=(0,None))
        if best[0]>=0.35:id=best[1]
        else:
            id=f'{family}-{self.next[family]:03d}';self.next[family]+=1
        self.used.add(id)
        cc=[self.cells[p] for p in points]
        cx=mean(c['x'] for c in cc);cz=mean(c['z'] for c in cc)
        rep=min(cc,key=lambda c:(c['x']-cx)**2+(c['z']-cz)**2)
        details={'bounds':{'min_x':min(p[0] for p in ps)*STEP,'max_x':max(p[0] for p in ps)*STEP+STEP-1,'min_z':min(p[1] for p in ps)*STEP,'max_z':max(p[1] for p in ps)*STEP+STEP-1},'centroid':{'x':cx,'z':cz},'representative':{'x':rep['x'],'y':rep['elevation'],'z':rep['z']},'sample_cells':len(ps),'estimated_area_blocks2':len(ps)*STEP*STEP,'elevation':{'min':min(c['elevation'] for c in cc),'max':max(c['elevation'] for c in cc),'mean':mean(c['elevation'] for c in cc)},'terrain_metrics':{'mean_slope':mean(c['slope'] for c in cc),'mean_roughness':mean(c['roughness'] for c in cc),'max_relief':max(c['relief'] for c in cc)},'biomes':dict(Counter(s['biome'] for c in cc for s in c['observed'])),'evidence':'members -> cells -> samples.observed -> chunks -> regions.sha256','boundary_censored':any(q not in self.cells for p in ps for q in neighbors(p))}
        details.update(extra or {})
        representative_sample=next(s for s in rep['observed'] if s['x']==rep['x'] and s['z']==rep['z'])
        details['representative']['y']=representative_sample['exposed_y']
        details['representative']['y_semantics']='sampled vegetation-filtered exposed surface, not cell mean'
        obj={'id':id,'family':family,'type':kind,'evidence_level':'interpretive' if family=='SITE' else 'derived','confidence':confidence,**details}
        self.db.execute('INSERT OR REPLACE INTO objects VALUES (?,?,?,?,?,?,1)',(id,family,kind,obj['evidence_level'],confidence,json.dumps(details)))
        self.db.execute('DELETE FROM members WHERE id=?',(id,))
        self.db.executemany('INSERT INTO members VALUES (?,?,?)',[(id,*p) for p in ps])
        self.current.append(obj)
        return id

def build_atlas(db,cells):
    atlas=Atlas(db,cells);geo={}
    classes=defaultdict(set)
    for p,c in cells.items():classes[c['terrain']].add(p)
    for kind,points in sorted(classes.items()):
        for group in sorted(components(points),key=lambda g:(-len(g),min(g))):
            id=atlas.add('GEO',kind,group,0.55 if len(group)>=4 else 0.3)
            for p in group:geo[p]=id
    db.executemany('UPDATE cells SET geo_id=? WHERE gx=? AND gz=?',[(id,*p) for p,id in geo.items()])
    adjacent=Counter()
    for p,id in geo.items():
        for q in ((p[0]+1,p[1]),(p[0],p[1]+1)):
            if q in geo and geo[q]!=id:adjacent[tuple(sorted((id,geo[q])))]+=1
    db.executemany('INSERT INTO adjacency VALUES (?,?,?)',[(a,b,n) for (a,b),n in adjacent.items()])
    water={p for p,c in cells.items() if c['water']>=0.6}
    hyd_groups=components(water)
    hyd_map={};feature_candidates=[]
    for group in sorted(hyd_groups,key=lambda g:(-len(g),min(g))):
        if len(group)<2:continue
        cc=[cells[p] for p in group];bios=Counter(c['biome'] for c in cc)
        ocean=sum(n for b,n in bios.items() if 'ocean' in b)>len(group)*0.25
        width=max(p[0] for p in group)-min(p[0] for p in group)+1
        depth=max(p[1] for p in group)-min(p[1] for p in group)+1
        fill=len(group)/(width*depth)
        edge=any(q not in cells for p in group for q in neighbors(p))
        if ocean:kind='ocean_connected_water_candidate'
        elif len(group)>=5 and (max(width,depth)/min(width,depth)>=3 or fill<0.28):kind='river_like_water_candidate'
        elif not edge:kind='inland_water_body_candidate'
        else:kind='boundary_connected_water_uncertain'
        id=atlas.add('HYD',kind,group,0.55,{'shape':{'width_cells':width,'depth_cells':depth,'bbox_fill':fill},'connectivity':'4-neighbor sampled water; unsampled gaps unverified','flow_direction':'unknown'})
        for p in group:hyd_map[p]=id
        if kind=='inland_water_body_candidate' and len(group)>=6:feature_candidates.append(('lakeshore_terrace_candidate',group,0.45,{'hyd_id':id}))
    land=set(cells)-water
    for group in components(land):
        group_set=set(group)
        boundary={q for p in group for q in neighbors(p) if q not in group_set}
        if 2<=len(group)<=200 and boundary and boundary<=water:
            feature_candidates.append(('island_candidate',group,0.55,{}))
    for p,c in cells.items():
        if p in water:continue
        if c['slope']>=0.65 and c['relief']>=50:feature_candidates.append(('escarpment_candidate',[p],0.45,{}))
        ns=[q for q in neighbors(p) if q in cells]
        wet=[q for q in ns if q in water]
        if wet and any('ocean' in cells[q]['biome'] for q in wet):
            feature_candidates.append(('coastline_candidate',[p],0.55,{}))
        if len(wet)>=3:feature_candidates.append(('peninsula_tip_candidate',[p],0.35,{}))
        # 山口要求两侧高、正交方向低；仅是 64 格鞍形候选。
        x,z=p
        if all(q in cells for q in neighbors(p)) and c['elevation']>95:
            a,b,d,e=[cells[q]['elevation']-c['elevation'] for q in neighbors(p)]
            if (min(a,b)>10 and max(d,e)<-3) or (min(d,e)>10 and max(a,b)<-3):feature_candidates.append(('mountain_pass_candidate',[p],0.35,{}))
        if c['terrain']=='valley_candidate':
            feature_candidates.append(('broad_valley_candidate' if c['slope']<0.2 else 'narrow_valley_candidate',[p],0.4,{}))
            if wet:feature_candidates.append(('river_valley_candidate',[p],0.4,{}))
    # 合并同类相邻候选，避免把每一个 cliff 网格都当作独立自然区域。
    bykind=defaultdict(set)
    for kind,group,conf,extra in feature_candidates:bykind[kind].update(group)
    for kind,ps in sorted(bykind.items()):
        for group in sorted(components(ps),key=lambda g:(-len(g),min(g))):
            atlas.add('FEAT',kind,group,0.35 if kind in ('mountain_pass_candidate','peninsula_tip_candidate') else 0.45)
    # 水面形状的离散判断只作为进一步观察线索，不推断流向/真实航道。
    patterns=defaultdict(set)
    for p in water:
        x,z=p
        if not all(q in cells for q in neighbors(p)):continue
        left,right,up,down=[q in water for q in neighbors(p)]
        if (not left and not right and up and down) or (left and right and not up and not down):patterns['narrow_crossing_candidate'].add(p)
        if sum((left,right,up,down))==3 and all(cells[q]['water']<1 for q in neighbors(p) if q in water):patterns['confluence_uncertain'].add(p)
        if sum((left,right,up,down))==1 and any('ocean' in cells[q]['biome'] for q in neighbors(p) if q in water):patterns['coastal_bay_candidate'].add(p)
    for kind,ps in patterns.items():
        for group in components(ps):atlas.add('HYD',kind,group,0.25)
    selected=[]
    # 每个地貌类型最多两处，且相距至少 512 格，保证候选类型与空间代表性。
    priorities=['mountain_pass_candidate','island_candidate','broad_valley_candidate','narrow_valley_candidate','escarpment_candidate','coastal_bay_candidate','plateau_candidate','plains_candidate','mountains_candidate','inland_water_body_candidate']
    for kind in priorities:
        candidates=sorted([o for o in atlas.current if o['type']==kind and o['family']!='SITE'],key=lambda o:-o['sample_cells'])
        count=0
        for obj in candidates:
            r=obj['representative']
            if any(math.hypot(r['x']-a['x'],r['z']-a['z'])<512 for a in selected):continue
            p=(r['x']//STEP,r['z']//STEP)
            potential='large-settlement/agriculture terrain potential' if kind=='plains_candidate' else 'monumental-landmark/isolated-retreat terrain potential'
            atlas.add('SITE',kind,[p],min(0.45,obj['confidence']),{'source_object':obj['id'],'potential':potential,'requires':'local terrain, water connectivity, artificial structures and visual verification; no Canon'})
            selected.append(r);count+=1
            if count==2:break
    return atlas.current
