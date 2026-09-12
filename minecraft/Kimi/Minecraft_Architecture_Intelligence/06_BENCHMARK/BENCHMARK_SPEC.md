# BENCHMARK_SPEC — Design Brief Benchmark 规格说明书

> 阶段：P4（Design Brief Benchmark）｜版本：P4-1.0｜生成：`scripts/build_benchmark.py`（种子 42，可复跑）
> 验收：`scripts/validate_benchmark.py` 全量 11 项自洽检查 + 10 条抽查明细，当前 **ALL CHECKS PASS**。

## 1. 用途

建立统一任务集，用于横向比较不同 Architect（ChatGPT / Codex / Kimi / Grok）与 B/C 两条设计管线
（B=规则约束单轮；C=Architect→Critic→Revision）。每条 brief 是一份机器可读的"设计任务书"，
评分细则见 `scoring_rubric.json`（任务书 §14 五维权重）。

## 2. 字段定义（design_briefs.jsonl，每行一条）

| # | 字段 | 类型 | 说明 |
|---|---|---|---|
| 1 | `brief_id` | string | `BRIEF-0001`…`BRIEF-0100`，唯一 |
| 2 | `difficulty` | enum | `Easy` / `Medium` / `Hard`（定级规则见 §3） |
| 3 | `style` | enum | `Medieval` / `Rustic` / `Fantasy` / `Japanese` / `Chinese`（真实库样本充足的 5 类） |
| 4 | `function` | enum | taxonomy function 类（Residential / Mixed-use / Workshop / Blacksmith / Warehouse / Farm / Inn / Civic / Religious / Castle / Tower / Gate） |
| 5 | `plot_width` | int | 地皮宽（方块数，≤96，工程上限 128 内） |
| 6 | `plot_depth` | int | 地皮深 |
| 7 | `max_height` | int | 限高（含屋顶） |
| 8 | `required_floors` | int | 要求楼层数 |
| 9 | `required_zones` | list[str] | 必需功能区（zone 语义见 `zone_catalog.json`，含 min_area 与 exterior 标记） |
| 10 | `optional_zones` | list[str] | 可选功能区（容量不足时可裁） |
| 11 | `required_adjacencies` | list[[a,b]] | 必须相邻的 zone 对 |
| 12 | `forbidden_adjacencies` | list[[a,b]] | 禁止相邻的 zone 对（如 forge×living_quarters 防火） |
| 13 | `entrance_constraints` | object | min/max 入口数、朝向、plot 边缘可达、门前 clearance |
| 14 | `vertical_circulation_constraints` | object | 是否需要垂直连通、允许手段（stairs/ladder）、假定层高 `assumed_floor_height`、楼梯顶部净高 |
| 15 | `palette_constraints` | object | 主导材料族、各族占比区间（取自 style_rules.json p25-p75）、禁用族 |
| 16 | `roof_constraints` | object | 屋顶形式、高度占比区间、最小出檐、预估屋顶高度 |
| 17 | `special_features` | list[str] | 风格化构件（烟囱、垛口、彩色玻璃等） |
| 18 | `hard_constraints` | list[object] | Validator 可机检约束，`validator_ref` 引用 V001-V012（任务书 §10） |
| 19 | `soft_constraints` | list[object] | Critic 维度约束，带 `dimension` 与 `target` |
| 20 | `scoring_dimensions` | object | 五维权重 40/25/20/10/5（§14，全 benchmark 一致） |

**扩展字段**（超出任务书 20 字段的补充）：`function_domain`（7 大功能域标签）、
`targets_gap`（是否命中 P0 缺口）、`gap_ref`（缺口矩阵 cell 引用）。

### 功能域 → taxonomy 映射

| 功能域 | taxonomy function |
|---|---|
| Residential | Residential |
| Mixed-use | Mixed-use |
| Workshop | Workshop / Blacksmith / Warehouse / Farm（生产-仓储域合并，记录在案） |
| Hospitality | Inn |
| Civic | Civic / Religious |
| Defensive | Castle / Tower / Gate |
| Constrained Plot | 底层 function 任意（Residential/Workshop/Inn/Tower），特征是 plot 长边 ≤15 且强制竖向发展 |

