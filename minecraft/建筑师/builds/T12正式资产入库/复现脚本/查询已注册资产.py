"""通过既有 L3 精确 REF 查询，拒绝以直接读 metadata 代替可发现性验证。"""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;module=R.parent/'AI-Blueprints/参考入库';sys.path[:0]=[str(module),str(module/'第三方')]
from L3_外交层.参考库公开接口 import resolve_reference_blueprint,query_references
r=resolve_reference_blueprint('REF-0123');q=query_references('REF-0123');assert q['count']==1 and q['results'][0]['id']=='REF-0123'
(R/'REF查询验证.json').write_text(json.dumps({'resolve':r,'query':q},ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'id':r['reference_id'],'query_count':q['count']}))
