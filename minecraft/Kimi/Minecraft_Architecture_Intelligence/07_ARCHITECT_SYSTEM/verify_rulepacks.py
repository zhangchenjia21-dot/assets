# -*- coding: utf-8 -*-
"""verify_rulepacks.py — P5 验收抽查：来源可追溯 / UNKNOWN 纪律 / 字段完整 / 职责分离。"""
import json
import random
from pathlib import Path

p = Path(r'D:\AI\kimi\kimi\workspace\Minecraft 建筑设计\Minecraft_Architecture_Intelligence')
arch = json.loads((p / '07_ARCHITECT_SYSTEM/architect_rules.json').read_text(encoding='utf-8'))
crit = json.loads((p / '07_ARCHITECT_SYSTEM/critic_rules.json').read_text(encoding='utf-8'))
style = {r['rule_id']: r for r in json.loads((p / '04_GRAMMARS/style_rules.json').read_text(encoding='utf-8'))['rules']}
func = {r['rule_id']: r for r in json.loads((p / '04_GRAMMARS/functional_rules.json').read_text(encoding='utf-8'))['rules']}
val = json.loads((p / '05_SPATIAL_VALIDATOR/validator_rules.json').read_text(encoding='utf-8'))

# 1) 字段完整性
required = {'id', 'category', 'type', 'statement', 'source', 'confidence', 'basis', 'applies_to'}
assert all(required <= set(r) for r in arch['rules'])
print('1) architect 全部 %d 条均含 8 必填字段 PASS' % len(arch['rules']))

# 2) 抽查 grammar 转换规则：数值与元信息必须与上游完全一致
random.seed(7)
sourced = [r for r in arch['rules']
           if r['source'].get('rule_id') in style or r['source'].get('rule_id') in func]
sample = random.sample(sourced, 12)
ok = True
for r in sample:
    src = style.get(r['source']['rule_id']) or func[r['source']['rule_id']]
    for k in ('median', 'p25', 'p75', 'min', 'max', 'frequency', 'sample_n'):
        if k in src and r['stats'].get(k) != src[k]:
            ok = False
            print('   MISMATCH', r['id'], k)
    if (r['type'], r['confidence'], r['basis']) != (src['rule_type'], src['confidence'], src['basis']):
        ok = False
        print('   META MISMATCH', r['id'])
print('2) 抽查 12 条 grammar 转换规则（共 %d 条可抽查），数值/type/confidence/basis 一致: %s'
      % (len(sourced), 'PASS' if ok else 'FAIL'))
for r in sample[:4]:
    print('   样例: %s -> %s' % (r['id'], r['source']['rule_id']))

# 3) validator_precheck 阈值一致性
pc = [r for r in arch['rules'] if r['category'] == 'validator_precheck']
mismatch = [r['id'] for r in pc if r['validator_params'] != val[r['source']['rule_id']]['params']]
print('3) validator_precheck %d 条阈值与 validator_rules.json 一致: %s'
      % (len(pc), 'PASS' if not mismatch else mismatch))

# 4) UNKNOWN 纪律
unknown_dims = ('window_rhythm', 'entrance_placement', 'roof_form')
bad = [r['id'] for r in sourced if any(u in r['source']['rule_id'] for u in unknown_dims)]
print('4) UNKNOWN 维度无数值规则: %s' % ('PASS' if not bad else bad))

# 5) critic 字段 / 禁止项
assert all({'id', 'dimension', 'statement', 'check', 'severity', 'revision_template', 'source'} <= set(r)
           for r in crit['rules'])
kinds = sorted({r['check']['kind'] for r in crit['rules']})
sev = sorted({r['severity'] for r in crit['rules']})
heur = [r for r in crit['rules'] if r['check']['kind'] == 'HEURISTIC']
print('5) critic %d 条字段完整; kinds=%s; severity=%s; HEURISTIC 均带 metric: %s'
      % (len(crit['rules']), kinds, sev, all('metric' in r for r in heur)))
assert 'critical' not in sev, 'critic 不应有 critical（客观必须项归 Validator）'

# 6) critic HEURISTIC 引用的 grammar 模板可展开成真实 rule_id
ref_ok = True
for r in crit['rules']:
    rid = r['source'].get('rule_id') or ''
    if '{style}' in rid or '{function}' in rid:
        cand = rid.replace('{style}', 'Medieval').replace('{function}', 'Residential')
        if 'palette_*_ratio' in cand:
            for d in ('palette_wood_ratio', 'palette_stone_ratio',
                      'palette_glass_ratio', 'palette_decorative_ratio'):
                c2 = cand.replace('palette_*_ratio', d)
                if c2 not in style:
                    ref_ok = False
                    print('   critic 来源缺失:', c2)
        elif (cand.startswith('STYLE.') or cand.startswith('FUNC.')) and cand not in style and cand not in func:
            ref_ok = False
            print('   critic 来源缺失:', cand)
print('6) critic 引用 grammar 模板可展开为真实 rule_id: %s' % ('PASS' if ref_ok else 'FAIL'))
print('\nALL CHECKS DONE')
