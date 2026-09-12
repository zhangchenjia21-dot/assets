# B_VS_C_OFFLINE_RUN — B vs C 离线生成对比实验报告（P6 阶段第二部分）

> 日期：2026-09-13 ｜ 状态：**已完成（真实运行，全部数字可复算）**
> 数据：`08_EVALUATION/evaluation_data.jsonl`（24 条新记录，含逐子项中间值）、
> `08_EVALUATION/p6b_summary.json`（汇总）、`08_EVALUATION/generated/`（IR 蓝图与 traces）。

## 0. 诚实性声明（先读）

- 本实验的生成器是 **programmatic reference generator (rule-driven)**——
  `scripts/generate_blueprint.py`，一个由 `architect_rules.json` 数值区间 +
  `style_rules.json` 实测区间 + brief 约束驱动的**确定性参数化算法**。
  **它不是 LLM Architect**，其产出质量是"规则直译"的工程天花板，
  不代表也不暗示任何 LLM 的水平。任务书 §18 的 B/C 对比在此验证的是
  **管线闭环**（Validator→Critic→Revision→Recheck 是否机器可通、是否有差异），
  不是生成智能的上限。
- 全程离线：零写入 `D:\Games`、零世界写入；产物全在 `$OUT`。
- B 与 C 的初稿**逐方块一致**（同一生成器同一参数）。两者差异只来自
  C 路线的 Validator 触发修订。若 B 无缺陷，则 C == B（如实成立：
  12 条中 11 条 `generated/B/*.json` 与 `generated/C/*.json` 逐字节相同）。

## 1. 实验设计

- **样本**：dev split（30 条）内选 12 条——4 Easy / 5 Medium / 3 Hard，
  覆盖 6 个功能域（Residential / Workshop / Hospitality / Constrained Plot /
  Mixed-use / Civic），含 3 条 `targets_gap=true`（BRIEF-0043/0053/0065）。
  清单：`run_benchmark.py.SELECTED`。
- **路线 B**（规则约束单轮）：生成 → Validator → rubric 评分。不返修。
- **路线 C**（`REVISION_PROTOCOL.md` 的程序化实现）：
  生成 → Validator → 有 HARD_FAIL/可修 WARNING 则 `revise_blueprint.py` 修订
  （体素级 patch 或带 overrides 重生成）→ Validator **Recheck（真实重跑）**
  → 无客观错误后进程序化 Critic（rubric 机器子项驱动）→ 收敛或 3 轮上限。
  锚点（footprint/风格/分区清单）逐轮校验；diff>30% 触发回退（本次未触发）。
- **评分口径**：`scoring_rubric.json` 五维全机器评（hard 40 / functional 25 /
  style 20 / material 10 / efficiency 5），封顶策略不变（1/3/5 个 HARD FAIL →
  40/25/10 封顶）。与 `score_v4_samples.py` 同口径，差异仅在：生成样本有机器
  可读 brief 与生成方案记录（IR `metadata.generation`），S03/S04/S07、M01、
  E01–E03、F01/F02/F03/F06 从"未评"升级为机器可评（面积/开口均用体素几何复核，
  不只信声明）；F05（公私分区）维持 LLM_ONLY——grammar 明确其 IR 不可判。
  zone 语义判定用了 `metadata.generation.rooms`（生成器 ground truth），
  这是相对 V4 评分口径的**已知增强**，在每条记录的 `scores.*.note` 中标注。

## 2. 生成器算法说明（`scripts/generate_blueprint.py`）

管线：`plan_from_brief`（平面规划）→ `build_voxels`（体素构建）→
`seal_envelope`（洪泛密闭自检）→ `fit_palette`（材料族占比确定性拟合）→ IR 输出。

1. **footprint 搜索**：满足 zone 容量（Σmin_area×1.3）、E03 投影占比 [0.3,0.9]、
   风格 footprint_ratio 区间（优先 IQR）、直跑楼梯跑道可行性（内墙线 ≥ fh+1）。
2. **层高/屋顶剖面**：fh ∈ brief assumed_floor_height 附近（≥4，保证净高 ≥3）；
   坡度候选 1:1/2:1/3:1/4:1（curved_* 用变坡阶梯近似）；总高 ≤ max_height，
   屋顶占比优先落入 brief 区间（S04），其次避免屋面密层被楼层启发式误检
   （S06，见 §5 局限 3）。
3. **分区**：zone→楼层（公共簇在下、私密在上、邻接对并查集同层、禁配对分层）；
   层内带状 guillotine 切分（带间留 1 格隔墙厚度），邻接带之间开 1×2 门洞，
   禁配对无开口；主入口落入最公共带（CIR-G-01）。
4. **垂直交通**：直跑梯沿外墙内侧落位（计划层检查：跑道+接近格可行、不撞门
   clearance；**不检查顶步三维落点余量**——单轮盲区，见 §5）；放不下时退化为
   折返楼梯塔（双柱逐层换向，上段底步=下段顶步的侧邻，V006 天然满足）。
   顶部两步上方楼板开洞（净高传递）。
