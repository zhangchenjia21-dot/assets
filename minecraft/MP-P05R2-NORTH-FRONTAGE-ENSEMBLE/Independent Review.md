# MP-P05R2 Independent Review｜minecraft-planner v0.5

日期：2026-09-14  
审核对象：`minecraft/MP-P05R2-NORTH-FRONTAGE-ENSEMBLE/`  
实现提交：`96425b0867c9a8fa9aa0a2032c45398b27093571`  
测试：`MP-P05R2｜北侧两户混合前沿 / URBAN_ENSEMBLE / Planner→Builder handoff`

## Verdict

> **PASS_WITH_NOTES — v0.5 Planner→Builder handoff 回归通过。MP-P05R2 已实际补齐 MP-I01 暴露的 shared-interface / boundary / external-service contract 缺口；前一轮 MP-P05R 的失败未复现。当前没有新的 foundational SKILL_GAP，保持 `minecraft-planner v0.5` 与 `minecraft-builder v1.11` 不变，进入 MP-I01R Builder integration regression。**

本轮最重要的结果不是“规划更详细”，而是 Builder-ready 信息终于从背景叙述变成了可解析合同：目标 BDP 明确携带 handoff readiness、边界离散语义、局部 Interface Baselines、最低净空要求、局部高程/断面基准、可调整范围、rights/access semantics、coordination owner、external service responsibility、revision 与直接依赖哈希。

同时，P05R2 没有为了让测试看起来完整而伪装成 `DESIGN_FREEZE_READY`。它正确保持 `CONCEPT_DESIGN_READY`，因为公共接口接受、跨界雨水受纳、具体基础影响体积和实际建筑功能仍需在后续阶段闭合。这是 v0.5 readiness contract 的正确使用，不是失败。

---

## 1. Provenance / Isolation Audit

### PASS

本轮 provenance 足以证明实际执行的是目标版本：

- `minecraft-planner v0.5`；
- Vibe-Coding source commit `fc6371361685e2eeaefdef5a513f21dbe64c6696`；
- Skill blob `dff88b163d18520cb5f5e5a59e7c2103883fd115`；
- shared `Minecraft Planner–Builder Contract v1.0`；
- shared contract blob `3431c7a048148cdb6c24f44604777eaa6c9b2c9e`；
- 两者在 L4 规划开始前读取并记录。

旧 `MP-P05R`、`MP-P05`、`MP-I01` 及相关 Independent Review 均未作为空间答案读取。父级只选择 MP-P04 PACKAGE-01 与直接公共协调对象 / factual evidence，未展开其它街区规划答案。

`world writes = 0`，相关世界文件与允许来源均有 unchanged / hash 证据。

---

## 2. v0.5 Target Regression

### PASS

前一轮 MP-P05R 的主要失败是：虽然声称使用 v0.5，却仍输出近似旧式的 `fixed / builder_owns / preflight` 简包，没有真正实现 v0.5 新增的 handoff contract。

P05R2 已实际输出：

- `builder_handoff_readiness`；
- `design_context`；
- `planning_causal_context`；
- explicit parcel cell envelope；
- `boundary_semantic`；
- `PLANNER_FIXED`；
- `BUILDER_ADAPTABLE`；
- `interface_baselines`；
- `external_service_interfaces`；
- `dependencies` + revision + SHA256；
- known uncertainties / `resolve_before`；
- upstream issue protocol。

因此本轮不是文档标题从 v0.4 改到 v0.5，而是 v0.5 的 interface model 真正进入了 artifact。

---

## 3. Previous MP-I01 Gap Closure

### PASS

MP-I01 当时无法冻结公共接口，原因包括：公共路线只有 ID / nominal width，缺局部线位、高程/断面、minimum clear、adjustment envelope、interface revision、coordination owner；同时 parcel 斜边也没有 Minecraft voxel 边界语义。

P05R2 对应修复如下：

### Public route / shared-space interface

局部 interface records 已包含：

- local geometry / protected cells；
- current surface / section baseline；
- planning design surface adjustment range；
- nominal width；
- minimum horizontal clear；
- minimum vertical clear；
- flow/service semantic；
- rights/access semantic；
- coordination owner；
- interface revision；
- `resolve_before`；
- uncertainty。

例如公共路 nominal width 与 minimum clear 已明确分开，且明确说明最终真实净宽仍需 Builder / runtime 验证，避免再次把规划 mask 当成实机道路认证。

### Minecraft boundary semantic

两户均明确使用：

`CELL_CENTER_MASK`

并发布显式合法 cells、tie rule、edge tolerance、vertical-boundary limitation 与 adjustment strip。Builder 不再需要自行猜“连续斜边到底按中心点、整方块还是容差落格”。

### External service ownership

洁净水、污物、小批货物/燃料、雨水均被对象化，明确：

- interface ref；
- Builder responsibility；
- public / upstream responsibility；
- local requirement；
- allowed local adjustment；
- `resolve_before`；
- uncertainty。

尤其雨水被正确保留为 `BEFORE_DESIGN_FREEZE` 的跨界 HOLD，而没有因为建筑需要排水就凭空发明公共沟渠或排入公共路。

结论：MP-I01 暴露的“handoff information missing”已从**缺信息**转为**信息明确但某些责任 / 批准仍待闭合**。两者必须区分。

---

## 4. Planner / Builder Authorship Boundary

### PASS

Planner 固定的仍是关系：

- 每包一户、两户总量不增；
- 低肩修理 / 上沿复核的角色关系；
- 公共通路和共同院不能被私人占用；
- 家庭小院与门前缓冲要保留；
- 地下现状不得擅改；
- 越界服务必须由公共责任方闭合。

Builder 仍拥有：

