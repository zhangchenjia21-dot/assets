# MP-I02A Independent Review｜Planner → Builder Minimal Upstream Revision

日期：2026-09-14  
审核对象：`minecraft/MP-I02A-INTERFACE-CLOSURE/`  
实现提交：`49091de27927e648dbd4bf2265f17bd09abd642a`  
Planner：`minecraft-planner v0.5`  
Shared contract：`Minecraft Planner–Builder Contract v1.0`

## Verdict

> **PASS_WITH_FINDINGS — Builder → Planner 的问题回报与“最小上游修订”机制通过；Planner 正确只修订 BDP-01 及受影响接口，并把 MP-I01R concept 标为 `STALE_FOR_FIDELITY_REVIEW`，没有重做整个 URBAN_ENSEMBLE，也没有为了追求 DESIGN_FREEZE_READY 而伪造公共通行或雨水能力。**
>
> **但本轮没有完成接口闭合目标：U-PUBLIC 与 U-RAINWATER 仍为 BEFORE_DESIGN_FREEZE HOLD，因此当前不能进入最终 MP-I02B Design Freeze 回归。需要一个更窄的 MP-I02A2，把“规划级可冻结接口”与“真实施工/运营证明”再分开一次。**

当前没有证据支持修改 `minecraft-planner v0.5`、`minecraft-builder v1.11` 或 shared contract。主要剩余问题属于本案接口闭合的执行/判断，而不是新的 foundational Skill gap。

---

## 1. Provenance / Isolation

### PASS

本轮 provenance 清楚：

- `minecraft-planner v0.5`；
- shared contract v1.0；
- source commit `fc6371361685e2eeaefdef5a513f21dbe64c6696`；
- 读取 MP-P05R2 的 BDP-01、明确 interface/service 依赖与 handoff register 中 public coordination；
- 读取 MP-I01R 的 issues、handoff consumption、design validation 以及极小量设计几何格式信息；
- 未读取 Independent Review；
- 未消费 BDP-02；
- `world writes = 0`。

没有发现通过旧 P05 / I01 答案补接口的迹象。

---

## 2. Minimal Revision Discipline

### PASS

本轮没有重新规划 MP-P05R2。

revision lineage 只升级：

- `BDP-01 r1 → r2`；
- `R2-IF-THRESHOLD-1 r1 → r2`；
- `R2-IF-LANE-04 r1 → r2`；
- `R2-S1-RAINWATER r1 → r2`。

`LANE-01 / LANE-02 / COMMON-EDGE` 及其它三项 service 保持原 revision / semantics。

这符合 shared contract 的最小修订原则：局部问题不应重做 settlement / ensemble。

---

## 3. Downstream Staleness Propagation

### PASS

MP-I01R concept r1 被明确标记：

`STALE_FOR_FIDELITY_REVIEW`

理由精确绑定到 `THRESHOLD-1 / LANE-04 / RAINWATER r1 → r2`，并注明原建筑设计没有被 Planner 修改。

这是本轮非常重要的成功点：

> **Planner revision 不直接重写 Builder 设计；它只使受影响设计失效到需要 Fidelity Review。**

这证明双向 revision chain 已经开始成立。

---

## 4. U-PUBLIC Partial Closure

### PASS_WITH_FINDING

Planner 新增了有价值的局部控制：

- `(757,1633)` 对应行走面 Y132；
- 私侧接触面固定为 Y132；
- 给出公共侧局部连接块；
- 给出 3-block vertical clear requirement；
- 私侧高差由 Builder 在 parcel 内解决；
- adjustment boundary 与责任角色明确。

这些比 r1 明显更接近真正可消费的 Interface Baseline。

但 Planner 正确没有把一个局部 2×2 / 四列连接块外推成整段公共路线已经连续可用；左右 tie-in 的法向 2-wide、转折、连续标高仍未证明。

### Finding I02A-F01 — over-conservative authority boundary

当前 closure register 还把 `PUBLIC-COORDINATOR` 的“承接 / 回签”列为 DESIGN_FREEZE 前缺项。

这里需要区分：

1. **规划级责任角色 / proposed interface baseline**；
2. **真实土地、地役、施工许可**。

后者当然必须等 Owner / rights holder，并可留到 `BEFORE_WORLD_WRITE`；但前者不需要先虚构一个现实机构真的“签字”，Planner 本身就可以在 DESIGN_PROPOSAL authority 下冻结 task-local coordination role 与 protected public envelope。

因此下一 revision 不应继续等待“真实公共管理者任命”才能完成 planning freeze。真正需要补的是**局部连续 corridor / section 几何**；真实权利许可继续留在 U-TITLE。

Finding class：`TASK_SPECIFIC_JUDGMENT / MODEL_EXECUTION_CONSERVATISM`，不是 Skill gap。

---

## 5. U-RAINWATER Responsibility

### PASS_WITH_FINDING

本轮没有把 threshold ref 假装成 outfall，也没有把两只干容器写成已证雨洪系统，这一点正确。

它也明确给出两条可能路径：

- 公共 receiving interface；或
- parcel-local closed strategy。

### Finding I02A-F02 — avoid turning Planner freeze into hydraulic simulation

