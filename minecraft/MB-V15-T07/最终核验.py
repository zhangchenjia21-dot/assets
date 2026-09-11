from pathlib import Path
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent;s='05-Water';m=json.loads((R/f'证据/{s}-实存元数据.json').read_text());actual=np.fromfile(R/f'证据/{s}-实存方块.u16',dtype='<u2').reshape(52,240,288);expected=np.load(R/f'方案-{s}.npz');E=expected['blocks']
def norm(s):
    if '[' not in s:return s
    a,b=s.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
allstates=sorted(set(map(norm,m['palette']))|set(map(norm,expected['palette'])));codes={s:i for i,s in enumerate(allstates)};ac=np.array([codes[norm(s)] for s in m['palette']])[actual];ec=np.array([codes[norm(s)] for s in expected['palette']])[E];bad=ac!=ec
# 全部方案占位（包括空气）对照，独立于执行器 samples；同时记录可检查外壳范围。
checks={}
for name,b in {'驿站外壳':[139,20,74,214,38,146],'水屋':[107,17,100,128,30,123],'工院':[137,20,161,150,27,181],'烘烤仓房':[116,20,181,133,28,197]}.items():
 x1,y1,z1,x2,y2,z2=b;checks[name]={'bounds':b,'difference_from_final_blueprint':int(bad[y1-12:y2-11,z1:z2+1,x1:x2+1].sum())}
out={'scope':[0,12,0,287,63,239],'compared_cells':int(bad.size),'mismatches':int(bad.sum()),'envelopes':checks,'note':'Exact final intent comparison does not by itself prove architectural quality; combine with perspectives, sections and route inspection.'}
(R/'证据/最终全域核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False))