- exact footprint；
- Plan / Section / Sequence；
- rooms / floor count；
- structure / foundation；
- roof / facade / openings；
- palette；
- local steps / retaining / drainage realization。

因此 v0.5 并没有因为“接口更具体”而越界成为建筑设计 Skill。

---

## 5. Readiness Semantics

### PASS_WITH_NOTE

BDP-01 / BDP-02 均标记：

`CONCEPT_DESIGN_READY`

理由成立：当前资料已经足够 Builder 开展有界 Architecture Design，但公共协调方尚未回签局部接口 / 标高与跨界雨水责任，Builder 也尚未证明实际 Plan / Section、habitability、foundation influence volume 与 movement。

这意味着下一轮 MP-I01R **不应该预设最终结果必须是 DESIGN_READY**。

正确测试问题是：

> Builder v1.11 能否读取 BDP + direct dependencies 后，正确编译 Inherited Planning Intent，继续 Architecture Design，并把仍未闭合的项目准确保留为 interface / fidelity HOLD，而不是重新报“Planner 没给路线坐标”、回读完整上游规划或擅自解决公共系统？

如果 Builder 再次声称缺 route geometry / boundary semantic / responsibility，才说明 Builder Intake 没有真正消费新 contract。

---

## 6. Geometry / Capacity / Artifact Consistency

### PASS

Validation 记录 50 项检查、0 项不满足，包括：

- 两户总量 = 2；
- parcel 总柱数 = 269；
- 两 parcel 无重叠；
- private/public masks 不重叠；
- 各户 yard / apron / architectural-search 分配完整互斥；
- public union 连通；
- frontage 与 public space 接触；
- 6 个 interface baseline 满足 minimum contract；
- BDP readiness 显式；
- embedded interface refs 可解析；
- direct dependency SHA256 匹配；
- external service refs 可解析；
- relevant world/source files unchanged；
- maps 存在。

这些检查只证明 artifact consistency，不替代规划质量或 Minecraft runtime verification；归档本身也正确保留了这一边界。

---

## 7. Human-geography / L4 Planning Continuity

### PASS

v0.5 没有为了测试 handoff contract 而丢掉 v0.4 的规划核心：

- 两户角色仍来自首卸→修理 / 复核→东向轻载的流动关系；
- 权利仍是 proposal，不因画出 mask 自动成为产权；
- public/common/private boundary 继续影响形态；
- supply / water / waste / rhythm 没有被建筑名词替代；
- Planner-only 深部 evidence 没有反写成历史行动者先验知识；
- 裸岩与浅层无空气没有被夸大为肥力、矿权或 foundation safety；
- 普通 slope adaptation 保留给 Builder，未统一大平台。

因此本轮 handoff 加强没有破坏已通过的 Human Geography Kernels。

---

## 8. Finding A — Handoff artifact is heavy

**Class:** `TASK_SPECIFIC_ARTIFACT_EFFICIENCY`  
**Severity:** non-blocking

`builder-design-packages.json` 约 250 KB，包含显式 cell masks，并存在部分 interface/service 信息嵌入。它的可审计性很好，但对未来大量建筑包而言可能产生 context / token / duplication 成本。

目前不建议修改 Skill：先完成 MP-I01R，确认 Builder v1.11 实际消费方式。若 Builder 只能通过整文件读取而导致邻包信息泄漏 / context flooding，再将 package storage 优化为“每个 BDP 独立文件 + manifest/direct refs”。

不要在当前集成验证尚未完成时提前优化格式。

---

## 9. Finding B — Concept readiness is not full closure

**Class:** `EXPECTED_UNRESOLVED_DEPENDENCY`  
**Severity:** non-blocking for MP-P05R2

`U-PUBLIC / U-HABITABILITY / U-GROUND` 在 `BEFORE_DESIGN_FREEZE` 前仍需闭合；`U-TITLE`、`U-SUPPLY`、`U-OPERATION` 则有更晚的 resolve-before 阶段。

这是 contract 成熟度的体现，而不是“Planner 又没做完”。

下一轮不要通过 Prompt 帮 Builder 解释这些状态，让 v1.11 自己消费。

---

## 10. Skill Decision

> **保持 `minecraft-planner v0.5` 不变。**
>
> **保持 `minecraft-builder v1.11` 不变。**
>
> **共享 `Minecraft Planner–Builder Contract v1.0` 不变。**

当前没有足够证据要求再改 Skill。

---

## 11. Next Step

进入：

`MP-I01R — minecraft-builder v1.11 Planner Context Intake / Planning Fidelity regression`

使用一个全新的 Codex context。

输入只给：

- MP-P05R2 `BDP-01`；
- BDP-01 声明的 direct dependencies / immutable local refs；
- 当前 minecraft-builder v1.11；
- 当前批准 CIV-001 Canon / Architecture Grammar；
- 必要 Site evidence。

禁止：

- MP-P05R2 `URBAN-ENSEMBLE.md`；
- MP-P05R2 Independent Review；
- BDP-02；
- MP-P04 / P05 / P05R / I01 完整规划或旧建筑答案。

本轮只做 Architecture Design，不 world-write。

独立审核时重点判断：

1. Builder 是否自动执行 Planner Context Intake；
2. 是否真正消费 interface baselines / boundary semantic / service responsibility；
3. 是否保持 Planner WHY / rights / flow / fixed relations；
4. 是否保持自身建筑作者权；
5. 是否把明确的 unresolved dependency 与 `INCOMPLETE_HANDOFF` 区分；
6. 是否在 Planning Fidelity Gate 中正确保持或关闭 HOLD；
7. 是否不回读完整上游“补课”。

P05R2 到此可视为 v0.5 handoff regression 成功样本。