# VALIDATION_SPEC — Spatial Validator 判定规范（项目代号 H · P2）

> 实现位置：`validator_source/`（`spatial_context.py` / `rules.py` / `core.py` / `validate_blueprints.py`）
> 阈值配置：`../validator_rules.json`（全部阈值外置，代码内无硬编码）
> 底层模型：`../../scripts/walkability.py`（P1 可通行模型，P2 只读复用 + 三处兼容性修复，见文末）
> 数据约定：Canonical IR schema_version=1，分析一律优先 `normalized/normalized-blueprint.json`；
> 坐标为蓝图局部坐标，原点 = 包络最小角。

## 0. 共享空间事实（SpatialContext）

每条规则都建立在同一份预计算事实上：

| 概念 | 定义 |
|---|---|
| 实体 / 空气 | block_id ∈ {air, cave_air, void_air} 为空气，其余为实体 |
| exterior air | 空气 6 连通洪泛，种子 = 包络边界 |
| interior air | 空气 ∧ ¬exterior air（洪泛语义下的封闭空气） |
| 站位（stance） | walkability 模型的合法站立点：支撑体素 u + 高程 E = u.y + surface(u)，净高 ≈1.8 |
| **内部站位** | 站位的身体格 u+1 落在 interior air 中。**这是 V004 不误杀屋顶/树梢的关键**——露天表面形成的天然连通分量全部不计入 |
| 站位图 | 节点=站位；边=水平 4 邻（ΔE≤0.5，楼梯助推 ≤1.0）+ 梯柱垂直边（同高程组间完全二部连接） |
| 主内部连通分量 | **主入口内侧站位所在分量**；无入口时退化为最大内部分量 |
| 楼梯簇 | STAIR 类体素的 26 连通聚类 |
| 有通行意义的楼梯簇 | size ≥ min_cluster_size 且 y_span ≥ min_y_span 且 size ≤ max_blocks_per_level×(y_span+1)（排除屋檐/镶边大面积楼梯薄板）且底部站位接入主流通 |
| 楼层 | P1 同法：y 层实体占比 ≥ 0.30 → 楼板候选，组顶+1 为行走面，间隔 <2 合并 |
| 低净高格 | 有支撑但站位非法、且身体格为内部空气的体素 |
| 隐含地面假设 | 门/开口在包络最底层（y=0）时按站在隐含地形上处理（参考蓝图通常不含地形） |

入口候选（优先级从高到低）：
1. **严格外门**：门 facing 通行轴一侧为 exterior air，另一侧为任意空气（open 门通行轴垂直于 facing）；
2. **宽松外门**：仅一侧 exterior air；
3. **无门开口**：interior air 格与 exterior air 格同层 4 邻接且两侧下方均有合法站位；
4. **梯子舱口**：梯柱部分格 6 邻接 interior air、部分格 6 邻接 exterior air。

主入口 = 候选列表第一个。内侧空气**不要求** flood 判定为 interior（带无玻璃窗/拱洞的建筑
内部空气会被洪泛吸收成 exterior，实测 REF-0003 农舍即如此，强制 interior 会系统性误报）。

## 1. 逐规则算法

### V001 No Exterior Entrance — HARD_FAIL（HEURISTIC）
- 适用条件：interior_air ≥ `min_interior_air`(27) **且** interior_stances ≥ `min_interior_stances`(9)。
  后者排除爬空间/结构缝隙（判不出"房间"就不算无入口）。
- 判定：无任何入口候选（外门/开口/舱口）→ 触发。
- 盲区：完全密封但作者意图是"后期开门"的壳体建筑会触发；装饰性空腔（空心树、陵墓
  墓室）会触发——客观事实正确，语义意图需人工判断。垂直开口（无梯子的天井口）不识别。

### V002 Main Entrance Blocked — HARD_FAIL（HEURISTIC）
- 适用条件：存在入口候选；否则 NOT_APPLICABLE（由 V001 负责）。
- 判定（门）：门槛站位存在（门在 y=0 时按隐含地面视为存在）＋ 门外接近站位 ＋ 门内接近站位
  ＋ 两侧同分量。接近站位允许脚部高程 ∈ [y−`max_drop`(1.0), y+0.6]。
- 判定（开口）：两侧接近站位存在且同分量。
- 判定（舱口）：梯柱周边 Chebyshev≤2、y±2 内同时存在内/外部站位；失败只给 **WARNING**
  （舱口的"前后通行空间"语义与门不同，静态判定置信度低）。
- 盲区：门外 2 格以上的台阶/坡道接近路径不识别（只查门边）；假门面（贴墙装饰门）会触发。

### V003 Major Interior Unreachable — HARD_FAIL/WARNING（HEURISTIC）
- 适用条件：interior_stances ≥ `min_interior_stances`(9) 且有入口候选。
- 判定：主入口内侧站位所在分量（隐含地面时取最大内部分量）的内部站位占比 <
  `max_reachable_ratio`(0.5) 且不可达站位 ≥ `min_unreachable_stances`(9) → 触发。
