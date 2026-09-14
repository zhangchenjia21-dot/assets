# MP-I01R｜Handoff Consumption Record

## 设计开始前的加载记录

- Builder：**minecraft-builder v1.11**。正式源 `zhangchenjia21-dot/Vibe-Coding`，commit `fc6371361685e2eeaefdef5a513f21dbe64c6696`，`skill/codex/minecraft-builder/SKILL.md`。以固定提交的只读快照加载；没有安装、修改或回写 Skill。
- Shared contract：**Minecraft Planner–Builder Contract v1.0**，同一 commit，`skill/codex/shared/minecraft-planner-builder-contract.md`。
- Planner handoff：`MP-P05R2 / BDP-01 / r1`，`CONCEPT_DESIGN_READY`，边界 `CELL_CENTER_MASK`，`world_write_authorization=false`。
- 来源哈希、四项 direct dependency 的匹配记录和 Canon 快照见 `inputs/来源与读取记录.json`。网络 HEAD 在加载时核实为上述 commit。

## Context intake（先于 Architectural Intent）

继承 WHY：西首卸与东向轻载之间的家庭规模小修理、值守与临院收交。Program：完整一家生活、工具与一批件、可独立使用的家庭小院。Rights：拟议户用地；公众路线与共同院不归本户圈占。Flow：来件→户内短存/小修理→原路交还；家庭独立通行；洁净收水与污物搬出错时。

本包的所有 interface baseline 都有本地 geometry、坐标语义、现状 section、调整范围及责任者。几何足以有界设计，**公共协调标高和雨水受纳不足以设计冻结**。因此 intake 使用 `CONCEPT_DESIGN_WITH_INTERFACE_HOLD`，不是 `INCOMPLETE_HANDOFF`，也不是集成回归结论。

## 读取选择与排除

`builder-design-packages.json` 由工具解析 JSON 容器，立即以 `package_id == BDP-01` 选择。模型只收到 BDP-01；没有输出、使用、复制或归档 BDP-02 内容。首次 BDP-01 大输出被工具截断，随后针对同一 BDP-01 字段分次读取；没有扩大上下文。

允许的 direct dependency：`interface-baselines.json` 和 `external-service-interfaces.json` 只提取 BDP-01 自带的确切 interface/service IDs；四个文件均先核对声明 SHA256。`地表采样.json` 与 `浅层采样.json` 只将本户 151 columns 进入设计快照；公路已有本地 section 直接使用包内值。未读取容器内容。

BDP-01 的 `source_refs` 指向 `provenance.json`、`sources/来源登记.json`，只用于追溯 Skill/contract 与批准 Canon/Grammar 来源；没有沿来源表继续打开 MP-P04 或其它父规划。CIV-001 Canon、D-014 与 Architecture Grammar 是当前允许的设计依据，其旧 Builder v1.2 引用不覆盖本任务明确要求的 v1.11。

未读取 MP-P05R2 `URBAN-ENSEMBLE.md`、Independent Review 或 Owner 解释文档；未读取 MP-P05R、MP-P05、MP-I01、MP-P04 完整规划或既有北岩台建筑答案。目录名称曾为定位而列出，不代表内容被读取。记忆注册表只用于找到历史 Builder 仓库地址，不作为设计输入；历史设计 rollout 未打开。

## Planning Fidelity 对照（不冻结、不裁定回归）

| 继承项 | 本轮消费 / 设计映射 | 状态与证据 |
|---|---|---|
| WHY | 低肩作坊、两条入口、门内短存 | 已落入平面；没有改成纯住宅或大型产业 |
| 一完整家庭 | 起居/炊食/两床/日储/封闭卫生 | 概念尺度已表达；实际家庭规模待确认 |
| 修理低肩与上沿复核关系 | 修理 Y132，仍由公共路继续向上沿 | 不设计邻户、不改变上沿接口 |
| 家庭院 | 同户西侧3×6露天，独立廊外私侧落脚可达 | 18 格，零屋面覆盖 |
| 原门前缓冲 | 原24格原位保留 | 未圈入封闭建筑 |
| 公共路/共同院 | 仅作为外部到达和不可占用 geometry | 模型零mask侵入；公共扫掠净宽仍待公共方核验 |
| CELL_CENTER_MASK | 逐体素查询发布 cells，不重算法线/斜边 | 全部模型列位于151格内，边缘容差0 |
| 标高 | (757,1633) Y132 接触候选；余高差户内消化 | 需PUBLIC-COORDINATOR接受，未称已冻结 |
| 建筑作者权 | 自行选双层住屋、独立廊、两种屋面与小院移位 | 没有读既有答案或复制房型 |
| 地下保护 | 不设地下室，未提出低于观测ground的编辑 | 地表替换/局部填高仍需基础影响审查 |
| 服务越界 | 仅收水、日储、密闭污物、雨水容器预留 | 没有创造公共水管、排水出口或废物终端 |
| 不确定性 | 全部按resolve_before拆开记录 | 见issues.json；不以图纸存在代替closure |

## 接口版本与后续最小补充

消费 `R2-IF-LANE-01/02/04`、`R2-IF-COMMON-EDGE` 与 `R2-IF-THRESHOLD-1`（以输入实际 ID 为准），direct dependency revision r1；source_revision 仍保留 MP-P04-r1，只是来源标签，不曾回读其规划内容。服务为四个 `R2-S1-*`，责任全部 `RESERVE_INTERFACE_ONLY`。

最小上游动作是回签本户接触点的允许表面、公共连续净宽/净高与雨水受纳责任及位置。Builder 已尝试把高差、院落与阶梯全部留在本户内；这不能替公共方签署道路与雨水决定。若有变化，仅受影响接口/BDP递增revision，并将本设计标记 `STALE_FOR_FIDELITY_REVIEW`。

Planning Fidelity 当前为**冻结前证据已整理 / INTERFACE HOLD**，不发放 gate PASS，也不把外部 HOLD 写为 Builder 失败。集成回归 verdict：**NOT_ASSIGNED，交 GPT + Owner**。
