import hashlib,json,sqlite3
import numpy as np
from L1_器件层.源快照保护器 import write_json

def encode(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def open_store(path):
    db=sqlite3.connect(path)
    db.executescript('''
    PRAGMA user_version=1;
    CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE atlas_objects(id TEXT PRIMARY KEY,family TEXT,type TEXT,status TEXT CHECK(status='PROPOSED'),evidence_status TEXT,machine_label TEXT,geometry_id TEXT,details TEXT);
    CREATE TABLE geometry_runs(geometry_id TEXT,z0 INTEGER,z1 INTEGER,x0 INTEGER,x1 INTEGER,PRIMARY KEY(geometry_id,z0,x0));
    CREATE INDEX geometry_point ON geometry_runs(z0,z1,x0,x1);
    CREATE TABLE atlas_members(object_id TEXT,gx INTEGER,gz INTEGER,role TEXT,PRIMARY KEY(object_id,gx,gz));
    CREATE INDEX member_cell ON atlas_members(gx,gz);
    CREATE TABLE cell_index(gx INTEGER,gz INTEGER,sample_x INTEGER,sample_z INTEGER,elevation REAL,water_fraction REAL,v1_terrain TEXT,v1_geo TEXT,unresolved_land INTEGER,unresolved_water INTEGER,PRIMARY KEY(gx,gz));
    CREATE TABLE lineage(object_id TEXT,source_kind TEXT,source_id TEXT,ref TEXT,role TEXT,PRIMARY KEY(object_id,source_kind,source_id));
    CREATE TABLE relations(source TEXT,target TEXT,kind TEXT,evidence_status TEXT,evidence TEXT,PRIMARY KEY(source,target,kind));
    CREATE TABLE uncertainty(object_id TEXT PRIMARY KEY,boundary TEXT,topology TEXT,semantic TEXT,requires_refinement INTEGER);
    CREATE TABLE calibration(id TEXT PRIMARY KEY,details TEXT);
    CREATE TABLE identity_registry(id TEXT PRIMARY KEY,stable_key TEXT UNIQUE,geometry_signature TEXT,state TEXT);
    ''')
    return db

def mask_runs(mask,origin,step=1,clip=None):
    """RLE保存实际mask成员而非bbox；采样mask的每点覆盖step方格，精度在geometry语义中保留。"""
    result=[]
    for j,row in enumerate(mask):
        starts=np.flatnonzero(np.diff(np.r_[False,row,False].astype(int))==1)
        ends=np.flatnonzero(np.diff(np.r_[False,row,False].astype(int))==-1)
        for s,e in zip(starts,ends):
            x0=origin[0]+int(s)*step;x1=origin[0]+int(e)*step-1;z0=origin[1]+j*step;z1=z0+step-1
            if clip:x0=max(x0,clip[0]);z0=max(z0,clip[1]);x1=min(x1,clip[2]);z1=min(z1,clip[3])
            if x0<=x1 and z0<=z1:result.append((z0,z1,x0,x1))
    return result

def geometry_summary(runs):
    area=sum((z1-z0+1)*(x1-x0+1) for z0,z1,x0,x1 in runs)
    return {'bounds':[min(r[2] for r in runs),min(r[0] for r in runs),max(r[3] for r in runs),max(r[1] for r in runs)],'indexed_area_blocks2':area,'run_count':len(runs)}

class IdentityRegistry:
    """固定ledger保留ID；形状变化必须显式匹配/拆并裁定，禁止重新排序便全体重编号。"""
    def __init__(self,path):
        self.path=path;self.previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {};self.current={}
    def bind(self,id,key,runs):
        sig=hashlib.sha256(encode(runs).encode()).hexdigest()
        old=self.previous.get(id)
        if old and (old['stable_key']!=key or old['geometry_signature']!=sig):raise ValueError('ID/形状已改变，需显式lineage匹配决策: '+id)
        if any(v['stable_key']==key and k!=id for k,v in {**self.previous,**self.current}.items()):raise ValueError('stable key不能分配第二ID')
        if old and old['state']=='RETIRED':raise ValueError('禁止回收历史ID')
        self.current[id]={'stable_key':key,'geometry_signature':sig,'state':'PROPOSED'}
    def finish(self,db):
        entries={**self.previous,**self.current}
        for id,entry in sorted(entries.items()):
            if id not in self.current:entry=dict(entry,state='RETIRED');entries[id]=entry
            db.execute('INSERT INTO identity_registry VALUES (?,?,?,?)',(id,entry['stable_key'],entry['geometry_signature'],entry['state']))
        write_json(self.path,entries)
