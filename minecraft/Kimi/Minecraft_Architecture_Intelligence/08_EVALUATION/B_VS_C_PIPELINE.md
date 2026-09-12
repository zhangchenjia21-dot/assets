# B_VS_C_PIPELINE — B（规则约束单轮） vs C（Architect→Critic→Revision）重评对比

> 评测时间：2026-09-13；数据：新 Spatial Validator 实测（`08_EVALUATION/validator_runs/{B,C-before,C-final}/`）+ rubric 机器评分（`evaluation_data.jsonl`）+ `evidence/C-revision-diff.json` 逐坐标差异（已独立复算核对一致）。
> 目标 style/function：B、C 均读自各自 design.md → Residential / Rustic（INFERRED，敏感性对照 Medieval 见 jsonl `style_sensitivity`）。

## 1. 三方 Validator / 评分总览

运行命令（真实执行，输入只读）：

```bash
# 2026-09-13 02:53:46
py -3 .../validate_blueprints.py --input "...\Architecture-V4\C-blueprint-before.json" --output "08_EVALUATION\validator_runs\C-before"
# 2026-09-13 02:53:47
py -3 .../validate_blueprints.py --input "...\Architecture-V4\C-blueprint-final.json"  --output "08_EVALUATION\validator_runs\C-final"
```

| 指标 | B（规则约束） | C-before（首轮） | C-final（终稿） |
|---|---|---|---|
| validation_status | WARNING | **HARD_FAIL** | WARNING |
| hard_fail / warning / info | 0 / 1 / 0 | **1 / 3 / 0** | 0 / 2 / 0 |
| rules_triggered | V004 | **V002(HARD)**, V003, V004, V008 | V004, V008 |
| walkability_score | 98.7 | 95.1 | 94.9 |
| connectivity_score | 96.2 | **0.0** | 50.5 |
| vertical_circulation_score | 100.0 | 100.0 | 100.0 |
| validator_confidence | high | high | high |
| hard_validity（/40） | 34 | **10** | 30 |
| functional（/25，仅 F04 机器评） | 25 | 25 | 25 |
| style（/20，S01/S02/S05/S06 机器评） | 14 | 20 | 20 |
| material（/10，M02/M03 机器评） | 6 | 8 | 8 |
| total_upper_bound（/95） | 79 | 63 | 83 |
| HARD FAIL 封顶 | 不适用 | **cap=40** | 不适用 |
| **total_capped（/95）** | **79** | **40** | **83** |
| 归一化 /100 与等级 | 83.2 GOOD | 42.1 POOR | 87.4 EXCELLENT |

## 2. C-before 的 Validator 问题清单（逐项证据）

| 规则 | 严重级 | 证据（Validator 原文） |
|---|---|---|
| V002 Main Entrance Blocked | **HARD_FAIL** | 唯一入口候选 = 东廊门 voxel(19,3,13)（raw (20,4,15)，facing west）；「门外接近空间不足 outside=[18,3,13]」 |
| V003 Major Interior Unreachable | WARNING（机制降级） | 主入口所在分量仅 0% 内部站位可达（0/232）；隔离环含 3 个可交互构件 → 由 HARD 降 WARNING |
| V004 Isolated Room | WARNING ×2 处 | 128 站位（含 DOOR 环）+ 102 站位（含 TRAPDOOR+DOOR 环）两个封闭空间与主分量断开 |
| V008 Door Clearance | WARNING | 东廊门 (19,3,13) front 向无接近站位 |

**根子上的空间事实**（本次逐坐标核实）：
- 设计意图的庭院主门 raw (13,4,9) 在 C-before 中**门洞上半是玻璃**（(13,5,9)=minecraft:glass，而非 door upper half）——头部高度被实心占据，不是一个可通行的门，因此根本没有进入入口候选列表；C-before 唯一被识别的入口只剩有缺陷的东廊门。
- 东廊门在 C-before 的门外（raw x=19 一列）无合法站位（无门廊/踏步），且门内侧连通分量不含任何内部站位 → 0.0 连通度。

## 3. Revision 是否修复了 C-before 的 Validator 问题？——逐坐标证据

结论：**是。C-final 的 HARD FAIL 从 1 降为 0，且修复是真实几何修复而非口径变化**（两版跑的是同一 Validator、同一 `validator_rules.json`）。

`evidence/C-revision-diff.json` 记录 653 个差异坐标（added 137 / removed 300 / changed 216）；本次用评分脚本对两份 IR 独立复算，**四项数字完全一致**（cross_check_match=true）。与 Validator 问题对应的关键差异：

### 3.1 入口修复（对应 V002 / V003 / V008）

