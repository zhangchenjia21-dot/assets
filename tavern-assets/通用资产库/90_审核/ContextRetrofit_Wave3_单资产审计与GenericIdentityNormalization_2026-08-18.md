---
title: Context Retrofit Wave 3｜单资产审计与 Generic Identity Normalization
status: pass
version: 1.0
date: 2026-08-18
assets:
  - EP-MAGIC-CORE v0.3
  - EP-DIVINE-CORE v0.2.1
pattern: 通用资产库_RuntimeContextContract模式_v0.4
---

# Context Retrofit Wave 3｜单资产审计与 Generic Identity Normalization

> [!success] Final Result
> **PASS。**
>
> `EP-MAGIC-CORE v0.3` 与 `EP-DIVINE-CORE v0.2.1` 的 Canonical Domain Semantics 不需要重写；本轮分类均为：
>
> **WORKSPACE / METADATA ONLY + Runtime Context Sidecar。**
>
> 两份业务正文版本保持不变。

---

# 1. Freshness / Stage Boundary

Wave 3 启动前重新核验项目 current：

- `sillytavern@3ad5b419...` 已完成 Controlled Multi-action；
- Engineering Exit Gate = PASS；
- Stage UAT 发现 Narrative Responsiveness **P1 BLOCKER**；
- G8 = ACTIVE；
- G9 = NOT AUTHORIZED。

因此本轮只产生 Semantic Context / Identity requirements，不冻结 machine schema。

最新 UAT 同时给出：

```text
Bounded != Starved
```

该结论直接传播到本轮 Context Audit。

---

# 2. EP-MAGIC-CORE v0.3

## 2.1 Canonical Semantics

PASS：

- Spell Magic Canonical Owner 清晰；
- Hard Character / Optional Combat / Health Handoff 边界合理；
- Program Judge / Formal Outcome / Commit 不属于资产；
- Spell Definition 与玩家 Attempt 分离；
- Theme Expansion 采用 Contribution，不复制施法系统；
- 基础 Spell Library = 36 个 Canonical Definition；
- Magic Strain != Health Condition；
- Combat Range / Reaction 等由 Combat Core owns。

## 2.2 Context Gap

缺口不是业务机制，而是：

- Routing Profile；
- immediate / state-mandatory / downstream activation；
- No-load；
- bounded selected-Spell projection；
- background Magic Strain / duration progression；
- large Spell Registry 不能全量进入 Prompt。

结论：**Sidecar v0.1**。

## 2.3 Generic Identity

正文已经明确：

- Cross-world reusable；
- 不假定埃瑟维亚 / 五神 / 大断裂等世界事实；
- “诸界余辉”章节只是首发 reference consumer；
- `reference_world_consumers` 已明确标为 reference。

因此“去除首发世界作为资产身份”在语义层已经 PASS。

遗留 `blueprint v0.1 / skill v0.5.2` 属于创作时 provenance / legacy backlink，不是当前 Generic Identity。当前治理 binding 由 Generic Library current Blueprint / Matrix / Maintenance 决定；不为这类历史元数据单独重写 7 万字正文。

Identity Result：**PASS / normalized by current workspace binding**。

---

# 3. EP-DIVINE-CORE v0.2.1

## 3.1 Canonical Semantics

PASS：

- Divine Covenant / Authority / Invocation / Channel Strain / Anchor / Audience / Miracle Owner 清晰；
- Divine Actor 被保护为自主 Actor，不是资源池；
- Church Office != Covenant != Authorization；
- Invocation 与 Spell Grammar 分离；
- Spell↔Divine Interaction Profile 显式；
- Open Attempt 保留；
- Miracle / Covenant / Authorization 正式变化仍需 Runtime Commit；
- Invocation Library = 84 个 Definition；
- 埃瑟维亚五神只作为 reference example。

## 3.2 Context Gap

需要补：

- Divine routing / activation；
- Covenant / Authority scoped Minimal Read；
- 84 Invocation Registry bounded projection；
- Divine Audience 的 purpose-built rich context；
- Channel Strain / duration 的 background Program progression；
- hidden Divine Actor truth / player-safe boundary；
- durable manifestation 的 Runtime referent Gate。

结论：**Sidecar v0.1**。

## 3.3 Generic Identity

正文已明确：

- 不硬编码埃瑟维亚五神；
- 世界实际神明、教义、教会、神域归 World Pack；
- 埃瑟维亚死亡 Sovereign 示例属于 world-specific example；
- reference consumer 不构成依赖。

因此 Generic Identity 在语义上已经成立。

Identity Result：**PASS / normalized by current workspace binding**。

---

# 4. Metadata Provenance vs Current Binding

本轮正式区分：

```text
authoring-time provenance
!= current governance binding
```

成熟资产正文中的历史：

- `skill: tavern-asset v0.5.2`；
- `blueprint: ...v0.1`；

表示当时的创作 /审核来源，不应被误读为当前仍只能受旧 Skill /旧 Blueprint 管理。

当前 binding 由：

- current Generic Library Blueprint；
- current Matrix；
- current Maintenance；
- current Context Index；
- current `tavern-asset`；

共同决定。

只有当旧元数据会改变实际资产语义 /消费路径时才要求正文 Patch；纯 provenance 不制造无意义版本 churn。

---

# 5. New Runtime Context Findings

Wave 3 + G8 UAT 共同冻结：

```text
Domain Activated
!= Full Definition Registry Visible
```

```text
Bounded
!= Starved
```

大型 Spell / Invocation Registry 必须留在 Runtime Definition / Registry 层，由当前角色 access / authorization 与当前 Intent 逐级检索到少量 selected Definition projection。

---

# 6. Version Decision

| Asset | Existing | Body Change | Context Change | Identity | Result |
|---|---:|---|---|---|---|
| EP-MAGIC-CORE | 0.3 | none | Sidecar v0.1 | PASS | keep 0.3 |
| EP-DIVINE-CORE | 0.2.1 | none | Sidecar v0.1 | PASS | keep 0.2.1 |

禁止为了“Wave 3 看起来都升版”机械修改正文。

---

# 7. Next

进入 Wave 3 Cluster Audit。

若 Cluster PASS：

```text
Wave 3 CLOSED
→ Wave 4 EP-MAGIC-COMBAT
→ Generic Library Context Convergence
```
