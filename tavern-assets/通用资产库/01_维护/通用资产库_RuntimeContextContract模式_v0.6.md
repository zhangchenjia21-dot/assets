---
title: 通用资产库｜Runtime Context Contract 模式
aliases:
  - Context Contract Pattern
  - Runtime Activation Pattern
version: 0.6
status: current-maintenance-pattern
created: 2026-08-18
updated: 2026-08-19
scope:
  - generic-asset-library
  - runtime-context
  - g9-upstream
reference_assets:
  - EP-REPUTATION-CORE v0.1
  - EP-ORG-CORE v0.1.2
  - EP-MAGIC-CORE v0.3
  - EP-DIVINE-CORE v0.2.1
  - EP-MAGIC-COMBAT v0.3
  - EP-KINSHIP-CORE v0.1
  - EP-POLITICS-CORE v0.1
skill: tavern-asset v1.0
asset_spec_binding: pending-g9-03
supersedes:
  - 通用资产库_RuntimeContextContract模式_v0.5
---

# 通用资产库｜Runtime Context Contract 模式 v0.6

> [!abstract]
> 本文件冻结 Semantic Asset 阶段的 Runtime Context Contract 写法，不是最终 JSON Schema / Runtime API / token budget。
>
> v0.6 完整继承 v0.5 的 Model-first Routing、Feature / Module pruning、Background Program Progression、Definition Registry Projection、`Bounded != Starved`、Narrative authoritative referent、Bounded Cross-Owner Projection Join 与 Outcome-Gated Continuation Activation。
>
> 本版新增经 **Kinship + Politics 两个独立大型关系图领域**验证的规则：
>
> **Large Relation Graph / Deterministic Subgraph Projection｜大型关系图 / 确定性相关子图投影。**

---

# 1. Runtime Context 基础集合

```text
Asset Library
!= Game Enabled Asset Set
!= Current Runtime Relevant Set
!= Current Model Visible Working Set
```

```text
Full Semantic Asset != Model Prompt Payload
Dependency Graph != Context Inclusion Graph
Hard Dependency != Transitive Prompt Inclusion
Whole Relation Graph != Model Prompt
```

对 Feature / Module：

```text
Installed
!= Package Included
!= Feature Enabled
!= Module Enabled
!= Runtime Relevant
!= Model Visible
```

目标不是最少 token，而是：**在信息边界内，用最小充分、高信号、当前职责相关的 Working Set 完成模型任务。**

---

# 2. Context Contract 标准 19 项

每个新 Core / 重要 Expansion 至少回答：

1. Routing Profile；
2. Immediate Activation；
3. State-mandatory Activation；
4. Downstream Activation；
5. No-load Conditions；
6. Minimal Read Set；
7. Model-needed Semantics；
8. Program-owned Logic；
9. Output Candidate；
10. Handoff / Information Boundary；
11. Context Cost / Bounded Strategy；
12. Feature / Module Activation Hierarchy（如适用）；
13. Background Program Progression（如适用）；
14. Definition Registry / Library Projection（如适用）；
15. Bounded Sufficiency / Anti-Starvation；
16. Narrative Affordance / Runtime Referent（如适用）；
17. Cross-Owner Projection Join（多 Provider / Theme / Composite 时）；
18. Outcome-Gated Continuation Activation（多阶段 / Coupling / Reaction 时）；
19. **Large Relation Graph / Deterministic Subgraph Projection（长期、多节点、多边关系图时）。**

## 2.1 Routing Profile

给第一轮 Model-first Router 的极小目录描述：ID / Name / One-line Scope / 少量 Typical Semantics。不能复制完整规则，也不能成为关键词白名单。

## 2.2 Immediate Activation

只回答当前 Input 现在需要哪些 Domain / Feature / Module 参与，不预测全部未来后果。

## 2.3 State-mandatory Activation

若 authoritative active state 使某 Domain 必须参与，Program 可以补入 Current Relevant Set；但 `Runtime Relevant != Model Visible`。

## 2.4 Downstream Activation

```text
Formal Event / State Change
→ Typed Handoff
→ downstream activation
```

Router 不一次预测全部后果。

## 2.5 No-load Conditions

明确常见“不应该因为 Enabled 就加载”的场景。No-load 是正式设计，不是性能备注。

