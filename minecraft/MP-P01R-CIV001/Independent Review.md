# MP-P01R Independent Review｜minecraft-planner v0.2

审核对象：`minecraft/MP-P01R-CIV001/`

实现提交：`ee03ded24603e05cd33fe4009e4f5308abbbae1e`

Skill：`minecraft-planner v0.2`

Skill 固定提交：`eb58654568d31d96ea1ee50f100e1ef6b927daa0`

审核性质：GPT 独立回归审核；不修改 Canon，不批准 world-write。

## Verdict

> **PASS_WITH_NOTES — v0.2 目标回归通过。**

MP-P01R 已经直接验证 v0.2 针对 P01 暴露出的三个基础问题：

1. current built fabric 未调查时，不再错误使用 `GREENFIELD`；
2. 国家级 Planner 可以正式向下一层 Planner 递归交接，而不是伪装成 Builder package；
3. 国家级节点不仅表达“在哪里”，还表达“目标成熟状态大约有多大”，并明确区分 Location Search Envelope / Built-Fabric Capacity / Functional Hinterland。

当前没有证据要求继续修改 Skill 后再进入 L1 测试。

---

## 1. Context / Evidence — PASS

`planning-objects.json` 明确记录：

- `fabric_observation_state = EXISTING_FABRIC_UNVERIFIED`
- `evolution_logic = EXISTING_EVOLUTION`
- `maturity_state = MATURE_WORKING_HYPOTHESIS`

这解决了 v0.1 在 CIV-001 上只能勉强写 `GREENFIELD` 的语义问题。

方案正文也明确：文明与联盟历史存在，但当前道路、聚落、地权和 built fabric 没有被调查，因此逻辑历史只是 causal reconstruction；下层发现实存后必须进入继承 / 修订，而不是按规划图清空世界。

Source Register 保留了 Observed / Derived / Approved Canon / Skill 的来源、SHA256、snapshot 和 limitations，并明确未读取 MP-P01、后续 G1 / Middle 等既有规划答案。

**结论：v0.2 Context 模型实际生效。**

---

## 2. Settlement Capacity / Scale — PASS

本轮六个重要节点均具有独立的：

- `location_search_envelope`
- `built_fabric_capacity`
- `functional_hinterland`

没有再用一个点同时代表位置、城镇面积和服务范围。

主要 Built-Fabric Capacity hypothesis：

| Node | Role | Built-fabric estimate | Confidence |
|---|---|---:|---|
| NODE-01 | 西域主市场候选 | 20,000–38,000 blocks² | LOW |
| NODE-02 | 北臂集货候选 | 5,000–10,000 | LOW |
| NODE-03 | 联盟公地活动核心 | 10,000–20,000 | LOW |
| NODE-04 | 中域北侧转运候选 | 12,000–24,000 | LOW |
| NODE-05 | 东域北部共同体集散 | 6,000–14,000 | LOW |
| NODE-06 | 东南生产共同体条件候选 | 3,000–9,000；可退为 0 | LOW |

主节点总目标建成面积假设为约 `56,000–115,000 blocks²`，另有西域分散 household / rural built fabric 假设 `6,000–14,000 blocks²`。这些数值被明确标记为 target-maturity sensitivity model，而不是现存人口、精确城界或通用密度常数。

尤其值得通过：

- Commons 全域 92,124 blocks² 与其活动核心 10,000–20,000 blocks² 被严格分开；
- 山地节点明确说明“总建成面积小于地理扩散范围”，没有用单一紧凑圆城替代台地簇；
- NODE-06 有真实 contraction branch，资源 / 水 / 通路不成立时可以不形成常住聚落；
- Capacity 公式保留 household pressure、land allowance、shared service land、drivers、sensitivity 和 exclusions，数字不是裸拍面积。

规划图册增加专门的 `03 聚落规模：搜索 ≠ 建成 ≠ 腹地` 图，并用等面积内外圈表达面积范围；HTML 同时列出面积区间、形态与 LOW confidence。

**结论：Owner 在 P01 中提出的“只有点、看不出城建区域大致多大”问题已被实质修复。**

---

## 3. Recursive Planner → Planner Handoff — PASS

`implementation-packages.json` 不再把 L0 输出伪装成 Builder package。

四个交接对象均明确：

- `parent_scale = POLITY_TERRITORY`
- `child_scale = REGIONAL_SYSTEM`
- `recipient = minecraft-planner`
- `world_write_authorization = false`
- `builder_ready = false`

并实际使用 v0.2 contract：

- `UPSTREAM_FIXED`
- `DOWNSTREAM_TO_RESOLVE`
- `DOWNSTREAM_ADAPTABLE`
- `REVISION_TRIGGER`
- `revision_protocol`

例如 West package 固定“连续生产地不能被集中建成区耗尽、主市场与地方服务分工”，但允许下一层移动主市场、拆分 / 合并地方节点和重新分配容量；若实际供给不足或无可替代场地，则触发 `UPSTREAM_PLANNING_ISSUE` 回修父案。

四个 L1 包分别处理：

