# 01_EXECUTIVE_SUMMARY — 执行摘要（P7 最终报告 1/8）

> 项目代号 H ｜ 2026-09-13 ｜ 本摘要不依赖其他文件独立成立。
> 一切数字可回溯：`01_INVENTORY`–`08_EVALUATION` 各阶段产物。

## 结论（先读这一段）

**本项目已建成一套离线、只读、可复跑的 Minecraft 建筑知识系统**：123 张参考蓝图全部解析并归一化（123/123，PARSE_FAILURE 0），每张拥有 50 字段机器可读元数据；建立了 Style 7 类 / Function 15 类分类体系与 228 条量化 grammar 规则（style 111 + functional 117）；实现了 12 条空间校验规则（V001–V012）的确定性 Validator，回归测试 30/30 通过，全库硬失败率经 7 轮校准从 0.829 降到 0.496 并稳定（残余触发抽查以真阳性/歧义阳性为主）；建立了 100 条机器可读设计 brief 的 benchmark（dev 30 / test 70）；产出 Architect 规则包 218 条 + Critic 规则包 20 条 + 修订协议；并用 V4 历史样本与 12 条 dev brief 的离线生成实验证明 **Validator→Critic→Revision→Recheck 闭环机器可通且修复代价极小**。

**推荐 pipeline 一句话**：`Brief Normalizer → Grammar Retrieval → Architect → Hard Spatial Validator → Critic → Revision → Validator Recheck → 3D Preview → Owner Approval → World Write`——默认走 B（规则约束单轮），命中复杂度判据（Hard 难度 / targets_gap / 紧张地块多楼层）转 C（含 Revision 闭环）；HARD_FAIL 不消除不交付，审美终裁归 Owner。详见 `07_RECOMMENDED_ARCHITECTURE_PIPELINE.md`。

## 最强数字（全部实测）

| 数字 | 含义 | 来源 |
|---|---|---|
| **123/123** | 参考蓝图解析成功；归一化到 DataVersion 4903 后 unresolved=0；损坏 0 | `01_INVENTORY`、`02_BLUEPRINT_METADATA` |
| **50 字段** | 每张蓝图的元数据（JSONL+CSV），逐字段带 OBSERVED/HEURISTIC/INFERRED/UNKNOWN 标注 | `02_BLUEPRINT_METADATA` |
| **V001–V012** | 空间校验规则 12 条（HARD 7 / WARNING 4 / INFO 1），阈值全外置 | `05_SPATIAL_VALIDATOR` |
| **30/30** | 回归测试通过（walkability 11 + validator 19），每条 HARD 规则有正例+负例，V006 负例必现 | `08_EVALUATION/VALIDATOR_TESTS.md` |
| **0.829 → 0.496** | 全库 hard_fail_rate 经 7 轮实证校准的轨迹；残余触发非系统性误报 | `05_SPATIAL_VALIDATOR/VALIDATION_SPEC.md` §4 |
| **100 brief** | benchmark 任务集（Easy 40 / Medium 40 / Hard 20；5 风格 × 12 功能；20 条命中 P0 缺口） | `06_BENCHMARK` |
| **218 + 20 条** | Architect 规则包 218 条（22 HARD）+ Critic 规则包 20 条（10 HEURISTIC / 9 LLM_ONLY / 1 HUMAN_REVIEW） | `07_ARCHITECT_SYSTEM` |
| **B vs C：0.083 → 0.000** | 12-brief 离线实验 hard_fail_rate；唯一硬缺陷样本 BRIEF-0099 经 1 轮 6 方块修订由 40(POOR) 升至 91(EXCELLENT) | `08_EVALUATION/B_VS_C_OFFLINE_RUN.md` |
| **V4 历史重评** | C-before 40（封顶）→ C-final 83/95；Revision diff 653 坐标独立复算一致 | `08_EVALUATION/B_VS_C_PIPELINE.md` |

## 核心问题 Q1–Q6（一句话版，详版见各分报告）

