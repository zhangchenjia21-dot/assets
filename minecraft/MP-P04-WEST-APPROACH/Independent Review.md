# MP-P04 Independent Review｜minecraft-planner v0.4

日期：2026-09-14  
审核对象：`minecraft/MP-P04-WEST-APPROACH/`  
实现提交：`486bd7ccbfe4267bbfd3ff700e4c5553a7572692`  
测试：`MP-P04｜西接坡交割与修理前沿 / DISTRICT`

## Verdict

> **PASS_WITH_NOTES — L2→L3 recursive planning 通过；v0.4 的 Agency / Knowledge / Adaptation / Metabolism / Competition / Feedback 已经落到 parcel / frontage / lane / shared-space 层。当前无新的 foundational SKILL_GAP，建议继续 P05 URBAN_ENSEMBLE。**

本轮不是把父级 `DISTRICT-01` 机械切成几块地，而是从“西侧重复交割需要首卸与复核”继续生成共同院、门前地役、家庭混合用地、东向轻载与南后巷。四户条件分支占用与公共通行并集 1,457 blocks²，保持在父包 1,200–1,600 blocks² / 4–6 户约束内；第 5–6 户未被为了填满容量而提前画出。

更关键的是，v0.4 的底层机制没有停留在区域/聚落层：权利、有限知识、普通工程适应、补给节奏、空间竞争、分户压力和反馈都实际改变了 parcel / frontage / lane 关系。

---

## 1. Source / Isolation Audit

### PASS

- 主上游输入仅为 MP-P03 `PACKAGE-01 / DISTRICT-01` 及其必要局部引用；
- MP-P03M `assessment-data` 作为补充 planning assessment 使用，没有升格 Canon；
- CIV-001 README 仅作为批准 Canon；
- 未读取 MP-P03 / MP-P03M Independent Review；
- 未读取其它街区方案；
- 世界读取保持只读，`world writes = 0`；
- `level.dat` 与两个相关 region 前后 SHA256 一致。

P04 记录的 Vibe-Coding source revision 为 `0e4cfe2d...`，晚于 v0.4 基准提交 `6746b17a...`，但该提交本身是其它 my-world 状态更新。P04 登记的 `SKILL.md` SHA256 `a6f2e3d2...` 与 MP-P03M v0.4 实际读取字节一致，因此没有发生 Planner Skill 漂移。

### Note

本轮读取了 MP-P03 `planning-data.json` 中 DISTRICT-01 / ROUTE / SPACE / FRONTAGE 的必要父级局部引用。这属于 parent package 的可追溯下钻，不构成读取被禁止的独立答案。

---

## 2. Scale Discipline / Recursive Handoff

### PASS

L3 真正解决了当前尺度问题：

- block relationship；
- provisional parcel / use-right geometry；
- frontage；
- shared courtyard；
- lane / easement；
- conditional household allocation；
- L3-level capacity accounting。

同时没有越界到 Builder：

- parcel 不是建筑 footprint；
- 没有房间、屋顶、结构或 palette；
- 基础、门窗、精确建筑占地仍留给 L4 / Builder；
- 三个下游包均为 `DISTRICT → URBAN_ENSEMBLE`，`builder_ready = false`。

三包分别是：

1. 北混合前沿；
2. 南家庭合院；
3. 公共院 / 门前带 / 全部共享通路与短储接口。

第三包单独拥有公共接口是一个重要优点：公共空间不会被两个住宅包各自“局部优化”后重复占地或切断。

---

## 3. Parcel / Frontage Causality

### PASS

五个 parcel / shared holding 不是等宽切块：

- P01 因最先接西来货流，承担修理、值守、工具暂存，前沿更宽；
- P02 靠近东向轻载出口，强调复核 / 短宿而非重货堆积；
- P03 面向卸载院且需要前后出入，因此更深，但深层空气使其仍保持条件性；
- P04 的转角价值来自照看共同院与轻修，同时明确不能通过侵占共享通路兑现“临街价值”；
- P05 因共同短储功能与共有控制而抵抗继承切分。

这说明 `relative site value → competition → parcel / frontage response` 已经真正进入 L3，而不是只写在 Skill 理论里。

未分配的 475 格也没有被自动包装成“绿地”或下一户用地，保留为调查、边界与基底调整余量，符合 Existing Evolution / uncertainty discipline。

---

## 4. Agency & Rights

### PASS

空间变化有明确行动者与 veto：

- 地方共同体 / 现有使用者可以提供或拒绝公共院与地役；
- 家庭承担日需与公共通行义务；
- 商旅可因负担或垄断转向其它交割点；
- 三席议会没有被错误当成统一征地机关。

因此共同院、门前带、后巷并非“Planner 觉得方便所以存在”，而是依赖协议和用益权成立。

未证权利不会被画图自动变成产权事实。该行为符合 v0.4 Agency Kernel。

---

## 5. Bounded Knowledge / Historical Validity

### PASS

Growth chain 没有使用 Planner 的地下扫描结果作为历史行动者先验知识：

1. 重复短时交割 → 首卸院 / 短储；
2. 供水、日需、生计、权属成立 → 四家庭条件常住；
3. 门前交割开始妨碍家庭后勤 → 协商形成南后巷。

后巷来自重复使用暴露出的冲突，而不是一开始就为了完成“漂亮路网”画出的环路。

每一步可以停留，不依赖未来 5–6 户或未知矿业，因此 Historical Validity 成立。

---

