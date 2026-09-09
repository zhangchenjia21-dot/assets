---
title: 汉末三国｜Politics Core 迁移规划
version: 0.1
status: current-migration-plan
created: 2026-08-19
updated: 2026-08-19
source_asset: 汉末三国_政争与势力_Expansion_Pack_v0.2.1
upstream_core: EP-POLITICS-CORE v0.1
execution_status: not-started
---

# 汉末三国｜Politics Core 迁移规划 v0.1

> [!abstract]
> `EP-POLITICS-CORE｜政治与公共权力核心 v0.1` 已 PASS / AUDITED CURRENT。本文件只规划汉末三国 `政争与势力 v0.2.1` 的拆分、迁移与重绑定；**本轮不修改旧汉末 Canonical Expansion、World Pack 或 Character Card。**

---

# 1. 迁移目标

旧 `汉末三国：政争与势力 v0.2.1` 已包含大量成熟政治语义，但当前把以下内容集中在一个 World-specific Owner：

- Political Faction；
- Political Affiliation；
- Office Definition / Holding；
- Authority / Jurisdiction；
- Recognition；
- Control；
- Diplomacy；
- Succession；
- Political Claim；
- Regime Transition。

在 Shared Foundation 已拥有 ORG / Kinship / Reputation / Relationship / Politics 后，必须拆为正确 Owner，而不是把旧包整体改名为 Generic Politics。

目标：

```text
旧 Han Politics composite owner
↓
ORG + Kinship + Relationship + Reputation + Generic Politics
↓
Han-specific political semantics / examples / history integration remain downstream
```

---

# 2. 总体迁移原则

1. **保留成熟语义，删除重复 Owner。**
2. `Political Faction` 不再默认作为第二 Organization entity。
3. Office / Affiliation / Membership 不再由 Han Politics 持久化。
4. 公共 Authority / Recognition / Claim / Control / Regime 迁到 `EP-POLITICS-CORE`。
5. 继承必须拆成 Kinship / ORG / Politics / future Law 四层。
6. Political Agreement 与 Commitment 继续分权。
7. `势力 / 政务` 作为汉末产品组合需求可以保留为 World-specific UI intent，但不能反向成为 Generic Politics 固定一级 Surface。
8. 不因迁移提前实现 Economy / War Core；只保留 typed handoff 待后续迁移。
9. 不冻结 G9-03 machine fields。

---

# 3. 迁移 Ledger

