# MP-P05R Independent Review｜minecraft-planner v0.5

日期：2026-09-14  
审核对象：`minecraft/MP-P05R-NORTH-FRONTAGE-ENSEMBLE/`  
实现提交：`6c6dafc6c1bc5163dccce76b54470e8edb48ab2a`  
目标：验证 `minecraft-planner v0.5` 是否修复 MP-I01 暴露的 Planner→Builder handoff contract 缺口。

## Verdict

> **FAIL_MODEL_EXECUTION — 本轮没有完成 v0.5 的核心回归目标。规划本身大体保持 L4 关系，但 Builder Design Packages 缺少 v0.5 明确要求的 Interface Baseline、boundary semantic、external service ownership、package/interface revision 与 builder_handoff_readiness；同时 `planning-data.json` 出现 `state=SCOPED` 与 `builder_ready=true` 的自相矛盾。现有 Skill 规则已经明确这些要求，因此当前证据更支持模型执行 / Skill 加载失败，而不是新的 foundational SKILL_GAP。**

**不要进入 MP-I01R。** 先重新执行 P05R，确保实际读取并遵守当前 `minecraft-planner v0.5` 与 shared Planner–Builder Contract。

---

## 1. Push / lineage

远端 `main` 已包含本轮归档。原本本地报告的 commit `02390c6...` 在同步远端后发生了 rebase / commit 重写，远端实际提交为：

`6c6dafc6c1bc5163dccce76b54470e8edb48ab2a`

提交信息保持：

`archive: add MP-P05R v0.5 Planner-Builder handoff regression`

本轮归档目录共有 8 个提交文件，均位于 `minecraft/MP-P05R-NORTH-FRONTAGE-ENSEMBLE/`。

---

## 2. What still works

### L4 causal concept is broadly plausible

方案仍保留北侧两户的核心分化：

- 低肩：修理 / 值守；
- 上沿：复核 / 有限短宿；
- 共享卸载—复核院；
- 东向轻载关系；
- 两户容量不扩为第三户；
- 地形按 Y129–136 分段适应，不要求整片找平。

这些方向与父包 PACKAGE-01 基本一致，也没有越级替 Builder 画建筑 Plan / Section / Roof / Structure。

`world writes = 0`，归档未包含 world-write 授权。

因此本轮不是“规划逻辑全面失败”。失败发生在 **v0.5 专门要验证的 Builder handoff contract**。

---

## 3. Core regression target: Interface Baseline

### FAIL

v0.5 明确要求：凡是进入 `PLANNER_FIXED`、跨 package / parcel 且影响当前 Builder 设计阶段的物理接口，必须提供可解析的局部 Interface Baseline 或 immutable ref，至少包含：

- interface id；
- source object / revision；
- local geometry + semantic；
- height / section baseline；
- nominal width；
- minimum clear requirement；
- adjustment envelope；
- rights / access semantic；
- coordination owner；
- resolve_before。

本轮 `builder-design-packages.json` 只有：

- `fixed`；
- `builder_owns`；
- `preflight`；
- lane / space ID。

没有 `interface_baselines` 或同等结构。

例如 BDP-NF-01 写：

`keep SPACE-01 and LANE-NF-01 continuous`

但没有给 Builder：

- LANE-NF-01 的局部 protected geometry / width envelope；
- threshold 对接断面；
- minimum clear；
- adjustment envelope；
- interface revision；
- coordination owner。

这与 MP-I01 暴露的缺口实质相同，因此 v0.5 修复没有在本次输出中被执行。

---

## 4. Minecraft boundary semantic

### FAIL

v0.5 要求连续 polygon / 斜边若成为 Builder voxel 合法边界，必须显式说明：

- `CELL_CENTER_MASK`
- `FULL_VOXEL_INSIDE`
- `CONTINUOUS_BOUNDARY_WITH_TOLERANCE`
- `NEGOTIABLE_EDGE`
- `REFERENCE_ONLY`

本轮 parcel 仍只给连续多边形坐标；`builder-design-packages.json` 与 `planning-data.json` 都没有 `boundary_semantic`。

这意味着如果现在交给 Builder，MP-I01 的“斜边到底怎样落到 voxel”问题仍会再次出现。

---

## 5. External service interface responsibility

### FAIL / INCOMPLETE

P05R 知道供水、污物、排水仍未闭合，但只写成：

- `confirm water interface`
- `confirm water and waste interfaces`
- `water: parent coordination required`

没有说明：

- interface id / local ref；
- external owner；
- Builder 是 `RESERVE_ONLY`、`LOCAL_CONNECTOR`、`CO_DESIGN` 还是 owner；
- resolve_before；
- public drainage / supply 可否进入当前 package。

因此 v0.5 的 `EXTERNAL_SERVICE_INTERFACES` 目标没有完成。

---

## 6. Builder handoff readiness

### FAIL

v0.5 已明确区分：

- `CONCEPT_DESIGN_READY`
- `DESIGN_FREEZE_READY`
- `INCOMPLETE_HANDOFF`

本轮 BDP 顶层只写：

