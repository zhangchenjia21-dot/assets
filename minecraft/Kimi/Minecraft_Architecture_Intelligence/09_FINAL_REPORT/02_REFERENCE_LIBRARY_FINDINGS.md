# 02_REFERENCE_LIBRARY_FINDINGS — 参考库发现（P7 最终报告 2/8）

> 数据来源：`01_INVENTORY/REFERENCE_LIBRARY_AUDIT.md`、`DATA_QUALITY_REPORT.md`、
> `02_BLUEPRINT_METADATA/feature_extraction_report.md`、`03_TAXONOMY/ARCHITECTURE_TAXONOMY.md`。
> 除注明外均为 OBSERVED。

## 1. 库构成总览

| 维度 | 分布 |
|---|---|
| 总量 | **123 张**参考蓝图（REF-0001…REF-0123，ID 稳定） |
| 原始 DataVersion | 2975×2, 3105×1, 3120×1, 3465×58, 3700×1, 3953×12, 4189×14, 4438×33, 4903×1（REF-0123 为 26.2 原生） |
| Region | 单 Region 122 张；双 Region 1 张（REF-0123 江户后期京都呉服商町家院落，42,660 blocks，全库最大） |
| 尺寸（max(x,z) 实测分布） | ≤15：14 张 / 16–30：26 / 31–60：35 / >60：48 |
| 楼层（HEURISTIC） | 1 层 56 / 2 层 33 / 3 层 11 / 4 层 4 / 5 层 1 / 6 层 1 / UNKNOWN 17 |
| 风格（taxonomy） | Rustic 20 / Medieval 19 / Fantasy 10 / Japanese 7 / Chinese 4 / Other 7 / **Unknown 56** |
| 功能（taxonomy） | Residential 23 / Decoration 22 / Castle 14 / Tower 13 / Religious 10 / Workshop 7 / Vehicle 7 / Inn 5 / Civic 4 / Gate 3 / Blacksmith 3 / Farm 3 / Mixed-use 2 / Warehouse 1 / Unknown 6 |
| 材料（中位数） | stone 0.481 / wood 0.156 / glass 0.0018——石木为主、玻璃普遍极少（Minecraft 建筑常态） |

**构成解读**：这是一个"外观精选库"而非"功能均衡库"——Decoration（树/园/亭/雕像）与 Unknown 风格合计 78 张（63%），村落核心功能（Inn/Civic/Gate/Blacksmith/Farm/Warehouse/Bridge）合计仅 19 张。这直接决定了 grammar 的覆盖边界与缺口矩阵的形状（见报告 03、08）。

## 2. 数据质量

| 指标 | 结果 |
|---|---|
| 损坏文件 | **0**（V6B 批次 PARSE_FAILED:0 / POSSIBLE_CORRUPT:0；P1 逐文件重读 123/123 成功） |
| 派生链覆盖 | blueprint.json / normalized IR / normalization-report / proxy（四视图 PNG+LOD npz）/ preview-metadata / analysis.md 全部 **123/123 = 100%** |
| air 表示 | **显式体素**（palette 含 `minecraft:air` 且在 blocks 中被引用，实测 123/123）；无 cave_air/void_air；体素化必须尊重显式 air（携带"有意留空"语义） |
| 元数据提取 | 123/123 成功、0 PARSE_FAILURE；jsonl 123 行、csv 123 行 × 50 列；全量耗时约 55 秒 |
| walkability 方块覆盖 | 未知方块类型 = **0**（全库 validator_confidence = high 的基础） |
| 材料族未匹配 | 23 种残余（lava/water/sculk 系/potted/粘液块等）；unknown_material_ratio 中位 0.016%，最高 0.676（水/岩浆特殊样本） |

## 3. 归一化状态（OBSERVED）

- **123/123 全部归一化到 DataVersion 4903**（V6C1 离线完成），compatibility：LEGACY_SAFE 67 / MIGRATED 55 / CURRENT_NATIVE 1。
- 归一化后 **unresolved blocks 合计 = 0**；旧 identifier（grass/chain 等）映射留痕于各 `normalization-report.json`；原始 IR 原样保留可溯源。
- 分析一律优先 `normalized/normalized-blueprint.json`；P1 起各阶段**全程未触碰 .litematic 原件**。

## 4. UNKNOWN 纪律的执行结果（元数据层）

| 字段 | UNKNOWN 数 | 比例 | 原因 |
|---|---:|---:|---|
| main_entrance / entrance_orientation | 110/123 | **89.4%** | 仅当 exterior_door_candidates 恰为 1 时才判定；多数蓝图 0 个（景观/雕塑/开放院落）或多个候选门 |
| estimated_floor_count / floor_elevations / floor_heights / usable_floor_area | 17/123 | 13.8% | 无密度 ≥0.30 的楼板层（树木/雕塑/低矮景观） |
| 其余全部字段 | 0 | 0% | — |

89.4% 的 UNKNOWN 是**刻意保守的纪律结果**而非缺陷；它直接导致了 grammar 层 entrance_placement 全风格 UNKNOWN（见报告 03）与 Validator 主入口选择的已知改进项（见报告 08）。

## 5. P3 重跑对齐记录（诚实声明）

P2 校准期间修复 walkability 模型三处（梯子同高程二部连接、栅栏门可交互开启、站位图边数组输出），P3 开始前按要求全量重跑元数据提取（123/123 成功）。**流程教训**：任务要求覆盖同名输出而未先留旧快照，导致无法逐字段数值 diff，只能以旧报告记录的分布为参照（median 基本不变，极端样本图结构确被修复改变）。后续如需 diff，应先快照再覆盖。

## 6. 已知限制（沿用工程约束）

各边最大 128 / 包络 ≤1,000,000 / 预览 ≤50,000 显式方块 / 施工上限 20,000；block entities、entities、scheduled ticks 不支持（标记 UNSUPPORTED，不静默丢弃）；block entities 语义（箱子内容、告示牌文字）UNKNOWN——功能判读不能依赖容器内容；蓝图 rotation/mirror 已烘焙，特征按烘焙后局部坐标系计算。

## 7. 对下游的含义

1. 派生链 100% 完整 → 全部分析可离线进行，无需 Minecraft 与原始文件；
2. 未知方块 0 → Validator 结果可信度高（`validator_confidence=high ×123`）；
3. 库的构成偏斜（装饰/Unknown 占多数）是 grammar 覆盖不足与缺口矩阵 90.4% 空缺的根因，补图计划必须以功能构成为导向（报告 08）。
