# CIV-001-MID-L1P｜Authority Matrix

状态：**ACTIVE INPUT BASELINE**

本文件控制 Middle L1 重编译时哪些内容必须继承、哪些必须重新求解、哪些旧成果必须隔离。

> 核心原则：**继承 L0 因果关系，不继承旧 Middle 答案。**

## A. `UPSTREAM_FIXED / OWNER_CONSTRAINT / APPROVED_CANON`

必须继承：

- revision154 Middle exact territory = **391,002 blocks²**；
- Alliance Commons exact geometry 与 X=89 政治接口不变；
- CIV-001 三席联盟、强地方自治与地方土地 / 普通治理权；
- Middle broad role：接驳、仓储、商贸、加工、低地—山地转换；
- D-025：Middle territory-wide 平均建筑 / 聚落密度最高、土地利用最紧；
- West 生产开敞、East 全域分散山地聚落等 sibling 关系；
- Commons 是共享机构性政治领土，不是第四域，也不自动是商业漏斗；
- 已接受 L0 父案中的跨域需求与关系语义；
- `world writes = 0`。

直接父包：

`minecraft/建筑师/planning/CIV-001/POLITY/CIV-001-L0P/handoff/L1-MIDDLE.md`

父规划：

`minecraft/建筑师/planning/CIV-001/POLITY/CIV-001-L0P/`

Decision：

`minecraft/建筑师/decisions/D-031_CIV-001-L0P接受并进入MiddleL1区域规划.md`

## B. `OBSERVED / DERIVED EVIDENCE`

优先复用：

- accepted natural geography / NG evidence；
- `WB-002R-R1`；
- `WB-003R`；
- revision154 exact territory；
- CIV-001-L0P 的 territory terrain / movement / flows / actors / capacity evidence。

Planner 可重新解释这些 evidence 在 Middle L1 的意义，但不得把：

- terrain proxy；
- weighted path；
- research sample；
- biome / surface contact；

伪装成现成道路、港口、城市、矿点、肥沃农田或已获得通行权。

### Freshness

L1 不以“全面重新扫描”为默认。

若决定某个区域中心、跨水接口、谷地通道或容量时，现有 evidence 不足：

- 允许 Just-in-time 小范围 read-only 当前世界补查；
- 必须说明为什么需要读；
- 必须记录范围、时间与不确定性；
- 不得 broad rescan。

## C. `TO_REDERIVE`｜本轮必须重新求解

不得从旧规划直接继承：

- 中域聚落 / 中心数量；
- principal / secondary 层级；
- 具体中心位置；
- Commons connector 是否形成独立门户聚落；
- 一个大中心 vs 多个分工中心；
- 中域内部 regional subareas；
- regional corridors / movement relations；
- West→Middle 与 Commons→Middle 是否共用接驳；
- Middle→East 的接口数量与角色；
- settlement capacities；
- regional growth sequence；
- regional land-use / density distribution；
- 向 L2 下放的 settlement packages。

## D. `LEGACY / REFERENCE_ONLY`｜Primary L1 Freeze 前禁止读取

在 `PRIMARY-FREEZE.json` 完成前禁止读取或搜索命中：

- `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/`
- 旧 P1–P5；
- 旧 N1 / N2 / N3 / N4 / G1；
- `minecraft/建筑师/research/build-sites/CIV-001/MD-001S1/`
- `minecraft/建筑师/planning/CIV-001/MIDDLE/G1/MD-001U1/`
- `minecraft/建筑师/architecture/civilizations/CIV-001/kits/MIDDLE/v0.1/`
- 旧 corridor / first-build / building program；
- `CIV-001-L0P/LEGACY-COMPARISON.md`。

注意：父规划其它 Primary artifacts 可以读取；禁止的是带旧答案的 Legacy comparison。

Freeze 后允许单独输出 `LEGACY-COMPARISON.md` 做 A/B，但不得回填 Primary。

## E. `DOWNSTREAM_TO_RESOLVE`

Middle L1 应至少把以下问题明确交给未来 L2，而不是越级解决：

- settlement exact footprint / exact street geometry；
- district boundaries；
- parcel / frontage；
-具体建筑 program；
- Architecture Kit exact modules / dimensions / palette；
- Builder Plan / Section；
- world-write geometry。

L1 可以确定 settlement role、search envelope、regional corridor relationship、capacity hypothesis 与跨 settlement 依赖，但不能提前画成建筑总平面。
