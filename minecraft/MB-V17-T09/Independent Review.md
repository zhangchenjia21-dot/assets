# T09 Independent Review｜minecraft-builder v1.7 Architecture Thinking Regression

## Verdict

**PASS_WITH_FINDINGS**

**v1.7 targeted objective: PASS**

T09 是目前 T01—T09 中第一次能够明确看到：Skill 不只是增加了检查步骤，而是实际改变了建筑的生成逻辑。

T08 的核心失败是 `generic shell → carve → style overlay`；T09 则已经出现了较清楚的：

> Purpose / Users → Program / Space Graph → Plan + Section → Structure / Material / Technology → Form → Minecraft construction

这不是仅凭 `Architectural Intent.md` 的文字判断。生成代码本身证明了该因果链进入了实现：冷厅、暖室、圆形热室、运动庭院、厕间、炉房、服务院和高位水箱并非由同一个通用建筑壳体缩放生成，而是按各自空间职责、地坪、跨度、支承、屋顶和技术系统分别建立。

因此，v1.7 的 Architectural Thinking Kernel 在 T09 中获得了第一份强正向证据。

---

## Strong Positive Evidence

### T09-P01｜Architectural Intent 实际约束了生成器，而非文档装饰

Intent 明确了：

- 城市公共洗浴 / 运动 / 社交的存在理由；
- 公共使用与维护后勤的两套流线；
- 北入口、西运动庭院、南热区、东服务区的场地关系；
- 更衣 → 冷浴 → 暖室 → 热浴的温度 / 空间序列；
- 热区抬高以容纳 hypocaust；
- 冷厅交叉拱、暖室低筒拱、热室鼓座穹顶、柱廊木梁瓦顶等不同构造体系；
- Minecraft 中压缩绝对尺度、保留空间层级和构造可读性。

生成代码与这些意图存在直接映射，而不是完成 Intent 后重新回到 generic box-first。

**Assessment:** `ARCHITECTURAL_THINKING_KERNEL_EFFECTIVE`

### T09-P02｜Program / Space Graph 真正先于建筑形态

公共序列和后勤序列均在 Macro 阶段已经进入实际几何：

- 北入口 → 更衣；
- 更衣 → 冷厅；
- 更衣 ↔ 西柱廊 / 运动庭院；
- 庭院 → 冷厅；
- 冷厅 → 暖室 → 热室；
- 庭院 → 厕间；
- 服务街 → 服务院 → 炉房 / 检修廊；
- 服务院 → 维护梯 → 水箱平台。

与 T08 的“最终只检查目标坐标能否绕到”不同，T09 QA 对每条预期 edge 使用受限区域进行验证，不接受全局绕路替代指定接口。

最终 14 条受限连接均成立。

**Assessment:** v1.7 对 T08 Portal / Threshold 问题采取的架构性修正有效。

### T09-P03｜Section 与技术系统开始生成空间，而不是施工后补解释

T09 的高度关系不是为了 silhouette 人工拉高：

- 普通场地 / 庭院；
- 冷区地坪；
- 热区抬升地坪；
- hypocaust 空腔；
- 低暖室；
- 高冷厅；
- 鼓座与圆形穹顶；
- 高位水箱；

均对应具体使用或技术原因。

尤其暖室和热室的架空地板、砖柱、炉房接口，以及冷厅跨间 / 支承关系已经在 Macro 而非 Micro 阶段生成。

这是 T08 所缺失的 `tectonic causality`。

### T09-P04｜Form is Consequence 得到真实体现

最终不同体量可以直接追溯到不同原因：

- 长方形高冷厅 ← 大公共集合空间 + 三跨拱顶；
- 低暖室 ← 温度过渡 + 较小跨度 + 热风层；
- 圆形高热室 ← 热浴终点 + 厚鼓座 + 穹顶；
- 开敞西庭院 ← 运动、日照与通风；
- 低服务房 ← 后勤设备；
- 高水箱 ← 重力供水 / 维护系统表达。

这比单纯要求“体量高低错落”重要得多：高低和形状有了来源。

### T09-P05｜Massing Gate 从“自我确认”变成了真实的 Gate

Macro 后并没有因为“轮廓可辨”直接通过。

Gate 前实际发现并返工：

- 穹顶 / 拱壳体素接缝断开；
- 西更衣门正对冷池；
- 鼓座与穹顶支承需要强化；
- 庭院浅阶和服务接口不足。

修订后才进入 Meso。

这与 T08 的 Massing Gate false positive 有本质区别。

### T09-P06｜研究质量更适合建筑生成

研究不再只有风格词汇。

Ostia 的 Baths of Neptune 提供了实际平面与公共 / 后勤相邻关系；Pompeii Stabian Baths 提供浴场序列与 hypocaust 语境；Caracalla 主要用于大型空间和尺度辅助。

因此研究能够进入 Plan / Section / technical system，而不仅是提供“罗马建筑应该有拱券”一类表面语言。

---

## Findings

### T09-F01｜后续施工仍会破坏已定义的 Portal / Junction

**Classification:** `MODEL_EXECUTION_FAILURE / IMPLEMENTATION_PIPELINE`
**Severity:** Moderate

Meso 阶段的墙面内衬再次覆盖了入口、东门和冷暖连接，因此需要 `02-JunctionRepair` 重开指定 portal。

这次问题被现有 QA 成功捕获，并没有进入最终世界，但它说明：

> architectural semantics 已经存在，施工数据结构却还没有真正保护这些 semantics。

