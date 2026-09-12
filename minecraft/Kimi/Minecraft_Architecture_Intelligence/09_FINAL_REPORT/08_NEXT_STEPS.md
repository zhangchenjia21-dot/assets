# 08_NEXT_STEPS — 后续计划（P7 最终报告 8/8）

> 依据：`04_GRAMMARS/data_gap_matrix.json`（375 cell 实测）、`05_SPATIAL_VALIDATOR/known_limitations.md`、
> `08_EVALUATION/B_VS_C_OFFLINE_RUN.md` §4–5。按优先级排序。

## 1. 缺口矩阵驱动的补图计划（Q6 落地，最高优先）

**P0（50 cell）——村落核心功能，Medieval/Rustic × small/medium：**

| 功能 | 全库现有 | 目标 | 缺口 cell 举例 |
|---|---:|---|---|
| Inn | 5 | 每 style×size ≥4 | Medieval×Inn×small/medium、Rustic×Inn×small |
| Civic | 4 | 同上 | Medieval×Civic×small、Rustic×Civic×small/medium |
| Gate | 3 | 同上 | Medieval×Gate×small、Rustic×Gate×small/medium |
| Blacksmith | 3 | 同上 | Medieval×Blacksmith×small/medium、Rustic×Blacksmith×medium |
| Farm | 3 | 同上 | Medieval×Farm×small、Rustic×Farm×small/medium |
| Warehouse | 1 | 同上 | Medieval×Warehouse×small/medium、Rustic×Warehouse×small |
| Bridge | **0** | 先建立类别（≥4） | Medieval×Bridge×small/medium 等全部 |

**并列最高优先：0 样本风格大类**——Modern / Industrial / Gothic / Victorian / Nordic 全库 0 张，任何 function×size 组合都无法形成 grammar，按需求排序采集（每风格先 ≥8 张到 SUPPORTED 门槛）。

**P1（31 cell）**：SUPPORTED 两类但组合空缺（如 Medieval×Residential×small/medium/large、Medieval×Tower×small 等）——补组合样本，把类别级 grammar 升级为组合级。

**P2（293 cell）**：一般组合空缺；**P3（1 cell）**：Rustic×Residential×large（n=4，可候补至 SUPPORTED）。

补图质量要求（来自本项目教训）：**新入库蓝图必须验证内部可通行**（本库 analysis.md 普遍"内部交通未验证"导致 hard_fail_rate 0.496 的读数）；入库即跑 Validator，HARD_FAIL 资产不得作为参考。

## 2. LLM Architect 接入重跑 benchmark（验证本项目的真正目标）

1. 把 `architect_rules.json`（218 条）+ `critic_rules.json`（20 条）+ `design_briefs.jsonl` 接入真实 LLM Architect（ChatGPT/Codex/Kimi/Grok）；
2. **brief 集不变**（100 条，dev 30 / test 70），先 dev 调 prompt、test 只跑一次；
3. 重跑 B vs C 完整对比：本项目的 programmatic generator 结果（B 90.75 / C 95.00，n=12）作为**参考生成器基线**保留，LLM 结果与其并列报告但不可直接比较性质（生成智能 vs 规则直译）；
4. 重新校准 Q5 复杂度判据（当前判据基于 12 样本 + 历史个案）；
5. 评分口径注意：对外部蓝图 F01/F02/F03/F06 回到 LLM_ONLY/HUMAN_REVIEW（无生成器 ground truth）。

## 3. Validator 已知改进项（按影响排序）

| 项 | 问题 | 建议 |
|---|---|---|
| 主入口选择 | 多外门建筑取"扫描序第一个严格外门"（BRIEF-0099 中 16 层阳台门先于 1 层正门被评估） | 按"可达内部站位占比"选主入口；注意：改动需重校全库并保留旧版作基准 |
| 楼层启发式噪声 | 密实屋顶/地毯层误检为楼板（P6b 8/12 样本 S06 误扣分；REF-0042/0035 伪影） | 加"该层是否有内部站位"二次过滤 |
| false negative 未测量 | 无全库人工标注 ground truth | 抽 20–30 张人工标注缺陷，测召回率 |
| V008–V012 负例夹具缺失 | WARNING/INFO 级无"必触发"回归锁 | 补合成夹具；补机制感知降级路径夹具 |
| 活板门舱口语义 | 关闭活板门判实体（REF-0006 类紧凑竖井误判堵） | 建模"可翻开"语义（需谨慎：会改变 V006 判据，必须配回归测试） |
| 洪泛 interior 脆性 | 无玻璃窗洞 → 室内判 exterior，connectivity 系统性偏低 | 研究"玻璃视同围护"的可选模式并重校准 |
| 跑酷式动线 | 不模拟跳跃/游泳/潜行 → 判断裂 | 文档化为主（改模型代价大、收益不明） |

## 4. Grammar / Metadata 改进项

1. **窗节奏（window_rhythm）**：做立面聚合（窗洞位置序列化），消除全风格 UNKNOWN；
2. **屋顶形制（roof_form）**：在现有材料信号之外做几何重建（坡度/曲线拟合），消除全风格 UNKNOWN；
3. **主入口判定扩展**：多候选门场景引入"门廊/踏步/路径"信号，把 89.4% UNKNOWN 降下来；
4. **房间语义**：维持 LLM_ONLY，不硬编码（任务书 §1.2 纪律）；可研究"功能构件邻近性"弱信号但保持 INFERRED 标注；
5. P1 连通性字段与 P2 修复后模型的差异已通过 P3 重跑对齐；后续任何 walkability 修复必须先快照再重跑。

## 5. 工程化建议

- 把 Validator 接入参考库入库流水线（新资产入库门槛：无 HARD_FAIL）；
- benchmark 的 GENERALIZATION_CASE 判定规则随 grammar 升级而收紧（gap cell 补齐后取消宽松判定）；
- Revision Protocol 的 diff 阈值（30% 回退 / 5% 收敛）当前为 HEURISTIC，积累 LLM 运行数据后重标定。

## 6. 明确的"不要做"

- 不要为让生成器/LLM 分数好看而改 Validator 规则（规则库是评测基准）；
- 不要把审美判断硬编码进 Validator；
- 不要在样本不足时硬建 grammar 类别（375 cell 中 339 个 GAP 如实保留）；
- 不要碰 `D:\Games\Minecraft\` 任何文件（只读铁律延续到下一阶段）。
