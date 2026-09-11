# T08 Independent Review｜v1.6 建筑体量专项

## Verdict

**FAIL_TARGETED_REGRESSION**

T08 的工程完整性、基本功能、可达性和阶段修订仍保持了 T06/T07 之后的稳定水平，但本轮是专门验证 `minecraft-builder v1.6` 新增 **Architectural Massing & Silhouette / Massing Gate** 是否真正改变建筑设计方式的专项测试。在这一核心目标上，结果不通过。

v1.6 确实改变了 Codex 的流程表现：模型主动生成 Massing Gate、单色轮廓、远中距透视与剖面，并在文档中逐项说明主次体量。然而生成逻辑仍以大型矩形 shell 为基础，再在 Meso 阶段叠加尖拱、肋拱、扶壁、窗洞和材料。也就是说，本轮出现了明显的 **process compliance without sufficient design improvement**：形式上执行了 Massing Gate，但 Gate 的判断标准过弱，未能阻止“generic box massing + Gothic overlay”。

## Positive evidence

### T08-P01｜v1.6 确实触发了 Massing workflow

模型在 Macro 后真实生成了：

- 西南 / 东北体量透视；
- 单色轮廓；
- 纵横剖面；
- `Massing Gate.md`；
- 进入 Meso 前的明确体量判断。

因此 v1.6 不是“完全没有被读取或执行”，而是**规则已经改变行为，但质量门本身不足以区分“可读”与“优秀”。**

### T08-P02｜建筑功能组织基本成立

长中殿、低侧廊、耳堂、交叉部、东端礼仪空间、南侧回廊、参事堂、宿舍及折返梯具有明确功能关系；最终 14 个关键点均被静态路线检查判为可达。

### T08-P03｜工程 QA 仍稳定

后期检查并修复了：

- 宿舍上层未接通；
- 附属门洞厚墙未贯通；
- 低屋面穿入高空间；
- 半砖屋面缝隙；
- 座位悬空；
- 东翼厚墙窗洞问题。

最终全体积与 Canonical Blueprint 一致、无六邻接孤立实体。说明 System / Construction Integrity 没有明显倒退。

## Findings

### T08-F01｜Massing Gate false positive

**Classification:** `SKILL_GAP + MODEL_EXECUTION_FAILURE`  
**Severity:** Critical for this targeted regression

`Massing Gate.md` 的核心通过依据是：去掉材质后仍能辨认长中殿、低侧廊、耳堂、交叉钟楼、西前室、回廊、宿舍和参事堂。

这证明的是 **typological legibility**，并不证明：

- 体量比例成熟；
- 各体量连接自然；
- roofline 已解决；
- 主要轮廓不是大型 primitive 的拼接；
- 结构系统真正驱动外形；
- silhouette 有建筑审美质量。

一个由多个粗糙长方体拼成的模型，同样可以非常容易地“看出这里是中殿、这里是耳堂”。因此当前 Massing Gate 存在系统性 false positive。

**Required direction:** Gate 不能只问“主次体量能不能认出来”，还必须检查 **composition / proportion / tectonic logic / junction resolution / roof transition / negative-space quality**。

### T08-F02｜Box-first method persists beneath v1.6

**Classification:** `MODEL_EXECUTION_FAILURE + SKILL_GAP`  
**Severity:** Major / target failure

生成器核心仍使用通用 `shell(x,z,w,d,h)`：先形成完整矩形实体，再掏空内部。主教堂首先由约 94×36 格的大 shell 建立，耳堂、前室、宿舍、参事堂随后继续由同类 shell 生成。

之后才在 Meso 中增加：

- 尖拱；
- 高窗；
- 肋拱顶；
- 扶壁；
- 门套；
- 柱脚 / 柱头；
- 材料变化。

因此实际设计顺序仍接近：

> generic shell → carve → Gothic vocabulary

而不是 v1.6 期望的：

> Function / Typology → structural & sectional system → Massing → Roofline → Facade

这说明“不要 box-first”目前仍主要是文字规则，没有真正进入生成策略。

### T08-F03｜Gothic structural language is applied after massing instead of generating massing

**Classification:** `SKILL_GAP + MODEL_EXECUTION_FAILURE`  
**Severity:** Major

哥特式建筑尤其依赖 section / bay / support / vault / buttress / roof system 共同决定形态。本轮却先建立完整石壳，再在 Meso 中把柱列、尖拱、肋顶和扶壁加进去。

这会产生一个根本问题：

> Gothic elements 成为“贴到已经完成的盒体上的语言”，而不是“生成建筑形态的结构系统”。

对于这种高度依赖构造体系的建筑，仅增加 Massing vocabulary 不够。需要在建筑任务中先识别 **tectonic / structural-spatial system**，再让主要体量由它产生。

### T08-F04｜Roof / Section junctions were not actually resolved at Massing Gate

**Classification:** `MODEL_EXECUTION_FAILURE + QA_GATE_GAP`  
**Severity:** Major

Completion Report 明确记录：直到 Micro / final perspective 阶段才发现：

- 低屋面穿入高空间；
- 半砖屋面出现缝隙；

随后 Repair 阶段才清除室内残余瓦片并闭合侧廊屋面基层。

这些不是典型 Micro 缺陷，而属于 **Macro / Meso 的 section + roof intersection**。既然 v1.6 Massing Gate 明确要求 Section / Roofline 在进入 Meso 前成立，那么这种错误能存活到 Micro，说明 Gate 没有真正检查 junction quality。

**Required direction:** Massing Gate 应明确抽查 major mass junctions：

