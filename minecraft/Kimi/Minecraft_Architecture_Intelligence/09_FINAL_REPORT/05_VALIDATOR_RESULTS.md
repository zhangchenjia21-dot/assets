# 05_VALIDATOR_RESULTS — Spatial Validator 结果（P7 最终报告 5/8）

> 实现：`05_SPATIAL_VALIDATOR/validator_source/`（spatial_context / rules / core / CLI）；
> 规范：`VALIDATION_SPEC.md`；阈值外置：`validator_rules.json`；测试：`08_EVALUATION/VALIDATOR_TESTS.md`。

## 1. 规则清单（12 条，严重级与性质）

| 规则 | 名称 | 严重级 | 性质 | 一句话判据 |
|---|---|---|---|---|
| V001 | No Exterior Entrance | HARD_FAIL | HEURISTIC | 有内部空间但无任何入口候选（外门/开口/舱口） |
| V002 | Main Entrance Blocked | HARD_FAIL | HEURISTIC | 主入口门槛/门外/门内接近站位缺失或两侧不同分量 |
| V003 | Major Interior Unreachable | HARD/WARN | HEURISTIC | 主入口分量覆盖 <50% 内部站位且不可达 ≥9；隔离环含可交互构件降 WARN |
| V004 | Isolated Room / Space | HARD/WARN | HEURISTIC | 主内部分量之外存在 ≥9 站位的内部分量（露天不计）；纯实体封闭且 ≥20 升 HARD |
| V005 | Stair Bottom Blocked | HARD_FAIL | OBSERVED | 有意义楼梯簇全部底格不可进入 |
| V006 | Stair Top Blocked ★ | HARD/WARN | OBSERVED | 全部顶格无出口（"楼梯尽头是墙"）；顶格被实体埋住降 WARN |
| V007 | Vertical Circulation Broken | HARD_FAIL | HEURISTIC | ≥2 可用楼层且各层站位无连通交集 |
| V008 | Door Clearance Failure | WARNING | HEURISTIC | 门沿通行轴任一侧缺接近站位 |
| V009 | Severe Headroom Failure | WARNING | HEURISTIC | 低净高格 ≥12 且占内部站位 ≥35% |
| V010 | Exterior Envelope Gap | WARNING | HEURISTIC | 排除设计性开口后泄漏 ≥10 格且 ≥2% 内部空气 |
| V011 | Roof Coverage Anomaly | WARNING | HEURISTIC | 无屋顶柱 ≥12 且占内部柱 ≥20% |
| V012 | Dead-end Circulation | INFO/WARN | HEURISTIC | 内部死端站位 ≥6（INFO）/ ≥15（WARN），纯统计提示 |

底层模型：walkability（站位 = 支撑体素 + 净高 ≈1.8；水平 4 邻 ΔE≤0.5、楼梯助推 ≤1.0；梯柱垂直边完全二部连接；非铁质门/栅栏门可交互开启 = 可过，关闭铁门 = 阻挡）。**air 为显式体素**，包络内未覆盖坐标按 air 处理。

## 2. 测试覆盖（30/30 通过）

- 最近运行：2026-09-13 02:58，`py -3 -m unittest tests.test_walkability tests.test_validator -v` → **Ran 30 tests — OK（0.051s）**。
- test_validator.py 19 例：V001–V007 七条 HARD 规则全部有正例+负例断言（任务书 §12 达标）；`stair_top_blocked` 负例为 V006 必现回归锁；`test_rooftop_component_not_counted_as_isolated_room` 锁定"露天分量不计孤立房间"的 P1 教训。
- test_walkability.py 11 例：平地/墙/半砖/楼梯/门语义/栅栏/梯子/净高/未知方块/死端。
- **已知覆盖缺口（诚实声明）**：V008–V012 无独立负例夹具（WARNING/INFO 级只有输出存在性断言）；机制感知降级路径（V003/V004 降 WARNING）无合成夹具锁定（在 V4 C-before 真实样本上出现过并人工核对）；舱口入口、交替梯子竖井等低频路径无夹具。

## 3. 全库指标（123/123，PARSE_FAILURE 0）

| 指标 | 值 |
|---|---|
| hard_fail_rate | **0.4959**（61 张 ≥1 条 HARD_FAIL） |
| warning_rate | 0.5935（73 张） |
| validation_status | HARD_FAIL 61 / WARNING 25 / PASS 37（34 张零触发） |
| walkability_score | mean 92.3（min 64.5，max 100） |
| connectivity_score | mean 51.3（内部空间大量不连通——参考库从未承诺内部可通行） |
| vertical_circulation_score | mean 97.3；UNKNOWN 43 张（开放结构/楼层未检出，规则设计如此） |
| validator_confidence | high ×123（归一化后未知方块为 0） |
| 运行性能 | 全库单批 <2 分钟（Windows，py -3，最大 ~17 万体素包络） |
| 校准轨迹 | 0.829 → 0.496（7 轮，见报告 04 第 2 节） |

**false positive / negative 声明**：抽查方法 = 每条 HARD 规则抽 2–3 个触发样本逐体素核实（SpatialContext 复现）。结论：残余触发以真阳性/歧义阳性为主，无系统性误报残留；**false negative 未做系统性测量**（无全库人工标注 ground truth——这是已知限制，见下）。

## 4. Known Limitations（摘要，全表见 `known_limitations.md`）

1. 蓝图不含地形：包络底界悬空放行；包络内半空悬门仍触发 V002。
2. 洪泛 interior 脆性：无玻璃窗洞/拱洞 → 内部空气被吸成 exterior，connectivity_score 系统性偏低（REF-0003 实测；V4-A 因此 6 条规则 NOT_APPLICABLE）。
3. 内部空间意图不可判：密封装饰空腔（树腔/墓室/压舱/屋顶结构层）几何 = "无入口封闭空间"，标"歧义阳性"保留触发。
4. 机制类通道未完全建模：关闭铁门=阻挡（红石不建模）；活板门-楼梯交替竖井判堵（REF-0006）。
5. 玩家能力近似：不模拟跳跃/游泳/潜行（跑酷式设计会判断裂）。
6. 规则级盲区逐条见 known_limitations §2 表（V001–V012 各一行）。
7. P1 元数据连通性字段为修复前模型计算，与 P2 存在已知差异；P3 开始前已重跑对齐（分布 median 基本不变）。

## 5. 职责边界

Validator 管"客观正确性"（有没有空间错误）；设计是否合理归 Critic（`07_ARCHITECT_SYSTEM/CRITIC_RULEPACK.md`）；审美终裁归人工。Validator 不评美、Critic 不重复 V001–V012——职责分离已写入两个 Rulepack 的显式声明。
