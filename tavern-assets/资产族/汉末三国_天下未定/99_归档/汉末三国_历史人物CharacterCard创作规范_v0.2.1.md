---
title: 汉末三国：历史人物 Character Card 创作规范
aliases:
  - 汉末三国历史人物卡创作规范
  - 三国CharacterCard规范
created: 2026-08-15
updated: 2026-08-15
status: candidate
version: 0.2.1
type: 资产族创作规范
workflow_mode: asset-family
operation_mode: create
skill: tavern-asset v0.2.0
output_profile: obsidian-markdown
capability_expansion: "[[汉末三国_人物能力与技艺_Expansion_Pack_v0.1]]"
asset_family: 汉末三国：天下未定
creator_binding: pending
asset_spec_binding: pending
supersedes:
  - "[[汉末三国_历史人物CharacterCard创作规范_v0.1]]"
related:
  - "[[汉末三国_资产组合总蓝图_v0.2]]"
  - "[[汉末三国_天下未定_World_Pack_v0.2]]"
tags:
  - 酒馆游戏
  - tavern-asset
  - 资产族
  - 三国
  - 角色卡
  - 历史人物
  - CharacterCard
  - HistoricalBaselineResolver
  - ResearchNote
  - Obsidian
---

# 汉末三国：历史人物 Character Card 创作规范 v0.2

> [!abstract] 文档定位
> 本文件是《汉末三国：天下未定》资产族内部的**历史人物 Character Card 创作规范**。
>
> v0.2 的核心目标不是让人物卡“记录更多”，而是让人物卡成为**短、稳定、高密度、适合 Runtime 调用的 Character Definition**。
>
> 详细史料、争议论证、人格推断依据与创作研究全部从正式人物卡中移出，进入独立的 **Historical Character Research Note**。
>
> 本规范不是 `tavern-asset-spec vNext` Schema，也不预设未来 Creator 的机器字段。

> [!important] v0.2 核心裁定
> 1. **一位历史人物只生产一张 Character Card。**
> 2. Character Card 是高密度 Runtime Character Definition，不是人物传记、年表或研究论文。
> 3. Character Card 默认目标长度：普通人物约 **1200–2500 中文字**；核心复杂人物原则上控制在 **2000–3500 中文字**；超过约 **4000 中文字**必须触发压缩审核。
> 4. 史料证据、冲突、人格推断链、文学形象差异等详细研究移入独立 **Historical Character Research Note**；Research Note 不是资产，不默认进入游戏上下文。
> 5. Character Card 在时间维度上只强制保存出生年份／范围／未知，以及必要身份消歧信息。
> 6. `T0` 前的官职、位置、关系、婚姻、经历、知识等生涯事实，由 **Historical Baseline Resolver** 在开局实例化阶段通过受控联网研究生成候选快照。
> 7. Historical Snapshot 被验证并锁入 Game State 后，`T0` 之后现实历史不再拥有改写本局世界的权威。
> 8. 角色卡优先保存“能解释大量行为的少量结构”，而不是穷举场景反应或固定台词。

---

# 0. Scope Lock

## 0.1 本规范只解决什么

本规范只解决：

> **真实汉末三国历史人物如何被压缩成一张可复用、可实例化、可供模型高效理解的 Character Card。**

适用于：

- 诸侯与君主；
- 文臣、谋士与官员；
- 将领与武人；
- 皇帝、宗室与外戚；
- 地方豪族与士人；
- 女性历史人物；
- 史料较少但身份可确认的人物；
- 可作为 NPC、玩家角色或双用途角色的真实历史人物。

## 0.2 本规范明确不解决

不在 Character Card 中生产：

- 三国完整历史年表；
- 世界级政治格局；
- 州郡地理数据库；
- 战争、政治、经济、治理、恋爱等通用运行机制；
- 当前游戏中的官职、位置、关系、婚姻、兵力、资产、伤势或资源；
- 每个年份的人物快照；
- Runtime 联网研究代码；
- Creator 编辑器实现；
- `tavern-asset-spec vNext` 的字段、Ref、ID、enum、Validator。

这些分别归 World Pack、Expansion Pack、Game Runtime / Game State、未来 asset-spec 与 Creator。

---

# 1. v0.2 的核心模型：三层人物资料

以后每个历史人物原则上存在三种不同资料，但只有第一种是正式资产。

```text
Character Card
稳定、高密度、运行时可加载
        │
        ├── 创作时参考 → Historical Character Research Note
        │                 长篇史料与论证，非资产
        │
        └── 开局时结合 → Historical Baseline Snapshot
                          T0 历史快照，进入 Game State
```

## 1.1 Character Card

**正式资产。**

回答：

> 这个人是谁？他通常怎样判断、行动、建立关系和表达自己？

它保存：

- 稳定身份锚点；
- 人格与价值结构；
- 能力与局限；
- 决策逻辑；
- 关系风格与自主性；
- 语言表现；
- 玩家接管边界；
- Resolver Handoff。

它不保存完整考据过程。

## 1.2 Historical Character Research Note

**非资产创作资料。**

回答：

> 为什么我们把这个人物这样写？哪些结论来自什么证据？哪里有争议？

它可以很长，并可保存：

- 使用过的史料与研究资料；
- 重要人物行为证据；
- 史料互相冲突之处；
- 生年等基础事实争议；
- 人格推断链；
- 后世评价；
- 演义、民间传统与正史差异；
- 创作取舍；
- 待核查项；
- 被 Character Card 主动舍弃的细节。

