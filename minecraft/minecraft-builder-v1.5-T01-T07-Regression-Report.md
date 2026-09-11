# minecraft-builder v1.5｜T01–T07 主回归总审计

日期：2026-09-11

范围：`MB-V11-T01` → `MB-V15-T07`

当前 Skill：`minecraft-builder v1.5`

本报告用于汇总七项主回归的跨测试证据，判断哪些规则已被验证、哪些问题仍持续、哪些应进入下一版 Skill、哪些应转移到工具链或未来 `minecraft-finisher`。

---

## 1. 总体结论

`minecraft-builder` 已经从“能够写方块，但容易在平地上堆对象、产生浮空/穿模/机械重复”的早期阶段，演化到：

> **能够比较稳定地完成 research/world rules → Plan + Section + Sequence → Macro/Meso/Micro → staged QA → bounded repair，并产出空间上成立、可进入、可审核的完整 Minecraft 场景。**

T06 与 T07 连续达到 `PASS_WITH_FINDINGS`，且没有复现 T03 的道路破坏建筑、T01/T02 的孤立重型几何、T04 的高架式假山路、T05 的静态错误水带等严重问题。

当前主要瓶颈已经从基础正确性迁移到：

1. **Architectural Massing & Silhouette / 建筑体量与轮廓成熟度**；
2. **Minecraft scale translation / 玩家尺度体验密度**；
3. **真实客户端感知式 QA**；
4. **受控 Vanilla fluid update 工具能力**；
5. **空间设计完成后的第二阶段精装。**

因此，`minecraft-builder v1.5` 可视为一个 **Release Candidate for bounded production**，但还不建议直接作为“无需人工中间检查、可在重要 Canon 区域无限自主施工”的最终版本。

---

## 2. 七项主回归结果

| Test | 题材 | Skill | Verdict | 主要结论 |
|---|---|---|---|---|
| T01 | 苏州园林 | v1.1 | PASS_WITH_MAJOR_FINDINGS | Plan/Section/Sequence 首次稳定进入施工；暴露裸地、植物、孤立几何、材质、参数化重复与感知 QA 缺口 |
| T02 | 山地修道院 | v1.1 | PASS_WITH_MAJOR_FINDINGS | 山地因果和游览序列成立；孤立几何、植物、材质、重复形态跨题材复现 |
| T03 | 中世纪河谷村落 | v1.2 | FAIL | Macro 成立，但道路后施工破坏建筑；暴露 System Interface / Envelope / Forced Elevation 缺口 |
| T04 | 山脊城堡 | v1.3 | PASS_WITH_MAJOR_FINDINGS | System/Envelope QA 生效；暴露 terrain-detached circulation、蛋糕山、材质 placement 与 facade craft 问题 |
| T05 | 幻想森林圣所 | v1.4 | FAIL_WITH_STRONG_POSITIVE_REGRESSION | Structural Vegetation 发生跃迁；水体缺少 Vanilla fluid 语义验证；花量仍偏保守 |
| T06 | 法式规则宫苑 | v1.5 | PASS_WITH_FINDINGS | Intentional regularity、花量、水体 QA、建筑表面语言均通过；主要剩尺度转译和 finishing |
| T07 | 绿洲商队驿站 | v1.5 | PASS_WITH_FINDINGS | Meaningful openness、干旱植被、水系/接口稳定；主要剩 box-dominant massing 与感知 QA |

总体趋势不是“问题越来越少”这么简单，而是问题层级持续上移：

> **施工错误 → 系统接口错误 → 地形/生态/流体语义 → 表面语言 → 建筑体量与最终完成度。**

这说明 Skill 的迭代总体有效。

---

## 3. 已被证明有效、应保留的核心规则

### 3.1 Plan + Section + Sequence

T01 起就稳定有效，并持续影响 T02–T07 的场地、标高、路径、视线和空间序列。它是整个 Skill 的核心，不应弱化。

### 3.2 Staged Construction + bounded repair

Codex 已形成 Macro → Meso → Micro → Repair 的工作方式，并会基于中间检查做有限返工，而不是一口气写完后只检查 samples。

### 3.3 Construction Integrity Sweep

T01/T02 的浮空、孤立石体问题推动 v1.2 后，后续测试中的六邻域/支承/孤立几何检查明显稳定。T04 甚至通过最终视图主动发现主塔封顶缺口并修订。

结论：**有效，保留。**

### 3.4 System Interface Integrity + Building Envelope Integrity

T03 的道路穿房是整个回归中最严重的系统性 false negative。v1.3 后 T04–T07 没再出现同等级“后施工系统把前序建筑切坏”的问题；模型还开始主动比较阶段前后建筑包络。

结论：**强有效，保留。**

### 3.5 Anti-Forced-Elevation + Terrain-Conforming Circulation

