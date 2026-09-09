---
title: Context Retrofit Wave 3｜Magic / Divine Cluster 收敛审核
status: pass
version: 1.0
date: 2026-08-18
cluster:
  - EP-MAGIC-CORE
  - EP-DIVINE-CORE
  - EP-CHAR-CORE
  - EP-COMBAT-CORE
  - EP-HEALTH-CORE
pattern: 通用资产库_RuntimeContextContract模式_v0.4
---

# Context Retrofit Wave 3｜Magic / Divine Cluster 收敛审核

> [!success] Final Result
> **PASS。**
>
> Wave 3 验证大型 supernatural Definition Registry 可以保持 Runtime-rich / Prompt-bounded；Magic / Divine 同时 Enabled 不等于 Spell / Invocation Library 全量常驻上下文。

---

# 1. Ownership

| Concern | Owner | Result |
|---|---|---|
| Character Capability | EP-CHAR-CORE | PASS |
| Spell Magic | EP-MAGIC-CORE | PASS |
| Divine Covenant / Invocation | EP-DIVINE-CORE | PASS |
| Direct Combat shell | EP-COMBAT-CORE | PASS |
| Bodily State | EP-HEALTH-CORE | PASS |
| RNG / Judge / Outcome / Commit | Runtime | PASS |
| Definition Registry storage / retrieval | Runtime binding | semantic requirement ready |

Magic 与 Divine 保持并列 Core；“超自然”不是新的万能 Owner。

---

# 2. Scenario A｜普通无关 Turn

Enabled：

```text
Character + Health + Combat + Magic + Divine
```

玩家在客栈与朋友闲聊，不谈超自然。

期望：

- Magic no-load；
- Divine no-load；
- 36 Spell + 84 Invocation = **0 条进入 Context**。

Result：**PASS。**

---

# 3. Scenario B｜单 Spell 施法

玩家：“我施展护盾挡住飞来的碎片。”

Router：Magic immediate。

Working Set：

- current caster；
- relevant capability / Spell Mastery；
- current Magic Strain；
- selected Shield Spell Definition；
- relevant target / scene facts。

不加载：

- 其余 35 个基础 Spell；
- 全部 Theme Spell；
- Divine；
- 完整 Character Profile。

Result：**PASS。**

---

# 4. Scenario C｜Spell in Combat

玩家在 Active Combat 中施法攻击。

```text
Combat state-mandatory
+
Magic selected Spell projection
→ Program composite resolution
→ Physical / bodily Effect
→ Health downstream activation
```

Combat 提供 Range / LOS / Reaction / Pressure；Magic 提供 Spell internal semantics；Health 只在真实 bodily effect 后接管。

没有：

```text
Combat full + Magic full + Character full + Health full
```

Result：**PASS。**

---

# 5. Scenario D｜Magic Background Progression

当前存在 maintained Spell，玩家随后进行无关社交。

Runtime 可以：

- 更新 duration；
- 处理 deterministic expiry；
- 恢复 Magic Strain；
- 处理已确定持续 effect bookkeeping。

除非产生新的开放式选择 / interaction / warning：

> **zero additional model call。**

Result：**PASS。**

---

# 6. Scenario E｜普通 Divine Invocation

玩家调用已授权治疗类 Invocation。

Working Set：

- current Covenant；
- relevant Authority Scope；
- selected Invocation Definition；
- Invocation Mastery；
- Channel Strain；
- target；
- relevant Anchor。

其余 83 Invocation 不进入模型。

正式身体后果通过 Handoff → Health。

Result：**PASS。**

---

# 7. Scenario F｜Divine Audience

玩家请求与其神性契约对象谈判扩大授权。

这是 Wave 3 最关键的 **Bounded Rich Context** 场景。

必须有界，但不能只给：

```text
godRef
+
covenantState
```

至少需要：

- 当前职责相关 Divine Actor profile；
- current Covenant / Authority；
- request；
- relevant obligations / prior covenant events；
- world sovereign boundary；
- 当前参与者 / scene。

模型产生自主 Divine Actor response Candidate；Runtime 决定并 Commit 正式 Covenant / Authorization / Miracle 变化。

Result：**PASS WITH BOUNDED SUFFICIENCY RULE**。

---

# 8. Scenario G｜Spell ↔ Divine Interaction

当 Spell 作用于 divine effect：

- Magic 读取 explicit Interaction Profile；
- Divine 读取 relevant Authority / Sovereign boundary；
- 两边只交换 bounded interaction facts；
- 不加载完整 Magic / Divine Library。

Result：**PASS。**

---

# 9. Definition Registry Scale Test

当前：

- Magic Core：36 个基础 Spell；
- Divine Core：84 个 Invocation。

假设未来：

```text
Spell Definitions ×10
Invocation Definitions ×10
```

普通 Turn：Context ≈ unchanged。

单 Spell / Invocation Turn：只增加 selected-definition retrieval cost，不随全库线性增长。

冻结：

```text
Domain Active != Full Registry Visible
```

Result：**PASS。**

---

# 10. Bounded != Starved

G8 Stage UAT 已证明“Context 过薄”会造成模型泛化和响应性差。

Wave 3 因此不把“最少 token”作为优化目标。

正确目标：

> **minimum sufficient high-signal context**

Magic：selected Spell 必须保留当前任务必需的 effect / variability / requirement / interaction semantics。

Divine Audience：必须保留足够 Divine Actor / Covenant / request / relevant history。

Result：**PASS。**

---

# 11. Narrative Affordance

若 Divine / Magic Effect 产生具体、持续、可交互的召唤物 / 化身 / messenger / entity：

```text
player-visible durable interactable
→ authoritative Runtime referent first
→ narrative presentation
```

纯瞬时光影 / 声音 /动作可以是 Ephemeral Narrative Realization。

Result：**PASS AS G9 / HOST REQUIREMENT**。

---

# 12. Generic Identity Normalization

Magic / Divine 的正文语义已 generic；诸界余辉只作 reference consumer。

本轮 current Workspace 统一记录：

```text
Canonical Identity = Generic Library Asset
Reference Consumer = 诸界余辉
Current Blueprint Binding = current Generic Library Blueprint
```

历史正文 `blueprint v0.1 / skill v0.5.2` 保留为 authoring provenance，不继续充当 current binding。

Result：**PASS。**

---

# 13. Future Explosion Review

检查：

- Full registry prompt explosion → prevented；
- transitive Character / Combat / Health full loading → prevented；
- Magic × Divine pairwise rule duplication → explicit bounded interaction；
- background strain/duration model-call explosion → prevented；
- Divine Actor context starvation → new sufficiency rule；
- world-specific identity leakage → reference-only。

当前没有发现需要暂停路线的 P0/P1 Asset Architecture blocker。

---

# 14. Exit

```text
Wave 3 Magic / Divine + Identity Normalization
✓ PASS / CLOSED

NEXT
Wave 4 EP-MAGIC-COMBAT
→ Generic Library Context Convergence
```
