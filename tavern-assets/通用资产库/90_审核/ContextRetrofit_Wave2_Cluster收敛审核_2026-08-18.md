---
title: Context Retrofit Wave 2｜Cluster 收敛审核
status: pass
version: 1.0
date: 2026-08-18
cluster:
  - EP-SURVIVAL
  - EP-TRAVELER-SYSTEM
  - EP-HEALTH-CORE
  - EP-CHAR-CORE
  - World OS / Runtime
pattern: 通用资产库_RuntimeContextContract模式_v0.3
---

# Context Retrofit Wave 2｜Cluster 收敛审核

> [!success] Final Result
> **PASS / CLOSED**。
>
> Wave 2 证明：长期状态可以由 Program 后台推进而不持续调用模型；多 Feature / Module Package 可以只把当前启用层级暴露给 Router，并只在当前 Turn 加载相关 Module + bounded Provider projection。

---

# 1. Scenario A｜正常一天的自动生存

条件：Survival Enabled；角色有食物、水、安全住宿；玩家无 Override。

World Time 推进。

期望：

```text
Program
→ Need progression
→ Routine consumption
→ state persist
```

模型不调用。

结果：**PASS**。

---

# 2. Scenario B｜玩家强行熬夜赶路

玩家：“今晚不睡，继续赶路。”

Immediate：Survival。

模型理解 Override / strategy；Program 持久化 Override 并推进 Sleep Deficit。

达到身体阈值后：

```text
Survival
→ Health handoff
→ Health Condition
```

不要求第一轮 Router 同时加载完整 Health。

结果：**PASS**。

---

# 3. Scenario C｜普通 Combat 中存在轻微 Hunger

Hunger 仍在后台累计，但当前直接战斗与 Hunger 无关键 Functional Effect。

Immediate：Combat；Survival no-load。

结果：**PASS**。

---

# 4. Scenario D｜Traveler/System Package Included，但双 Feature OFF

期望：

- 不创建 Traveler Identity；
- 不创建 System State；
- Router Directory 不出现 Traveler / System Feature / Modules；
- 不显示 System Surface；
- 模型不能“偶尔发任务”。

结果：**PASS / fail-closed**。

---

# 5. Scenario E｜System ON，只启用 Appraisal + Shop

Router Directory：只包含 System framework + Appraisal + Shop routing profiles。

不包含 Healing / Lottery / Relationship / Teleport 等关闭 Module。

Conditional Dependency 只为当前已启用 / 当前调用的 Module建立。

结果：**PASS**。

---

# 6. Scenario F｜使用 Healing Module

```text
System Healing invocation
↓
Health bounded provider / mutation interface
↓
Health formal state
```

System 不加载完整 Health Core，也不自己写 HP / Condition。

结果：**PASS**。

---

# 7. Scenario G｜Lottery

System Lottery 被调用。

模型可以理解“抽一次”的 Intent，但随机结果由 Program RNG 产生；Reward 通过正式 Grant / Item / Resource Owner 提交。

结果：**PASS**。

---

# 8. Scenario H｜System Quest

Quest Offer 由 System 提供来源、条件、Reward Contract。

玩家接受后：World OS Task / Objective Owner 保存正式任务。

System 不形成第二 Task State。

结果：**PASS**。

---

# 9. Transitive Context Explosion

错误模式：

```text
Traveler/System package enabled
→ load Character + Health + Relationship + Survival + Magic + Divine + Combat
```

当前模式：

```text
active Feature / Module routing profile only
↓
current module selected
↓
bounded provider projection only if needed
```

结果：**PASS**。

---

# 10. Background Cost Explosion

错误模式：

```text
每个 World Time tick
→ model checks hunger / thirst / sleep / exposure
```

当前模式：Program deterministic progression；只有语义决策 / warning /开放式策略需要模型。

长期 Session 成本不会因日常生存 tick 线性扩大模型调用次数。

结果：**PASS**。

---

# 11. Future Explosion Review

假设：

- Survival actors ×10；
- System Modules ×10；
- Quest / Shop / Storage history ×10。

普通无关 Turn 仍由 background program + pruned routing directory + bounded projection 维持。

当前未发现新的 P0 / P1 Context Explosion。

---

# 12. Exit / Next

Wave 2：**CLOSED / PASS**。

Next：

```text
Wave 3
EP-MAGIC-CORE
→ EP-DIVINE-CORE
→ Generic Identity Normalization（可合并）
→ Wave 3 Cluster Audit
```

Kinship 继续暂停，直到 Existing Expansion Retrofit 全部收敛。