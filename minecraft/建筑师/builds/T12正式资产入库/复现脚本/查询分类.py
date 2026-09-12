from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;module=R.parent/'AI-Blueprints/建筑理解';sys.path[:0]=[str(module),str(module/'第三方')]
from L3_外交层.建筑理解公开接口 import read_reference_classification
r=read_reference_classification('REF-0123');assert r['classification_v2']['primary_use']=='mixed_use'
(R/'V2查询验证.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print('REF-0123 V2 mixed_use resolved')
