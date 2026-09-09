---
title: Kinship × Relationship × ORG × Reputation｜Cluster 收敛审核
status: pass
date: 2026-08-19
scope:
  - EP-KINSHIP-CORE v0.1
  - EP-RELATIONSHIP-ROMANCE-CORE v0.2
  - EP-ORG-CORE v0.1.2
  - EP-REPUTATION-CORE v0.1
---

# Kinship × Relationship × ORG × Reputation｜Cluster 收敛审核

> [!success] Final Result
> **PASS / CLOSED。** 家族与亲缘核心与现有 Relationship / ORG / Reputation 没有形成重复事实源；未来 Politics / Law 接口保持清晰且未被提前实现。

## 1. Marriage / Kinship

冻结：

```text
婚姻作为两人之间的人际关系事实
→ Relationship

婚姻带来的姻亲结构
→ Kinship 按需推导 / 消费
```

Kinship 不保存第二份婚姻状态。

结果：**PASS。**

## 2. Family Bond / Kinship Truth

Relationship 可以表达“亲情、疏远、依恋、家庭共同关系意义”；Kinship 只表达亲缘结构。

```text
家人身份
!= 感情好
```

养父子可以结构上成立，同时 Relationship 极度疏远；两套事实并存且不冲突。

结果：**PASS。**

## 3. Family / Organization

```text
家系 / 血缘共同体 / 家族分支
→ Kinship

成员资格 / 正式职位 / 等级 / 族长 / 内部权限 / 管理机构
→ ORG
```

Family Branch 不等于 ORG Department。家族与同名宗族组织可通过明确引用关联，但不能共用一套状态。

结果：**PASS。**

## 4. Kinship / Reputation

Kinship 提供可公开的亲缘 / 家系事实；Reputation 负责社会对人物或家族的评价。

```text
“X 是王室后裔”
!=
“社会因此尊敬 / 鄙视 X”
```

公众是否相信某个谱系说法首先属于未来 Knowledge / Information / Rumor 语义，不由 Reputation 或 Kinship 偷偷代管。

结果：**PASS。**

## 5. Truth / Claim / Public Belief

Cluster 统一：

```text
Authoritative Kinship Truth
!= Genealogy Claim
!= Public Belief
!= Character Knowledge
```

因此秘密身世不会因 Reputation / Relationship / ORG Context join 自动泄漏。

结果：**PASS。**

## 6. Adoption

正式收养结果：

- Kinship → 养亲结构；
- Relationship → 双方关系意义；
- ORG → 若家族同时是组织，可能另行发生 Membership/Role 后果；
- Reputation → 若事件公开且具有社会意义，再处理评价。

下游不在收养尚未正式成立时提前提交。

结果：**PASS。**

## 7. Severance / Disownment

“断绝关系”最多分别影响：

- Relationship bond；
- Family recognition / adoptive / recognized kinship（按世界规则）；
- 未来 Law / Politics 后果。

已成立的 biological parentage 不被删除。

结果：**PASS。**

## 8. Succession Boundary

Kinship 可以回答：

- 谁是谁的后裔；
- 相隔几代；
- 属于哪一支；
- 某谱系是否确认 /争议。

Kinship 不回答：

- 谁“应该”继承；
- 谁具法律资格；
- 谁正式取得王位 /职位；
- 哪种继承制度有效。

结果：**PASS。未来 Politics / Law Owner 未被抢占。**

## 9. Context Composition

### 普通家庭对话
Relationship 可 immediate；Kinship 若只需确定“这是母亲”可由程序提供一个 bounded fact，不加载家谱。

### 身世调查
Kinship immediate + 必要人物 /证据上下文；Relationship / Reputation 不因“可能有后果”提前加载。

### 家族政治继承
未来形成：Kinship relevant lineage slice + Politics / Law bounded projection；不展开整个家谱 /整个政治状态。

结果：**PASS。**

## 10. Future Explosion

500–2000 人家族仍采用：

```text
source kinship edges
→ deterministic graph query
→ bounded current slice
```

不建立每对成员之间的全部“堂叔 / 表侄 / 姻亲”等持久关系；Relationship / Reputation 也不镜像完整 Kinship Graph。

结果：**PASS。**

## 11. Final Decision

```text
EP-KINSHIP-CORE v0.1               AUDITED CURRENT
Relationship boundary              PASS
ORG boundary                       PASS
Reputation boundary                PASS
Politics / Law future handoff      PASS / DEFERRED OWNER IMPLEMENTATION
Cluster                            PASS / CLOSED
```

当前资产线 NEXT：**EP-POLITICS-CORE + Han migration planning**。
