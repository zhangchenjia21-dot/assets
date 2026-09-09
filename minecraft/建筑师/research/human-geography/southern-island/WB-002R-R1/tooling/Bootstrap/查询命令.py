import sys,json,argparse
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L1_器件层.区域查询器 import ProfileReader
p=argparse.ArgumentParser();p.add_argument('command',choices=['coordinate','zone','low-relief','context','hypotheses']);p.add_argument('--x',type=int);p.add_argument('--z',type=int);p.add_argument('--radius',type=int,default=64);p.add_argument('--id');args=p.parse_args()
try:
    if args.radius<0:raise ValueError('radius must be nonnegative')
    if args.command in ('coordinate','low-relief','context') and (args.x is None or args.z is None):raise ValueError('x,z required')
    if args.command=='zone' and not args.id:raise ValueError('id required')
    reader=ProfileReader(Path(__file__).resolve().parents[2]/'raw-or-queryable/regional-profile.sqlite')
    try:print(json.dumps(reader.query(args.command,vars(args)),ensure_ascii=False,sort_keys=True))
    finally:reader.close()
except (ValueError,KeyError) as e:
    print(json.dumps({'error':str(e)},ensure_ascii=False));sys.exit(2)
