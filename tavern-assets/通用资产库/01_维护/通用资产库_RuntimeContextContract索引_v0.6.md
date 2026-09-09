---
title: 通用资产库｜Runtime Context Contract 索引
version: 0.6
status: current-maintenance-index
created: 2026-08-18
updated: 2026-08-19
pattern: 通用资产库_RuntimeContextContract模式_v0.6
supersedes:
  - 通用资产库_RuntimeContextContract索引_v0.5
---

# 通用资产库｜Runtime Context Contract 索引 v0.6

> 本索引只回答某个 current Expansion 的唯一 Context Contract 在哪里；不拥有 Domain Semantics，不是 G9-03 machine manifest。

| Asset | Asset Version | Contract Location | Contract Version / Pattern | Status |
|---|---:|---|---|---|
| EP-CHAR-CORE | 0.1.5 | `ContextContracts/EP-CHAR-CORE_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-RELATIONSHIP-ROMANCE-CORE | 0.2 | `ContextContracts/EP-RELATIONSHIP-ROMANCE-CORE_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-HEALTH-CORE | 0.1 | `ContextContracts/EP-HEALTH-CORE_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-COMBAT-CORE | 0.1 | `ContextContracts/EP-COMBAT-CORE_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-ORG-CORE | 0.1.2 | embedded in asset | embedded | PASS |
| EP-REPUTATION-CORE | 0.1 | embedded in asset | embedded | PASS / reference |
| EP-KINSHIP-CORE | 0.1 | embedded in asset | born v0.5; audited compatible with v0.6 graph rule | PASS / graph reference |
| EP-POLITICS-CORE | 0.1 | embedded in asset | born v0.5; audited against v0.6 graph rule | PASS / graph reference |
| EP-SURVIVAL | 0.2 | `ContextContracts/EP-SURVIVAL_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-TRAVELER-SYSTEM | 0.2 | `ContextContracts/EP-TRAVELER-SYSTEM_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-MAGIC-CORE | 0.3 | `ContextContracts/EP-MAGIC-CORE_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-DIVINE-CORE | 0.2.1 | `ContextContracts/EP-DIVINE-CORE_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |
| EP-MAGIC-COMBAT | 0.3 | `ContextContracts/EP-MAGIC-COMBAT_RuntimeContextContract_v0.1.md` | sidecar 0.1 | PASS |

## 1. 当前覆盖

```text
Existing Reusable Expansions = 13
Unique Context Contract Sources = 13
Coverage = 13 / 13 PASS
Current Pattern = v0.6
```

## 2. Pattern v0.6

新增：

> **Large Relation Graph / Deterministic Subgraph Projection**

证据：

- Kinship：genealogy graph；
- Politics：authority / claim / recognition / control / issue / agreement graph。

```text
Whole Relation Graph
→ Program current-relevant path / subgraph
→ owner-safe + player-safe bounded slice
→ Model only when needed
```

## 3. Kinship / Politics Binding Note

Kinship v0.1 与 Politics v0.1 的正文最初按 Pattern v0.5 born-compliant；二者自己的正文已经包含 v0.6 新增的大型图要求，并通过 cross-domain Architecture Reflection，因此当前视为 **v0.6-compatible PASS**。

不为同一 asset version 再创建 Sidecar；避免第二 Context Contract source。

## 4. 唯一性

同一 `asset_id + asset_version` 只能有一个 current Context Contract source。

Sidecar 只拥有 Runtime Context Binding；born-compliant 新 Core 默认正文内建。

## 5. 更新

资产 Version 变化后重新审核；Owner / dependency / handoff / graph semantics 改变则重做 Context Audit。

G9 当前 02BC PASS、02B ACTIVE、G9-03 未授权；本索引仍不充当 machine manifest。
