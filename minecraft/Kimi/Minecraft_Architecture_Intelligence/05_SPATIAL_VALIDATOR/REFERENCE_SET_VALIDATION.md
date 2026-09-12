# REFERENCE_SET_VALIDATION — 全库 123 张参考蓝图校验报告（P2）

> 运行：`py -3 05_SPATIAL_VALIDATOR/validator_source/validate_blueprints.py --input <references\derived> --output 05_SPATIAL_VALIDATOR\validation_run`
> 输入只读；输出 `validation_run/validation_results.jsonl` + `validation_summary.json`。
> 校验器版本：迭代 7（迭代轨迹见 VALIDATION_SPEC.md 第 4 节）。

## 1. 总量指标

| 指标 | 值 |
|---|---|
| blueprints_validated | **123 / 123**（PARSE_FAILURE 0） |
| hard_fail_rate | **0.4959**（61 张至少 1 条 HARD_FAIL） |
| warning_rate | **0.5935**（73 张至少 1 条 WARNING） |
| validation_status 分布 | HARD_FAIL 61 · WARNING 25 · PASS 37（其中 34 张零触发） |
| HARD_FAIL 共现深度 | 1 条:32 张 · 2 条:21 张 · 3 条:8 张 |
| walkability_score | mean 92.3（min 64.5，max 100） |
| connectivity_score | mean 51.3（内部空间大量不连通，见 V003/V004 分析） |
| vertical_circulation_score | mean 97.3；UNKNOWN 43 张（开放结构/楼层未检出） |
| validator_confidence | high ×123（归一化后未知方块为 0） |

## 2. 逐规则触发频率表

| 规则 | 名称 | 触发数 | HARD_FAIL | WARNING | INFO |
|---|---|---|---|---|---|
| V001 | No Exterior Entrance | 20 | 20 | – | – |
| V002 | Main Entrance Blocked | 14 | 11 | 3 | – |
| V003 | Major Interior Unreachable | 35 | 21 | 14 | – |
| V004 | Isolated Room / Space | 54 | 32 | 22 | – |
| V005 | Stair Bottom Blocked | 3 | 3 | – | – |
| V006 | Stair Top Blocked | 13 | 7 | 6 | – |
| V007 | Vertical Circulation Broken | 4 | 4 | – | – |
| V008 | Door Clearance Failure | 11 | – | 11 | – |
| V009 | Severe Headroom Failure | 41 | – | 41 | – |
| V010 | Exterior Envelope Gap | 0 | – | 0 | – |
| V011 | Roof Coverage Anomaly | 0 | – | 0 | – |
| V012 | Dead-end Circulation | 55 | – | 34 | 21 |

V010/V011 全库零触发：参考库围护/屋顶完整性整体良好（或缺陷低于高置信度阈值，
见 known_limitations.md）。V009 触发率 33% 偏高——"低净高格"无法区分通道压抑与装饰性
暗格，保持 WARNING 级并在已知限制中声明。V012 为 HEURISTIC 统计提示，不参与 HARD 判定。

## 3. false_positive_review（人工抽查）

方法：每条 HARD 规则抽 2–3 个触发样本，结合 `02_BLUEPRINT_METADATA`、
`references\derived\<REF>\analysis.md` 与逐体素探查（SpatialContext 复现）判定。
**重要背景**：这些参考资产的 analysis.md 普遍标注"内部交通未验证；REFERENCE_ONLY"——
参考库按外观精选，从未承诺内部可通行。

### V001（20 触发）——结论：基本真阳性，语义歧义已降级处理并声明
- **REF-0005 中世纪大门守卫房**（迭代前触发）：**误报**——守卫室经梯子+舱口进入，
  旧模型梯子边漏接。修复梯子二部连接与舱口入口检测后不再触发。✅ 已修复
- **REF-0022 六角亭**：触发 = 屋顶结构腔（y15–23 封闭空间）无入口。几何事实成立，
  但该空间是屋顶结构层而非房间。**歧义阳性**（装饰性空腔），已在 known_limitations 声明。
- **REF-0035 唐屋_小**：内部 3433 格全封闭、全库 0 个门方块、无开口——**真阳性**
  （壳体式资产，作者没留门）。
- **REF-0032 哈利卡纳苏斯陵墓**：封闭墓室——陵墓封死符合语义，**意图性封闭**。

### V002（11 HARD + 3 WARNING）——结论：真阳性为主
- **REF-0122 魔法空岛小屋**：门内侧是 5 格深的竖井（地板在 y=27，门在 y=32）——
  进得去出不来，**真阳性**。
- **REF-0021 八角塔**：门外地面在门槛下 2 格（E=5.0 vs 门槛 7.0），无台阶——
  出去要跳、回来上不去，**真阳性**（或依赖未包含的地形，已声明）。
