---
title: 通用资产库｜Shared Foundation 架构规划
version: 0.7
status: current-planning
created: 2026-08-17
updated: 2026-08-18
skill: tavern-asset v0.9
asset_spec_binding: pending-g9
creator_binding: pending-g9
supersedes:
  - 通用资产库_Shared_Foundation架构规划_v0.6
---

# 通用资产库｜Shared Foundation 架构规划 v0.7

> Existing Expansion Context Retrofit（Wave 1–4）与 Generic Library Context Convergence 已 **PASS / CLOSED**。因此解除 Kinship 暂停：**当前 NEXT = EP-KINSHIP-CORE｜亲缘与谱系核心。**

## 1. 已完成 P0-A

- EP-ORG-CORE v0.1.2｜Organization / Membership / Role / Rank / Internal Authority｜PASS
- EP-REPUTATION-CORE v0.1｜Target × Audience Public Social Evaluation｜PASS

二者与 Character / Relationship / Health / Combat 等 Core 的 Context Composition 已收敛。

## 2. 当前 NEXT｜EP-KINSHIP-CORE

唯一责任：Biological / Adoptive / Genealogical Kinship、Lineage、Branch、Generation、Disputed Genealogy，以及继承资格所需的谱系事实/证据边界。

必须区分：

```text
Kinship != Relationship
Kinship != Organization Membership
Kinship != Reputation
Kinship != Political Recognition
Kinship != Legal Judgment
```

新 Core 从出生即内建 Runtime Context Contract Pattern v0.5。

重点预审：
- 大谱系图 != 全量 Prompt；
- 当前人物 / 当前继承问题只读取 bounded genealogy slice；
- disputed genealogy / knowledge / public belief 与 authoritative kinship truth 分层；
- downstream Politics / Law / Reputation 通过 Handoff，不提前加载。

## 3. P0-B

```text
EP-KINSHIP-CORE
↓
EP-POLITICS-CORE + Han migration
↓
EP-ECONOMY-CORE + Han migration
↓
EP-WAR-CORE + Han migration
```

Politics Hard：ORG。Economy / War relations 在各自 Domain Audit 冻结，不预造依赖。Governance / Law 继续 DEFERRED P1。

## 4. Context baseline

从 Kinship 起默认 born-compliant：Model-first immediate routing；No-load；bounded graph/registry projection；owner-preserving cross-owner join；outcome/event-gated downstream activation；`Bounded != Starved`；durable referent / game-local materialization boundary。

Pattern v0.5；Index v0.4。

## 5. Han Migration

对应 Generic Core audited-current 前不批量迁移 Han World Pack / Character Card。

Politics：Organization skeleton → ORG；public authority / recognition / control / claim → Politics。  
Economy：Treasury / bulk / population / market / production → Economy。  
War：Formation / campaign / occupation / operational command → War。

## 6. G9 Boundary

资产 Shared Foundation 可继续 Semantic Design；Game 当前 G8-UAT-02 ACTIVE，G9 machine schema 未授权。Kinship 不冻结 final JSON fields / Router API / compiler / token budget。
