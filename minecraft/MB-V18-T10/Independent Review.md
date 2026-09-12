# T10 Independent Review｜v1.8 Finishing Isolation

## 结论

**独立暂定判定：PASS_WITH_FINDINGS**

> T10 的专项目标不是证明 v1.8 已经可以完整生产，而是验证：一个已经达到 `SPATIAL_COMPLETE` 的 Builder Core，在进入 Finishing 后，是否能够提高近景完成度，同时保持上游设计、空间、结构、水体与交通不被重新设计。

就当前归档代码、逐坐标账本、局部连接检查、phase protection 与重载证据而言，这个目标成立。没有发现阻断级 `SKILL_GAP`，也没有发现 Finishing 借“精修”之名重做 Builder Core。

最终是否在玩家真实视角下足以称为 `FINISHED`，仍等待 Owner Minecraft 客户端巡检。客户端感知是当前审计尚未闭合的主要证据缺口。

---

## 1. 核心判断：v1.8 的阶段隔离不是停留在文档层

Spatial Completion Gate 在任何精修写入之前重新检查了原 T09 的 Spatial Logic、14 条局部预期连接、Massing / Section、结构环境、Minecraft usability 与 Upstream Defect Test，并明确冻结 Program / Space Graph、主体量、Plan / Section、主屋顶、主入口、主要交通、地形、水体、池体、skyline 和空间序列。

本轮实际生成代码也体现了这个边界：Finishing 从 `00-Baseline` 实存数组出发，仅生成增量；所有写入被限制在 `y < 24`，禁止修改 water；新增家具只能写入 air，表面精修只能替换现有实体。最终 phase protection 记录 326 个相对基准变化、0 个未解释变化、Y24+ 变化 0、水状态变化 0、基准实体删除 0，14 条预期连接仍全部成立、0 orphan。

因此本轮可以确认：

> **Finishing 继承了上游设计意图，但没有继承重新设计 Core 的权限。**

这是 v1.8 最重要的专项回归结果。

### T10-F01｜Finishing Phase Isolation 成立 — Positive Regression

**Severity：Positive / Core Target Pass**  
**Classification：v1.8 DESIGN SUCCESS**

实际精修没有修改主平面、主体量、屋顶、水体、主要 circulation、空间序列或功能分区；Restricted 修改仅为后勤院外 10 格 `grass_block → coarse_dirt`，保持原标高和路线语义。

这证明 `Spatial Completion Gate → freeze Core → Finishing` 的架构可以实际执行，而不只是 Skill 文本中的理想流程。

---

## 2. Finishing 决策总体符合“从原因产生细节”

本轮没有采用“看哪里空就塞什么”的方式。

实际 Functional pass 主要集中在明确活动节点：更衣空间增加可使用储物、入口管理台，热浴边增加少量浴后用品台，后勤燃料院增加整理工作台和储存；Material pass 把烟熏放在炉口上方，把磨损放在集中入场路径，把踩踏地面放在服务院边缘；Composition pass 只调整少数低位任务光源，并主动把冷厅中央、上部拱顶、热池周边、运动庭院作为 Quiet 区域保留。

### T10-F02｜Use / Material / Attention 三条因果链实际进入施工 — Positive Regression

**Severity：Positive**  
**Classification：v1.8 DESIGN SUCCESS**

至少可以从生成代码中追溯出：

- changing use → storage / management；
- bath use → small supply surface；
- fuel handling → work surface / storage；
- furnace smoke source → local soot gradient；
- entrance foot traffic → localized wear；
- monumental hall / palaestra → deliberate quietness。

这与“统一密度装饰”“随机做旧”有本质区别。

---

## 3. Restraint Pass 是真实删除，不是报告措辞

05-Restraint 实际删除了：

- 第二只浴后器皿；
- 一只重复储桶；
- 6 格冷厅中央小型嵌饰，并恢复为原 T09 基准。

### T10-F03｜Restraint 具备真实反向编辑能力 — Positive Regression

**Severity：Positive / Important**  
**Classification：v1.8 DESIGN SUCCESS**

Finishing Agent 不再只会连续增加 detail；它能够判断某些新细节抢占工作面、制造重复或分散主空间注意力，并主动撤销。

对于未来大型正式项目，这一能力比“更多细节”本身更重要。

---

## 4. 仍需 Owner 实机决定的问题：`FINISHED` 的阈值是否过宽

最终相对巨大浴场 Scope 只保留 326 格净变化。这个数字本身既不能证明太少，也不能证明合理；Finishing 的正确目标本来就不是提高 block count。

从代码逻辑看，克制是有意的，而且大部分 Quiet 区域有合理原因。但当前工具没有原生 Minecraft 客户端视角，因此仍无法独立确认：

- 更衣室是否已经从“毛坯 + 箱子”提升为可信使用空间；
- 热室下墙材料带在真实纹理下是否自然，还是显得过于条带化；
- 冷厅大尺度留白是庄重还是仍显 unfinished；
- 运动庭院的安静是否成立；
- 低位蜡烛在真实 FOV / 光照下是否形成空间层级；
- 整体精修增量是否足以支持状态从 `SPATIAL_COMPLETE` 升级到 `FINISHED`。

### T10-F04｜FINISHED Threshold 仍是感知型 WATCH

**Severity：WATCH / potentially Major if Owner disagrees**  
**Classification：TOOLING_LIMITATION + possible SKILL_GAP**

当前建议不因这一项立刻修改 Skill。先由 Owner 实机确认。若 Owner 明确感觉“隔离做得很好，但仍只是半成品”，则说明 Spatial Completion Gate 很成功，而 **Finishing Completion Gate / FINISHED 状态定义偏宽**，这会成为 v1.8 需要优先修订的抽象问题。

---

