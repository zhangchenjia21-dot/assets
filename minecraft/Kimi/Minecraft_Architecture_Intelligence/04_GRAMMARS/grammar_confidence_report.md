# grammar_confidence_report — P3 Grammar 置信度与覆盖报告

## 1. 各类别样本量与规则分级计数

### Style

| 类别 | sample_n | 级别 | 规则数 | HARD/STRONG/SOFT/OPTIONAL |
|---|---:|---|---:|---|
| Medieval | 19 | SUPPORTED | 22 | 0/5/13/4 |
| Rustic | 20 | SUPPORTED | 23 | 0/6/11/6 |
| Fantasy | 10 | SUPPORTED | 22 | 0/4/14/4 |
| Japanese | 7 | PROVISIONAL | 23 | 0/0/17/6 |
| Chinese | 4 | PROVISIONAL | 21 | 0/0/17/4 |
| Other | 7 | OBSERVATION ONLY | 0 | 0/0/0/0 |
| Unknown | 56 | 非类别 | 0 | — |

### Function

| 类别 | sample_n | 级别 | 规则数 | HARD/STRONG/SOFT/OPTIONAL |
|---|---:|---|---:|---|
| Residential | 23 | SUPPORTED | 13 | 0/2/7/4 |
| Decoration | 22 | SUPPORTED | 13 | 0/1/7/5 |
| Castle | 14 | SUPPORTED | 13 | 0/1/10/2 |
| Tower | 13 | SUPPORTED | 13 | 1/1/8/3 |
| Religious | 10 | SUPPORTED | 13 | 0/2/7/4 |
| Workshop | 7 | PROVISIONAL | 13 | 0/0/11/2 |
| Vehicle | 7 | PROVISIONAL | 13 | 0/0/10/3 |
| Inn | 5 | PROVISIONAL | 13 | 0/0/11/2 |
| Civic | 4 | PROVISIONAL | 13 | 0/0/10/3 |
| Gate | 3 | OBSERVATION ONLY | 0 | 0/0/0/0 |
| Blacksmith | 3 | OBSERVATION ONLY | 0 | 0/0/0/0 |
| Farm | 3 | OBSERVATION ONLY | 0 | 0/0/0/0 |
| Mixed-use | 2 | OBSERVATION ONLY | 0 | 0/0/0/0 |
| Warehouse | 1 | OBSERVATION ONLY | 0 | 0/0/0/0 |

## 2. UNKNOWN 维度清单（按类别，含原因）

- **Style/Medieval**：floor_height（可得样本 4/19，不足半数或 <4）；window_rhythm 规律性（窗洞位置节奏需立面聚合，本阶段 UNKNOWN）；entrance_placement（main_entrance 可判定仅 4/19，89% 全库 UNKNOWN 的纪律结果）
- **Style/Rustic**：window_rhythm 规律性（窗洞位置节奏需立面聚合，本阶段 UNKNOWN）；entrance_placement（main_entrance 可判定仅 4/20，89% 全库 UNKNOWN 的纪律结果）
- **Style/Fantasy**：floor_height（可得样本 2/10，不足半数或 <4）；window_rhythm 规律性（窗洞位置节奏需立面聚合，本阶段 UNKNOWN）；entrance_placement（main_entrance 可判定仅 0/10，89% 全库 UNKNOWN 的纪律结果）
- **Style/Japanese**：window_rhythm 规律性（窗洞位置节奏需立面聚合，本阶段 UNKNOWN）；entrance_placement（main_entrance 可判定仅 0/7，89% 全库 UNKNOWN 的纪律结果）
- **Style/Chinese**：floor_count（可得样本 3/4，不足半数或 <4）；floor_height（可得样本 1/4，不足半数或 <4）；window_rhythm 规律性（窗洞位置节奏需立面聚合，本阶段 UNKNOWN）；entrance_placement（main_entrance 可判定仅 0/4，89% 全库 UNKNOWN 的纪律结果）
- **Style/Other**：全部维度：样本不足/异质集合，仅列观测不形成规则
- **Function/Residential**：entrance_relation.方位（main_entrance 可判定仅 4/23 → UNKNOWN）
- **Function/Decoration**：entrance_relation.方位（main_entrance 可判定仅 0/22 → UNKNOWN）
- **Function/Castle**：entrance_relation.方位（main_entrance 可判定仅 0/14 → UNKNOWN）
- **Function/Tower**：entrance_relation.方位（main_entrance 可判定仅 3/13 → UNKNOWN）
- **Function/Religious**：entrance_relation.方位（main_entrance 可判定仅 0/10 → UNKNOWN）
- **Function/Workshop**：entrance_relation.方位（main_entrance 可判定仅 0/7 → UNKNOWN）
- **Function/Vehicle**：entrance_relation.方位（main_entrance 可判定仅 0/7 → UNKNOWN）
- **Function/Inn**：entrance_relation.方位（main_entrance 可判定仅 1/5 → UNKNOWN）
- **Function/Civic**：entrance_relation.方位（main_entrance 可判定仅 1/4 → UNKNOWN）
- **Function/Gate**：全部维度：样本 <4，仅列观测不形成规则
- **Function/Blacksmith**：全部维度：样本 <4，仅列观测不形成规则
- **Function/Farm**：全部维度：样本 <4，仅列观测不形成规则
- **Function/Mixed-use**：全部维度：样本 <4，仅列观测不形成规则
- **Function/Warehouse**：全部维度：样本 <4，仅列观测不形成规则