T02/T03 的平台化、T04 的长石质高架登山路推动规则收敛。到 T07，驿站不再通过大石台抬高，外部道路也不使用大包络清空/填高。

结论：**有效。**

### 3.6 Natural Terrain Morphology

T04 的连续等高台阶推动 v1.4；T07 在 Macro 自检中主动增加冲蚀沟打断连续层级，说明模型已经能识别“数学高度场味”。

仍未完全成熟，但继续加微规则收益有限。

结论：**有效但执行能力仍有上限，暂不继续扩写。**

### 3.7 Structural Vegetation / Layered Vegetation

T01–T03 的单株散点问题，到 T05 出现明显跃迁：祖树和大型结构树群真正承担 canopy、围合、背景、路径与主题表达；草、蕨、苔地、腐殖土也进入近地层。

T07 又证明该规则不会机械泛化到沙漠。

结论：**强有效。**

### 3.8 Flower Abundance Bias

T05 证明原规则过保守；v1.5 在 T06 中产生约千格花卉，同时 T07 能根据干旱生态主动降低花量。

结论：**当前力度基本合理，不再继续加量。**

后续仍需专项观察自然草甸/林缘中花群是否存在边缘扩散和低密度背景，而不是仅封闭 patch。

### 3.9 Controlled Material Language + Material Placement + Facade Articulation

T01/T02 的“材料少/整面单纹理”问题，在 T06/T07 已明显改善：palette 更丰富，且材料开始跟墙脚、窗套、屋顶、道路、棚架等构造职责关联。

当前建筑问题已不再主要是“方块种类少”。

结论：**有效。**

### 3.10 Water / Fluid Semantics

T05 暴露“connected water voxels ≠ Minecraft-valid water”。v1.5 后 T06/T07 开始分别报告：geometry connectivity / water-level logic / containment / fluid stability，并在无 tick 工具时明确写 `fluid stability unverified`。

结论：**Skill 侧修复有效；剩余缺口属于工具链。**

### 3.11 Intentional Regularity / Meaningful Openness

T06 证明 Anti-Grid 不会误杀有历史因果的轴线、对称、树列和规则花坛；T07 证明 Space Use / Vegetation 规则不会错误填满沙漠。

这两个 reverse test 很重要：说明 Skill 没有因为增加规则而完全失去题材判断能力。

---

## 4. 当前最值得进入 v1.6 的通用缺口

### 4.1 Architectural Massing & Silhouette｜建筑体量与天际线

**Decision：正式进入 v1.6。**

证据不是 T07 单例：

- T01/T02 已出现同一 generator 导致建筑形态重复；
- T04 大型建筑虽体量成立，但远中距离仍偏基础几何；
- T07 明确出现“box + facade details”模式：表面和屋顶有进步，但总体仍读成火柴盒。

当前 Skill 已有：

- Reusable Generator ≠ Repeated Morphology；
- Material Placement Logic；
- Facade & Surface Articulation。

但这些分别约束“不要复制”“材料怎么放”“墙面怎么做”，缺少一个专门检查**远中距离体量**的层。

v1.6 建议新增：

> ### Architectural Massing & Silhouette
> 建筑不能只在完成长方体主壳后，通过窗、材料和表面构件来“装饰成建筑”。在 Macro/Meso 阶段应检查体量层级、轮廓与截面是否由功能、结构、等级和题材产生。
>
> 对题材允许的建筑，应考虑：volume hierarchy、recess/projection、不同翼高、入口/核心体量、tower/iwan/vault/dome/terrace/courtyard edge、roofline variation、parapet/roof silhouette 等。
>
> 矩形和正交本身不错误；仓房、堡垒、商队驿站、现代建筑都可以高度方正。禁止的是“所有对象先做成相似 box，再靠 facade detail 区分”的无意识默认。
>
> Final Review 应从远景/中景检查 silhouette，而不仅是近景墙面。

这应是 v1.6 最重要、也可能是唯一必须新增的大规则。

### 4.2 Minecraft-scale Translation / Experiential Density

**Decision：保持 WATCH，不作为 v1.6 强规则。**

T01 苏州园林和 T06 规则宫苑都出现“现实尺度成立，但 Minecraft 玩家尺度偏松”的迹象；但 T07 又证明大面积空旷在沙漠可以完全正确。

如果立即写成“缩小/增加内容密度”，容易误伤真正需要开阔尺度的题材。

当前更适合只在 Final Review 中轻量提醒：

> 现实参考的绝对尺度不必 1:1 转成方块；应检查玩家实际移动时间、近中景信息密度和空间层级是否仍成立。

先作为观察项，不单独扩成一章。

---

## 5. 不应继续塞进 minecraft-builder 的问题

### 5.1 展示级 Micro / decorative finish

T06/T07 已经证明 Builder 可以让空间“成立”，但仍可能像高质量毛坯。