目前 portal 仍只是“先 carve air，后续 fill 如果覆盖再检查修复”。

**Recommendation:** 不必继续向 Skill 添加更多文字。更值得在生成器 / 工具层探索 `semantic ownership / protected interface mask`：已登记的 portal、stairs、route edge、water interface 等高价值接口在后续 fill / surface pass 中默认不可被覆盖，除非显式授权。

这是 tooling / implementation improvement，不是新的 Architectural Thinking 原则。

### T09-F02｜Micro 仍会产生局部碰撞与悬空陈设

**Classification:** `MODEL_EXECUTION_FAILURE`
**Severity:** Minor–Moderate

Micro 后发现：

- 侧座挡门；
- 8 个悬空储物格方块；
- 厕间和服务路局部衔接不足。

最终 Repair 已处理。

这说明“先正确设计建筑”显著提高了整体质量，但 Micro object placement 仍需要局部 clearance / support sweep。

现有 Construction / Portal QA 已经足以处理，不建议因此扩写 Thinking Kernel。

### T09-F03｜Vault / Dome 的 Minecraft craft 仍带算法体素感

**Classification:** `MINECRAFT_TRANSLATION / TASK_SPECIFIC_JUDGMENT`
**Severity:** Moderate, non-blocking

冷厅交叉拱和热室穹顶已经由结构与剖面生成，这是重大进步；但具体表面仍主要由数学曲线离散成体素，Completion Report 也承认拱顶存在明显方块阶梯感。

这已经不是“建筑底层逻辑错误”，而是 Minecraft translation / finish quality 问题。

未来可通过：

- stairs / slabs / walls 的局部形状优化；
- 更适合玩家视点的曲率离散；
- 关键拱券和檐口的专门 detail pass；

改善，但不应重新把 Builder 拖回大量装饰规则。

### T09-F04｜功能系统仍是“建筑表达”，不是运行模拟

**Classification:** `SCOPE / TOOLING_LIMITATION`
**Severity:** Low

hypocaust、炉房、烟道、供水陶管、高位水箱的空间关系已经成立，但并不模拟真实热工、水压或完整地下水网。

这符合当前 Builder 的职责范围。重要的是 Completion Report 已明确边界，没有把象征性系统冒充真实工程模拟。

未来 Canon 中若某个技术系统本身是玩法 / 世界设定核心，再单独提升其模拟深度即可。

### T09-F05｜Vanilla fluid stability 仍未得到真实验证

**Classification:** `TOOLING_LIMITATION`
**Severity:** Persistent

最终静态检查显示 1,138 个 water blocks 侧面 / 底部没有空气漏口，几何 containment 合理；但仍无 controlled fluid tick，因此只能标记 `fluid stability unverified`。

v1.5 的 Skill 处理方式正确；问题继续属于工具能力而非 Skill 缺口。

### T09-F06｜真实 Minecraft 客户端 Perceptual QA 仍是最大剩余盲区

**Classification:** `TOOLING_LIMITATION`
**Severity:** Persistent / High-value tooling target

所有最终透视仍为离线体素渲染，不能验证：

- 实际材质与 stairs/slabs 模型；
- 玩家 FOV；
- 光照和阴影；
- 水面观感；
- 移动速度下的尺度；
- 真实碰撞和跳跃体验。

T09 的代码和空间逻辑已经足以说明 v1.7 的思维链有效，但“最终 Minecraft 观感”仍应以 Owner 实机检查为最高感知证据。

---

## T08 → T09 change assessment

| 维度 | T08 v1.6 | T09 v1.7 |
|---|---|---|
| 设计起点 | typology + generic shell | purpose / users / program / site |
| 空间生成 | box first, carve later | room / system specific |
| Section | 有描述，但多为 shell 后解释 | 在 Macro 直接生成地坪、跨度、拱顶、hypocaust |
| Structure | Gothic vocabulary 后贴 | 支承、拱顶、鼓座、穹顶直接参与体量 |
| Massing | 主要目标本身 | 前序逻辑的结果 |
| Portal QA | 全局 reachable 可掩盖坏门 | restricted expected edge，不接受绕路 |
| Gate | false positive | 真实发现问题并在进 Meso 前返工 |
| 后勤系统 | 基本附属体量 | 与公共流线独立且进入空间设计 |

因此 T09 最重要的结论不是“罗马浴场做得比哥特教堂漂亮”，而是：

> **v1.7 changed the generative model, not merely the checklist.**

---

## Recommendation for Skill

### 现在不要立即 v1.8

T09 是 v1.7 的第一份强正向样本，但一个历史公共浴场不足以证明 Architectural Thinking Kernel 对所有建筑都稳定。

建议：

1. **冻结 v1.7**，暂不新增建筑思维规则；
2. 下一轮验证完全不同的 building logic，而不是继续罗马 / 历史大型公共建筑；
3. 优先验证一个结构、材料、使用者和场地逻辑都不同的样本；
4. 如果 v1.7 再通过 1—2 个异质样本，再将其视为稳定 architecture baseline；
5. 接下来优先投资 `real-client perceptual QA` 和 `semantic interface protection`，收益可能高于继续扩写 Skill。

候选下一测试方向：木构民居 / 商业建筑、工业生产建筑、或幻想文明建筑。测试 prompt 仍应保持最小，不把本次 findings 写进去作为提示。

## Final Assessment

**T09: PASS_WITH_FINDINGS**

**Architectural Thinking Kernel: STRONG POSITIVE EVIDENCE**

**v1.7: keep unchanged pending heterogeneous follow-up regression.**
