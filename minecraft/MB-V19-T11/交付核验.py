"""核对零施工重载与审计文件；不修改世界。"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;E=R/'证据'
def j(n):return json.loads((E/n).read_text(encoding='utf8'))
b=j('09-Restraint-实存.json');a=j('reload-实存.json');r=j('reload-执行.json')
assert a['palette']==b['palette']
assert (E/'reload.u16').read_bytes()==(E/'09-Restraint.u16').read_bytes()
assert r['changed_blocks']==0 and r['save_completed'] and r['shutdown_verified']
assert a['name']=='MB-V19-T11-京町家' and a['generation']['generate_structures']==0
assert a['generation']['dimensions']['minecraft:overworld']['generator']['type']=='minecraft:flat'
assert j('reload-阶段保护.json')['critical_core_state_changes']==0
views=j('观察点.json')
for v in views:
 for stage in ['04-Base','09-Restraint']:assert (E/f"{stage}-{v['name']}.png").is_file()
out={'scope_state':'FINISHED','regression_verdict':'NOT_ASSIGNED','world_name':a['name'],'superflat':True,'structures':False,'reload_changed_blocks':0,'reload_same_palette':True,'reload_same_sample_bytes':True,'sample_origin':[0,10,0],'sample_shape_yzx':[36,96,56],'sample_sha256':a['sha256'],'same_camera_pairs':len(views),'native_client_verified':False,'finishing_gate':'see Finishing Completion Gate.md','history':['DESIGN_READY','CORE_BUILDING','SPATIAL_COMPLETE after 04-Base','FINISHING 05-09','FINISHED after Finishing Completion Gate'],'skill_blob':'5420c7cbbca25199e81ec1204dbc928b70abf73c'}
(E/'交付核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print('reload identical; 19 view pairs; scope FINISHED, no regression verdict')
