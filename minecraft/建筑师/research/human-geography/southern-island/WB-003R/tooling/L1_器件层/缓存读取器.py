"""只读R1标准SQLite/NPZ交付，不导入历史工具内层或复制历史数据库。"""
import sqlite3,json
import numpy as np
from L0_公理层.基底契约 import BOUNDS
def load(old):
    db=sqlite3.connect((old/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
    names=[r[1] for r in db.execute('PRAGMA table_info(samples)')]
    rows=np.fromiter((v for r in db.execute('SELECT * FROM samples ORDER BY z,x') for v in r),dtype=np.int32).reshape(-1,len(names))
    shape=(BOUNDS[3]-BOUNDS[1]+1,BOUNDS[2]-BOUNDS[0]+1)
    a={n:np.ascontiguousarray(rows[:,i].reshape(shape)) for i,n in enumerate(names)}
    for k in ('leaf','trunk'):a[k]=np.full(shape,-1,np.int16)
    for x,z,leaf,trunk in db.execute('SELECT x,z,leaf,trunk FROM vegetation'):
        a['leaf'][z-BOUNDS[1],x-BOUNDS[0]]=leaf;a['trunk'][z-BOUNDS[1],x-BOUNDS[0]]=trunk
    states={i:json.loads(s) for i,s in db.execute('SELECT * FROM states')};biomes=dict(db.execute('SELECT * FROM biomes'));db.close()
    with np.load(old/'raw-or-queryable/derived.npz') as f:m={k:f[k] for k in ('west','east','land_component','water_component','terrain_class','slope8','step1','relief16','relief32','shoreline')}
    return a,m,states,biomes
def distribution(v):
    v=np.asarray(v);v=v[np.isfinite(v)]
    return dict(zip(('min','p10','median','p90','max'),map(float,np.percentile(v,[0,10,50,90,100])))) if len(v) else None
def distance(seed):
    """精确城市街区距离：不限于陆地，不等于可步行/取水路径。"""
    d=np.where(seed,0,100000).astype(np.int32)
    for axis in (0,1):
        shape=[1,1];shape[axis]=d.shape[axis];i=np.arange(d.shape[axis]).reshape(shape)
        forward=np.minimum.accumulate(d-i,axis=axis)+i
        backward=np.flip(np.minimum.accumulate(np.flip(d+i,axis=axis),axis=axis),axis=axis)-i
        d=np.minimum(forward,backward).astype(np.int32)
    return d
