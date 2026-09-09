"""依赖注入入口：使用已安装 nbtlib 2.0.4，不加载建筑模块内部代码。"""
import argparse
import sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT.parents[1]/'AI-Blueprints'/'参考入库'/'第三方'))
from L3_外交层.自然调查接口 import survey,rebuild_views

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['scan','views'])
    parser.add_argument('--world')
    args=parser.parse_args()
    if args.command=='views':rebuild_views(ROOT)
    elif args.world:survey(args.world,ROOT)
    else:parser.error('scan requires --world')
