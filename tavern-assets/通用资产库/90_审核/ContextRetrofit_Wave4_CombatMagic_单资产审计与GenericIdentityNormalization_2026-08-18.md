---
title: Context Retrofit Wave 4｜Combat Magic 单资产审计与 Generic Identity Normalization
status: pass
version: 1.0
date: 2026-08-18
asset: EP-MAGIC-COMBAT v0.3
pattern: 通用资产库_RuntimeContextContract模式_v0.5
---

# Context Retrofit Wave 4｜Combat Magic 单资产审计与 Generic Identity Normalization

> [!success] Final Result
> **PASS / WORKSPACE-METADATA ONLY。**
>
> `EP-MAGIC-COMBAT v0.3` 的 Canonical Domain Semantics、Hard Dependency、Combat/Magic Ownership、Open Attempt、Information Boundary 与 Program Authority 均无需重写；缺口是 Runtime Context Binding 与 current Generic Library identity binding。
>
> 正式处理：新增唯一 Context Sidecar v0.1；业务正文保持 v0.3。

---

# 1. Canonical Ownership

| Concern | Owner | Result |
|---|---|---|
| Character long-term capability | EP-CHAR-CORE | PASS |
| Spell Grammar / Mastery / Strain / Countermagic Core | EP-MAGIC-CORE | PASS |
| Martial Outcome / Range / Reaction / combat timing | EP-COMBAT-CORE | PASS |
| Combat Spell Definitions / Style / Spell-specific Coupling | EP-MAGIC-COMBAT | PASS |
| Bodily consequence | EP-HEALTH-CORE | PASS / optional handoff |
| RNG / Judge / Formal Outcome / Commit | Runtime | PASS |

Combat Magic 没有复制 Combat Core 命中规则，也没有创建第二套 Countermagic。

---

# 2. Dependency Audit

Hard：

```text
Character + Magic + Combat
→ EP-MAGIC-COMBAT enablement prerequisite
```

但正式冻结：

```text
Hard Dependency
!= transitive Prompt inclusion
```

Combat Magic 当前动作只消费三个 Provider 的 bounded projections。

Optional Divine / Health 只在真实 target / consequence 需要时加入，不转成包级常驻 Context。

Result：**PASS。**

---

# 3. Open Attempt / Authority

资产正文明确允许：打掉法杖、扑倒施法者、遮挡视线、普通弓箭攻击等非 Spell Attempt；Style 不是职业白名单。

程序继续拥有：

- Martial Outcome；
- Reaction Window；
- Countermagic Resolution；
- RNG / Dice；
- Formal Composite Outcome；
- State Commit。

Result：**PASS。**

---

# 4. Definition / Instance / Materialization

52 个 Combat Spell 是 Definitions；抑术场、猎印、武器短时强化等持续对象进入 Game-local / Runtime Effect Instance，不回写 Source Asset。

最新 G8-UAT-02 的 Semantic Materialization 规则与本资产一致：

```text
semantic definition / proposal
→ Program validation + stable identity
→ game-local canonical / effect instance
→ Runtime state
→ player-safe projection / Narrative
```

Generic placeholder 不足以满足 durable referent。

Result：**PASS。**

---

# 5. Context Audit

### Scenario A｜普通武器战斗

Enabled：Character + Magic + Combat + Combat Magic。

玩家只挥剑。

期望：Combat immediate；Combat Magic no-load；52 Spell = 0 条进入 Model Context。

**PASS。**

### Scenario B｜普通 Magic Spell

玩家施展一个非 Combat-Magic 来源 Spell。

期望：Magic active；Combat Magic 不因 Magic+Combat 都 Enabled 而自动参与。

**PASS。**

### Scenario C｜震荡斩

Working Set：selected CBT Definition + actor relevant capability + current Combat projection + current Magic state。

禁止：Character/Magic/Combat 全文 join。

**PASS。**

### Scenario D｜断法斩 miss

```text
Intent
→ Combat resolves no effective_contact
→ no Countermagic continuation
```

不加载 downstream Countermagic resolution corpus。

**PASS。**

### Scenario E｜断法斩 effective_contact

Formal upstream Outcome 成立后，才加入 Coupling + bounded Magic Countermagic projection。

**PASS。**

### Scenario F｜敌法者对神术

只有真实 Divine interaction target 存在时读取 bounded Divine Interaction Profile；不加载 Divine 全库。

**PASS。**

---

# 6. Generic Identity Normalization

正文已满足跨世界 Generic：

- 不硬编码埃瑟维亚 Canonical Mechanism；
- World Pack 只负责教学、制度、地方称呼与禁令；
- 诸界余辉只是 reference consumer；
- `asset_family` 已指向 Generic Library。

旧 `skill / blueprint` 字段属于 authoring provenance，不足以构成重写 62KB 正文的理由。

Current binding 由当前 Generic Library + Context Index + Tavern Skill 提供。

Result：**PASS / no body version churn。**

---

# 7. New Pattern Evidence

本资产稳定证明两条新的横切规则：

## Bounded Cross-Owner Projection Join

```text
Composite/Theme active
→ bounded provider projections
→ owner-preserving join
```

而不是：

```text
Theme active
→ expand all hard dependencies recursively
```

## Outcome-Gated Continuation Activation

```text
Potential continuation
!= active downstream context

formal upstream Outcome / Trigger
→ downstream continuation becomes relevant
```

这两条适合升级进入 Generic Library Pattern 与 `tavern-asset`。

---

# 8. Final Classification

```text
Canonical body patch          NO
Asset version bump            NO
Context Sidecar               YES
Generic Identity workspace    NORMALIZED
Pattern upgrade               YES
Skill upgrade                 YES
Final                         PASS
```