1. 西域生产—市场系统；
2. 中域与跨水接口系统；
3. 东域山地共同体系统；
4. Alliance Commons 与三域公共访问接口。

第 4 包作为跨 Region shared system 单独存在是合理的；没有强行把 Commons 塞入某一个地方 Region package。

**结论：v0.2 已具备真正的多尺度递归规划接口。**

---

## 4. Causal / Scale Quality — PASS

P01R 仍保持国家尺度的因果规划，而没有因为新增面积要求下钻成城市总规。

方案继续区分：

- 西域生产 / 人口 /普通市场；
- 中域运输方式转换；
- Commons 共同政治访问；
- 东域山地多点地方服务。

政治中心没有被推成最大城市，货物也没有被强迫经过政治中心。

与 v0.1 的 P01 相比，本轮没有复制原来的 9 个节点，而是重新收敛为 6 个主节点 + 6 条概念关系，并保留 East South 的取消分支；核心网络逻辑却仍收敛到“政治、人口市场、转运中心分离 + 山地分段网络”。这属于较强的稳定性证据：Skill 更像在重复产生同一类因果结构，而不是记住一套固定节点答案。

Critic 也实际导致修订：中域搜索位置移动、R06 从疑似陆路改为条件混合地形调查带、公地用真实成员重算、容量增加供给不足退缩分支。

---

## 5. Evidence / Safety — PASS

验证记录确认：

- 6 nodes；
- 6 routes；
- 4 Planner packages；
- search / capacity / catchment 三种 envelope 已分离；
- capacity arithmetic 自洽；
- Commons area = 92,124；
- 5 张规划图均生成并被执行 Agent 查看；
- pinned Skill bytes match；
- deterministic rebuild equal；
- `world writes = 0`；
- Minecraft save access = NONE。

未验证内容也没有被洗成 PASS：current world freshness、existing fabric、water / food carrying capacity、navigation、exact mineral / fuel resources、exact settlement boundaries 均明确保持 UNVERIFIED。

---

# Findings / Notes

## F01 — Capacity 数字仍是低置信度规划假设

**Class:** EXPECTED_UNCERTAINTY / NOT_A_SKILL_FAILURE  
**Severity:** Minor at L0; must be refined at L1

90–140 households、150–190 blocks² household allowance 等数字不是人口普查或既有项目事实。当前成果正确地把它们标为 `PLANNING_ASSUMPTION / LOW`，并提供 sensitivity / contraction branch，因此 L0 可以接受。

进入 L1 后必须用：

- existing fabric；
- water；
- productive land / supply；
- actual route cost；
- terrain continuity；
- local land tenure

重新校准容量。

不要把 P01R 数字升级为 Canon。

## F02 — L0 等面积圆只表示“量级”，不表示真实聚落形状

**Class:** REPRESENTATION_LIMIT / EXPECTED_AT_SCALE  
**Severity:** Minor

地图使用等面积圆表示 20k–38k 等 Built-Fabric Range，非常适合 Owner 在国家尺度判断“有多大”，但山地 / 岸线聚落实际不可能呈圆形。

P01R 已明确声明这一点，因此当前不是缺陷。

建议 L1 开始根据真实 buildable pockets、route frontage、water / slope constraint 生成 terrain-constrained provisional envelope，而不继续只用圆。

## F03 — 当前实存与 terrain freshness 尚未读取

**Class:** EVIDENCE_BOUNDARY  
**Severity:** Expected

这正是 v0.2 Context Contract 要表达的情况。不得把它变成 P01R 的失败；但所有 child packages 在第一次 L1 使用时必须首先刷新相关 evidence。

## F04 — Blindness 不是全新会话级物理隔离

**Class:** TEST_BOUNDARY  
**Severity:** Minor

Agent 主动声明共享上下文中曾出现项目状态信息，但实际 source register 没有读取 MP-P01 / later planning artifacts。当前足以用于回归判断，但未来高要求 benchmark 最好继续采用独立 runner / fresh context。

---

# Skill Decision

**不建议因 MP-P01R 再更新 `minecraft-planner`。**

v0.2 的三个目标修订已经获得直接正向证据：

1. Existing-but-unobserved Context：PASS；
2. Settlement Capacity / Built-Fabric Envelope：PASS；
3. Recursive Planner Handoff：PASS。

继续修改反而容易在尚未测试 L1 / L2 的情况下过早扩张规则。

下一步应进入 **MP-P02｜REGIONAL_SYSTEM**，用 P01R 的真实 child package 测试 v0.2 是否能把上层约束转化为更细的区域 settlement network、capacity refinement 与下一层 handoff。

建议优先选择 **东域山地共同体系统（PACKAGE-03）**：它同时具有地形阻力、分散 settlement、资源位置不确定、容量可退缩和条件性远端节点，能最大程度检验 Planner 在 L1 的真实能力，而不会又回到 G1 式微街区问题。

---

## Final Verdict

> **PASS_WITH_NOTES — MP-P01R 通过；minecraft-planner v0.2 可进入 L1 Regression。**

本结论只批准继续规划测试，不批准修改 Canon 或 Minecraft world-write。