5. **围护**：外墙石基座+石木混砌（fraction 为拟合旋钮）；屋顶逐柱梯形覆盖
   （踏步沿=楼梯、踏面=半砖，每柱必有面层），墙线柱在面层以下填实
   （山墙三角与檐口楔统一封口）；`seal_envelope` 洪泛兜底（门 ±1 格保护，
   口径同 V010 opening_margin）。
6. **功能构件**：主入口 DOOR + 门外 2×3 门廊（V002 接近位）；外部 zone
   （如 watch_platform）实现为顶层**阳台平台**（悬挑板+栏板+墙上 DOOR 门——
   无门开口会让内外洪泛互通，P2 教训）。
7. **材料拟合**：族占比对照 brief 区间，旋钮迭代（楼板石比/墙木比/地毯覆盖/
   屋顶族/窗密度，方向反转步长减半）→ 逐格 polish → 双参数网格兜底；
   拟合历史全记录，残留偏差保留进评分（不掩饰）。

## 3. 结果（真实数字；复算入口见 §6）

### 3.1 逐条对比表

| brief_id | 难度 | 功能域 | 风格 | gap | B: hard_fail | B: 五维（40/25/20/10/5） | B: total | C: hard_fail | C: total | revision_cost（轮/变更方块） |
|---|---|---|---|---|---|---|---|---|---|---|
| BRIEF-0006 | Easy | Residential | Medieval | | 0 | 40/25/17/10/5 | 97 | 0 | 97 | 0/0 |
| BRIEF-0037 | Easy | Workshop | Rustic | | 0 | 40/25/17/10/5 | 97 | 0 | 97 | 0/0 |
| BRIEF-0053 | Easy | Hospitality | Rustic | ✓ | 0 | 40/25/17/10/5 | 97 | 0 | 97 | 0/0 |
| BRIEF-0091 | Easy | Constrained | Medieval | | 0 | 40/25/17/10/5 | 97 | 0 | 97 | 0/0 |
| BRIEF-0017 | Medium | Residential | Rustic | | 0 | 40/20/20/10/5 | 95 | 0 | 95 | 0/0 |
| BRIEF-0030 | Medium | Mixed-use | Chinese | | 0 | 40/25/11/10/5 | 91 | 0 | 91 | 0/0 |
| BRIEF-0056 | Medium | Hospitality | Japanese | | 0 | 40/25/17/10/3 | 92 | 0 | 92 | 0/0 |
| BRIEF-0065 | Medium | Civic | Rustic | ✓ | 0 | 40/25/14/10/5 | 94 | 0 | 94 | 0/0 |
| BRIEF-0096 | Medium | Constrained | Medieval | | 0 | 40/20/17/10/5 | 92 | 0 | 92 | 0/0 |
| BRIEF-0043 | Hard | Workshop | Rustic | ✓ | 0 | 40/25/17/10/5 | 97 | 0 | 97 | 0/0 |
| BRIEF-0068 | Hard | Civic | Rustic | | 0 | 40/25/17/10/5 | 97 | 0 | 97 | 0/0 |
| BRIEF-0099 | Hard | Constrained | Japanese | | **2（V002/V003）** | 16/22/14/10/5 | **40（封顶）** | **0** | **91** | 1 轮 / 6 方块 |

### 3.2 汇总（n=12/路线）

| pipeline | hard_fail_rate | validator_score(/40) | functional_score(/25) | style_score(/20) | material(/10) | efficiency(/5) | mean total(/100) | revision_cost |
|---|---|---|---|---|---|---|---|---|
| B（规则约束单轮） | 0.083 | 38.00 | 23.92 | 16.25 | 10.00 | 4.83 | 90.75 | n/a |
| C（→Validator→Revision→Recheck） | **0.000** | **40.00** | 23.92 | 16.25 | 10.00 | 4.83 | **95.00** | 0.08 轮 / 0.5 方块（均值） |

- **C 修复成功率：1/1 = 100%**（唯一硬缺陷样本 BRIEF-0099：B 总分 40 POOR →
  C 91 EXCELLENT；修订 = 阳台门沿墙平移 3 格，1 轮、变更 6 方块、
  diff_ratio 0.74%、锚点三项不变；traces 见 `generated/_traces/BRIEF-0099/`）。
- **如实陈述**：12 条中 11 条 B 本就零硬缺陷（规则直译 + 生成侧密闭自检覆盖了
  绝大多数校验项），B vs C 的差异完全由 1 条 Hard 紧张地块样本驱动。
  **样本量小，不构成统计结论**；它证明的是闭环可用、修订代价极小，
  而不是"C 路线普遍优于 B"。

### 3.3 B 路线缺陷分布（11 条 PASS 样本的残留扣分，两路线相同）

