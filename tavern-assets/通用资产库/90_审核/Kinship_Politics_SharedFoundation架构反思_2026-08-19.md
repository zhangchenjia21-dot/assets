# Kinship + Politics｜Shared Foundation 架构反思

状态：**PASS / CROSS-DOMAIN RULE PROMOTED**  
日期：2026-08-19

## 1. 为什么现在反思

`通用资产库_维护规范_v0.7` 与路线 v0.8 都把 `Kinship + Politics` 收口后设为下一次正式 Architecture Reflection 点。

当前证据：

```text
EP-KINSHIP-CORE v0.1      PASS / AUDITED CURRENT
EP-POLITICS-CORE v0.1     PASS / AUDITED CURRENT
Politics Boundary Cluster PASS / CLOSED
```

因此可以判断 Kinship 的大型图经验是否只是领域特例。

---

## 2. 两个独立领域的共同问题

### Kinship

长期图包含：

- parentage；
- adoption；
- family / lineage；
- branch；
- genealogy claim；
- historical ancestry。

错误路线：保存所有兄弟 /祖孙 /叔侄 /堂表 /姻亲 pairwise derived edges，并在查询时加载整张谱系图。

### Politics

长期图包含：

- Regime；
- Authority / source / scope；
- Claim；
- Recognition；
- Control；
- Issue / Stance；
- Agreement；
- Delegation；
- political lifecycle refs。

错误路线：建立 pairwise loyalty / legitimacy / faction matrix，并把全国政治状态送给模型。

---

## 3. 共同稳定解法

两个领域独立得到同一结构：

```text
Canonical Source Facts / Edges
↓
Program deterministic current-relevant path / subgraph selection
↓
player-safe bounded owner projection
↓
Model only for open semantic work
```

并同时满足：

```text
Whole Relation Graph != Model Prompt
Derived Pairwise Summary != Canonical Truth
World Graph Growth != Ordinary Turn Context Growth
```

### Kinship reference

- 保存 parentage / adoption 等源关系；
- sibling / cousin / common ancestor / generation distance 由 Program 查询；
- 当前问题只投影必要亲缘路径。

### Politics reference

- 保存 Authority / Claim / Recognition / Control / Issue / Agreement 等规范政治事实；
- 当前地点 /政权 /议题先由 Program 选择相关政治子图；
- 模型不读取完整国家 /世界政治网络。

---

## 4. 为什么现在可以升格

这不再是“Kinship 的特殊优化”，原因：

1. 两个 Canonical Owner 完全不同；
2. 图结构语义完全不同；
3. 两者都存在长期增长和 pairwise explosion 风险；
4. 两者都存在大量确定性图查询；
5. 两者都需要 information-boundary-safe projection；
6. 两者都证明模型只需要当前问题相关子图，而不是整图。

因此已达到跨领域可复用规则的最低证据门槛。

---

# 5. 正式提升规则

建议正式升级 Runtime Context Pattern：

> **Large Relation Graph / Deterministic Subgraph Projection**

适用于：

- genealogy；
- politics；
- future knowledge / clue graph；
- social / organization relation graphs；
- future ownership / dependency / networked state；
- 其它长期、多节点、多边、可确定查询的领域。

规则：

```text
Large Relation Graph
→ store canonical source facts / minimal authoritative edges
→ avoid materializing all derivable pairwise relations
→ Program selects current-relevant paths / subgraph deterministically when possible
→ enforce player-safe / owner-safe projection
→ Model receives only minimum sufficient semantic slice
```

---

## 6. 不是所有关系都必须“只存源边”

此规则不能机械化为：

> “任何图都只准存最原始边。”

若某个关系本身就是长期 Canonical Truth，例如：

- Political Recognition；
- Political Agreement；
- ORG Membership；
- Relationship Shared Bond；

它本身就应该保存。

真正禁止的是：

> **为了方便查询，把可以稳定重算的成对派生结论大规模镜像成第二事实源。**

因此更准确的原则是：

> **Canonical source facts / semantically primary relations should persist；deterministically derivable graph projections should normally remain projections.**

---

## 7. Program / Model 分工

Program 优先承担：

- graph traversal；
- shortest / relevant path；
- direct-neighbor retrieval；
- common ancestor / generation distance；
- direct recognition / control / claim lookup；
- scope filtering；
- enabled / player-safe filtering；
- bounded subgraph assembly。

模型承担：

- 玩家开放式问题理解；
- 争议 / 模糊关系解释；
- 非标准语义；
- 多事实政治 / 社会意义判断；
- player-safe natural-language realization。

---

## 8. Context Contract 新增问题

建议 Pattern 从 18 项扩为 19 项：

> **19. Large Relation Graph / Deterministic Subgraph Projection（如适用）**

必须回答：

- Canonical primary relations 是什么？
- 哪些 pairwise / aggregate relations 可确定重算？
- Program 如何按当前问题选择 relevant path / subgraph？
- 如何避免 Whole Graph Prompt？
- 如何执行 private / player-safe filtering？
- 图规模增长 5–10 倍时普通 Turn Context 是否稳定？

---

## 9. Skill 是否应升级

**是。**

原因：本规则已通过两个独立 Core 证据，不再是项目专属 Politics / Kinship 细节，属于 Tavern 资产设计与 Context Audit 的可复用方法。

建议：

```text
tavern-asset v0.9
→ v1.0
```

新增：

- Large Relation Graph Gate；
- Canonical primary relation vs derived projection；
- deterministic subgraph projection；
- Future Explosion Review 中的 pairwise graph explosion / whole-graph prompt tests。

---

## 10. 对 G9 的影响

影响级别：**P2｜后续能力约束，不阻断当前 G9-02B。**

原因：

- G9-02BC 已建立 JIT projection / bounded owner-preserving join；
- 当前 G9-02B 可继续 registry / domain breadth；
- G9-02C 在 large registry / long-session context proof 时，应同时覆盖 large relation graph relevant-subgraph projection；
- 不需要现在修改 Host authority，也不需要提前冻结 G9-03 schema。

现有 Runtime Context Orchestration 总原则已要求长期世界状态增长不能等于 Prompt 增长，因此本规则是对现有架构的具体化，不改变 Stage DAG。

---

# 11. Final

```text
Kinship graph evidence                  PASS
Politics graph evidence                 PASS
Cross-domain repetition                 PASS
Pairwise explosion risk                 CONFIRMED
Deterministic subgraph solution         CONFIRMED
Pattern promotion                       APPROVED
Skill promotion                         APPROVED
G9-02B blocker                          NO
G9-02C future constraint                YES / P2
```

> **结论：将“Large Relation Graph / Deterministic Subgraph Projection”正式提升为通用 Runtime Context 设计规则。**
