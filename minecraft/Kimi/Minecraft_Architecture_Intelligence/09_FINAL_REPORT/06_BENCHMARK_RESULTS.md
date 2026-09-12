# 06_BENCHMARK_RESULTS — Benchmark 结果（P7 最终报告 6/8）

> 数据来源：`06_BENCHMARK/BENCHMARK_SPEC.md`、`coverage_stats.json`、`BASELINE_RESULTS.md`、
> `08_EVALUATION/B_VS_C_OFFLINE_RUN.md`、`BASELINE_VS_RULED.md`、`B_VS_C_PIPELINE.md`、`p6b_summary.json`。

## 1. Benchmark 任务集（100 brief，机器可读）

- 文件：`design_briefs.jsonl`（每行一条，20 必备字段 + 扩展字段）；生成种子 42 可复跑；独立校验脚本 11 项全量检查 **ALL CHECKS PASS**。
- 难度分布：**Easy 40 / Medium 40 / Hard 20**（定级由功能模板驱动，非事后标注）。
- 风格覆盖（真实库样本充足的 5 类）：Medieval 27 / Rustic 25 / Fantasy 16 / Japanese 16 / Chinese 16。
- 功能覆盖：12 个 taxonomy 功能类（Residential 28 / Inn 14 / Mixed-use 12 / Workshop 8 / Civic 8 / Tower 7 / Castle 6 / Religious 4 / Warehouse 4 / Gate 4 / Blacksmith 3 / Farm 2）。
- 功能域 × 难度：Residential 23 / Defensive 15 / Workshop 14 / Mixed-use 12 / Hospitality 12 / Civic 12 / Constrained Plot 12。
- **targets_gap = 20 条（20%）**：全部命中缺口矩阵 P0 cell（脚本断言非 P0 直接失败），plot 长边严格落在 V6C2 size_class 边界内，可精确回指 cell；评定时 style_compliance 按邻近 style 宽松判定并标 GENERALIZATION_CASE。
- 防过拟合：dev/test = 30/70 分层抽样（`benchmark_split.json`），调参只用 dev。
- 数值锚定：层高/材料区间/屋顶占比/长宽比全部取自 grammar 实测 IQR（不发明数值）。

## 2. V4 历史样本重评分（n=1/路线，个案证据，非统计结论）

口径：机器可评子项的上界估计（未评子项按 0 扣分，满分 95 = 100 − efficiency 整维 NO_CONSTRAINT）；HARD FAIL 封顶 1/3/5 → 40/25/10。

| 样本 | hard_fail | validator(/40) | functional(/25) | style(/20) | material(/10) | total_capped(/95) | 归一化/等级 |
|---|---:|---:|---:|---:|---:|---:|---|
| V4-A（自由生成） | 0 | 40（6 条规则 NOT_APPLICABLE，证据弱） | 25 | 20 | 6 | 91 | 95.8 EXCELLENT* |
| V4-B（规则约束） | 0 | 34（V004 −6） | 25 | 14 | 6 | 79 | 83.2 GOOD |
| V4-C-before | **1（V002）** | 10 | 25 | 20 | 8 | **40**（cap=40，封顶前 63） | 42.1 POOR |
| V4-C-final | 0 | 30 | 25 | 20 | 8 | 83 | 87.4 EXCELLENT |

要点：
- **C 路线 Revision 真实有效**：C-before→C-final 硬失败 1→0、connectivity 0.0→50.5、hard_validity +20；revision_cost = 10 变更动作 / 1 轮 / 653 坐标（added 137 / removed 300 / changed 216，占终稿 23.5%），独立复算一致。
- **A 的 PASS 打星号**：内部空气 = 0（开口/无玻璃窗使洪泛吸收全部"室内"），6 条规则不适用——高分部分来自"检查器对其内部失明"；B 接受全部 12 条规则检验（内部 293 站位全量受检），证据强度不可比。
- **敏感性**：B/C 的 Rustic 标签为 INFERRED；改 Medieval 口径则 B style 14→17、总分 79→82；逐样本写入 `evaluation_data.jsonl` 的 style_sensitivity 字段。
- C-before 当年 Critic **未点名**的硬缺陷（门洞上半是玻璃、门外无接近站位）由本次新 Validator 补刀发现——实证了"Validator 嵌入 Architect→Critic 之间"的价值。

