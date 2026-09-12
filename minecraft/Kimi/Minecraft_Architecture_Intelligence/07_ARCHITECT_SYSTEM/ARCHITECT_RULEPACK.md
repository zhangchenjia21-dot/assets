# ARCHITECT_RULEPACK — 生成侧规则包（项目代号 H · P5）

> 配套机读文件：`architect_rules.json`（218 条，由 `build_rulepacks.py` 生成，数值直接拷贝自
> grammar/validator 产物，可追溯、可抽查）。
> 上游来源：`04_GRAMMARS/style_rules.json`（111 条）、`04_GRAMMARS/functional_rules.json`（117 条）、
> `04_GRAMMARS/grammar_confidence_report.md`、`05_SPATIAL_VALIDATOR/validator_rules.json`（V001–V012）、
> `05_SPATIAL_VALIDATOR/VALIDATION_SPEC.md` 与 `known_limitations.md`、`03_TAXONOMY/`、`CONTEXT.md`。

## 0. 使用总则

1. **每条规则带 8 个字段**：`id / category / type(HARD|STRONG|SOFT|OPTIONAL) / statement / source /
   confidence / basis / applies_to`；数值类另带 `stats{median,p25,p75,min,max,sample_n}`。
2. **type 语义**（任务书第 20 节）：HARD=功能必需，STRONG=高频稳定规律，SOFT=常见可打破，
   OPTIONAL=装饰倾向。HARD 不可违反；SOFT/OPTIONAL 可权衡但需在提交说明中声明。
3. **可追溯纪律**：`source.rule_id` 指向上游真实规则（grammar rule_id 或 V001–V012）；
   脚本内置自检，凡引用不存在的 rule_id 即拒绝生成。**禁止手写无 source 的规则。**
4. **UNKNOWN 纪律**：grammar 标 UNKNOWN 的维度，本包同样标 UNKNOWN（见第 9 节清单），
   不编数值规则，交给 LLM 自由发挥或人工。
5. **生成即合规**：global/circulation/vertical 三组规则与 Validator V001–V012 一一对应——
   按本包生成，提交时 Validator 不应再报 HARD_FAIL。

## 1. 八个规则组

### 1.1 global_architecture_rules（13 条，GA-001…GA-013）

任何建筑通用的生成约束，全部映射到 Validator 或工程上限：

| id | type | 要点 | source |
|---|---|---|---|
| GA-001 | HARD | 包络 ≤128 边 / ≤1,000,000 体素 / 施工 ≤20,000 | CONTEXT.md §7 |
| GA-002 | HARD | 至少一个 exterior→interior 入口 | V001 |
| GA-003 | HARD | 主入口内外各留接近站位（高差 ≤1.0） | V002 |
| GA-004 | HARD | 主内部空间与主入口同分量，覆盖 ≥50% 内部站位 | V003 |
| GA-005 | HARD | 不留 ≥20 内部站位的纯实体封闭孤立空间 | V004 |
| GA-006 | HARD | 门两侧通行轴上都有接近站位；避免贴墙假门 | V008 |
| GA-007 | STRONG | 主要通路净高 ≥2 格 | V009 |
| GA-008 | STRONG | 围护完整；无玻璃窗洞 = 真实泄漏 | V010 |
| GA-009 | STRONG | 内部空间上方有屋顶覆盖；有意天井需标注 | V011 |
| GA-010 | SOFT | 内部死端站位 <15 | V012 |
| GA-011 | STRONG | 主动线不依赖铁门/活板门等红石机关语义 | known_limitations §1.4 |
| GA-012 | SOFT | 入口/梯底落在 y=0 或有支撑，不悬空 | known_limitations §1.1 |
| GA-013 | SOFT | 不依赖跳跃/游泳/潜行通过主动线 | known_limitations §1.5 |

### 1.2 style_selection_rules（7 条，SS-001…SS-007）

brief → grammar 的检索与回退决策：

- **SUPPORTED**（Medieval n=19 / Rustic n=20 / Fantasy n=10）：正常用规则，取 median 与 IQR。
- **PROVISIONAL**（Japanese n=7 / Chinese n=4）：全部降格为咨询性，标注"grammar 置信度低"，
  目标落在 IQR 内即可，不追求 median。
- **OBSERVATION ONLY / 零样本**（Other n=7 异质；Modern/Industrial/Gothic/Victorian/Nordic 0 样本）：
  **无 style grammar**。回退 = global_architecture_rules + functional grammar + LLM 自由发挥，
  交付说明必须标注"style grammar 无背书"，禁止编造数值。
- 功能类回退：Gate/Blacksmith/Farm/Mixed-use/Warehouse 样本 <4 无规则；Inn/Civic/Workshop/Vehicle
  为 PROVISIONAL。缺失时回退到 SUPPORTED 功能类作参考并标注来源（SS-007）。
- 风格标签歧义（conf<0.55 的降级判例存在于 label_summary.json）：先确认或显式声明假设（SS-005）。

### 1.3 function_rules（72 条，FUNC.{class}.{dimension}）

从 functional_rules.json 逐条转换（9 个功能类 × 8 个生成相关维度）：
`required_zones.enclosed_interior / required_zones.exterior_door / optional_zones.upper_floor /
optional_zones.courtyard / public_private_separation / entrance_relation.exterior_door_count /
vertical_access.presence / vertical_access.means`。

