import argparse,sys,json
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tooling'))
sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
from L3_外交层.图册公开接口 import check_sources,prepare_inputs,propose_segments,build_atlas,query_atlas,render_atlas
if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    for name in ('gate','seal'):
        q=sub.add_parser(name);q.add_argument('--world',required=True)
    for name in ('prepare','segments','build','views'):sub.add_parser(name)
    for name in ('coordinate','context'):
        q=sub.add_parser(name);q.add_argument('--x',type=int,required=True);q.add_argument('--z',type=int,required=True)
        if name=='context':q.add_argument('--radius',type=int,required=True)
    for name in ('object','neighbors'):
        q=sub.add_parser(name);q.add_argument('--id',required=True)
    q=sub.add_parser('search');q.add_argument('--family',choices=['NGEO','NHYD','NFEAT','NSITE']);q.add_argument('--type');q.add_argument('--evidence-status',choices=['SUPPORTED','PROVISIONAL','UNRESOLVED'])
    a=vars(p.parse_args());command=a.pop('command')
    try:
        if command=='prepare':prepare_inputs(ROOT)
        elif command=='segments':propose_segments(ROOT)
        elif command=='build':build_atlas(ROOT)
        elif command=='views':render_atlas(ROOT)
        elif command in ('gate','seal'):check_sources(ROOT,a['world'],command=='seal')
        else:print(json.dumps(query_atlas(ROOT,command,**a),ensure_ascii=True,sort_keys=True,separators=(',',':')))
    except (ValueError,KeyError) as e:
        print(json.dumps({'schema_version':'natural-atlas/1.0','error':str(e)},ensure_ascii=True,sort_keys=True));sys.exit(2)
