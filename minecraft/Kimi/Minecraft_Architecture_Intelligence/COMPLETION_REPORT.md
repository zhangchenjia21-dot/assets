# COMPLETION_REPORT — Minecraft Architecture Intelligence System（项目代号 H）

> 完成日期：2026-09-13 ｜ 结构按任务书 §30 ｜ 验收清单对照见文末附录（§31 逐项打勾）。

## Environment

- 真实工程根：`D:\Games\Minecraft\AI工程`（任务书中的 `D:\AI\Minecraft-AI-Fabric-26.2-Test`、`D:\Games\Minecraft\AI-Preview` 不存在）。
- 参考库根：`D:\Games\Minecraft\AI工程\AI-Blueprints\references`；原始 .litematic 主库：`D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\schematics\`（123 个，只读）。
- Parser：`AI-Blueprints\interop-test`（Node 24 CLI + 公开 API）+ 已派生 Canonical IR（schema_version=1）；本项目分析全程离线读 IR，未触碰 .litematic 原件。
- Git 状态：`D:\Games\Minecraft\AI工程` 与 `$OUT` 均非 Git 工作区（版本管理靠 MB-Vxx 批次目录与 AI-Test 证据目录）。
- 运行环境：脚本以 `py -3` + `PYTHONPATH=D:\AI\kimi\daimon-share\daimon\runtime\python\.venv\Lib\site-packages`（只读挂载 numpy/pandas）执行；托管 Python 基础解释器路径失效已绕过（见 `scripts/README.md`）。
- 产出根（$OUT）：`D:\AI\kimi\kimi\workspace\Minecraft 建筑设计\Minecraft_Architecture_Intelligence\`。

## Assets

- blueprint 数量：**123**；REF ID 数量：**123**（REF-0001…REF-0123，全程稳定未重命名）。
- normalized 状态：**123/123** 归一化到 DataVersion 4903（LEGACY_SAFE 67 / MIGRATED 55 / CURRENT_NATIVE 1）；归一化后 unresolved blocks 合计 = 0。
- 派生链覆盖 100%：blueprint.json / normalized IR / normalization-report / proxy（四视图 PNG + LOD npz + palette.json）/ preview-metadata / analysis.md 全部 123/123。
- 损坏文件：0。

## Metadata

- 成功解析：**123/123**；PARSE_FAILURE：0。
- 字段数量：**50 列**（CSV）/ JSONL 逐字段带 `_basis` 标注（OBSERVED/HEURISTIC/INFERRED/UNKNOWN）；schema 见 `02_BLUEPRINT_METADATA/METADATA_SCHEMA.md`。
- UNKNOWN 比例：main_entrance / entrance_orientation 89.4%（110/123，刻意保守的纪律结果）；楼层四字段 13.8%（17/123）；其余全部字段 0%。walkability 未知方块类型 0；unknown_material_ratio 中位 0.016%。
- 关键字段算法说明：楼层密度启发式、外部空气洪泛、walkability 站位模型、材料族子串匹配等均在 METADATA_SCHEMA.md 逐字段写明。

## Taxonomy

- Style 7 类（含 Unknown）：Rustic 20 / Medieval 19 / Fantasy 10（SUPPORTED）；Japanese 7 / Chinese 4（PROVISIONAL）；Other 7（OBSERVATION ONLY）；Unknown 56。候选类 Modern/Industrial/Gothic/Victorian/Nordic 0 样本未硬建。
- Function 15 类（含 Unknown）：Residential 23 / Decoration 22 / Castle 14 / Tower 13 / Religious 10（SUPPORTED）；Workshop 7 / Vehicle 7 / Inn 5 / Civic 4（PROVISIONAL）；Gate 3 / Blacksmith 3 / Farm 3 / Mixed-use 2 / Warehouse 1（OBSERVATION ONLY）；Unknown 6。新增类 Vehicle（n=7）；候选类 Bridge 0 样本未建立。
- 主信号 V6C2 审核分类 + 几何交叉验证（只校验/下调，不提拔）；低置信降级 5 条记录在案。

## Grammars

- 规则总量：**228 条**（style_rules.json 111 + functional_rules.json 117），全部带 sample_n 与统计区间，机器可读。
- SUPPORTED：style 3 类 67 条（Medieval 22 / Rustic 23 / Fantasy 22）；function 5 类 65 条。
- PROVISIONAL：style 2 类 44 条（Japanese 23 / Chinese 21，最高 SOFT）；function 4 类 52 条。
- OBSERVATION ONLY：Other、Gate/Blacksmith/Farm/Mixed-use/Warehouse 不出规则（仅列观测）。
- UNKNOWN 维度如实标注：entrance_placement（全风格+全功能类）、window_rhythm（全风格）、roof_form（全风格）、floor_height（3 类）、floor_count（Chinese）、房间语义（全库）。
- 数据缺口矩阵：5 style × 15 function × 5 size = 375 cell，非零 36（9.6%）；P0=50 / P1=31 / P2=293 / P3=1。

## Validator

- 规则数量：**12 条（V001–V012）**，HARD 7 / WARNING 4 / INFO 1；阈值全外置 `validator_rules.json`。
- test 数量：**30（walkability 11 + validator 19），最近运行 30/30 通过**（2026-09-13 02:58，0.051s）；V001–V007 每条 HARD 规则有正例+负例；V006 负例（楼梯尽头是墙）必现回归锁。
- hard fail 检测：全库 hard_fail_rate **0.4959**（61/123），校准轨迹 0.829 → 0.496（7 轮实证修复）。
- false positive：逐规则人工抽查（每条 HARD 规则 2–3 样本逐体素核实）——残余触发以真阳性/歧义阳性为主，**无系统性误报残留**；全库性误报（露天分量、梯子漏接、栅栏门语义等）已修复并配回归锁。
- false negative：**未系统性测量**（无全库人工标注 ground truth）——如实声明为已知限制。
- 已知盲区全表：`05_SPATIAL_VALIDATOR/known_limitations.md`。

## Benchmark

- brief 数量：**100**（`design_briefs.jsonl`，机器可读，种子 42 可复跑，11 项自洽检查 ALL CHECKS PASS）。
- difficulty 分布：Easy 40 / Medium 40 / Hard 20（模板驱动定级）。
- style 覆盖：Medieval 27 / Rustic 25 / Fantasy 16 / Japanese 16 / Chinese 16；function 覆盖 12 个 taxonomy 类；功能域 7 个。
- targets_gap = 20 条（全部命中缺口矩阵 P0 cell，脚本断言）；dev/test = 30/70 分层。
- 评分细则：五维 40/25/20/10/5 + HARD FAIL 封顶（`scoring_rubric.json`）。

## Evaluation

- 历史样本数量：**4 个 V4 样本**（A / B / C-before / C-final）全部用新 Validator + rubric 重评，真实数据：A 91 / B 79 / C-before 40（cap）/ C-final 83（/95 满分口径）；C 路线 revision_cost = 10 动作 / 1 轮 / 653 坐标（added 137 / removed 300 / changed 216，独立复算一致）。n=1/路线，个案证据非统计结论。
- B/C 样本数量：**12 条 dev brief**（P6b 离线生成实验，2026-09-13 真实运行）：B hard_fail_rate 0.083 vs C 0.000；mean total 90.75 vs 95.00；C 修复成功率 1/1（BRIEF-0099：40→91，1 轮 6 方块，diff 0.74%）。
- before/after 是否存在真实数据：**是**——V4 有 C-before/C-final 两份真实 IR + 逐坐标 diff；P6b 有 `generated/` 24 份 IR + 逐轮 traces + CLI 回归 24/24。
- 生成器性质：**programmatic reference generator（rule-driven），非 LLM**——验证的是管线闭环，不代表 LLM 水平；12 样本不构成统计结论。

## Strongest Findings（最可靠发现，8 条）

1. **"楼梯尽头是墙"可确定性检测**：几何子类 = 楼梯簇顶格在站位图中无出边（V006），回归夹具必现；根因 = 生成缺全局可达性推理（主因）+ 验证层无拓扑检查（放大器），施工/preview 排除。
2. **参考库内部交通从未被验证是全库性事实**：hard_fail_rate 0.496、connectivity_score 均值 51.3——精选外观库不承诺内部可走；未来入库门槛应含 Validator 无 HARD_FAIL。
3. **校验器必须先校准再使用**：初版 0.829 的硬失败率主要是校验器自身的语义定义问题（洪泛 interior 脆性、露天分量、机制语义），7 轮实证修复后稳定于 0.496。
4. **材料/比例类 grammar 在 3 风格 5 功能上可靠**：如 Medieval 石占比 0.589 [0.389, 0.625]（n=19）、Rustic 高对称频率 0.0（n=20）、Residential 外部门频率 0.78（n=23）——全部 OBSERVED/INFERRED 带区间。
5. **机制感知分级是诚实出口**：隔离环含门/活板门/梯子 → 降 WARNING，让"模型无法分辨意图"有分级处理而非虚构通过或误杀。
6. **Revision 闭环机器可通且代价极小**：V4 历史（C-before 40 → C-final 83）与 P6b（BRIEF-0099 40→91，1 轮 6 方块）双重实证；锚点冻结 + diff 阈值防漂移机制已制度化。
7. **Validator 嵌入 Architect→Critic 之间有独立价值**：V4 C-before 当年 Critic 未点名的硬缺陷（玻璃封门洞、门外无接近）被新 Validator 直接点名。
8. **组合级覆盖极度稀缺**：375 cell 仅 36 非零（90.4% 空缺）——122 张够类别级 grammar，远不够组合级；缺口矩阵已给出 P0 50 cell 的具体补图清单。

## Weakest Areas（不可靠的检测或 grammar）

1. main_entrance 判定：全库 89.4% UNKNOWN，入口相关 grammar 全部缺位。
2. 楼层密度启发式：密实屋顶/地毯层误检（V007 伪影 2 例、S06 评分伪阳性 8/12）。
3. V009 净高规则：触发率 33% 偏高，"通道压抑"与"装饰暗格"不可区分，仅 WARNING。
4. 洪泛 interior 语义：无玻璃窗洞建筑内部被判 exterior，connectivity_score 系统性偏低（V4-A 6 条规则不适用）。
5. Japanese/Chinese grammar 仅 PROVISIONAL（n=7/4），无 STRONG 规则；5 个功能类（n<4）与 5 个风格大类（n=0）无 grammar。
6. V008–V012 无负例夹具；机制感知降级路径无合成夹具；false negative 未测量。
7. B/C 实验样本量小（12），差异由 1 条样本驱动；生成器天花板低不代表 LLM。

## Unknowns（仍无法解决）

- 房间语义（bedroom/kitchen）自动识别——IR 不可判，维持 LLM_ONLY/HUMAN_REVIEW。
- 窗洞位置节奏（window_rhythm）——需立面聚合，未做。
- 屋顶形制（roof_form：歇山/悬山/攒尖/坡度曲线）——未测量。
- 内部空间的作者意图（密封装饰空腔是否缺陷）——静态分析不可判。
- 红石机关语义（关闭铁门旁的按钮/拉杆）——不建模。
- 审美质量——归人工终裁（HUMAN_REVIEW），不硬编码。
- 5 个 0 样本风格与 Bridge 等 0/低样本功能的建筑规律——无数据即无结论。

## Recommended Next Step

给 Codex / GPT / Owner 的下一阶段建议（按序）：
1. **按缺口矩阵 P0 清单补图**（村落核心功能 Medieval/Rustic × Inn/Civic/Gate/Blacksmith/Farm/Warehouse/Bridge 的 small/medium；Bridge 从 0 建类；并列：Modern 等 0 样本风格），新资产入库前跑 Validator 且不得有 HARD_FAIL；
2. **接入真实 LLM Architect 重跑 benchmark**（brief 集不变，dev 调参 test 跑一次），把本项目 programmatic generator 结果作为参考基线并列报告；
3. **Validator 两项改进**：主入口按"可达内部站位占比"选择、楼层启发式加"内部站位存在"二次过滤（改动须重校全库并保留旧版基准）。

## Files Changed

全部为**新增**（$OUT 内，无任何对 $OUT 外文件的修改）：

| 位置 | 文件 | 说明 |
|---|---|---|
| 根 | `00_PROJECT_CHARTER.md`、`COMPLETION_REPORT.md`（本文件）、`CONTEXT.md`（P0 建） | 章程 / 完成报告 / 共享上下文 |
| `01_INVENTORY/`（4） | `REFERENCE_LIBRARY_AUDIT.md`、`BLUEPRINT_MANIFEST.md`、`DATA_QUALITY_REPORT.md`、`audit_scan_results.json` | P0 |
| `02_BLUEPRINT_METADATA/`（6） | `METADATA_SCHEMA.md`、`blueprint_metadata.jsonl/.csv`、`palette_dictionary.json`、`feature_extraction_report.md`、`extraction_summary.json` | P1 |
| `03_TAXONOMY/`（6） | `ARCHITECTURE_TAXONOMY.md`、`style_taxonomy.json`、`function_taxonomy.json`、`labels.jsonl`、`label_summary.json`、`LABELING_NOTES.md` | P3 |
| `04_GRAMMARS/`（7） | `STYLE_GRAMMARS.md`、`FUNCTIONAL_GRAMMARS.md`、`style_rules.json`（111）、`functional_rules.json`（117）、`grammar_confidence_report.md`、`data_gap_matrix.json`（375 cell）、`ir_features.jsonl` | P3 |
| `05_SPATIAL_VALIDATOR/`（9+） | `VALIDATION_SPEC.md`、`validator_rules.json`、`REFERENCE_SET_VALIDATION.md`、`known_limitations.md`、`validator_source/`（5 个 .py + README）、`validation_run/`（jsonl + summary） | P2 |
| `06_BENCHMARK/`（7） | `BENCHMARK_SPEC.md`、`design_briefs.jsonl`（100）、`scoring_rubric.json`、`benchmark_split.json`、`zone_catalog.json`、`coverage_stats.json`、`BASELINE_RESULTS.md` | P4 |
| `07_ARCHITECT_SYSTEM/`（8） | `ARCHITECT_RULEPACK.md`、`architect_rules.json`（218）、`CRITIC_RULEPACK.md`、`critic_rules.json`（20）、`REVISION_PROTOCOL.md`、`usage_examples.md`、`build_rulepacks.py`、`verify_rulepacks.py` | P5 |
| `08_EVALUATION/` | `VALIDATOR_TESTS.md`、`BASELINE_VS_RULED.md`、`B_VS_C_PIPELINE.md`、`B_VS_C_OFFLINE_RUN.md`、`evaluation_data.jsonl`、`p6b_summary.json`、`score_v4_samples.py`、`validator_runs/`（A/B/C-before/C-final）、`generated/`（24 IR + traces + CLI 回归） | P6 |
| `09_FINAL_REPORT/`（8） | `01_EXECUTIVE_SUMMARY.md` … `08_NEXT_STEPS.md` | P7（本阶段） |
| `scripts/`（14 个 .py/.ps1 + README） | 审计/提取/标签/语法/校验/基准/评分/生成/修订/重跑脚本，路径全走 CLI 参数 | 全阶段 |
| `tests/`（2 测试模块 + fixtures） | `test_walkability.py`（11）、`test_validator.py`（19）、`fixtures/`（8 夹具 + 生成器） | P2/P6 |

修改既有文件：无（`CONTEXT.md` 为 P0 阶段新建；本阶段新增 `00_PROJECT_CHARTER.md`、`09_FINAL_REPORT/` 8 份、`COMPLETION_REPORT.md`、`scripts/safety_check*.ps1`）。

## Safety

**实测验证（2026-09-13 执行，非照抄声明）**：

```text
Formal world writes: 0
Reference source files modified: 0
Formal save files modified: 0
```

验证命令与结果（脚本存档 `scripts/safety_check.ps1` / `safety_check_bom.ps1`；cutoff = 会话开始 2026-09-12 23:31）：

```powershell
# Get-ChildItem -Recurse -File <path> | Where-Object { $_.LastWriteTime -gt '2026-09-12 23:31' } | 计数
schematics  modified/new since cutoff: 0    # D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\schematics
references  modified/new since cutoff: 0    # D:\Games\Minecraft\AI工程\AI-Blueprints\references（递归）
saves       modified/new since cutoff: 0    # ...\26.2-Fabric 0.19.5\saves（正式世界存档）
```

补充证据：
- `D:\Games\Minecraft\AI工程` 顶层目录 LastWriteTime 全部 ≤ 2026-09-12 23:25（最新为"研究缓存"23:25、MB-V110-M01-DS 19:41），均早于会话开始；
- 补充用 `find ... -newermt "2026-09-12 23:31"` 对 schematics 目录独立复核：无输出（0 文件）；
- 本项目全程未启动 Minecraft、未调用任何世界写入接口；所有脚本对 `D:\Games\Minecraft\` 只读（P1/P2/P6 输入均为只读打开）；
- 未删除任何旧版 PASS 资产（V4/V5/V6 各批次目录与证据原样保留）。

---

## 附录：任务书 §31 验收清单逐项对照

### Reference Library
- [x] 识别全部可用参考蓝图（123 张，`01_INVENTORY/BLUEPRINT_MANIFEST.md`）
- [x] REF ID 保持稳定（未重命名，映射表原样使用）
- [x] 原始 reference 未修改（Safety 实测：references / schematics 自会话开始 0 修改）

### Metadata
- [x] JSONL/CSV 可机器读取（jsonl 123 行、csv 123×50，pandas 验证通过）
- [x] 有 schema（`METADATA_SCHEMA.md`）
- [x] UNKNOWN 明确（逐字段 `_basis` 标注 + extraction_summary.json 统计）
- [x] 关键字段有算法说明（schema 逐字段 + 附录算法与盲区）

### Architecture Grammar
- [x] 规则有 sample_n（228 条全部带 n 与区间）
- [x] SUPPORTED / PROVISIONAL 区分（n≥8 / 4–7 / <4 三级，另有 OBSERVATION ONLY）
- [x] 有机器可读输出（`style_rules.json` / `functional_rules.json` / `data_gap_matrix.json`）
- [x] 无少样本过度泛化（n<4 不出规则；UNKNOWN 维度清单化管理）

### Validator
- [x] 可离线运行（全库 123 张 <2 分钟，py -3，无需 Minecraft）
- [x] 实现入口、连通性、楼梯、垂直交通核心检查（V001–V007）
- [x] "楼梯顶部堵死"可检测（V006，负例夹具必现回归锁）
- [x] Hard Fail / Warning 分开（含机制感知分级）
- [x] regression tests 存在（30 例，30/30 绿）

### Benchmark
- [x] ≥60 条 brief（实际 100 条）
- [x] 机器可读（jsonl + rubric + split + zone catalog）
- [x] 难度分层（Easy 40 / Medium 40 / Hard 20，模板驱动）
- [x] style × function 有覆盖（5 风格 × 12 功能矩阵 + 20 条 P0 gap brief）

### Architect System
- [x] Architect Rulepack（218 条，8 组，可追溯 source 自检）
- [x] Critic Rulepack（20 条，10 维度，无 critical）
- [x] Revision Protocol（锚点冻结 / diff 30% 回退 / ≤3 轮 / 机读状态机）
- [x] Validator 与 Critic 职责分离（两个 Rulepack 均有显式声明）

### Safety
- [x] 无正式世界破坏（saves 0 修改；从未启动 Minecraft）
- [x] 无 reference overwrite（references / schematics 0 修改）
- [x] 无删除旧版 PASS 资产（V4–V6 各批次与证据目录原样保留）

**未完成项：无。** 所有清单项完成；但"完成"不等于"无限制"——Weakest Areas 与 Unknowns 两节列出的边界均为如实声明，不因验收打勾而消失。
