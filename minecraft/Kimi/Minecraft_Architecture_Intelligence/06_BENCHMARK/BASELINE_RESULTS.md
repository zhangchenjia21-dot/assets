# BASELINE_RESULTS — Benchmark 基线评测结果

> 状态：**2.1 历史样本复测已回填（2026-09-13，P6 阶段第一部分）；2.2/2.3 与第 3 节已由
> P6b 离线生成实验回填（同日，programmatic reference generator，非 LLM）**。
> 注意：2.1 填入的是 **4 个 V4 历史样本**（A/B/C-before/C-final）的重评结果，**不是完整 benchmark 运行**；
> 样本量 n=1/路线，不构成统计结论。2.2/2.3/3 节为 12 条 dev brief 的生成评测（同样小样本）。
> 铁律：历史样本不足时写 `Historical baseline insufficient`，不得伪造 Before/After（任务书 §18）。
> 数据来源：`08_EVALUATION/validator_runs/*/`（Validator 原始输出）、`08_EVALUATION/evaluation_data.jsonl`（逐子项公式与中间值）、`08_EVALUATION/score_v4_samples.py`（可复跑）。

## 1. 指标定义

| 指标 | 定义 | 计算来源 |
|---|---|---|
| `hard_fail_rate` | 触发 ≥1 个 HARD FAIL 的 blueprint 占比 | Validator 输出 `hard_fail_count ≥ 1` 的样本数 / 总样本数 |
| `validator_score` | hard_validity 维度得分（满分 40） | scoring_rubric.json `hard_validity` 扣分项逐条结算 |
| `functional_score` | functional_layout 维度得分（满分 25） | scoring_rubric.json `functional_layout`（zone 缺失 / 邻接 / 死路） |
| `style_score` | style_compliance 维度得分（满分 20） | scoring_rubric.json `style_compliance`（对照 style_rules.json 区间） |
| `revision_cost` | C 路线修正代价 | Critic 建议条数、Revision 轮数、修正前后 diff 方块数（参照 V4 `evidence\C-revision-diff.json` 格式） |
| `total_score` | 五维合计（满分 100），HARD FAIL 时按 rubric 封顶 | `min(Σ五维, cap(hard_fail_count))` |

## 2. 评测表骨架（P6 回填）

### 2.1 历史样本复测（V4 A/B/C + V5 candidates，若可用）

> 已回填（2026-09-13）。口径：validator_score=functional_score=style_score 按 rubric 扣分结算；
> **未评子项按 0 扣分（上界估计）**——functional 仅 F04 机器可评（F01/F02/F03/F05/F06 → LLM_ONLY/HUMAN_REVIEW），
> style 仅 S01/S02/S05/S06 机器可评，efficiency 整维 NO_CONSTRAINT（不计入 total）。
> total_score 列为 total_capped（封顶后，满分 95）；括号内为封顶前。revision_cost = 变更动作数/轮数/diff 坐标数。

| sample | 来源 | brief 对应 | hard_fail_count | validator_score(/40) | functional_score(/25) | style_score(/20) | revision_cost | total_score(/95) |
|---|---|---|---|---|---|---|---|---|
| V4-A | `AI-Test\Architecture-V4\A-blueprint.json` | 无 brief（自由生成；style 按 Rustic 邻近判定，GENERALIZATION_CASE） | 0 | 40（6 条规则 NOT_APPLICABLE，证据弱） | 25（仅 F04 已评） | 20 | n/a | 91 |
| V4-B | `AI-Test\Architecture-V4\B-blueprint.json` | 规则约束（Residential/Rustic，INFERRED） | 0 | 34（V004 −6） | 25（仅 F04 已评） | 14（S02 −3、S06 −3※启发式存疑） | n/a | 79 |
| V4-C-before | `AI-Test\Architecture-V4\C-blueprint-before.json` | C 路线首轮（Residential/Rustic，INFERRED） | **1**（V002） | 10（V002 −8、V003 −12、V004 −6、V008 −4） | 25（仅 F04 已评） | 20 | — | **40**（封顶前 63；cap=40） |
| V4-C-final | `AI-Test\Architecture-V4\C-blueprint-final.json` | C 路线终稿（Residential/Rustic，INFERRED） | 0 | 30（V004 −6、V008 −4） | 25（仅 F04 已评） | 20 | 10 动作 / 1 轮 / 653 坐标（added 137、removed 300、changed 216；独立复算一致） | 83 |

补充：material_coherence（/10，未在表头列出）：A=6、B=6、C-before=8、C-final=8（M02 材料族占比偏离 Rustic 区间，明细见 jsonl）。
等级（归一化 /100）：A 95.8 EXCELLENT / B 83.2 GOOD / C-before 42.1 POOR / C-final 87.4 EXCELLENT。

### 2.2 Benchmark 生成评测（10-20 条 brief，dev 集内选取）

