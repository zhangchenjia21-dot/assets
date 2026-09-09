---
title: 通用资产库｜Shared Foundation 架构规划
aliases:
  - 通用资产库上游核心规划
  - Generic Shared Foundation Plan
version: 0.6
status: current-planning-baseline
created: 2026-08-17
updated: 2026-08-18
scope:
  - generic-asset-library
  - shared-foundation
  - canonical-ownership
  - migration-planning
  - runtime-context
skill: tavern-asset v0.8.2
asset_spec_binding: pending-g9
creator_binding: pending-g9
supersedes:
  - 通用资产库_Shared_Foundation架构规划_v0.5
---

# 通用资产库｜Shared Foundation 架构规划 v0.6

> [!abstract] 当前裁定
> 社会结构 Shared Foundation 已完成前两项：
>
> `ORG v0.1.2 → Reputation v0.1`
>
> 二者已经通过 Ownership + Runtime Context Cluster Audit，并冻结 `Runtime Context Contract Pattern v0.4`。
>
> **现在暂停继续生产 Kinship；先对既有 Runtime Expansion 做分波次 Context Retrofit。** Retrofit 收敛后再恢复 `Kinship → Politics → Economy → War`。

---

# 1. P0-A Independent Foundation

## EP-ORG-CORE｜组织与任职核心

状态：**AUDITED CURRENT v0.1.2**。

Owner：Organization / Membership / Formal Affiliation / Role / Rank / Branch / Internal Authority / generic organization relation lifecycle。

Context：retrofit reference / PASS。

## EP-REPUTATION-CORE｜名望与社会评价核心

状态：**AUDITED CURRENT v0.1**。

Owner：Target × Audience 公共社会评价、传播、显著性、争议、时效与 Social Epithet。

Hard：无。

Optional：ORG / Relationship / Character / future Politics / Law。

Context：**born-compliant Reference Implementation / PASS**。

关键边界：

```text
Reputation != Relationship
Reputation != Knowledge
Reputation != Organization Rank
Reputation != Political Recognition
Reputation != Legal Status
Reputation != Character Capability
```

## EP-KINSHIP-CORE｜亲缘与谱系核心

状态：**PLANNED / PAUSED FOR CONTEXT RETROFIT**。

Owner：Biological / Adoptive / Genealogical Kinship、Lineage、Branch、Generation、Disputed Genealogy 与继承资格证据。

---

# 2. P0-B Large-scale Domain Core

## EP-POLITICS-CORE

状态：PLANNED GENERICIZATION。
Hard：ORG。

## EP-ECONOMY-CORE

状态：PLANNED GENERICIZATION。

## EP-WAR-CORE

状态：PLANNED GENERICIZATION。
Hard：ORG。

Governance / Law 继续 DEFERRED P1。

---

# 3. Canonical Ownership Registry｜目标态

| Domain | Canonical Owner |
|---|---|
| Character Capability | EP-CHAR-CORE |
| Bodily State | EP-HEALTH-CORE |
| Direct Combat | EP-COMBAT-CORE |
| Relationship / Romance | EP-RELATIONSHIP-ROMANCE-CORE |
| Survival | EP-SURVIVAL |
| Organization / Role / Rank / Membership | EP-ORG-CORE |
| Public Social Reputation | EP-REPUTATION-CORE |
| Kinship / Genealogy | future EP-KINSHIP-CORE |
| Public Political Authority / Recognition / Control | future EP-POLITICS-CORE |
| Economy / Bulk Resources / Population / Market | future EP-ECONOMY-CORE |
| War / Formation / Campaign / Occupation | future EP-WAR-CORE |
| Governance Execution | future Governance |
| Legal Case / Wanted / Judgment / Procedure | future Law |
| Game State / Time / Position / Item / Knowledge / Task / Commitment / Event | World OS / Runtime |
| RNG / Dice / Formal Outcome / Atomic Commit | Runtime |

---

# 4. Runtime Context Gate

冻结：

```text
Asset Library != Game Enabled != Runtime Relevant != Model Visible
Full Semantic Asset != Model Prompt Payload
Dependency Graph != Context Inclusion Graph
```

Pattern：`[[通用资产库_RuntimeContextContract模式_v0.4]]`；Contract location 见 `[[通用资产库_RuntimeContextContract索引_v0.3]]`。

