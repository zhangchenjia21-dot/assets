---
title: EP-REPUTATION-CORE v0.1｜单资产审核
status: pass
review_date: 2026-08-18
asset: EP-REPUTATION-CORE
asset_version: 0.1
review_type:
  - asset-audit
  - context-contract-audit
  - consumer-stress-test
skill: tavern-asset v0.8.0
---

# EP-REPUTATION-CORE v0.1｜单资产审核

> [!success] 结论
> **PASS / AUDITED CURRENT。**
>
> `EP-REPUTATION-CORE v0.1` 填补了“公共社会评价事实”Canonical Owner 空白，没有复制 Relationship / ORG / Politics / Law / Knowledge / Character Capability；同时完整通过首轮 Runtime Activation / Context Contract Gate，可作为后续旧 Expansion Retrofit 的 Reference Implementation。

---

# 1. Owner Gap / Genericity

去掉“江湖 / 三国 / 古代中国”等世界名后，机制仍成立：Character / Organization 的公共名望与恶名、商业信誉、士林 / 官场 /军中口碑、Fantasy Guild / Church / Mage reputation、多 Audience 相互矛盾的社会评价。

至少存在独立消费者：汉末三国人物 /政治集团 /士林社会评价；江湖资产族侠名 /恶名 /门派声誉；商业 /组织玩法的组织信誉 /履约口碑。

结论：Genericity Gate PASS。

---

# 2. Canonical Ownership

Reputation Own：Target × Audience social evaluation；Spread / Salience / Contest / Currentness；Provenance reference；Social Epithet；public-perception lifecycle。

明确不 Own：

| Fact | Owner |
|---|---|
| 某人是否喜欢 / 尊重 / 信任另一人 | Relationship |
| Membership / Role / Rank | ORG |
| actual Skill / Capability | Character Core |
| Political Recognition / Claim / Control | Politics |
| Wanted / Case / Conviction | Law |
| 某 Character 是否知道某 Reputation | Knowledge / World OS |
| source Event 的真假 | Event / Information Owner |

结论：Ownership Gate PASS。

---

# 3. Semantic Namespace

```text
Organization Rank != Reputation Social Standing
Relationship Respect != Public Reputation of being respected
Political Recognition != Popular / Social Reputation
Legal Wanted / Conviction != Criminal Notoriety Reputation
Actual Capability != Reputation of Capability
```

结论：Semantic Namespace Gate PASS。

---

# 4. Audience Model

Audience 是一等语义；Region 不等于 Audience；Organization group / social class / geography 可以共同提供 Scope；Core 只引用 Audience Scope，不拥有 Region / ORG 本体；单个具体人默认不作为 Reputation Audience，以免复制 Relationship。

风险：未来机器协议需要定义 Audience reference / query primitive。

处理：记录为 G9 Binding Requirement，不影响当前 Semantic PASS。

---

# 5. Truth / Knowledge Boundary

资产允许虚假、误传、宣传、污名形成真实 Reputation State，但不保存第二份 truth flag。

```text
Reputation Claim != World Truth
Reputation exists != Character knows it
```

结论：Information Boundary PASS。

---

# 6. 单一分数 / Projection 审核

拒绝全局 Reputation Score。

允许 Runtime 在单个 Record / Dimension 内使用隐藏量化帮助 Spread / Salience / Credibility / Contest / Persistence，但不冻结数值范围，Derived Summary 不可反写 Canonical Records。

结论：Canonical vs Projection PASS。

---

# 7. Open Attempt / Program Authority

玩家可以冒充名号、夸大名声、散布污名、公开洗白；Reputation 不作为输入白名单。

模型只输出 candidate evaluation / spread / epithet / interpretation；Program / Runtime Own Ref validation、State persistence、lifecycle bookkeeping、Formal Outcome、Atomic Commit、Save / Restore。

结论：Open Attempt + Program Authority PASS。

---

# 8. Runtime Context Contract Audit

- Routing Profile：PASS，一行 Scope + 少量语义提示可区分邻近 Domain；
- Immediate Activation：PASS，查询 /利用 /操纵公众评价时直接激活；
- Downstream Activation：PASS，公开决斗、犯罪、政治事件等通过 Formal Event / Handoff 后激活；
- No-load：PASS，私人闲聊、普通 Combat action parsing、纯 Health /移动 /物品操作不因 Enabled 自动加载；
- Minimal Read：PASS，Target + relevant Audience + relevant Evaluation + bounded provenance summary；
- Model-needed：PASS，自然语言路由、社会意义解释、candidate evaluation / epithet、矛盾声誉摘要；
- Program-owned：PASS，State / Ref / persistence / commit 留在 Runtime；
- Context Cost：PASS，`All Reputation Records != Current Context Slice`。

结论：Runtime Relevance / Bounded Working Set PASS。

---

# 9. Consumer Stress Test

## Case A｜江湖侠客

actual martial skill → Character / Martial domain；江南武林与官府圈层的评价 → Reputation；Wanted → future Law；NPC 个人是否敬重 → Relationship。无 Owner 冲突，PASS。

## Case B｜门派

“苍梧剑派在江南武林以护短著称”：Organization identity / members → ORG；organization-target reputation → Reputation。PASS。

## Case C｜汉末名士

“士林普遍认为某人清议极高，但政权没有授官”：士林评价 → Reputation；Office / public authority → ORG + Politics；名望不自动产生任命。PASS。

## Case D｜商业信誉

“某商号在河运商人中被认为从不拖欠”：Organization → ORG；market/resource → Economy；public reliability evaluation → Reputation。PASS。

---

# 10. Surface Audit

不 owns 一级 Extension Surface。贡献 Person Detail / Organization Detail / Information / Contextual。未来江湖 Workspace 存在时仅 contributes。PASS。

---

# 11. 已知 Future / Non-blocking

1. Audience machine primitive 等待 G9；
2. Cross-audience spread 具体算法不在 Semantic 阶段冻结；
3. Place / Item Target 仅轻量兼容；
4. Reputation Dimension machine registry 等待 Creator / asset-spec vNext；
5. token budget 等待真实 Provider Context Composition Benchmark；
6. Law / Politics 尚未 genericized，但边界已冻结。

---

# 12. Final Gate Summary

| Gate | Result |
|---|---|
| Genericity / Shared Foundation | PASS |
| Canonical Ownership | PASS |
| Semantic Namespace | PASS |
| Relation Typing | PASS |
| Definition / Instance | PASS |
| Canonical vs Projection | PASS |
| Cause / Process / Consequence | PASS |
| Open Attempt | PASS |
| Program Authority | PASS |
| Information Boundary | PASS |
| UI Surface | PASS |
| Creator Authorability | PASS at semantic level / G9 binding pending |
| Runtime Relevance / Context | PASS |
| Consumer Stress Test | PASS |
| Future Explosion Review | PASS WITH RETROFIT PLAN |

最终状态：**EP-REPUTATION-CORE v0.1 = AUDITED CURRENT**。
