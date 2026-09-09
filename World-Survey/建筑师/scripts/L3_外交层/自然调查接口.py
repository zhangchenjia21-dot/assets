from pathlib import Path
from L2_流程层.自然调查流程 import run,regenerate

def survey(world,output):
    """调查已存在的 4903 主世界，输出必须与世界分离；失败抛出，不加载 Minecraft。"""
    world=Path(world).resolve();output=Path(output).resolve()
    if world==output or world in output.parents or output in world.parents:
        raise ValueError('输出与世界目录不得嵌套')
    if not (world/'level.dat').is_file():raise ValueError('缺少已有 level.dat')
    run(world,output)

def rebuild_views(output):
    """仅从已有 SQLite 重建 JSONL、地图、短报告，不访问世界。"""
    regenerate(Path(output).resolve())