当前 local-strategy closure 条件要求 design rainfall event、有效储量、恢复过程、超限失效等定量证据。

这些可以是 Builder / environmental design 在 DESIGN_FREEZE 前需要证明的内容，但不应全部成为 Planner 自己必须先解决的“上游公共接口”问题。

Planner 此处真正需要决定的是：

> **雨水是否允许跨 parcel；若不允许，Builder 是否成为 parcel-local collection / retention 的设计 owner。**

如果 Planner 在下一 revision 选择：

`NO_CROSS_BOUNDARY_DISCHARGE + BUILDER_OWNS_LOCAL_CLOSED_STRATEGY`

那么公共 receiving obligation 可以变成 `NONE`，而 gutter / cistern / storage / safe overflow / performance proof 留给 Builder 的 Design Freeze Gate。

这样既不会虚构雨量或公共排水，也不会让 Planner 变成水工模拟器。

Finding class：`TASK_SPECIFIC_JUDGMENT / MODEL_EXECUTION_CONSERVATISM`，不是 Skill gap。

---

## 6. Readiness Honesty

### PASS

BDP-01 r2 仍为：

`CONCEPT_DESIGN_READY`

没有因为生成了更多字段就错误提升成 `DESIGN_FREEZE_READY`。

这是正确的。artifact 完整度不能替代真实 interface closure。

---

## 7. Validation Quality

### PASS_WITH_NOTE

17 项 artifact / geometry consistency check 全部通过：

- embedded interface/service 匹配；
- dependency hash 匹配；
- unaffected fields 不变；
- patch 位于 existing lane mask；
- patch 不侵入 parcel；
- private contact 位于 apron；
- source 未改变；
- downstream stale 标记存在。

但 validation 自己也正确保留以下未验证项：

- two-sided continuous public tie-in；
- rainwater quantitative closure；
- Builder fidelity under r2；
- actual rights / public appointment / world execution。

因此这些 checks 只能证明 revision artifact 内部一致，不能证明 interface 已闭合。

---

# 8. Regression Interpretation

MP-I02A 的测试目标包含两个层面：

### A. Builder issue → Planner minimal revision protocol

**PASS**

已经证明：

```text
Builder HOLD
→ structured upstream issue
→ Planner reads minimum affected scope
→ only affected objects revised
→ revision numbers advance
→ downstream design becomes stale
→ unaffected planning remains stable
```

### B. Produce a Builder-freeze-ready public interface

**NOT YET CLOSED**

这不是因为 Planner 必须重做整个规划，而是最后两个 freeze-boundary 仍混合了：

- planning proposal authority；
- physical / operational proof；
- real rights authorization。

因此本轮整体给 `PASS_WITH_FINDINGS`，而不是 FAIL。

---

# 9. Required Next Step — MP-I02A2

不要直接进入 MP-I02B。

先做一个非常窄的 Planner revision：`MP-I02A2 / Freeze Baseline Closure`。

它只需要完成两件事：

## U-PUBLIC

在 `DESIGN_PROPOSAL` authority 下：

- 明确一段可解析的 protected public corridor / swept-envelope proposal；
- 从 BDP-01 threshold 向 LANE-04 两侧 tie-in；
- minimum horizontal clear = 2；
- minimum vertical clear = 3；
- 给出 planning design-surface / section sequence 或等价 per-cell baseline；
- adjustment envelope 清楚；
- `PUBLIC-COORDINATOR` 作为 task-local coordination role 即可，不要求真实机构任命；
- actual easement / title 仍留 `BEFORE_WORLD_WRITE`。

不需要声明 Minecraft runtime 已验证。

## U-RAINWATER

Planner 选择责任模式，而不是自己做完整水工设计：

```text
cross_boundary_discharge = FORBIDDEN_UNLESS_FUTURE_INTERFACE_REVISION
public_receiving_obligation = NONE
builder_responsibility = DESIGN_AND_PROVE_PARCEL_LOCAL_CLOSED_STRATEGY
resolve_before = BEFORE_DESIGN_FREEZE
```

Builder 在 MP-I02B 中再证明 storage / gutter / overflow / native block translation 是否成立；如果 parcel-local strategy 无法成立，再返回新的 upstream issue。

完成后，Planner handoff 可以升级为：

`DESIGN_FREEZE_READY` **from planning-interface perspective**

但这不代表建筑本身已经 `DESIGN_READY`；Builder 仍需关闭 U-GROUND / U-HABITABILITY / B-TRANSLATION / local rainwater performance，并通过 Planning Fidelity Gate。

---

## Final Assessment

> **MP-I02A 证明了双向 revision protocol 是工作的。**
>
> **当前剩余障碍不是“Planner 和 Builder 接不上”，而是最后一次 interface-freeze semantics 需要收敛：规划层负责固定 corridor / responsibility，Builder 层负责工程与 voxel 证明，真实权利留到 world-write 授权。**

因此：

- `minecraft-planner v0.5`：保持；
- `minecraft-builder v1.11`：保持；
- shared contract v1.0：保持；
- 下一步：MP-I02A2；
- MP-I02A2 通过后再执行最终强制关 MP-I02B。
