"""Atlas为PROPOSED派生索引；坐标为闭区间，负坐标使用数学floor。"""
SCHEMA='natural-atlas/1.0'
ALGORITHM='ng3-consolidation/1.0'
BASE='166515fe12ac7f5edd2dd04bccefa49f4e8b0951'
FAMILIES=('NGEO','NHYD','NFEAT','NSITE')
EVIDENCE=('SUPPORTED','PROVISIONAL','UNRESOLVED')
CELL_SIZE=64

def cell_of(x,z):
    return x//CELL_SIZE,z//CELL_SIZE
