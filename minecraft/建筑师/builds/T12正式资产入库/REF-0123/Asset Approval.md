# T12 Asset Approval

## Owner acceptance

Owner 已完成 `MB-V110-T12-京町家修复` 的真实 Minecraft 客户端复核，并确认修复结果可以接受。

本次 Owner 实机验收解除 T12 独立审核中剩余的主要 `real-client movement UNVERIFIED` 边界：当前町家已通过 Owner 对楼梯、墙脚 / 柱脚、主要入口、仓库入口 / 台阶及主要移动路线的实际检查。

因此：

- T12 targeted regression 视为完整闭环；
- `minecraft-builder v1.10` 可进入 `建筑师` **Production Pilot**；
- 当前修复后的町家状态可升级为正式 **Asset Candidate — APPROVED FOR INGEST**。

## Approved source

资产提取必须以 T12 **修复后的最终实存状态**为唯一来源：

- world：`MB-V110-T12-京町家修复`
- source lineage：`MB-V19-T11-京町家` → T12 bounded physical Repair
- Skill：`minecraft-builder v1.10`
- Repair：47 格有界物理修复已归档并 reload 稳定

不得从 T11 原始版本、T12 baseline、测试中间状态或人工重新拼装版本提取正式资产。

## Ingest authorization

Owner 当前指令“我看过觉得可以了，下一步可以把这个建筑加入资产了吧？”视为对本候选的明确 **批准入库**。

允许下一步执行正式资产提取 / 转换 / 注册，但该授权仅针对资产库：

- 不授权修改 `建筑师` 正式存档；
- 不自动把本町家写入任何 Canon SITE；
- 不把测试脚本、QA 扫描器、超平坦外围或无关世界内容作为资产主体；
- 不允许为了资产化重新设计已通过验收的建筑。

## Ingest requirements

正式资产应至少保留：

- 修复后的完整建筑与其被 Owner 认可的前后庭 / 直接场地关系；
- 干净 bounding box 与明确 anchor / ground level / facing；
- 可复用的 Canonical Blueprint；
- 若当前资产系统支持，导出可由 26.2 Litematica 原生读取的 `.litematic`；
- stable REF ID；
- 类型、风格 / 时代、用途、尺寸、入口方向、ground interface、依赖与使用限制等 metadata；
- preview / 代表性视图；
- source provenance 与 Owner approval；
- 转换 / round-trip 验证，要求 0 unintended diff。

当前建议语义：`Architecture / Japanese / Edo-period / Machiya / Mixed commercial-residential / Courtyard compound`。

若现有正式资产库已有稳定目录、REF ID 分配和注册协议，必须沿用现有协议，不得为本资产另造第二套 registry。