- 分级：不可达分量的隔离环（身体格 1 圈邻域）上若出现门/活板门/梯子/栅栏门等可交互
  构件（可能经模型未覆盖的通道相连）→ 降 WARNING；纯实体封闭 → HARD_FAIL。
- 盲区：主入口选错（多入口建筑选了次要入口）会改变分子；内部空间经外部绕行（出后门
  再进侧门）在图上是连通的，不算不可达（语义上是否算"内部可达"存疑，见 known_limitations）。

### V004 Isolated Room / Space — HARD_FAIL/WARNING（HEURISTIC）
- 适用条件：存在内部站位。**露天分量一律不计**（P1 实测：屋顶/树梢等露天表面会形成
  大量天然分量，全库误报的主要源头）。
- 判定：主内部连通分量之外，内部站位 ≥ `warn_min_stances`(9) 的分量 → 触发。
- 分级：隔离环含可交互构件 → WARNING；纯实体封闭且 ≥ `hard_min_stances`(20) → HARD_FAIL。
- 盲区：装饰性密封空腔（树腔、墓室、船底舱）客观成立、意图未知；1 格高爬空间不形成
  站位所以不计；地毯+门组合等导致的建模外断连可能残留。

### V005 Stair Bottom Blocked — HARD_FAIL（OBSERVED）
- 适用：有通行意义的楼梯簇；`skip_bottom_at_envelope_floor`(true) 时底格全在 y=0 的簇跳过
  （入口在隐含地形上）。
- 判定：底格（簇内最低 y 的全部体素）中存在**至少一格**可进入即通过——可进入 = 有合法
  站位且存在相邻站位 E_m ≤ E_self+0.55（可走上/平级踏上），且该邻居不是同簇更高一级。
  全部底格不可进入 → 触发。
- 盲区：底格在包络内部但建筑架空（塔楼底层入口梯从 y>0 开始而下方无支撑）时可能误报；
  底部紧邻被关闭铁门拦住的入口会判堵（铁门语义见 walkability）。

### V006 Stair Top Blocked — HARD_FAIL/WARNING（OBSERVED）★ 重点规则
- 对应真实失败案例"楼梯尽头是墙"。
- 判定：顶格（簇内最高 y）中存在至少一格可走出即通过——可走出 = 有合法站位且存在邻居
  E_m > E_self+0.05（向上落点），或 E_m ≥ E_self−0.05 且支撑非楼梯（同级半砖/平台落点）。
  全部顶格无出口 → 触发。
- 分级：顶格站位存在但无出口 → **HARD_FAIL**（典型"尽头是墙"）；顶格站位全部被实体埋住
  （无 headroom）→ **WARNING**（可能是檐口/柱体装饰纹理埋梯）。
- 回归夹具 `stair_top_blocked` 必现：顶端三面砌墙，HARD_FAIL 稳定触发。
- 盲区：顶部经活板门舱口继续向上（关着的木活板门在模型里是半砖实体）会判堵——
  玩家实际可翻开；宽楼梯的"可走出"判定只看顶格一行，弧形楼梯的侧向出口已覆盖。

### V007 Vertical Circulation Broken — HARD_FAIL（HEURISTIC）
- 适用条件：interior_stances ≥ `min_interior_stances`(9)（纯露天结构的高差不计入——
  树冠/桥面的"层"不是楼层）；楼层检测 UNKNOWN → NOT_APPLICABLE。
- 判定：可用楼层（该层内部站位 ≥ `min_floor_stances`(6)，|E−楼层高程| ≤ `level_tol`(0.6)）
  ≥2 且各层站位集合的分量无交集 → 触发。
- 盲区：楼层密度启发式会把密实屋顶/树冠层误检为"楼板"（REF-0042 圣诞树即如此）；
  跳跃类垂直动线（跑酷式设计）不建模。

### V008 Door Clearance Failure — WARNING（HEURISTIC）
- 判定：每扇门沿 facing 通行轴（open 门取垂直轴）检查两侧：空气侧无接近站位 → 记缺。
  两侧皆实体 = 装饰性贴墙门，跳过。任一侧缺失 → 触发。
- 盲区：双开门两扇分别判定；门前有地毯/雪层时接近判定偶有偏差。

### V009 Severe Headroom Failure — WARNING（HEURISTIC）
- 判定：低净高格数 ≥ `min_cells`(12) 且占内部站位比 ≥ `min_ratio`(0.35) → 触发。
- 盲区：低净高格的定义是"有支撑但站不直"，无法区分"通道净高不足"与"装饰性夹层/阁楼
  地板下的暗格"；该规则只作 WARNING 级提示。

