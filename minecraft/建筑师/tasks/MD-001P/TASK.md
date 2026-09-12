# MD-001P｜Middle Domain Detailed Master Planning

状态：**AUTHORIZED / DISPATCH READY**
日期：2026-09-12

## 0. 任务定位

本任务负责 CIV-001 **中域（Middle Domain）详细总体规划**。

这不是建筑设计任务，不施工，不写真实 Minecraft world。

`world writes = 0`。

必须使用 TT-002R 已接受的 revision 154 领土 geometry：

`minecraft/建筑师/research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json`

正式决策：

- `minecraft/建筑师/decisions/D-024_TT-002R中域东域精修边界接受并进入MD-001P.md`
- `minecraft/建筑师/decisions/D-025_三域聚落密度与土地利用梯度.md`

不得再用 WB-003R `M` research mask 代替正式中域边界。

---

## 1. 规划目标

回答：

> **整个中域应该如何在真实地形上形成一个可信的、三域中土地利用强度最高的前现代接驳—商贸—加工—坡麓转换区域？**

完成后，GPT + Owner 应能够明确知道：

- 中域内部有哪些自然 / 人文规划子区；
- 主聚落与次级聚落应该在哪里；
- 人口、商业、仓储、加工、居住、渡运和交通大致如何组织；
- 中域如何连接 Alliance Commons；
- 中域如何向东部山地输送人员 / 货物并接收矿产 / 石材 / 金属产品；
- 如何体现中域相对于 West / East 更高的平均建筑密度与土地利用强度；
- 第一座中域中等规模建筑应该从哪个节点、哪类功能中产生。

---

## 2. 必读资料

至少读取：

1. `minecraft/建筑师/current/项目状态.md`
2. `minecraft/建筑师/current/世界构建原则.md`
3. `minecraft/建筑师/current/建造原则.md`
4. `minecraft/建筑师/world/civilizations/CIV-001/README.md`
5. `minecraft/建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md`
6. `minecraft/建筑师/decisions/D-021_先完成中域区域调查与总体规划再进入首栋建筑.md`
7. `minecraft/建筑师/decisions/D-024_TT-002R中域东域精修边界接受并进入MD-001P.md`
8. `minecraft/建筑师/decisions/D-025_三域聚落密度与土地利用梯度.md`
9. `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/`
10. `minecraft/建筑师/research/human-geography/southern-island/WB-003R/`
11. `minecraft/建筑师/research/build-sites/CIV-001/AB-001P1R/`
12. `minecraft/建筑师/research/human-geography/southern-island/territory-refinement/TT-002R/`
13. 本 Task Packet。

---

## 3. 当前正式领土基线

revision 154：

```text
ALLIANCE_COMMONS = 92,124
WEST_DOMAIN      = 575,397
MIDDLE_DOMAIN    = 391,002
EAST_DOMAIN      = 1,198,158
UNASSIGNED       = 0
DISPUTED         = 0
```

Middle 当前 component count = 2；largest component ≈ **390,995** columns，另有极小 secondary component。

总体规划默认以 largest Middle component 为主要规划对象；极小 secondary component 只记录性质，不得为了“完整”强行赋予重要聚落功能。

### 3.1 Owner 三域密度 / 土地利用梯度

必须把 D-025 作为规划硬输入：

```text
territory-wide 平均建筑 / 聚落密度：Middle > West > East
土地利用与空间组织强度：Middle 最高
大面积农牧生产景观：West 最强
山地适应 / 地形工程能力：East 最强
East 聚落分散广布程度：最高
```

Middle 的含义不是“把每一格都盖满”，而是：

- 三域中平均建成强度最高；
- 主聚落最紧凑；
- 居住 / 商贸 / 仓储 / 加工 / 旅宿 / 公共功能混合度最高；
- 土地浪费最少；
- 重点节点应体现紧凑街区、窄街、院落、仓院、后院与多层使用；
- 仍必须保留真实地形需要的坡地、岸线、公共空间、通行和缓冲。

不得因为 D-025 而大面积推平地形或做现代高密网格城市。

---

## 4. 数据策略

### 默认只复用现有证据

