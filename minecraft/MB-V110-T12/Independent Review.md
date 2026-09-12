# T12 Independent Review

## Verdict

**PASS_WITH_FINDINGS — Targeted regression passed, with real-client movement still unverified.**

本轮验证目标不是重新评价 T11 的设计美学，而是检验 `minecraft-builder v1.10` 新增的 Construction Closure & Clearance Gate 是否能在**没有人工指出具体故障位置**的情况下，从现有建筑中自主发现物理完整性问题，并以有界 Repair 修复，同时避免破坏已成立的建筑设计与 Finishing。

基于归档的世界差量、扫描器、初始 / 修复后 Gate、关联完整性、reload 证据与 Repair 账本，本轮目标成立。

---

## 1. 自主诊断：PASS

T12 的初始扫描不是根据人工坐标表逐项修复。扫描器从当前建筑实存出发，对 Scope 内低层墙 / 柱基部、非屋面 stairs / steps、主要 Space Graph edges、实际 stair chains 与小型支承对象进行检查，并使用原生方块 collision shape、0.6×1.8 玩家身体包络、≤0.1 格采样与连续 swept envelope 估算路线净空。

初始 Gate 自主得到四类有效问题：

- 17 格墙 / 柱脚底部空缝；
- 8 格台阶下支承缺口；
- 仓库入口前连续地坪缺接；
- 上楼路线与横梁发生净空冲突。

其中墙脚悬空与楼梯被梁阻挡，正好对应 Owner 在 T11 实机检查中发现的主要物理故障类型；T12 还额外发现了仓库入口接地问题。这是 v1.10 Gate 真正改变诊断行为的强证据。

旧的 endpoint / graph reachability 仍能显示连接成立，但 T12 没有接受它作为通过证明，而是继续检查完整 movement envelope。这符合 v1.10 的核心原则：`Reachable endpoint ≠ usable route`。

---

## 2. False Positive / Intentional Void 区分：PASS

T12 没有把所有空气、悬挑或局部碰撞图中的断开都当成错误。

它明确审查并保留了：

- 有意的门窗 / reveal；
- courtyard / kitchen upper opening；
- eave cantilever；
- stairwell 本身的必要 void；
- warehouse apron 外扩但并非真实通行门洞的区域；
- hanging lantern 因原生 collision shape 不表达吊链而在 contact graph 中出现的假“未支承”。

这点重要，因为一个只会“把所有空洞补满”的 Closure Gate 会直接伤害建筑。T12 表现出的是 `detect → classify → repair only confirmed defect`，而不是机械补洞。

---

## 3. Repair 边界：PASS

实际 Repair 只有 **47 格差量**，且差量与账本一致：

- 补齐墙 / 柱脚和台阶基础；
- 补仓库入口前连续地坪；
- 删除侵入 stair movement envelope 的 5 格梁段；
- 在原 stairwell 边界补局部侧梁，使构造语义保持完整。

没有重新设计房间、Program、Space Graph、主体量、主楼板、门洞、主屋面、庭院或主要 circulation；没有趁 Repair 增加家具、植被或装饰。

reload 后实际差量仍严格是这 47 格；roof states、原 stairs 与 water states 保持不变。说明 v1.10 的状态回退和 bounded Repair 没有退化为“大修整个建筑”。

---

## 4. 同类风险复扫：PASS

Repair 后并非只重新确认几个已修坐标，而是重新执行同类 Scope 扫描：

- 492 个墙 / 柱基部；
- 82 条非屋面 stair / step strips；
- 17 条主要 route；
- warehouse apron 的额外横向使用线。

归档结果中，已知 Closure 与静态 Clearance 失败均无剩余；reload 后结果保持一致。

这通过了本轮最重要的测试要求之一：**发现一个问题后必须扫描整个 Scope 的同类风险，而不是只修一个点。**

---

## 5. 状态机与 epistemic discipline：PASS

T12 没有因为来源建筑已经是 `FINISHED` 就跳过 Core 问题。初始物理 Gate 失败后，继承的完成状态被撤销，进入 bounded Core Repair；修复后重新跑 Spatial / Finishing / Integrity 检查。

同时 Codex 没有把静态 collision-envelope 模型包装成真实玩家测试。最终 Construction Closure & Clearance Gate 明确保持：

> **UNVERIFIED**

理由是当前证据没有实际 Minecraft 玩家 step / gravity / input / pose / dynamic collision walk-through。

这不是回归失败，而是正确暴露了工具边界。对 T12 目标而言，静态检测已足够证明“自主发现并修复”；对最终世界物理认证而言，还需要 Owner 实机走行。

---

## Findings

### F01 — Real player movement remains unverified

**Classification:** C `TOOLING_LIMITATION`  
**Severity:** Major for final physical certification; not a failure of the targeted T12 regression.

当前扫描使用 Minecraft 26.2 原生静态 collision shapes + 0.6×1.8 body envelope + swept AABB / step-band 近似。它比 endpoint reachability 强很多，但不是原生玩家移动求解。

因此目前可以说：

> 已知静态闭合 / 净空失败已修复。

不能说：

> 玩家真实走行已经通过。

Owner 需要在客户端至少实际走一遍楼梯、入口、仓库阶前和主要 route。

### F02 — QA scanner is project-adaptive, not yet a universal verifier

**Classification:** C `TOOLING_LIMITATION` / WATCH  
**Severity:** Minor.

扫描器整体方法很好，但实现仍带当前建筑语境：使用当前项目的 Space Graph，部分 route 有项目特定 intermediate points，墙脚候选识别也针对当前常用 terracotta / vertical log 等材料。

这对 T12 完全合理，因为目标就是修当前建筑；但不能把该脚本本身视为“已经完成的通用 Minecraft collision validator”。如果以后不同题材反复需要同类能力，再考虑工具层抽象，不应现在把这些项目特例塞进 Skill。

### F03 — Public archive cannot independently prove every private source-world hash

**Classification:** C `EVIDENCE_BOUNDARY`  
**Severity:** Minor.

归档说明完整 source-world 文件哈希索引因包含玩家文件名而只留本机。公开证据支持复制 / reload / Repair 差量及源保护流程，但第三方无法仅靠仓库重跑“整个 T11 源存档完全未变化”的全部私有哈希核验。

这不影响本轮设计 / Repair 判断，但应继续保持该证据边界的明确表述。

---

## Release implication

**当前不建议因为 T12 再修改 Skill。**

v1.10 新增的 Closure / Clearance 思路在第一轮针对性回归中已经真实生效：它找到了 Owner 已知但未向测试提示公开的主要故障类型，也发现了额外接口问题；修复有界、没有破坏上游设计，并且在不能真实验证客户端 movement 时没有伪造 PASS。

下一步只需要 Owner 实机复核当前 `MB-V110-T12-京町家修复`：

1. 正常步行上楼并通过楼梯顶部；
2. 近距离绕建筑检查墙脚 / 柱脚是否仍存在无意空缝；
3. 正常经过主入口；
4. 正常经过仓库入口 / 台阶；
5. 沿主要 route 正常移动，确认没有新的碰撞或 Repair 副作用。

若 Owner 实机确认这些项目，T12 可视为完整闭环，`minecraft-builder v1.10` 可以进入 `建筑师` 的 **Production Pilot**；该町家也可以进入正式 Asset Candidate 审批流程，但仍需 Owner 明确 `批准入库`，不得自动注册。
