# MP-I01 Independent Review｜Planner → Builder Integration

日期：2026-09-14  
审核对象：`minecraft/MP-I01-PLANNER-BUILDER-P01/`  
实现提交：`81688b0711e5685db27fa045762a66f48d474efb`  
Planner source：MP-P05 `BDP-00 + BDP-01`  
Builder：`minecraft-builder v1.10`

## Verdict

> **PASS_WITH_FINDINGS — Planner → Builder 的语义交接成立：Builder 能仅凭 BDP-00 / BDP-01 正确继承 WHY、Program、Flow、Rights、PLANNER_FIXED、BUILDER_ADAPTABLE、Architecture Kit 与 uncertainty，并据此形成因场地和规划背景而异的 Architecture Design；但当前 handoff contract 仍缺少足以冻结跨包公共接口的几何 / 版本 / 边界语义，因此尚不能称为 production-complete integration。**

这不是 `minecraft-planner v0.4` 的规划核心失败，也不是 `minecraft-builder v1.10` 的建筑设计执行失败。相反，Builder 对缺失接口没有自行回读上游、猜测公共道路或静默修改 Planner，而是正确返回 `UPSTREAM_PLANNING_ISSUE — INCOMPLETE_HANDOFF` 并保持设计冻结 HOLD。

因此本轮同时证明两件事：

1. **两个 Skill 的核心思维模型天然兼容，语义链已经接通；**
2. **正式接口协议仍需要补强，尤其是跨 Scope 的 shared interface baseline。**

---

## 1. Isolation / Source Audit

### PASS

实际消费范围符合 MP-I01 测试要求：

- 只读取 MP-P05 `BDP-00 / BDP-01`；
- 未读取 BDP-02；
- 未读取 MP-P05 Planning Packet、Critic、Independent Review；
- 未读取 MP-P04 或更上游完整规划；
- 读取 CIV-001 approved Canon 与 Architecture Grammar；
- 场地只读取必要 factual site evidence / provenance；
- `world writes = 0`。

归档中的 `sources/handoff.json` 是 BDP-00/01 的原样交接快照，`source-register.json` 明确记录 forbidden files 本轮未读。

这保证本轮确实测试的是 **Builder 是否能消费 Planner handoff**，而不是 Builder 通过回读完整上游方案“补课”。

---

## 2. Planning Intent Consumption

### PASS

Builder 没有把任务退化成“东域山地造一栋好看的住宅”。Architecture Intent 与建筑设计明显由 Planner 的因果输入驱动：

- `WHY`：西来货物首卸后的小件修理与值守；
- `Program`：完整单户生活 + 小件修理 + 工具短储，而非冶炼厂 / 矿仓 / 旅店；
- `Flow`：营业流与家庭流分门，顾客止于修理空间，家庭不经营业空间才能生活；
- `Rights`：公共通行不得被门前停留、门扇或私人院落侵占；
- `Site`：西低东高，采用低修理翼 + 高生活主屋，而非统一大平台；
- `Architecture Kit`：东域石基 / 木上层 / 山地适应 / 工作生活混合；
- `Uncertainty`：权利、供给、基底、真实通行继续保持未证。

最终产生的“低修理翼 + 高两层生活主屋”是 Planner 关系进入建筑剖面和体量后的结果，而不是风格贴皮。

---

## 3. PLANNER_FIXED Preservation

### PASS

Builder 对主要 fixed relationship 的处理正确：

- 户数保持 1，不新增第三户；
- 82 列建筑占地位于 Planner 55–85 列 nonbinding exploration budget 内；
- 建筑实体列保持在 parent parcel column mask 内；
- 工作与家庭入口分离；
- 家庭私院不是公共捷径；
- 未私有化公共院 / 户间公共关系；
- 没有把整个组团削成一块等高平台；
- 没有引入大宗矿石堆场、冶炼炉等破坏 Planner role 的 program；
- 没有擅自修改权利 / 供给 / 地下现状。

特别重要的是，Builder 发现公共路线 baseline 不足时，没有为了“完成设计”自行发明 LANE-04 / LANE-02 的具体位置。

---

## 4. BUILDER_ADAPTABLE Authorship

### PASS

Builder 保留并实际使用了自身建筑作者权：

- exact footprint；
- 两体量组合；
- 两层生活主屋；
- room arrangement；
- Plan + Section；
- internal stair；
- roof system；
- stone / timber tectonic concept；
- openings；
- smoke / drainage concept；
- Minecraft block translation；
- private-yard internal circulation。

