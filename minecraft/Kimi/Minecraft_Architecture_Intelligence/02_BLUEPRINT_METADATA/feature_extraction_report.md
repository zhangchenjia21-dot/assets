# feature_extraction_report — P1 特征提取报告

> 输入：123 张参考蓝图（normalized IR 优先）；输出：`blueprint_metadata.jsonl` / `blueprint_metadata.csv` / `extraction_summary.json`。
> 执行：`scripts/extract_blueprint_metadata.py --references-root … --catalog … --output …`，全量耗时约 55 秒。

## 1. 成功 / 失败

| 指标 | 值 |
|---|---:|
| 蓝图总数 | 123 |
| 提取成功 | **123** |
| PARSE_FAILURE | **0** |
| jsonl 行数 | 123（= 成功数 + 失败数，本批全为 OK 记录） |
| csv | 123 行 × 50 列，pandas 读取验证通过 |

## 2. UNKNOWN 比例（按字段，Top）

| 字段 | UNKNOWN 数 | 比例 | 原因 |
|---|---:|---:|---|
| main_entrance | 110/123 | 89.4% | 仅当 exterior_door_candidates 恰为 1 时才判定；多数蓝图有 0 个（景观/雕塑/开放院落）或多个候选门，按纪律写 UNKNOWN |
| entrance_orientation | 110/123 | 89.4% | 同上 |
| estimated_floor_count | 17/123 | 13.8% | 无密度 ≥0.30 的楼板层（多为树木、雕塑、低矮景观） |
| floor_elevations | 17/123 | 13.8% | 同上 |
| floor_heights | 17/123 | 13.8% | 同上 |
| usable_floor_area | 17/123 | 13.8% | 同上 |
| 其余全部字段 | 0 | 0% | — |

walkability 方块分类表覆盖全库：未知方块类型 = **0**（UNKNOWN 计入统计 = 0）。材料族未匹配类型 23 种（残余：lava/water/sculk 系/potted 残余/粘液块等），unknown_material_ratio 中位数 **0.016%**，最高 0.676（REF 中以水/岩浆为主的特殊样本）。

## 3. 关键字段分布摘要

### 楼层检测（HEURISTIC）
- 层数分布：1 层 56 / 2 层 33 / 3 层 11 / 4 层 4 / 5 层 1 / 6 层 1 / UNKNOWN 17
- 置信度：high 37 / medium 69 / low 17（low → 楼层字段 UNKNOWN）
- 抽查 REF-0123（町家院落）：floor_elevations=[3,14]，confidence=high，符合两层町家直觉。

### 连通性（HEURISTIC，walkability 模型）
- walkable_components：min 2 / median 285 / max 14,625；**全部 123 张 ≥ 2 个分量**
- largest_component_ratio：min 0.001 / median 0.386 / max 0.853；≥0.5 的 43 张
- vertical_connections：median 474；dead_end_count：median 250

> **解读注意**：分量把屋顶、树梢、墙顶、装饰檐口等露天表面都算作站位（它们露天、净高无限），而参考蓝图多数屋面是断开的小区域，所以“分量大、最大分量占比低”**不等于建筑不可走**。6.6 字段是原始图指标，真正的“入口不可达/房间孤立/楼梯堵死”判定是 P2 Validator 的职责（将结合 exterior/interior 划分与入口锚点）。

### 门 / 窗 / 垂直交通
- door_count：median 1；53 张为 0（真实属性：树木/雕塑/开放构筑物无门）；exterior_door_candidates==0 的 54 张
- window_count_estimate：median 13（玻璃体素数，≈窗面积）
- stair_count：median 339；stair_cluster_count 与梯柱共同构成 vertical_access_candidates

### 材料（OBSERVED）
- stone_ratio median 0.481、wood_ratio median 0.156、glass_ratio median 0.0018——库以石木为主，玻璃普遍很少（Minecraft 建筑常态）

## 4. 与 catalog.json 已有字段的关系

