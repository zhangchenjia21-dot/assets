---
title: 通用资产库｜Runtime Context Contract 索引
version: 0.3
status: current-maintenance-index
created: 2026-08-18
updated: 2026-08-18
pattern: 通用资产库_RuntimeContextContract模式_v0.4
---

# 通用资产库｜Runtime Context Contract 索引 v0.3

> [!summary]
> 本索引只回答：**某个 current Expansion 的唯一 Context Contract 在哪里。**
>
> 它不拥有 Domain Semantics，不复制资产正文，不是 G9 machine manifest。

| Asset | Asset Version | Contract Location | Contract Version | Status |
|---|---:|---|---:|---|
| EP-CHAR-CORE | 0.1.5 | `ContextContracts/EP-CHAR-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-RELATIONSHIP-ROMANCE-CORE | 0.2 | `ContextContracts/EP-RELATIONSHIP-ROMANCE-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-HEALTH-CORE | 0.1 | `ContextContracts/EP-HEALTH-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-COMBAT-CORE | 0.1 | `ContextContracts/EP-COMBAT-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-ORG-CORE | 0.1.2 | embedded in `组织与任职核心_Expansion_Pack_v0.1.2.md` | embedded | PASS |
| EP-REPUTATION-CORE | 0.1 | embedded in `名望与社会评价核心_Expansion_Pack_v0.1.md` | embedded | PASS |
| EP-SURVIVAL | 0.2 | `ContextContracts/EP-SURVIVAL_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-TRAVELER-SYSTEM | 0.2 | `ContextContracts/EP-TRAVELER-SYSTEM_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-MAGIC-CORE | 0.3 | `ContextContracts/EP-MAGIC-CORE_RuntimeContextContract_v0.1.md` | 0.1 | Wave 3 / PASS / sidecar |
| EP-DIVINE-CORE | 0.2.1 | `ContextContracts/EP-DIVINE-CORE_RuntimeContextContract_v0.1.md` | 0.1 | Wave 3 / PASS / sidecar |
| EP-MAGIC-COMBAT | 0.3 | pending Wave 4 | — | NEXT |

---

# 1. 唯一性规则

同一个 `asset_id + asset_version`：

> 只能存在一个 current Context Contract source。

若正文内建，则不再创建 active Sidecar；若 Sidecar 是 current，则正文中的旧临时 Context Notes 不能与其形成第二套冲突规则。

---

# 2. Sidecar 权威边界

Sidecar 只拥有 Runtime Context Binding Metadata：

- Routing；
- Activation；
- No-load［
- Minimal Read［
- Model-needed［
- Program-owned；
- Handoff Context；
- Information Boundary［
- Context Cost。

Domain Owner / gameplay truth 仍只由正式 Expansion 正文拥有。

---

# 3. 更新规则

资产 Version 变化后必须重新检查对应 Context Contract：

- 语义完全兼容 → Sidecar 可 rebind / patch；
- Owner / dependency / handoff 改变 → 重新 Context Audit；
- 新正文已经 born-compliant → Sidecar 退役并在本索引改为 embedded。


---

# 4. Wave 2 新增索引原则

带 Feature / Module 的资产，索引仍只指向**一个 Package-level canonical Context Contract source**；Feature / Module routing profile 是该 Contract 内部声明，不为每个 Module 再创建独立事实源。

Background deterministic progression 仍属于对应资产 + Runtime 的执行语义，不创建“后台模型 Contract”第二来源。


---

# 5. Wave 3 新增索引原则

大型 Definition Registry 仍只登记一个 Package / Core-level Context Contract source；Spell / Invocation 等 Definition 不各自创建 Context Contract。

```text
Domain Active != Full Definition Registry Visible
```

Definition retrieval / selection 属于未来 Runtime Binding 行为，当前索引只声明语义要求。

`Bounded != Starved`：Index 不以“有 Sidecar”代替内容充分性审核；若 Sidecar 的 Minimal Read 过薄，同样不得标 PASS。