### V010 Exterior Envelope Gap — WARNING（HEURISTIC）
- 适用条件：interior_air ≥ `min_interior_air`(27)，否则 NOT_APPLICABLE（开放式建筑：
  桥梁/雕塑/露台/门廊不误杀）。
- 判定：泄漏格 = interior air 与 exterior air 6 邻接；排除门/开口周边 `opening_margin`(1)
  格的设计性开口后，泄漏 ≥ `min_gap_voxels`(10) 且 ≥ `min_gap_ratio`(0.02)×interior_air → 触发。
- 盲区：无玻璃的开窗是真实泄漏（与"围护断裂"不可区分）；大幕墙缺口若通向被洪泛判定为
  exterior 的大厅则不计。

### V011 Roof Coverage Anomaly — WARNING（HEURISTIC）
- 适用条件同 V010。
- 判定：含内部空气的 (x,z) 柱中，最高内部空气格上方无任何实体 → 无屋顶柱；柱顶到包络
  上界的记为 boundary_truncated（蓝图截断，单列不计）。无屋顶柱 ≥ `min_columns`(12) 且占
  内部柱 ≥ `min_ratio`(0.2) → 触发。
- 盲区：天井/中庭（设计性露天室内）会触发；屋顶上方另有高层建筑遮挡时不影响判定
  （只看柱内实体）。

### V012 Dead-end Circulation Anomaly — INFO/WARNING（HEURISTIC，标 HEURISTIC）
- 判定：只统计**内部**死端（度数为 1 的内部站位；露天端部如屋脊/树梢天然大量度数 1，
  不计）。≥ `info_min`(6) → INFO；≥ `warn_min`(15) → WARNING。
- 盲区：死端≠设计错误（壁龛、房间尽头、储藏室都是死端）；本规则本质上是统计提示。

## 2. 输出字段（任务书第 11 节）

每张蓝图输出 `validation_status / hard_fail_count / warning_count / info_count /
rules_triggered / walkability_score / connectivity_score / vertical_circulation_score /
validator_confidence`，另加 `diagnostics`（站位数、楼层、门/梯计数等）与逐规则明细。

评分定义（0–100 或 UNKNOWN）：
- `walkability_score` = 100 × 合法站位 / 潜在站位（提供支撑且正上方无实体的体素——
  "真正能站的位置"中被净高等因素淘汰的比例）。
- `connectivity_score` = 100 × 主内部分量站位 / 全部内部站位；无内部站位时退化为
  100 × largest_component_ratio。
- `vertical_circulation_score` = 可用楼层 ≤1 → 100；否则 100 × 与第一层同分量的可用
  楼层占比；楼层 UNKNOWN 或无内部站位 → UNKNOWN。
- `validator_confidence` = 未知方块 0 种 high；≤3 种 medium；否则 low
  （未知方块保守按实体处理，越多越可能误判阻挡）。

## 3. 对 P1 walkability.py 的三处兼容性修复（P2 校准期间实证驱动）

1. `return_graph=True` 可选返回站位图边数组（新增，不改既有输出）。
2. **梯子链式边修复**：旧实现同柱站位按高程排序链式相连，同一高度多个站位（梯井两侧
   不同房间）只有排序相邻的一个被挂到上一级，其余漏接（REF-0005 守卫房实测漏接）。
   修复为相邻高程组间完全二部连接。test_walkability 11/11 保持绿。
3. **栅栏门语义**：closed 栅栏门由"阻挡"改为"可交互开启 → 可过"，与 P1 既有的非铁质
   门语义对齐（玩家可开）。实测修复 REF-0009 等一批楼梯顶部被关闭栅栏门拦住的误报。

注意：P1 `blueprint_metadata.jsonl` 中的连通性字段是修复前模型计算的；如需严格一致，
重跑 P1 extract 即可（本阶段未重跑，差异已在已知限制中声明）。

## 4. 校准迭代记录（hard_fail_rate 轨迹）

| 迭代 | 修复 | hard_fail_rate |
|---|---|---|
| 0 | 初版 | 0.829 |
| 1 | 梯子二部连接 + 门内侧空气不限 interior + V005/V006 任一可进/可出 + 紧致性门控 + V007 内部站位门控 | 0.659 |
| 2 | 门 facing 通行轴 + open 门轴旋转 + 包络底界隐含地面 + V008 通行轴化 | 0.626 |
| 3 | V001 加内部站位门控 + V008 排除全嵌墙装饰门 | 0.577 |
| 4 | V003/V004 机制感知分级（隔离环含门/活板门/梯子/栅栏门 → WARNING） | 0.529 |
| 5 | 舱口主入口 clearance 降为 WARNING + 邻域放宽 | 0.529 |
| 6 | 栅栏门可交互 + V005 入口语义（≤E+0.55）+ 包络底界楼梯跳过 + V006 埋梯降 WARNING | 0.496 |
| 7 | 主内部分量锚定主入口（V004/connectivity_score） | 0.496（稳定） |