Research Note：

- 不属于 Character Definition；
- 不默认发送给模型 Runtime；
- 不作为 Game State；
- 不应被未来游戏本体当作隐形第二张人物卡。

## 1.3 Historical Baseline Snapshot

**开局实例化结果。**

回答：

> 在这一局的 `T0`，截至这一刻这个人物已经经历了什么、目前是什么状态？

由 Character Card + World Pack + `T0` + Historical Baseline Resolver 共同生成，经验证后进入 Game State。

---

# 2. 一人一卡与时间边界

## 2.1 一人一卡

一个真实历史人物只维护一张 Character Card。

禁止长期维护：

- `曹操_184.md`；
- `曹操_200.md`；
- `曹操_208.md`；
- `曹操_220.md`。

这类差异属于实例化历史状态，而不是四个不同 Character Definition。

## 2.2 Character Card 的时间字段最小化

当前只强制：

- 出生年份；或
- 出生年份范围；或
- 出生年份未知／存在争议。

允许附带：

- 必要身份消歧；
- 极简史料备注。

当前不强制：

- 死亡年份；
- 每年官职；
- 每年位置；
- 每年所属势力；
- 每年婚姻；
- 每年关系；
- 每年知识；
- 逐年军功与政治经历。

未来是否增加轻量生命周期元数据，由 `asset-spec vNext` 根据真实 Runtime / Creator 需求决定。

## 2.3 `T0` 是历史与游戏未来的分界线

```text
T0 之前
→ 可以用现实史料恢复已经发生的过去

T0
→ Historical Snapshot 验证并锁定到本局

T0 之后
→ World OS + Game State 自主演化
→ 现实历史只保留参考身份
```

不得在长期游戏过程中周期性联网“同步人物真实历史”。

---

# 3. 五层事实 Owner

## 3.1 World Historical Baseline

Owner：World Pack。

负责：

- 世界级历史时点；
- 政权与时代；
- 大型历史事件；
- 世界级公开政治格局；
- 地理与社会历史背景。

Character Card 不复制完整世界历史。

## 3.2 Character Definition

Owner：Character Card。

负责：

- 这个人物是谁；
- 稳定人格；
- 价值与判断结构；
- 能力轮廓；
- 局限；
- 关系风格；
- 自主性；
- 表达风格；
- 玩家接管边界。

## 3.3 Research Evidence

Owner：Historical Character Research Note。

负责：

- 证据；
- 争议；
- 推断链；
- 创作理由。

它支持创作，但不拥有正式 Runtime 人物定义。

## 3.4 Historical Baseline Snapshot

Owner：Game Bootstrap / Historical Baseline Resolver。

负责 `T0` 当前历史状态候选。

## 3.5 Current Character State

Owner：Game Runtime / Game State。

包括：

- 当前官职；
- 当前位置；
- 当前势力；
- 当前关系；
- 当前家庭／婚姻状态；
- 当前知识；
- 当前目标；
- 当前意向；
- 当前伤势；
- 当前资源；
- 当前生死。

---

# 4. Character Card 长度与信息密度规范

## 4.1 长度不是越短越好

目标是：

> **用最少但足够的信息，使模型能够稳定区分人物、推演行为并保持自主性。**

不得为了满足数字限制删除真正决定角色行为的关键信息。

## 4.2 默认长度预算

这些是创作纪律，不是未来 Schema 硬限制。

### 简单 / 史料较少人物

建议：**700–1600 中文字**。

### 普通重要人物

建议：**1200–2500 中文字**。

### 核心复杂人物

建议：**2000–3500 中文字**。

### 超长警戒线

约 **4000 中文字以上**触发强制压缩审核。

只有以下情况才能合理超出：

- 人物存在多个真正决定行为的稳定身份层；
- 玩家/NPC 双用途边界极其复杂；
- 史料争议必须在卡中保留少量关键警告；
- 删除内容会明显破坏人物可识别性或安全边界。

“人物很有名”不是超长理由。

## 4.3 不设最低字数

史料少的人物不为了“完整”虚构：

- 人格；
- 爱好；
- 私密心理；
- 性格弱点；
- 恋爱倾向。

资料不足时允许一张很短但诚实的卡。

## 4.4 高密度写作原则

优先写：

- 能解释很多行为的核心价值；
- 多场景可复用的决策逻辑；
- 关键能力与局限；
- 明确的自主性边界；
- 与其他角色区分度高的表现特征。

减少：

- 形容词堆叠；
- 同义反复；
- 大量生平事件；
- 场景穷举；
- 大量示例台词；
- “他很聪明、他有谋略、他足智多谋”式重复；
- 已可由 Resolver 在 T0 恢复的历史状态。

## 4.5 每个信息进入正式卡前问三个问题

1. **它是否跨多个时间节点仍有意义？**
2. **它是否会显著改变模型对人物的判断或行为推演？**
3. **如果删除它，人物是否仍然可以被稳定地区分和扮演？**

若前两项都是否，通常不进入 Character Card。

---

# 5. Character Card 正式正文：8 个核心章节

正式卡默认只保留以下 8 个主体章节。

## 5.1 身份锚点

保存：

- 姓名；
- 字／号／常用称呼；
- 出生年份／范围／争议；
- 籍贯与基础出身；
- 必要身份消歧；
- 一句话辨识。