优先复用：

- R1 elevation / slope / relief / biome / water / shoreline / topology；
- WB-003R landing / crossing / terrain-cost / materials evidence；
- TT-002R accepted political boundary；
- Alliance Commons connector geometry。

默认：

- `broad rescan = 0`
- `world writes = 0`

如果某个具体规划节点因为证据缺失无法判断，可做 **Just-in-time 极小范围 read-only 补查**；必须记录范围、必要性和结果。

不得为了规划方便重新扫描整个东岛或整个南部岛群。

---

## 5. 必须完成的总体规划层级

### A. 中域自然规划骨架

把中域内部划成 **3–6 个有地理依据的 Planning Subareas**。

每个 subarea 至少记录：

- geometry / bounds；
- elevation / slope / relief；
- water / shoreline relation；
- major flat / gentle space；
- movement relation；
- 与 Commons / East 的关系；
- 适合与不适合的聚落 / 生产活动；
- 建议的人文利用强度等级。

分区必须服从真实地形，不按规则矩形、现代 zoning 或固定面积机械切分。

### B. 聚落层级

基于地理、中域 Canon 和 D-025，提出一套成熟期 settlement hierarchy。

至少考虑：

- **1 个 principal hub candidate**：中域最重要、也是中域最高密度的接驳 / 商贸 / 加工 / 行政性聚落候选；
- **2–4 个 secondary nodes**：例如渡运节点、山前加工镇、仓储节点、谷地居民聚落等；
- 更小的 hamlet / waystation / production cluster 只在确有地理必要时提出。

这些是总体规划节点，不是立即施工 Site。

必须体现：

- principal hub 应明显紧凑而不是摊大饼；
- secondary nodes 可以因地形分散，但中域整体人文利用强度仍应高；
- 聚落之间的空地应有地形、生产、交通或景观理由，不得是无意义留白。

如果真实地形不支持“1 主 + 多副”，应明确提出更合理结构，不得为了任务格式硬凑。

### C. 交通与交换网络

规划长期 movement system：

- Alliance Commons connector → Middle core；
- Middle core → East mountain interface；
- 水岸 landing / ferry interfaces；
- 主陆路 / 次陆路 / 山前路径；
- 货物与普通居民交通的基本关系。

必须区分：

- existing terrain evidence；
- proposed future road / dock；
- only corridor reservation。

不得把 WB-003R terrain-cost path 自动变成现成道路。

中世纪 / 前现代道路避免现代网格和大直轴，优先服从地形、既有节点和逐步生长逻辑。

高密不意味着道路更宽；更合理的中域应通过紧凑街巷、院落和节点密度提高利用率。

### D. 土地使用 / 功能布局

至少规划成熟期的：

- 商贸 / 市场；
- 仓储；
- 加工 / 手工业；
- 居民区；
- 客栈 / 商旅服务；
- 马厩 / 车马 / 装卸；
- 中域地方公共建筑；
- 祭祀 / 宗教；
- 食物与日常供应；
- 岸线活动；
- 结构性植被 / 地形保留；
- 与 East 矿业产品交换接口。

中域不是纯商业园区，也必须有长期居民与日常生活系统。

土地使用必须体现 Middle 的高强度特征：

- 主聚落核心优先 mixed-use；
- 避免功能之间出现大面积现代式退距；
- 仓储 / 加工 / 商贸 / 住宿 / 居住可以形成近距离互补，但必须处理噪声、火灾、货运与生活空间冲突；
- 低价值空地应减少，但高价值公共空间、交通空间、岸线与 terrain buffer 必须保留。

### E. 人口 / 居住逻辑

不需要精确人口数字，但必须说明：

- 哪些人会长期住在中域；
- 主聚落与次节点大致的居住密度差异；
- 商人、仓储工、加工匠人、摆渡人、旅店经营者、车夫、地方官 / 书记、祭司、普通家庭等如何形成真实社区；
- 哪些区域应是高密街区，哪些应保留低密 / 坡麓 / 岸线缓冲；
- 如何通过紧凑的混合使用而不是现代高层建筑体现高土地价值。

### F. 与两侧政治空间的接口

必须明确：

