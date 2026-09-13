# MP-P01 Independent Review｜minecraft-planner v0.1

Review target: `c12ce5419f6a5567a3d9db91a530543244a845f3`

## Verdict

> **PASS_WITH_FINDINGS — P01 证明 v0.1 已具备真实的 POLITY_TERRITORY 级因果规划能力；但在递归 Planner→Planner 交接与“已有文明、当前聚落实存未知”的 Context 语义上暴露出两个第一版结构缺口。规划图的 Owner 视觉可读性仍需真人确认。**

本结论只评价本轮国家级规划回归，不批准任何 World Canon、区域总规、聚落落位或 world-write。

---

## 1. 测试纪律 / 输入隔离 — PASS_WITH_NOTE

本轮实际读取 `minecraft-planner v0.1`、6 份适用 reference、CIV-001 Minimal Canon、Current Natural Atlas 子集与 R1 自然地理数据；`source-register.json` 明确记录未读取 G1/N1/Middle 后续规划、Architecture Design 与相关评审。Skill / Canon / terrain / proposal 的 authority 也有区分。

正向点：

- 没有把 Current Atlas 当成 Canon 或施工授权；
- 没有把具体矿口、港深、航运能力、水源等未证事实伪装成 Observed；
- 明确 `world reads = 0 / world writes = 0`，使用的是已接受快照；
- 主动说明共享会话中存在过项目状态摘要，因此不虚假声称“新会话级盲测”。

Note：由于共享上下文曾出现项目状态，本轮是**有纪律的信息隔离**，不是严格物理隔离 benchmark。若未来要比较不同模型，应使用真正无后续规划上下文的新会话 / 独立工作区。

---

## 2. Scale Discipline — PASS

这是本轮最重要的正向结果之一。

Planner 没有从 L0 直接下钻到街区、parcel 或建筑平面，而是停在：

- territorial / regional roles；
- settlement search anchors；
- long-distance flow；
- qualitative catchment；
- causal growth；
- 3 个下一层 `REGIONAL_SYSTEM` package。

`building-program.json` 也明确把需求表达成区域功能，而不是建筑数量；例如西域只要求“生产腹地生活/维护、周期交易与储备、分散水粮保障”，并明确“不规定 dedicated building”。这符合 `Demand ≠ Building`。

没有出现“国家尺度直接决定某间铁匠铺 / 某街区道路”的尺度越权。

---

## 3. Territorial Causality — PASS

本轮不是把三域机械翻译成三块 zoning，而是形成了一个有辨识度的国家级空间命题：

> **政治中心、人口/市场中心、货物转换中心分离；东域采用分段地方服务网络。**

该结果有可追踪因果：

- 西岛低平与 C 形绕行成本 → 南部主要市场 + 北弧次级市场，而不是单一中心吞掉全岛；
- 跨水 / 坡麓运输方式转换 → 03 / 05 接驳与换载角色；
- 三席共同治理与地方自治 → Commons 具有高政治位阶但不自动成为人口 / 贸易首都；
- 东岛高起伏、主脊阻力 + 东域矿业 Canon → 分段山地服务 / 就近减重，而不是“一座东域矿业首都 + 一条直线大道”；
- 远端南岸只保留条件性海运替代，未把未知航运升级成事实。

这是 v0.1“因果关系 → 空间结构”核心使命的直接正向证据。

---

## 4. Demand / Flow / Externality — PASS

`demand-matrix.json` 与 `flows-externalities.json` 基本实现了 Skill 想要的中间层：

- Demand 记录 driver / users / magnitude / frequency / dependency / externality / maturity / possible response；
- 食物、矿业、换载、共同治理、地方日常、燃料维护、信息防御、外部交换没有直接一一映射成独立建筑；
- 货流、政治流、日常流被区分；
- 矿业污染、清水、燃料、侵蚀等 externality 没被简化成现代“工业区”。

尤其 `FLOW-03` 把政治代表流指向 Commons，同时允许主要商品流绕过政治中心，是很好的反现代单中心规划表现。

---

## 5. Anchor / Settlement Hierarchy / Catchment — PASS_WITH_FINDING

9 个节点不是 9 座被宣布存在的城市，而是 `settlement_search_anchor`，均带 96-block 搜索窗和 uncertainty；角色也区分 regional center、gateway、institutional center、mountain service、specialized exchange、conditional maritime alternative。

这比“每域一个主城 + 若干村”更成熟。

