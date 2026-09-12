# 03_ARCHITECTURAL_GRAMMARS — 建筑语法发现（P7 最终报告 3/8）

> 数据来源：`03_TAXONOMY/`（taxonomy 与标签）、`04_GRAMMARS/STYLE_GRAMMARS.md`、`FUNCTIONAL_GRAMMARS.md`、
> `grammar_confidence_report.md`、`data_gap_matrix.json`。
> 样本纪律：n≥8 SUPPORTED（可 STRONG）；n=4–7 PROVISIONAL（最高 SOFT）；n<4 OBSERVATION ONLY（不出规则）。

## 1. 分级总览

### Style（111 条规则）

| 类别 | n | 级别 | 规则数 | HARD/STRONG/SOFT/OPTIONAL |
|---|---:|---|---:|---|
| Medieval | 19 | SUPPORTED | 22 | 0/5/13/4 |
| Rustic | 20 | SUPPORTED | 23 | 0/6/11/6 |
| Fantasy | 10 | SUPPORTED | 22 | 0/4/14/4 |
| Japanese | 7 | PROVISIONAL | 23 | 0/0/17/6 |
| Chinese | 4 | PROVISIONAL | 21 | 0/0/17/4 |
| Other | 7 | OBSERVATION ONLY（异质） | 0 | — |
| Unknown | 56 | 非类别 | 0 | — |

Style 维度**无 HARD**（HARD = 功能必需，只出现在功能语法）。候选类 Modern/Industrial/Gothic/Victorian/Nordic 全库 0 样本，**不硬建**。

### Function（117 条规则）

| 级别 | 类别（n） | 规则数 |
|---|---|---|
| SUPPORTED | Residential(23) / Decoration(22) / Castle(14) / Tower(13) / Religious(10) | 5×13 = 65 |
| PROVISIONAL | Workshop(7) / Vehicle(7) / Inn(5) / Civic(4) | 4×13 = 52 |
| OBSERVATION ONLY | Gate(3) / Blacksmith(3) / Farm(3) / Mixed-use(2) / Warehouse(1) | 0 |
| 非类别 | Unknown(6) | 0 |

唯一 HARD 规则：**Tower 多层 ⇒ 必有垂直交通**（条件频率 1.00，n_multi=8，HEURISTIC）。
**新增类**：Vehicle（载具/运输构筑，n=7，候选表无、样本支持）；候选类 Bridge 0 样本未建立。

## 2. 最强量化规律（带 sample_n 与区间，可直接消费）

以下全部是 OBSERVED/HEURISTIC 统计、INFERRED 成规则；完整清单见 `style_rules.json` / `functional_rules.json`。

**材料族（OBSERVED，high 置信）**
- Medieval 石占比 median 0.589，IQR [0.389, 0.625]，n=19（STRONG）；木 0.165 [0.110, 0.233]。
- Rustic 石 0.380 [0.283, 0.446]、木 0.195 [0.171, 0.301]，n=20；**Rustic 高对称（≥0.9）频率 = 0.0**（n=20，与 Medieval 0.316 形成可机检的风格区分信号）。
- Fantasy 石 0.698 [0.483, 0.755]、装饰族 0.106 [0.050, 0.156]，n=10。
- Japanese 木 0.254 [0.227, 0.295]（n=7，PROVISIONAL）；Chinese 石 0.535 [0.478, 0.615]（n=4）。

**体量/比例**
- Medieval footprint_ratio median 1.091，IQR [1.046, 1.229]，n=19（STRONG，OBSERVED）。
- Rustic height_ratio 0.823 [0.741, 0.964]，n=20（STRONG）；floor_count median 2.0 [1.0, 2.0]（n=18，HEURISTIC）。
- Rustic floor_height median 6.0 格（IQR [4.875, 9.5]，n=12）；Japanese 8.0（n=4，low）。
- 层高基准值（benchmark 锚定）：Medieval/Rustic/Chinese fh=5，Fantasy/Japanese fh=6。

**功能画像（HEURISTIC 为主）**
- Residential：至少 1 扇外部门频率 0.78（n=23，STRONG）；垂直交通存在频率 1.00；可用楼面中位 1342 格 [926, 1948]（n=19）；死端比例中位 0.133。
- Castle：外部门候选中位 15（[0.5, 26.75]，n=14）；可用楼面中位 2206 格。
- Tower：≥2 层频率 0.62；多层⇒垂直交通条件频率 1.00（唯一 HARD）。
- Decoration / Vehicle 为**负向画像**：外部门候选中位 0、垂直交通中位 0——"无门无室内"本身是功能特征，生成侧不得强加门和房间。

## 3. UNKNOWN 维度（全库性知识缺口，诚实清单）

| 维度 | 范围 | 原因 |
|---|---|---|
| entrance_placement（入口方位/位置规律） | 全部 5 风格 + 全部 9 功能类 | main_entrance 可判定样本过少（全库 89.4% UNKNOWN 的纪律结果） |
| window_rhythm（窗洞位置节奏） | 全部 5 风格 | 需立面聚合，本阶段未做（window_density 已有，节奏 UNKNOWN） |
| roof_form（屋顶形制/坡度曲线） | 全部 5 风格 | 未测量（现有 roof_height_ratio / material_share 是材料信号，非几何重建） |
| floor_height | Medieval / Fantasy / Chinese | 可得样本不足半数或 <4 |
| floor_count | Chinese | 可得样本 3/4 |
| 房间语义（bedroom/kitchen 等） | 全库 | IR 不可判；zone 均为 walkable connected region；公私分区为 INFERRED |
| 全部维度 | Other / 5 个 0 样本风格 / n<4 功能类 | 异质或样本不足 |

## 4. 缺口矩阵（任务书 §24，Q2/Q6 的量化底座）

- 维度：5 style × 15 function × 5 size_class = **375 cell**；size_class 复用 V6C2 scale。
- 覆盖：**非零仅 36 cell（9.6%）**；GAP 339 / OBSERVATION 35 / PROVISIONAL 1。
- 优先级：P0=50 / P1=31 / P2=293 / P3=1。
- P0 全部集中在村落核心功能（Inn/Civic/Gate/Blacksmith/Farm/Warehouse/Bridge）× Medieval/Rustic × small/medium——典型如「Medieval × Inn × small/medium」「Rustic × Farm × small/medium」「Bridge 全库 0 样本」。
- 结论（Q2）：122 张对**类别级** grammar 部分足够（3 风格 + 5 功能 SUPPORTED），对**组合级**（style×function×size）严重不足——90.4% cell 空缺，无法支撑组合级 grammar。

## 5. 交叉验证与降级纪律

- 分类主信号 = V6C2 人工+规则审核分类；P1 几何/材料字段只做校验/下调，从不单独提拔。
- 实际降级 5 条（chinese@0.48 ×3、japanese@0.48 ×1、desert@0.48 ×1 → Unknown，阈值 0.55）；全库未发生几何强冲突。
- grammar 标 UNKNOWN 的维度，Architect Rulepack 同样标 UNKNOWN、不编数值规则（见 `07_ARCHITECT_SYSTEM/ARCHITECT_RULEPACK.md` §2），交 LLM 自由发挥或人工。
