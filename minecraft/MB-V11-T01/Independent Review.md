# T01 Independent Review｜minecraft-builder v1.1

日期：2026-09-09

测试世界：`MB-V11-T01-苏州园林`

结论：`PASS_WITH_MAJOR_FINDINGS`

本审核为独立回归审核，不接受 Builder 自报 PASS 作为空间质量完成证据。Owner 已进入 Minecraft 实际游览并提供现场观察；GitHub 中的 Completion Report、研究与设计记录、施工脚本、阶段证据与存档审计用于交叉验证。

## 总体判断

`minecraft-builder v1.1` 在 T01 中已经明显改变了模型的空间设计方式。相比旧版“平地上摆建筑”的典型失败，本轮真实形成了山、水、建筑、道路与结构性植被共同组织的三维园林骨架；Plan / Section / Sequence 也真实进入了设计与施工，而不是停留在文字说明。

当前主要瓶颈已经从“不会规划三维空间”下移到：地表完成度、细节植物 palette、形态多样性、材料层次、rockwork 质量、施工完整性检查，以及真实客户端画面的感知式 QA。

## 18 项统一审核摘要

1. Research / World Rules：PASS。研究结论确实影响宅园边界、山水建筑共同组织与游览序列。
2. Plan：PASS。主池、叠山、入口、西院、竹院等主次关系成立。
3. Section：PASS。水面 Y=62、道路约 Y=63–67、山亭基座 Y=76，形成真实垂直关系。
4. Sequence：PASS。入口屏墙转折、见水、登山回望、曲桥入岛等形成连续体验。
5. Terrain：PASS_WITH_NOTES。已经主动造山，但 rockwork 仍偏 heightfield / 方块化。
6. Water：PASS_WITH_NOTES。水体承担空间组织作用，但深浅、水岸与水下形态较薄。
7. Architecture：PASS。建筑基本嵌入山水关系，不是散落摆件。
8. Structural Vegetation：PARTIAL_PASS。主要乔木与竹林参与空间组织，但树形参数化重复明显。
9. Detail Vegetation：FAIL。Micro 植物种类与覆盖明显不足。
10. Density / Open Space：PARTIAL。存在合理留白，但整体画布与内容密度存在失配，大面积默认草地显得未完成。
11. Scale：PARTIAL。建筑—山体—树冠关系基本成立，但园林总体尺度偏松。
12. Anti-Grid：PASS。未见无意识规则网格主导设计。
13. Asset-copy Feel：PASS_WITH_NOTES。未机械复制资产库，但自写参数化生成器产生相似形态。
14. Skyline：PASS_WITH_NOTES。树冠、山体、屋顶已有层次，但树形相似削弱天际线丰富度。
15. Accessibility：PASS_WITH_NOTES。主要目的地可达，但路线扫描仍保留局部 blocked-cell 告警。
16. Player-perspective Richness：PARTIAL_PASS。Sequence 逻辑正确，但真实客户端下仍暴露空旷与细节不足。
17. Staged Construction：PASS。Macro → Meso → Micro → bounded correction 有真实设计意义。
18. Self-check：PARTIAL。能发现廊柱侵路、峰石遮挡等问题，但漏掉裸草地完成度、浮空石块等低级缺陷。

## Findings Ledger

### Positive Evidence

- `T01-P01`｜Macro 山水—建筑—路线一体化明显改善。
- `T01-P02`｜Plan / Section / Sequence 已真实影响施工与修正。

### Findings

#### T01-F01｜Ground Plane 完成度不足

分类：`B｜MODEL_EXECUTION_FAILURE`，同时记 `A｜SKILL_GAP WATCH`

Owner 现场看到大量裸露 `grass_block`，视觉上仍像未完成的超平坦基底，而非有意识设计的草坪、地被、林下层、土面、碎石或种植床。

现有 Skill 已明确 Detail Vegetation，但 Final Review 对 Ground Plane 没有独立强检查项。当前先记录，不修改 Skill；若在不同题材重复出现则升级为 v1.2 候选。

#### T01-F02｜原版细节植物 palette 严重未利用

分类：`B｜MODEL_EXECUTION_FAILURE`，同时记 `A｜SKILL_GAP WATCH`

Micro 实际施工主要使用荷叶、杜鹃叶等少量元素，几乎没有主动使用 Minecraft 已有的花、草本、藤本、地被等丰富植物块。

现有 Skill 已明确“花、草、小灌木、荷叶、藤蔓、地被、小型点景植物”，因此本轮首先属于模型执行不足。后续观察模型是否错误泛化“不要依赖原生小树”为“原版植物都不重要”。

