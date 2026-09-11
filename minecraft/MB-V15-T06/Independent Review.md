# T06 Independent Review｜规则宫苑

## Verdict

**PASS_WITH_FINDINGS**

这是目前回归组中第一轮比较接近“空间设计与工程正确性均成立，主要剩完成度与体验密度问题”的样本。

T06 成功通过了本轮最重要的反向压力测试：模型没有把 Anti-Grid / Anti-Repeat 机械理解为“所有轴线、对称、规则树列和规则花坛都必须被打散”。在真实凡尔赛式规则园林研究支持下，轴线、对称、树列、绿墙、刺绣花坛、平台与镜池均被作为有因果的人工秩序使用。

## Positive regression evidence

### T06-P01｜Intentional Regularity

- 宫殿—观园平台—花坛—圆池—镜渠形成明确长轴。
- 两侧修剪树列、绿墙园室、花坛对称具有历史与空间理由。
- 模型没有因为 Skill 的 Anti-Grid 原则而强行打散规则式园林。

**结论：PASS。**

### T06-P02｜Architectural Surface Quality 改善

宫殿不再仅由单一墙材和方洞构成：使用 smooth sandstone、quartz、chiseled sandstone、deepslate tiles、glass、slabs/stairs，并通过墙脚、窗套、柱式、山花、屋顶和收边表达构造层级。阶段 02 发现侧立面偏空后又执行 02a 修订。

**结论：v1.4/v1.5 Material Placement + Facade Articulation 有正向效果。**

### T06-P03｜Water QA 行为改善

独立池体有明确设计水位、连续池底/侧壁和岸顶约束；Completion Report 明确把 `fluid stability unverified` 与几何、水位、containment 检查分开，没有再把几何连通冒充 Vanilla 流体稳定性。

**结论：v1.5 Water Semantics 更新生效。**

### T06-P04｜Flower abundance 数量已显著提高

终态实存统计：

- white tulip 254
- red tulip 272
- orange tulip 334
- cornflower 192

总计约 1,052 格花卉，已经不属于 T01—T05 那种“数量不足”的问题。

## Findings

### T06-F01｜Minecraft Experiential Density / Scale Translation

**Classification:** `B MODEL_EXECUTION_FAILURE + A SKILL_GAP WATCH`

Owner 实机感受到大面积草方块空地。结合生成逻辑，这并非完全“漏做”：设计文件明确把大草坪作为衬托花坛、水面和长轴的正式园林组成，因此现实原型层面存在合理性。

但在 Minecraft 中，224×320 的场地尺度使许多现实中成立的大草坪在玩家尺度下显得过于空、重复，缺少中近景信息。

问题应区分为两层：

1. **空间骨架层**：大草坪/留白有历史和构图理由，不能因为“空”就全部填满。
2. **Minecraft 表达层**：现实尺度不能机械换算成方块尺度；过长的空旷距离可能需要适度压缩，或在不破坏正式构图的前提下加入更细的边界、地表、雕塑、盆栽、修剪构件、座椅、灯具、水景构件等玩家尺度信息。

建议后续 Skill 候选：`Experiential Scale Compression / Minecraft-scale Translation`。真实世界大尺度场景应优先保留空间层级与视线，而非原样保留所有绝对距离。

### T06-F02｜Spatial Completion 与 Decorative Finish 应区分

**Classification:** `D WORKFLOW / PRODUCT-SCOPE FINDING`

T06 暴露出一个较清晰的工作流边界：`minecraft-builder` 已能完成 Macro/Meso、主要 Micro、功能与接口，成品在“空间设计”层面可成立，但仍可能看起来像一版高质量毛坯。

建议未来考虑独立第二阶段 Skill，例如：

`minecraft-finisher` / `minecraft-detailer`

职责只在已通过空间审核的成品上进行：