## 2.6 Minimal Read Set

只读当前实体 / 当前关系 / 当前局部状态 / selected Definition / 少量必要历史摘要。禁止默认整表、全历史、全世界。

## 2.7 Model-needed Semantics

模型只承担自然语言意图、开放式角色 / 社会语义、结构化 Candidate、player-safe realization 等真正需要 LLM 的工作。

## 2.8 Program-owned Logic

ID / Ref、authoritative state、deterministic rules、permission、graph traversal / filtering、RNG / Dice、Program Judge、Formal Outcome、Atomic Commit、Save / Restore / Recovery 优先 Program。

## 2.9 Output Candidate

模型输出 Candidate / Intent / Interpretation / Clarification Need，不直接成为 Formal State Mutation。

## 2.10 Handoff / Information Boundary

同时回答 Incoming / Outgoing；Handoff 是 Ownership Boundary，也是 Context Complexity Boundary。后台 private truth 不得因跨域协作泄漏。

## 2.11 Context Cost

至少证明状态、资产、Registry 或 Relation Graph 规模扩大 5–10 倍时，普通无关 Turn 仍基本稳定。

## 2.12 Feature / Module Activation Hierarchy

关闭的 Feature / Module 不进入 Router Directory，不产生 Conditional Dependency，不产生 module state / surface。

## 2.13 Background Program Progression

```text
Background deterministic progression
!= Model Activation
```

Need accumulation、timer、cooldown、固定资源消耗、routine automation、确定性 lifecycle 等由 Program 处理。

## 2.14 Definition Registry / Library Projection

```text
Domain Active
!= Full Definition Registry Visible
```

推荐：

```text
Enabled Registry
→ actor-accessible / authorized subset
→ intent-relevant retrieval
→ selected Definition Projection
→ Model
```

## 2.15 Bounded Sufficiency / Anti-Starvation

```text
Bounded != Starved
```

Minimal = minimum sufficient。不得删除决定当前语义正确性的 actor identity、goal、selected Definition、target/ref、current outcome、relevant relationship / source / history 等。

## 2.16 Narrative Affordance / Runtime Referent

若 Narrative / UI 把具体对象呈现为可持续、可寻址、可后续交互：

```text
authoritative Game-local / Runtime referent
→ player-safe projection
→ Narrative / Product presentation
```

Generic placeholder 不满足 durable referent gate。

## 2.17 Cross-Owner Projection Join

多 Provider 场景：

```text
current purpose
→ current-needed projection from each relevant Owner
→ preserve owner / provenance
→ owner-preserving bounded join
→ current model / resolution step
```

禁止递归展开全部上游正文、全状态与 transitive dependencies。

## 2.18 Outcome-Gated Continuation Activation

```text
Potential continuation
!= Current Relevant downstream context
```

只有 authoritative upstream Outcome / Trigger 成立后，才加载 continuation 需要的 Owner / Definition projection。

## 2.19 Large Relation Graph / Deterministic Subgraph Projection

长期关系图若会随世界规模持续增长，必须回答：

1. **哪些关系本身是 Canonical primary relations / source facts？**
2. **哪些 pairwise / aggregate 结论可以确定重算，因此应保持 Projection？**
3. **Program 如何根据当前问题选择 relevant path / subgraph？**
4. **如何先执行 enabled / scope / owner / player-safe filtering？**
5. **模型真正需要看到哪一小段语义切片？**
6. **图规模扩大 5–10 倍时，ordinary unrelated Turn 是否基本不增长？**

标准链：

```text
Large Relation Graph
→ persist canonical primary relations / minimal authoritative edges
→ avoid materializing all derivable pairwise relations
→ Program deterministic current-relevant path / subgraph selection
→ owner-safe + player-safe bounded projection
→ Model only for open semantic work
```

正式冻结：

```text
Whole Relation Graph != Model Prompt
Derived Pairwise Projection != Canonical Truth
World Graph Growth != Ordinary Turn Context Growth
```

### Kinship Reference

- canonical：parentage / adoption / family affiliation 等；
- derived：sibling / cousin / common ancestor / generation distance；
- Program 先选必要谱系路径。

### Politics Reference