- **庭院主门被修成真正的门**：raw (13,5,9) 由 `glass` → `dark_oak_door[half=upper]`；门槛外侧 raw (13,4,10) 的 bottom slab 移除。→ C-final 中该门成为合法入口候选，并被选为主入口（voxel (12,3,7)，facing south）。
- **东廊墙与门整体东移 1 格**：x=20 一列（raw (20,2..6,11..16) 的墙/地板/门）全部移除，在 x=21 重建（含门 (21,4..5,15)）；原墙内收出的空间成为三格深门廊，另新增 5 格 stone_brick_stairs 踏步（raw (12..14, 2..3, 13..14) 等）。→ 门外接近站位出现，V002 不再触发。
- 对应 C-critique.md 的处置条目：「ADD 三格深门廊」「ADD 偏心入口罩棚、双灯、连续踏步」「中央改成有识别度的入口」「CHANGE 石径终点以匹配新门廊」。

### 3.2 楼梯/塔楼修复（对应 Critic 的 Structural/Proportion 条目）

- **拆除通往第三层的第二段楼梯**：raw x=6/7、y=9..13 的 10 格 `spruce_stairs`（沿 z 递减的上行段）改为 air / spruce_planks；其中 (6,13,9)、(7,13,9) 变为楼板，封住原梯口。
- **塔楼降 3 格**：diff 的 y 分布集中在 raw y=13..18（合计约 340 格），即塔墙顶 Y15→Y12 与攒尖顶同步下降；第三层平台随之消失。
- 注意：C-before 的楼梯**并未**触发 V005/V006（底可进、顶可出——顶格落在第三层小平台上）；该缺陷属于"楼梯通向无意义空间"的语义层，见 §5 Q1 分析。

### 3.3 修复前后指标变化

| 指标 | C-before | C-final | 变化 |
|---|---|---|---|
| hard_fail_count | 1 | 0 | **−1（修复）** |
| warning_count | 3 | 2 | −1 |
| V002 / V003 | 触发 / 触发(0%) | 不触发 / 不触发 | 修复 |
| V004 | 2 处封闭空间 | 1 处（100 站位，环含 DOOR） | 部分修复 |
| V008 | 东廊门 front | 东廊门 front（位移后仍缺正前方接近） | **未完全修复** |
| connectivity_score | 0.0 | 50.5 | +50.5 |
| hard_validity 得分 | 10 | 30 | +20 |

### 3.4 残余问题（诚实声明）

1. **V008 仍触发**：东廊门正前方（facing 轴）仍无同高接近站位；V002 放行是因为 max_drop 容忍内在踏步上找到了接近站位。门廊接近体验仍有改进空间。
2. **V004 仍触发 1 处**：西塔内部 100 站位的封闭空间与主分量断开，隔离环含 1 扇门——很可能只能"出庭院再进门"绕行到达（VALIDATION_SPEC 已声明：经外部绕行的图上连通性存在语义争议）。这是设计性布局（塔楼独立门）还是缺陷，需人工判断。
3. Critic 报告当年的措辞是"可读性/比例"问题，**并未指认**"门洞上半是玻璃""门外无接近空间"这类硬空间缺陷——Revision 在可读性驱动下恰好修复了它们。新 Validator 证明：C-before 存在 Critic 未明确识别的硬缺陷，若当年在 Critic 之前接入本 Validator，这些缺陷会被直接点名。

## 4. revision_cost 的实际定义与数值

按 `06_BENCHMARK/BASELINE_RESULTS.md` §1 定义：`revision_cost` = Critic 建议条数 + Revision 轮数 + 修正前后 diff 方块数。本次实测：

| 组成 | 数值 | 来源 |
|---|---|---|
| Critic 变更动作数 | **10**（ADD 4 / REMOVE 2 / CHANGE 4；KEEP 不计） | C-critique.md 处置表 |
| Revision 轮数 | **1** | summary.md / C-critique.md |
| diff 坐标数 | **653**（added 137 / removed 300 / changed 216） | evidence/C-revision-diff.json，独立复算一致 |
| diff 占终稿坐标比 | 23.5%（653/2782） | 复算 |
| 机器化补充：hard_fail 修复数 | 1（V002） | Validator 两次运行 |
| 机器化补充：hard_validity 得分变化 | +20（10→30） | rubric |

说明：C-before 从未施工，removed 语义是"终稿不再占用该坐标"，不是拆除世界方块（C-critique.md 已声明）。时间成本当年未记录（benchmark.json 只记施工链路毫秒），本报告不伪造。

## 5. Q1 专节：「楼梯尽头是墙」的根因归属分析

