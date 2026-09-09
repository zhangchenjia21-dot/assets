---
title: 通用资产库｜Shared Foundation 架构规划
version: 0.9
status: current-planning
created: 2026-08-17
updated: 2026-08-19
skill: tavern-asset v1.0
asset_spec_binding: pending-g9-03
creator_binding: pending-g9-03
supersedes:
  - 通用资产库_Shared_Foundation架构规划_v0.8
---

# 通用资产库｜Shared Foundation 架构规划 v0.9

> `EP-POLITICS-CORE｜政治与公共权力核心 v0.1` 已 **PASS / AUDITED CURRENT**；汉末三国 Politics Migration Plan 已 **COMPLETE / NOT YET EXECUTED**。当前 Shared Foundation 下一安全动作：**执行汉末《政争与势力》真实消费者迁移**。

## 1. 已完成基础

```text
EP-ORG-CORE v0.1.2          PASS
EP-REPUTATION-CORE v0.1     PASS
EP-KINSHIP-CORE v0.1        PASS
EP-POLITICS-CORE v0.1       PASS
```

Politics 已通过：

- 单资产 Audit；
- `Politics × ORG × Kinship × Reputation × Relationship` Cluster；
- Large Political Graph Future Explosion Review；
- Han Migration Plan；
- Kinship + Politics Architecture Reflection。

## 2. Politics 冻结边界

```text
Regime / Political Order != Government Organization
Role Holding != Public Authority
Internal Authority != Public Authority
Claim != Recognition != Political Control != Military Occupation != Jurisdiction
Public Reputation != Political Recognition
Kinship != Succession Outcome
Political Agreement != Commitment Promise Lifecycle
```

Politics Hard Depend `EP-ORG-CORE`；Kinship / Reputation / Relationship / Character / Health 为 optional integrations。

不建立 universal loyalty / legitimacy / stability / control score。

## 3. Large Relation Graph｜正式提升

Kinship + Politics 已证明：

```text
Large Relation Graph
→ canonical primary relations / source facts
→ Program deterministic current-relevant path / subgraph
→ owner-safe + player-safe bounded projection
→ Model only for open semantic work
```

因此：

- Runtime Context Pattern → v0.6；
- Context Contract → 19 项；
- `tavern-asset` → v1.0。

## 4. 当前 NEXT｜Han Politics migration execution

迁移规划 current：

`资产族/汉末三国_天下未定/20_迁移/汉末三国_Politics_Core迁移规划_v0.1_2026-08-19.md`

执行时至少：

```text
Political Faction
→ ORG organization / Politics regime-or-issue split

Political Affiliation
→ ORG formal affiliation + Politics issue-specific stance

Office Definition / Holding
→ ORG

Public Authority / Jurisdiction
→ Politics

Succession
→ Kinship + ORG + Politics (+ future Law)
```

Politics migration 完成并 real-consumer convergence PASS 后，再进入 Economy Core。

## 5. P0-B 路线

```text
EP-KINSHIP-CORE                           ✓ PASS
EP-POLITICS-CORE                          ✓ PASS
Han Politics migration planning           ✓ COMPLETE
↓
Han Politics migration execution          CURRENT
↓
EP-ECONOMY-CORE + Han migration
↓
EP-WAR-CORE + Han migration
↓
Shared Foundation Convergence
```

Governance / Law 继续 deferred；在 Politics / Economy / War 完成后重新评估。

## 6. Context baseline

后续新 Core 默认 born-compliant Pattern v0.6：

- Model-first routing；
- No-load；
- bounded registry projection；
- large relation graph relevant-subgraph projection；
- owner-preserving cross-owner join；
- outcome-gated downstream activation；
- `Bounded != Starved`；
- durable referent / game-local materialization boundary。

## 7. G9 Boundary

项目当前：G9 ACTIVE；G9-02A PASS / CLOSED；G9-02BC PASS / CLOSED；G9-02B ACTIVE；G9-03 NOT AUTHORIZED。

Shared Foundation 资产可以对齐已证明的 Source → Game-local、Built-in Domain Host、typed handoff、JIT Projection、bounded owner-preserving join，但仍不冻结 final asset-spec fields、Router API、relation query DSL、Compiler 或 Creator machine UI。
