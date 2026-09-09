---
title: 通用资产库｜Shared Foundation 架构规划
version: 0.8
status: current-planning
created: 2026-08-17
updated: 2026-08-19
skill: tavern-asset v0.9
asset_spec_binding: pending-g9-03
creator_binding: pending-g9-03
supersedes:
  - 通用资产库_Shared_Foundation架构规划_v0.7
---

# 通用资产库｜Shared Foundation 架构规划 v0.8

> `EP-KINSHIP-CORE｜家族与亲缘核心 v0.1` 已 **PASS / AUDITED CURRENT**。当前 Shared Foundation NEXT 正式切换到：**EP-POLITICS-CORE｜政治与公共权力核心 + 汉末三国迁移规划。**

## 1. 已完成基础

```text
EP-ORG-CORE v0.1.2          PASS
EP-REPUTATION-CORE v0.1     PASS
EP-KINSHIP-CORE v0.1        PASS
```

Kinship 已通过：

- 单资产 Audit；
- `Kinship × Relationship × ORG × Reputation` Cluster Convergence；
- 大谱系图 bounded-context / Future Explosion Review。

## 2. Kinship 冻结边界

```text
Kinship != Relationship
Family / Lineage != Organization
Kinship != Reputation
Kinship != Political Recognition
Kinship != Legal Judgment
```

核心责任：Family / Lineage Identity、Parentage、Adoption、Recognized Kinship、Family Branch、Genealogy Claim / Evidence Boundary、bounded genealogy projection。

婚姻事实由 Relationship；姻亲结构按需推导。生物亲缘不因断亲删除。继承资格只消费 Kinship，不由 Kinship 决定。

## 3. 当前 NEXT｜Politics

Politics 应在 Kinship 已存在的前提下正式处理：

- 公共权力身份；
- 政治职位与实际控制的区别；
- 政权 /政治共同体；
- 统治权、承认、主张、合法性与控制；
- 家系 /亲缘如何成为政治主张的输入，但不能自动等于政治权力；
- ORG Role / Membership 与 Politics Authority 的边界；
- Reputation / public belief 与政治承认的边界。

Politics 的具体 Hard / Optional 关系在其 Domain Audit 中冻结，不因为 Kinship 已完成而预造依赖。

## 4. P0-B 路线

```text
EP-KINSHIP-CORE                           ✓ PASS
↓
EP-POLITICS-CORE + Han migration          NEXT
↓
EP-ECONOMY-CORE + Han migration
↓
EP-WAR-CORE + Han migration
↓
Shared Foundation Convergence
```

Governance / Law 继续 deferred；在 Politics / Economy / War 完成后重新评估。

## 5. Han Migration 原则

Politics audited-current 前不批量迁移 Han World Pack / Character Cards。

未来迁移至少区分：

```text
历史人物之间的亲缘 / 家系
→ Kinship

组织身份 / 官职骨架
→ ORG

公共权力 / 政治承认 / 统治主张 / 实际控制
→ Politics
```

不能因为汉末政治高度家族化，就把家族身份和政治权力合并为一个 Owner。

## 6. Context baseline

后续新 Core 默认 born-compliant Pattern v0.5：Model-first routing、No-load、bounded projection、跨 Owner 有界拼接、结果门控下游激活、`Bounded != Starved`、durable referent。

Kinship 新增的领域实践：大型谱系图优先由程序查询必要路径，再给模型有限结果。

## 7. G9 Boundary

项目当前：G9 ACTIVE；G9-02A PASS / CLOSED；G9-02BC Shared Runtime Foundation ACTIVE；G9-03 NOT AUTHORIZED。

Shared Foundation 资产可以对齐已经证明的 Source → Game-local → Runtime / Context 架构，但仍不冻结 final asset-spec 字段、Router API、Compiler、Creator machine UI 或任意查询 DSL。