一句话辨识必须描述人物的**运行意义**，不是百科简介。

## 5.2 人格核心

优先保存：

- 2–5 个真正有解释力的核心价值／倾向；
- 1–3 个核心矛盾；
- 风险偏好；
- 压力下可能发生的变化；
- 哪些重大经历可能改变其长期信条。

不得把后世标签直接当人格真相。

例如“奸雄”“仁君”“武圣”只能作为历史评价或文学标签，不应未经分析直接成为人格定义。

## 5.3 能力与局限

只写**稳定 Character Definition 层的语义能力轮廓**：

- 主要长处；
- 重要经验；
- 真实局限；
- 典型误判风险。

这部分是未来 `Capability Bootstrap` 的证据输入，不是 Runtime Capability Profile 本身。

因此禁止直接在 Character Card 中固定：

- 统率 / 武力 / 智力 / 政治 / 魅力数值；
- 骑术 / 长兵 / 行政 / 财计等正式技能等级；
- T0 以后才可能形成的经历或专长。

历史人物在某个 `T0` 的正式能力状态应由：

```text
Character Definition
+
Historical Snapshot
+
Research Evidence
+
《人物能力与技艺》
↓
Capability Profile Candidate
↓
Validation
↓
Game State
```

生成。

Character Card 可以写“善统兵”“擅长人才组织”“军事经验丰富”这类稳定语义轮廓，但不能直接等价成：

> `统率 = 顶尖`

或：

> `统兵 = 卓越`

不因为人物著名就写成全能。

## 5.4 决策与行为逻辑

这是 Character Card 最重要的章节之一。

应回答：

- 遇到重大问题时优先保护什么；
- 如何权衡利益、风险、名义、恩义、长期目标；
- 什么条件下合作；
- 什么条件下拒绝；
- 如何面对失败、背叛、威胁与失控；
- 什么类型的证据或关系能真正改变其判断。

目标是提供**生成式决策结构**，而不是固定剧情脚本。

## 5.5 关系风格与自主性

应回答：

- 如何建立信任；
- 如何看待亲族、主从、同僚、部属、竞争者；
- 对利益与私人感情如何排序；
- 什么会破坏关系；
- 是否容易原谅；
- 在玩家不在场时会如何继续追求自己的目标；
- 不会因为“玩家是主角”而自动做什么。

可写亲密关系风格，但不得预设具体恋爱结果。

## 5.6 语言与表现

只保留真正能区分人物的表现信息：

- 表达节奏；
- 公私场合差异；
- 礼貌／直接程度；
- 情绪表达；
- 少量措辞倾向。

示例台词：

- 可选；
- 通常 0–3 条；
- 只用于校准语感；
- 不作为固定宏；
- 不要求模型复述历史名言。

## 5.7 Player Character 接管说明

如果该角色支持玩家扮演，必须明确：

### `T0` 前锁定

- 已发生的人生；
- 已建立的身份；
- 已存在的世界事实；
- Bootstrap 锁定的关系与知识。

### `T0` 后交给玩家

包括：

- 行动；
- 立场；
- 忠诚；
- 政治选择；
- 爱恨；
- 是否背叛；
- 是否原谅；
- 人生目标；
- 价值变化。

系统不得以“历史上的此人后来……”强迫玩家选择。

纯 NPC 卡可将本节简化为“不作为玩家角色”的说明。

## 5.8 Historical Baseline Resolver Handoff

只写 Resolver 真正需要的**身份锚点和查询范围**。

建议包含：

- 规范姓名；
- 身份消歧；
- 出生时间信息；
- T0 需要恢复的状态类别；
- 已知重点争议；
- 禁止把 T0 后历史写成当前事实。

不得在 Handoff 中提前写一套年表。

---

# 6. 可选短章节

以下内容只有真正必要时进入 Character Card。

## 6.1 极简史料备注

最多保留少量会直接影响 Runtime 解释的警告，例如：

- 生年存在重大争议；
- 两个同名人物容易混淆；
- 某著名人格标签主要来自后世文学而非可靠史料。

详细论证必须进入 Research Note。

## 6.2 稳定私密事实

如果存在真正跨年代稳定、且对角色扮演必要的私密事实，可以短写。

必须同时满足：

- 有可靠来源或明确创作授权；
- 不是 `T0` 当前状态；
- 不会泄露给普通玩家视角；
- 不属于 Runtime 应动态维护的秘密。

默认少用。

## 6.3 人物特有依赖

仅记录此人物独有的资产依赖。

不要每张卡重复：

- 本资产族 World Pack 名称；
- 通用恋爱包；
- Game Runtime；
- Creator；
- asset-spec。

这些属于资产族蓝图。

---

# 7. Historical Character Research Note 规范

## 7.1 定位

Research Note 是：

> **人物卡的证据层与创作工作底稿。**

它可以比 Character Card 长很多。

## 7.2 何时必须建立

以下任一情况建议建立独立 Research Note：

- 核心历史人物；
- 人格评价争议较大；
- 正史与后世文学形象差异明显；
- 生年、身份或重要经历存在争议；
- 需要跨多种史料归纳人格；
- Character Card 将作为资产族示范卡或质量基准。

资料极少、角色简单时，可以只保留极短创作记录，不强制做长篇附录。

## 7.3 Research Note 可以包含什么