`status = READY_FOR_INDEPENDENT_REVIEW`

没有 `builder_handoff_readiness`。

更严重的是 `planning-data.json` 同时写：

- `state = SCOPED`
- `builder_ready = true`

这两个状态互相冲突。

Planner state 仍停在 `SCOPED` 时不能同时宣告 Builder-ready；而且 v0.5 明确要求 Planner state 与 Builder handoff readiness 是两个不同维度，不能混用。

因此本轮 Handoff Gate 不成立。

---

## 7. Package / interface revision traceability

### FAIL

没有：

- `package_revision`；
- per-interface revision；
- immutable interface refs；
- direct local slice revision。

`direct-dependencies.json` 只列 `P04-ROUTE-02` 和 CIV-001，没有把 Builder 必须冻结的共享 public interfaces 做成可版本化输入。

这无法满足 v0.5 “Builder 只读 BDP + direct refs 即可设计”的 progressive-disclosure 目标。

---

## 8. Source / Skill-load audit

### FAIL_TO_PROVE

归档没有：

- `source-register.json`；
- Skill snapshot / commit；
- shared contract snapshot；
- validation / source hashes。

README 也没有记录实际读取的 Skill revision。

因此独立审核无法证明本次 Codex 实际读取的是 `minecraft-planner v0.5`（Vibe-Coding `fc637136...`）而不是旧版 / 缓存 / 简化执行。

由于当前 v0.5 Skill 本身已经明确写出本轮缺失的 Interface Baseline、boundary semantic、external service responsibility 与 readiness 规则，本轮更像：

> **MODEL_EXECUTION_FAILURE / POSSIBLE SKILL-LOAD FAILURE**

而不是 “v0.5 仍不知道该做什么”。

---

## 9. Additional planning inconsistency: LANE-NF-03

### FINDING — MODEL EXECUTION / SCOPE INTERPRETATION

P05R 新增：

`LANE-NF-03 = 两户后侧服务巷`

但父包 PACKAGE-01 的 fixed relation 是：

- 保留 `LANE-04`；
- 保留东轻载出口；
- 北侧两户不是整栋楼体；
- 下游自己解决门前 / 家庭后院关系。

父包中真正依赖后巷的是 PACKAGE-02 南侧两户；PACKAGE-01 并没有要求北侧两户共享后巷。

P05 原回归反而明确“不新增共用后巷”。

P05R 将位于南侧 / PACKAGE-03 体系中的服务巷关系重新解释为北侧两户后巷，至少需要新的明确因果与几何证明。目前没有。

这不是 v0.5 contract 的主失败，但说明本轮 L4 execution 也存在 scope leakage / interface misinterpretation 风险。

---

## 10. Visual artifacts

归档提供 `owner-overview.svg` 与 `section-west-east.svg`，而且 SVG 是可审计文本，能看出：

- 两 parcel；
- 共同院；
- 西接 / 东向流；
- 地形剖面。

但图本身没有补足 machine-readable handoff contract 缺失。一个画出来的 route 不能代替带 semantic / revision / minimum-clear / adjustment-envelope 的 Interface Baseline。

因此 Visual artifact 不改变 FAIL 结论。

---

## 11. Finding classification

### A. Missing Interface Baseline

Class: `MODEL_EXECUTION_FAILURE`  
Severity: blocking

Skill 已明确要求，输出未执行。

### B. Missing boundary semantic

Class: `MODEL_EXECUTION_FAILURE`  
Severity: blocking before Builder voxel freeze

### C. Missing external-service ownership

Class: `MODEL_EXECUTION_FAILURE`  
Severity: blocking for affected design freeze

### D. State/readiness contradiction

Class: `MODEL_EXECUTION_FAILURE`  
Severity: blocking

### E. Cannot prove v0.5 was actually loaded

Class: `UNKNOWN / POSSIBLE SKILL-LOAD FAILURE`  
Severity: high for regression validity

### F. LANE-NF-03 north-group interpretation

Class: `MODEL_EXECUTION_FAILURE / TASK_SPECIFIC_JUDGMENT`  
Severity: medium

---

## 12. Skill decision

> **Do not modify minecraft-planner v0.5 or minecraft-builder v1.11 based on this run.**

The required behavior already exists in current Skill / shared contract. P05R failed to demonstrate that behavior.

The next action should be a clean rerun, not another Skill patch.

---

## 13. Rerun requirement

Rerun P05R in a fresh Codex context and require only the same task boundaries, but verify during completion that the model records the actual loaded Skill revision and produces a Builder handoff consistent with v0.5.

Do not feed this review to the rerun.

The rerun should naturally produce, where applicable:

- BDP package revision / readiness;
- parcel boundary semantic;
- local cross-scope Interface Baselines or immutable refs;
- width semantic with nominal vs minimum clear;
- local elevation / section baseline;
- adjustment envelope;
- rights / access semantic;
- interface owner / revision;
- external service interface responsibility;
- known uncertainty / resolve_before;
- source register proving v0.5 + shared contract were actually consumed.

Only after that passes should MP-I01R start.