## 3. 离线 12-brief B/C 对比（P6b，2026-09-13）

> **性质声明（先读）**：生成器 = **programmatic reference generator（rule-driven）**（`scripts/generate_blueprint.py`），由规则数值区间 + brief 约束驱动的确定性参数化算法，**不是 LLM**。本实验验证的是**管线闭环**（Validator→Critic→Revision→Recheck 是否机器可通、是否有差异），不代表任何 LLM Architect 水平。B 与 C 初稿逐方块一致，差异只来自 C 路线的 Validator 触发修订。

样本：dev 集内 12 条（4 Easy / 5 Medium / 3 Hard，6 功能域，3 条 targets_gap）。

| 指标 | B（规则约束单轮） | C（含 Revision 闭环） | Δ |
|---|---|---|---|
| hard_fail_rate | 0.083（1/12） | **0.000（0/12）** | −0.083 |
| validator_score（/40） | 38.00 | 40.00 | +2.00 |
| functional_score（/25） | 23.92 | 23.92 | 0 |
| style_score（/20） | 16.25 | 16.25 | 0 |
| material（/10）/ efficiency（/5） | 10.00 / 4.83 | 10.00 / 4.83 | 0 |
| **mean total（/100）** | 90.75 | **95.00** | +4.25 |
| revision_cost | n/a | 0.08 轮 / 0.5 方块（均值） | — |

- **C 修复成功率 1/1 = 100%**：唯一硬缺陷样本 BRIEF-0099（Hard / Constrained Plot / Japanese）B 总分 40 POOR → C 91 EXCELLENT；修订 = 阳台门沿墙平移 3 格，1 轮、6 方块、diff_ratio 0.74%、锚点三项不变；每轮 traces（蓝图+校验+diff+SHA256）齐全。
- **如实陈述**：11/12 样本 B 本就零硬缺陷（规则直译 + 生成侧密闭自检覆盖了绝大多数校验项），B/C 差异完全由 1 条 Hard 紧张地块样本驱动——**闭环有效性成立，统计意义不足**。
- CLI 回归：24 份生成 IR 全部被 `validate_blueprints.py` 正常消费（24/24）。
- 评分口径已知增强：F01/F02/F03/F06 使用生成器 ground truth（rooms），对外部蓝图应回到 LLM_ONLY/HUMAN_REVIEW；F05 维持 LLM_ONLY。

## 4. 实验副产物（pipeline 缺陷，均如实记录）

1. **单轮计划层盲区**：门选址不感知楼梯井楼板洞口 → BRIEF-0099 B 路线 V002/V003 硬失败——正是"规则未覆盖就可能出错"的现实缺陷模式，由 Validator 发现、Revision 修复。
2. **Validator 主入口语义**：多外门建筑取"扫描序第一个严格外门"为主入口（0099 中 16 层阳台门先于 1 层正门被评估）——缺陷真实存在，但措辞有歧义；建议按"可达内部站位占比"选主入口（记入改进项，**本阶段不改 Validator——规则库是评测基准，不能为让生成器好看而改**）。
3. **楼层密度启发式噪声**：8/12 样本 S06 被误扣分（梯形屋顶密层/地毯层误检为楼板）；对 B/C 同向同值不掩盖差异，但污染 style_score 绝对值；建议用"该层是否有内部站位"二次过滤。
4. **修复器覆盖边界**：V009 与 Critic 语义维度无机器实现 → KEEP 并记录理由（协议允许）。

## 5. 复算入口

`evaluation_data.jsonl`（每条含逐子项公式与中间值，总分可手算复核）；`p6b_summary.json`；`generated/`（B/C IR + `_traces` + `_validator_cli_check`）；重跑：`py -3 scripts/run_benchmark.py [--only BRIEF-0099]`（确定性；重跑前先把 jsonl 截回 V4 的 5 行，见脚本 docstring）。
