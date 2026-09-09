---
title: Context Retrofit Wave 1｜单资产审计与执行台账
status: current-audit-ledger
version: 1.0
date: 2026-08-18
scope:
  - EP-CHAR-CORE
  - EP-RELATIONSHIP-ROMANCE-CORE
  - EP-HEALTH-CORE
  - EP-COMBAT-CORE
  - EP-ORG-CORE
pattern: 通用资产库_RuntimeContextContract模式_v0.2
---

# Context Retrofit Wave 1｜单资产审计与执行台账

> [!summary]
> Wave 1 先执行 Asset Audit，再决定是否修改正式 Expansion 正文。
>
> 结论：Character / Relationship / Health / Combat 的 Domain Semantics 已经满足 Canonical Owner / Open Attempt / Program Authority / Handoff 的基础要求，缺口主要是横切 Runtime Context Binding，因此采用 **WORKSPACE / METADATA ONLY Sidecar Retrofit**；ORG 的正文已嵌入早期 Contract，但缺 Pattern v0.2 的 State-mandatory / Downstream 明确项，因此做 v0.1.2 Patch。

---

# 1. 审计分类

| Asset | Current | Audit Result | Execution | Domain Semantics Change? |
|---|---:|---|---|---|
| EP-CHAR-CORE | 0.1.5 | WORKSPACE / METADATA ONLY | Sidecar v0.1 | No |
| EP-RELATIONSHIP-ROMANCE-CORE | 0.2 | WORKSPACE / METADATA ONLY | Sidecar v0.1 | No |
| EP-HEALTH-CORE | 0.1 | WORKSPACE / METADATA ONLY | Sidecar v0.1 | No |
| EP-COMBAT-CORE | 0.1 | WORKSPACE / METADATA ONLY | Sidecar v0.1 | No |
| EP-ORG-CORE | 0.1.1 | PATCH REQUIRED | Asset v0.1.2 | No Owner change |

Reputation v0.1 作为 born-compliant reference，不属于本轮 Retrofit target。

---

# 2. EP-CHAR-CORE

现有正文已经明确：

- Character Capability 是统一长期能力 Owner；
- 其他 Expansion 只消费 / 贡献 Skill Definition，不建立第二套 Capability State；
- Runtime 决定 Formal Outcome；
- 未掌握技能也不构成 Attempt 白名单；
- NPC 能力知识与真实 Capability 分离。

缺口：没有把“Character 很常用”与“Character Core 永久 Prompt”明确分离。

执行：Sidecar 明确 Capability Provider 模式、Minimal Read、普通对话 No-load、downstream provider request。

结果：**PASS after sidecar**。

---

# 3. EP-RELATIONSHIP-ROMANCE-CORE

现有正文已经明确：

- Directed State / Shared Bond / Trust / Respect / Attraction 等由 Relationship Core 唯一拥有；
- External Event → Relationship Interpretation / Memory；
- 玩家 Attempt 与 NPC response 分离；
- RNG / Program Judge / Atomic Commit 不归本 Core；
- private relationship truth 与 public / political facts 分离。

缺口：缺少 pair-local Minimal Read 和“角色同场 ≠ Relationship 全图加载”的 Context Contract。

执行：Sidecar。

结果：**PASS after sidecar**。

---

# 4. EP-HEALTH-CORE

现有正文已经明确：

- Persistent Bodily State / Condition / HP / Consciousness / Recovery Owner；
- Combat / Magic / Divine 只提供 Health-relevant Cause / Effect；
- Runtime 负责数值、RNG、Formal Outcome、Atomic Commit；
- 模型不得临场决定 HP；
- player-safe diagnosis boundary 已存在。

缺口：需要明确 Combat Action 解析阶段通常不加载 Health，Physical Impact 后再 downstream activation；已有伤势仅提供 bounded Functional Projection。

执行：Sidecar。

结果：**PASS after sidecar**。

---

# 5. EP-COMBAT-CORE

现有正文已经明确：

- Combat Semantic Owner != Program Authority；
- Character Core 是 Hard Provider，但 Combat 不拥有第二套 Capability；
- Health 通过 Physical Impact Handoff；
- Runtime 负责 RNG / Dice / Program Judge / Formal Outcome / Atomic Commit；
- Combat Context / Range / LOS / Pressure 等是局部 projection，不重建世界位置。

缺口：缺少 Active Combat 的 state-mandatory Activation，以及 Hard Dependency 不等于全文 Context Inclusion 的显式约束。

执行：Sidecar。

结果：**PASS after sidecar**。

---

# 6. EP-ORG-CORE

v0.1.1 已有 embedded Context Contract，但它诞生早于 Pattern v0.1 最终冻结，缺：

- 独立 State-mandatory Activation；
- 独立 Downstream Activation；
- Contract 内明确 Information Boundary。

执行：v0.1.2 Patch，仅补 Context Contract 完整性；Canonical Owner 不变。

结果：**PASS after patch**。

---

# 7. 额外发现｜Metadata Drift

Character / Relationship / Health / Combat 正文 Frontmatter 仍存在旧 `skill` / `blueprint` 引用。

本轮不把该问题混入 Context Retrofit，因为：

- 不影响 Canonical Domain Semantics；
- 不是本轮 Context Contract blocker；
- Generic Metadata / Identity Normalization 已有独立维护任务。

登记：**separate maintenance debt / do not silently combine**。

---

# 8. G8 / G9 Stage Gate

Freshness Preflight 确认当前：

- G8 ACTIVE；
- Final Host Convergence 仍为 required critical path；
- G9 machine asset protocol 仍 blocked by G8 Exit；
- Semantic Asset Retrofit 可以继续，因为它不冻结 Schema / API / Compiler，也不反向发明 Host Capability。

---

# 9. Wave 1 单资产结论

```text
Character sidecar PASS
Relationship sidecar PASS
Health sidecar PASS
Combat sidecar PASS
ORG v0.1.2 PASS
↓
进入 Wave 1 Context Cluster Audit
```