### A. 身份与基础事实研究

- 姓名与异名；
- 字号；
- 籍贯；
- 出生时间；
- 身份消歧。

### B. 行为证据库

收集真正能支持人格和决策判断的历史事件。

重点不是复制完整年表，而是回答：

> 哪些已发生行为能证明这个人物通常怎样判断？

### C. 史料冲突

保留：

- 来源 A；
- 来源 B；
- 冲突点；
- 当前处理；
- 是否影响 Character Card。

### D. 人格推断链

使用：

```text
历史行为 / 陈述
→ 可支持的中层判断
→ Character Card 中采用的高层人格结构
```

禁止：

```text
后世标签
→ 直接写成心理事实
```

### E. 文学与大众形象差异

记录：

- 正史；
- 裴注等补充材料；
- 《三国演义》；
- 民间传统；
- 现代流行形象。

明确哪些内容不进入默认正史人物卡。

### F. 创作取舍

说明：

- 为什么某条写入 Character Card；
- 为什么某条被舍弃；
- 哪些地方有意保持留白。

### G. 待核查

无法确认的内容不要为了完成度强行裁定。

## 7.4 Research Note 不得偷偷成为第二人物卡

Research Note 中可以有大量事实，但 Runtime 默认不应加载全文。

未来 Creator 如果允许“查看研究资料”，也必须明确它是创作辅助，不是正式 Character Definition。

---

# 8. 史实、推断与创作分层

所有研究与人物卡创作至少区分五类。

## S1｜来源支持的稳定事实

例如：

- 姓名；
- 籍贯；
- 可确认的家族身份；
- 可确认出生时间范围。

## S2｜来源支持的行为证据

某人物确实做过、说过或被可靠材料记录的行为。

行为事实不自动等于人格标签。

## I1｜人格推断

由多项行为证据归纳出的倾向。

必须允许被新证据修正。

## L1｜文学 / 后世传统

《三国演义》、民间传说、后世评价、现代流行文化。

默认不作为正史事实。

## C1｜创作补全

史料空白时为了可玩性进行的有限补全。

必须：

- 不与已知事实冲突；
- 不冒充史料；
- 不制造无依据的重大私密设定；
- 必要时保留为“不确定”。

---

# 9. 人格抽象：从“标签”转向“生成规则”

## 9.1 不写标签清单

避免：

- 雄才大略；
- 多疑；
- 重情；
- 冷酷；
- 聪明；
- 有野心。

这些词本身解释力太低。

## 9.2 改写成决策结构

例如不要只写：

> 多疑。

而应尝试说明：

> 在政治安全受到威胁、信息来源互相矛盾或控制力下降时，会显著提高对背叛可能性的权重，因此可能接受更高的误伤风险来避免失控。

这样模型才能把同一人格迁移到新情境。

## 9.3 核心矛盾比“优点缺点”更重要

优秀人物卡通常包含至少一个长期矛盾，例如：

- 理想与现实；
- 私情与政治责任；
- 信任人才与控制风险；
- 名义合法性与实际权力；
- 豪迈进取与资源约束。

但不得为了戏剧性强行制造不存在的矛盾。

## 9.4 允许人物成长

Character Definition 不是命运锁。

人格应描述：

- 初始结构；
- 惯常判断；
- 改变需要多大的原因。

不能写成永远不会变化的固定人格机器人。

---

# 10. 能力与知识：只保留轮廓

## 10.1 能力不写成万能排名

只记录人物真正有历史依据或高度可信依据的能力领域。

不要因为人物后来成功就反推：

> 他在所有相关能力上都顶级。

## 10.2 Character Card 记录知识能力，不记录 T0 全部知识

可以写：

- 教育背景；
- 熟悉领域；
- 信息网络倾向；
- 专业经验；
- 典型知识盲区。

不写：

> 208 年他现在知道某军已经从某条路线出发。

这属于 Game State / Historical Snapshot。

## 10.3 不允许史书全知

历史人物不能因为现实互联网存在其完整传记，就知道：

- 自己未来；
- 他人未来；
- 未发生战争结果；
- 未公开阴谋；
- 后世对自己的评价。

---

# 11. 关系、婚姻与恋爱边界

## 11.1 稳定关系风格归 Character Card

例如：

- 如何建立信任；
- 如何对待亲族；
- 如何对待部属；
- 如何处理竞争；
- 是否倾向把私人关系服从于政治利益。

## 11.2 T0 当前关系归 Historical Snapshot / Game State

例如：

- 某年是否已经结婚；
- 与某人当前是否敌对；
- 某人是否已经投奔；
- 当前亲密程度。

不得永久写入跨年代 Definition。

## 11.3 恋爱机制不归 Character Card

Character Card 可以决定：

- 人物怎样建立亲密；
- 什么会产生信任；
- 哪些价值冲突会阻止关系。

但不能规定：

- 玩家达到多少好感自动恋爱；
- 此人物是“可攻略角色”；
- 必然爱上玩家。

## 11.4 不虚构私密性取向

史料未支持时，不把现代意义上的私密性取向作为确定历史事实。

可在具体游戏中通过角色自主发展，而不是提前伪史实化。

---

# 12. NPC 自主性与玩家接管

## 12.1 NPC 模式

人物作为 NPC 时：