不要继续把以下内容大量塞入 Builder：

- 家具与生活杂物；
- 雕塑、灯具、座椅；
- 大量小型点景；
- 细密地表老化；
- 装饰性边界处理；
- 展示级室内陈设；
- 为每个角落补视觉信息。

建议建立独立：

`minecraft-finisher` / `minecraft-detailer`

其输入应是**已经通过 Builder 空间审核的世界/区域**；默认不得重做主道路、主地形、主建筑体量、主水体和核心空间序列，除非发现 blocker。

### 5.2 题材专用细则

不要把某次测试的道路宽度、河岸做法、花数量、固定树距、具体建筑材料、固定窗洞节奏等写入通用 Skill。

---

## 6. 工具链优先级高于继续扩 Skill 的问题

### 6.1 Minecraft 客户端 Perceptual QA

T01–T07 一直存在：软件体素透视不能完整反映真实纹理、光照、透明度、stairs/slabs/fence 实际模型、材质重复和玩家视觉尺度。

优先级：**High**。

理想能力：

- 指定世界、坐标、yaw/pitch；
- 自动切换玩家/旁观视角；
- 批量截图固定观察点；
- 可选白天/夜间；
- Builder 完成后生成一组真实客户端验收图。

这比再往 Skill 增加十条“看起来要好看”的文字更有价值。

### 6.2 Controlled Vanilla Fluid Update

v1.5 已能诚实报告 `fluid stability unverified`，但没有真正闭环水体运行时验证。

优先级：**High for water-heavy builds**。

需要：

- 对指定区域触发正常 neighbor/fluid tick；
- 等待稳定；
- 重新读取区域；
- 对比是否侧漏、回填、断流或形成意外 flowing water。

该能力应放在工具层，不应让 Skill 继续靠文字“猜”流体。

---

## 7. Production Readiness｜是否可以进入真实 `建筑师` 存档

### 结论

**可以进入 bounded production pilot；暂不建议 unlimited autonomous production。**

当前能力判断：

| 维度 | 状态 |
|---|---|
| 世界目标/写入安全 | PASS |
| Plan / Section / Sequence | PASS |
| Staged construction | PASS |
| Construction integrity | PASS |
| System interface | PASS |
| 基础可达性 | PASS |
| Terrain | PASS_WITH_NOTES |
| Vegetation | PASS |
| Material / facade | PASS_WITH_NOTES |
| Water static semantics | PASS_WITH_LIMITATION |
| Architectural massing | PARTIAL |
| Perceptual QA | TOOLING_GAP |
| 展示级 finishing | OUT_OF_SCOPE / FUTURE_SKILL |

### 推荐生产方式

在真实 `建筑师` 存档中，首批任务应选择：

- 有明确边界；
- 允许局部 undo / rebuild；
- 不直接覆盖核心既有建筑；
- 以新增区域为主；
- 在正式世界写入前仍保留 blueprint / preview；
- 完成后由 Owner 实机巡检，再决定是否进入 Finisher 或继续扩建。

对于大型水利、关键主城、不可逆核心遗产区域，仍建议等待客户端截图 QA / fluid update 工具增强后再完全放权。

---

## 8. v1.6 建议

### 必改

1. `Architectural Massing & Silhouette`。

### 轻量补充 / 不单独扩章

2. Final Review 增加 Minecraft-scale translation / traversal density 的一句检查。

### 不改

- 不继续增加花量规则；
- 不增加固定植被数量；
- 不把 Finisher 内容塞进 Builder；
- 不继续细化自然地形的微观生成公式；
- 不用 Skill 假装解决 Vanilla fluid tick 工具缺失；
- 不加入题材专用建筑模板。

建议完成上述最小 v1.6 后，不再马上重跑完整七项；可先做一个独立建筑专项样本验证 massing，再进入真实存档 bounded pilot。

---

## 9. 七轮回归真正说明了什么

最重要的结论不是某一个建筑“好不好看”，而是这套 Skill 已经证明可以通过独立测试逐步改变 Agent 的行为：

- 浮空/孤立几何 → 后续稳定检查；
- 后序系统破坏建筑 → 后续阶段接口复核；
- 强制平台化 → 开始顺应地形；
- 原版小树/散点树 → 自定义大型结构植被；
- 花永远太少 → 题材敏感的高花量，同时不污染沙漠；
- 水只看连通 → 分离 containment / level / fluid verification；
- 材料只存在 palette → 开始按构造 placement；
- Anti-Grid → 没有误杀规则式宫苑；
- Anti-Empty → 没有误杀沙漠留白。

因此 `minecraft-builder` 已经完成从“提示词集合”向“可验证设计方法”的转变。

下一阶段的重点不应再是继续无限堆规则，而应是：

> **建筑体量成熟度 + 客户端真实 QA + 独立 Finisher 工作流。**
