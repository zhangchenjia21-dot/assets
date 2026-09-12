# MD-001U1｜G1 Gateway Micro-District + Middle Architecture Kit v0.1

状态：**AUTHORIZED / DISPATCH READY**
日期：2026-09-12

## 0. 任务定位

本任务取代原计划中的“G1 首栋单建筑 Architecture Design”。

根据 D-028：

> **G1 这类高密区域以微街区 / 建筑组团作为 Architecture Design unit。**

本轮必须同时完成：

1. G1 内一个可审核的 **Gateway Micro-District / Urban Ensemble**；
2. CIV-001 **Middle Regional Architecture Kit v0.1**。

本轮只设计、预览、校验和沉淀 reusable rules。

`world writes = 0`。

---

## 1. 必读资料

至少读取：

1. `minecraft/建筑师/current/项目状态.md`
2. `minecraft/建筑师/decisions/D-028_高密区域以微街区为作业单元并建立文明地域ArchitectureKit.md`
3. `minecraft/建筑师/decisions/D-027_MD-001P-R1总规Owner接受并进入G1首栋SiteGate.md`
4. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/`
5. `minecraft/建筑师/research/build-sites/CIV-001/MD-001S1/`
6. `minecraft/建筑师/tasks/MD-001S1/COMPLETION.md`
7. `minecraft/建筑师/world/civilizations/CIV-001/README.md`
8. `minecraft/建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md`
9. 当前 `minecraft-builder` Skill。

MD-001S1 的 S1 / S2 / S3 是**局部现状证据**，不是必须照用的单建筑地块。

---

## 2. 当前锁定基线

继续锁定：

- revision 154 territory；
- Middle = 391,002；
- P1 = 13,661；
- G1 = 7,175；
- political threshold = 2,077 / zero building footprint；
- G1 through-clearance overlay = 1,451；
- Alliance Commons 不可侵入；
- N1 仍为 Middle principal hub；
- G1 是 specialized gateway secondary community。

MD-001S1 已知当前世界 evidence：

- S1 = 570 gross columns，Y66–67；
- S2 = 586；
- S3 = 605；
- 当前 G1 与旧 cache 仅发现极小表层差异；
- 候选浅层地下未见已识别重大冲突；
- 具体饮水、深层地下、实际建筑入口等仍需在设计 / pre-build 阶段继续约束。

不要把 S1 的 570 格当作本任务微街区的面积上限。

---

## 3. Task A｜确定一个微街区 Design Envelope

### 目标

在 G1 内确定一个**比单栋 Site 更大、但明显小于整个 G1**的 coherent micro-district envelope。

它必须：

- 使用当前世界证据；
- 至少包含多个独立建筑体量的空间能力；
- 同时容纳街巷 / 共享院 / 服务和日常生活关系；
- 与 G1 → N1 的通行链协调；
- 不堵 political threshold；
- 不占 through-clearance；
- 不向 Commons 或 N1 借地；
- 服从真实地形、植被、排水和现有内容。

### 方法

- 优先复用 MD-001S1 current-world snapshot；
- 若局部 evidence 对微街区范围不足，只允许 Just-in-time read-only 扩展；
- 若发现快照相对当前存档已经失效，必须先刷新最小必要局部证据并保留 lineage；
- 不 broad rescan。

S1 可作为 anchor pocket，但不是强制中心；若 S1 + 邻近空间不适合形成 coherent block，可以选择更合理的 G1 组合范围。

### 输出

至少给出：

- exact design envelope；
- gross area；
- terrain / vegetation / artificial-content / subsurface summary；
- 与 through-clearance、R1a/R1b、G1 边缘的关系；
- 为什么它适合作为一个“微街区”而非单栋场地。

---

## 4. Task B｜G1 Gateway Urban Ensemble

### 设计对象

设计一个完整、可增长的门户微街区。

必须是：

> **多个独立建筑体量 + 共同街巷 / 院落 / 服务空间的整体。**

不得把所有功能塞进一栋 mega-building 来假装“组团”。

### 功能池

根据总体规划与实际场地选择组合，不要求每项都独立成一栋：

- 共享周转 / 短仓；
- 经营家庭住家；
- 食物 / 日用品铺面；
- 小型旅宿 / 饮食；
- 修理 / 工匠；
- 驮运短停 / 装卸；
- 消息 / 向导 / 告示；
- 小公共服务；
- 储水 / 消防 / 污物与维护空间。

### 空间要求

整体设计至少解决：

- main pedestrian / pack-animal approach；
- resident entrance；
- service / loading circulation；
- shared court；
- narrow lanes / passages；
- street edge；
- building-to-building spacing；
- corner / end condition；
- terrain step / drainage；
- fire / maintenance access；
- future growth interfaces。

### 设计表达

复杂组团必须遵守：

> **Plan + Section + Sequence**

至少输出：

- 总平面；
- 至少 2 条关键剖面；
- 主要行走 / 货物流线；
- 建筑角色图；
- 屋顶 / skyline 图；
- 分期生长图；
- 玩家视角 / 3D preview。

不要求一次设计整个 G1。

---

## 5. Task C｜Middle Regional Architecture Kit v0.1

### 目的

把 AB-001 的抽象 Grammar 转化成 Codex 以后可以**直接复用**的 Middle 建筑设计系统。

目录建议：

`minecraft/建筑师/architecture/civilizations/CIV-001/kits/MIDDLE/v0.1/`

至少包含：

```text
README.md
KIT.md
KIT.json
typologies.json
modules.json
palette-families.json
variation-rules.json
forbidden-combinations.md
```

### Kit 层级

明确区分：

#### CIV-001 Shared DNA

记录 Middle 与 West / East 仍应共享的文明建造亲缘。

#### Middle Regional DNA

落实 Middle 的：

- stone base + timber upper；
- 高土地价值 / 高混合使用；
- 仓储、商住、旅宿、加工与院落关系；
- 紧凑街巷与共享院；
- shore → lowland → foothill 的转换建筑逻辑。

### Kit 内容

至少具体化：

- foundation / plinth / wall systems；
- structural bay habits；
- floor-to-floor ranges；
- roof families / roof pitch / gable rules；
- facade rhythm；
- opening hierarchy；
- window / door / warehouse-door families；
- stairs / porch / canopy / balcony / arcade modules；
- courtyard wall / gate / service-yard modules；
- corner / party-wall / end-wall conditions；
- palette families；
- street-edge rules；
- drainage / terrain-step patterns；
- signage / small details；
- regional forbidden combinations。

### Typology templates

至少形成若干可复用 typology skeleton，例如：

- mixed shop-house；
- short-storage + residence；
- repair/workshop house；
- inn/food house；
- small public / record-service house；
- courtyard/service compound。

数量由实际设计需要决定，不为了凑数生成。

### Template 原则

模板必须保存：

- required core；
- optional modules；
- variation knobs；
- allowed dimension / proportion ranges；
- terrain adaptation options；
- incompatible combinations。

禁止把模板定义成一栋固定建筑的逐方块复制件。

如果已有 Blueprint / Litematica 基础设施适合，可在本地生成 module prototype；GitHub 默认保存轻量规则 / schema / preview，不为此上传巨大 binary。

### 成熟度标记

v0.1 中的每个规则 / 模块必须标记：

- `PROPOSED`
- `PREVIEW_VALIDATED`
- `BUILT_AND_OWNER_ACCEPTED`

本轮最多到 `PREVIEW_VALIDATED`。

后续真实建成并通过 Owner review 后，才允许升级为 proven pattern。

---

## 6. Style Consistency ≠ Repetition

Architect / Critic 必须同时检查：

### 一致性

玩家应明显读出：

> 这些建筑由同一个 Middle 社会、同一套施工传统、相近工匠体系建成。

### 变化

又必须避免：

- 同宽同高；
- 同一屋顶复制；
- 同一窗洞节奏；
- 每栋完全同 palette；
- 同样的门廊 / 山墙 / 转角；
- 机械镜像；
- prefab suburb 感。

变化应来自：

- 功能；
- 建造年代 / 扩建痕迹；
- 地块形状；
- terrain；
- 街道位置；
- 建筑等级；
- owner / craft variation。

目标是：

> **family resemblance, not clones。**

---

## 7. Multi-building Functional QA

本轮 Critic 必须检查：

- 是否出现 stairs-to-wall / blocked doors；
- 是否所有楼层可达；
- 建筑之间是否形成死巷 / 无意义缝隙；
- 装卸是否堵住全天居民通行；
- 生活与危险工序是否冲突；
- 院落是否有真实功能；
- 雨水是否被建筑组团围成死洼；
- 建筑是否越过 G1 / clearance / threshold；
- 是否误读成海关、收费门城或边防设施；
- 是否为追求统一而无视 terrain；
- 是否为了“密集”删除必要消防 / 维护 / 日照与公共空隙。

---

## 8. Deliverables

### Urban Ensemble

写入建议：

`minecraft/建筑师/planning/CIV-001/MIDDLE/G1/MD-001U1/`

至少：

```text
README.md
URBAN-ENSEMBLE.md
URBAN-ENSEMBLE.json
site-envelope.json
building-roles.json
circulation.json
phasing.json
validation/
visual/
```

### Architecture Kit

写入：

`minecraft/建筑师/architecture/civilizations/CIV-001/kits/MIDDLE/v0.1/`

按第 5 节交付。

### Preview

至少提供能审核：

- top plan；
- 2 sections；
- 3–6 个玩家视角 / 斜视图；
- roof / skyline；
- kit / module overview。

---

## 9. 本轮禁止

- `world writes`；
- 修改 revision 154；
- 修改 MD-001P-R1 总体规划；
- 侵入 Commons；
- 占 political threshold；
- 占 through-clearance；
- 一次设计整个 G1；
- 直接开始施工；
- 把 v0.1 模板声称为 built/proven；
- 用复制粘贴建筑代替地域一致性。

`world writes = 0`。

---

## 10. Completion / Stop

完成后：

- 写 `minecraft/建筑师/tasks/MD-001U1/COMPLETION.md`；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT + Owner 审核。

若通过，下一阶段才创建 bounded multi-building build task，并按 D-028 将同一微街区分批 world-write。
