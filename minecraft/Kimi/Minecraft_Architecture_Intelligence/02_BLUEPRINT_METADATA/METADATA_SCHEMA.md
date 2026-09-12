# METADATA_SCHEMA — Blueprint Metadata DB 字段定义

> 数据文件：`blueprint_metadata.jsonl`（每行一张蓝图，UTF-8 JSON）+ `blueprint_metadata.csv`（扁平主要字段）。
> 生成脚本：`scripts/extract_blueprint_metadata.py`。分析输入一律优先 `normalized\normalized-blueprint.json`（回退 `blueprint.json`，记录于 `ir_source`）。

## _basis 标记规则

每条记录含 `_basis` dict：`字段名 → OBSERVED | HEURISTIC | INFERRED | UNKNOWN`：

- **OBSERVED**：从 IR 几何 / block state / catalog 直接读取或确定性计算（计数、比例、熵、暴露面等）。
- **HEURISTIC**：经本工程明确算法近似（楼层检测、外部空气洪泛、walkability 模型、聚类定义）。
- **INFERRED**：跨蓝图统计规律（P1 未产生，留待 P3 Grammar）。
- **UNKNOWN**：算法无法稳定判断。此时**字段值本身为字符串 `"UNKNOWN"`**，`_basis` 同步标 UNKNOWN。

CSV 不含 `_basis`；JSONL 为唯一完整事实来源。

## 6.1 基础字段

| 字段 | 类型/单位 | 定义与算法 | basis |
|---|---|---|---|
| ref_id | string | 目录名 REF-xxxx | OBSERVED |
| status | string | OK / PARSE_FAILURE | OBSERVED |
| source_file | string | 原始 .litematic 文件名（catalog.original_filename） | OBSERVED |
| source_name | string | catalog.name（人类可读名） | OBSERVED |
| data_version | int | 原始 minecraft_data_version（catalog） | OBSERVED |
| normalized_status | string | catalog.compatibility：LEGACY_SAFE / MIGRATED / CURRENT_NATIVE | OBSERVED |
| region_count | int | catalog.region_count | OBSERVED |
| size_x / size_y / size_z | 格 | IR dimensions 与 blocks 实际范围的较大者 | OBSERVED |
| bounding_volume | 格³ | size_x × size_y × size_z | OBSERVED |
| non_air_blocks | 格 | 包络内非空气体素数（显式 air 与未覆盖空洞都计为空气） | OBSERVED |
| air_blocks | 格 | bounding_volume − non_air_blocks | OBSERVED |
| occupancy_ratio | 0–1 | non_air / bounding_volume | OBSERVED |
| unique_block_states | 个 | 非空气体素用到的 palette 状态数 | OBSERVED |
| unique_block_types | 个 | 非空气体素用到的 block_id 数 | OBSERVED |
| palette_entropy | bit | 非空气体素 block state 频次的 Shannon 熵（−Σp·log2p） | OBSERVED |

## 6.2 材料字段

材料族由 `palette_dictionary.json` 唯一定义：按 families 顺序对 block_id 做子串匹配，先匹配先生效；未匹配 → UNKNOWN。**所有比例分母 = non_air_blocks**。

| 字段 | 定义 | basis |
|---|---|---|
| dominant_palette | 频次 Top-10 block state 字符串列表 | OBSERVED |
| top_5_block_types | Top-5 block_id 及计数 | OBSERVED |
| top_10_block_states | Top-10 state 及计数 | OBSERVED |
| wood_ratio / stone_ratio / glass_ratio / metal_ratio / decorative_ratio / functional_block_ratio | 各族体素占比 | OBSERVED |
| unknown_material_ratio | 未匹配方块占比（如实保留） | OBSERVED |
| unknown_material_block_types | 未匹配 block_id 清单 | OBSERVED |

## 6.3 几何字段

| 字段 | 定义与算法 | basis |
|---|---|---|
| footprint_area | 含 ≥1 非空气体素的 (x,z) 柱数 | OBSERVED |
| solid_volume | = non_air_blocks | OBSERVED |
| surface_area_estimate | 暴露面计数：6N − 2×(6 邻接实体对数) | OBSERVED |
| width_height_ratio | size_x / size_y | OBSERVED |
| depth_height_ratio | size_z / size_y | OBSERVED |
| center_of_mass | 实体体素质心 [x,y,z]（蓝图局部坐标） | OBSERVED |
| vertical_mass_distribution | y 轴 5 等分带的实体占比（和=1） | OBSERVED |
| symmetry_x / symmetry_z | 镜像匹配率：对 mid 面镜像后，候选（至少一侧实体）体素中两侧皆实体的比例 | OBSERVED |
| exterior_shell_ratio | 与“外部空气”相邻的实体体素占比。外部空气 = 从包络边界 6 连通洪泛可达的空气 | HEURISTIC（“外部”由洪泛定义） |
| interior_air_ratio | 内部空气体素 / bounding_volume。内部空气 = 洪泛不可达的空气 | HEURISTIC |