## 6. Human Adaptation / Constraint Transformation

### PASS

P04 没有退回 v0.3 的环境决定论：

- 地面高差通过分段卸载、普通步级 / 路基 / 短挡护等低层适应来处理；
- 不要求整个共同院削成统一等高大平台；
- 井 / 蓄水 / 搬运继续作为候选方案，但没有虚构井位；
- 地下 24 格发现的更深空气没有导致全区禁建或机械缩容；
- P03 / L03 只把具体基础与重载位置留待更细复核。

正确边界也被保留：若必须大填大挖、巨井或其它与小型节点不相称的工程才能成立，则应回退而不是强救方案。

---

## 7. Effective Accessibility

### PASS_WITH_NOTE

街区内部已经把 heavy / light / pedestrian-service flow 区分出来：

- L01：西接首卸，驮运候选；
- L02：东向轻载；
- L03：南后巷，步行 / 分时清运，不承担整队重货；
- L04：北前沿门前地役。

但是 P04 仍明确承认：

- 图外西接坡连续驮运；
- 转弯 / 会让；
- 权利；
- seasonal usability；
- movement / collision

尚未实证。

这不是缺陷；L3 没有把“画出 lane”错误升级成可用道路事实。下一层必须继续关闭这些问题。

---

## 8. Metabolism / Resilience

### PASS

P04 没有只画货物流：

- 首卸 / 复核是周期高峰；
- 粮食与生活物是批量输入、每日消耗；
- 水是每日且峰值增加；
- 污物是日常暂存、定期清运；
- 修理是间歇性输入。

P05 只是短储，不重复充当整个聚落粮仓；家庭库存与父级共储不重复计量。

面对峰值，它首先使用错峰、分段和共同库存，而不是为了“韧性”凭空发明第二条全天候道路，说明 v0.4 resilience 没有退化成机械冗余 checklist。

---

## 9. Feedback / Demographic Pressure

### PASS

反馈链实际改变了形态：

```text
重复交割
→ 沿院服务价值提高
→ 四户条件常住
→ 门前后勤冲突
→ 南后巷
→ 后巷改善又可能提高分户压力
→ 公共院 / 通路 / 供给约束抑制无条件增密
```

第 5–6 户只保留为待证分支，没有因为父包上限存在就提前占用余地。这说明 demographic pressure 被作为过程，而不是人口数字配额。

---

## 10. Capacity / Geometry Audit

### PASS

- parent district：1,200–1,600 blocks² / 4–6 户；
- current branch：1,457 blocks² / 4 户；
- package accounting：269 + 275 + 913 = 1,457；
- shared public land 没有在多个 package 重复计量；
- technical validation 报告 parcel / lane cell overlap = 0；
- 原 ≤16 深空气与当前分配无重叠；
- 新 24 深 evidence 只改变风险标记与下层调查责任。

这里的 1,457 是 L3 的具体 planning geometry accounting，而非声称已有建成面积，因此该精度在当前尺度可接受。

---

## 11. Visual Evidence

### PASS_WITH_REVIEW_LIMIT

归档包含：

- `街区地块与通行.png`；
- `通路与高差剖面.png`；
- 两张同坐标阶段图。

Codex validation 记录实际查看 4 张图并修正：深空气符号遮蔽、阶段容量说明、门前衔接和空间编号。

本独立审核会话通过 GitHub connector 核对了地图文件、坐标对象、几何与生成后的 validation，但未直接解码查看 binary PNG 像素。因此本次 PASS 不以“独立视觉美观 / 可读性验收”为决定性依据。Owner 若发现主图难读，应作为 visual artifact correction 处理，不自动视为规划因果失败。

---

## 12. Findings Classification

### Finding A — Effective access remains unverified

**Class:** `TASK_SPECIFIC_JUDGMENT / EVIDENCE LIMITATION`  
**Severity:** non-blocking

需要 L4 / cross-package 继续确认图外西接驮运、跨边界接口、真实权利与 movement。

不建议修改 Skill。

### Finding B — P03 deeper void still unresolved

**Class:** `EVIDENCE LIMITATION`  
**Severity:** non-blocking

L3 正确地只把它变成拟用体积 / 基础核查责任，没有机械禁建。

不建议修改 Skill。

### Finding C — Public courtyard size remains throughput-sensitive

**Class:** `TASK_SPECIFIC_JUDGMENT`  
**Severity:** non-blocking

S01 细化后约 569.5 blocks²，理由是卸载、轮候、坡面分段与轻载转换。由于真实峰值货流仍未证，L4 应允许缩小非必要停留面或重新分时，而不是把该面积当永恒固定广场。

不建议修改 Skill。

---

## 13. Regression Conclusion

MP-P04 证明当前 Planner 已经可以把：

```text
POLITY_TERRITORY
→ REGIONAL_SYSTEM
→ SETTLEMENT
→ DISTRICT
```

连续下钻到具有 parcel / frontage / lane / shared-space 因果结构的街区，而没有越级成为建筑设计。

尤其重要的是，v0.4 的 Human Geography Kernels 在 L3 仍然产生实际空间后果，而不是只在高尺度写成背景理论。

### Skill decision

> **保持 minecraft-planner v0.4，不更新 Skill。**

下一步应继续 P05 `URBAN_ENSEMBLE`，验证最后一层 Planner 是否能把 parcel group / shared interfaces 转成真正 Builder-ready 的 design packages，同时仍保留 Builder architectural authorship。
