"""只读SQLite查询；每次请求独立连接，几何命中使用成员runs，不使用对象bbox。"""
import json,sqlite3,math
from L0_公理层.图册契约 import cell_of

class AtlasReader:
    def __init__(self,path):
        self.db=sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True);self.db.row_factory=sqlite3.Row
        self.meta={r['key']:json.loads(r['value']) for r in self.db.execute('SELECT * FROM meta')}
    def close(self):self.db.close()
    def object(self,id,full=True):
        row=self.db.execute('SELECT details FROM atlas_objects WHERE id=?',(id,)).fetchone()
        if row is None:raise KeyError('unknown Atlas ID: '+id)
        obj=json.loads(row[0]);refs=[dict(r) for r in self.db.execute('SELECT source_kind,source_id,ref,role FROM lineage WHERE object_id=? ORDER BY source_kind,source_id',(id,))]
        if full:obj['lineage']=refs;return obj
        compact=[r for r in refs if r['source_kind']!='V1']+[r for r in refs if r['source_kind']=='V1'][:3]
        return {**{k:obj[k] for k in ('id','family','type','status','evidence_status','machine_label','summary','representative','uncertainty')},'geometry_semantics':obj['geometry']['semantics'],'lineage_refs':compact,'lineage_total':len(refs),'full_lineage_query':'object --id '+id,'calibration_refs':obj['calibration_refs'],**{k:obj[k] for k in ('requires_local_observation','requires_world_write_authorization','planning_potential','flow_direction') if k in obj}}
    def distances(self,x,z):
        distances={}
        for row in self.db.execute('SELECT geometry_id,z0,z1,x0,x1 FROM geometry_runs'):
            d=math.hypot(max(row['x0']-x,0,x-row['x1']),max(row['z0']-z,0,z-row['z1']))
            gid=row['geometry_id'];distances[gid]=min(d,distances.get(gid,float('inf')))
        return {row['id']:distances[row['geometry_id']] for row in self.db.execute('SELECT id,geometry_id FROM atlas_objects ORDER BY id')}
    def near(self,x,z,radius):
        distances=self.distances(x,z)
        return [(id,d) for id,d in sorted(distances.items(),key=lambda item:(item[1],item[0])) if d<=radius]
    def coordinate(self,x,z):
        b=self.meta['world_coverage_bounds'];inside=b[0]<=x<=b[2] and b[1]<=z<=b[3]
        gx,gz=cell_of(x,z);row=self.db.execute('SELECT * FROM cell_index WHERE gx=? AND gz=?',(gx,gz)).fetchone() if inside else None
        distances=self.distances(x,z);membership=[self.object(id,False) for id,d in sorted(distances.items()) if d==0 and inside]
        near_regions=sorted(((id,d) for id,d in distances.items() if id.startswith('NGEO') and d>0),key=lambda t:(t[1],t[0]))[:3]
        sites=sorted(((id,d) for id,d in distances.items() if id.startswith('NSITE')),key=lambda t:(t[1],t[0]))[:1]
        nearby=[dict(self.object(id,False),distance_blocks=round(d,6)) for id,d in sorted(distances.items(),key=lambda t:(t[1],t[0])) if id.startswith(('NHYD','NFEAT')) and 0<d<=512]
        return {'coordinate':{'x':x,'z':z},'coverage':'INSIDE_SAMPLED_WORLD' if inside else 'OUTSIDE_SAMPLED_WORLD','cell_index':dict(row) if row else None,'memberships':membership,'nearby_NGEO':[dict(self.object(id,False),distance_blocks=round(d,6)) for id,d in near_regions],'nearby_water_and_features_512':nearby,'nearest_NSITE':[dict(self.object(id,False),distance_blocks=round(d,6)) for id,d in sites],'membership_warning':'64-block regional membership is approximate; exact local masks and observation points have separate semantics. Nearby is not containment. Outside-world nearest objects do not establish coverage.'}
    def neighbors(self,id):
        self.object(id)
        relations=[dict(r) for r in self.db.execute('SELECT * FROM relations WHERE source=? OR target=? ORDER BY source,target,kind',(id,id))]
        for r in relations:r['evidence']=json.loads(r['evidence'])
        ids=sorted({r['target'] if r['source']==id else r['source'] for r in relations})
        return {'id':id,'relations':relations,'objects':[self.object(x,False) for x in ids]}
    def search(self,family=None,type=None,evidence_status=None):
        clauses=[];args=[]
        for key,value in [('family',family),('type',type),('evidence_status',evidence_status)]:
            if value is not None:clauses.append(key+'=?');args.append(value)
        sql='SELECT id FROM atlas_objects'+(' WHERE '+' AND '.join(clauses) if clauses else '')+' ORDER BY id'
        return [self.object(r[0],False) for r in self.db.execute(sql,args)]
    def context(self,x,z,radius):
        selected=self.near(x,z,radius);ids={id for id,d in selected}
        objects=[dict(self.object(id,False),distance_blocks=round(d,6)) for id,d in selected]
        relations=[]
        for r in self.db.execute('SELECT * FROM relations ORDER BY source,target,kind'):
            if r['source'] in ids and r['target'] in ids:relations.append(dict(r, evidence=json.loads(r['evidence'])))
        return {'center':{'x':x,'z':z},'radius_blocks':radius,'selection':'minimum Euclidean distance to actual indexed member rectangles/points, not bbox or centroid','coordinate_context':self.coordinate(x,z),'objects_within_radius':objects,'relations_within_radius':relations,'constraints':self.meta['global_warnings'],'calibration':[json.loads(r[0]) for r in self.db.execute('SELECT details FROM calibration ORDER BY id')],'world_write_authorized':False,'design_or_canon_generated':False}