## 6.4 楼层特征（HEURISTIC）

算法：逐 y 层计算实体密度 `density(y) = solid(y)/(size_x·size_z)`；density ≥ 0.30 的层为楼板候选；连续候选层合并为一组，楼面（行走面）高程 = 组顶 y + 1；间距 < 2 格的楼面去重合并。

| 字段 | 定义 | basis |
|---|---|---|
| estimated_floor_count | 楼面数 | HEURISTIC；无候选层时 UNKNOWN |
| floor_elevations | 楼面 y 高程列表 | 同上 |
| floor_heights | 相邻楼层层高差列表 | 同上 |
| usable_floor_area | 各楼面下一层（y = e−1）实体体素数之和（近似可站立面积） | 同上 |
| floor_detection_confidence | high（≥2 层且峰值密度 ≥0.40）/ medium（有候选层）/ low（无候选层 → 其余字段 UNKNOWN） | HEURISTIC |

已知盲区：无实体楼板的开放式地基、密实雕塑（密度全高都高但无“层”）、低密度大跨屋顶 → 可能 low/UNKNOWN 或高估层数。

## 6.5 入口 / 门 / 窗 / 垂直交通

| 字段 | 定义与算法 | basis |
|---|---|---|
| door_count | half=lower 的门体素数（门扇数，非门体素数） | OBSERVED |
| exterior_door_candidates | 门扇 4 邻（脚部高度）存在外部空气的门数 | HEURISTIC |
| entrance_candidates | = exterior_door_candidates 的坐标+朝外方向列表 | HEURISTIC |
| main_entrance | 仅当 exterior_door_candidates == 1 时给出 {pos, facing_out}，否则 UNKNOWN | HEURISTIC / UNKNOWN |
| entrance_orientation | 主入口朝外方向（west/east/north/south） | 同上 |
| window_count_estimate | 玻璃+玻璃板体素数（≈窗面积，非窗个数） | HEURISTIC |
| stair_count | 楼梯类体素数 | OBSERVED |
| stair_cluster_count | 楼梯体素的 26 连通聚类数 | HEURISTIC |
| ladder_count | 梯子类体素数 | OBSERVED |
| ladder_column_count | 梯子按 (x,z) 分组的柱数 | OBSERVED |
| vertical_access_candidates | stair_cluster_count + ladder_column_count | HEURISTIC |

注意：`door_count ≠ entrance_count`（任务书要求）。door_count==0 的蓝图有 53 张（景观/雕塑/开放式院落），这是真实属性。

## 6.6 空间连通性（全部来自 walkability 模型，HEURISTIC）

| 字段 | 定义 |
|---|---|
| walkable_voxels | 合法站位（stance）数：有支撑、脚部/头部净高 ≥1.8 |
| walkable_components | 站位连通图的分量数（水平 4 邻 + 高差 ≤0.5 步高 + 楼梯 ≤1.0 + 梯柱垂直边） |
| largest_component_ratio | 最大分量站位数 / 总站位数 |
| isolated_space_count | 除最大分量外，规模 ≥8 体素的分量数 |
| vertical_connections | 高差 >0 的边数（楼梯步进边 + 梯柱边） |
| dead_end_count | 图中度数为 1 的站位节点数 |

模型细节见 `scripts/walkability.py` 模块 docstring 与 `02_BLUEPRINT_METADATA/feature_extraction_report.md` 的解读注意事项。**分量把屋顶、树梢、围墙顶等露天表面也算作站位**——参考蓝图普遍 components ≥ 2，解读留给 P2 Validator。

## 诊断字段（不在任务书 6.x 内）

`ir_source`（OBSERVED，normalized/canonical）、`walkability_unknown_block_types`（OBSERVED，walkability 分类表未覆盖的 block_id；本次全库 = 0）、`component_sizes_top10`、`class_counts`（walkability 内部统计，随 record 附带的诊断信息在 JSONL 中仅保留前两者）。

## PARSE_FAILURE 结构

```json
{"ref_id": "REF-xxxx", "status": "PARSE_FAILURE", "file": "...", "error": "...", "possible_reason": "..."}
```

本次全量提取 PARSE_FAILURE = 0。
