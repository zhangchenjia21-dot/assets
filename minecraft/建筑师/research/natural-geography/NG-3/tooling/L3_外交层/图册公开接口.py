from pathlib import Path

def check_sources(output,world,final=False):
    """验证现有存档freshness和证据不变性，输出仅限NG-3；失败抛出且不启动游戏。"""
    from L2_流程层.快照核验流程 import gate
    output=Path(output).resolve();world=Path(world).resolve()
    if output.name!='NG-3' or output==world or world in output.parents:raise ValueError('输出边界无效')
    gate(output,world,final)

def prepare_inputs(output):
    """解压只读输入的工作副本；不运行或改写历史调查脚本。"""
    from L2_流程层.快照核验流程 import prepare
    prepare(Path(output).resolve())

def propose_segments(output):
    """只生成数值候选与审阅地图；结果需显式语义决策后才能进入Proposed Atlas。"""
    from L2_流程层.候选归并流程 import candidates
    candidates(Path(output).resolve())

def build_atlas(output):
    """将已审阅的分段/语义决策汇编为PROPOSED SQLite；ID漂移拒绝执行，不访问世界。"""
    from L2_流程层.图册汇编流程 import build
    build(Path(output).resolve())

def query_atlas(output,command,**args):
    """标准库只读查询；坐标/半径为整数，半径非负；未知ID抛KeyError，未覆盖坐标显式返回OUTSIDE。"""
    from L2_流程层.图册查询流程 import query
    for name in ('x','z','radius'):
        if name in args and (isinstance(args[name],bool) or not isinstance(args[name],int)):raise ValueError(name+' must be an integer')
    if args.get('radius',0)<0:raise ValueError('radius must be nonnegative')
    if command not in ('coordinate','object','neighbors','search','context'):raise ValueError('unknown query command')
    return query(Path(output).resolve()/'raw-or-queryable/atlas.sqlite',command,**args)

def render_atlas(output):
    """从Atlas只读库重建派生地图；地图不覆盖源数据或证据状态。"""
    from L1_器件层.图册地图生成器 import render_maps
    render_maps(Path(output).resolve())