- 有自己的利益；
- 有自己的目标；
- 会主动行动；
- 会拒绝玩家；
- 可以误解玩家；
- 可以改变关系；
- 玩家不在场时仍会继续生活。

不能成为玩家奖励器或历史剧情触发器。

## 12.2 Player Character 模式

玩家接管历史人物后：

```text
T0 前：既成事实成立
T0 后：关键主动选择归玩家
```

系统可继续模拟：

- 环境；
- 他人反应；
- 身体无法完全控制的反应；
- 行动结果。

不得替玩家决定：

- 站队；
- 忠诚；
- 爱恨；
- 婚恋选择；
- 背叛；
- 原谅；
- 牺牲；
- 政治路线；
- 人生目标。

## 12.3 双用途卡

同一张卡可以支持 NPC 与玩家接管。

不需要生产“NPC 曹操”和“玩家曹操”两张卡。

---

# 13. Historical Baseline Resolver Handoff 规范

## 13.1 Handoff 不是年表

Handoff 只告诉 Resolver：

> 应怎样确认这个人的身份，以及 T0 需要恢复哪些类别的历史状态。

## 13.2 推荐最小内容

```text
身份：
- 规范姓名
- 字／号
- 籍贯／家族等消歧锚点
- 出生年份／范围／争议

T0 查询：
- 是否已出生
- 是否仍可作为活跃人物实例化
- 当前合理身份／官职
- 当前政治归属
- 当前区域／可确认位置
- T0 前主要已发生经历
- 已建立的重要关系
- 婚姻／家庭状态
- 当前合理知识
- 公开声望

规则：
- 区分已确认／争议／推断／未知
- 禁止把 T0 后历史作为当前事实

Capability Bootstrap：
- 恢复截至 T0 已发生的训练、军政、治理、学术等相关经历
- 保留来源与证据强度
- 不从后世游戏数值或流行人物排名直接生成五维 / 技能等级
- 由《人物能力与技艺》统一生成 Capability Profile Candidate
```

## 13.3 Resolver 结果不是直接世界写入

流程必须是：

```text
联网资料
→ 模型综合
→ Historical Snapshot Candidate
→ 冲突处理 / 验证
→ Bootstrap 锁定
→ Game State
```

不能：

```text
搜索结果
→ 直接修改世界
```

## 13.4 网络不可用

未来 Runtime 应失败关闭或使用已经缓存并明确版本化的可靠历史资料。

不得让模型凭记忆假装已经联网确认。

---

# 14. Obsidian 正式 Character Card 默认模板

> [!note]
> 下列 Frontmatter 只是当前 Obsidian 人工管理元数据，不是未来 `tavern-asset-spec` Schema。

```markdown
---
title: 人物名
aliases: []
type: character-card
asset_family: 汉末三国：天下未定
historical_character: true
birth_year: 未确认
status: candidate
research_note: "[[人物名_历史人物研究附录]]"
capability_expansion: "[[汉末三国_人物能力与技艺_Expansion_Pack_v0.1]]"
creator_binding: pending
asset_spec_binding: pending
---

# 人物名｜Character Card

## 1. 身份锚点

- 规范姓名：
- 字 / 号 / 常用称呼：
- 出生年份 / 范围 / 争议：
- 籍贯与基础出身：
- 身份消歧：
- 一句话辨识：

## 2. 人格核心

- 核心价值 / 倾向：
- 核心矛盾：
- 风险偏好：
- 压力下的变化：
- 长期改变需要什么：

## 3. 能力与局限

> 本节只写稳定语义轮廓，不填写五维数值或正式技能等级；它是 Capability Bootstrap 的证据输入。

- 主要长处：
- 重要经验：
- 局限：
- 典型误判风险：

## 4. 决策与行为逻辑

- 优先保护：
- 主要权衡顺序：
- 合作条件：
- 拒绝条件：
- 面对失败 / 威胁 / 背叛：
- 什么真正能改变其判断：

## 5. 关系风格与自主性

- 信任如何建立：
- 对亲族 / 主从 / 同僚 / 竞争者：
- 私情与利益如何权衡：
- 关系破裂条件：
- 玩家不在场时的主动性：
- 不会因为玩家是主角而自动：

## 6. 语言与表现

- 表达风格：
- 公私场合差异：
- 情绪表现：
- 可选风格示例：0–3 条

## 7. Player Character 接管说明

- T0 前锁定：
- T0 后交给玩家：
- 系统不得替玩家决定：

## 8. Historical Baseline Resolver Handoff

- 身份锚点：
- T0 需要解析：
- Capability Bootstrap 需要恢复的相关训练 / 经历 / 职责证据：
- 已知重点争议：
- 未来污染禁令：不得把 T0 后现实历史写成当前人物事实。
- 能力污染禁令：不得直接套用后世游戏五维、武力排名或网络人物数值。

## 可选｜极简史料备注

仅保留会直接影响人物解释或身份消歧的少量警告。
```

---

# 15. Obsidian Historical Character Research Note 模板

