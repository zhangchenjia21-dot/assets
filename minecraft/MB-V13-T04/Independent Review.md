# T04 Independent Review｜山脊城堡

## Verdict

**PASS_WITH_MAJOR_FINDINGS**

T04 的 Macro / Meso 层面总体成立：山脊选址、防御层级、内外院、壕沟、城门、主塔与主要建筑关系清楚；v1.3 新增的 System Interface Integrity、Building Envelope Integrity 与 Construction Integrity 也确实改变了 Codex 的施工与 QA 行为。本轮没有复现 T03 那种后序系统直接破坏前序建筑的严重退化。

但终态仍存在几项系统性设计问题，主要集中在自然地形、登高交通与建筑表面表达。

## Positive Regression Evidence

### T04-P01｜System Interface Integrity 生效

Codex 增加了阶段接口复核，对后期植被 / Micro 阶段是否删除或破坏前序建筑结构进行比较。本轮没有发现道路、植被或后期施工切坏建筑 envelope 的明显问题。

### T04-P02｜Construction Integrity 已进入稳定流程

Codex 对主要路线、可达目标、六邻域重型几何、孤立构件和最终存档状态进行了检查；并在最终玩家高度视图中发现主塔顶部环带缺失，随后完成 03a 有界修订。这说明工程完整性与最终视觉检查比 v1.1 明显进步。

### T04-P03｜Ground Plane / Detail Vegetation 改善

与 T01/T02 相比，短草、蕨、粗土和林下地表明显增加，说明 v1.3 的 Layered Vegetation 与 Ground Plane 规则已经产生行为变化。

## Findings

### T04-F01｜Terrain-Detached Circulation

**Classification:** SKILL_GAP + MODEL_EXECUTION_FAILURE  
**Severity:** Major

Owner 实机观察发现，坡脚至城堡的长石质登高道路 / 台阶虽然具有实体支承，却在较长距离内脱离自然坡面，形成类似独立高架结构。

生成逻辑先定义道路的目标三维高度，再在道路高于当前地形的位置用石体从原地面填至道路标高。因此其工程上“有支撑”，但空间上没有充分依托地形。

这说明 Anti-Forced-Elevation 的概念目前主要覆盖建筑，尚未充分约束 circulation。

**Recommended Skill direction:** Terrain-Conforming Circulation。山路、坡道和用于克服自然高差的室外台阶默认应顺坡、贴坡、折返或局部切填；桥梁、栈道、城墙楼梯等有明确工程目的的独立构筑可例外。

### T04-F02｜Contour-Terrace Terrain

**Classification:** MODEL_EXECUTION_FAILURE + SKILL_GAP WATCH  
**Severity:** Major

大面积山坡表现为连续、平行的 Minecraft 等高台阶，形成明显的“heightfield / 蛋糕山”视觉。虽然已经脱离超平坦，但自然地貌仍缺少沟谷、凸脊、坡肩、侵蚀、岩体断面和坡脚堆积等组织。

**Recommended Skill direction:** Natural Terrain Morphology。自然地形不能仅依靠连续高度函数和少量噪声，应通过有尺度的地貌特征打破机械等高线。

### T04-F03｜Facade Articulation / Architectural Craft不足

**Classification:** MODEL_EXECUTION_FAILURE + SKILL_GAP WATCH  
**Severity:** Major

主塔、厅堂等大型建筑的体量成立，但玩家中近距离下大量立面仍是大面积单平面墙体配简单方洞。材料替换本身不足以解决该问题；需要符合构造逻辑的墙脚、转角、门窗框、扶壁、梁架、檐口、屋脊及局部进退。

### T04-F04｜Flowering Community 仍过于象征性

**Classification:** SKILL_GAP + MODEL_EXECUTION_FAILURE  
**Severity:** Moderate

本轮近地植被明显增加，但花卉仅使用极低密度的 oxeye_daisy。适合出现自然野花的草坡 / 林缘仍主要表现为草与蕨。

**Recommended Skill direction:** flowering species 应作为生态 / 色彩相容的小型群落、边缘带或疏密斑块出现，而不是只用一种极低密度花朵象征“有花”；同时禁止平均撒花和无语境集齐颜色。

### T04-F05｜Material Placement Logic 仍不足

**Classification:** MODEL_EXECUTION_FAILURE + SKILL_GAP  
**Severity:** Major

palette 中已有 stone / andesite / cobblestone / stone bricks / mossy stone bricks / polished andesite / wood / plaster / deepslate 等材料，但实际大型墙面、屋顶和院地仍长期由单一材质覆盖。问题已经从“没有 palette”转为“不会把 palette 按构造和环境原因组织到表面”。

**Recommended Skill direction:** Material Placement Logic。材料变化应跟随墙脚、转角、门窗、受潮 / 风化、修补、屋脊 / 檐口和构造层级，而不是随机 noise mixing。

## Overall Assessment

v1.3 已经明显改善“后序施工破坏前序系统”和“只做方块写入正确性”的问题。本轮主要瓶颈已经从工程完整性迁移到设计合理性与 Minecraft architectural craft：

1. 工程上有支撑，不代表道路与自然地形关系合理；
2. 会生成高差，不代表会生成自然地貌；
3. 有材料 palette，不代表会做成熟表面语言；
4. 有草蕨，不代表花卉与植被群落完成。

这些结论用于后续 Skill 修订与回归；不得把 T04 Owner feedback 当作下一测试的额外题目提示。
