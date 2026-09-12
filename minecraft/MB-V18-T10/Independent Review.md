# T10 Independent Review｜v1.8 Finishing Isolation

## 结论

**最终判定：FAIL_TARGETED_REGRESSION**

> T10 的阶段隔离成功，但 `SPATIAL_COMPLETE → FINISHED` 的精修效果没有达到玩家可自然感知的完成度提升。

这不是因为 Finishing 破坏了 Builder Core。相反，`Spatial Completion Gate → Freeze Core → Finishing` 在本轮执行得非常好。失败点在另一端：**v1.8 当前能够做到“正确而克制地改一点”，但还不能可靠判断“什么时候已经真的精修完成”。**

Owner 原生 Minecraft 客户端巡检的关键反馈是：

> **精修幅度偏小；如果不被提醒去看那些具体位置，几乎不会主动注意到变化。**

这直接闭合了此前最大的 WATCH：当前 `FINISHED` 阈值过宽。Finishing 不应以 block count 为目标，但如果正常玩家沿主要路线游览时几乎感知不到从 `SPATIAL_COMPLETE` 到 `FINISHED` 的差别，就不应升级为 `FINISHED`。

因此 T10 应拆开判断：

- **Builder / Finisher Isolation：PASS**；
- **Frozen Core Protection：PASS**；
- **Finishing causal logic：PASS**；
- **Finishing perceptual effectiveness / FINISHED threshold：FAIL**；
- **T10 Overall：FAIL_TARGETED_REGRESSION**。

---

## 1. 强正向结果：v1.8 的阶段隔离真实成立

Spatial Completion Gate 在任何精修写入之前重新检查了原 T09 的 Spatial Logic、14 条局部预期连接、Massing / Section、结构环境、Minecraft usability 与 Upstream Defect Test，并冻结 Program / Space Graph、主体量、Plan / Section、主屋顶、主入口、主要交通、地形、水体、池体、skyline 和空间序列。

实际生成代码也执行了这一边界：Finishing 从 `00-Baseline` 实存数组出发，只生成增量；写入限制在 `y < 24`，禁止 water 修改；新增家具只能写入 air，表面精修只能替换现有实体。

最终 phase protection：

- baseline changed cells：326；
- unexplained changes：0；
- Y24+ changes：0；
- water state changes：0；
- baseline solid removed：0；
- 14 条 expected edges：全部保持；
- orphan cells：0。

来源 T09 的 87 个文件也保持原 SHA256；T09 与 `建筑师` 的世界写入均为 0；最终零施工 reload 与最终保存快照一致。

### T10-F01｜Finishing Phase Isolation 成立 — Positive Regression

**Severity：Positive / Core Target Pass**  
**Classification：v1.8 DESIGN SUCCESS**

> **Finishing 继承了上游 Intent，但没有继承重新设计 Core 的权限。**

这一点应完整保留，不能因为后续要增强 Finishing 效果而放宽 Frozen 边界。

---

## 2. Finishing 的因果逻辑本身是对的

本轮没有采用“哪里空就塞什么”的策略。

实际施工可追溯出：

- 更衣活动 → 储物 / 管理台；
- 浴后活动 → 少量用品台；
- 燃料维护 → 工作台 / 储存；
- 炉口 → 局部烟熏；
- 高频入口 → 局部磨损；
- 冷厅 / 穹顶 / 运动庭院 → deliberate quietness。

### T10-F02｜Use / Material / Attention 因果链进入施工 — Positive Regression

**Severity：Positive**  
**Classification：v1.8 DESIGN SUCCESS**

问题不是“细节没有原因”，而是**有原因的细节覆盖面与感知强度不足**。

---

## 3. Restraint 机制真实有效，但出现了新的平衡问题

05-Restraint 实际删除了第二只浴后器皿、一只重复储桶，并撤销 6 格冷厅中央嵌饰，恢复为 T09 基准。

### T10-F03｜Restraint 具备真实反向编辑能力 — Positive Regression

**Severity：Positive / Important**  
**Classification：v1.8 DESIGN SUCCESS**

Agent 已经会删东西，这是重要能力。

但 T10 同时表明：**当前 Skill 对 restraint 的约束强于对 finishing coverage 的约束。** 模型非常谨慎地避免 over-detail，却没有同等强的机制防止 `under-finish`。

> **Restraint ≠ invisibility.**  
> **Quiet ≠ untouched.**

这应成为下一版修订的关键平衡点。

---

## 4. Owner Client Review：FINISHED 判定失败

Owner 在原生 Minecraft 客户端实际游览后的判断是：

> **“幅度偏小，不提醒我看这些地方我都注意不到。”**

这不是单个 prop、颜色或灯光的偏好问题，而是对本轮目标的直接否定。

Finishing 的目标不是让审核者通过 before/after 对照、坐标列表和提示去寻找差异，而应让正常玩家在自然游览中感受到：

> 这个空间从“建筑已经成立”进入了“建筑被真正完成、使用和维护”。

如果只有被点名后才看得见变化，那么本轮虽然完成了五个 Pass，但作品状态仍更接近：

> **`SPATIAL_COMPLETE + LIGHT_FINISH`**

而不是可靠的 `FINISHED`。

### T10-F04｜Finishing Completion Threshold 过宽 — Major / Foundational

**Severity：Major / Release-blocking for Integrated Finishing**  
**Classification：SKILL_GAP + MODEL_EXECUTION_FAILURE**

当前 Skill 已要求 Far / Mid / Near / Route Review，也列出 `Under-finish`，但没有一个明确的**精修完成门槛**要求：

