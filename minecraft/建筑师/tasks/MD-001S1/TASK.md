# MD-001S1｜G1 Shared Turnover & Living Courtyard Local Site Gate

状态：**AUTHORIZED / DISPATCH READY**
日期：2026-09-12

## 0. 任务目标

在已被 Owner 接受的 G1 门户社区内，为中域第一座规划建筑：

> **G1「共享周转与生活院」**

完成一次**真实当前存档 Local Site Gate**。

本任务不是建筑设计任务，也不是施工任务。

`world writes = 0`。

最终只需要：

- 找到 **2–3 个**真实可核验的微型候选 Site；
- 比较它们；
- 推荐 **1 个**优先 Site；
- 停止交 GPT + Owner 审核。

不得直接进入建筑设计。

---

## 1. Authority / Planning Baseline

必须读取：

1. `minecraft/建筑师/current/项目状态.md`
2. `minecraft/建筑师/decisions/D-027_MD-001P-R1总规Owner接受并进入G1首栋SiteGate.md`
3. `minecraft/建筑师/decisions/D-026_P1连接带升级为中域门户聚落并修订MD-001P.md`
4. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/MASTERPLAN.md`
5. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/REVISION-R1.md`
6. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/R1独立审核.md`
7. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/first-build-recommendation.md`
8. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/validation/gateway-evidence.json`
9. `minecraft/建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md`
10. 本 Task Packet。

### 锁定规划事实

- territory revision = **154**；
- Middle Domain = **391,002 blocks²**；
- P1 = **13,661 blocks²**；
- G1 planning envelope = **7,175 blocks²**；
- G1 through-clearance overlay = **1,451 blocks²**；
- political / movement threshold = **2,077 blocks²，零建筑占地**；
- G1 锚点 `[190,1731]` 是交通链上的 planning anchor，**不是建筑位置**；
- N1 principal hub 与其它总规骨架不变。

---

## 2. Current-world Freshness Gate

与此前 masterplan 不同，本轮必须核对**当前真实存档**。

优先使用项目已验证的 current-world / direct-world read-only 能力；若通过 save-level 工具读取，也必须先确认 world identity。

至少记录：

- 存档名称 / identity；
- DataVersion / game version（如可读）；
- 当前世界路径或可复核 identity；
- 本轮读取时间；
- 是否发现与 planning cache 不一致的表层事实。

如果无法确认正在读取的就是目标 `建筑师` 存档：

> 立即停止，状态 `CURRENT_WORLD_IDENTITY_NOT_CONFIRMED`。

不得拿旧 cache 假装完成 Site Gate。

---

## 3. Candidate Search Scope

只允许在：

> **G1 planning envelope 内**

搜索候选 Site。

必须排除：

- political / movement threshold；
- through-clearance overlay；
- shoreline / terrain reserve；
- 已识别人工内容保护范围；
- 明显排水风险 / 洼地；
- 会截断 Commons → G1 → N1 全天通行的区域。

不得因为“场地更平”越出 G1，亦不得向 Alliance Commons 借地。

### 不使用硬编码建筑尺寸

不要先假设一个固定 30×30、45×45 或其它矩形再找地。

Site capacity 应由以下组合判断：

- 共享周转与生活院的功能；
- 中等规模建筑量级；
- 必需院落；
- 装卸 / 短停；
- 居民入口；
- 消防 / 维护；
- 排水；
- G1 紧凑街院的长期生长逻辑。

输出“可承载能力 / gross usable envelope”，不要冻结最终 architecture footprint。

---

## 4. 每个候选必须检查

### A. 表层地形

- 精确 surface Y；
- 局部坡度与 relief；
- 是否需要轻微顺地适配；
- 是否会要求不合理大规模削平 / 填方；
- 玩家视角下是否自然嵌入门户聚落。

### B. 当前人工内容

检查候选及必要缓冲内：

- 玩家 / 既有人工方块；
- 结构；
- 道路 / 小径 / 设施；
- block entities（如可读）；
- 其它不应覆盖的现有内容。

不得把“现有规划图没标人工物”当作当前世界为空。

### C. 浅层地下

至少做与中等建筑基础相关的浅层检查，重点识别：

- 大洞穴 / 空腔；
- 水体；
- 明显人工地下结构；
- 会影响基础与排水的异常。

无需 broad underground survey；只检查候选及其合理缓冲。

### D. 通行 / 物流

必须同时考虑：

- Commons → G1 的主通行；
- G1 → N1 的继续通行；
- 短仓 / 装卸 / 驮运停驻；
- 居民与访客日常步行；
- 不允许建筑形成横断道路的“门城”。

如果某候选只能通过封堵主穿行线才能成立，应淘汰。

### E. 居住生活

检查：

- 家庭入口是否能与货物流线合理共存；
- 是否有院落 / 后勤 / 小供给空间；
- 噪声与短仓活动是否会把住家压成附属物；
- 是否能表达“生活 + 周转”而不是物流仓库。

### F. 水 / 排水 / 消防

不得假定附近水体就是饮用水。

至少判断：

- 雨水 / 地表排水方向；
- 是否容易积水；
- 未来取水 / 储水 / 消防水是否有可行的规划关系；
- 污物与生活区是否能分开组织。

本 Gate 不要求设计完整水利系统。

### G. 视觉与城市关系

比较：

- 从 Alliance Commons 进入中域时的可见性；
- 与 G1 门户社区未来街院的关系；
- 是否会喧宾夺主，误读为联盟边界官署；
- 与 N1 principal hub 的空间层级是否清楚。

---

## 5. Candidate 数量与比较

最终保留 **2–3 个**候选，不要给十几个点。

每个候选至少输出：

- ID；
- 精确 world bounds / polygon 或 RLE；
- surface elevation range；
- gross usable area；
- terrain adaptation；
- existing-content risk；
- subsurface risk；
- access / loading relation；
- resident-life relation；
- drainage / water note；
- political / visual risk；
- pros / cons；
- verdict。

必须给出一个清晰的 comparison matrix。

---

## 6. 最终推荐

只推荐 **1 个**优先 Site。

但推荐的只是：

> **建筑设计可以从这里开始的 Site envelope**

不是：

- 最终建筑 footprint；
- 施工区域；
- 最终道路；
- Plan / Section；
- block palette。

必须明确：

- 推荐 Site 为什么胜出；
- 为什么不会堵塞门户交通；
- 为什么适合“共享周转与生活院”；
- 哪些风险必须留到 Architecture Design / pre-build check 再解决。

---

## 7. Required Deliverables

写入建议目录：

`minecraft/建筑师/research/build-sites/CIV-001/MD-001S1/`

至少：

```text
README.md
SITE-GATE.md
candidates.json
recommended-site.json
current-world-audit.json
surface-terrain.json
existing-content-audit.json
subsurface-audit.json
access-drainage-audit.json
visual/
validation/
```

可视化至少：

1. G1 current-world site base；
2. 2–3 candidate comparison map；
3. recommended Site detail map。

如果能提供玩家视角截图，可作为附加 evidence，但不能代替机器坐标图。

---

## 8. 严格禁止

本轮不得：

- 修改任何 Minecraft block；
- WorldEdit 写入；
- 建道路 / 基础 / 标记柱；
- 设计建筑平面或剖面；
- 冻结 block palette；
- 修改 MD-001P-R1 总规；
- 修改 revision 154 boundary；
- 占用 political threshold / through-clearance；
- broad rescan。

`world writes = 0`。

---

## 9. Stop Rule

完成后：

- 写 `minecraft/建筑师/tasks/MD-001S1/COMPLETION.md`；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT + Owner 独立审核。

只有 Site Gate 被接受后，下一步才允许创建：

> **G1 共享周转与生活院 Architecture Design Task**
