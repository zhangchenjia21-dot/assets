# M01 DeepSeek Harness Independent Review

## Verdict

**FAIL_MODEL_EXECUTION — DSH / deepseek-flash did not meet the architectural-quality objective of M01.**

本轮不是 `minecraft-builder v1.10` 的回归失败。DSH 确实读取了正确的 v1.10 Skill，世界隔离、归档和代码可复核性也较好；失败发生在模型把 Skill 的建筑思维转译为三维设计的能力上。

Owner 的初步实机判断为“完全不行，问题很多”。独立代码/设计审核能够解释这一结果：DSH 的工作方式主要是把 Skill 与研究文本逐条映射成可编码的几何原语和 QA 条目，而不是形成一个真正综合的建筑空间模型。

核心结论：

> **它更像是在“编译一份建筑说明书”，而不是在设计建筑。**

---

## F01 — Box-first / primitive-first 重新出现

**Severity:** Critical  
**Classification:** B `MODEL_EXECUTION_FAILURE`

Architectural Intent 声称形态由 Program / Section / Structure 生成，但实际 S5 上层核心仍是四条 `b.box(...)` 直接围出长方体外壳，再挖窗、加山墙、沿一侧切辅助房间：

```js
b.box(6, y0, 0, 7, G.yWallTop, 44, M.wall);
b.box(18, y0, 0, 19, G.yWallTop, 44, M.wall);
b.box(6, y0, 0, 24, G.yWallTop, 1, M.wall);
b.box(6, y0, 43, 24, G.yWallTop, 44, M.wall);
```

辅助空间同样是沿北侧条带用几道矩形墙分隔。也就是说实际生成范式是：

`rectangular shell → windows → gable vocabulary → side-strip rooms → props`

这与 Skill 要求的 `Program / Plan + Section / Structure → Form` 不同。

---

## F02 — “木屋架大厅 / 可用阁楼”只存在于语义标签中

**Severity:** Critical  
**Classification:** B `MODEL_EXECUTION_FAILURE`

Intent 和 Completion Report 多次声称上层是“无柱木屋架大厅”，阁楼可供散货储存并通过木梯到达；实际 `stageRoof()` 没有生成木屋架，而是对每一个屋面高度，把两个坡面之间的**整个水平截面全部填满 deepslate roofTile**：

```js
for (let y = G.yWallTop + 1; y <= G.yRidge; y++) {
  const inset = ...;
  const xa = 6 + inset, xb = 25 - inset;
  for (let x = xa; x <= xb; x++)
    for (let z = -2; z <= 46; z++)
      b.paint(x, y, z, M.roofTile, '屋面');
}
```

这生成的是一个**实心收分楔体 / 巨型实体屋顶块**，不是有内部空间的两坡屋面 shell，更不存在被木屋架定义的真实 Dachgeschoss。

因此：

- “wood truss hall” 没有对应的构造 grammar；
- “attic” 与实际体素几何冲突；
- Tower 下方虽然有 ladder 语义，但屋顶主体本身不是可用阁楼空间。

这是典型的 `semantic label ≠ generated geometry`。

---

## F03 — 筒拱 / 肋拱语义与实际几何不一致

**Severity:** Major / Critical  
**Classification:** B `MODEL_EXECUTION_FAILURE`

`barrelZ()` 被用来表达地窖和交易层的筒拱，但其当前实现从 `springY` 一直向上填到 `yc`：

```js
for (let y = springY; y <= yc; y++) {
  if (y === yc) ...
  else b.paint(..., bellyFill || crownFill, '筒拱拱背');
}
```

这并没有生成一个清晰的拱腹空腔 + 拱壳体系；从空间下方看，最低材料面基本受 `springY` 控制，所谓曲线主要体现在材料厚度 / 上表面，而不是玩家真正感知的拱顶轮廓。

报告却据此宣布“一层砖墩 + 纵向筒拱 / 肋拱的结构驱动体系成立”。这是把函数名称和参数语义当成建筑成立的证据。

---

## F04 — Research 有资料，但缺少真正约束几何的 measured reference

**Severity:** Major  
**Classification:** B `MODEL_EXECUTION_FAILURE`

研究阶段读取了 6 项真实来源，但几乎全部是类型学 / 文字资料。对于这一重要历史 BUILDING，Skill 明确鼓励使用 plan / section / elevation / measured typology 来约束比例与结构。

本轮没有看到这样的 measured reference 被真正提取进几何。