| 子项 | 次数 | 性质 |
|---|---|---|
| S06 楼层数误检 | 8 | **评分启发式伪阳性**（梯形屋顶密层/地毯层被楼层密度法误检为楼板；S06 caveat 已文档化） |
| S04 屋顶占比出界 | 3 | 真实 brief 张力：大平地 + 全覆盖坡顶 + 限高（0043/0065/0068） |
| S05 高宽比出界 | 2 | 0065（gap，GENERALIZATION_CASE 宽松判仍出界）、0099（细高塔楼） |
| S02 footprint 出 IQR | 2 | 0030/0096（容忍区间内、IQR 外） |
| F02 邻接不满足 | 2 | 0017/0096：紧张地块容量-邻接冲突（分区被容量回退拆到不同层） |
| F06 分区面积不足 | 2 | 0017/0096：同一张力的面积维度 |
| E03 投影略超 0.9 | 1 | 0056 |
| V002/V003/V008 | 1 | 0099：阳台门中线选址撞楼梯井楼板洞口（**C 已修**） |

## 4. 发现的 pipeline 缺陷（本次实验的副产物，均如实记录）

1. **单轮计划层盲区（实证）**：门选址按"墙面中点"规则，不感知楼梯井楼板洞口
   → BRIEF-0099 B 路线 V002/V003 硬失败。这正是任务书预期的"规则未覆盖就可能
   出错"的现实缺陷模式，由 Validator 发现、Revision 修复，闭环成立。
2. **Validator 主入口语义**：多外门建筑中 V002/V003 取"扫描序第一个严格外门"
   为主入口（0099 中 16 层的阳台门先于 1 层的正门被评估）。底层缺陷真实存在，
   但"主入口"措辞在多门建筑上有歧义；建议后续按"可达内部站位占比"选主入口
   （记入候选改进，不在本阶段改 Validator——规则库是评测基准，不能为让
   生成器好看而改）。
3. **楼层密度启发式噪声**：8/12 样本 S06 被扣分（梯形屋顶 pitch>1 时屋面基层
   实体密度 ≥0.30；或地毯+墙线层与楼板层并组）。对 B/C 同向同值，不掩盖差异，
   但污染 style_score 绝对值；建议后续用"该层是否有内部站位"做二次过滤。
4. **修复器覆盖边界**：已实现 V002/V003/V004/V005/V006/V007/V008/V010/V011 +
   材料/分区线/邻接开口的程序化修复；V009（结构性低净高）与 Critic 语义维度
   （CR-CQ-02 动线合理性等）无机器实现 → KEEP 并记录理由（协议允许）。
5. **开发期发现并修复的生成器 bug**（为完整性记录）：隔墙不到顶形成"墙顶走道"
   孤立分量（V004）、pitch>1 坡顶踏面未覆盖导致整楼不密闭（interior_air=0，
   Validator 对全露天结构空转 PASS）、分带未留隔墙厚度。这些在正式运行前修复；
   它们说明"生成器自认为合规 ≠ Validator 判定合规"，闭环回归（§6）是必需的。

## 5. 局限性

- **生成器天花板低**：单体量方盒子 + 带状分区 + 直跑/折返梯 + 双坡/四坡
  阶梯屋顶。其结果**不代表 LLM Architect 水平**；B/C 在此只验证管线闭环与
  机器可测指标，不验证设计智能。LLM 接入后应重跑本实验（brief 集不变）。
- **样本量小**：12 条 dev 样本；B/C 差异由 1 条驱动。无统计显著性。
- **评分口径增强的偏差风险**：F01/F02/F03/F06 用到了生成器 ground truth
  （metadata.generation.rooms）；虽然面积/开口均经体素几何复核，但"房间矩形"
  的划分本身来自生成器。对外部蓝图（非本生成器产物）这些子项应回到
  LLM_ONLY/HUMAN_REVIEW。
- **S04 的 roof_base_y 取生成方案记录**（几何代理 UNKNOWN）；S06 伪阳性未剔除
  （见 §4.3）。两者都已在逐条记录的 evidence 中标注。
- **targets_gap 处理**：S01/S05 按 style [min,max] 判定、S02 豁免并标
  GENERALIZATION_CASE（rubric §style_compliance note）。
- Critic 的程序化实现只覆盖 rubric 机器子项（M02/F02/F06 修复与 S02–S06/F04
  KEEP 决策）；10 个判断性维度未机器化。

## 6. 复算入口

```bash
export PYTHONPATH="D:\AI\kimi\daimon-share\daimon\runtime\python\.venv\Lib\site-packages"
# 全量重跑（确定性，可复跑；会重写 generated/ 并追加 jsonl——重跑前先把
# evaluation_data.jsonl 截回 V4 的 5 行，见 run_benchmark.py docstring）
py -3 scripts/run_benchmark.py
# 单条重跑
py -3 scripts/run_benchmark.py --only BRIEF-0099
# 24 份 IR 的 CLI 回归（已跑：24/24 被 validate_blueprints.py 正常消费）
py -3 05_SPATIAL_VALIDATOR/validator_source/validate_blueprints.py \
    --input 08_EVALUATION/generated/B/BRIEF-0099.json --output <任意输出目录>
```

- 每条记录的 `items[*]` 含逐子项公式与中间值（坐标/占比/区间），总分可手算复核。
- C 路线每轮：`generated/_traces/<brief_id>/round{k}_blueprint.json` +
  `round{k}_validation.json` + `round{k+1}_diff.json`（含 SHA256 与锚点校验）。
- CLI 回归输出：`generated/_validator_cli_check/{B,C}/<brief_id>/`。
