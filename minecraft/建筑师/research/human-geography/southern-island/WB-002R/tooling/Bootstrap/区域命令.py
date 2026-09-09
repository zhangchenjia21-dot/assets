import sys,argparse,json
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tooling'))
sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
from L3_外交层.区域公开接口 import read_world,derive_profile,render_profile,build_profile,query_profile,analyze_relations
if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    for name in ('read','refresh','seal'):sub.add_parser(name).add_argument('--world',required=True)
    for name in ('derive','views','build','hypotheses','relations'):sub.add_parser(name)
    for name in ('coordinate','context','low-relief'):
        q=sub.add_parser(name);q.add_argument('--x',type=int,required=True);q.add_argument('--z',type=int,required=True)
        if name!='coordinate':q.add_argument('--radius',type=int,required=True)
    sub.add_parser('zone').add_argument('--id',required=True)
    a=vars(p.parse_args());command=a.pop('command')
    try:
        if command=='derive':derive_profile(ROOT)
        elif command=='views':render_profile(ROOT)
        elif command=='build':build_profile(ROOT)
        elif command=='relations':analyze_relations(ROOT)
        elif command in ('read','refresh','seal'):read_world(ROOT,a['world'],'refresh' if command=='refresh' else command=='read')
        else:print(json.dumps(query_profile(ROOT,command,**a),ensure_ascii=True,sort_keys=True,separators=(',',':')))
    except (ValueError,KeyError) as e:print(json.dumps({'error':str(e),'schema':'southern-island-profile/1.0'}));sys.exit(2)
