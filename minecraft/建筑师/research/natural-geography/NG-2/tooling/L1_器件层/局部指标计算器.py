import json
import heapq
from collections import deque,Counter
import numpy as np

def grid(db,target,bounds,step=8):
    x0,z0,x1,z1=bounds;shape=((z1-z0)//step+1,(x1-x0)//step+1)
    h=np.full(shape,-32768,dtype=np.int16);water=np.zeros(shape,dtype=np.int16);bottom=np.full(shape,-32768,dtype=np.int16);biome=np.full(shape,-1,dtype=np.int16);surface=np.full(shape,-32768,dtype=np.int16)
    for x,z,sy,gy,wy,wb,bid in db.execute('SELECT s.x,s.z,s.surface_y,s.exposed_y,s.water_y,s.water_bottom,s.biome FROM samples s JOIN target_samples t USING(x,z) WHERE t.target=?',(target,)):
        if (x-x0)%step or (z-z0)%step:continue
        ix=(x-x0)//step;iz=(z-z0)//step
        if 0<=iz<shape[0] and 0<=ix<shape[1]:h[iz,ix]=gy;water[iz,ix]=wy;bottom[iz,ix]=wb;biome[iz,ix]=bid;surface[iz,ix]=sy
    if np.any(h==-32768):raise ValueError(f'{target} incomplete {step}-block grid')
    return {'height':h,'water_top':water,'water_bottom':bottom,'biome':biome,'surface':surface}

def components(mask,top=None,bottom=None):
    """四邻域连通；水必须有同Y的实际水区间重叠，不能跨斜角或干桥连通。"""
    labels=np.zeros(mask.shape,dtype=np.int32);height,width=mask.shape;counts=[]
    for z,x in zip(*np.where(mask)):
        if labels[z,x]:continue
        label=len(counts)+1;labels[z,x]=label;q=deque([(int(z),int(x))]);count=0
        while q:
            a,b=q.popleft();count+=1
            for c,d in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                if c<0 or c>=height or d<0 or d>=width or not mask[c,d] or labels[c,d]:continue
                if top is not None and max(bottom[a,b],bottom[c,d])>min(top[a,b],top[c,d]):continue
                labels[c,d]=label;q.append((c,d))
        counts.append(count)
    return labels,counts

def distribution(values):
    return {'min':float(np.min(values)),'p10':float(np.percentile(values,10)),'median':float(np.median(values)),'p90':float(np.percentile(values,90)),'max':float(np.max(values)),'mean':float(np.mean(values))}

def component_info(labels,label,bounds,step):
    if label==0:return None
    zz,xx=np.where(labels==label);mask=labels==label;x0,z0,x1,z1=bounds
    edge=[]
    for name,arr in [('north',mask[0]),('south',mask[-1]),('west',mask[:,0]),('east',mask[:,-1])]:
        if arr.any():edge.append(name)
    perimeter=int(np.sum(mask[:,1:]!=mask[:,:-1])+np.sum(mask[1:]!=mask[:-1])+np.sum(mask[0])+np.sum(mask[-1])+np.sum(mask[:,0])+np.sum(mask[:,-1]))*step
    return {'component':int(label),'columns':len(xx),'area_blocks2':len(xx)*step*step,'bounds':[int(x0+xx.min()*step),int(z0+zz.min()*step),int(min(x1,x0+xx.max()*step+step-1)),int(min(z1,z0+zz.max()*step+step-1))],'touches_roi_edges':edge,'grid_perimeter_blocks':perimeter}

def outer_ring(mask):
    """返回外侧相邻柱与内孔相邻柱；四邻域补集从ROI边缘判定外侧。"""
    ring=np.zeros(mask.shape,bool)
    ring[1:]|=mask[:-1];ring[:-1]|=mask[1:];ring[:,1:]|=mask[:,:-1];ring[:,:-1]|=mask[:,1:];ring &= ~mask
    complement,counts=components(~mask)
    exterior_ids=np.unique(np.concatenate((complement[0],complement[-1],complement[:,0],complement[:,-1])))
    exterior=np.isin(complement,exterior_ids[exterior_ids>0])
    return ring&exterior,ring&~exterior

def metrics(db,target,config,point,out):
    bounds=config['bounds'];a=grid(db,target,bounds,8);h=a['height'].astype(float);water=a['water_top']!=-32768
    dz,dx=np.gradient(h,8);slope=np.hypot(dx,dz)
    tx=(point['x']-bounds[0])//8;tz=(point['z']-bounds[1])//8
    result={'roi_bounds':bounds,'grid8_elevation':distribution(h),'grid8_slope_rise_run':distribution(slope),'water_sample_fraction':float(np.mean(water)),'target_height':int(h[tz,tx]),'surface_minus_filtered':distribution(a['surface'].astype(float)-h),'biomes':dict(Counter(db.execute('SELECT name FROM biomes WHERE id=?',(int(b),)).fetchone()[0] for b in a['biome'].ravel()))}
    masks={'low_slope_land':(~water)&(slope<=0.125),'target_elevation_band':(~water)&(np.abs(h-h[tz,tx])<=12),'high_terrain_200':(~water)&(h>=200)}
    for name,mask in masks.items():
        labels,counts=components(mask);label=labels[tz,tx];p=(tz,tx);contains=bool(label)
        if label==0 and counts:
            distances=np.where(mask,(np.indices(mask.shape)[0]-tz)**2+(np.indices(mask.shape)[1]-tx)**2,10**12);p=np.unravel_index(np.argmin(distances),mask.shape);label=labels[p]
        result[name]=component_info(labels,int(label),bounds,8)
        a[name]=labels==label if label else np.zeros(mask.shape,bool)
        if label:
            result[name].update({'contains_v1_grid_sample':contains,'selected_seed':[int(bounds[0]+p[1]*8),int(bounds[1]+p[0]*8)],'seed_distance_to_v1_point':float(np.hypot(bounds[0]+p[1]*8-point['x'],bounds[1]+p[0]*8-point['z'])),'area_method':'8-block sampled mask area; not exact column area'})
            result[name]['elevation']=distribution(h[labels==label]);result[name]['slope']=distribution(slope[labels==label])
    a['slope']=slope.astype(np.float32)
    np.savez_compressed(out/'raw-or-queryable'/f'{target}-grid8.npz',**a)
    result['samples']=db.execute('SELECT count(*) FROM target_samples WHERE target=?',(target,)).fetchone()[0]
    result['stage_new_sample_counts']=dict(db.execute('SELECT stage,count(*) FROM target_samples WHERE target=? GROUP BY stage',(target,)))
    result['artificial_material_samples']=db.execute('SELECT count(*) FROM samples s JOIN target_samples t USING(x,z) WHERE target=? AND artificial_material=1',(target,)).fetchone()[0]
    result['artificial_material_names']=[{'state':json.loads(raw),'count':n} for raw,n in db.execute('SELECT st.json,count(*) FROM samples s JOIN target_samples t USING(x,z) JOIN states st ON st.id=s.exposed_state WHERE target=? AND artificial_material=1 GROUP BY st.id',(target,))]
    return result

def topology(db,target,config,point,out):
    bounds=config['bounds'];a=grid(db,target,bounds,1);wet=a['water_top']!=-32768
    wl,wcounts=components(wet,a['water_top'],a['water_bottom']);ll,lcounts=components(~wet)
    tx=point['x']-bounds[0];tz=point['z']-bounds[1]
    primary_water=int(wl[tz,tx]);primary_land=int(ll[tz,tx])
    if not primary_water and wet.any():
        z,x=np.where(wet);i=np.argmin((z-tz)**2+(x-tx)**2);primary_water=int(wl[z[i],x[i]])
    if not primary_land and (~wet).any():
        z,x=np.where(~wet);i=np.argmin((z-tz)**2+(x-tx)**2);primary_land=int(ll[z[i],x[i]])
    info={'method':'1-block columns; four-neighbor real water vertical intervals must share at least one Y; no interpolation or biome connectivity','water_columns':int(wet.sum()),'land_columns':int((~wet).sum()),'water_components':len(wcounts),'land_components':len(lcounts),'target_is_water':bool(wet[tz,tx]),'primary_water':component_info(wl,primary_water,bounds,1),'primary_land':component_info(ll,primary_land,bounds,1),'largest_water_components':sorted(wcounts,reverse=True)[:10],'flow_direction':'not inferred'}
    if primary_land:
        mask=ll==primary_land
        ring=np.zeros(mask.shape,bool)
        ring[1:]|=mask[:-1];ring[:-1]|=mask[1:];ring[:,1:]|=mask[:,:-1];ring[:,:-1]|=mask[:,1:];ring &= ~mask
        labels=sorted(int(v) for v in np.unique(wl[ring]));info['land_boundary_neighbor_water_components']=labels
        # 外部补集的边界连通分量排除岛内池塘；不能把内湖当成外海断裂。
        outer,inner=outer_ring(mask)
        outer_labels=sorted(int(v) for v in np.unique(wl[outer]))
        info['outer_boundary_water_components']=outer_labels
        info['interior_water_boundary_columns']=int(inner.sum())
        info['land_fully_enclosed_by_one_water_component']=not info['primary_land']['touches_roi_edges'] and len(outer_labels)==1 and outer_labels[0]>0
        if mask.any():
            heights=np.where(mask,a['height'],-32768);z,x=np.unravel_index(np.argmax(heights),heights.shape)
            info['land_highest']={'x':int(bounds[0]+x),'y':int(heights[z,x]),'z':int(bounds[1]+z)}
    if primary_water:
        mask=wl==primary_water;info['primary_water']['elevation']=distribution(a['water_top'][mask]);info['primary_water']['depth']=distribution((a['water_top']-a['water_bottom']+1)[mask])
        labels=Counter(int(v) for v in a['biome'][mask]);info['primary_water']['biomes']={db.execute('SELECT name FROM biomes WHERE id=?',(bid,)).fetchone()[0]:n for bid,n in labels.items()}
    np.savez_compressed(out/'raw-or-queryable'/f'{target}-topology1.npz',**a,water_labels=wl,land_labels=ll)
    return info

def depression_test(db,target,bounds,point,out):
    """一格实测地表的最低溢出路径；只判断低点/鞍部形态，不声称游戏角色可通行。"""
    a=grid(db,target,bounds,1);h=a['height'];tz=point['z']-bounds[1];tx=point['x']-bounds[0];start=int(h[tz,tx])
    cost=np.full(h.shape,32767,dtype=np.int16);cost[tz,tx]=start;parent={};queue=[(start,tz,tx)];exits={};end=None
    while queue:
        c,z,x=heapq.heappop(queue)
        if c!=cost[z,x]:continue
        edges=[]
        if z==0:edges.append('north')
        if z==h.shape[0]-1:edges.append('south')
        if x==0:edges.append('west')
        if x==h.shape[1]-1:edges.append('east')
        for edge in edges:
            if edge not in exits:exits[edge]={'minimum_required_height':c,'rise_above_target':c-start,'endpoint':[bounds[0]+x,bounds[1]+z]}
        if edges and end is None:end=(z,x)
        for zz,xx in ((z-1,x),(z+1,x),(z,x-1),(z,x+1)):
            if zz<0 or xx<0 or zz>=h.shape[0] or xx>=h.shape[1]:continue
            nc=max(c,int(h[zz,xx]))
            if nc<int(cost[zz,xx]):cost[zz,xx]=nc;parent[(zz,xx)]=(z,x);heapq.heappush(queue,(nc,zz,xx))
    tests=[]
    for offset in [0,2,4,8,16]:
        labels,counts=components(h<=start+offset);label=int(labels[tz,tx]);tests.append({'height_ceiling':start+offset,'component':component_info(labels,label,bounds,1)})
    path=[];p=end
    while p is not None:
        z,x=p;path.append({'x':int(bounds[0]+x),'z':int(bounds[1]+z),'y':int(h[z,x])});p=parent.get(p)
    path.reverse()
    routes={}
    # 顶部无被过滤遮挡、无水、相邻柱高差不超过1，是保守地形步进图；非完整游戏物理。
    clear=(a['surface']==h)&(a['water_top']==-32768)
    for axis in ('east-west','north-south'):
        costs=np.full(h.shape,32767,dtype=np.int16);parents={};heap=[]
        starts=[(z,0) for z in range(h.shape[0])] if axis=='east-west' else [(0,x) for x in range(h.shape[1])]
        for z,x in starts:
            if clear[z,x]:costs[z,x]=h[z,x];heapq.heappush(heap,(int(h[z,x]),z,x))
        goal=None
        while heap:
            c,z,x=heapq.heappop(heap)
            if c!=costs[z,x]:continue
            if (axis=='east-west' and x==h.shape[1]-1) or (axis=='north-south' and z==h.shape[0]-1):goal=(z,x);break
            for zz,xx in ((z-1,x),(z+1,x),(z,x-1),(z,x+1)):
                if zz<0 or xx<0 or zz>=h.shape[0] or xx>=h.shape[1] or not clear[zz,xx] or abs(int(h[zz,xx])-int(h[z,x]))>1:continue
                nc=max(c,int(h[zz,xx]))
                if nc<int(costs[zz,xx]):costs[zz,xx]=nc;parents[(zz,xx)]=(z,x);heapq.heappush(heap,(nc,zz,xx))
        route=[];p=goal
        while p is not None:
            z,x=p;route.append({'x':int(bounds[0]+x),'z':int(bounds[1]+z),'y':int(h[z,x])});p=parents.get(p)
        route.reverse()
        routes[axis]={'exists':goal is not None,'minimum_required_height':int(costs[goal]) if goal else None,'columns':len(route),'closest_to_v1_point':min((float(np.hypot(p['x']-point['x'],p['z']-point['z'])) for p in route),default=None),'path':route,'limitation':'Conservative integer-height graph. Slab half heights and full Minecraft entity physics are not modeled; failure does not prove absolute impassability.'}
    result={'bounds':bounds,'resolution':1,'target_height':start,'edge_escape_minimax':exits,'low_components':tests,'minimum_escape_path':path,'terrain_step_crossings':routes,'meaning':'Morphological escape elevation and conservative real-column terrain-step connectivity; not gameplay pathfinding.'}
    np.savez_compressed(out/'raw-or-queryable'/f'{target}-critical1.npz',**a,minimax_height=cost)
    return result
