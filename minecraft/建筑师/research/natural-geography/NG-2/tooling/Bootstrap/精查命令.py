import argparse
import sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tooling'))
# 优先使用调用环境依赖；当前宿主已有稳定nbtlib分发，不复制或改写V1。
sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
from L3_外交层.精查公开接口 import survey,rebuild_views,audit,derive_evidence,finalize_evidence

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['scan','views','audit','derive','finalize']);p.add_argument('--world');p.add_argument('--targets',nargs='*');args=p.parse_args()
    if args.command=='views':rebuild_views(ROOT)
    elif args.command=='derive':derive_evidence(ROOT)
    elif args.command=='finalize':finalize_evidence(ROOT)
    elif args.world and args.command=='audit':audit(args.world,ROOT)
    elif args.world:survey(args.world,ROOT,args.targets)
    else:p.error('scan requires existing --world')
