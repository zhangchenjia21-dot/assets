---
title: 通用资产库｜Runtime Context Contract 索引
version: 0.4
status: current-maintenance-index
created: 2026-08-18
updated: 2026-08-18
pattern: 通用资产库_RuntimeContextContract模式_v0.5
supersedes:
  - 通用资产库_RuntimeContextContract索引_v0.3
---

# 通用资产库｜Runtime Context Contract 索引 v0.4

> 本索引只回答某个 current Expansion 的唯一 Context Contract 在哪里；不拥有 Domain Semantics，不是 G9 machine manifest。

| Asset | Asset Version | Contract Location | Contract Version | Status |
|---|---:|---|---:|---|
| EP-CHAR-CORE | 0.1.5 | `ContextContracts/EP-CHAR-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-RELATIONSHIP-ROMANCE-CORE | 0.2 | `ContextContracts/EP-RELATIONSHIP-ROMANCE-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-HEALTH-CORE | 0.1 | `ContextContracts/EP-HEALTH-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-COMBAT-CORE | 0.1 | `ContextContracts/EP-COMBAT-CORE_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-ORG-CORE | 0.1.2 | embedded in asset | embedded | PASS |
| EP-REPUTATION-CORE | 0.1 | embedded in asset | embedded | PASS / reference |
| EP-SURVIVAL | 0.2 | `ContextContracts/EP-SURVIVAL_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-TRAVELER-SYSTEM | 0.2 | `ContextContracts/EP-TRAVELER-SYSTEM_RuntimeContextContract_v0.1.md` | 0.1 | PASS / sidecar |
| EP-MAGIC-CORE | 0.3 | `ContextContracts/EP-MAGIC-CORE_RuntimeContextContract_v0.1.md` | 0.1 | Wave 3 / PASS |
| EP-DIVINE-CORE | 0.2.1 | `ContextContracts/EP-DIVINE-CORE_RuntimeContextContract_v0.1.md` | 0.1 | Wave 3 / PASS |
| EP-MAGIC-COMBAT | 0.3 | `ContextContracts/EP-MAGIC-COMBAT_RuntimeContextContract_v0.1.md` | 0.1 | Wave 4 / PASS |

## 1. 唯一性

同一 `asset_id + asset_version` 只能有一个 current Context Contract source。Sidecar 只拥有 Runtime Context Binding Metadata；正文仍拥有 Domain / Gameplay Truth。

## 2. 更新

资产 Version 变化后重新审核：语义兼容可 rebind/patch；Owner / dependency / handoff 改变则重做 Context Audit；新正文 born-compliant 时 Sidecar 退役。

## 3. Registry / Module

一个 Package/Core 只登记一个 Contract source；Feature/Module profile、Spell/Invocation Definition 不各自创建 Context Contract。

## 4. Wave 4 / Library Convergence

全部 11 个 Existing Reusable Expansion 已有唯一 Contract location。

新增：

```text
Hard Dependency != Transitive Prompt Inclusion
Potential downstream capability != Current Relevant downstream context
```

Theme / Composite 的多 Provider projection join 与 Outcome-gated continuation 都由其同一 Package-level Contract 声明，不为每个 Coupling / Spell 再建 Sidecar。