使用要点：
- 房间语义（bedroom/kitchen）不可识别，grammar 不声称——生成侧也不许声称"按 grammar 布置了厨房"。
- `public_private_separation` 全部为 INFERRED（"楼上=私密"是常识推断），只能作 SOFT 指导。
- Decoration/Vehicle 类的规则多为**负向画像**（无门/无室内），这本身是功能特征，不要给它们强加门和房间。

### 1.4 circulation_rules（39 条）

= 36 条转换自 grammar（`zone_adjacency.largest_component` / `zone_adjacency.isolated_spaces` /
`circulation_constraints.dead_end_ratio` / `circulation_constraints.usable_floor_area`）
+ 3 条生成侧规则（CIR-G-01…03，对齐 V003/V012 及 VALIDATION_SPEC V003 盲区）。
核心：主入口直达主空间；内部空间之间走内部通道，"出后门绕行"不算好动线；死端比例对照功能类 IQR。

### 1.5 vertical_access_rules（14 条）★ "楼梯尽头是墙"的生成侧预防

= 9 条转换自 grammar（`vertical_access.multifloor_requires`）+ 5 条生成侧规则：

| id | type | 要点 | source |
|---|---|---|---|
| VA-G-01 | HARD | 楼梯底部可进入：底格至少一格有站位且邻位高程 ≤底格+0.55 | V005 |
| VA-G-02 | HARD | **楼梯顶部有落点+净高：先放落点平台再接楼梯** | V006 |
| VA-G-03 | STRONG | 顶部唯一出口不要是关闭的活板门舱口 | known_limitations §2 V006 |
| VA-G-04 | HARD | ≥2 可用楼层 ⇒ 全部与第一层同连通分量 | V007 |
| VA-G-05 | SOFT | 梯井出口处留 1 格平台 | VALIDATION_SPEC §3 fix2 |

### 1.6 roof_rules（21 条）

= 5 风格类 × 4 个屋顶维度（`roof_height_ratio / roof_material_share_top3 / roof_overhang /
roof_overhang_ratio`）共 20 条转换规则 + 1 条 UNKNOWN 元规则（STY.ROOF.UNKNOWN.roof_form）。
**屋顶形制（歇山/悬山/攒尖/坡度曲线）全风格 UNKNOWN**——不编规则，LLM 依据风格常识自由发挥。

### 1.7 palette_rules（40 条）

5 风格类 × 8 个材料维度（`palette_wood/stone/glass/decorative_ratio / palette_top_blocks /
material_transition / foundation_bottom_family / foundation_stone_base`），全部带 sample_n 与 IQR。
示例：Medieval stone 占比 median 0.589，IQR[0.389,0.625]，n=19（源 STYLE.Medieval.palette_stone_ratio）。

### 1.8 validator_precheck（12 条，PC-V001…PC-V012）

生成后、提交前的自检清单，与 V001–V012 一一对应；每条带 `validator_severity`、
`validator_params`（真实阈值）与 `fail_condition`。顺序执行，任一 HARD 项不通过则不提交。
**PC-V006（楼梯顶部）是重点自检项。**

## 2. UNKNOWN 维度清单（不编规则，交 LLM/人工）

| 维度 | 类别 | 原因 | 处置 |
|---|---|---|---|
| window_rhythm | 全部 5 风格类 | 窗洞位置节奏需立面聚合，P3 未做 | LLM 自由发挥/人工 |
| entrance_placement | 全部 5 风格类 | main_entrance 可判定样本过少（全库 89% UNKNOWN） | LLM 自由发挥/人工 |
| floor_height | Medieval/Fantasy/Chinese | 可得样本不足半数或 <4 | LLM 自由发挥/人工 |
| floor_count | Chinese | 可得样本 3/4 | LLM 自由发挥/人工 |
| roof_form（形制/坡度） | 全部 5 风格类 | 未测量 | LLM 自由发挥/人工 |
| 全部维度 | Other/Modern/Industrial/Gothic/Victorian/Nordic | 异质或 0 样本 | 回退策略 SS-004 |
| entrance_relation.方位 | 全部 9 功能类 | main_entrance 可判定样本过少 | LLM 自由发挥/人工 |
| 全部维度 | Gate/Blacksmith/Farm/Mixed-use/Warehouse | 样本 <4 | 回退策略 SS-007 |

机读版见 `architect_rules.json` 的 `unknown_dimensions` 字段。

## 3. 规则计数（category × type）

| category | HARD | STRONG | SOFT | OPTIONAL | 小计 |
|---|---:|---:|---:|---:|---:|
| global_architecture_rules | 6 | 4 | 3 | 0 | 13 |
| style_selection_rules | 3 | 2 | 2 | 0 | 7 |
| function_rules | 0 | 6 | 39 | 27 | 72 |
| circulation_rules | 1 | 2 | 36 | 0 | 39 |
| vertical_access_rules | 4 | 1 | 8 | 1 | 14 |
| roof_rules | 1 | 0 | 16 | 4 | 21 |
| palette_rules | 0 | 4 | 30 | 6 | 40 |
| validator_precheck | 7 | 5 | 0 | 0 | 12 |
| **合计** | 22 | 24 | 134 | 38 | **218** |

## 4. 与 Critic 的职责边界（显式声明）

Architect Rulepack 与 Validator 管"客观正确性"；设计是否合理（层级/节奏/比例/焦点）归
`CRITIC_RULEPACK.md`。Critic 不重复 V001–V012 的检查；本包也不评审美。
