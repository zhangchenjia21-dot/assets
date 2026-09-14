# MP-P05 Independent Review｜minecraft-planner v0.4

日期：2026-09-14  
审核对象：`minecraft/MP-P05-NORTH-FRONTAGE-ENSEMBLE/`  
实现提交：`f726b25b7780af8ced877e463ca8029f40a44b9d`  
测试：`MP-P05｜北侧两户混合前沿 / URBAN_ENSEMBLE`

## Verdict

> **PASS_WITH_NOTES — L3→L4→Builder handoff 通过。minecraft-planner v0.4 已完成从 POLITY_TERRITORY → REGIONAL_SYSTEM → SETTLEMENT → DISTRICT → URBAN_ENSEMBLE 的纵向递归，并能在最低规划尺度生成边界清楚、保留建筑作者权的 Builder Design Packages。当前无新的 foundational SKILL_GAP。**

本轮的核心成功不是把两块 parcel 继续细分，而是把父级的“北侧两户混合前沿”转译成足够具体、又没有越界成建筑设计的 ensemble contract：两户分别拥有不同经营/生活关系、受控家庭院落与入口搜索段，同时共享并保护公共门前通行；精确 footprint、Plan/Section、结构、屋顶、立面、材料、基础与 Minecraft Translation 仍由 Builder 决定。

---

## 1. Source / Isolation Audit

### PASS_WITH_NOTE

- 主输入为 MP-P04 `PACKAGE-01`；
- 只读取 PACKAGE-03 中与本组团直接相关的 `LANE-04 / LANE-02 / SPACE-01` 公共接口；
- CIV-001 README 作为 APPROVED_CANON；
- 使用当前 v0.4 Skill 字节；
- 未读取 Independent Review 内容或既有 ensemble 答案；
- `world writes = 0`。

Codex 披露一次父包浅层 JSON 输出连带出现 PACKAGE-02 摘要。该内容没有进入本轮空间对象、Builder package 或因果链，归档 source-register 也明确记录此事。因此分类为 **PROCESS_ISOLATION_NOTE / non-blocking**，不构成答案污染。

---

## 2. Scale Discipline｜L4 是否真的停在规划边界

### PASS

本轮解决的是 ensemble 级问题：

- parcel group；
- public frontage / threshold；
- private yard relation；
- shared access；
- service / clean-dirty relation；
- building search envelope；
- Builder package dependency；
- local capacity test budget。

同时没有替 Builder 完成：

- exact building footprint；
- room plan；
- exact section / floor height；
- floor count；
- structure / tectonics；
- roof / facade / openings；
- exact foundation / drainage geometry；
- block palette；
- Minecraft Translation。

因此 `URBAN_ENSEMBLE` 没有退化为“Planner 先设计完建筑，Builder 只负责摆方块”。

---

## 3. Ensemble Causality

### PASS

两户不是复制关系：

- P01 / 下肩户：西来货物首先触发小修理；较深地块承担工具、生活与较安静家庭院落；
- P02 / 上沿户：临东向轻载出口，核心是复核和值守，1–2 人短宿只是受限附带服务；浅地块与窄尾限制其 program，不能为了“旅店”侵占家庭空间或公共路。

共同 frontage 的连续性来自公共通行和货流关系，而不是建筑必须齐线、等高或共墙。两户不共享私院，也没有被强造一条未获批准的共用后巷。

这说明 L4 仍然是 `relationship → architectural task`，不是 `building list → geometry`。

---

## 4. Human Geography Kernels at L4

### PASS

v0.4 的底层机制在最低规划尺度仍有空间后果：

- **Agency / Rights**：地方权利人、经营户与共同通行者都有 veto；规划图不能自动生成产权；
- **Bounded Knowledge**：地下证据没有倒写成历史居民的先验知识；
- **Adaptation**：小高差优先用短步级、局部地面适应与入口调整，而不是整体大平台；
- **Metabolism**：小修理、家庭水粮、短宿、污物具有不同 rhythm / stock / failure response；
- **Feedback**：经营稳定提高 frontage value，同时增加占路压力；公共地役抑制无限私有化；
- **Competition / Capacity**：短宿增长先通过预约/错时收缩服务，不自动塞第三户或吞掉公共路。

没有出现“越到建筑尺度，人类地理 Kernel 越只剩背景文字”的退化。

---

## 5. Builder Design Package Quality

### PASS

`builder-design-packages.json` 的三包结构合理：

1. `BDP-00`：两户门前接口联审；
2. `BDP-01`：P01 下肩修理/值守户；
3. `BDP-02`：P02 上沿复核/有限短宿户。

`BDP-00` 单独存在是优点。它不是第三栋建筑，而是要求 Builder 在两户各自冻结设计前先联合解决门前高程、公共净宽、入口与东口接口，避免两个局部建筑都“设计正确”却把组团公共关系夹死。

`BDP-01/02` 均提供：