- 正常玩家不依赖提示就能感知精修提升；
- 主要空间与主要路线获得足够 finishing coverage；
- Quiet 区域虽可低密度，但仍应具有有意完成的 construction / material / light / edge resolution；
- 细节不能只集中在少数孤立节点，然后把整个 Scope 宣告为 `FINISHED`。

因此当前缺失的不是“更多装饰规则”，而是：

> **Density hierarchy 已经有了，但 Finishing coverage 与 perceptual delta 没有成为 `FINISHED` 的硬语义。**

这是本轮最重要的新发现。

---

## 5. 核心抽象：区分 Detail Density 与 Finishing Coverage

T10 说明这两个概念不能混在一起。

### Detail Density

控制某个位置“多复杂”。

v1.8 已经做得较好：

- Focal 可以密；
- Supporting 中等；
- Quiet 可以稀。

### Finishing Coverage

控制整个 Scope 中“哪些空间已经被有意完成”。

当前缺口在这里。低密度不等于零处理；Quiet 区域仍可以通过：

- 清晰的建筑收口；
- 合理表面关系；
- 轻微使用痕迹；
- 光暗层级；
- 地面 / 墙脚 / 水边接口；
- 极少但准确的生活信息；

让玩家感到它是**完成后的安静**，而不是**没精修的空**。

> **A finished scene may be sparse, but it cannot feel unfinished.**

下一版不应设 block 数量配额，也不应要求每面墙都有东西；应建立“低密度但充分覆盖”的完成逻辑。

---

## 6. 道具视觉语言仍较 Generic，但不是本轮主因

更衣区使用 8 个 Vanilla chest，浴后用品用 flower pot 抽象。功能语义成立，但历史与视觉特异性有限。

### T10-F05｜Functional Prop Vocabulary 偏 Generic

**Severity：Minor / WATCH**  
**Classification：MODEL_EXECUTION_FAILURE + TASK_SPECIFIC_JUDGMENT**

即使把这些道具全部换成更漂亮的资产，也无法解决 Owner 所指出的“整体变化难以察觉”。因此不要把 T10 误诊为资产库不足。

---

## 7. Architectural Refinement Coverage 偏窄

277 格 Architectural pass 主要是已有实体表面替换：入口石材收口、冷厅地坪边饰、热室下墙与压顶。门窗深度、檐口、柱头、栏杆、屋脊、构造接口等几何 refinement 并未形成足够广泛的玩家可读变化。

### T10-F06｜Architectural Refinement 没有承担足够的中景完成度

**Severity：Major contributor**  
**Classification：MODEL_EXECUTION_FAILURE + possible SKILL_GAP**

T10 原本是隔离专项，因此保守处理本身不错误；但在最终仍宣告 `FINISHED` 的前提下，这种覆盖范围就不足。下一版应强调：Architectural Refinement 不要求处处新增几何，但应检查哪些近 / 中景 construction relationships 仍显粗糙，并形成可感知的收口。

---

## 8. Phase Protection 强，但不是通用 semantic diff

Y24+ / water / solid deletion / expected edges 等保护对 T10 很有效，但不能一般性证明所有 Frozen semantic 都未改变。

### T10-F07｜Phase Protection 是强防线，不是完整 semantic proof

**Severity：WATCH**  
**Classification：TOOLING_LIMITATION**

本轮无实际越权，因此不影响隔离结论。

---

## 9. 工具边界

### T10-F08｜Real Client Perception / Interaction / Lighting 工具仍缺

**Severity：Tooling Gap**  
**Classification：TOOLING_LIMITATION**

Codex 不能自行取得原生 Minecraft 客户端真实行走、FOV、纹理与夜景证据。Owner 实机因此仍然是最终感知验证的重要组成。

但本轮已经证明：即使没有自动客户端工具，Skill 也不能因此把“静态检查都通过”当成 `FINISHED`。当原生感知证据不可用时，状态应更保守，而不是更宽松。

---

# 维度审计

| 维度 | 最终判断 |
|---|---|
| Spatial Completion Gate | **PASS** |
| Builder / Finisher Isolation | **PASS** |
| Frozen Core Protection | **PASS in this sample** |
| Use-driven Finishing | **PASS** |
| Material / Aging causality | **PASS** |
| Restraint | **PASS** |
| Over-detail | **PASS / 未发现** |
| Finishing coverage | **FAIL** |
| Perceptual delta | **FAIL by Owner client review** |
| Architectural Refinement | **UNDER-COVERED** |
| Prop specificity | **WATCH** |
| Circulation preservation | **PASS** |
| Water preservation | **PASS statically** |
| `FINISHED` state claim | **FAIL** |

---

# 对 v1.8 的发布建议

**暂停 T11，不以当前 v1.8 直接进入第二轮。**

这正属于 T10 设计时预先约定的阻断条件：

> 如果 Owner 感觉“没破坏 Core，但整体仍不像完成后的作品”，则先修订 Finishing Completion Threshold，再做从零端到端测试。

下一版应优先修订一个抽象问题，而不是增加更多局部装饰规则：

> **建立 Finishing Completion / Perceptual Completion Gate，显式区分 detail density 与 finishing coverage，并规定 `FINISHED` 必须在正常玩家路线与近中景中产生可自然感知的完成度提升。**

同时保持：

- Architectural Thinking Kernel 不动；
- Builder Core 不动；
- Spatial Completion Gate 不动；
- Frozen / Restricted / Allowed 权限边界不动；
- Restraint 保留；
- Water / Terrain / Vegetation / Circulation 等成熟模块不动。

T10 的正确处理不是推翻 v1.8，而是保留它成功的**隔离架构**，补上 Finishing 的**完成判定架构**。
