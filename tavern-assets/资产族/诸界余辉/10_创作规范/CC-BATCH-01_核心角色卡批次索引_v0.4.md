---
title: CC-BATCH-01｜核心角色卡批次索引
created: 2026-08-16
updated: 2026-08-16
status: audited-current
version: 0.4
workflow_mode: asset-family
operation_mode: revise
asset_type: character-batch-index
skill: tavern-asset v0.5.2
output_profile: obsidian-markdown
asset_family: 诸界余辉
blueprint: "[[诸界余辉_资产组合总蓝图_v0.11]]"
world_pack: "[[埃瑟维亚_诸界余辉_World_Pack_v0.1.3]]"
language: zh-CN
---

# CC-BATCH-01｜核心角色卡批次索引 v0.4

> [!success] 当前状态
> **10 / 10 Character Personality / Ownership / Dependency / Combat Binding 总审核 PASS。**
>
> 本索引根据当前实际交付的 10 张 Character Card 重建并收口，不恢复任何旧 v0.1 人格版本。

# 1. Roster

| ID | 人物 | 版本 | 种族 | 核心定位 | 尺度 | Priority | Complexity | Hard Dependency 摘要 | 当前接口状态 |
|---|---|---|---|---|---|---|---|---|---|
| CC-01 | 莉维娅·塞兰 | v0.2 | 人类 | 学院正式法师 | 中层精英 | S | 核心复杂 | EP-CHAR-CORE + EP-MAGIC-CORE | 无 Combat / Health Hard Dependency |
| CC-02 | 阿德里安·维尔克 | v0.3 | 人类 | 魔剑士 | 中层精英 | A | 中高复杂 | EP-CHAR-CORE + EP-COMBAT-CORE + EP-MAGIC-CORE + EP-MAGIC-COMBAT | Combat Binding PASS |
| CC-03 | 杜恩·石痕 | v0.3 | 赫姆拉 | 魔弓手 / 魔猎者 | 普通成熟职业者 | A | 中等 | EP-CHAR-CORE + EP-COMBAT-CORE + EP-MAGIC-CORE + EP-MAGIC-COMBAT | Combat Binding PASS |
| CC-04 | 塞芙琳·凯铎 | v0.3 | 人类 | 传奇敌法者 | 传奇人物 | S | 核心复杂 | EP-CHAR-CORE + EP-COMBAT-CORE + EP-MAGIC-CORE + EP-MAGIC-COMBAT | Combat Binding PASS |
| CC-05 | 艾蕾娜·瓦尔德 | v0.3 | 人类 | 圣骑士 | 高层人物 | S | 核心复杂 | EP-CHAR-CORE + EP-COMBAT-CORE + EP-DIVINE-CORE | Combat Binding PASS |
| CC-06 | 塔维尔·伊瑟恩 | v0.3 | 瑟林 | 审判官 | 中层精英 | A | 中高复杂 | EP-CHAR-CORE + EP-COMBAT-CORE + EP-DIVINE-CORE | Combat Binding PASS |
| CC-07 | 玛芮娅·科岚 | v0.2 | 人类 | 祭司 / 圣所主持者 | 高层人物 | A | 核心复杂 | EP-CHAR-CORE + EP-DIVINE-CORE | 无 Combat / Health Hard Dependency |
| CC-08 | 弥珂·第七弦 | v0.2 | 灵造民 | 神医 | 中层精英 | A | 中高复杂 | EP-CHAR-CORE + EP-DIVINE-CORE | Health Optional Integration |
| CC-09 | 罗塔·铜誓 | v0.2 | 灵造民 | 非施法公共工程组织者 | 普通成熟职业者 | A | 中等 | EP-CHAR-CORE | 无 Magic / Divine / Combat / Health Hard Dependency |
| CC-10 | 赛芮雅·维恩 | v0.2 | 界裔 | 第五神遗迹研究者 / 异常 Covenant | 高层 / 特殊专业权威 | S | 核心复杂 | EP-CHAR-CORE + EP-MAGIC-CORE + EP-DIVINE-CORE | 无 Combat / Health Hard Dependency |


# 2. Character Personality Distinctiveness Closure

当前 10 张角色的人格差异继续冻结：

- **CC-01 莉维娅**：学术野心、竞争欲、理论优越感；害怕只被记住为事故后的安全负责人。
- **CC-02 阿德里安**：骄傲、贵族身份意识、对怜悯敏感；否认但实际需要家族认可。
- **CC-03 杜恩**：边境猎人、重同伴、迷信、记仇、反征编；熟悉地形时容易过度自信。
- **CC-04 塞芙琳**：安全与控制优先；支持部分灾难级施法者强制登记 / 训练 / 监管。
- **CC-05 艾蕾娜**：真正虔诚的传统主义圣骑士；重誓约、圣秩、神圣传统，对合法宗教权威有初始信任。
- **CC-06 塔维尔**：长生种式程序保守主义；重档案 / 先例；对年轻人的情绪证词有真实偏见。
- **CC-07 玛芮娅**：共同体与关系驱动；非常关心他人；容易发展为家长主义与“替人照顾过头”。
- **CC-08 弥珂**：身体自主、自我定义、私人体验；可能低估有机生命对身体连续性的身份意义。
- **CC-09 罗塔**：野心、控制欲、商业现实主义；支持人格权不代表劳动 / 合同政策温和。
- **CC-10 赛芮雅**：研究纪律 + 对边界 / 第五神的危险浪漫主义；会主动承担普通研究者不愿承担的风险。