> 已回填（2026-09-13，P6b 离线生成实验）。生成器 = **programmatic reference
> generator (rule-driven)**（`scripts/generate_blueprint.py`，非 LLM）；12 条 dev brief
> （4E/5M/3H，6 功能域，gap×3）。实验设计/局限详见 `08_EVALUATION/B_VS_C_OFFLINE_RUN.md`。
> 满分 100（五维全机器评；F05 维持 LLM_ONLY）；C 的 revision_cost = 轮数/变更方块数。

| brief_id | difficulty | pipeline | hard_fail_count | hard_fail_rate* | validator_score | functional_score | style_score | revision_cost | total_score |
|---|---|---|---|---|---|---|---|---|---|
| BRIEF-0006 | Easy | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0轮0方块 | 97 / 97 |
| BRIEF-0037 | Easy | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0 | 97 / 97 |
| BRIEF-0053 | Easy(gap) | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0 | 97 / 97 |
| BRIEF-0091 | Easy | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0 | 97 / 97 |
| BRIEF-0017 | Medium | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 20 / 20 | 20 / 20 | n/a / 0 | 95 / 95 |
| BRIEF-0030 | Medium | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 11 / 11 | n/a / 0 | 91 / 91 |
| BRIEF-0056 | Medium | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0 | 92 / 92 |
| BRIEF-0065 | Medium(gap) | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 14 / 14 | n/a / 0 | 94 / 94 |
| BRIEF-0096 | Medium | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 20 / 20 | 17 / 17 | n/a / 0 | 92 / 92 |
| BRIEF-0043 | Hard(gap) | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0 | 97 / 97 |
| BRIEF-0068 | Hard | B / C | 0 / 0 | 0 / 0 | 40 / 40 | 25 / 25 | 17 / 17 | n/a / 0 | 97 / 97 |
| BRIEF-0099 | Hard | B / C | **2 / 0** | **1 / 0** | **16 / 40** | 22 / 22 | 14 / 14 | n/a / **1轮6方块** | **40 / 91** |

\* hard_fail_rate 为汇总指标，单条样本填 0/1，汇总行填比率。

### 2.3 汇总对比（B vs C）

| pipeline | n | hard_fail_rate | mean validator_score | mean functional_score | mean style_score | mean revision_cost | mean total_score |
|---|---|---|---|---|---|---|---|
| B（规则约束单轮） | 12 | 0.083 | 38.00 | 23.92 | 16.25 | n/a | 90.75 |
| C（Architect→Validator→Critic→Revision→Recheck） | 12 | **0.000** | **40.00** | 23.92 | 16.25 | 0.08 轮 / 0.5 方块 | **95.00** |

补充：material_coherence 两路线均 10.00/10（拟合收敛），efficiency 均 4.83/5。
C 修复成功率 1/1（BRIEF-0099：40 POOR → 91 EXCELLENT，锚点三项不变，diff 0.74%）。
注意：11/12 样本 B 本就零硬缺陷，差异由 1 条 Hard 样本驱动——闭环有效性成立，
统计意义不足（详见 B_VS_C_OFFLINE_RUN.md §3.2 的如实陈述）。

## 3. B vs C 对比表（P6b 离线生成实验，2026-09-13）

| 指标 | B（规则约束单轮） | C（含 Revision 闭环） | Δ |
|---|---|---|---|
| hard_fail_rate | 0.083（1/12） | 0.000（0/12） | −0.083 |
| validator_score（/40） | 38.00 | 40.00 | +2.00 |
| functional_score（/25） | 23.92 | 23.92 | 0 |
| style_score（/20） | 16.25 | 16.25 | 0 |
| material_score（/10） | 10.00 | 10.00 | 0 |
| efficiency_score（/5） | 4.83 | 4.83 | 0 |
| total_score（/100，封顶后） | 90.75 | 95.00 | +4.25 |
| revision_cost | n/a | 1 轮 / 6 方块（仅 BRIEF-0099） | — |

生成器性质：programmatic reference generator (rule-driven)，**非 LLM**；
不代表 LLM Architect 水平。复算：`08_EVALUATION/evaluation_data.jsonl`
（24 条，sample 形如 `BRIEF-0099|B`）、`08_EVALUATION/p6b_summary.json`、
`08_EVALUATION/generated/`（B/C IR + `_traces` 逐轮中间结果 +
`_validator_cli_check` CLI 回归 24/24 通过）。

### 3.1 回填纪律

1. 仅使用 dev 集（30 条）做规则/prompt 迭代；test 集（70 条）仅最终对比运行一次。
2. 每个数字必须能回溯到 Validator / 评分脚本的原始输出文件，禁止手填。
3. targets_gap=true 的 brief 单独分组报告，style_score 按 GENERALIZATION_CASE 规则宽松判定。
4. 若 P6 环境不允许离线生成：如实记录 `Historical baseline insufficient / Generation environment unavailable`，本表保留骨架不填数。
