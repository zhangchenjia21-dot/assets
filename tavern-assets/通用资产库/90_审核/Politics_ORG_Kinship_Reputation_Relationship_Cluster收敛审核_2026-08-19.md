# Politics × ORG × Kinship × Reputation × Relationship｜Cluster 收敛审核

状态：**PASS / CLOSED**  
日期：2026-08-19

## 1. 目标

验证 `EP-POLITICS-CORE v0.1` 加入 Shared Foundation 后，不会与 ORG、Kinship、Reputation、Relationship、Commitment 形成第二事实源；同时为未来 Economy / War / Law 保留正确交接边界。

---

## 2. Politics × ORG｜PASS

### ORG owns

- Organization identity；
- Membership / Formal Affiliation；
- Role / Rank；
- Role Holding；
- Internal Authority；
- Organization branch / department；
- 通用 Formal Inter-Organization Relation lifecycle skeleton。

### Politics owns

- Regime / Political Order；
- Public Authority / Jurisdiction；
- Claim；
- Recognition；
- Political Control；
- Political Issue / Stance；
- Political Agreement semantics；
- Delegation / Regency；
- Public Authority Transition。

核心冻结：

```text
Government Organization != Regime
Role Holding != Public Authority
Internal Authority != Public Authority
Political Faction membership != Politics-owned second membership
```

汉末旧包中的 Faction / Affiliation / Office 不再保留为 Generic Politics second owner。

---

## 3. Politics × Kinship｜PASS

Kinship 提供：

- parentage / descent；
- family / lineage；
- branch；
- disputed genealogy；
- bounded genealogy projection。

Politics 提供：

- succession Claim；
- political support / opposition；
- Recognition；
- authority transfer；
- regime continuity / transition。

冻结：

```text
Kinship fact
!= succession eligibility
!= Political Recognition
!= Public Authority
```

“最近血亲”不能自动成为统治者。

---

## 4. Politics × Reputation｜PASS

Reputation 回答：

> 某 Audience 如何社会性评价某人 /组织 /对象。

Politics Recognition 回答：

> 某政治主体正式承认哪个政治身份、权力、政权、主张或控制状态。

冻结：

```text
Public popularity / esteem
!= Political Recognition
```

允许：民众高度支持但政治机构不承认；政治主体广泛承认但社会评价很差。

不建立统一 Legitimacy Score 混合二者。

---

## 5. Politics × Relationship｜PASS

Relationship owns：

- Sentiment；
- Trust；
- Respect；
- Attachment；
- Relationship Commitment；
- Romantic Attraction；
- Marriage Bond；
- Relationship Memory。

Politics owns：

- 针对明确政治 Issue / Claim / Regime 的正式支持 /反对 /背书；
- 联姻产生的政治协议 /政治后果（若正式成立）。

冻结：

```text
Private relationship
!= Formal Political Stance
Marriage
!= Political Alliance
```

同一人物可以私人亲近但政治反对，或私人敌对但政治合作。

---

## 6. Politics × Commitment｜PASS

Politics owns Political Agreement。

Commitment owns explicit fulfillable Promise lifecycle：

```text
Political Agreement
+
“未来出兵 / 运粮 / 释放 / 支付”
↓
Commitment
```

Politics 只消费 fulfilled / broken 等正式结果，不建立 `pending political promise` 第二状态。

---

## 7. Politics × Character / Health｜PASS

Character Capability 只影响真实可改变空间中的执行质量，不能制造 Authority / Recognition / Control。

Health 只提供身体事实；失能可以产生摄政 / delegation / succession pressure，但 Politics 不复制昏迷 /疾病状态。

---

## 8. Politics × future Economy｜PASS / DEFERRED

预留边界：

```text
Politics
→ policy / authority / taxation decision / public order

Economy
→ resources / treasury / tax result / production / market / population consequence
```

Politics 不因为“有权征税”就直接创造收入。

Economy Core 尚未创建，不提前冻结具体 dependency / payload。

---

## 9. Politics × future War｜PASS / DEFERRED

预留边界：

```text
War owns Military Occupation / Formation / Campaign / Battle
Politics owns Claim / Recognition / Political Control / public war objective
```

军事占领可以形成政治接管 candidate，但不自动成为 Political Control。

War Core 尚未创建，不提前冻结具体 dependency / payload。

---

## 10. Politics × future Law｜PASS / DEFERRED

Law future owns：

- 法律条文；
- 法定程序；
- legal eligibility；
- 法律裁决 / 合法性判断。

Politics owns：

- 当前政治权力事实；
- 政治承认；
- 实际控制；
- 政治转移结果。

政治上取得权力可以与法律上是否有效产生张力；两者不得合并。

---

## 11. 大型图 Context Convergence｜PASS

Politics 是 Kinship 之后第二个大型关系图 Reference。

共同稳定模式：

```text
Canonical source facts / edges
↓
Program deterministic current-relevant subgraph / path selection
↓
player-safe bounded projection
↓
Model only for open semantic work
```

### Kinship

- parentage / adoption / family source edges；
- 计算共同祖先 / 世代 /必要亲缘路径。

### Politics

- Authority / Claim / Recognition / Control / Issue / Agreement / Delegation source facts；
- 只选择当前地点 /政权 /议题 /权力相关子图。

两个独立领域均不需要 pairwise derived-state matrix 或全图 Prompt。

---

## 12. Outcome-gated Handoff｜PASS

政治行为不预加载全部下游：

```text
Diplomatic proposal
→ agreement failed
   → no Commitment / Economy / War continuation
→ agreement established
   → explicit promises → Commitment
   → only actual resource / military obligations activate downstream
```

```text
War occupation
→ no political takeover candidate
   → Politics no-load
→ formal takeover candidate
   → Politics control / recognition processing
```

---

# 13. Final

```text
Politics × ORG             PASS
Politics × Kinship         PASS
Politics × Reputation      PASS
Politics × Relationship    PASS
Politics × Commitment      PASS
Politics × Character       PASS
Politics × Health          PASS
Politics × Economy         PASS / DEFERRED
Politics × War             PASS / DEFERRED
Politics × Law             PASS / DEFERRED
Large Graph Context        PASS
Outcome-gated handoff      PASS
```

> **Shared Foundation Politics Boundary Cluster：PASS / CLOSED。**
