"""仅以整数柱/runs查询；bbox只用于摘要，不作实际成员判断。"""
import json,sqlite3,math
class ProfileReader:
    def __init__(self,path):
        self.db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True);self.db.row_factory=sqlite3.Row
    def close(self):self.db.close()
    def entity(self,id):
        row=self.db.execute('SELECT json FROM objects WHERE id=?',(id,)).fetchone()
        if row is None:raise KeyError('unknown research object '+id)
        return json.loads(row[0])
    def near(self,x,z,radius,family=None):
        distances={}
        for id,zz,x0,x1 in self.db.execute('SELECT object_id,z,x0,x1 FROM geometry_runs ORDER BY object_id,z,x0'):
            if family and not id.startswith(family):continue
            d=math.hypot(max(x0-x,0,x-x1),zz-z)
            distances[id]=min(d,distances.get(id,float('inf')))
        return [dict(self.entity(id),distance_blocks=round(d,6)) for id,d in sorted(distances.items(),key=lambda p:(p[1],p[0])) if d<=radius]
    def coordinate(self,x,z):
        row=self.db.execute('SELECT s.*,m.* FROM samples s JOIN metrics m USING(z,x) WHERE s.z=? AND s.x=?',(z,x)).fetchone()
        if row is None:return {'coverage':'OUTSIDE_STUDY_AREA','x':x,'z':z,'world_membership':'not inferred'}
        result=dict(row)
        result['filtered_material_category']=self.db.execute('SELECT category FROM material_categories WHERE state_id=?',(result['exposed_state'],)).fetchone()[0]
        for key in ('biome','filtered_biome'):result[key]=self.db.execute('SELECT name FROM biomes WHERE id=?',(result[key],)).fetchone()[0]
        for key in ('surface_state','exposed_state','water_state'):result[key]=json.loads(self.db.execute('SELECT json FROM states WHERE id=?',(result[key],)).fetchone()[0])
        result['source_chunk']=dict(self.db.execute('SELECT * FROM chunks WHERE cx=? AND cz=?',(x//16,z//16)).fetchone())
        result['source_region']=dict(self.db.execute('SELECT * FROM source_regions WHERE region=?',(result['source_chunk']['region'],)).fetchone())
        return {'coverage':'INSIDE_STUDY_AREA','point':result,'nearby_low_relief':self.near(x,z,128,'FLAT')[:5]+self.near(x,z,128,'GENTLE')[:5],'nearby_water':self.near(x,z,128,'WATER')[:5],'semantics':'nearby by actual indexed columns; no build suitability or water navigation claim'}
    def query(self,command,args):
        if command=='coordinate':return self.coordinate(args['x'],args['z'])
        if command=='zone':
            if not args['id'].startswith('SIRZ-'):raise ValueError('zone requires SIRZ ID')
            return self.entity(args['id'])
        if command=='low-relief':return self.near(args['x'],args['z'],args['radius'],'FLAT')+self.near(args['x'],args['z'],args['radius'],'GENTLE')
        if command=='hypotheses':return json.loads(self.db.execute('SELECT json FROM profiles WHERE name=?',('owner-hypothesis-evaluation',)).fetchone()[0])
        if command=='context':return {'coordinate':self.coordinate(args['x'],args['z']),'nearby_objects':self.near(args['x'],args['z'],args['radius']),'hypotheses':self.query('hypotheses',{}),'world_write_authorized':False,'civilization_or_build_generated':False}
        raise ValueError('unknown command')