#### T01-F03｜浮空 / 孤立石块未被发现

分类：`A｜SKILL_GAP` + `B｜MODEL_EXECUTION_FAILURE`

Owner 在叠山旁、水池上方发现实际浮空石块。现有最终审计主要验证指定方块回读一致性和路线可达性，没有检查 unintended floating / isolated / disconnected geometry。

该问题属于基础施工正确性，提前列为 `v1.2 early candidate`：未来应加入轻量 Construction Integrity / Support & Orphan Geometry Check，区分设计性悬挑与非意图孤立残片。

#### T01-F04｜Final Review 偏工程正确，弱完成度巡检

分类：`A｜SKILL_GAP WATCH` + `B｜MODEL_EXECUTION_FAILURE`

最终自检能抓到遮挡、廊柱侵路和可达性，但未抓到大面积默认基底、植被完成度与孤立石块。说明当前 QA 对“是否成功写入/是否能走到”强，对“是否像完成作品/是否有低级视觉缺陷”弱。

#### T01-F05｜总体尺度与内容密度失配

分类：`B｜MODEL_EXECUTION_FAILURE`

约 184×148 的园界承载七处厅亭与有限植被，导致亲密尺度的苏州园林体验被拉松。空旷感不只来自植物数量少，也来自内容被摊在偏大的画布中。

该问题高度依赖题材，暂不写成通用 Skill 规则。

#### T01-F06｜参数化形态重复

分类：`B｜MODEL_EXECUTION_FAILURE`，同时记 `A｜SKILL_GAP WATCH`

建筑主要由同一 `hall()` 生成器改变尺寸；乔木主要由同一 `tree()` 生成器使用近似分枝模板，仅调整高度、冠幅和倾斜。工程实现高效，但产生明显 morphology repetition。

后续重点观察不同题材是否继续出现“同一建筑 resize / 同一树型 scale variant”的程序模板感。

#### T01-F07｜Material Surface Modulation 不足

分类：`B｜MODEL_EXECUTION_FAILURE`，同时记 `A｜SKILL_GAP WATCH`

材料体系是连贯的，但存在“一种空间职责 = 一种纯材料整片铺设”的工程化倾向，如大面积 grass_block、smooth_stone、gravel、white_concrete 等。问题不是材料少本身，而是缺少有理由的风化、过渡、边缘与局部层次。

不应把此 finding 误写成“方块种类越多越好”。

#### T01-F08｜Rockwork Morphology 不足

分类：`B｜MODEL_EXECUTION_FAILURE`

主动造山已成功，但主要地形仍接近数学 heightfield / 椭圆山丘，叠山所需的峰、谷、洞、缝、壁、咬合石体和小尺度穿行关系不足。该问题题材特异，暂不升级为通用 Skill 规则。

#### T01-F09｜Perceptual QA Gap

分类：`C｜TOOLING_LIMITATION`

Codex 最终主要审阅的是存档回读后生成的简化方块几何和纯色材质，而 Owner 看到的是 Minecraft 客户端最终纹理、光照、植被与尺度体验。裸草地、重复纹理、真实树叶/栏杆比例等问题在 debug render 中容易被低估。

未来工具链高价值增强：支持真实客户端指定坐标 + yaw/pitch 的玩家高度截图、自动观察点截图或环绕截图，用于最终感知式 QA。

#### T01-F10｜Audit Finding Triage 不够严格

分类：`C｜TOOLING_LIMITATION / QA DESIGN`

最终审计虽然整体标记 PASS，但路线数据仍保留西/东岸局部 blocked cells，曲桥入岛有较多 blocked cells，随后由 Builder 自行解释为栏杆边缘等预期几何。

未来审计宜区分：`PASS / EXPECTED_GEOMETRY / WARNING_REVIEWED / FAIL`，避免“机器报异常 → Builder 自解释 → Builder 自 PASS”的闭环。

## 当前 v1.2 候选状态

- 强候选：`Construction Integrity / unintended floating-orphan geometry check`（T01-F03）。
- 观察候选：Ground Plane 完成度（F01）、原版 Detail Vegetation 利用（F02）、Final completion sweep（F04）、参数化重复（F06）、材料层次（F07）。
- 题材专项，暂不通用化：T01-F05、T01-F08。
- 工具链改进：T01-F09、T01-F10。

## 回归纪律

本轮不修改 `minecraft-builder v1.1`。继续冻结当前版本执行 T02–T04，观察上述问题是否跨题材复现。除明显基础性安全/正确性缺口外，只有重复 finding 才升级为正式 Skill 修改候选。
