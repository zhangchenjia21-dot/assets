# WB-003R｜Economic & Accessibility Substrate Reconnaissance

状态：**AUTHORIZED / DISPATCH READY**

授权：`../../decisions/D-012_WB-003R经济与通达性最小调查授权.md`

## 0. 任务定位

这是 CIV-001 文明设计的**最小资源 / 通达性补充调查**。

前序 WB-002R-R1 已经完成 whole-scope terrain / biome / land-water / vegetation Regional Profile。本轮禁止把它重新做一遍。

目标：只补齐足以回答“三域为什么互相需要、怎么移动”的事实。

**world writes = 0**。

---

## 1. 必读

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/世界构建原则.md`
4. `minecraft/建筑师/decisions/D-010_大型扫描证据GitHub轻量化.md`
5. `minecraft/建筑师/architecture/大型扫描数据交付与审核契约.md`
6. `minecraft/建筑师/decisions/D-011_CIV-001人类三域联盟与三席议会方向批准.md`
7. `minecraft/建筑师/decisions/D-012_WB-003R经济与通达性最小调查授权.md`
8. `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/README.md`
9. `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/独立审核.md`
10. 本 Task Packet

WB-002R / R1、V1 / NG-2 / NG-3 immutable。

---

## 2. 空间框架

当前 CIV-001 高层 Human Geography：

```text
西域 = 西部 C 形低岛
中域 = 东岛西部低地 / 坡麓过渡带
东域 = 东岛山地核心
```

这三个是文明设计区，不要求本轮重新画政治边界。

前序 whole-scope bounds：

`X=-800..2463, Z=1376..3487`

优先复用 R1 现有 terrain / biome / surface / vegetation / water 数据。

---

## 3. 调查问题

### 3.1 Lowland / agricultural-substrate proxy

不要估算农业产量。

基于已有：

- LOW_RELIEF_FLAT / GENTLE_SLOPE；
- surface biome；
- surface material；
- inland-water / shoreline distance；

形成可解释的低平生产空间 proxy，并分别比较西域 / 中域 / 东域。

输出必须明确：这只是形态 / 环境 proxy，不等于肥力或真实产量。

### 3.2 Construction materials

调查会真实影响建筑的材料空间差异，至少关注：

- logs / wood 类型与结构性植被来源；
- exposed / near-surface stone palette；
- sand / gravel / clay；
- 其它明显可作为建设材料的自然方块。

优先使用现有 surface / vegetation 数据；只有近表层信息确实缺失时才做 targeted read。

### 3.3 Mineral presence

不需要全岛逐方块矿物普查。

采用可解释的 sampled / targeted 3D 方法确认若干关键矿物 / ore 的：

- presence / absence within sampled scope；
- west / middle / east 相对差异；
- sampling depth / density / limitations。

禁止把样本结果直接写成“富矿区”“矿业中心”。

### 3.4 Water / shoreline accessibility proxy

基于已有水陆拓扑，补充：

- inland-water adjacency；
- low-slope shoreline sections；
- adjacent-water depth proxy（如可可靠读取）；
- shoreline approach geometry。

这些只能叫：

- `WATER_ACCESS_PROXY`
- `LANDING_ACCESS_PROXY`

不得叫天然港、航道、可饮用淡水。

### 3.5 Inter-island crossing

计算西岛与东岛之间：

- 最短表层水面间距；
- 若干代表性低坡岸对岸距离；
- 不同 crossing candidate 的岸坡 / 邻水深度 proxy。

只用于说明跨岛联系成本，不规划正式航线。

### 3.6 East-island movement

利用 R1 terrain grid 形成从：

`东岛西部低地 / 坡麓 → 东部山地内部`

的 terrain-based least-cost / corridor proxy。

至少考虑：

- slope；
- relief；
- step / cliff penalty；
- water barrier。

输出 2～5 条有解释力的自然通行 corridor candidate 或说明不存在明显 corridor。

不是道路规划。

---

## 4. Human Geography interpretation

最后只能提出 **bounded hypotheses**：

例如：

- 哪一域更容易承载密集低平聚落；
- 哪一域对石材 / 木材 / 某类矿物接触更多；
- 哪一域承担跨岛交换节点的自然条件更强；
- 哪些自然差异可以解释三域互相依赖。

每条必须标记：

- `SUPPORTED_BY_CURRENT_EVIDENCE`
- `PLAUSIBLE_BUT_UNVERIFIED`
- `NOT_SUPPORTED`

不得直接生成正式经济 Canon。

---

## 5. “三席议会中心岛”边界

Owner 已批准：三席议会相关建筑优先安排在其所称“西部平岛的中心岛”。

本轮：

- 不规划建筑；
- 不 world write；
- 不擅自猜坐标；
- 若现有 topology / map 可以唯一对应该 referent，可记录候选 machine mapping；
- 若不能唯一对应，输出 `OWNER_REFERENT / COORDINATE_TBD` 即可。

---

## 6. 大型扫描轻量化硬约束

严格遵守 D-010。

### Local-only

默认不 push：

- 新增完整逐柱 observed DB；
- dense 3D block arrays；
- 全量矿物 sample trace；
- 重复 R1 raw database；
- 巨型 geometry expansion。

如需要，留 Local Raw Cache，并登记 manifest。

### GitHub Review Bundle

目标总新增 research payload **<=15 MiB**。

超过 25 MiB：**禁止 push，除非另获明确授权。**

至少保留：

```text
review/index.json
review/key-metrics.json
review/stratified-witnesses.jsonl
review/limitations.json
manifest/raw-cache.json
manifest/source-fingerprint.json
manifest/lineage.json
profile/substrate-summary.json
profile/material-profile.json
profile/mineral-sample-profile.json
profile/water-access-profile.json
profile/crossing-profile.json
profile/movement-corridors.json
profile/human-geography-hypotheses.json
reports/经济与通达性前置画像.md
visual/（必要的少量地图）
validation/summary.json
validation/rebuild.json
```

不要求无意义凑齐文件；允许合理合并。

---

## 7. Validation

至少验证：

- current-world freshness；
- R1 reuse 与 source hash 对齐；
- targeted read provenance；
- task 期间 world unchanged；
- `world writes = 0`；
- sample design 可复现；
- crossing / corridor 结果可重建；
- Review Bundle 能支撑主要结论；
- GitHub payload size 符合 D-010。

---

## 8. 禁止事项

不得：

- 修改 World Canon；
- 创建正式贸易路线；
- 确定农业产量 / 人口；
- 宣称港口 / 航运能力；
- 宣称矿区富集，除非未来专门任务验证；
- 创建 Architecture Bible；
- 规划或施工三席议会建筑；
- 修改 Minecraft world；
- 重写 predecessor evidence。

---

## 9. Completion

完成后：

- `minecraft/建筑师/tasks/WB-003R/COMPLETION.md`
- `minecraft/建筑师/research/human-geography/southern-island/WB-003R/`
- current 仅机械回写 implementation completed / awaiting review；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT 独立审核。

本任务完成不自动把经济 hypotheses 升格为 Canon，也不授权 Architecture / Build。
