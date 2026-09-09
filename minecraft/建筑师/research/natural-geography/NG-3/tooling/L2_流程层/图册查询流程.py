from L0_公理层.图册契约 import SCHEMA
from L1_器件层.图册查询器 import AtlasReader

def query(path,command,**args):
    """固定快照下输出确定JSON对象；只读关闭连接，不把freshness as-of伪装成实时验证。"""
    reader=AtlasReader(path)
    try:
        handlers={'coordinate':reader.coordinate,'object':reader.object,'neighbors':reader.neighbors,'search':reader.search,'context':reader.context}
        result=handlers[command](**args)
        return {'schema_version':SCHEMA,'atlas_status':'PROPOSED','snapshot':{'geography_snapshot_status':reader.meta['geography_snapshot_status'],'checked_at':reader.meta['freshness_checked_at'],'live_world_checked_by_this_query':False},'command':command,'result':result}
    finally:reader.close()
