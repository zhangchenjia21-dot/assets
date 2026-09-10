"""先以冻结R1格网确定样本，再持锁读取144根三维柱；全trace仅存本地。"""
import json
from collections import Counter
from contextlib import ExitStack
import numpy as np
from L0_公理层.基底契约 import BOUNDS,domains,ore_kind
from L1_器件层.缓存读取器 import load
from L1_器件层.矿物柱读取器 import ColumnReader
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json,digest
from L2_流程层.源复用流程 import roots
def sample(out,cache,world):
    assert not (cache/'mineral-columns.json').exists(),'已有采样，不得覆盖'
    a,m,_,_=load(out.parent/'WB-002R-R1');dd=domains(a,m);rng=np.random.default_rng(3003);plan=[]
    grid=(a['x']%64==32)&(a['z']%64==32)
    for domain,mask in dd.items():
        indices=np.flatnonzero(mask&grid);indices=indices[np.lexsort((a['x'].ravel()[indices],a['z'].ravel()[indices],a['exposed_y'].ravel()[indices]))]
        for j,stratum in enumerate(np.array_split(indices,3)):
            for idx in sorted(rng.choice(stratum,min(16,len(stratum)),replace=False).tolist()):
                plan.append({'id':f'S-{len(plan)+1:03d}','domain':domain,'stratum':j,'x':int(a['x'].ravel()[idx]),'z':int(a['z'].ravel()[idx]),'surface_y':int(a['exposed_y'].ravel()[idx])})
    write_json(out/'review/sampling-design.json',{'seed':3003,'method':'64-block lattice at x,z mod64=32; each domain split into three equally sized elevation-ranked lattice strata; 16 sites per stratum without replacement','sites':plan,'vertical_scope':'every Y from -60 through R1 exposed surface inclusive; same absolute depth bands compared separately','no_extrapolation':'stratified site counts are not regional ore density estimates'})
    rr=roots(out,world);baseline=json.loads((cache/'source-before.json').read_text(encoding='utf-8'));traces=[];witnesses=[]
    with ExitStack() as stack:
        for p in rr.values():stack.enter_context(ReadGuard(p))
        assert {n:fingerprint(p) for n,p in rr.items()}==baseline
        reader=ColumnReader(world)
        for site in plan:
            blocks=reader.read(site['x'],site['z'],site['surface_y']);region=f'dimensions/minecraft/overworld/region/r.{site["x"]//512}.{site["z"]//512}.mca'
            traces.append(dict(site,first_y=-60,blocks=blocks,region=region,region_sha256=baseline['world'][region]['sha256']))
            if int(site['id'][2:])%8==1:
                witnesses.append(dict(site,region=region,region_sha256=baseline['world'][region]['sha256'],sampled_blocks=len(blocks),mineral_counts=dict(Counter(k for n in blocks if (k:=ore_kind(n)))),near_surface_top16=blocks[-16:],evidence='direct sampled column, scalar/vector match'))
        assert {n:fingerprint(p) for n,p in rr.items()}==baseline
        write_json(out/'validation/targeted-read.json',{'status':'PASS','sample_columns':len(plan),'chunks':len(reader.cache),'scalar_vector_comparisons':reader.checked,'source_unchanged':True,'world_writes':0,'whole_region_rescan':False})
    write_json(cache/'mineral-columns.json',traces)
    (out/'review/stratified-witnesses.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n' for v in witnesses),encoding='utf-8',newline='\n')
    print('targeted sample PASS',len(plan),reader.checked,flush=True)
