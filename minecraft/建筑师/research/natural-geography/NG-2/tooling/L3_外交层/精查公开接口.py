from pathlib import Path
from L2_流程层.局部精查流程 import scan,views,verify_all
from L2_流程层.派生证据流程 import derive
from L2_流程层.交付整理流程 import finalize

def survey(world,output,targets=None):
    """只读既有世界；输出只能是NG-2且必须与源世界/V1分离，失败抛出，不能加载游戏。"""
    world=Path(world).resolve();output=Path(output).resolve()
    if output.name!='NG-2' or world==output or world in output.parents or output in world.parents:raise ValueError('非法输出边界')
    scan(world,output,targets)

def rebuild_views(output):
    """从NG-2数据库重建派生图；读取V1历史SITE元数据，不修改V1，不访问世界。"""
    views(Path(output).resolve())

def audit(world,output):
    """对已采集NG-2补充独立源解码验证；要求源世界仍与首轮全文件指纹一致。"""
    verify_all(Path(world).resolve(),Path(output).resolve())

def derive_evidence(output):
    """从NG-2数据库重算指标与细节图，不访问源存档，不自动作地貌语义判决。"""
    derive(Path(output).resolve())

def finalize_evidence(output):
    """将已编写的解释和可追溯事实汇编入库并验证；不访问世界、不改变V1。"""
    finalize(Path(output).resolve())
