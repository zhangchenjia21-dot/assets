# CIV-001-MID-A-QG-L3P｜Authority Matrix

状态：**ACTIVE INPUT BASELINE**

## A. 必须继承

- D-024 revision154 territory；
- Alliance Commons 边界 / X=89 接口；
- accepted CIV-001 L0；
- accepted Middle L1；
- accepted MID-A L2；
- D-032：MID-A 是联盟最高密度 / 最高土地利用城市；
- D-033：Game-readable Infrastructure；
- Q-GATE 是 MID-A 内部片区，不是独立城市；
- 公共访问不得因商业繁华被封堵；
- 门户不具有自动海关 / 收费 / 强制交易权；
- Q-GATE 必须同时包含真实居民生活、交换和公共服务，不得变成纯商业布景；
- world writes = 0。

直接父包：

`minecraft/建筑师/planning/CIV-001/MIDDLE/MID-A/CIV-001-MID-A-L2P/handoff/L3-Q-GATE.md`

## B. 当前世界证据

优先使用 MID-A L2 于 2026-09-14 取得的有界 current-world snapshot：

- `evidence/current-observation.json`
- `evidence/shallow-exceptions.json`
- `evidence/settlement-geometry.json`
- `evidence/access-probes.json`

如当前世界已经 materially 改变，或 L3 精确形态涉及未覆盖体积，只做 Just-in-time 有界只读刷新。

不 broad rescan。

## C. Game-readable Infrastructure

本轮对基础设施的完成标准是：

- 玩家能看到 / 理解主要取水关系；
- 街道 / 院落有可读排水逻辑；
- 高密环境中有可读消防 / 维护空间；
- 装卸 / 后巷 / 服务院不与主要居民通行互相抹除。

不要求：

- 地下供水网络；
- 地下污水网络；
- 真实消防工程；
- 水压 / 流量 / 工程容量模拟。

L3 可以保留一个或多个公共井 / 水槽 / 蓄水点的规划需求，但具体构造由后续 Builder 决定。

## D. Legacy Firewall

Primary L3 Freeze 前不得用以下旧成果作为答案：

- 旧 G1 exact envelope / threshold / clearance；
- MD-001S1 Site 推荐；
- MD-001U1 1310格 / 五栋方案；
- Middle Kit v0.1 模块与尺寸；
- 旧 first-build / building program；
- 旧 R1a/R1b 街道几何。

Freeze 后可以做 A/B comparison：

- 比较是否有独立重现的门户功能；
- 复用仍新鲜且范围完全匹配的观测事实；
- 不得回填 Primary。

## E. 下游必须重新求解

- Q-GATE 内部真实 district morphology；
- 主 / 次街道与巷道关系；
- 街坊 / frontage / shared courtyard / service lane；
- 公共 / 共用 / 半私有空间；
- 地块分割 / 合并的历史逻辑；
- 门户最繁华带与向 Q-MARKET 连续过渡；
- 玩家可见的水 / 排水 / 消防 / 后勤空间；
- Architecture Kit Requirements；
- L4 Urban Ensemble packages；
- 第一批推荐 Builder / build package 的优先顺序。

不得在 L3 直接设计具体建筑。
