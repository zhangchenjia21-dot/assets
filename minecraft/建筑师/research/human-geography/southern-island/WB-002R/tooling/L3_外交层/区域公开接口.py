from pathlib import Path
def read_world(output,world,extract=False):
    """只读当前建筑师存档并在指定WB-002R写研究证据；锁/身份/指纹失败抛错，不启动游戏。"""
    from L2_流程层.区域读取流程 import audit
    out=Path(output).resolve();world=Path(world).resolve()
    if out.name!='WB-002R' or world==out or world in out.parents:raise ValueError('output scope mismatch')
    audit(out,world,extract)

def derive_profile(output):
    """只从本轮observed.sqlite推导指标/数值分区候选；不访问世界，不自动裁定自然区。"""
    from L2_流程层.区域派生流程 import derive
    derive(Path(output).resolve())

def render_profile(output):
    """从本任务只读数据生成有坐标方向的离线派生地图；不访问世界。"""
    from L1_器件层.区域地图生成器 import render
    render(Path(output).resolve())

def build_profile(output):
    """固定本轮观测与解释汇编SQLite；只写WB-002R，不改变既有Atlas。"""
    from L2_流程层.区域汇编流程 import build
    build(Path(output).resolve())

def query_profile(output,command,**args):
    """标准库只读查询；整数坐标，非负radius；未知ID报错，ROI外明确OUTSIDE。"""
    from L1_器件层.区域查询器 import ProfileReader
    from L0_公理层.区域契约 import SCHEMA
    if any(not isinstance(v,int) or isinstance(v,bool) for k,v in args.items() if k in ('x','z','radius')) or args.get('radius',0)<0:raise ValueError('integer coordinates and nonnegative radius required')
    reader=ProfileReader(Path(output).resolve()/'raw-or-queryable/regional-profile.sqlite')
    import json
    try:return {'schema':SCHEMA,'status':'RESEARCH_CANDIDATE','live_world_checked':False,'snapshot':json.loads(reader.db.execute('SELECT value FROM meta WHERE key=?',('snapshot',)).fetchone()[0]),'result':reader.query(command,args)}
    finally:reader.close()

def analyze_relations(output):
    """由本轮快照生成水陆路径见证及阈值敏感性；不访问实时世界或创造用途。"""
    from L2_流程层.区域关系核验流程 import analyze
    analyze(Path(output).resolve())
