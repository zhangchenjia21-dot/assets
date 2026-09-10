"""独立按SQLite行聚合材料，核对阳性见证与已保存raw，不重新扫描世界。"""
import sys,json,sqlite3
from pathlib import Path
from collections import Counter
import numpy as np
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L1_器件层.源快照保护器 import write_json
out=Path(__file__).resolve().parents[2];old=out.parent/'WB-002R-R1'
db=sqlite3.connect((old/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
with np.load(old/'raw-or-queryable/derived.npz') as f:west=f['west'];east=f['east']
names={k:json.loads(v)['Name'] for k,v in db.execute('SELECT * FROM states')};counts={k:Counter() for k in ('W','M','E')}
for x,z,y,s in db.execute('SELECT x,z,exposed_y,exposed_state FROM samples'):
    domain='W' if west[z-1376,x+800] else ('M' if east[z-1376,x+800] and x<640 and y<=120 else ('E' if east[z-1376,x+800] and x>=640 and y>=140 else None))
    if domain:counts[domain][names[s]]+=1
materials=json.loads((out/'profile/material-profile.json').read_text(encoding='utf-8'))['domains'];sub=json.loads((out/'profile/substrate-summary.json').read_text(encoding='utf-8'))['domains']
for k in counts:assert dict(counts[k])==materials[k]['exposed_block_columns'];assert sum(counts[k].values())==sub[k]['columns']
raw=json.loads(Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/WB-003R/mineral-columns.json').read_text(encoding='utf-8'));sites={s['id']:s for s in raw}
mineral=json.loads((out/'profile/mineral-sample-profile.json').read_text(encoding='utf-8'));n=0
for w in mineral['positive_witnesses']:
    s=sites[w['sample_id']];assert (w['x'],w['z'],w['region_sha256'])==(s['x'],s['z'],s['region_sha256']);assert s['blocks'][w['y']+60]==w['block'];n+=1
for line in (out/'review/stratified-witnesses.jsonl').read_text(encoding='utf-8').splitlines():
    w=json.loads(line);s=sites[w['id']];assert w['near_surface_top16']==s['blocks'][-16:]
assert sum(len(s['blocks']) for s in raw)==25176
cross=json.loads((out/'profile/crossing-profile.json').read_text(encoding='utf-8'));geo=json.loads((out/'validation/geometry-sampling.json').read_text(encoding='utf-8'))
for p,v in zip(cross['candidates'],geo['crossing_exact_supercover']):assert p['exact_closed_cell_water_only']==v['closed_cell_supercover_water_only'];assert sorted(p['intersected_dry_cells'])==sorted(v['dry_cells'])
write_json(out/'validation/aggregate-witness-check.json',{'status':'PASS','independent_sql_material_domains':3,'material_count_conservation':True,'positive_mineral_witnesses':n,'stratified_top16_witnesses':18,'raw_sample_blocks':25176,'independent_segment_algorithms_agree':True,'known_sampled_vs_exact_discrepancy':'X-02 retained and rejected, not hidden'})
print('aggregate and witnesses PASS',flush=True)
