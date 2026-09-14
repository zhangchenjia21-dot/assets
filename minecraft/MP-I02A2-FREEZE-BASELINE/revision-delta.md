# MP-I02A2 revision delta

父包：MP-I02A / BDP-01 r2。新包：MP-I02A2 / BDP-01 r3。源规划仍为 MP-P05R2-r1。

| 对象 | 原问题 / r2 | r3 最小变化 | 闭合层级 |
|---|---|---|---|
| U-PUBLIC | 四格 patch，两侧连续性未固定；实际承接/回签仍当成缺口 | 完整50列公共扫掠、连续surface、每列净空、端部控制和调整范围；公共角色按本轮task-local定义 | Planning interface closed |
| U-RAINWATER | 仅预留；等待公共受纳或先有量化本地方案才能更新责任 | 明确禁止跨界、公共受纳义务为NONE、Builder直接负责设计和证明parcel-local策略 | Planning interface closed；工程性能仍open |
| BDP-01 | CONCEPT_DESIGN_READY | DESIGN_FREEZE_READY，明确不等于建筑DESIGN_READY | Planner handoff readiness only |
| MP-I01R 当前设计 | r1设计已被r2标stale | 对r3仍STALE_FOR_FIDELITY_REVIEW，原设计不改 | 等待Builder重新核验 |

R2-IF-LANE-04、R2-IF-THRESHOLD-1、R2-S1-RAINWATER 均 r2→r3。其余接口/服务对象原样保留，r1不变；新文件容器revision不自动升级它们。LANE-04只覆盖本户前沿的局部clear path，原 route object、其它路段、其它package均未重规划。

## 几何决定及证据

原中心线与cell-center mask只是名义走廊，不能证明斜边和转弯净宽。本轮把本户局部通行路径放入已有公共mask与共同院内，使用可精确计算的矩形并集。每段路径的半宽1方形扫掠互相以完整2×2方形重叠；不存在只靠对角接触的窄口。全部50列属于已有公共土地集合，和本户151列零重叠。以14列已属共同院的空间提供局部转角/肩部净宽补偿，仍保留共同使用属性。

接触面仍为 Y132，未移动本户入口。西端/东端分别与原控制点观测顶面 Y131/Y134 对接。H(X)的连续插值和每列角标高全部明示；设计值标记DESIGN_PROPOSAL，观测列保持OBSERVED_SNAPSHOT。逐列核对相对观测的调整不超过±1；没有读取或假定地下可施工条件。

本轮提供的是沿原前沿关系的最小局部可通行控制，不是现代格网或统一平台，不改变修理低肩、独立家庭院、一户容量及西来转轻载的因果关系。若Builder需要改变公共通道或接触面，必须新修订接口；屋顶、户内阶梯和蓄水构造仍由Builder自定。

## 消除责任误置

MP-I02A 的实际任命/回签要求不再作为本任务规划冻结条件。当前 Owner 已明确允许 task-local DESIGN_PROPOSAL 公共baseline；它不生成真实地役。雨水也不再要求 Planner 先完成水文工程再发 handoff：责任边界已明确，性能证明作为 Builder 冻结前义务保留。

旧的 `RESERVE_INTERFACE_ONLY`、有条件研究但未选择local strategy、要求公共receiving point等活动字段已从 r3 雨水接口删除，防止旧新责任混用。历史值仅保留在 `inputs/` 快照中用于追溯。

## 状态上限

无剩余 planning-interface HOLD。Builder 的基础、居住、转译、雨水性能和Planning Fidelity条件仍未核验。不认定建筑DESIGN_READY，不认定真实通行/机构/许可，不判回归PASS/FAIL。所有执行与存档写入为0。