本 Metadata DB **不复制** catalog 的分类语义字段（primary_use / styles / scale / settlement_roles / terrain_fit / material_profile 等 60+ 字段），通过 `ref_id` 关联；仅复用其身份与技术字段（original_filename / name / minecraft_data_version / compatibility / region_count）作为 OBSERVED 输入。

新增价值（catalog 没有的）：几何（暴露面/质心/对称性/外壳与内部空气）、楼层启发式、门窗楼梯计数、**walkability 连通性全套**——这是解决“楼梯尽头是墙”的 P2 Validator 的数据底座。

已知口径差异：catalog.block_count 为显式方块数（含显式 air），本库 non_air_blocks 为非空气体素数；两者不一致属预期，本库字段口径以 METADATA_SCHEMA.md 为准。

## 5. 已知限制

1. 楼层启发式对“密实雕塑型”蓝图可能高估层数，对“无实体楼板”蓝图给出 low/UNKNOWN——均按 HEURISTIC/UNKNOWN 标注。
2. window_count_estimate 是玻璃体素计数（面积），不是窗户个数；个数需要立面聚合，留待 P2+。
3. main_entrance 判定刻意保守（单一外部门才判定），89% UNKNOWN 是纪律结果而非缺陷。
4. walkability 模型为近似：不模拟跳跃、游泳路径不计站位、门“可交互开启”视为可过（铁质 closed 除外）。参数与分类表数据驱动，可扩展。
5. symmetry 按蓝图烘焙后局部坐标系计算，不代表放置到世界后的朝向对称。

## 6. P3 重跑对齐记录（walkability 模型三处修复后）

**背景**：P2 阶段对 `walkability.py` 做了三处修复，P1 首批元数据的连通性字段（6.6）与修复后模型存在已知差异。P3 开始前按任务要求重跑 `extract_blueprint_metadata.py` 全量覆盖。

**三处修复**（详见 `scripts/README.md` 与 walkability 模块注释）：
1. `analyze(..., return_graph=True)` 新增站位图边数组输出（`graph_src/graph_dst/stance_mask`）——纯增量，不改变既有指标数值；
2. **梯柱二部连接**：同高程梯口站位组与相邻高程组间改为完全二部连接，修复旧链式实现漏接"梯井两侧分属不同房间的同高站位"的问题——影响 63 张含梯子的蓝图，方向为合并分量（`walkable_components` 下降或不变）；
3. **栅栏门可交互**：非铁质关闭栅栏门由"阻挡"改为"玩家可开启→可过"（与门语义一致）——影响 69 张含 fence_gate 体素的蓝图，方向为新增可通行站位并合并分量。

**重跑结果**：123/123 成功、0 失败，输出覆盖 `blueprint_metadata.jsonl / .csv / extraction_summary.json`（同名文件，按要求覆盖）。

**前后对比（诚实记录）**：任务要求覆盖同名文件，**未保留旧 jsonl 快照**，因此无法做逐字段 diff，仅能以本报告第 3 节记录的旧分布为参照：

| 指标 | 旧（P1 首批，第 3 节记录） | 新（本次重跑） |
|---|---|---|
| walkable_components min / median / max | 2 / 285 / 14,625 | 3 / 285 / 14,659 |
| largest_component_ratio ≥0.5 数量 | 43 | 43 |
| vertical_connections median | 474 | 486 |
| dead_end_count median | 250 | 249 |

整体分布仅小幅移动（median 基本不变），与"修复只影响含梯子/栅栏门子集、且多数分量本已连通"的预期一致；min/max 的小幅变化说明极端样本（大型复杂构筑物）的图结构确实被修复改变。分量变化方向同时受"新站位产生"（栅栏门格变为可站）与"分量合并"两个相反因素影响，非单调属正常。

**暴露的问题（如实记录）**：无提取失败、无 UNKNOWN 方块新增；唯一流程问题是"覆盖同名输出而未先留快照"导致无法数值 diff，已在本节以旧报告记录值代替。后续阶段如需 diff，应先快照再覆盖。
