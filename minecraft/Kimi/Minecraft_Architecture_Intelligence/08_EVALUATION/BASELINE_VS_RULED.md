# BASELINE_VS_RULED — V4-A（自由生成） vs V4-B（规则约束）重评对比

> 评测时间：2026-09-13；评测人：项目 H · P6 阶段第一部分。
> 数据：新 Spatial Validator 实测输出（`08_EVALUATION/validator_runs/{A,B}/`）+ rubric 机器评分（`08_EVALUATION/evaluation_data.jsonl`）。
> 口径声明：总分为**机器可评子项的上界估计**（未评子项按 0 扣分，满分 95 = 100 − efficiency 5 分整维 NO_CONSTRAINT）。
> 目标 style/function：B 读自 B-design.md（木构住宅 → Residential / Rustic，INFERRED）；A 无设计文档，按 summary.md「双层乡居」取邻近 grammar（GENERALIZATION_CASE）。

## 1. Validator 实测对比

运行命令（两次均真实执行，输入只读）：

```bash
# 2026-09-13 02:53:21
py -3 05_SPATIAL_VALIDATOR/validator_source/validate_blueprints.py \
  --input "D:\Games\Minecraft\AI工程\AI-Test\Architecture-V4\A-blueprint.json" \
  --output "08_EVALUATION\validator_runs\A"
# 2026-09-13 02:53:44
py -3 05_SPATIAL_VALIDATOR/validator_source/validate_blueprints.py \
  --input "D:\Games\Minecraft\AI工程\AI-Test\Architecture-V4\B-blueprint.json" \
  --output "08_EVALUATION\validator_runs\B"
```

| 指标 | A 花楸炉居（自由生成） | B 曲梁宅（规则约束） |
|---|---|---|
| validation_status | **PASS** | **WARNING** |
| hard_fail / warning / info | 0 / 0 / 0 | 0 / 1 / 0 |
| rules_triggered | （无） | V004（WARNING：1 个 11 站位的纯实体封闭内部空间，sample (8,10,9)；<20 不升 HARD） |
| walkability_score | 96.7 | 98.7 |
| connectivity_score | 47.1（※语义不同，见下） | 96.2 |
| vertical_circulation_score | UNKNOWN | 100.0 |
| validator_confidence | high | high |
| 楼层高程（启发式） | [2, 7]（2 层） | [3, 8, 12]（检出 3 层） |
| 门 / 楼梯簇 | 3 / 4 | 3 / 14 |
| 内部空气 / 内部站位 | **0 / 0** | 1450 / 293 |

**A 的 PASS 必须打星号阅读**：A 的内部空气为 0（无玻璃窗/多处开口使洪泛把全部"室内"空气吸收为 exterior，与 P2 已记录的 REF-0003 农舍现象同类），导致 V001/V003/V004/V007/V010/V011 共 **6 条规则 NOT_APPLICABLE**。A 实际只被 V002/V005/V006/V008/V009/V012 评审且未触发。connectivity_score=47.1 是"无内部站位时的退化口径"（露天最大连通分量占比），与 B 的 96.2（主入口分量占全部内部站位比）**语义不同，不能直接比较**。vertical_circulation_score 对 A 为 UNKNOWN——并非 A 的楼梯有问题（V005/V006 均适用且未触发），而是"开放结构不做垂直交通评分"的规则设计。

## 2. rubric 机器评分对比（满分口径见表注）

| 维度（权重） | A | B | B 扣分来源 |
|---|---:|---:|---|
| Hard Validity（40） | 40 | 34 | V004 −6 |
| Functional Layout（25） | 25 | 25 | 仅 F04 机器可评：A dead_end_ratio=0.0491、B=0.0760，均 ≤0.20 不扣分；F01/F02/F03/F05/F06 房间语义不可机器判定 → **不评（LLM_ONLY/HUMAN_REVIEW）** |
| Style Compliance（20） | 20 | 14 | S02 −3：footprint_ratio=1.0952 微低于 Rustic IQR 下界 1.0964；S06 −3：检出 3 层 vs 设计 2 层（楼板密度启发式，疑为屋顶/夹层误检，见 §4 讨论） |
| Material Coherence（10） | 6 | 6 | M02 −4：stone 占比（A 0.6344 / B 0.6370）超出 Rustic [0.0209, 0.5799]；decorative 占比（A 0.0010 / B 0.0025）低于 Rustic min 0.0102；M03 主导族 stone ∈ 声明 {stone, wood} 不扣分 |
| Efficiency（5） | 不评 | 不评 | V4 无机器可读 plot/max_height 约束 → 整维 NO_CONSTRAINT |
| **total_upper_bound（满分 95）** | **91** | **79** | |
| HARD FAIL 封顶 | 不适用（0 个） | 不适用（0 个） | |
| **total_capped（/95）** | **91** | **79** | |
| 归一化（/100）与等级 | 95.8 EXCELLENT | 83.2 GOOD | |