但 machine-readable taxonomy 仍略显过早把所有重要节点写成 `SETTLEMENT-xx`：例如 Commons 的制度中心、换载搜索点、条件性海运替代本质上首先是**planning node / anchor role**，并不都已经证明会成熟为 settlement。

**Finding P01-F01 — Node identity is slightly settlement-biased**  
Class: `SKILL_GAP / MODEL_EXECUTION_WATCH`  
Severity: Minor.

建议后续允许 L0 使用更中性的 `NODE-* / ANCHOR-*`，只有在 settlement existence / persistence 得到充分理由后再提升为 `SETTLEMENT-*`。

---

## 6. Causal Growth / Path Dependence — PASS

`growth-sequence.json` 不是简单年代列表，而是每阶段显式保存：

`driver → response → new_constraint → next_pressure → standalone_viability`

且四阶段都做了 Historical Validity：

- GROWTH-01 不依赖未来联盟；
- GROWTH-02 双边季节贸易不依赖未来议会；
- GROWTH-03 联盟制度不依赖南岸外贸；
- GROWTH-04 允许节点降级 / 收缩而不是永远增长。

这是本轮很强的正向信号：模型没有把“最终国家结构”反写成早期居民预知的总图。

---

## 7. Terrain Necessity / Route Discipline — PASS_WITH_UNVERIFIED_BOUNDARY

Planner 实际用标高、land component、slope8 修正了多个候选点；Critic 还记录把过陡的 08 / 09 移到更合理的搜索位置，并把最大采样坡比 2.39 的路线重做后仍只称为“走廊搜索见证”。

这是很好的 epistemic discipline：

- 水面 topology ≠ 可航；
- 8-block sampled route ≠ Minecraft 可走道路；
- slope threshold ≠ 驮运实证；
- search point ≠ site。

`validation.json` 也明确把 `route_usable_clearance_or_navigation = UNVERIFIED`，没有用几何线长度冒充实际运输能力。

因此 Terrain Necessity 本轮通过，但**任何路线可施工性仍未验证**，应留给 L1 / 更高分辨率证据。

---

## 8. Critic Quality — PASS

本轮 Planner Critic 有实际修订，不是纯 checklist：

- 修改高坡候选点；
- 重做异常山地路线；
- 修复图签和 Growth 图的时序表达；
- 执行 Terrain counterfactual、Anchor removal、Historical validity、Anti-zoning、Terrain necessity、Parcel causality、Kit clone。

尤其：

> 如果两岛陆连，03候渡需求显著下降；如果移除 Commons，政治流消失但 01/03/05 的交易仍有理由。

这种 counterfactual 确实验证了因果结构，而不是只复述最终方案。

---

## 9. Context Modifier — FOUNDATIONAL FINDING

`planning-objects.json` 把 Context 标为 `GREENFIELD`，随后用 note 解释：这里只表示“本轮从人文关系空白开始规划”，并明确“不知道现状不能推平”。这个处理避免了实际错误，但语义本身并不理想。

CIV-001 是一个明确已经存在并具有历史的成熟联盟；真正未知的是：**当前世界里的聚落 / 道路 / 地权实存没有被本轮读取**。这既不是严格 GREENFIELD，也不能安全宣告为完整 `EXISTING_EVOLUTION`。

**Finding P01-F02 — Context vocabulary lacks an existing-but-unobserved state**  
Class: `SKILL_GAP`  
Severity: Major / Foundational, but not a P01 failure.

建议 v0.2 引入类似：

- `GREENFIELD`
- `EXISTING_EVOLUTION`
- `EXISTING_STATE_UNKNOWN` / `CURRENT_FABRIC_UNVERIFIED`

或者把 `maturity/history` 与 `current_fabric_observation` 拆成两个正交字段。

这个缺口应在下一轮 Existing / Regional regression 前修正，避免未来模型把“没读现状”误解成“现状为空”。

---

## 10. Recursive Planner → Planner Handoff — FOUNDATIONAL FINDING

P01 的最高尺度行为暴露了 v0.1 一个更重要的结构缺口。

`implementation-packages.json` 的接收者实际是 `next minecraft-planner`、尺度为 `REGIONAL_SYSTEM`，这是正确方向；但 package schema 仍沿用了 Builder handoff 的 `planner_fixed / builder_adaptable`。例如一个 L0→L1 package 同时写着 `recipient = next minecraft-planner`，却列出 `Plan/Section / roof / facade / palette` 等 `builder_adaptable` 字段。

