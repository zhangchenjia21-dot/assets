# EP-POLITICS-CORE v0.1｜单资产审核

状态：**PASS / AUDITED CURRENT**  
日期：2026-08-19

## 1. 审核对象

`拓展包/通用拓展包/政治与公共权力核心_Expansion_Pack_v0.1.md`

审核目标：确认 Genericity、Canonical Ownership、Dependency、Open Attempt、Program Authority、Information Boundary、Runtime Context、Future Explosion 与 G9-03 边界是否可进入稳定通用语义基线。

---

## 2. Genericity Gate｜PASS

去掉“汉末 / 三国 / 皇帝 / 州郡”等世界专名后，核心语义仍成立：

- 公共权力；
- 政权 / 政治秩序；
- 权力来源与作用范围；
- 主张；
- 承认；
- 实际政治控制；
- 政治议题与正式立场；
- 政治协议；
- 授权 / 代行；
- 政权生命周期与公共权力结构变更。

可覆盖君主制、共和国、城邦、部落联盟、神权、革命政府、自治政权与奇幻政治秩序。

结论：**cross-world generic成立。**

---

## 3. Canonical Ownership｜PASS

Politics 唯一拥有：

- Regime / Political Order；
- Public Authority / Jurisdiction；
- Claim；
- Recognition；
- Political Control；
- Political Issue / Formal Political Stance；
- Political Agreement；
- Delegation / Regency；
- Political Authority Transition。

明确不拥有：

- Organization / Membership / Role / Office Holding → ORG；
- Kinship / Genealogy → Kinship；
- private Relationship / Marriage → Relationship；
- public social evaluation → Reputation；
- Military Occupation → future War；
- Economy state → future Economy；
- legal eligibility / legal procedure → future Law；
- Promise lifecycle → Commitment；
- Formal Outcome / Commit → Runtime。

没有发现第二事实源。

---

## 4. ORG Hard Dependency｜PASS

Politics 把政府机构、党团、派系组织、官署、职位、成员与任职全部交给 `EP-ORG-CORE`。

公共权力可以来自 ORG Role Holding，但：

```text
Role Holding
!= Public Authority
Internal Authority
!= Public Authority
```

Politics 若不依赖 ORG，将被迫重新创建 Office / Faction membership；因此 Hard Dependency 合理且无 Hard Cycle：ORG 本身不 Hard Depend Politics。

---

## 5. Political Agreement × ORG Relation Skeleton｜PASS WITH RULE

潜在风险：Politics 的外交 / 联盟关系与 ORG 的 Formal Inter-Organization Relation lifecycle skeleton 双写。

v0.1 已冻结：

- Politics 拥有 domain-specific political meaning；
- Organization 参与时复用 / 对齐 ORG relation lifecycle；
- Politics 不复制 Organization identity / Membership；
- 若 ORG skeleton 被用作生命周期宿主，不允许再建立独立、互相漂移的第二 lifecycle。

当前语义足够；最终机器 hosting / record shape 等待 G9-03，不提前冻结。

---

## 6. Future Law Boundary｜PASS / DEFERRED

Politics 拥有“当前公共政治权力 / 政治承认 /政治控制”事实，但不判断：

- 某项权力在法律上是否合宪；
- 谁依法具有继承资格；
- 法律程序是否有效；
- 法院 / 法律如何裁决。

未来 Law 可以向 Politics 提供 legal judgment / eligibility；Politics 不把“政治上已经取得权力”自动等同于“法律上合法”。

没有因 Law 尚未建立而制造临时第二 Law Owner。

---

## 7. Claim / Recognition / Control / Occupation｜PASS

正式区分：

```text
Political Claim
!= Political Recognition
!= Political Control
!= Jurisdiction
!= Military Occupation
```

允许同一地区 / 身份出现冲突与重叠，不退化为单一 `owner` 或 `legitimacy` 数值。

---

## 8. Numeric-State Audit｜PASS

拒绝通用：

- loyalty；
- legitimacy；
- stability；
- control percentage；
- political power score。

世界 / UI 可以计算派生摘要，但派生值可重算、不可反写 Canonical Political Truth。

---

## 9. Open Attempt / Program Authority｜PASS

无权者仍可尝试：称帝、越权任命、伪造诏令、冒名谈判、拒绝承认、策反等。

Authority 影响 Formal Effect，不是输入白名单。

模型只提出 Candidate / interpretation；Program 负责 structural validation、deterministic query、Formal Outcome、Atomic Commit、Save / Restore / Recovery。

---

## 10. Information Boundary｜PASS

正式区分：

```text
Authoritative Political Truth
!= Public Political State
!= Player-known Political State
```

秘密支持、秘密外交、隐蔽授权与私下政治交易不得自动进入 Player Context。

Politics 不建立“每个角色知道什么”的完整知识系统。

---

## 11. Materialization / Durable Referent｜PASS

政治口号 / 建国宣言可先保持 Claim。

一旦政权成为持续可寻址、会被承认 /控制 /外交 /后续剧情引用的政治对象，必须 materialize 为 stable Game-local Regime。

禁止 Narrative-only 幽灵政权。

---

## 12. Runtime Context Contract｜PASS

正文内建 Pattern v0.5 全 18 项。

关键大型政治图链：

```text
Whole Political Graph
→ current target / question
→ Program deterministic relevant subgraph selection
→ player-safe bounded political slice
→ Model only if semantic work is needed
```

Dependency 不产生 transitive Prompt expansion；Economy / War 等潜在下游等待正式政治 Outcome / Handoff。

---

## 13. Future Explosion Review｜PASS

压力目标：

```text
Regime 5 → 50
Organization 20 → 200
Political actors 100 → 2000
Political edges 200 → 5000
Session history ↑↑↑

ordinary unrelated Turn context ≈ stable
local political query context ≈ current-relevant subgraph
```

典型局部问题：

- “谁控制洛阳？”只需洛阳直接相关 Claim / Control / Occupation / Recognition；
- “谁能代表这个政权谈判？”只需相关 Regime + ORG roles + Authority / Delegation；
- “谁支持新君？”只需目标政治状态 + direct Recognition / Issue Stance；
- 继承问题只 join 当前 ORG office/vacancy + Kinship relevant lineage path + Politics claims/recognition。

没有发现必须全图 Prompt 的理由。

---

## 14. G9 Boundary｜PASS

当前 G9-02BC 已 PASS / CLOSED；G9-02B ACTIVE；G9-03 NOT AUTHORIZED。

Politics v0.1 对齐已经证明的：

- built-in Domain Host；
- package / feature / module activation；
- owner-scoped canonical record / runtime state；
- typed change / event / handoff；
- JIT context projection；
- bounded owner-preserving join。

但不冻结 final JSON / machine schema / query DSL / Compiler / Creator controls / Surface ID。

---

# 15. Final

```text
Genericity                         PASS
Canonical Ownership               PASS
ORG Hard Dependency               PASS
Political Agreement boundary      PASS
Future Law boundary               PASS / DEFERRED
Claim/Recognition/Control split   PASS
Open Attempt                      PASS
Program Authority                 PASS
Information Boundary              PASS
Durable Referent                  PASS
Context Contract                  PASS
Future Explosion                  PASS
G9 Boundary                       PASS
```

> **EP-POLITICS-CORE v0.1：PASS / AUDITED CURRENT。**