## 5. 道具语义成立，但历史与视觉特异性仍有限

更衣区使用 8 个 Vanilla chest 表达反复使用的保管点。它们具有 Minecraft 原生可交互性，位置和净空也经过检查；但从历史/视觉表达上，它们可能更容易读成“Minecraft 一排储物箱”，而不是罗马浴场的衣物保管、壁龛、架位或 attendant-managed storage。

热浴用品通过 flower pot 抽象为小器皿也存在类似问题。

### T10-F05｜Functional Prop Vocabulary 仍较 Generic

**Severity：Minor / WATCH**  
**Classification：MODEL_EXECUTION_FAILURE + TASK_SPECIFIC_JUDGMENT**

这不是当前证据下的 Skill 底层缺陷。Skill 已要求细节来自使用；本轮确实做到了。下一步缺的是更成熟的 Minecraft prop translation / asset vocabulary，而不是再增加“更衣室必须用什么”之类的硬规则。

Owner 实机时建议特别观察：这些 props 是强化“真实有人使用”，还是首先让人想到 Vanilla storage wall。

---

## 6. Architectural Refinement 本轮主要证明“克制”，没有充分覆盖其能力上限

277 格 Architectural pass 大部分是已有实体表面的材料替换：入口石材收口、冷厅地坪边饰、热室可擦洗下墙与压顶。它没有大规模新增门窗深度、檐口、柱头、栏杆、屋脊等几何 refinement。

### T10-F06｜Architectural Refinement Coverage 偏窄，但不构成失败

**Severity：Minor / Coverage Limitation**  
**Classification：TASK_SPECIFIC_JUDGMENT**

T10 的目标是 Existing Build Isolation，而不是强迫每一个 Finishing 模块都产生修改。原 T09 建筑本身已经有明确构造，本轮保守处理反而符合隔离目标。

因此不要因为“这一轮没展示全部 Finishing 技巧”就给 Skill 添加强制细节量。T11 从零端到端测试更适合验证 Architectural Refinement 是否自然发生。

---

## 7. Phase Protection 当前实现对本轮足够，但不是通用语义证明器

本轮保护脚本通过：

- Y24+ 全冻结；
- water 状态冻结；
- 禁止 baseline solid → air；
- 修改账本全解释；
- 14 条预期 edge 保持；
- orphan = 0；

对 T10 这种预先已知 Scope 非常有效。

但这些条件并不能一般性证明所有 Frozen semantic 都未改变。例如未来某建筑的核心室内系统本来就在 Y24 以下，理论上仍可能通过“solid→solid 材料替换 / air→prop”在不违反这些指标的情况下破坏视觉语义。

### T10-F07｜Phase Protection 是强防线，不是完整 semantic diff

**Severity：WATCH**  
**Classification：TOOLING_LIMITATION**

本轮通过人工/代码审阅没有发现实际越权，所以不影响 T10 结论。未来若工具化，可考虑让 Builder Core 输出更明确的 protected regions / semantic interfaces；目前不建议为此增加 Skill 文本复杂度。

---

## 8. 仍未闭合的工具证据

### T10-F08｜Real Client Perception / Interaction / Lighting 仍未验证

**Severity：Major Evidence Gap, not design failure**  
**Classification：TOOLING_LIMITATION**

当前仍缺：

- 原生客户端实际行走；
- chest 打开等真实互动；
- 真实方块模型与碰撞；
- 日夜光照；
- 原生 FOV / 纹理下的 detail density；
- controlled fluid tick。

静态活动点验证显示新增站位具有两格净空、8 个箱盖上方有空间，但 `native_interaction_tested=false`。因此 Owner 实机巡检对 T10 不是锦上添花，而是完成最终感知判断所必需的证据。

---

# 维度审计

| 维度 | 独立判断 |
|---|---|
| Spatial Completion Gate | **PASS**：没有靠重建 Core 获得精修资格 |
| Builder / Finisher Isolation | **PASS** |
| Frozen Core Protection | **PASS in this sample** |
| Functional Finishing | **PASS_WITH_FINDINGS** |
| Material / Aging causality | **PASS** |
| Lighting logic | **PASS structurally / client unverified** |
| Focal / Supporting / Quiet hierarchy | **PASS by implementation; perceptual confirmation pending** |
| Restraint | **PASS，且是真实删除** |
| Prop specificity | **WATCH** |
| Over-detail | **未发现** |
| Under-finish | **Owner perceptual review pending** |
| Circulation preservation | **PASS** |
| Water preservation | **PASS statically; fluid tick unverified** |
| Real-client player experience | **UNVERIFIED** |

---

# 对 v1.8 的当前建议

**暂不修改 Skill。**

T10 没有暴露需要立即修订 v1.8 的阻断级问题。相反，它第一次给出了较强证据，说明 Integrated Finishing 的隔离、因果细节、视觉层级与 Restraint 机制能够按设计运行。

如果 Owner 实机巡检没有发现 Critical / Major 的 Finishing 问题，则应保持当前 v1.8 commit 不变，直接执行 **T11 From-Zero End-to-End Regression**。这样 T11 才能检验同一个 Skill 版本是否能够从 Architectural Thinking 一路自然推进到 FINISHED，而不是测试一个被 T10 结果污染后修订过的版本。

如果 Owner 发现的是局部 prop、颜色、灯光、材料带之类问题，先记录为 T10 finding，不应自动改 Skill；如果 Owner 发现的是系统性问题，例如“空间没有被破坏，但整个 Finishing 几乎没有提升完成度却自行宣告 FINISHED”，则应暂停 T11，先讨论 `FINISHED` Gate 是否存在基础缺口。

---

## Owner Client Review｜待补

等待 Owner Minecraft 客户端实机巡检结果后补充最终判定。