## 3. 数据缺口矩阵解读（任务书第 24 节）

矩阵：5 style × 15 function × 5 size = 375 cells；size_class 复用 V6C2 scale（阈值见分类规则规模表）。

优先级分布：P0=50 / P1=31 / P2=293 / P3=1

### Top 缺口（前 20）

| style | function | size | n | coverage | priority | 原因 |
|---|---|---|---:|---|---|---|
| Medieval | Inn | small | 0 | GAP | P0 | 村落核心功能 Inn 全库仅 5 样本且该 cell 空缺 |
| Medieval | Inn | medium | 0 | GAP | P0 | 村落核心功能 Inn 全库仅 5 样本且该 cell 空缺 |
| Medieval | Civic | small | 0 | GAP | P0 | 村落核心功能 Civic 全库仅 4 样本且该 cell 空缺 |
| Medieval | Gate | small | 0 | GAP | P0 | 村落核心功能 Gate 全库仅 3 样本且该 cell 空缺 |
| Medieval | Blacksmith | small | 0 | GAP | P0 | 村落核心功能 Blacksmith 全库仅 3 样本且该 cell 空缺 |
| Medieval | Blacksmith | medium | 0 | GAP | P0 | 村落核心功能 Blacksmith 全库仅 3 样本且该 cell 空缺 |
| Medieval | Farm | small | 0 | GAP | P0 | 村落核心功能 Farm 全库仅 3 样本且该 cell 空缺 |
| Medieval | Warehouse | small | 0 | GAP | P0 | 村落核心功能 Warehouse 全库仅 1 样本且该 cell 空缺 |
| Medieval | Warehouse | medium | 0 | GAP | P0 | 村落核心功能 Warehouse 全库仅 1 样本且该 cell 空缺 |
| Medieval | Bridge | small | 0 | GAP | P0 | 村落核心功能 Bridge 全库仅 0 样本且该 cell 空缺 |
| Medieval | Bridge | medium | 0 | GAP | P0 | 村落核心功能 Bridge 全库仅 0 样本且该 cell 空缺 |
| Rustic | Inn | small | 0 | GAP | P0 | 村落核心功能 Inn 全库仅 5 样本且该 cell 空缺 |
| Rustic | Civic | small | 0 | GAP | P0 | 村落核心功能 Civic 全库仅 4 样本且该 cell 空缺 |
| Rustic | Civic | medium | 0 | GAP | P0 | 村落核心功能 Civic 全库仅 4 样本且该 cell 空缺 |
| Rustic | Gate | small | 0 | GAP | P0 | 村落核心功能 Gate 全库仅 3 样本且该 cell 空缺 |
| Rustic | Gate | medium | 0 | GAP | P0 | 村落核心功能 Gate 全库仅 3 样本且该 cell 空缺 |
| Rustic | Blacksmith | medium | 0 | GAP | P0 | 村落核心功能 Blacksmith 全库仅 3 样本且该 cell 空缺 |
| Rustic | Farm | small | 0 | GAP | P0 | 村落核心功能 Farm 全库仅 3 样本且该 cell 空缺 |
| Rustic | Farm | medium | 0 | GAP | P0 | 村落核心功能 Farm 全库仅 3 样本且该 cell 空缺 |
| Rustic | Warehouse | small | 0 | GAP | P0 | 村落核心功能 Warehouse 全库仅 1 样本且该 cell 空缺 |

### 补充：0 样本风格大类（不进矩阵）

Modern / Industrial / Gothic / Victorian / Nordic 全库 0 样本（见 03_TAXONOMY/ARCHITECTURE_TAXONOMY.md），任何 function×size 组合都无法形成 grammar，整体列为最高优先采集方向之一（与 P0 cell 同级，按需求排序）。