- **REF-0038 圣埃德大教堂**（舱口主入口）：邻域 2 格内确有站位但语义不确定 →
  已降为 **WARNING**。舱口类主入口统一降级处理。

### V003（21 HARD + 14 WARNING）——结论：真阳性为主
- **REF-0004 中世纪四层小屋**：楼层 1/2 连通，3、4 层（y=8/13，各 111+ 内部站位）
  无任何楼梯/梯子连接（簇 2 只到 y=4，簇 1 是 y=11–17 的大面积屋顶薄板）。
  **真阳性**，与 V007 共发。
- **REF-0026 利维坦号**：4912 个内部站位与主分量断开，隔离环含 490 个活板门——
  甲板间舱口通道依赖活板门（模型中关着的活板门是实体）→ 已降 **WARNING**。
- **REF-0002 世界之塔**：塔内房间经无玻璃窗洞洪泛成"外部"，内部站位稀少、主入口
  内房间可达性低——部分为建模边界情形，保留触发、置信度 high（门禁侧几何明确）。

### V004（32 HARD + 22 WARNING）——结论：露天误报已消除；剩余为真封闭空间
- **全库系统性误报（露天分量）**：迭代前 V004 触发 51 且大量来自屋顶/树冠天然分量——
  通过"内部站位 = 身体格在洪泛内部空气中"定义修复，回归夹具
  `test_rooftop_component_not_counted_as_isolated_room` 锁定。✅ 已修复
- **REF-0042 大圣诞树**：树腔 983 内部站位、隔离环纯实体——客观封死，**歧义阳性**
  （装饰性空腔）。
- **REF-0026 利维坦号 / REF-0103 糖果城堡**：隔离环含大量门/活板门 → **WARNING**
  （机制感知分级生效）。

### V005（3 触发）——结论：数量少，疑似真阳性但带舱口/装饰歧义
- **REF-0003 中世纪农舍 / REF-0046 女巫小屋**（迭代前触发）：包络底界的室外台阶，
  入口在未包含的地形上——`skip_bottom_at_envelope_floor` 后不再触发。✅ 已修复
- **REF-0054 帆船 / REF-0056 飞艇**：现存触发为桅杆/索具层的小楼梯簇（底格被
  栅栏/木板围死）。几何上确不可进入；是装饰纹理还是坏梯子无法静态区分——保留触发，
  数量仅 3，可人工复核。

### V006（7 HARD + 6 WARNING）——结论：核心规则工作正常，夹具必现
- **回归夹具 `stair_top_blocked`**：顶端三面砌墙 → HARD_FAIL 稳定触发（测试锁定）。
- **REF-0006 中世纪工具匠铺**：楼梯簇顶端被关闭的木活板门+上面一层楼梯压住
  （活板门-楼梯交替的紧凑竖井 trick），模型视为实体 → 触发。玩家实际可翻开活板门——
  **歧义**，已声明为已知盲区。
- **REF-0009 中世纪据点_小**（迭代前触发）：顶端被关闭的橡木栅栏门拦住——栅栏门
  改为可交互开启后不再触发。✅ 已修复
- **REF-0071 月宫**：顶端落点方向悬空无支撑（高台式宫殿的装饰梯）——**真阳性**倾向。

### V007（4 触发）——结论：真阳性 2，启发式伪影 2（已声明）
- **REF-0004**：见 V003，**真阳性**。
- **REF-0006**：上层翼楼仅靠活板门竖井连接 → **真阳性**（同 V006 歧义链）。
- **REF-0042 大圣诞树 / REF-0035 唐屋_小**：树冠密实层/屋顶密实层被楼层密度启发式
  误判为"楼板"，腔内站位计为该层 → 楼层断裂。**启发式伪影**，已在
  known_limitations 声明（楼层检测本身是 HEURISTIC）。

## 4. 校准结论

1. 迭代 0 的 hard_fail_rate=0.829 确实是 Validator 问题（任务书预判正确）：洪泛
   interior 语义脆、梯子边漏接、装饰楼梯薄板未排除、门通行轴未用 facing、栅栏门语义
   过严、露天分量误算孤立房间——六轮修复后降至 **0.496** 并稳定。
2. 残余 HARD_FAIL 的抽查结论是**真阳性/歧义阳性为主**：精选库的内部交通从未被验证
   （analysis.md 自述），密封装饰空腔、壳体建筑无门、门面悬空等问题客观存在。
   Validator 没有系统性误报残留。
3. 所有"模型无法分辨意图"的情形均已通过机制感知分级降为 WARNING 或在
   known_limitations.md 声明，未虚构通过。
4. 回归测试 30/30 绿（walkability 11 + validator 19），每条 HARD 规则有正例+负例断言，
   V006 负例（楼梯尽头是墙）必现。