```markdown
---
title: 人物名｜历史人物研究附录
aliases: []
type: historical-character-research-note
asset_family: 汉末三国：天下未定
character_card: "[[人物名]]"
status: working
runtime_asset: false
---

# 人物名｜历史人物研究附录

> 本文件是创作研究资料，不是 Character Card，不默认进入 Runtime。

## 1. 研究目标

## 2. 身份与基础事实

## 3. 主要资料来源

## 4. 行为证据库

| 证据 | 来源 | 可支持什么 | 不足以证明什么 |
|---|---|---|---|

## 5. 史料冲突与争议

| 议题 | 说法 A | 说法 B | 当前处理 | 是否影响正式卡 |
|---|---|---|---|---|

## 6. 人格推断链

### 推断 1

历史证据：

中层判断：

最终进入 Character Card 的表达：

不应扩大成：

## 7. 正史 / 文学 / 大众形象差异

## 8. 创作补全与留白

## 9. 被正式卡舍弃的细节

## 10. Resolver 重点提醒

## 11. 待核查事项

## 12. 修订记录
```

---

# 16. 单张人物卡生产流程 v0.2

## CC0｜Scope Lock

确认：

- 正在生产哪个人物；
- NPC / 玩家 / 双用途；
- 是否属于真实历史人物；
- 是否需要独立 Research Note。

退出条件：人物身份明确。

## CC1｜研究与证据恢复

对核心人物：

1. 建立或更新 Research Note；
2. 收集稳定身份事实；
3. 收集少量高解释力行为证据；
4. 区分史实、争议、人格推断、文学传统、创作补全；
5. 不追求复制完整传记。

退出条件：足以支撑人物核心结构。

## CC2｜稳定 / 时间依赖分离

把研究结果分为：

### Stable Definition

进入 Character Card 候选。

### T0-dependent

交给 Resolver。

### World-level

回到 World Pack。

### Mechanic

交给 Expansion Pack。

### Current State

只能进入 Game State。

退出条件：不存在明显 Owner 混乱。

## CC3｜高密度压缩

先写完整理解，再压缩成正式 8 章节。

压缩时：

- 合并同义人格；
- 删除年表；
- 删除重复史料；
- 删除不能改变运行判断的细节；
- 删除大量场景例子；
- 把详细依据移动到 Research Note。

退出条件：卡片达到长度与信息密度目标。

## CC4｜决策结构审核

检查人物是否能够根据新情境生成行为，而不是只会复现历史。

至少回答：

- 什么最重要；
- 怎样权衡；
- 什么会改变判断；
- 什么不会因为玩家身份而自动改变。

## CC5｜玩家 / NPC 边界

检查：

- NPC 自主性；
- 玩家接管代理权；
- 关系不自动双向；
- 恋爱不预设。

## CC6｜Resolver Handoff

建立最小身份锚点和 T0 查询范围。

不得把详细年表搬入 Handoff。

## CC7｜最终压缩

重新计算大致中文长度。

如果超过约 4000 字：

1. 查找传记化内容；
2. 查找研究论证；
3. 查找历史状态；
4. 查找重复人格；
5. 查找过量台词；
6. 把非 Runtime 必需内容外移。

## CC8｜质量 Gate

全部 Gate 通过后才进入候选资产状态。

---

# 17. Character Card 质量 Gate v0.2

## HC0｜身份与来源 Gate

通过条件：

- 人物身份可确认；
- 事实与推断分开；
- 重要争议不被伪装成确定事实。

## HC1｜Ownership Gate

通过条件：

- 世界历史未被复制进人物卡；
- 动态机制未写进人物卡；
- 当前状态未被固定为 Definition。

## HC2｜Runtime Density Gate

通过条件：

- 正文以高解释力信息为主；
- 没有大段人物传记；
- 没有大段史料论证；
- 没有大量与运行无关的细节。

## HC3｜Length Gate

通过条件：

- 长度与人物复杂度匹配；
- 超过约 4000 中文字时已有明确必要性说明；
- 不为追求统一长度补写虚构内容。

## HC4｜Decision Generativity Gate

通过条件：

> 人物面对历史上没有发生过的新问题时，模型仍能依据该卡推导合理行为。

如果只能复现几个历史事件，则失败。

## HC5｜Future Contamination Gate

通过条件：

- 没有把 T0 后现实历史写成必然未来；
- 没有后见之明；
- 没有史书全知。

## HC6｜Player Agency Gate

通过条件：

- 玩家接管后关键选择归玩家；
- 不以历史结果锁定玩家未来。

## HC7｜NPC Autonomy Gate

通过条件：

- NPC 有自己的利益和判断；
- 不自动信任、爱慕、服从、原谅或等待玩家。

## HC8｜Information Boundary Gate

通过条件：

- Character Definition 与 T0 知识分开；
- 私密信息不会自动变成玩家知识；
- Research Note 不默认进入玩家或 Runtime 上下文。

## HC9｜Research Separation Gate

通过条件：

- 详细史料、争议与推断依据已经移到 Research Note；
- Character Card 不需要读取 Research Note 才能理解人物核心；
- Research Note 不成为第二 Character Definition。

## HC10｜Resolver Ready Gate

通过条件：

- 有足够身份消歧信息；
- Resolver 查询范围清楚；
- 不依赖人物卡内置年代快照。

## HC11｜Definition / Instance Gate

通过条件：

- Character Card = Definition；
- Historical Snapshot = Bootstrap；
- Current Character State = Game State。

三层没有混写。

---

# 18. 压缩检查表

正式发布候选前逐项检查：

