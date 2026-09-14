"""检查机械契约和主产物哈希；不把检查结果当作规划独立审核。

freeze显式单次执行，已存在封存则拒绝覆盖。verify只读，不改任何产物。
"""
from pathlib import Path
import argparse,hashlib,json,datetime
from PIL import Image
P=Path(__file__).resolve().parents[1]
def read(q):return json.loads(q.read_text('utf-8-sig'))
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def check():
    plan=read(P/'L0-POLITY-PLAN.json')
    assert plan['scale']=='POLITY_TERRITORY' and plan['world_write_authorization'] is False
    assert plan['context']['evolution_logic']=='EXISTING_EVOLUTION'
    flows={v['id'] for v in read(P/'flows-system.json')['flows']}
    roles={v['id'] for v in read(P/'settlement-hierarchy.json')['roles']}
    routes={v['id'] for v in read(P/'movement-access-skeleton.json')['relations']}
    caps={v['id'] for v in read(P/'capacity-scale.json')['capacities']}
    assert set(plan['flow_refs'])==flows and set(plan['role_refs'])==roles
    assert set(plan['movement_refs'])==routes and set(plan['capacity_refs'])==caps
    for r in read(P/'settlement-hierarchy.json')['roles']:
        assert r['capacity'] in caps and set(r['flows'])<=flows and set(r['routes'])<=routes
    for r in read(P/'movement-access-skeleton.json')['relations']:assert set(r['flow_refs'])<=flows
    for name in ['WEST','MIDDLE','EAST']:
        q=read(P/f'handoff/L1-{name}.json')
        assert q['parent_plan_revision']==plan['revision']
        assert q['child_scale']=='REGIONAL_SYSTEM' and q['world_write_authorization'] is False
        assert q['scope']['revision']==154 and q['scope']['territory_sha256']==plan['territory_ref']['sha256']
        assert set(q['upstream_flows'])<=flows and set(q['upstream_anchors'])<=roles
        assert set(q['upstream_movement_relations'])<=routes and set(q['capacity_hypothesis']['ids'])<=caps
        for k in ['UPSTREAM_FIXED','DOWNSTREAM_TO_RESOLVE','DOWNSTREAM_ADAPTABLE','cross_package_dependencies','revision_triggers','expected_L1_outputs']:assert q[k]
        assert all(x['authority'] in ['OWNER_CONSTRAINT','APPROVED_CANON'] for x in q['UPSTREAM_FIXED'])
    assert [r['area'] for r in read(P/'evidence/territory-terrain-summary.json')['categories']]==[92124,575397,391002,1198158]
    maps=read(P/'visual/map-metadata.json')
    assert maps['pixels_per_block']==.5 and len(maps['maps'])==5
    for item in maps['maps']:
        with Image.open(P/item['file']) as im:assert im.size==(2400,1320)
    required=['README.md','L0-POLITY-PLAN.md','AUTHORITY-TRACE.md','ACTORS-RIGHTS.md','FLOWS-SYSTEM.md','SETTLEMENT-HIERARCHY.md','MOVEMENT-ACCESS-SKELETON.md','CAPACITY-SCALE.md','GROWTH-PATH-DEPENDENCE.md','RESILIENCE-DEPENDENCIES.md','handoff/COMMONS-HANDOFF-DECISION.md','validation/PLANNER-CRITIC.md']
    for s in required:assert (P/s).stat().st_size>0
    for q in P.rglob('*.json'):read(q)
    print('Mechanical contracts valid; not an independent planning verdict.')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['check','freeze','verify']);a=ap.parse_args();check()
    seal=P/'validation/PRIMARY-FREEZE.json'
    if a.mode=='freeze':
        if seal.exists():raise FileExistsError('Primary Freeze immutable; refuse replacement')
        # 冻结全部当前主目录文件，不读取任何Legacy；后续比较和最终核验另列。
        files=[dict(path=q.relative_to(P).as_posix(),bytes=q.stat().st_size,sha256=sha(q)) for q in sorted(P.rglob('*')) if q.is_file()]
        data=dict(schema='primary-freeze/1',plan_revision='CIV-001-L0P-r1',frozen_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),repo_execution_base='a91abf728218ca43a694be96c08e71e456ed4910',planning_state='HANDOFF_READY',primary_artifacts=files,legacy_middle_planning_not_read_before_freeze=True,statement_scope='Current-run tool retrieval: no Authority C-class file opened or used as premise before freeze. Mandatory A-class records contain legacy status and links; these were not followed.',prior_context_limitation='Conversation history contains earlier tasks and summary; not a claim of fully blinded model memory.',world_writes=0,world_write_authorization=False,review_status='AWAITING_GPT_OWNER_REVIEW')
        seal.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('PRIMARY FROZEN',len(files),data['frozen_at_utc'])
    elif a.mode=='verify':
        freeze=read(seal)
        for item in freeze['primary_artifacts']:
            q=P/item['path'];assert q.stat().st_size==item['bytes'] and sha(q)==item['sha256'],item['path']
        print('PRIMARY HASHES UNCHANGED',len(freeze['primary_artifacts']))
if __name__=='__main__':main()
