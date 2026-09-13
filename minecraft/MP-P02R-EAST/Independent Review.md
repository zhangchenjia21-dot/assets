# MP-P02R Independent Review｜minecraft-planner v0.3

日期：2026-09-13  
审核对象：`minecraft/MP-P02R-EAST/`  
实现提交：`51ee54963705ccd4b616552466d27785c42bbe46`  
测试：`MP-P02R｜CIV-001 东域山地共同体系统 / REGIONAL_SYSTEM`

## Verdict

> **PASS_WITH_NOTES — v0.3 的 Surface / Substrate / Land-Cover 修复已在真实区域规划中生效；可进入 L2 SETTLEMENT 测试。**

本轮最关键的问题不是“Codex 有没有在文档里写到石头”，而是：**地表差异是否真正改变了规划角色、容量分配、形态和下游调查要求。** 独立复核结果为 YES。

MP-P02R 不再只把北台地理解成“较平的 Y≈130 台地”。它从 R1 `exposed_state` 逐列分类 surface family，并结合 4-block vegetation sample、坡度与起伏，对四个候选窗分别建立 surface profile。北部 NODE-01 被识别为约 78.72% ROCK_SURFACE、2.75% SOIL_SURFACE、18.35% SAND_GRAVEL；NODE-02 则约 86.94% SOIL_SURFACE、12.59% ROCK_SURFACE。该差异随后改变了两者的规划分工，而不是停留在地图着色层。

---

## 1. Surface evidence 是否真实进入 Planner

### PASS

本轮实际读取：

- `exposed_y`
- `exposed_state`
- `artificial_material`
- `land_component`
- `slope8`
- `relief32`
- 4-block vegetation sample

并把地表显式分类为：

- `SOIL_SURFACE`
- `ROCK_SURFACE`
- `SAND_GRAVEL`
- `TERRACOTTA_SURFACE`
- `MUD_CLAY`
- `SNOW_ICE`
- `SURFACE_PLANT`
- `OTHER_UNRESOLVED`

分类表、unknown policy 和 state dictionary 已归档。`substrate` 继续保持 `UNRESOLVED`，没有把 surface block 伪装成土深、岩层或地质剖面。

这修复了 MP-P02 的 foundational gap：Planner 现在不再只知道“平不平”，而能知道“这块平地是什么表面”。

---

## 2. 北岩台差异是否真正改变规划

### PASS

NODE-01 北岩台：

- ROCK_SURFACE ≈ 78.72%
- SOIL_SURFACE ≈ 2.75%
- SAND_GRAVEL ≈ 18.35%
- leaf sample presence ≈ 0.14%

Planner 因此没有把其较大缓地面积解释成“适合扩大常住人口”。相反，它把 NODE-01 的角色收敛为：

> 共享交割、维修、储备和吞吐服务面；常住不能随平岩面积膨胀，稀缺土面优先保留调查。

其 capacity 仍为低置信度 3.5k–8k blocks²，但 household pressure 只有 12–24，较大部分面积来自 shared service pressure，而不是把裸岩台全部转成住宅。

NODE-02 西肩：

- SOIL_SURFACE ≈ 86.94%
- ROCK_SURFACE ≈ 12.59%
- leaf sample presence ≈ 11.32%

它被赋予更多家庭生活 / 地方共同体支援角色，household pressure 18–36；同时明确要求保留连续土面、不得因“绿色”就自动铺成聚落，也不得把 grass/dirt 直接解释为肥沃农田。

因此 surface character 实际改变的是：

```text
北岩台 → 吞吐 / 共享服务权重 ↑，常住压力受限
西肩草土 → 家庭 / 日常生活权重 ↑，但生产能力仍待证
```

这是有效的因果规划，不是 cosmetic annotation。

---

## 3. Surface Necessity Test

### PASS

Planner 自检提出：

- 如果北岩台换成草土，土面保留压力、本地供给调查和常住分配应改变；
- 如果西肩草土换成裸岩，其家庭支援优势会下降。

独立检查 planning objects / handoff 后，这个反事实是有实际后果的：节点 role、household allocation、morphology、surface-specific requirement 都会变化。

因此当前方案不能简单平移到一个相同 slope / relief、但地表不同的山地世界而保持不变。

---

## 4. 未出现过推断

### PASS

本轮正确保留了以下边界：