- nave ↔ aisle；
- nave ↔ transept；
- tower ↔ crossing；
- church ↔ cloister；
- main block ↔ attached wing；
- roof ↔ internal volume。

### T08-F05｜Secondary architecture remains primitive-volume dominant

**Classification:** `MODEL_EXECUTION_FAILURE`  
**Severity:** Major

即使主教堂具有十字体量，西前室、宿舍、参事堂和回廊仍主要由矩形 shell / flat slab 组合生成。尤其回廊屋面在实现层直接表现为低位整片 slab plane，而非真正经过截面组织的 lean-to / roof system。

这说明 v1.6 的“重要建筑体量”规则没有充分传递到 secondary masses。建筑群的主次可以有复杂度差异，但次要建筑不应自动退化为 primitive box。

### T08-F06｜Roof silhouette uses generic voxel primitives rather than resolved roof construction

**Classification:** `MODEL_EXECUTION_FAILURE`  
**Severity:** Moderate–Major

主屋面和耳堂采用规则化 gable generator；交叉钟楼顶部采用逐层缩小的方形 slab 层形成尖顶。作为远景轮廓这可能产生高度变化，但仍有明显“程序几何”风险：屋面被处理成数学收缩体，而不是具有明确脊线、坡面、檐口、交接和支承逻辑的建筑构造。

该问题与 T07 的“火柴盒”属于同一上位问题：对象有轮廓变化，不代表已经形成成熟 architectural composition。

### T08-F07｜Facade / material improvement cannot rescue weak massing

**Classification:** `MODEL_EXECUTION_FAILURE`  
**Severity:** Moderate

本轮已有 stone bricks、smooth sandstone、polished andesite、deepslate roof、wood、glass，并使用尖拱、高窗、柱束和扶壁。材料和立面 vocabulary 并不贫乏。

但这反而证明了此前判断：

> material richness / facade articulation ≠ massing quality

Completion Report 也承认大块石墙与东翼立面仍较简洁。继续增加方块种类不会解决当前核心缺陷。

### T08-F08｜Functional QA remains binary and late

**Classification:** `QA_DESIGN + MODEL_EXECUTION_FAILURE`  
**Severity:** Moderate

Meso 后才发现宿舍上层未接通，说明 Plan / Section 中虽然写了垂直交通，但并未在建筑骨架阶段落实。

最终“14 targets reachable”证明可以抵达指定坐标，但不证明：

- 路径体验自然；
- 楼梯构造完整；
- 栏杆安全；
- 门洞比例与方向合理；
- 玩家无需奇怪跳跃或绕行。

工程可达性应继续保留，但不能作为 architectural circulation 完成度的主要证据。

### T08-F09｜Research is descriptive but insufficiently geometric for an architecture-specialist test

**Classification:** `TASK_SPECIFIC_JUDGMENT / RESEARCH_QUALITY`  
**Severity:** Moderate

本轮有 English Heritage 的 Rievaulx Abbey 作为高质量来源，但其它主要形态来源仍以百科式 Gothic / Fountains Abbey 描述为主。研究成功得到“长中殿 + 侧廊 + 耳堂 + 回廊 + 宿舍”等类型事实，却缺少一份被真正使用的高质量：

- plan；
- section；
- elevation；
- bay / vault / buttress measured relationship。

这容易让模型掌握名词关系，却无法掌握比例与构造关系。

对于 BUILDING 专项和未来重要 Canon 建筑，应优先取得至少一项可靠平面 / 剖面 / 立面几何参考。

### T08-F10｜Perceptual QA gap remains

**Classification:** `TOOLING_LIMITATION`  
**Severity:** Persistent

最终证据仍是简化体素软件渲染，而非 Minecraft 客户端真实纹理、光照、楼梯模型和玩家 FOV。模型可以在软件图中自证“轮廓可读”，但真实客户端中 primitive massing、墙面尺度、屋顶厚重感和构件比例可能明显更差。

这进一步说明未来客户端自动截图 / 指定观察点工具价值很高。

## v1.6 regression assessment

| v1.6 change | T08 result |
|---|---|
| Massing Gate exists | **YES** |
| Monochrome / silhouette review | **YES** |
| Section / roofline consciously discussed | **YES, but insufficient** |
| Box-first generation prevented | **NO** |
| Massing materially improved enough to pass specialist test | **NO** |
| Gate catches unresolved roof/mass junctions | **NO** |

因此最准确的结论是：

> **v1.6 changed the procedure, but did not yet reliably change the underlying architectural design method.**

## Recommended next direction

暂时不要通过继续加入更多“塔、屋顶、凹凸、层级”名词来修补，因为模型已经会列这些词。

下一版更值得解决两个更底层的问题：

1. **Architectural Tectonics / Structural-Spatial System**  
   对依赖结构体系的建筑，先识别 bay / span / supports / vertical section / roof-vault system / circulation，再让 massing 从这些关系产生；不得先完成通用 shell 后再把风格构件覆盖上去。

2. **Stronger Massing Gate**  
   Gate 从“可读主次”升级为：
   - proportion；
   - volumetric composition；
   - major mass junctions；
   - roof transition；
   - tectonic causality；
   - silhouette quality；
   - secondary-mass quality。

必要时在复杂 / 重要建筑中使用一次 Architect → Critic → bounded Revision，但不必将多 Agent 流程强制到所有普通建筑。

## Owner feedback status

本文件在 Owner 尚未提供具体 T08 问题清单前完成，作为独立审核基线。后续 Owner 实机反馈应追加对照，不回写本次独立判断本身。