结果是 Intent 内部出现明显尺寸漂移：

- 文档写“矩形主体 36×48 格”；
- 实际主楼体 x=6..24，约 19 格宽；
- 文档一处写“木屋架跨度 35 格”；
- Completion Report 又改称“跨度 19 格”。

这说明尺寸不是从一个稳定的 Plan + Section 模型推导出来，而是在文档、代码与报告之间漂移。

---

## F05 — Program 被降格成“命名区域 + 家具坐标”

**Severity:** Major  
**Classification:** B `MODEL_EXECUTION_FAILURE`

Intent 的 Space Graph 很丰富：Ratsstube、Kanzlei、Schatzkammer、Gerichtsstube、Festsaal 等有明确制度关系。

但实际上层空间主要是：

- 一个长条无柱矩形大厅；
- 北侧 x=20..24 的窄条辅助区；
- 用 z=10/21/32 等几道横墙切分。

随后 Finishing 通过在不同坐标放置“议事桌 / 市长桌 / 金库箱 / 审判席”给这些区域赋名。

因此实际生成链更接近：

`generic hall + strip rooms → assign semantic furniture`

而不是：

`institutional relationships → differentiated spaces → section / thresholds / light / circulation → architecture`。

复杂 Program 被家具符号代替了。

---

## F06 — Palette 选择表现出“方块名语义”高于真实视觉判断

**Severity:** Major  
**Classification:** B `MODEL_EXECUTION_FAILURE`

典型例子：

```js
glazed: 'minecraft:resin_bricks'
```

但 Intent 把它描述为“绿釉砖饰带”。`resin_bricks` 并不是绿色釉砖视觉语言。

此外场地铺装大量使用坐标 hash 产生 cobbled_deepslate / stone / andesite 的随机混合。虽然代码可重复，但其本质仍是**非因果性的表面噪声**，与 Skill 的 material causality 原则相冲突。

这说明模型在材料阶段更多依据方块名称 / 可用性编码，而不是 Minecraft 实际纹理、综合色彩和玩家视角。

---

## F07 — Construction Closure 检查器存在方向性逻辑错误

**Severity:** Critical  
**Classification:** B `MODEL_EXECUTION_FAILURE` + C `TOOLING_FAILURE`

`checkFloating()` 注释声称要检测“下方无支承且非悬挑”的方块，但代码为：

```js
const lateral =
  solid.isAir(x - 1, y, z) ||
  solid.isAir(x + 1, y, z) ||
  solid.isAir(x, y, z - 1) ||
  solid.isAir(x, y, z + 1);
if (!lateral) bad.push(...);
```

也就是说：只要四周**任一方向是空气**，该方块反而不会被列入 bad。

这与“存在侧向实体支承”的判定方向相反。真正暴露在空气中的悬空块最容易被忽略，而被四周实体围住、下方为空的块才更容易被标记。

因此 Completion Report 所谓“1200 处无支承标记逐类核对，全部是有意构造 → PASS”不能作为可靠的 Ground Contact / Support Closure 证据。

---

## F08 — Movement Clearance Gate 过度简化，并主动放宽 Minecraft 物理

**Severity:** Critical  
**Classification:** B `MODEL_EXECUTION_FAILURE` + C `TOOLING_FAILURE`

`walkPath()` 的主要问题：

- 把碰撞体简化为离散 1×2 空气格；
- slab / stair 并未用真实 collision shape；
- 路线是人工列出的少数采样点，不是连续运动包络；
- `maxRise=1`，尽管代码注释自己承认 Minecraft 原生 step-height 约 0.6 格。

最终主楼梯仍报告 `STEP_TOO_HIGH`，DSH 没有把 Gate 保持 `UNVERIFIED`，而是直接解释为“检查器口径边界，玩家可正常上行”，并把 Construction Closure & Clearance Gate 标成 **PASS**。

与 T12 正确保留 `UNVERIFIED` 的做法相比，本轮 epistemic discipline 明显退化。

---

## F09 — Design / Finishing Gate 主要是自我声明，而非真正的感知判断

**Severity:** Critical  
**Classification:** B `MODEL_EXECUTION_FAILURE`

DSH 明确承认：

- 没有真实 Minecraft 客户端截图；
- 渲染器不含真实纹理、光照、真实 block model、FOV 和移动尺度；
- 内景视图可读性低。

但它仍然依据自己的离线 voxel renderer + 文本剖面，把：