机器可评子项明细与公式、中间值逐条见 `evaluation_data.jsonl`（每个 deduct 都附 evidence 与 formula 字段）。

**敏感性声明（style 目标映射）**：B/C 的设计文档未使用 taxonomy 标签，Rustic 为 INFERRED 映射。若改用 Medieval 口径：B 的 S02 不扣分（1.0952 ∈ Medieval IQR [1.0461, 1.2288]），style 由 14 → 17、总分 79 → 82；A 两口径均满分。S06 扣分两口径相同。机器评分结论对 style 映射的敏感性已逐样本写入 `evaluation_data.jsonl` 的 `style_sensitivity` 字段。

## 3. 与 V4 summary.md 当年结论的异同

### 一致的部分

1. **"三栋均可正常施工、状态合法"**：当年三份 MCP `validate_blueprint` 均 `valid=true`；新 Validator 对 A、B 同样无 HARD FAIL。两个时代的检查在"可施工、可进入、楼梯不堵死"上结论一致（V002/V005/V006 对 A/B 均未触发）。
2. **"两层可用地板、真实门、双格楼梯"**：A 检出 2 层、3 门、4 楼梯簇，与描述一致；B 的主层 [3, 8] 与"主楼两层"一致。

### 不同 / 新发现的部分

1. **评价维度不同**：V4 当年的 validate 只覆盖方块 ID/state 合法性与地形碰撞（WARN 来自授权的地表替换），**不含任何空间拓扑检查**；本次重评首次给出 A/B 的连通性、净高、孤立空间读数。
2. **B 的"楼层数"**：新 Validator 在 B 检出 3 个楼板高程 [3, 8, 12]，与设计"主楼两层"不符。这大概率是楼板密度启发式把折坡屋顶下段/夹层误判为楼板（VALIDATION_SPEC V007 已知盲区："密实屋顶会误检为楼板"），而非设计真的多了一层——**该扣分标记为 HEURISTIC 存疑项**，人工复核前不应视为 B 的真实缺陷。
3. **B 存在一个 11 站位的封闭内部空间**（V004 WARNING）：当年未被任何检查发现。规模未达 HARD 阈值（20），孤立环为纯实体，可能是阁楼/夹层暗格；是否设计意图需人工判断。
4. **A 的"无内部空间"读数暴露其围护开放度**：A 的室内在洪泛语义下全部与室外连通（大开口/无玻璃窗）。这对"乡居"不一定是缺陷，但意味着 A 的"入口/连通性无问题"证据强度天然弱于 B——**自由生成路线 A 的 PASS 是"检查器看不见内部"下的 PASS**。
5. **材料**：A、B 的 stone 族占比（0.63–0.64）均略超 Rustic 参考库区间上界 0.58——两者都比 123 张 Rustic 参考蓝图"更石质"；装饰族（植物/羊毛等）都几乎为零，低于参考库下限。这一机器读数当年没有对应观察。

### 当年结论保持有效的部分

- "审美结论等待 Owner，不预设胜者"：本次机器重评不提供审美判断；A 91 vs B 79 的差距全部来自机器可判子项（且含 1 项存疑的 S06），不得解读为"A 优于 B"。rubric 未评的 22/25 functional 分与 efficiency 5 分仍待 LLM Critic / 人工补齐。

## 4. 小结

| | A（自由生成） | B（规则约束） |
|---|---|---|
| 硬空间错误 | 未发现（但 6 条规则不适用） | 未发现；1 个 V004 WARNING |
| 机器总分（/95，上界） | 91 | 79 |
| 证据强度 | 弱（内部不可见） | 强（内部 293 站位全量受检） |

规则约束路线 B 接受了**更严格且更完整**的机器检验（全部 12 条规则适用）并交出 96.2 的真实连通性读数；A 的高分部分来自"检查器对其内部失明"。比较两条路线时，证据完整度差异必须与分数差异一起阅读。