Model-first Router：Player Input + Enabled Routing Profiles + minimal active context → immediate Domain / Intent candidates；Program 只做 structural validation + state-mandatory augmentation；后续由 Event / Handoff 再激活。

---

# 5. Reference Implementation / Cluster 结论

`EP-REPUTATION-CORE v0.1` 验证：

- Routing Profile 可非常短；
- immediate routing 与 downstream activation 可分离；
- Target × Audience 可形成局部 Minimal Read；
- provenance 可以摘要，不需要完整事件历史；
- Reputation truth / Character Knowledge 可隔离。

`ORG + Reputation` Cluster 验证：

- 同时 Enabled 不要求同时 Prompted；
- bounded projection 足以跨 Owner 协作；
- Handoff 可以替代 pairwise state mirroring；
- Role / Rank 与社会声望没有 duplicate owner。

该证据已与 Wave 1 / Wave 2 / Wave 3 一起收敛为 current `Context Contract Pattern v0.4`。

Wave 3 新增证明：
- `Domain Active != Full Definition Registry Visible`；
- 大型 Spell / Invocation Registry 应先裁剪到 actor-accessible / authorized / intent-relevant subset；
- `Bounded != Starved`，Context 必须最小但足够；
- durable/interactable Narrative affordance 必须存在 authoritative Runtime referent。

---

# 6. Existing Expansion Context Retrofit｜当前最高优先级

```text
Wave 1
Character → Relationship → Health → Combat → ORG recheck
✓ PASS / CLOSED

Wave 2
Survival → Traveler/System
✓ PASS / CLOSED

Wave 3
Magic → Divine + Generic Identity Normalization
✓ PASS / CLOSED

Wave 4
Combat Magic
NEXT
↓ Generic Library Context Convergence
```

Wave 1：Character / Relationship / Health / Combat 通过 Sidecar Retrofit；ORG v0.1.2 补齐 embedded Pattern。

Wave 2：Survival / Traveler-System 通过 Sidecar Retrofit；新增后台 Program progression 与 Feature / Module activation hierarchy。

Sidecar 只拥有 Context Binding Metadata，不获得 Domain Ownership。

---

# 7. Retrofit 后恢复 Shared Foundation

```text
Context Retrofit Convergence
↓
EP-KINSHIP-CORE
↓
EP-POLITICS-CORE + Han migration
↓
EP-ECONOMY-CORE + Han migration
↓
EP-WAR-CORE + Han migration
↓
Generic Library Convergence
↓
Governance / Law re-evaluation
↓
Jianghu-specific assets
```

---

# 8. 汉末三国 Migration Strategy

对应 Generic Core 未 audited-current 前，不批量迁移 Han Character Cards / World Pack。

Politics：Faction / staff / Office skeleton → ORG；Authority / Recognition / Control / Claim → Politics。

Economy：Treasury / Bulk / Population / Market / Production → generic Economy；Governance execution → future Governance。

War：Formation / Campaign / Command / Siege / Occupation → generic War；standing military organization → ORG。

History Reference / Divergence 继续 Han-specific。

---

# 9. 江湖资产族进入条件

江湖专用：Martial Arts → Jianghu Ecology → Court-Jianghu。

在 Shared Foundation 与 Context Retrofit 至少达到可组合稳定前，不批量生产 World Pack / Character Cards。

---

# 10. Periodic Architecture Audit

每形成一个高耦合 Cluster，检查：

- 规模 5–10 倍是否仍成立；
- duplicate owner / state mirroring；
- pairwise / transitive context explosion；
- over-modularization / shotgun change；
- Prompt-owned deterministic mechanics；
- 成本 /延迟是否随无关资产数量或 Session 长度增长。

必要时邀请用户做 Owner Reflection。

---

# 11. G9 Boundary

不冻结：JSON / Schema / Router API / token budget / retrieval algorithm / Creator machine fields / Bundle contract。

Freshness Gate：G8 Engineering Gate 为 historical PASS，但 Stage UAT 已 FAIL 并正式 REOPEN G8；当前 Next = G8-UAT-01，G9 NOT AUTHORIZED。Semantic Retrofit 可继续，并为 G9-02 提供 handwritten runtime profile requirements，但不能反向定义 Host。

当前冻结 Semantic Ownership、Context Contract Pattern 与生产 / Retrofit 顺序。
