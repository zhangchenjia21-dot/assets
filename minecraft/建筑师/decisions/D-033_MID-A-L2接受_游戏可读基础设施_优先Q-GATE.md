# D-033｜接受 MID-A L2，并采用“游戏可读基础设施”原则，优先 Q-GATE

状态：**OWNER APPROVED / ACTIVE**

日期：2026-09-20

## 1. MID-A L2 接受

Owner 接受：

`CIV-001-MID-A-L2P-r1`

Implementation：

`478bc56769b19de88dc09a875c5a756fdb05d582`

GPT 独立审核：

`../planning/CIV-001/MIDDLE/MID-A/CIV-001-MID-A-L2P/独立审核.md`

正式结论：

> **PASS_WITH_NOTES / GPT REVIEW ACCEPTED / OWNER ACCEPTED**

接受的核心：

- MID-A = 29,175 格单一连续城市规划；
- Alliance Commons 东侧门户属于 MID-A，不是独立城市；
- 门户繁华，综合市场 / 日常生活核心稍向东；
- MID-A 继续作为整个 CIV-001 联盟建筑密度最高、土地利用率最高的城市；
- Q-GATE / Q-MARKET / Q-YARDS 是同一城市内部片区责任，不是三座城，也不是现代单功能 zoning；
- 50%–57% building footprint 只是规划方向，不是必须完成的 KPI；
- 当前世界浅层水 / 空腔 / 蜂巢 / 已知地下内容继续作为实际约束证据。

## 2. Owner Rule｜Game-readable Infrastructure

本项目是 Minecraft 世界建造，不是现实市政工程模拟。

今后 water / fire / drainage / waste / maintenance 等基础设施遵循：

> **优先保证玩家能够看见、理解并感受到城市具备这些功能；没有视觉、空间或玩法价值的隐藏工程可以抽象。**

### Water

可使用：

- 井；
- 公共水槽；
- 蓄水池 / 小型水池；
- 水桶 / 水缸 / 储水设施；
- 可读的取水点；
- 少量可见引水设施。

默认不要求：

- 完整地下供水管网；
- 真实水压；
- 水文模拟；
- 每户管线。

规划仍需保证高密城市中“居民有合理取水方式”，但不需要证明现实工程意义上的完整供水系统。

### Fire

可通过：

- 公共水缸 / 蓄水；
- 街角水桶；
- 有意义的小型开敞空间；
- 石材隔断 / 防火间隔；
- 可达巷道；

表达消防能力。

不做真实消防系统模拟。

### Drainage

优先使用玩家可见的：

- 路边明沟；
- 檐沟；
- 排水槽；
- 小沟渠；
- 石质盖沟 / 短涵洞；
- 顺地形排水。

不要求建立完整地下污水 / 雨水管网。

### Waste / Maintenance

通过：

- 后巷；
- 服务院；
- 垃圾 / 粪污短存点；
- 堆料与清运空间；
- 维护通道；

表达即可。

不要求模拟现实城市完整污水处理链。

### Rule of abstraction

如果某项隐藏工程：

1. 玩家看不到；
2. 不影响建筑 / 街道 / 景观；
3. 不产生有趣玩法；
4. 不改变上层因果规划；

则默认抽象为“存在合理的日常运营安排”，无需继续工程化。

但不得以“游戏抽象”为由删除：

- 玩家实际会经过的街道；
- 可见水点；
- 消防 / 通行需要的空间；
- 排水造成的可见地形关系；
- 装卸 / 后场 / 公共空间；
- 影响建筑布局的浅层风险。

## 3. 建设 / 规划优先级

Owner 授权 GPT 根据游戏体验安排 MID-A 的优先实施顺序。

当前优先顺序：

1. **Q-GATE｜门户街市片**
2. **Q-MARKET｜内城市场生活片**
3. **Q-YARDS｜南侧混合后场**

### 为什么 Q-GATE 第一

- 玩家从 Alliance Commons 进入 MID-A 时最先看到；
- 最能直接表达“全联盟最繁华城市”的第一印象；
- 同时包含居民、商业、旅宿、短存、修理、公共访问，能测试高密混合城市语言；
- 建成后可作为后续 Q-MARKET 的街道 / 建筑语言与 Architecture Kit 经验来源；
- 不需要等整座城市所有后勤细节完全模拟后才获得可见成果。

该优先级是 Minecraft 实施顺序，不等同于世界历史生长顺序。

## 4. 下一阶段

授权：

> **CIV-001-MID-A-QG-L3P｜Q-GATE Gateway Market District Planning**

使用 `minecraft-planner v0.5`。

本轮只做到 L3 District Planning：

- 不调用 Builder；
- 不设计具体建筑；
- 不 world-write。

L3 完成并经 GPT + Owner 接受后，再进入 L4 Urban Ensemble，并由 GPT 决定第一批实际建造组团。

`world writes = 0`。
