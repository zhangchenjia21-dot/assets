"""复核世界隔离、重载和有限修复结果，保留真实移动 UNVERIFIED。"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;E=R/'证据'
def j(f):return json.loads((E/f).read_text(encoding='utf8'))
src=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V19-T11-京町家');before=j('来源世界文件哈希.json')
now={str(p.relative_to(src)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in src.rglob('*') if p.is_file()};assert before==now
left=j('01-Repair-实存.json');right=j('reload-实存.json');run=j('reload-执行.json')
assert left['palette']==right['palette'] and (E/'01-Repair.u16').read_bytes()==(E/'reload.u16').read_bytes()
assert run['changed_blocks']==0 and run['save_completed'] and run['shutdown_verified']
d=j('reload-物理扫描.json');checks=j('reload-关联完整性.json')
assert not d['closure_candidates'] and not d['small_support_review']
assert all(r['static_envelope_clear'] for r in d['routes'])
assert all(r['static_envelope_clear'] or r.get('excluded_from_through_route_gate') for r in d['stair_lanes'])
assert not checks['unexpected_differences'] and all(r['review']!='UNEXPLAINED' for r in checks['unrooted_native_collision_nodes'])
assert checks['roof_states_unchanged'] and checks['stair_states_unchanged'] and checks['water_states_unchanged']
skill=(R/'研究/技能原文-SKILL.md').read_bytes();blob=hashlib.sha1(b'blob '+str(len(skill)).encode()+b'\0'+skill).hexdigest();assert blob=='aa235db5bccabe7e2fa16714cf95867ba991624d'
out={'world':right['world'],'world_name':right['name'],'skill_version':'v1.10','skill_blob':blob,'source_file_count':len(now),'source_files_unchanged_including_lock':True,'source_manifest_sha256':hashlib.sha256(json.dumps(now,sort_keys=True).encode()).hexdigest(),'repair_cells':checks['actual_changed_cells'],'reload_same_sample_bytes_and_palette':True,'reload_sample_sha256':right['sha256'],'construction_closure_clearance_gate':'UNVERIFIED','known_closure_failures_remaining':0,'known_static_envelope_failures_remaining':0,'actual_player_movement':'UNVERIFIED','scope_state':'FINISHED with explicit physical UNVERIFIED boundary','regression_verdict':'NOT_ASSIGNED','asset_registration':False}
(E/'交付核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
q=json.loads((R/'完整配置资格验证/qualification.json').read_text(encoding='utf8'));(E/'世界与运行环境资格.json').write_text(json.dumps({'source_world':str(src),'test_world':q['world_path'],'qualification':q['qualification'],'qualification_status':q['status'],'source_unchanged':True,'initial_minimal_profile_rejected':'QUALIFICATION_METADATA_CHANGED; enabled datapacks missing; no repair ran in failed qualification clone','mod_profile':'full T11 source instance mods/config copied to isolated instance, compared and qualified; actual files are not archived'},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=True))
