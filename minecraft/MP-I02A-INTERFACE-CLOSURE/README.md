# MP-I02A｜Planner → Builder 上游接口闭合回归材料

状态：**最小 revision package 已编制 / AWAITING GPT + OWNER REVIEW**。

`BDP-01 r2` 仍为 `CONCEPT_DESIGN_READY`。U-PUBLIC 与 U-RAINWATER 均保留 `UNRESOLVED / BEFORE_DESIGN_FREEZE`；本包没有把局部补充包装成设计冻结就绪。回归结论 `NOT_ASSIGNED`，由 GPT + Owner 裁决。`world writes = 0`。

本轮使用当前 `minecraft-planner v0.5` 与 shared contract v1.0，源 HEAD 已核对为 `fc6371361685e2eeaefdef5a513f21dbe64c6696`。只发布 BDP-01 局部 overlay，不替换 MP-P05R2 整包，不改变建筑方案、地块、家庭程序、道路走线、Canon、Skills 或 contract。

建议审核顺序：

1. [修订差异.md](修订差异.md)：决定、理由与没有闭合的最小缺口。
2. [公共接口局部图.svg](公共接口局部图.svg)：观测标高、规划级局部控制与未闭合的两侧衔接。
3. [BDP-01.json](BDP-01.json)、[interface-baselines.json](interface-baselines.json)、[external-service-interfaces.json](external-service-interfaces.json)：可直接消费的 r2 对象。
4. [closure-register.json](closure-register.json)、[revision-lineage.json](revision-lineage.json)、[source-provenance.json](source-provenance.json)：剩余条件、失效范围和来源。
5. [validation.json](validation.json)、[manifest.json](manifest.json)：文件/几何一致性证据，均不是回归裁决。

当前 MP-I01R / BDP-01 concept r1 在此修订分支下明确标为 **STALE_FOR_FIDELITY_REVIEW**。原建筑文件没有改动；“stale”不代表 Builder 设计失败，也不代表已经对新接口完成核验。

## 公共接口

观测 `(757,1633)` ground block Y131，行走面 Y132。规划级固定私侧接触面 `X=[757,758], Z=1634, Y=132`；私側高度变化由 Builder 留在本户消化。公侧局部连接块 `X=[756,758], Z=[1634,1636]` 四列全部在原 LANE-04 mask 内，观测行走面均为 Y132。给出 Y132 设计面和其上 3 格净高控制。

这个 2×2 连接块是局部断面控制，**不是连续公共通行已经闭合的证明**。其左右两侧接入斜向既有路带时，仍需连续法向净宽、转折和标高衔接的局部几何证据。原中心线采样与 CELL_CENTER_MASK 不能替代这些证据。本轮没有把该缺口推迟到施工。

PUBLIC-COORDINATOR 承担公共路面、净空和跨界服务的规划协调职责。该角色在原 register 中为 `PROPOSED_ROLE_NOT_ACTUAL_APPOINTMENT`，本轮不伪造承接人或回签。真实土地/地役许可仍在 `BEFORE_WORLD_WRITE`。

## 雨水接口

当前 Builder 责任仍是 `RESERVE_INTERFACE_ONLY`。允许提交闭合本地策略作定量比较；在证明设计事件、入流/有效储量、恢复过程和超限失效安全之前，不升级为已选定闭合策略或 `FULL_SCOPE_OWNER`。

冻结前有两个等价的闭合路径：公共方提供受纳位置/标高/能力及责任，或 Builder 提交经核验的本地闭合性能证据并据此修订 service。不得假定岩石可渗、两只容器容量足够、住户无限清空，或公共路可接溢流。没有设计 gutter、pipe、cistern 或 foundation 的精确工程参数。

供水、污物运营等维持原 resolve_before；U-GROUND、U-HABITABILITY、B-TRANSLATION 等不在本轮闭合范围，保留原状态。

## 复现与边界

`python -X utf8 接口修订.py` 在原工程位置按记录的允许输入重新编译修订文件；脚本只写其自身目录。归档中的输入快照可用于直接核对，不需重读整份上游规划。`python -X utf8 交付校验.py` 可在归档目录独立运行；额外传入 `--verify-sources` 仅对登记的本机源文件做 SHA256 核对。

本轮没有启动游戏、执行器、服务端或任何存档读取/写入作业。归档按 Owner 指定路径 `minecraft/MP-I02A-INTERFACE-CLOSURE/`，覆盖仓库默认项目路径规则。完成交付后停止，等待 GPT + Owner 审核。