## 3. 难度定级规则

| 维度 | Easy | Medium | Hard |
|---|---|---|---|
| 楼层 | 1（个别 2，允许梯子） | 2 | ≥2，Constrained/Tower 3-5 |
| required_zones | ≤2（个别 3） | 3 | ≥4 |
| required_adjacencies | 0-1 | 1-2 | ≥2 |
| forbidden_adjacencies | 0 | 0-1 | ≥1 |
| 限高余量 | floors×fh + roof + 2~4 | 同左 | floors×fh + roof + 1（紧约束） |
| 垂直连通 | 多数不要求 | 必须 | 必须且全楼层连通 |

定级由功能模板（`build_benchmark.py` 中 `T[function][difficulty]`）驱动，非事后标注。

## 4. 数值锚定（与真实库一致，不发明数值）

- **层高 fh**：Medieval/Rustic/Chinese=5，Fantasy/Japanese=6。依据 STYLE.Rustic.floor_height 实测
  中位 6.0（范围 3-12）、Japanese 中位 8；取"净高 3 + 楼板 1 + 余量"的保守值。
- **plot 档位**：small ≤15 / medium 16-30 / large 31-60 / xlarge 61-96。参照 blueprint_metadata
  实库 max(x,z) 分布（≤15:14 张 / 16-30:26 / 31-60:35 / >60:48），benchmark 偏向中小尺度
  （small 44 / medium 43 / large 9 / xlarge 4），因生成评测关注空间组织正确性而非巨构。
- **长宽比**：按各 style footprint_ratio 的 p25-p75 采样（如 Medieval 1.05-1.23，Japanese 1.06-2.10）。
- **材料区间**：palette 各族区间直接取 STYLE.*.palette_*_ratio 的 p25-p75。
- **屋顶占比**：取 STYLE.*.roof_height_ratio 实测区间（Medieval 0.05-0.25、Japanese 0.09-0.30、
  Chinese 0.11-0.35）。
- **max_height** = floors × fh + 预估屋顶高（0.22×长边，限 [3,14]）+ 余量，保证 C01/C02 自洽。

## 5. 覆盖矩阵（真实统计，100 条）

### 5.1 style × function（全难度合计）

| style | Residential | Mixed-use | Workshop | Blacksmith | Warehouse | Farm | Inn | Civic | Religious | Castle | Tower | Gate | 合计 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Medieval | 7 | 2 | 1 | 2 | 3 | 1 | 3 | 3 | 1 | 1 | 1 | 2 | 27 |
| Rustic | 5 | 2 | 2 | 1 | 1 | 1 | 5 | 3 | 1 | 1 | 1 | 2 | 25 |
| Fantasy | 5 | 2 | 2 | · | · | · | 2 | 1 | · | 2 | 2 | · | 16 |
| Japanese | 5 | 3 | 1 | · | · | · | 3 | · | 1 | 1 | 2 | · | 16 |
| Chinese | 6 | 3 | 2 | · | · | · | 1 | 1 | 1 | 1 | 1 | · | 16 |

### 5.2 功能域 × 难度

| 功能域 | Easy | Medium | Hard | 合计 |
|---|---|---|---|---|
| Residential | 15 | 6 | 2 | 23 |
| Mixed-use | 3 | 6 | 3 | 12 |
| Workshop | 5 | 8 | 1 | 14 |
| Hospitality | 4 | 5 | 3 | 12 |
| Civic | 3 | 6 | 3 | 12 |
| Defensive | 4 | 7 | 4 | 15 |
| Constrained Plot | 6 | 2 | 4 | 12 |
| **合计** | **40** | **40** | **20** | **100** |

### 5.3 targets_gap 清单（20 条，占 20%）

全部命中 `data_gap_matrix.json` 的 **P0** cell（脚本断言非 P0 直接失败）：

