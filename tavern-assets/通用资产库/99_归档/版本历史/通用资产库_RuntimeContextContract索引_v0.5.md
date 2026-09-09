---
title: 通用资产库｜Runtime Context Contract 索引
version: 0.5
status: current-maintenance-index
created: 2026-08-18
updated: 2026-08-19
pattern: 通用资产库_RuntimeContextContract模式_v0.5
supersedes:
  - 通用资产库_RuntimeContextContract索引_v0.4
---

# 通用资产库｜Runtime Context Contract 索引 v0.5

> 本索引只回答某个 current Expansion 的唯一 Context Contract 在哪里；不拥有 Domain Semantics，不是 G9-03 machine manifest。

| Asset | Asset Version | Contract Location | Contract Version | Status |
|---|---:|---|---:|---|
| EP-CHAR-CORE | 0.1.5 | `ContextContracts/EP-CHAR-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-RELATIONSHIP-ROMANCE-CORE | 0.2 | `ContextContracts/EP-RELATIONSHIP-ROMANCE-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-HEALTH-CORE | 0.1 | `ContextContracts/EP-HEALTH-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-COMBAT-CORE | 0.1 | `ContextContracts/EP-COMBAT-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-ORG-CORE | 0.1.2 | embedded in asset | embedded | PASS |
| EP-REPUTATION-CORE | 0.1 | embedded in asset | embedded | PASS / reference |
| EP-KINSHIP-CORE | 0.1 | embedded in asset | embedded | PASS / born-compliant |
| EP-SURVIVAL | 0.2 | `ContextContracts/EP-SURVIVAL_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-TRAVELER-SYSTEM | 0.2 | `ContextContracts/EP-TRAVELER-SYSTEM_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-MAGIC-CORE | 0.3 | `ContextContracts/EP-MAGIC-CORE_RuntimeContextContract_v0.1.md` | 0.1 | Wave 3 / PASS |
| EP-DIVINE-CORE | 0.2.1 | `ContextContracts/EP-DIVINE-CORE_RuntimeContextContract_v0.1.md` | 0.1 | Wave 3 / PASS |
| EP-MAGIC-COMBAT | 0.3 | `ContextContracts/EP-MAGIC-COMBAT_RuntimeContextContract_v0.1.md` | 0.1 | Wave 4 / PASS |

## 1. 当前覆盖

```text
Existing Reusable Expansions = 12
Unique Context Contract Sources = 12
Coverage = 12 / 12 PASS
```

## 2. Kinship

Kinship v0.1 从第一版即正文内建 Pattern v0.5 全 18 项，不创建 Sidecar。

其大型图上下文采用：

```text
whole genealogy graph
→ deterministic relevant subgraph/path
→ player-safe bounded slice
→ model when needed
```

## 3. 唯一性

同一 `asset_id + asset_version` 只能有一个 current Context Contract source。Sidecar 只拥有 Runtime Context Binding；born-compliant 新 Core 默认正文内建。

## 4. 更新

资产 Version 变化后重新审核；Owner / dependency / handoff / graph semantics 改变则重做 Context Audit。

G9 当前 02BC ACTIVE，但 G9-03 未授权，本索引仍不充当 machine manifest。