Planner 没有通过 handoff 偷走 Architecture Design；Builder 也没有把 Planner fixed relationship 当成完整建筑 Blueprint。

因此 Planner / Builder 职责边界在本轮表现健康。

---

## 5. Program / Space Graph / Sequence

### PASS

Builder 建立了可审计 Space Graph：

- `TH-01 → S-WORK`：顾客进入低修理间；
- `TH-02 → S-LIVE`：家庭独立进入生活空间；
- `S-WORK → S-LIVE`：户内受控短阶，不成为公共穿堂；
- `S-LIVE → S-SLEEP`：内部竖向交通；
- `S-LIVE → S-YARD`：家庭私院路线。

该关系直接延续 Planner 的“经营 / 家庭 / 私院 / 公共通行”逻辑，而不是事后用房间标签解释随机平面。

两格宽梯初稿会挤压寝层通路，Builder 将其改成单格梯并保留寝层走带，也说明 Builder 的 Architecture Design / Minecraft-scale thinking 在实际工作，而不是机械翻译 Planner 数据。

---

## 6. Terrain / Tectonic Response

### PASS_WITH_NOTE

低翼地坪 Y132、高主屋地坪 Y133、寝层 Y137；两体量分别落在不同高程，没有构造统一大石台。石质首层 / 基础与木上层、短跨坡屋面符合 CIV-001 East-domain Grammar 的一般方向。

这证明 Planner 的 terrain adaptation requirement 能被 Builder 转译成 Plan / Section / massing。

但 `FOUNDATION_STABILITY` 仍未验证，当前 shallow read 不能证明承载力；Builder 正确没有把“下 24 格未见空气”写成工程安全证明。

---

## 7. Builder Safety / Upstream Issue Behavior

### PASS

本轮最值得肯定的行为之一，是 Builder 面对 handoff 缺口时没有越权。

Builder 明确保持：

`DESIGN_REVIEW_READY_WITH_INTERFACE_HOLD`

而不是无条件 `DESIGN_READY`。

它记录：

`UPSTREAM_PLANNING_ISSUE — INCOMPLETE_HANDOFF`

并列出已尝试的 bounded adaptation：门位留在 Planner search segment 内、落脚尽量收进本户、两体量顺地形、不开建公共道路。

仍不足以证明公共通行连续时，Builder 正确停止冻结，而不是静默修改 Planner。

这说明现有 v1.10 即使没有正式 `Planner Context Intake` 章节，也已经具备与 handoff contract 相容的上游回退行为。

---

## 8. Found Integration Gap A — Shared Public Interface Baseline

### FINDING — FOUNDATIONAL HANDOFF CONTRACT GAP

**Severity：blocking for design freeze；non-blocking for conceptual Architecture Design**

BDP-00 告诉 Builder：

- LANE-04 名义 2 格；
- LANE-02 名义 3 格；
- 公共通行必须连续；
- 两户设计冻结前应先做接口联审。

但 handoff 没有提供 Builder 完成该联审所需的最小 baseline：

- route / lane 的 local coordinate geometry；
- relevant ground / design elevation；
- minimum-clear vs nominal width semantics；
- threshold 与 lane 的局部 section；
- 哪些边界可调整、调整多少；
- shared-interface revision / version；
- 哪个 package / actor 对接口最终协调负责。

BDP-01 的 TH-01/02 搜索段和局部地面 Y 只能约束门位，不能证明整条公共通路。

### Required fix

Planner → Builder contract 应要求：

> **所有进入 `PLANNER_FIXED` 且跨 package / parcel 的物理接口，必须携带可解析的 Interface Baseline，或提供 immutable object reference + revision，使 Builder 能只解引用必要对象而不读取完整上游规划。**

推荐字段：

```text
interface_id
source_object / immutable_ref
revision
local_geometry
height / section baseline
nominal_width
minimum_clear_requirement
adjustment_envelope
rights / access semantic
owner / coordination responsibility
uncertainty
```

不需要把整条地区道路复制进每个 BDP，只需要提供当前 Builder scope 所需的局部接口切片。

---

## 9. Found Integration Gap B — Minecraft Boundary Discretization

### FINDING — HANDOFF CONTRACT GAP

**Severity：non-blocking now；blocking before voxel freeze / world write**

Planner 提供连续 polygon + `151 columns`，但没有显式说明 Minecraft 离散边界规则。

Builder 本轮推断使用 column-center inclusion，并退掉两个超界中心列。这是谨慎行为，但这种规则不应该依赖 Builder 自己猜。

Planner → Builder 应明确类似：