| 旧概念 | 操作 | 新 Owner / 去向 | 说明 |
|---|---|---|---|
| Political Faction | **SPLIT** | ORG + Politics Regime/Issue | 有成员/领导/内部结构的集团 → ORG；真正公共政治秩序 → Regime；不得继续万能 Faction |
| Political Affiliation | **SPLIT / REBIND** | ORG + Politics | formal service / retainer / staff → ORG；针对政治议题的正式站队 → Politics Stance |
| Office Definition | **MIGRATE** | ORG | 官职 /公共职位首先是 Role Definition |
| Office Holding | **MIGRATE** | ORG | 任职事实不再由 Politics 保存 |
| Office political effect | **SPLIT** | Politics | Role 产生的 Public Authority / Jurisdiction 在 Politics |
| Appointment / Removal | **SPLIT** | ORG + Politics | Role change → ORG；政治授权 /公共后果 → Politics |
| Internal Authority | **REBIND** | ORG | 与公共政治 Authority 分离 |
| Public Authority | **MIGRATE** | EP-POLITICS-CORE | 保留成熟语义，补 source / scope / delegation |
| Jurisdiction | **MIGRATE / REFINE** | EP-POLITICS-CORE | 范围可按地域 /对象 /事项 /时间 /条件 |
| Political Recognition | **MIGRATE** | EP-POLITICS-CORE | 方向性、有对象、有内容；拒绝全局 legitimacy score |
| Political Control | **MIGRATE / REFINE** | EP-POLITICS-CORE | 与 Claim / Occupation / Jurisdiction 严格分开 |
| Territorial / Office / Succession Claim | **MIGRATE** | EP-POLITICS-CORE | Claim 不自动产生 Recognition / Control |
| Political Support / Opposition | **MIGRATE / REFINE** | Politics Issue/Stance | 必须针对明确政治议题 /主张；不建立 loyalty |
| Diplomatic Political Relation | **MIGRATE / REBIND** | Politics + ORG relation skeleton | 政治语义 → Politics；组织参与时对齐 ORG lifecycle |
| Political Agreement | **MIGRATE** | EP-POLITICS-CORE | 协议本身迁移 |
| Explicit Promise in Agreement | **REBIND** | Commitment | 不在 Politics 建 pending/fulfilled/broken 第二状态 |
| Succession genealogy input | **REBIND** | EP-KINSHIP-CORE | 血缘 /家系 /分支只由 Kinship 提供 |
| Succession office/vacancy | **REBIND** | EP-ORG-CORE | 当前职位与空缺归 ORG |
| Succession legal eligibility | **DEFER / REBIND LATER** | future Law | 不由 Han Politics 临时承担 |
| Succession political process/result | **MIGRATE** | EP-POLITICS-CORE | Claim / support / recognition / public authority transition |
| Regency | **MIGRATE / REFINE** | EP-POLITICS-CORE | 表达为 delegation / authority acting arrangement |
| Regime | **MIGRATE / REFINE** | EP-POLITICS-CORE | 与 Organization 分离，建立稳定政治秩序身份 |
| Regime Transition | **MIGRATE / GENERALIZE** | EP-POLITICS-CORE | 改名 /继承 /政变 /革命等归公共权力结构变更 |
| Marriage Bond | **KEEP EXTERNAL** | Relationship | 旧包已正确分权，继续不迁入 Politics |
| Marriage political consequences | **MIGRATE** | Politics | Political Agreement / Claim / Recognition consequence |
| Family / dynastic lineage | **REBIND** | Kinship | 不因政治继承再次复制家系 |
| Public popularity / social legitimacy | **REBIND** | Reputation / future public-belief layer | 不混入 Political Recognition |
| Character political capability mastery | **KEEP EXTERNAL** | EP-CHAR-CORE | Politics 只可贡献 Skill Definition |
| Diplomacy Skill Definition | **MIGRATE CANDIDATE** | Generic Politics contribution | 跨世界通用 |
| 辩说 / 公共论证 Skill Definition | **MIGRATE CANDIDATE** | Generic Politics contribution | 跨世界通用 |
| 政局判断 / 政治分析 Skill Definition | **MIGRATE CANDIDATE** | Generic Politics contribution | 跨世界通用 |
| 法政 Skill | **SPLIT** | Politics + future Law | 政治制度理解可留 Politics；法律专业 /程序等等待 Law |
| 人事与识才 | **SPLIT / RE-EVALUATE** | ORG / Character | 组织用人不应由 Politics 独占 |
| Health availability read | **KEEP / REBIND** | EP-HEALTH-CORE optional | 身体事实仍外部读取 |
| Economy integration | **KEEP HANDOFF / DEFER** | future EP-ECONOMY-CORE | 不提前冻结 |
| War integration | **KEEP HANDOFF / DEFER** | future EP-WAR-CORE | Occupation 与 Control 分离 |
| History divergence integration | **KEEP HAN-SPECIFIC** | 汉末历史参照与分歧 | Generic Politics 不拥有历史贴合 |
| `势力 / 政务` 一级 Surface | **KEEP HAN-SPECIFIC / RE-EVALUATE** | Han composition / Product | 不迁为 Generic Politics 固定 Surface |
| Political Control map overlay | **KEEP AS UI INTENT** | Politics contribution | G9-03 前不冻结 Surface ID / machine shape |
| T0 Historical baseline | **SPLIT** | 各 Canonical Owner | ORG / Kinship / Politics 分别初始化自己的事实 |
| Save / Restore political state | **SPLIT** | 各 Owner + Runtime | 不由 Han Politics 保存其它 Owner state |

---