- exposed rock ≠ quarry / ore deposit；
- exposed ore block 被归入 rock-like surface 时，不升级为矿床证据；
- grass / dirt ≠ fertile farmland；
- terracotta surface ≠ 已证黏土工业资源；
- leaf presence ≠ sustainable timber yield；
- exposed surface ≠ substrate / soil depth；
- gentle columns ≠ net buildable area；
- artificial flag ≠ 已识别 settlement fabric。

南部 NODE-03 / NODE-04 也不是用“哪个更绿”机械决定。NODE-04 草土更多但 Y≈253，Planner 仍保留高程 / 运输成本；NODE-03 较低但岩面 / terracotta surface 更多。两者保持互斥条件分支，没有把 surface 优势覆盖 terrain resistance。

---

## 5. Recursive handoff

### PASS

三个下游包继续交给 `SETTLEMENT` Planner，而不是 Builder。

尤其 PACKAGE-01 / PACKAGE-02 已把 surface evidence 作为下游输入，并要求下一尺度继续解决：

- current built fabric / road / tenure；
- stable water；
- rock fracture / soil depth / substrate / erosion；
- vegetation / land use / renewal；
- actual resource location and supply pressure；
- usable route geometry。

同时保留迁移、拆分、缩容、季节化和 upstream revision trigger。

这说明 v0.3 没有把 surface classification 误当成最终 Site Gate，而是正确地把它作为 L1→L2 约束与待解证据。

---

## 6. Capacity / Morphology

### PASS_WITH_NOTE

本轮没有因为裸岩而套一个统一 `rock penalty`，这是正确的。北部总 capacity 仍大致保持上游 6k–14k 压力量级，但内部角色分配发生改变：服务更多落在岩台，家庭生活更多落在草土西肩。

这比简单把所有 rocky land 容量打 50% 更合理，因为当前仍缺：

- stable water；
- actual soil depth / substrate；
- food carrying capacity；
- current settlement fabric；
- actual resource location；
- usable transport route。

因此 **surface 已影响 planning，但尚不足以独立定量确定 carrying capacity**。当前 LOW confidence 与 L2 继续调查是正确状态，不构成新的 Skill gap。

---

## 7. Visual / artifact evidence

本轮生成并验证五张正式地图：

- 地形与区域交换关系
- 地表差异与候选规模
- 植被采样与开放地压力
- 候选区域同范围比较
- 关系线地形探针

地图生成逻辑、artifact hash、确定性重建和引用关系均完整。Connector 环境不能直接对仓库 PNG 做像本地图片查看器一样的像素级人工审美检查，因此 Owner 对地图是否“直观好读”的肉眼体验仍是最终视觉判断来源；这不影响对 underlying planning data / map semantics 的独立审核。

---

## 8. Notes / Remaining boundaries

### NOTE-01｜Surface ≠ substrate

当前只有 exposed-state surface evidence。岩台是否存在浅覆土、裂隙、稳定基岩、排水问题，草土是否只有一层薄覆土，都还不知道。L2 必须继续调查；当前 Skill 已正确要求这一点。

### NOTE-02｜Vegetation proxy 仍然粗

植被是 4-block sample，主要用 presence ratio，不应作为冠幅、木材量或生态产能。当前方案没有越界，但 L2 若要讨论生活支持 / 林料，应补更局部证据。

### NOTE-03｜当前实存仍未观察

`EXISTING_FABRIC_UNVERIFIED` 继续成立。不能拿本轮 surface map 当作“天然空白土地”证明。

这些均属于正常的下层 evidence boundary，不要求继续修改 v0.3。

---

## Final decision

> **MP-P02R = PASS_WITH_NOTES**

> **minecraft-planner v0.3 的 Surface / Substrate / Land-Cover foundational fix 已通过真实东域 REGIONAL_SYSTEM regression。**

当前没有证据要求继续给 Skill 增加 task-specific 规则。下一步可以进入 `SETTLEMENT` 尺度测试，并优先选择 **NODE-01 北岩台集散候选**，因为它能继续检验：

```text
裸岩主导地表
+ 稀缺土面保护
+ 共享服务 / 常住分离
+ 山地高差
+ 当前实存未知
↓
完整 settlement morphology
```

L2 必须保持 `world writes = 0`，先完成现状、供水、substrate、可通行性、anchor / district / capacity 精化，再决定是否继续向 L3 下钻。