- WHY / planning role；
- upstream anchors / flows；
- parcel envelope；
- access search segments；
- shared-space / service relation；
- program requirements；
- Architecture Kit requirements；
- `PLANNER_FIXED`；
- `BUILDER_ADAPTABLE`；
- dependencies；
- known uncertainty；
- upstream issue protocol。

这已经足以作为一次真正的 Planner→Builder integration regression 输入，而无需 GPT 重新把 Planner 思路人工翻译一遍。

---

## 6. Fixed vs Adaptable Boundary

### PASS

Planner 固定的是关系，而不是建筑形状，例如：

- 两户独立生活与家庭开敞空间；
- 公共通行不能被门扇、停留或服务占用消灭；
- 不把公共院 / 户间间隙私有化；
- 不强迫通过另一户私域通行；
- 修理户面向首卸后的手提流；
- P02 保留轻载出口与家庭生活优先级。

Builder 仍可决定 exact footprint、Plan/Section、层数、高程、结构、屋顶、立面、开口、基础、排水、palette 与 Minecraft translation。

该权限边界符合 Planner / Builder 的职责分离目标。

---

## 7. Uncertainty / Return Protocol

### PASS

P05 没有把 `HANDOFF_READY` 冒充施工许可。五类重要未决项被显式传给 Builder：

- `C-RIGHTS`；
- `C-SUPPLY`；
- `C-GROUND`；
- `C-ACCESS`；
- `C-CAPACITY`。

其中还区分了何时必须解决，例如 foundation design freeze、Builder design acceptance、world write / permanent occupation。

若普通门位调整、分段落脚、户内重排与服务错时仍无法满足 fixed relation，Builder 被要求返回：冲突约束、拟用体积/使用证据、有界适应尝试、最小父层决定，而不能静默扩地、增户、封路或删 program。

这使 Planner→Builder 不再是单向“发任务”，而具备 upstream issue 回路。

---

## 8. Capacity / Geometry

### PASS

- 父包两 parcel 分别为 151 / 118 列；
- overlap = 0；
- parent parcel geometry 未改变；
- 与 LANE-02 / LANE-04 的私用列重叠 = 0；
- P01 / P02 建筑 footprint 只给 nonbinding test range，不被当成精确建筑占地；
- P02 窄尾没有为了满足短宿而强塞居室。

P05 正确把“规划空间预算”与“Builder 证明建筑净空间可行”分开。

---

## 9. Visual Evidence

### PASS_WITH_REVIEW_LIMIT

归档提供两张 2800px 宽地图：组团关系与真实地形、现状地形与门前高差。文件与生成记录存在，Planning Packet / machine-readable geometry 与地图语义一致。

本独立审核通过 connector 核对了地图文件、坐标对象、图面生成说明和 validation，但没有完成独立像素级视觉审美/可读性验收。因此本次 PASS 不依赖“地图视觉已经由 GPT 独立看过”这一点。若 Owner 发现主图难读，应作为 artifact correction，而不是自动判定因果规划失败。

---

## 10. Findings

### Finding A — Planner→Builder output side is now strong enough for integration test

**Class:** `SYSTEM_INTEGRATION_PENDING`  
**Severity:** non-blocking for Planner

P05 已经证明 Planner 能发出包含 causal context、fixed/adaptable、rights/access、uncertainty 与 return protocol 的 Builder package。

尚未证明的是 **minecraft-builder v1.10 是否会自动、完整、忠实地消费这些字段**。这是 Builder intake / cross-skill integration 问题，不应继续通过修改 Planner 猜测解决。

### Finding B — Rights / supply / real access remain unresolved

**Class:** `EVIDENCE LIMITATION`  
**Severity:** non-blocking for design-only handoff; blocking for world-write / permanent operation

不建议修改 Skill。

### Finding C — P02 short-stay capacity remains a Builder design test

**Class:** `TASK_SPECIFIC_JUDGMENT`  
**Severity:** non-blocking

Planner 正确没有用“可做两层”之类未经建筑设计证明的理由关闭问题。

---

## 11. Regression Conclusion

MP-P05 完成了 Planner 第一轮完整纵向递归：

```text
POLITY_TERRITORY
→ REGIONAL_SYSTEM
→ SETTLEMENT
→ DISTRICT
→ URBAN_ENSEMBLE
→ Builder Design Packages
```

### Skill decision

> **保持 minecraft-planner v0.4，不更新 Planner Skill。**

下一步不再继续 Planner 尺度回归，而应执行独立的 **Planner→Builder Integration Regression**：只把 P05 的 Builder package 交给当前 minecraft-builder v1.10，不用 GPT 额外复述 Planner 的设计逻辑，观察 Builder 是否会主动读取并继承 WHY、flows、rights、fixed/adaptable、uncertainty 与 Architecture Kit requirements。

若 Builder 丢失这些信息，再据真实失败点决定是否需要 Builder v1.11 的 `Planner Context Intake + Planning Fidelity Gate`，以及是否需要共享 cross-skill contract。