这不是 P01 模型本身的严重错误，而是当前 reference 只有清晰的 **Planner→Builder contract**，却缺少等价明确的 **Planner→Planner recursive inheritance contract**。

**Finding P01-F03 — Recursive handoff contract is missing**  
Class: `SKILL_GAP`  
Severity: Major / Foundational.

建议 v0.2 增加：

- `UPSTREAM_FIXED`：已接受的 L0 关系；
- `DOWNSTREAM_TO_RESOLVE`：L1 必须自行调查 / 推导的问题；
- `DOWNSTREAM_ADAPTABLE`：L1 可改变的节点位置、规模、catchment、corridor geometry 等；
- `REVISION_PROTOCOL`：L1 新证据如何请求回退 L0；
- 只有到真正 Builder-facing 的 package 才使用 `PLANNER_FIXED / BUILDER_ADAPTABLE`。

这应在 P02 `REGIONAL_SYSTEM` 前修正，因为 P02 正是第一轮递归下钻测试。

---

## 11. Handoff Boundary — PASS_WITH_NOTE

正向：三个 package 都明确 `direct_builder_ready = false`、`world_write_authorization = false`，并解释“L0→L1 尚无 parcel / envelope，不向 Builder 伪造可直接施工包”。这一点非常重要。

Note：`planner_fixed` 当前写“保留本轮提出的节点角色关系”，在本轮还只是 `DESIGN_PROPOSAL / GPT+Owner review pending` 时，不应被理解为真正冻结。只有 Owner / 上游审查接受 L0 方案后，这些关系才能成为下一层的 fixed authority。

因此推荐状态解释为：

> `HANDOFF_READY_FOR_REVIEW`

而不是“已经可以直接派发到 L1”。这是命名/状态语义问题，不影响本轮规划质量。

---

## 12. Planning Maps — TECHNICAL PASS / OWNER VISUAL REVIEW REQUIRED

归档包含：

- territory；
- flows；
- catchments；
- growth-1..4；
- terrain-base；
- HTML 切换入口。

`validation.json` 证明图片可解码、坐标转换存在，并记录世界坐标 / orientation / scale；`index.html` 也明确提示点是搜索代表、路线是候选。

独立审核端当前只能验证这些 artifact 的存在、坐标/来源约束和生成逻辑，不能等价替代 Owner 实际打开规划图后的视觉判断。

另有一个轻微 UI QA：`index.html` 重复出现两个“节点与腹地”按钮；不影响规划内容。

Map verdict：`TECHNICAL_PASS / PERCEPTUAL_READABILITY_PENDING_OWNER`。

---

## 13. Overall Skill Regression Result

### Strong positives

P01 已证明 `minecraft-planner v0.1` 至少具备以下真实能力：

- 能在国家 / 联盟尺度工作，而不是退化成 G1 街区规划器；
- 能区分 Canon、Observed / Derived、Planning Assumption 与 Design Proposal；
- 能从 Terrain + Institution + Economy + Flow 推导多中心 territorial system；
- 能避免现代 zoning 和“一域一城”的机械对称；
- 能输出 causal growth，而不是最终图的事后故事；
- 能保持 Scale Discipline；
- 能把 L0 结果停在 L1 handoff，而不是直接施工。

### Remaining first-version gaps

1. Context vocabulary 缺少“文明已存在，但 current built fabric 未观测”的状态；
2. 缺少正式 Planner→Planner recursive handoff contract；
3. L0 node ID 语义略偏向把所有 anchor 预先称为 settlement；
4. Map 的最终直观可读性仍需 Owner 真人确认。

## Final verdict

> **PASS_WITH_FINDINGS**

P01 的目标——验证 `minecraft-planner` 是否具有真正的 `POLITY_TERRITORY` 级因果规划能力——已通过。

不建议因为个别节点或路线判断去改 Skill；但 P01-F02 / P01-F03 属于**跨任务通用、且下一尺度马上会碰到的架构缺口**，适合在 P02 前进入 `minecraft-planner v0.2` 的小幅结构修订。

下一步建议：

1. Owner 先独立查看 maps / HTML，补充视觉与世界观直觉反馈；
2. 根据 Owner 反馈最终确认 P01；
3. 若无新的 blocker，将 F02 / F03（以及可选 F01）纳入 v0.2；
4. 然后以 P01 已接受的一个 Region 进行 P02 `REGIONAL_SYSTEM` 回归；继续 `world writes = 0`。