- 表面细化；
- 小尺度构件；
- 点景；
- 地表变化；
- 精细种植；
- 雕塑、盆栽、灯具、座椅等环境对象；
- 局部材质老化/边界处理；
- 可选室内陈设。

该 Skill 默认不得重做总体道路、主要建筑体量、主水体或核心空间序列，除非先发现明确 blocker。

因此不建议把所有“精装”责任继续塞进 minecraft-builder，避免 Skill 膨胀和注意力竞争。

### T06-F03｜Flower Zoning Rigidity

**Classification:** `D TASK_SPECIFIC_JUDGMENT + A WATCH`

花卉数量本轮并不少；真正的问题是**高度分区化**。生成逻辑把四种花主要锁定在四个刺绣花坛和少数附属花带中，几乎形成“花只属于被规划过的花区”的行为。

对本轮法国规则式宫苑而言，这种控制是合理甚至正确的：正式花坛本来就应高度园艺化，不能拿森林/草甸标准要求其随机扩散。

因此本轮不能据此修改通用 Skill。

但要继续观察：当下一次题材属于自然草甸、林缘、乡野或幻想 lush 环境时，模型是否仍然把花限制在少数明确多边形 patch 中。如果会，则说明 Flowering Community 被模型误解成“先划几个花区”，需要补充 `patch diffusion / edge transition / background low-density presence` 的概念。

### T06-F04｜Garden-room 内容层次仍偏少

**Classification:** `B MODEL_EXECUTION_FAILURE`

西侧水园、东侧绿剧场等空间类型已经存在，但园室内部的中尺度内容仍较少。形式上有池、草心、短座阶、绿墙，但玩家进入后能互动/观察的局部对象有限。

这与 F02 的“Finishing Pass”高度相关，不建议直接扩写 minecraft-builder 通用规则。

### T06-F05｜Formal Garden 仍可进一步强化 vertical layering

**Classification:** `B MODEL_EXECUTION_FAILURE / D TASK-SPECIFIC`

规则式园林不只依靠平面图案，也依赖不同高度的绿墙、修剪树、低篱、盆栽、雕塑、水景喷射、台阶和建筑立面共同形成垂直层次。本轮已有树列、绿墙、花坛、宫殿高差，但近地—中层—高层的层级仍可更丰富。

不建议作为通用硬规则加入 Skill；更适合未来 detail/finisher 阶段。

## Owner feedback interpretation

### 1. “场地太空”

判定：**部分成立，但不是单纯 Skill 失败。**

现实参考确实支持大草坪、宽阔轴线和开敞视域；代码和设计文件也明确把 grass lawn 作为主动设计结果，而非超平坦残留。

真正的问题是现实园林尺度到 Minecraft 玩家尺度的转译，以及空间设计完成后缺少第二层 finishing。

### 2. “花像被规划成只有这里才能长”

判定：**本轮待定。**

终态约 1,052 格花，数量已经充分；集中在刺绣花坛与附属花带符合本轮规则式园艺逻辑。因此不能用本轮直接证明 v1.5 Flowering Community 仍失败。

下一次自然环境测试应专门观察花丛边缘是否有疏密渐变、背景低密度存在和群落过渡，而不是只出现几个封闭 patch。

## Overall Assessment

T06 是重要正向样本：

- Anti-Grid 没有过度抑制历史上合理的规则性；
- 建筑材质与立面构造比早期测试明显进步；
- 水景 QA 从“连通”升级到了水位/containment/验证边界；
- 花卉数量已经大幅提高；
- 没有发现影响交付的建筑/交通/孤立几何硬错误。

当前主要瓶颈已经从“空间设计错误”进一步迁移到：

> **Minecraft 尺度转译 + 玩家尺度完成度 + 第二阶段精装。**

因此本轮不建议因为“草地显空”立即把 minecraft-builder 改成一个无限添加装饰的 Skill。优先完成 T07；之后再决定是否创建独立 `minecraft-finisher`。