- [ ] 是否有超过 150 字、但本质只是人物传记的段落？
- [ ] 是否重复解释了同一个人格特征？
- [ ] 是否存在可以移动到 Research Note 的证据和论证？
- [ ] 是否写了 Resolver 本来可以恢复的 T0 历史状态？
- [ ] 是否列了太多历史事件，只为证明人物“经历丰富”？
- [ ] 是否有超过 3 条示例台词？
- [ ] 是否有“所有著名优点都写上”的全能化倾向？
- [ ] 是否有后世标签直接变成人格事实？
- [ ] 是否有具体当前关系、婚姻、官职或位置？
- [ ] 是否有任何内容删除后不会影响模型对人物的判断？

如果最后一项答案为“有”，优先删除或移动到 Research Note。

---

# 19. 典型反模式

## 19.1 人物百科卡

错误：

> 从出生写到死亡，按年列出全部官职、战争、迁徙和家族事件。

修正：

> 正式卡只保留稳定 Character Definition；生涯研究进 Research Note；T0 当前状态交给 Resolver。

## 19.2 研究论文卡

错误：

> 每个人格判断后附几百字史料辩论。

修正：

> 卡中写结论；证据链进 Research Note。

## 19.3 标签卡

错误：

> 雄才大略、多疑、奸雄、爱才、残酷、浪漫。

修正：

> 把标签转换为可在新情境中运行的决策规则。

## 19.4 历史剧本卡

错误：

> 角色在 208 年必然南征，随后必然发生赤壁。

修正：

> T0 后行为由当前局势和角色判断产生。

## 19.5 台词宏卡

错误：

> 收录十几条名言并要求角色频繁引用。

修正：

> 只保留语言风格，必要时少量示例。

## 19.6 全能名人卡

错误：

> 因为人物著名，所以政治、战争、文学、社交、识人、治理全部顶级。

修正：

> 只记录有支持的长处，并保留真实局限。

## 19.7 Research Note 偷偷进入 Runtime

错误：

> 为了让模型“更懂曹操”，每次对话都加载完整研究附录。

修正：

> Runtime 默认只加载正式 Character Card + 当前 Game State + 当前相关 Context。

---

# 20. Runtime Requirements Ledger 增量

## R-HIST-01｜Historical Baseline Resolver

需要一个受控流程，根据：

- Character Card 身份锚点；
- World Pack；
- T0；
- 历史资料政策；

生成 Historical Snapshot Candidate。

## R-HIST-02｜Bootstrap Snapshot Lock

验证后的快照必须锁入 Game Instance。

Save / Restore 恢复锁定结果，不重新联网生成过去。

## R-HIST-03｜T0 Future Filter

Historical Resolver 必须防止：

- T0 后历史事件；
- 人物未来死亡；
- 后续官职；
- 后来的关系；
- 后世评价；

污染 T0 当前状态。

## R-HIST-04｜Research Note 非 Runtime 资产

Game Runtime 不应默认把 Historical Character Research Note 作为正式资产加载。

如果未来提供开发诊断引用，也必须与普通角色上下文隔离。

## R-HIST-05｜失败关闭

网络、来源或身份无法可靠确认时：

- 保留未知；
- 请求用户裁定；或
- 使用明确版本的可信缓存。

不得假装确认。

---

# 21. asset-spec vNext Requirements Ledger 增量

以下只是未来需求，不是当前字段设计。

## AS-HIST-01｜轻量 Character Definition

未来 Character Card 格式应允许保存短小稳定 Definition，而不要求嵌入完整生涯年表。

## AS-HIST-02｜最小时间元数据

至少需要考虑出生年份／范围／未知的表达需求。

死亡年份是否需要进入最小元数据，留待 G9 根据真实实例化与筛选需求决定。

## AS-HIST-03｜Historical Resolver Handoff

需要一种受控方式表达：

- 历史人物身份消歧；
- Resolver 是否适用；
- T0 需要解析哪些类别。

当前不冻结字段。

## AS-HIST-04｜Research Note 不应被误认成 Character Asset

如果未来 Creator 能关联研究资料，协议应明确：

> Research Note 是创作元资料，不是正式角色定义或 Game Asset。

## AS-HIST-05｜不要求多年代复制卡

协议不能迫使创作者为每个开局年代复制同一个人物 Definition。

---

# 22. Creator Requirements Ledger 增量

## C-HIST-01｜高密度人物卡编辑视图

Creator 应帮助创作者专注：

- 人格核心；
- 决策逻辑；
- 自主性；
- Resolver Handoff。

而不是诱导填写巨大人物百科表单。

## C-HIST-02｜Research Note 独立工作区

Creator 可允许：

- 关联人物研究资料；
- 查看来源；
- 查看争议；
- AI 辅助从研究资料压缩 Character Card。

但需要清晰标识：

> Research Note 不会默认进入 Runtime Asset。

## C-HIST-03｜长度与密度提示

Creator 可以提示：

- 当前字数；
- 重复信息；
- 疑似年表内容；
- 疑似研究论证；
- 疑似 T0 状态；
- 可移动到 Research Note 的内容。

不应把字数限制做成机械硬裁剪。

## C-HIST-04｜T0 历史预览

未来可以让创作者选择一个年代，预览 Resolver 生成的实例化候选，但预览不是 Character Card 本体。

---

# 23. UI Host Requirements Ledger 增量

## UI-HIST-01｜普通游戏只消费玩家安全人物投影

Research Note 和后台 Character Definition 私密内容不能因为存在于资产库就全部发送到客户端。

## UI-HIST-02｜历史资料查看与角色资料分离