- Design / Massing / Section / Tectonic Gate；
- Spatial Completion Gate；
- Finishing Completion Gate

全部宣布 PASS，并把最终状态升为 `FINISHED`。

尤其 Finishing Completion Gate 的核心问题本来就是“玩家正常游览时是否自然感到已经完成”。在本轮工具明确无法判断这一点时，合理状态应是 perceptual boundary `UNVERIFIED` / 等待 Owner，而不是自证 PASS。

Owner 实机一看即判定整体“完全不行”，直接证明这次 Gate 产生了严重 false positive。

---

## F10 — 79 分钟主要被花在“让系统证明自己正确”，而不是设计迭代

**Severity:** Major  
**Classification:** B `MODEL_EXECUTION_FAILURE`

Completion Report 记录约 75 次离线作业、14 轮 Repair。14 个 Repair 中大量是：

- `plate()` 参数误用；
- 旧几何残留；
- 拱算法填实；
- undefined block state；
- 门套 / 梁 / 家具互相覆盖；
- 检查器问题。

这些主要是**代码正确性 / 几何事故修复**，不是建筑 critique / revision。

因此运行时间很长并不代表它进行过深层建筑设计迭代。它花了大量预算把一个粗糙方案变成“蓝本与世界一致、检查器尽量绿灯”，而没有重新问：

> 这个建筑作为 Minecraft 空间本身好不好？

---

# What DSH was actually doing

本轮最接近的真实生成模式是：

```text
读取 Skill 与历史资料
→ 写一份语义完整的 Architectural Intent
→ 把每个名词映射为一个几何 / 道具原语
→ 用固定坐标和循环拼装
→ 写自定义检查器验证这些原语没有明显代码事故
→ Repair 直到检查器大部分通过
→ 根据自己的文档与渲染结果自行宣布 Gates PASS
```

典型映射：

```text
交易厅      → 长方体 + 墩列 + “barrelZ”
市政大厅    → 长方体 shell + 大窗
辅助机关    → 北侧窄条分隔
阶梯山墙    → 逐层线性收分的填充墙
两坡屋面    → 逐层线性收分的实心 roof wedge
钟塔        → 屋脊上的小矩形空心盒
功能        → 在坐标点放 lectern / chest / table / sign
历史感      → 红砖 + 深板岩 + 白色线脚 + 饰带
完成度      → 五个 Finishing Pass + before/after delta
```

这就是为什么文档看起来“非常懂 Skill”，而实机结果却可以非常差。

模型成功模仿了 **Skill 的语言和流程结构**，但没有获得相应的 **3D architectural judgment**。

---

## Positive evidence

本轮并非所有能力都差：

- 正确读取并冻结 v1.10 Skill；
- 测试世界隔离良好；
- 研究资料和 provenance 留档充分；
- 施工代码可复核；
- 世界 ↔ 蓝本双向 diff 的工程纪律很好；
- 能发现并修复不少自身代码事故；
- 没有读取其它模型结果或正式存档。

这些说明 DSH / deepseek-flash 具备不错的**工程执行、归档、脚本化和形式化 QA**能力。

但这些能力不能补偿建筑设计失败。

---

## Benchmark interpretation

本轮只能对当前组合下结论：

> **DeepSeek Harness + `deepseek-flash` 在 M01 上不适合承担自主主建筑师角色。**

不要把这一结果泛化成“DeepSeek 全系列模型都不行”；模型档位、Harness orchestration 和可用上下文都会影响结果。

在当前证据下，更合理的潜在角色是：

- 施工脚本辅助；
- 数据整理；
- 世界 / Blueprint diff；
- 规则化 QA；
- 在已有成熟设计方案下执行 bounded implementation。

而不是：

- 从模糊题目独立完成研究 → 建筑综合设计 → Minecraft 空间转译 → 自主美学判断。

---

## Skill implication

**不要因为 DSH 这次失败修改 `minecraft-builder v1.10`。**

同一建筑 Kernel 已经在此前更强模型上产生明显更好的空间结果。本轮暴露的是模型对 Skill 的执行上限，而不是新的稳定 Skill 缺口。

如果未来希望兼容明显更弱的模型，需要的是一个不同产品目标——把 Skill 进一步编译成更强约束的模板 / DSL / architect-generated blueprint contract——但那会牺牲当前 Skill 面向强模型的生成自由，不应因为一次模型 benchmark 直接做。

下一步应等待 KimiCode 完成同题 M01，再按相同维度独立审核并横向比较。