```text
boundary_semantic:
  CELL_CENTER_MASK
  FULL_VOXEL_INSIDE
  CONTINUOUS_BOUNDARY_WITH_TOLERANCE
  NEGOTIABLE_EDGE
```

以及必要的 edge tolerance / adaptable strip。

否则同一斜地块可能被不同 Builder 实现成不同的 voxel legal envelope。

---

## 10. Found Integration Gap C — External Service Interface Ownership

### FINDING — CONTRACT CLARITY GAP

**Severity：non-blocking for current concept design**

Builder 能自行设计建筑内部 drainage，但当雨水、洁净补给或污物离开 parcel 并进入公共空间时，它需要知道：

- 由哪个 package / system owner 接收；
- 当前是 fixed interface、可协商 interface，还是 unresolved external dependency；
- Builder 是否只需预留接口，还是需要一起设计局部公共工程。

本轮 Builder 正确选择 HOLD，没有擅自向公共路排水。

建议在 shared interface contract 中加入 `external_service_interfaces / responsibility`，而不是让每栋建筑回读街区完整方案。

---

## 11. Does Builder Need a Dedicated Planner Intake?

### YES — but the test changes the rationale

MP-I01 说明 **Builder 的设计推理本身已经能正确理解 Planner 数据**。因此不需要为了“让 Builder 变聪明”重写 Architectural Thinking Kernel。

真正需要的是把本轮由测试 Prompt 强制执行的行为正式固化进 Skill：

### `Planner Context Intake`

当输入存在 Builder Design Package 时，在 Architectural Intent 之前：

1. 读取 BDP 与直接 interface dependencies；
2. 编译 `Inherited Planning Intent`；
3. 区分 `PLANNER_FIXED / BUILDER_ADAPTABLE / UNRESOLVED`；
4. 验证 required external interfaces 是否可解析；
5. 缺失时返回 `INCOMPLETE_HANDOFF`，不得通过回读完整上游方案自行补答案。

### `Planning Fidelity Gate`

Architecture Design 冻结前检查：

- WHY 是否仍可从最终设计读出；
- fixed frontage / access / shared-space 是否保留；
- rights / public-private threshold 是否被侵占；
- program 是否被 Builder 偷换；
- capacity / parcel / terrain relationships 是否越界；
- unresolved condition 是否被误写成已解决；
- 如有冲突是否正确返回 upstream issue。

MP-I01 实际已经手工完成了这两个动作；vNext 需要把它们从“好模型行为”升级成“Skill contract”。

---

## 12. Visual / Design Review Limit

归档提供五张软件体素预览、OBJ 与 voxel JSON。

本独立审核确认了预览文件存在，并通过 Architectural Intent、Space Graph、voxel/design checks 审核其体量与空间逻辑；当前审核环境未直接进行完整 Minecraft 客户端渲染 / walk-through，因此不把视觉美观、真实门扇交互、FOV 或引擎 collision 作为 PASS 依据。

这与本测试目标一致：MP-I01 测的是 **Planner → Builder 设计交接**，不是 world-built completion。

---

## 13. Regression Conclusion

### Semantic interoperability

**PASS**

Builder 能理解并执行 Planner 的：

```text
WHY
→ users / program
→ flow
→ rights / public-private relation
→ terrain response
→ Architecture Kit
→ fixed / adaptable
→ uncertainty
→ Architecture Design
```

### Handoff completeness

**PARTIAL / NEEDS REVISION**

缺失跨包 public interface baseline、voxel boundary semantic 和 external service ownership，使设计不能无条件冻结。

### Builder architectural reasoning

**PASS**

没有发现需要修改 Builder Architectural Thinking / Core 的设计逻辑缺口。

### Planner core reasoning

**PASS**

没有发现需要修改 Planner v0.4 Human Geography Kernels 的新问题。

### Interface decision

> **下一步应建立 shared Planner–Builder Contract，并分别在 Planner 输出侧和 Builder 输入 / Fidelity Gate 侧接入。不要再继续依靠任务 Prompt 临时解释交接协议。**

推荐版本方向：

- `minecraft-planner v0.5`：Builder-ready package completeness / interface baseline；
- `minecraft-builder v1.11`：Planner Context Intake + Planning Fidelity Gate；
- 两者共同引用一个 shared contract，避免双份 schema 漂移。

在上述接口升级后，建议运行 MP-I01R：使用同一 P01 规划语义重新导出 handoff，让 Builder 不读完整上游即可完成公共接口联审并达到可冻结 Architecture Design 的状态。
