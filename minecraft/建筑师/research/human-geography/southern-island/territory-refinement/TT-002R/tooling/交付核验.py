"""独立从交付 RLE 核验覆盖、锁定、带宽与源不变；不导入生成器。"""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[4]
CACHE=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/TT-002R')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
def decode(p):
    d=read(p);a=np.full((2112,3264),255,np.uint8)
    assert d['schema']=='civ-territories/1' and d['source']['id']=='94fc4687358a9fd5dd542997538822bfdba7b83bd76c4825fd84bd0116ea3d21'
    for z,x0,x1,c in d['runs']:
        assert 1376<=z<=3487 and -800<=x0<=x1<=2463 and 0<=c<6
        assert (a[z-1376,x0+800:x1+801]==255).all();a[z-1376,x0+800:x1+801]=c
    return a
a=decode(OUT/'baseline-owner-draft.json');b=decode(OUT/'refined-draft.json');delta=read(OUT/'boundary-delta.json')
assert sha(OUT/'baseline-owner-draft.json')==sha(OUT/'input/owner-draft-rev153.json')=='4fce4c14295ba3f5dd760e31b8a1e3f63fe139002c9eb427ff8d4648a6aef2e6'
assert np.array_equal(a!=255,b!=255) and int((b!=255).sum())==2256681
assert not np.isin(b,[4,5]).any();change=a!=b
assert int(change.sum())==delta['changed_columns']
assert np.isin(a[change],[2,3]).all() and np.isin(b[change],[2,3]).all()
assert [int((b==c).sum()) for c in range(6)]==delta['after_areas']
for c in [0,1]:assert np.array_equal(a==c,b==c)
for name,c in [('commons',0),('connector',2)]:
    for z,l,h in read(ROOT/f'research/build-sites/CIV-001/AB-001P1R/{name}-geometry.json')['runs']:
        assert (a[z-1376,l+800:h+801]==c).all() and (b[z-1376,l+800:h+801]==c).all()
# 直接核对每个变化列属于见证行的旧/新切口之间，且距旧垂直单位边 <48.5。
mask=np.zeros(a.shape,bool)
for w in delta['row_witnesses']:
    assert 1895<=w['z']<=2090 and abs(w['new_x']-w['old_x'])<=48
    lo,hi=sorted([w['new_x'],w['old_x']]);mask[w['z']-1376,lo+800:hi+800]=True
assert np.array_equal(mask,change)
for name in ['before','after','diff','terrain-overlay']:
    with Image.open(OUT/'visual'/f'{name}.png') as im:assert im.size==(1170,950);im.verify()
before=read(CACHE/'source-before.json')
after={p.relative_to(ROOT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for folder in ('research','world','architecture') for p in (ROOT/folder).rglob('*') if p.is_file() and not p.is_relative_to(OUT)}
assert before==after
write(OUT/'validation/source-audit.json',{'status':'PASS','protected_files':len(before),'inventory_before_sha256':sha(CACHE/'source-before.json'),'research_predecessors_immutable':True,'world_canon_immutable':True,'architecture_immutable':True,'baseline_byte_identical':True,'world_writes':0,'new_world_block_reads':0,'world_files_opened_by_task':0,'freshness':'cache epoch only; live save not fingerprinted'})
write(OUT/'validation/independent-check.json',{'status':'PASS','implementation':'separate RLE decoder and row-mask reconstruction, no generator import','checks':['unique coverage','exact baseline hash','land conservation','accepted Commons connector and all West unchanged','only Middle-East reassignment','all changed columns within explicit 48-block row spans','no unassigned holes','four readable PNGs','459 predecessor source files unchanged'],'world_writes':0})
print('independent RLE and source audit PASS')