> 任务书 §23-Q1：过去为什么会出现"楼梯尽头是墙"？属于建筑生成、方块施工、preview、validator 缺失还是空间推理缺失？
> 本节结合 V006 规则实现机制与 C 路线证据回答。

### 5.1 V006 的实现机制（回答"这类错误现在如何被发现"）

V006 Stair Top Blocked（VALIDATION_SPEC §1，OBSERVED 级）：
1. 全部 STAIR 类体素做 26 连通聚类，过滤出"有通行意义的楼梯簇"（size≥3、y_span≥2、排除屋檐薄板、底部接入主流通）；
2. 对簇内最高 y 的顶格，判定是否存在"可走出"：有合法站位 **且** 存在邻居落点（向上落点 E_m>E_self+0.05，或同级非楼梯支撑平台 E_m≥E_self−0.05）；
3. 全部顶格无出口 → HARD_FAIL（典型"尽头是墙"）；顶格被实体埋住（无 headroom）→ WARNING。

关键点：这是一个**纯几何/拓扑判定**，不需要理解"房间语义"，只需要 walkability 图。"楼梯尽头是墙"在数学上 = 楼梯簇顶格在站位图中无出边。

### 5.2 C 路线证据（V4 真实样本）

- C-before 的楼梯缺陷是"楼梯尽头是墙"的**同族变体**：两段楼梯通向"只有小平台的第三层"（C-critique.md Structural credibility 行：「REMOVE 第三层平台与第二段楼梯」）。新 Validator 复核：C-before 的 V005/V006 **未触发**——顶格落在小平台上，图上有出边。即：该缺陷的"可用性"部分（能站上去）成立，"意义"部分（上去没有功能空间）不成立。
- 该缺陷当年的发现路径：MCP `validate_blueprint`（只查方块 ID/state/地形合法性）判 `valid=true` → 离线体素 preview（2D 投影 PNG）用于人工/模型审查 → **Critic 在语义审查中发现**并以 REMOVE 处置。施工环节从未参与（C-before 从未施工；三栋终稿施工后 9,478 坐标全量核对一致）。
- 同一 C-before 上还共存着 Critic 未点名的硬缺陷（门洞上半是玻璃、门外无接近站位），由本次新 Validator 补刀发现（§3）。

### 5.3 根因归属结论

| 候选环节 | 是否根因 | 证据 |
|---|---|---|
| 建筑生成（Architect） | **主因** | 楼梯/门洞按局部模式逐段放置，放置后不验证"顶端是否有可达目的地"；C-before 第二段楼梯、玻璃封顶的门洞都是生成产物 |
| 空间推理缺失 | **主因（生成的内在机制）** | 生成过程缺"通路必须有可达终点"的全局推理；属于生成侧能力缺口，不是独立环节 |
| Validator 缺失 | **放大器/次因** | V4 时代只有合法性 validate，无拓扑检查；硬缺陷一路漏到 Critic 甚至漏过 Critic（V002/V008 类） |
| 方块施工 | **排除** | C-before 从未施工；A/B/C 终稿施工坐标 9,478 个全部一致（benchmark.json），错误在施工前已存在于蓝图 |
| Preview | **排除（但无功）** | preview 是 2D 可视化而非检查器；它能让人看见问题（Critic 确实用了它），但不会主动报警 |

**一句话结论**："楼梯尽头是墙"= 生成阶段缺乏全局可达性推理（主因）+ 验证层没有空间拓扑检查（放大器）；与施工、preview 无关。其中"顶格被墙堵死/无 headroom"子类现在可由 V006（及 V005/V007）**确定性检测**；"楼梯通向无意义小平台"这类语义子类**仍需 Critic**——C 路线的价值正在于这两层互补，这也是 §23-Q3/Q4 分工判断的实证基础。

## 6. B vs C 路线结论（基于 4 个历史样本，非完整 benchmark）

- 单轮规则约束 B：无 HARD FAIL，1 个 WARNING，机器总分 79/95。一次成型，revision_cost=0。
- C 路线：首轮出现 1 个 HARD FAIL（当年无人识别其为硬错误），一轮 Revision 后修复至 0 HARD FAIL + 2 WARNING，机器总分 40 → 83/95，revision_cost = 10 个变更动作 / 1 轮 / 653 坐标（23.5%）。
- 本次证据支持任务书的既有分工（§22）：**默认 B、复杂项目转 C**；同时表明把 Hard Validator 嵌入 C 路线的 Architect→Critic 之间（§17 Revision Protocol），可以让 Revision 由"审美驱动碰巧修复"变成"硬错误点名必修"。
- 样本量声明：n=1（B）/ n=1（C），以上为历史个案证据，不构成统计结论；完整 benchmark 运行见 Phase 8 后续。