- canonical：Authority / Claim / Recognition / Control / Issue / Agreement / Delegation 等；
- derived：综合合法性 / 综合势力 / pairwise loyalty 等摘要不成为第二事实源；
- Program 先选当前地点 / 政权 /议题 / 权力相关政治子图。

> 注意：本规则不是“所有关系都只准存最原始边”。如果某关系本身就是长期 Canonical Truth，例如 Membership、Recognition、Agreement、Shared Bond，就应持久化。禁止的是大规模镜像**可确定重算的派生关系**。

---

# 3. Canonical Context Contract Location

新资产默认正文内建 Context Contract。

成熟 audited-current 旧资产若 Domain Semantics 不变、只缺横切 Routing / Activation / Projection，可用唯一 Sidecar：

- precise bind `asset_id + asset_version`；
- `canonical_domain_ownership: none`；
- 不复制正文；
- 不新增玩法；
- 不改变 Outcome / Owner；
- 同一资产版本只有一个 current Contract source。

冲突优先级：

```text
Canonical Asset Domain Semantics
>
Context Sidecar Binding Metadata
```

---

# 4. Model-first Routing 标准链

```text
Player Input
+ Enabled / Feature-Module-pruned Routing Profiles
+ minimal current scene / active context
↓
Router Model
↓
immediate candidates
↓
Program structural validation
+ state-mandatory augmentation
↓
JIT bounded runtime projections / relevant subgraphs
↓
Semantic / Program resolution / Narrative
```

Router miss 不是玩家行为白名单。

---

# 5. Audit Questions

至少检查：

1. Routing Profile 是否短且可区分邻近 Domain？
2. Immediate 是否没有预测全部后果？
3. State-mandatory 是否来自 authoritative state？
4. 是否把 Dependency 错当 Prompt Inclusion？
5. No-load 是否真实？
6. Minimal Read 是否退化成全量状态？
7. deterministic logic 是否仍 Prompt-owned？
8. Handoff 是否导致 transitive context explosion？
9. Information Boundary 是否正确？
10. 资产 /历史增长时普通 Turn 是否稳定？
11. Router miss 是否破坏 Open Attempt？
12. Contract canonical location 是否唯一？
13. Sidecar 是否偷加 Domain Semantics？
14. disabled Module 是否泄漏进 Router / dependency？
15. background progression 是否高频调模型？
16. Domain active 是否全量展开 Registry？
17. Minimal Read 是否 starved？
18. durable/interactable affordance 是否有 authoritative referent？
19. 多 Provider 是否错误做成 transitive full-context expansion？
20. downstream continuation 是否在 upstream Outcome 前提前加载？
21. 大型 Relation Graph 是否把整图塞入 Prompt？
22. 是否把可确定重算的 pairwise / aggregate projection 镜像成第二 Canonical State？
23. Program 是否能先选择 current-relevant subgraph / path？
24. private / player-safe filter 是否发生在 Model Projection 前？

---

# 6. Evidence

- Reputation：born-compliant Context Reference；
- ORG：embedded Retrofit；
- Wave 1 Character / Relationship / Health / Combat：Sidecar Retrofit；
- Wave 2 Survival / Traveler-System：Background progression + Feature/Module pruning；
- Wave 3 Magic / Divine：Large Registry Projection + Bounded != Starved；
- G8-UAT-02：semantic materialization / concrete Game-local referent；
- Wave 4 Combat Magic：multi-provider bounded join + Outcome-gated continuation；
- **Kinship v0.1：Large Genealogy Graph / deterministic path projection；**
- **Politics v0.1：Large Political Graph / deterministic relevant-subgraph projection。**

当前 Existing Reusable Expansion 共 13 个，全部具有唯一 Context Contract source；Politics current 同样 born-compliant。

---

# 7. Host / G9 Boundary

当前项目：G9 ACTIVE；G9-02A PASS；G9-02BC PASS；G9-02B ACTIVE；G9-03 NOT AUTHORIZED。

G9-02BC 已证明 Built-in Domain Host、JIT Projection 与 bounded owner-preserving join；本 v0.6 作为 G9-02C / G9-03 上游语义要求，不冻结 final Schema fields、Router API、Context Compiler、Relation Query DSL、token budget 或 Provider-specific prompt layout。