# 4. 旧玩法闭环迁移

## 4.1 仕进 / 投奔

旧链：Political Affiliation。

新链：

```text
投奔 /征辟 /招揽 Attempt
↓
Character choice
↓
ORG Membership / Formal Affiliation / Role candidate
↓
如产生公共政治身份 /权力
→ Politics Authority / Stance consequence
```

Politics 不再 owns“加入集团”。

## 4.2 任命

```text
Office / Role existence      → ORG
任命者当前 Public Authority  → Politics
目标是否接受                  → Character / Relationship context
Role Holding commit          → ORG
产生的 Public Authority      → Politics
```

## 4.3 外交

旧成熟链基本保留：

```text
Political negotiation
→ Political Agreement
+ explicit Commitment extraction
→ future fulfillment / violation
```

新增：参与方为 Organization 时对齐 ORG formal relation skeleton。

## 4.4 继承

```text
Kinship relevant lineage
+ ORG office / vacancy
+ Politics Claim / Issue / Stance / Recognition / Control
(+ future Law eligibility when available)
↓
Formal political outcome
```

禁止复制前任的全部 Office / Control / Recognition / Army / Relationship 给继承者。

## 4.5 政权转型

旧 `Regime Transition` 保留价值，但迁为 Generic：

```text
Claim / process
→ authority structure change
→ Recognition / Control change
→ stable Regime lifecycle
```

汉末专有“称帝 / 奉天子 / 禅让”等作为世界语义实例，不成为 Generic 默认流程。

---

# 5. 汉末专用内容保留

以下不应被“通用化”删除：

- 汉末官制名称与职位定义；
- 汉廷、诸侯、州郡等历史 /世界对象；
- 奉天子、称帝、禅让等具体历史政治语境；
- 汉末势力关系与初始政治格局；
- 汉末 History Divergence handoff；
- 汉末 UI / 玩家表达习惯；
- 与财赋、军略、历史参照的世界专用组合。

它们在迁移后成为：

> Generic Core 的 Han-specific definitions / composition / initial data / theme semantics。

---

# 6. 迁移执行顺序

```text
1. EP-POLITICS-CORE v0.1 audited-current        ✓
2. 本 Migration Plan                            ✓
3. 读取 Han World Pack / 政争与势力 / ORG & Kinship current refs
4. 建立逐段迁移映射
5. 修订汉末《政争与势力》为下游 World-specific Politics Expansion
6. 更新 Han asset family index / blueprint / version lock
7. 检查 World Pack / Character Card 引用
8. 单资产 Audit
9. Han Politics × Generic Core convergence
10. 再进入 Economy Core 生产
```

---

# 7. 执行时禁止

- 直接把旧 `Political Faction` 改名 `Regime` 后保留成员 / Office；
- 在 Han Politics 留第二份 Role Holding；
- 把 dynastic succession 血缘复制到 Politics；
- 把 Reputation / public belief 当成 Recognition；
- 把 Military Occupation 当 Control；
- 因 Law 未创建就在 Politics 冻结法定继承引擎；
- 一次性顺手迁移 Economy / War canonical state；
- 为兼容未发布旧语义长期保留 duplicate fallback owner；
- 在 G9-03 前建立机器 adapter / final schema。

---

# 8. 成功标准

迁移执行后至少满足：

```text
Han Politics duplicate Organization owner       = 0
Han Politics duplicate Office Holding            = 0
Han Politics duplicate Kinship truth             = 0
Han Politics duplicate Relationship truth        = 0
Han Politics duplicate Commitment lifecycle      = 0
Claim / Recognition / Control split              = PASS
Military Occupation != Political Control         = PASS
Han-specific semantics preserved                 = PASS
G9-03 premature machine contract                 = 0
```

---

# 9. 当前状态

> **PLAN COMPLETE / MIGRATION NOT YET EXECUTED。**

当前下一安全动作：按本 Ledger 修订 `汉末三国_政争与势力_Expansion_Pack_v0.2.1.md`，完成真实 Han consumer migration 后，再进入 Economy Core。