如果未来提供“历史资料”功能，应与：

- 当前人物资料；
- 玩家角色知识；
- Game State；

清晰区分。

---

# 24. v0.1 → v0.2 迁移规则

如果已经存在按 v0.1 写出的 Character Card：

## Step 1｜保留原文作为创作资料

不要直接删除。

## Step 2｜识别四类内容

### A. Runtime Stable Definition

压缩进入 v0.2 Character Card。

### B. 史料证据 / 人格论证

移动到 Historical Character Research Note。

### C. T0-dependent 历史状态

从卡中删除，登记 Resolver Handoff。

### D. World / Mechanic / Current State

交还正确 Owner。

## Step 3｜压缩成 8 个核心章节

## Step 4｜运行 HC0–HC11

## Step 5｜旧 v0.1 保持历史版本，不作为新 Runtime 默认资产

---

# 25. 首批人物生产策略

正式人物生产建议采用两阶段试制，而不是立刻批量做几十张。

## 第一阶段｜压力测试人物

优先选择：

- 时间跨度长；
- 史料丰富；
- 人格复杂；
- NPC / 玩家双用途价值高；
- 可以充分测试压缩规范。

目的不是尽快扩充人物数量，而是验证：

> **一张约 2000–3500 字的高密度卡，是否足以让复杂历史人物稳定运行。**

## 第二阶段｜不同类型人物

再各选：

- 文臣；
- 武将；
- 女性人物；
- 史料较少人物；
- 后期人物。

检查同一模板是否会过度偏向诸侯型人物。

## 批量生产 Gate

只有至少数张不同类型人物卡证明：

- 长度合理；
- 人物区分度足够；
- Resolver Handoff 可用；
- 不需要研究附录才能运行；
- 玩家接管与 NPC 自主性没有冲突；

才开始大规模人物库生产。

---

# 26. 当前审核

## G-OWNERSHIP｜通过

正式人物卡、Research Note、Historical Snapshot 与 Game State 已分离。

## G-DENSITY｜通过设计审核

新增明确长度预算和压缩 Gate。

实际效果需首批人物卡验证。

## G-SOURCE｜通过

详细证据转入 Research Note；正式卡仍保留必要争议提醒。

## G-AGENCY｜通过

玩家接管后 T0 后选择不受现实历史强制。

## G-AUTONOMY｜通过

人物卡强调生成式决策与 NPC 自主性，而非剧情脚本。

## G-INFORMATION｜通过

Research Note、Character Definition、Historical Snapshot、玩家知识与 Game State 不混同。

## G-DEFINITION｜通过

Character Definition 与实例状态边界清楚。

## G-RUNTIME｜通过

联网结果仍需 Resolver → Validation → Bootstrap，不直接修改世界。

## G-CREATOR｜待未来绑定

仅登记产品需求，不猜 Creator 机器实现。

## G-SPEC｜待未来绑定

不生成 asset-spec 字段、ID、Ref 或 enum。

---

# 27. 当前状态与下一步

本规范当前状态：

> **候选 v0.2**

如果用户确认本规范，后续历史人物 Character Card 统一按 v0.2 生产。

首张压力测试人物建议仍选择复杂核心人物，用于验证：

1. 2000–3500 字目标是否合理；
2. 8 章节是否足够；
3. Research Note 与 Character Card 的分离是否自然；
4. Resolver Handoff 是否精简且可用；
5. 模型是否能凭 Character Definition + T0 Snapshot 推演历史上未发生的新情境。

首张卡通过后，再决定是否需要进一步把长度目标、模板和 Gate 写回 `tavern-asset` Skill 的下一版本。

---

# 28. 变更记录

## v0.2｜2026-08-15

相对 v0.1：

1. 将 Character Card 明确收口为高密度 Runtime Character Definition；
2. 新增独立 Historical Character Research Note；
3. 把详细史料、争议、人格推断链从正式卡迁出；
4. 默认主体从 14 个章节压缩为 8 个核心章节；
5. 新增人物卡长度预算与约 4000 中文字超长警戒线；
6. 新增 Runtime Density Gate、Length Gate、Research Separation Gate；
7. 删除正式卡中重复的 Scope、依赖、审核等大段流程性正文要求；
8. Resolver Handoff 收口为身份锚点 + T0 查询范围；
9. 明确 Research Note 不默认进入 Runtime；
10. 新增 v0.1 → v0.2 迁移规则；
11. 新增首批试制后再批量生产的 Gate。

## v0.1｜2026-08-15

首次建立：

- 一人一卡；
- 稳定 Definition；
- Historical Baseline Resolver；
- T0 历史边界；
- 玩家接管代理权；
- 史实 / 推断 / 文学 / 创作分层。

---

# v0.2.1 修订说明｜人物能力机制接入

本次不改变“高密度 Runtime Character Definition”主体。

新增边界：

1. Character Card 的“能力与局限”是稳定语义证据，不是正式 Capability Profile；
2. 五维、技能等级、经历与专长的 Runtime 状态统一由《人物能力与技艺》管理；
3. Historical Baseline Resolver 除恢复生涯事实外，还需提供截至 T0 的训练、职责、战争、治理等能力证据；
4. Research Note 可以保存能力推断证据，但不得直接把历史评价翻译成固定五维数值；
5. 后续人物卡禁止从《三国志》游戏、网络排名、演义强弱榜直接导入能力值。
