# 07_RECOMMENDED_ARCHITECTURE_PIPELINE — 最终推荐设计流程（P7 最终报告 7/8）

> 以本次 P0–P6 实测结果为准，对任务书 §22 候选 pipeline 的确认与修订。
> 证据：`08_EVALUATION/B_VS_C_PIPELINE.md`（V4 历史个案）、`B_VS_C_OFFLINE_RUN.md`（12-brief 离线实验）、
> `07_ARCHITECT_SYSTEM/`（218+20 规则与修订协议）、`05_SPATIAL_VALIDATOR/`。

## 1. 最终推荐 Pipeline

```text
User Brief
↓
① Brief Normalizer        — 风格/功能标签确认或显式声明（SS-005）；模糊标签先确认
↓
② Grammar Retrieval       — style + function grammar 检索；SUPPORTED 取 median/IQR，
                            PROVISIONAL 降格咨询性，OBSERVATION/零样本回退并标注"无背书"
↓
③ Architect               — 按 ARCHITECT_RULEPACK 218 条生成（含 validator_precheck 12 项自检；
                            UNKNOWN 维度交 LLM 自由发挥并注明"无数据背书"）
↓  Canonical IR blueprint.json（schema_version=1）
④ Hard Spatial Validator  — V001–V012 确定性校验
↓        ├─ 任一 HARD_FAIL → 直接进 ⑥ Revision（Critic 不评审带病稿件："先治病再选美"）
⑤ Critic                  — 10 维度 20 条判断性评审（不重复 Validator 检查，不评"丑"）
↓
⑥ Revision                — 按优先级修订（体素级 patch 或带 overrides 重生成），产出逐坐标
                            diff + SHA256；锚点（footprint/风格标签/功能分区）冻结，
                            diff>30% 触发回退检查；迭代上限 3 轮，未决项转 HUMAN_REVIEW
↓
⑦ Hard Validator Recheck  — 修订后必须真实重跑 Validator（修订可能引入新客观错误）
↓  （无客观错误）
⑧ 3D Preview              — 四视图 PNG + LOD（references 派生链同款）
↓
⑨ Owner Approval          — 审美终裁归 Owner（CR-VF-02；规则满足 ≠ 美观自动通过）
↓
⑩ World Write             — 经批准后施工（本项目内 Formal world writes = 0）
```

## 2. 对任务书 §22 候选的修订点（以结果为准）

1. **确认：Hard Validator 位于 Architect 与 Critic 之间**。实证依据：V4 C-before 存在当年 Critic 未点名的硬缺陷（门洞上半是玻璃、门外无接近站位），若 Validator 在 Critic 之前接入会被直接点名；P6b BRIEF-0099 同样由 Validator 发现生成侧盲区。
2. **确认：Recheck 不可省**。修订是体素级改动，可能引入新客观错误（协议状态机 REVALIDATE→REVISE 回路）。
3. **新增显式环节 ① Brief Normalizer 与 ② Grammar Retrieval**：标签歧义（conf<0.55 降级判例存在）与 grammar 分级回退（SUPPORTED/PROVISIONAL/OBSERVATION/零样本）必须在生成前定型，否则 Architect 无据可依。
4. **新增 ⑨ Owner Approval 前置约束**：HARD_FAIL 未消除不得进入 Final；WARNING 可保留但须逐条给理由（含"歧义阳性"引 known_limitations 条目）。

## 3. B/C 分工与复杂度判定（Q5）

- **默认 B**（规则约束单轮：Architect 按 Rulepack 生成 → Validator → 交付）：P6b 12 样本中 11 条 B 零硬缺陷；规则直译 + 生成即合规（GA/VA/PC 组规则与 V001–V012 一一对应）已能覆盖绝大多数校验项。
- **复杂项目转 C**（Validator→Critic→Revision→Recheck 闭环）。

**复杂度判据**（满足任一即转 C；HEURISTIC，可由 Owner 调整）：

| 判据 | 依据 |
|---|---|
| brief 难度 = Hard（楼层≥2 且 zones≥4、禁配邻接 ≥1、限高余量仅 1 格） | P6b 唯一硬缺陷样本 BRIEF-0099 即 Hard；V4 C-before 同为复杂多体量 |
| `targets_gap = true`（无本地 grammar 背书，需泛化） | gap 组合无 IQR 可锚定，单轮规则直译风险高 |
| Constrained Plot（长边 ≤15 强制竖向发展）/ Tower 类 3–5 层 | 紧张地块容量-邻接冲突在 P6b 中两次出现（F02/F06 残留扣分） |

- C 路线代价实测中位极小：12 样本均值 0.08 轮 / 0.5 方块；唯一修复实例 1 轮 6 方块、diff 0.74%、锚点不变。
- **样本量声明**：上述依据来自 12 条 dev 样本 + V4 历史个案（n=1/路线），不构成统计结论；LLM Architect 接入后应以完整 test 集（70 条）重跑再校准判据。

## 4. 角色职责边界（Q3/Q4 落地）

| 环节 | 回答的问题 | 工具 |
|---|---|---|
| Validator | 有没有客观空间错误？ | V001–V012 确定性检查（HEURISTIC 但可程序化） |
| 规则系统 | 数值该落在哪？ | grammar IQR/频率 → Architect Rulepack 218 条 |
| Critic | 即使可用，设计是否合理？ | 20 条（10 HEURISTIC / 9 LLM_ONLY / 1 HUMAN_REVIEW，无 critical） |
| 人工 | 美不美？UNKNOWN 维度怎么定？ | Owner Approval / HUMAN_REVIEW |

## 5. 当前 pipeline 的已知短板（不掩饰）

1. 生成器天花板低（单体量方盒子 + 带状分区 + 直跑/折返梯 + 阶梯屋顶）——**不代表 LLM Architect 水平**；
2. Validator 主入口选择在多门建筑有歧义；楼层启发式噪声污染 S06 评分；
3. 修复器未覆盖 V009 与 Critic 语义维度；
4. gap 组合与 0 样本风格无 grammar 支撑，C 路线在那里的价值尚未被真实测量（生成器按 GENERALIZATION_CASE 宽松判分）。

改进计划见 `08_NEXT_STEPS.md`。