- **Q1「楼梯尽头是墙」根因**：生成阶段缺乏"通路必须有可达终点"的全局空间推理（主因）+ 验证层只有方块合法性检查、无空间拓扑检查（放大器）；与施工、preview 无关。其几何子类（顶格被堵/无净高）现由 V006 确定性检测，语义子类（通向无意义空间）仍需 Critic。（证据：`08_EVALUATION/B_VS_C_PIPELINE.md` §5）
- **Q2 122 张够不够**：**部分够**。3 个风格类（Rustic 20 / Medieval 19 / Fantasy 10）与 5 个功能类（n≥10）达到 SUPPORTED 可出可靠 grammar；Japanese(7)/Chinese(4) 仅 PROVISIONAL；5 个功能类 n<4 只能 OBSERVATION；style×function×size 联合分布 375 cell 仅 36 非零（90.4% 空缺）；Modern/Industrial/Gothic/Victorian/Nordic 全库 0 样本。
- **Q3 知识分工**：客观空间正确性 → 程序 Validator（V001–V012）；有样本支撑的量化统计规律（IQR/频率/材料区间）→ 规则系统（grammar/rulepack）；判断性维度（语义动线、风格语汇、视觉焦点）→ LLM Critic；审美终裁 → 人工。
- **Q4 可检查性分层**：可确定性检查 = 入口存在/堵塞、内部可达性、孤立空间、楼梯底/顶封堵、垂直断裂（V001–V007，几何+拓扑）；只能 heuristic = 净高、围护缺口、屋顶覆盖、死端统计（V008–V012，依赖洪泛/密度近似，有已声明盲区）；最好交模型/人 = 窗节奏、屋顶形制、房间语义、审美（Critic 中 9 条 LLM_ONLY + 1 条 HUMAN_REVIEW）。
- **Q5 B/C 分工**：默认 B（规则约束单轮），复杂项目转 C。复杂度判据（满足任一）：brief 难度 Hard（楼层≥2 且 zones≥4、禁配邻接≥1、限高紧张）、`targets_gap=true`（无本地 grammar 背书需泛化）、Constrained Plot / Tower 类强制竖向发展。依据：P6b 12 样本中 11 条 B 零硬缺陷，差异全部由 1 条 Hard 紧张地块样本驱动；C 修复成功率 1/1 且代价 6 方块。
- **Q6 最缺什么蓝图**：缺口矩阵 Top priority = 村落核心功能的 Medieval/Rustic × {Inn, Civic, Gate, Blacksmith, Farm, Warehouse, Bridge} 的 small/medium 档（P0 共 50 cell；Bridge 全库 0 样本），并列最高优先的是 5 个 0 样本风格大类（Modern/Industrial/Gothic/Victorian/Nordic）。

## 必须同时阅读的诚实声明

1. **B/C 离线实验的生成器是 programmatic reference generator（规则直译），不是 LLM**——它验证的是管线闭环，不代表任何 LLM Architect 的水平；12 条样本不构成统计结论。
2. 全库 hard_fail_rate 0.496 高，但参考库按外观精选、从未承诺内部可通行（analysis.md 自述 REFERENCE_ONLY）；残余触发经人工抽查为真阳性/歧义阳性为主，不是 Validator 残留误报。
3. main_entrance 全库 89.4% UNKNOWN、窗节奏与屋顶形制全风格 UNKNOWN——这是纪律结果，不是遗漏。
4. V4 重评中 A（自由生成）的 PASS 证据强度弱（内部空气=0，6 条规则不适用）；分数比较必须连同证据完整度一起阅读。

## 分报告索引

| # | 报告 | 内容 |
|---|---|---|
| 02 | `02_REFERENCE_LIBRARY_FINDINGS.md` | 库构成、数据质量、归一化状态 |
| 03 | `03_ARCHITECTURAL_GRAMMARS.md` | grammar 分级发现、最强量化规律、UNKNOWN 维度 |
| 04 | `04_SPATIAL_FAILURE_MODES.md` | 全库真实空间缺陷类型学（V001–V012 画像、0.829→0.496 教训） |
| 05 | `05_VALIDATOR_RESULTS.md` | 规则清单、测试覆盖、全库指标、已知限制 |
| 06 | `06_BENCHMARK_RESULTS.md` | 100 brief 覆盖、V4 重评分、12-brief B/C 对比 |
| 07 | `07_RECOMMENDED_ARCHITECTURE_PIPELINE.md` | 最终推荐 pipeline 与 B/C 复杂度判据 |
| 08 | `08_NEXT_STEPS.md` | 缺口驱动补图计划、LLM Architect 接入、Validator 改进项 |
