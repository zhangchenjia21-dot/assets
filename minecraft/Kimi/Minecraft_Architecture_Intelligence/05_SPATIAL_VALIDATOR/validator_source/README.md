# validator_source README — Spatial Validator（项目代号 H · P2）

对 Canonical Blueprint IR 做离线空间质量校验：V001–V012 共 12 条规则
（入口/连通/孤立房间/楼梯底顶/垂直交通/门 clearance/净高/围护/屋顶/死端）。
只读输入，产出写入指定目录。**对 `D:\Games\...` 参考库全程零写入。**

## 运行环境

```bash
export PYTHONPATH="D:\AI\kimi\daimon-share\daimon\runtime\python\.venv\Lib\site-packages"
py -3 <script> ...
```
（托管 venv 基础解释器损坏，用 `py -3` + 只读挂载其 site-packages；见 `scripts/README.md`）

## 模块

| 文件 | 职责 |
|---|---|
| `spatial_context.py` | 共享空间上下文：体素化（复用 P1 blueprint_io）、内外空气洪泛、walkability 图、内部站位、门/开口/舱口候选、楼梯簇、楼层、低净高格 |
| `rules.py` | V001–V012 规则实现，全部阈值来自 `validator_rules.json` |
| `core.py` | 单张编排 + 任务书第 11 节输出字段 + 四个评分 |
| `validate_blueprints.py` | CLI：批量 / 单张 |
| `../validator_rules.json` | 规则参数（severity、阈值，可调不硬编码） |

## 用法

```bash
# 批量：references derived 根目录（扫描 REF-* 子目录，只读）
py -3 validate_blueprints.py \
  --input "D:\Games\Minecraft\AI工程\AI-Blueprints\references\derived" \
  --output "<输出目录>"

# 单张：REF 派生目录 或 normalized-blueprint.json / blueprint.json
py -3 validate_blueprints.py --input "...\derived\REF-0001" --output "<输出目录>"

# 从 metadata.jsonl 批量（需 --references-root 解析 ref_id）
py -3 validate_blueprints.py \
  --input "..\..\02_BLUEPRINT_METADATA\blueprint_metadata.jsonl" \
  --references-root "D:\Games\Minecraft\AI工程\AI-Blueprints\references" \
  --output "<输出目录>"

# 自定义规则阈值
py -3 validate_blueprints.py --input ... --output ... --rules my_rules.json
```

输出：`<输出目录>\validation_results.jsonl`（每张一行：第 11 节字段 + 逐规则明细
+ diagnostics）与 `validation_summary.json`（触发频率、hard_fail_rate 等）。

## 作为库调用

```python
import sys
sys.path.insert(0, r"...\05_SPATIAL_VALIDATOR\validator_source")
from core import validate_one
result = validate_one(r"...\derived\REF-0001")   # dict，见 VALIDATION_SPEC.md 第 2 节
```

## 测试

```bash
# 在 $OUT（Minecraft_Architecture_Intelligence）根目录下
py -3 -m unittest tests.test_validator -v    # 19 个用例，8+1 组合成夹具
py -3 -m unittest tests.test_walkability -v  # P1 模型 11 个用例
```

夹具在 `tests/fixtures/*.json`（合成 Canonical IR，`generate_fixtures.py` 可重新生成；
测试启动时若缺失会自动生成）。判定算法/阈值/盲区见 `../VALIDATION_SPEC.md`，
全库校准结果见 `../REFERENCE_SET_VALIDATION.md`。
