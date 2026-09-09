---
title: 通用资产库｜Runtime Context Contract 模式
aliases:
  - Context Contract Pattern
  - Runtime Activation Pattern
version: 0.5
status: current-maintenance-pattern
created: 2026-08-18
updated: 2026-08-18
scope:
  - generic-asset-library
  - runtime-context
  - retrofit
  - g9-upstream
reference_assets:
  - EP-REPUTATION-CORE v0.1
  - EP-ORG-CORE v0.1.2
  - EP-MAGIC-CORE v0.3
  - EP-DIVINE-CORE v0.2.1
  - EP-MAGIC-COMBAT v0.3
skill: tavern-asset v0.9
asset_spec_binding: pending-g9
supersedes:
  - 通用资产库_RuntimeContextContract模式_v0.4
---

# 通用资产库｜Runtime Context Contract 模式 v0.5

> [!abstract]
> 本文件冻结 G9 前 Semantic Asset 阶段的 Runtime Context Contract 写法，不是最终 JSON Schema / Runtime API / token budget。
>
> v0.5 完整保留此前的 Model-first Routing、Feature/Module pruning、Background Program Progression、Definition Registry Projection、`Bounded != Starved` 与 Narrative authoritative referent，并新增两条由 Combat Magic / 全库收敛验证的规则：
>
> 1. **Bounded Cross-Owner Projection Join**；
> 2. **Outcome-Gated Continuation Activation**。
>
> 最新 G8-UAT-02 进一步确认：generic placeholder / label 不能替代 concrete Game-local canonical referent。

---

# 1. Runtime Context 基础集合

```text
Asset Library
!= Game Enabled Asset Set
!= Current Runtime Relevant Set
!= Current Model Visible Working Set
```

进一步：

```text
Full Semantic Asset != Model Prompt Payload
Dependency Graph != Context Inclusion Graph
Hard Dependency != Transitive Prompt Inclusion
```

对内部 Feature / Module：

```text
Installed
!= Package Included
!= Feature Enabled
!= Module Enabled
!= Runtime Relevant
!= Model Visible
```

目标不是最少 token，而是：**在信息边界内，用最小充分高信号 Working Set 完成当前模型职责。**

---

# 2. Context Contract 标准 18 项

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
18. Outcome-Gated Continuation Activation（多阶段 / Coupling / Reaction 时）。

## 2.1 Routing Profile

给第一轮 Model-first Router 的极小目录描述：ID / Name / One-line Scope / 少量 Typical Semantics。不能复制完整规则，也不能成为关键词白名单。

## 2.2 Immediate Activation

只回答当前 Input 现在需要哪些 Domain / Feature / Module 参与语义理解与当前处理，不预测全部未来后果。

## 2.3 State-mandatory Activation

若 authoritative active state 使某 Domain 必须参与，Program 可以补入 Current Relevant Set；但 `Runtime Relevant != Model Visible`。

## 2.4 Downstream Activation

```text
Formal Event / State Change
→ Typed Handoff
→ downstream activation
```

Router 不负责一次预测全部后果。

## 2.5 No-load Conditions

明确常见“不应该因为 Enabled 就加载”的场景。No-load 是正式设计，不是性能备注。

## 2.6 Minimal Read Set

只读当前实体 / 当前关系 / 当前局部状态 / selected Definition /少量必要历史摘要。禁止默认整表、全历史、全世界。

## 2.7 Model-needed Semantics

模型只承担自然语言意图、开放式角色/社会语义、结构化 Candidate、player-safe realization 等真正需要 LLM 的工作。

## 2.8 Program-owned Logic

ID/Ref、authoritative state、deterministic rules、permission、RNG/Dice、Program Judge、Formal Outcome、Atomic Commit、Save/Restore/Recovery 优先 Program。

## 2.9 Output Candidate

模型输出 Candidate / Intent / Interpretation / Clarification Need，不直接成为 Formal State Mutation。

## 2.10 Handoff / Information Boundary

同时回答 Incoming / Outgoing；Handoff 是 Ownership Boundary，也是 Context Complexity Boundary。后台 private truth 不得因跨域协作泄漏。