| brief_id | difficulty | style | function | size_class | plot | floors | maxH |
|---|---|---|---|---|---|---|---|
| BRIEF-0041 | Medium | Medieval | Blacksmith | small | 28x32 | 1 | 15 |
| BRIEF-0042 | Medium | Medieval | Blacksmith | medium | 36x39 | 1 | 18 |
| BRIEF-0043 | Hard | Rustic | Blacksmith | medium | 38x50 | 2 | 22 |
| BRIEF-0044 | Easy | Medieval | Warehouse | small | 21x23 | 1 | 13 |
| BRIEF-0045 | Medium | Medieval | Warehouse | medium | 49x56 | 1 | 21 |
| BRIEF-0046 | Medium | Rustic | Warehouse | small | 23x32 | 2 | 21 |
| BRIEF-0048 | Easy | Medieval | Farm | small | 31x32 | 1 | 15 |
| BRIEF-0049 | Medium | Rustic | Farm | medium | 48x56 | 1 | 20 |
| BRIEF-0050 | Easy | Medieval | Inn | small | 24x28 | 1 | 13 |
| BRIEF-0051 | Easy | Medieval | Inn | small | 18x20 | 1 | 11 |
| BRIEF-0052 | Easy | Rustic | Inn | small | 19x24 | 2 | 18 |
| BRIEF-0053 | Easy | Rustic | Inn | small | 23x29 | 2 | 20 |
| BRIEF-0062 | Easy | Medieval | Civic | small | 31x32 | 1 | 16 |
| BRIEF-0063 | Easy | Medieval | Civic | small | 18x21 | 1 | 14 |
| BRIEF-0064 | Medium | Rustic | Civic | small | 19x26 | 2 | 18 |
| BRIEF-0065 | Medium | Rustic | Civic | medium | 59x64 | 2 | 26 |
| BRIEF-0079 | Easy | Medieval | Gate | small | 24x26 | 2 | 18 |
| BRIEF-0080 | Medium | Medieval | Gate | small | 31x32 | 2 | 19 |
| BRIEF-0081 | Medium | Rustic | Gate | small | 31x32 | 2 | 21 |
| BRIEF-0082 | Hard | Rustic | Gate | medium | 37x47 | 2 | 21 |

gap brief 的 plot 长边严格落在 V6C2 size_class 边界内（small 17-32 / medium 33-64），
确保评测报告能精确回指缺口矩阵 cell。这些 brief 测试 Architect 在**无本地 grammar 支撑**的
组合上的泛化能力，评定时 style_compliance 按邻近 style 宽松判定并标注 GENERALIZATION_CASE
（见 scoring_rubric.json）。

## 6. 设计原则

1. **真实库锚定**：一切数值区间来自 style_rules.json / functional_rules.json / blueprint_metadata.jsonl
   的实测统计；gap brief 的尺寸档来自 data_gap_matrix 的 V6C2 scale 规则。
2. **内部自洽**：生成器内置断言（层高×楼层 ≤ 限高；zone 容量 ≤ 可用面积），
   独立校验脚本 `validate_benchmark.py` 再做 11 项全量检查，双重把关。
3. **可机检**：hard_constraints 逐条映射 Validator 规则 V001-V012；soft_constraints 逐条映射
   Critic 五维；zone 语义集中在 `zone_catalog.json`（min_area + exterior）。
4. **无重复**：内容键（style/function/difficulty/plot/maxH/floors/zones）唯一性断言。
5. **可复跑**：固定种子 42；`py scripts/build_benchmark.py --root <根>` 一键重建全部产物。
6. **防过拟合**：dev/test = 30/70 分层抽样（`benchmark_split.json`），调参只用 dev。

## 7. 产物清单

| 文件 | 说明 |
|---|---|
| `design_briefs.jsonl` | 100 条 brief（每行一条 JSON，20 必备字段 + 扩展字段） |
| `BENCHMARK_SPEC.md` | 本文件 |
| `scoring_rubric.json` | 五维评分细则 + HARD FAIL 总分封顶规则 |
| `benchmark_split.json` | dev 30 / test 70 分层划分 |
| `zone_catalog.json` | zone 语义目录（min_area / exterior） |
| `coverage_stats.json` | 覆盖统计机读版（本文件 §5 的数据源） |
| `BASELINE_RESULTS.md` | 基线评测表骨架（P6 阶段回填） |