#### Middle ↔ Alliance Commons

- connector 是政治边界和陆路接口；
- 未来是否形成关卡、界石、桥头市、迎宾 / 转运设施等只作为规划选择讨论；
- 不得把 Commons 纳入中域城市扩张。

#### Middle ↔ East

- accepted refined boundary revision 154 为规划边界；
- 谷地 / 山口 / 坡麓转换应决定主要交流接口；
- 不得让中域城市无视山体继续向东规则扩张。

---

## 6. 第一座建筑的规划出口

MD-001P **不得直接设计建筑**，但最终必须回答：

> 下一步最值得进入 Local Site Gate 的第一座中域中等规模建筑是什么？为什么？

输出：

- 推荐建筑类型 1 个；
- 备选最多 2 个；
- 每个对应规划节点；
- 功能理由；
- 为什么它适合作为 CIV-001 第一座地方建筑样板；
- 该建筑如何体现 Middle 的高密、高混合使用、交换 / 加工导向；
- 预期规模只给量级，不冻结尺寸。

此前“商旅转运会馆 / 山海驿馆”只是候选，不是强制答案。

---

## 7. 可视化要求

必须输出至少：

1. **Middle Domain terrain planning base map**
2. **Planning subareas map**
3. **Settlement hierarchy + nodes map**
4. **Movement / exchange network map**
5. **Land-use / functional master plan map**
6. **Human-use intensity / density map**：明确高密核心、次级紧凑节点、低强度 / terrain reserve 区；
7. **Phasing / first-build recommendation map**

要求：

- 使用真实 territory geometry；
- 等比例；
- 坐标可追踪；
- Alliance Commons 与 East 作为邻接 context 显示，但不得混入 Middle 规划范围；
- 不做纯幻想插画代替规划图；
- density map 必须体现 D-025，不得只画均匀的彩色覆盖。

若适合，可另制作一张面向 Owner 的简化彩色总图，但机器可核验底图必须同时存在。

---

## 8. 机器可读交付

写入：

`minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/`

至少：

```text
README.md
MASTERPLAN.md
MASTERPLAN.json
subareas.json
settlement-nodes.json
movement-network.json
land-use.json
human-use-intensity.json
first-build-recommendation.md
visual/
validation/
```

`MASTERPLAN.json` 至少记录：

- source territory revision = 154；
- Middle exact area；
- D-025 density principle；
- planning subareas；
- settlement hierarchy；
- proposed corridors；
- land-use zones；
- human-use intensity zones；
- water interfaces；
- Commons interface；
- East interface；
- reserved / no-build terrain；
- first-build recommendation；
- `world_write_authorized=false`。

---

## 9. Planner Critic

总体规划形成后做一次内部 Critic：

至少检查：

- 是否真的服从 terrain，而不是把颜色盖在地图上；
- 是否真正体现 `Middle > West > East` 的 territory-wide 密度梯度；
- 是否把“高密度”错误理解成填满所有空地；
- 是否有真实居民和日常经济，而非纯功能节点；
- 是否把所有商贸都堆在 connector；
- 是否误把 terrain-cost proxy 写成道路；
- 是否在陡峭山地规划大面积规则街区；
- 是否产生现代 zoning / 网格感；
- 是否为未来 East / Commons 连接保留合理接口；
- 第一座建筑是否来自整体规划，而不是事先指定后硬找位置。

交付最终修订版，不需要给 Owner 三套完整 masterplan 选择。

---

## 10. 严格禁止

本轮不得：

- 修改真实 Minecraft world；
- 施工道路、码头、城镇或建筑；
- 设计第一栋建筑的详细 Plan / Section / block palette；
- 修改 revision 154 territory boundary；
- 修改 Alliance Commons；
- 修改 CIV-001 Canon / AB-001 Grammar；
- broad rescan；
- 自动授权下一步 Build。

`world writes = 0`。

---

## 11. Completion / Stop

完成后：

- 写 `minecraft/建筑师/tasks/MD-001P/COMPLETION.md`；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT + Owner 独立审核。

通过后，下一步才创建：

> **中域第一座中等规模建筑的 Local Site Gate**