World OS / Runtime 安全规则不作为 NPC 人格模板。

# 3. Combat Binding Closure

Hard Depend `EP-COMBAT-CORE`：

| ID | Combat Skill |
|---|---|
| CC-02 | 近战兵器：卓越；战术判断：精通 |
| CC-03 | 远程兵器：卓越；战术判断：熟练 |
| CC-04 | 近战兵器：精通；战术判断：顶尖 |
| CC-05 | 近战兵器：卓越；战术判断：精通 |
| CC-06 | 战术判断：精通 |

CC-01 / 07 / 08 / 09 / 10 不因为“世界可能发生战斗”机械增加 Combat Hard Dependency。

具体长剑 / 弓等继续由 Specialty / Experience / Weapon Profile 表达，不建立第二套武器 Skill Owner。

# 4. Health Core Binding Closure

`EP-HEALTH-CORE v0.1` 已存在，但 10 张当前卡都没有需要写入 Character Definition 的稳定开局 Health Condition。

因此：

> **10 张卡均不因为“未来可能受伤 / 生病 / 被治疗”机械 Hard Depend Health Core。**

实际游戏中：

- Combat Impact；
- Magic Backlash；
- Divine Treatment；
- 事故 / 疾病 / 中毒；

若形成 Persistent Health State，由 Runtime 通过 `EP-HEALTH-CORE` 处理。

未来如果某张 Character Card 增加慢性病、稳定残疾、开局康复或长期身体改造等定义，再单独增加 Health Hard Dependency。

# 5. Relationship Registry｜15 条唯一历史关系边

| # | A | B | 既往关系 |
|---:|---|---|---|
| 1 | CC-01 | CC-04 | 闭门技术会面；对反魔法与国家监管存在分歧 |
| 2 | CC-01 | CC-06 | 基础术式事故证据格式交流 |
| 3 | CC-01 | CC-07 | 基础术式安全 / 公共教学合作 |
| 4 | CC-01 | CC-10 | 共同参加受许可遗迹考察 |
| 5 | CC-02 | CC-03 | 跨境护送短期合作 |
| 6 | CC-02 | CC-04 | 联合演练中被塞芙琳击败并重构训练 |
| 7 | CC-03 | CC-09 | 长期路线勘察 / 护卫合作 |
| 8 | CC-03 | CC-10 | 危险区域向导合作 |
| 9 | CC-04 | CC-06 | 跨体系反制训练与考核 |
| 10 | CC-05 | CC-06 | 长期神术 / 调查体系共事 |
| 11 | CC-05 | CC-07 | 重大灾害救援协作 |
| 12 | CC-05 | CC-08 | 人格 / Covenant 争议中的安全保护 |
| 13 | CC-07 | CC-08 | 长期医学 / 神术专业交流 |
| 14 | CC-08 | CC-09 | 弥拉泽灵造民公共议题熟人 |
| 15 | CC-09 | CC-10 | 遗迹考察后勤 / 责任合同合作 |


这些关系只冻结：

- 已发生的历史；
- 认识来源；
- 可复用互动钩子。

不冻结：

- 当前好感；
- 当前信任；
- 当前敌意；
- 游戏开始后必须合作 / 冲突。

# 6. Definition / Instance

10 张卡继续保持：

```text
Character Card Definition
→ instantiate
→ Character State
→ Runtime changes
→ Game State
```

游戏中：

- 当前关系；
- 当前 Health；
- 当前位置；
- 当前 Spell / Invocation Mastery；
- Covenant State；
- Magic / Channel Strain；
- 职位；
- 生死状态；

不回写原 Character Card。

# 7. Batch Final Gate

| Gate | 结果 |
|---|---|
| Roster / Version Consistency | PASS |
| Personality Distinctiveness | PASS |
| Ownership | PASS |
| Dependency Minimalization | PASS |
| Combat Binding | PASS |
| Health Binding | PASS |
| Character Knowledge Boundary | PASS |
| Relationship Registry | PASS — 15 edges |
| Program Authority | PASS |
| Definition / Instance | PASS |
| Creator Authorability | WARN — G9 binding pending |
| Pioneer Closure | PASS |

> **CC-BATCH-01 = AUDITED / CLOSED。**