## 2.11 Context Cost

至少证明状态或资产规模扩大 5–10 倍时，普通无关 Turn 仍基本稳定。

## 2.12 Feature / Module Activation Hierarchy

关闭的 Feature / Module 不进入 Router Directory，不产生 Conditional Dependency，不产生 module state / surface。

## 2.13 Background Program Progression

```text
Background deterministic progression
!= Model Activation
```

Need accumulation、timer、cooldown、固定资源消耗、routine automation 等可确定推进由 Program 处理。

## 2.14 Definition Registry / Library Projection

```text
Domain Active
!= Full Definition Registry Visible
```

推荐链：

```text
Enabled Registry
→ actor-accessible / authorized subset
→ intent-relevant retrieval
→ selected Definition Projection
→ Model
```

第一轮 Router 不为了识别 Domain 展开完整 Spell / Invocation / Technique / Recipe / Item Registry。

## 2.15 Bounded Sufficiency / Anti-Starvation

```text
Bounded != Starved
```

Minimal = minimum sufficient。不能为省 token 删除决定当前语义正确性的 actor identity、goal、selected Definition effect/requirement、target/ref、current outcome、relevant history 等。

## 2.16 Narrative Affordance / Runtime Referent

若 Narrative / UI 把一个具体对象呈现为可持续、可寻址、可后续交互：

```text
authoritative Game-local / Runtime referent
→ player-safe projection
→ Narrative / Product presentation
```

纯瞬时氛围可以 Narrative-only。Generic placeholder 不满足 durable referent gate。

## 2.17 Cross-Owner Projection Join

当 Theme / Composite 依赖多个 Canonical Provider：

```text
current purpose
→ request current-needed projection from each relevant Owner
→ preserve owner/provenance
→ owner-preserving bounded join
→ current model / resolution step
```

禁止递归展开所有上游正文、全状态与 transitive dependencies。Consumer 不建立 mirror state，也不因为 join 获得 Provider Ownership。

## 2.18 Outcome-Gated Continuation Activation

多阶段、Reaction、Counter、Cross-Action Coupling：

```text
Potential continuation
!= Current Relevant downstream context
```

只有 authoritative upstream Outcome / Trigger 成立后，才加载 continuation 需要的 Owner / Definition projection。

例：Combat Magic `断法斩` miss 时不加载 Countermagic continuation；只有 `effective_contact` 后继续。

---

# 3. Canonical Context Contract Location

新资产默认正文内建 Context Contract。

成熟 audited-current 旧资产若 Canonical Owner / Domain Semantics / Dependency-Handoff / Open Attempt / Program Authority 均不变，只缺横切 Routing / Activation / Projection，可用唯一 Sidecar：

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
JIT bounded runtime projections
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
19. 多 Provider Theme 是否错误做成 transitive full-context expansion？
20. downstream continuation 是否在 upstream Outcome 成立前提前加载？

---

# 6. Evidence

- Reputation：born-compliant Context Contract Reference；
- ORG：embedded Retrofit；
- Wave 1 Character / Relationship / Health / Combat：Sidecar Retrofit；
- Wave 2 Survival / Traveler-System：Background progression + Feature/Module pruning；
- Wave 3 Magic / Divine：Large Registry Projection + Bounded != Starved；
- G8-UAT-01：Narrative authority + durable referent；
- G8-UAT-02：semantic materialization / concrete Game-local referent；
- Wave 4 Combat Magic：multi-provider bounded join + Outcome-gated continuation。

全部 11 个 Existing Reusable Expansion 已完成 Context Audit；Generic Library Context Convergence PASS / CLOSED。

---

# 7. Host / G9 Boundary

当前 Game：G8-UAT-01 PASS/CLOSED；Stage UAT 新增 G8-UAT-02 Semantic Materialization + Living World blocker；G9 NOT AUTHORIZED。

本 Pattern 作为未来 G9-02 handwritten runtime profile / requirements corpus 输入，但不冻结 final Schema fields、Router API、Context Compiler、Retrieval Algorithm、token budget、模型调用次数或 Provider-specific prompt layout。
