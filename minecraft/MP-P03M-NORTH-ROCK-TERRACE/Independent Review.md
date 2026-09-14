# MP-P03M Independent Review｜minecraft-planner v0.4

日期：2026-09-14  
审核对象：`minecraft/MP-P03M-NORTH-ROCK-TERRACE/`  
实现提交：`118bf8a02a89be76c6c452ce7ba422565ace2d0e`  
测试：`MP-P03M｜CIV-001 东域北岩台长期聚落专项复核 / SETTLEMENT`

## Verdict

> **PASS_WITH_NOTES — v0.4 Human Geography Decision Kernels 专项回归通过。**

本轮最重要的验证目标不是重做 MP-P03 聚落总图，而是检查 v0.4 是否能把同一批环境事实从“未天然闭合即接近 blocker”的静态适宜度逻辑，升级为“行动者 + 能力 + 普通适应 + 有效通达 + 供给节奏 + 反馈”的人类地理判断。该目标已实现。

北岩台不再因为没有已证高台地表水、裸岩占优或存在浅层空气而被机械降为零常住或整体禁建。Planner 对水、食物/燃料、通达、浅层空洞/砂砾和局部危险分别列出时代与规模相称的适应方式、承担者、负担、验证条件、残余约束和否决边界；只有当普通工程、移位、分期和制度协作均不足以维持父包关系时，才触发上游修订。

当前没有新的 foundational SKILL_GAP 需要在 P04 前修复。v0.4 可继续进入 DISTRICT 回归。

---

## 1. Source / Isolation Discipline

输入边界基本符合专项任务要求：

- 使用 `minecraft-planner v0.4`，固定到 Vibe-Coding `6746b17af504b31b790e425d6f36bf2a2ac5f480`；
- 使用 CIV-001 当前批准 Canon；
- 使用 MP-P02R `PACKAGE-01` 及必要上游 ROUTE 引用，保持为 `DESIGN_PROPOSAL`；
- 从 MP-P03 仅读取获准的事实/派生调查证据、provenance 和地图底图；
- 明确未采用 MP-P03 聚落方案、planning-data、implementation-packages、Critic/Gate 或 Independent Review；
- 未把父规划或事实调查升级成 World Canon。

Canonical technology support 也没有越界：CIV-001 Canon 明确具备成熟前现代石木、桥梁、水利、矿山、冶炼与手工业工程，因此“调查普通井、蓄水、局部路工、挡护”等属于合理能力范围，而不是为测试临时发明超时代技术。

`world writes = 0`。validation 显示本轮涉及的 `level.dat` 和两个 region 文件前后 SHA256 一致；没有再次启动游戏/服务器或写存档。

---

## 2. v0.4 Target Behavior

### 2.1 Mitigation 不再等于自动许可，也不再等于自动否决

`CT-WATER` 的处理是本轮最关键证据：

- 井：Canon 能力支持“调查”，但地下水与开凿负担仍未知；
- 蓄水/雨水：明确“储存本身不产水”；
- 低处水搬运/局部提水：需验证水点、通路和日常劳动；
- 深岩巨井、长距离大型引水等不相称方案明确不能被包装成普通低成本工程。

因此，“没有已证高台地表水”被正确转换为**供水工程与运营约束**，而不是“绝对无水 / 无法居住”。

同样，浅层空气被转换成拟用位置调查、局部移位/跨越/地基调整问题；Planner 明确不整体填洞、不全台禁建，也不把“未发现空气”当结构安全证明。

### 2.2 Agency / Power 已进入空间因果

本轮没有把“社会”当作单一理性行动者。至少区分：

- 地方共同体与土地使用者；
- 承担交割的商旅与生产家庭；
- 常住服务家庭。

并记录各自受益、负担、合作条件和 veto。地方共同体能否允许共院、取水与通路，商旅是否愿意承担运输，服务家庭是否愿意承受输入依赖，都会改变节点是否形成。三席议会没有被当成可以自动征地和强制建镇的中央 Planner。

### 2.3 Bounded Knowledge 正常工作

Planner 明确把地下空气识别为 Planner-only evidence，没有把完整地下扫描倒写成早期居民知识；形成路径依赖行走、取水、试用和逐步发现。未证远端资源也没有进入早期选址原因。

这说明 Historical Validity 已从“未来阶段不能预知”进一步升级为“历史行动者不能拥有 Planner 的全图知识”。

### 2.4 Metabolism / Resilience 不再只有箭头 Flow

本轮区分了：

- 水的日常消耗；
- 粮食/燃料的批量输入；
- 交割日旅客和牲畜峰值；
- 家庭储存与共同储备；
- 补给中断与缓冲。

没有编造具体库存吨位或补给天数，而是把它们留给下层依据实际节奏闭合。对韧性也没有为了“冗余”凭空画第二条道路，而优先采用家庭+共同库存、错峰、地方分点等与已知规模相称的缓冲方式。

### 2.5 Feedback 已进入 Growth

逻辑不再只是单向增长：

`供水/路工改善 → 服务家庭与交割增加 → 公共院/取水压力上升 → 错峰、分点或增长受抑制`。

这已经构成有效的正/负反馈，而不是“基础设施一建，城市必然继续膨胀”。

---

## 3. Capacity / Spatial Consequence

本轮没有因为 v0.4 强调人类适应，就反向把所有约束抹平。

- 父包 `12–24户 / 3,500–8,000 blocks²` 被保留为 **LOW-confidence conditional range**；
- 首段只论证 `12–16户 / 3,500–5,000 blocks²`；
- 上限只有在更高服务压力、供水/通达继续成立、基底与用地核定后才可兑现；
- 若日常供给尚未闭合，常住容量保持 `UNRESOLVED`，而不是自动等于 0。

这比 MP-P03 中“水未闭合时常住分支直接归零”的处理更符合比例原则，同时仍保留真实的扩张限制。

A/B 调查窗也没有被误写成建成边界：A 作为优先核查区域，B 因砂砾与浅层空气更多而后置细查，但都不是“可建设面积”或“禁建区”。

---

## 4. Critic / Handoff

本轮自检已经覆盖 v0.4 的新增核心项：Agency、Knowledge、Mitigation、Metabolism/Resilience、Feedback，同时保留 Terrain/Surface/Capacity/Anti-Zoning/Recursive Handoff 等旧测试。

状态 `HANDOFF_READY` 在本专项中成立，因为下一层问题被明确拆成供水、有效通达、真实交换需求/供给、基底/占地、权利等调查项；并明确不是 Builder-ready、不是施工授权、不是全年宜居证明。

---

## 5. Findings / Notes

### NOTE-01｜Capacity 上限仍是父包压力假说

`8,000 blocks² / 24户` 当前不是被本轮空间或供给证据独立证明的容量，而是保留的上游低置信上限。Planner 已正确注明这一点，因此属于 `TASK_SPECIFIC_JUDGMENT / EVIDENCE_LIMITATION`，不是 Skill 缺陷。P04/P05 若继续收敛，不应机械维持该上限。

### NOTE-02｜Effective accessibility 仍未做现场连续路线证明

西侧/西南方向仍是关系方向与调查对象，不是已证驮路。v0.4 已正确将 physical + rights + season + transport mode 组合成待验证的 effective access。此项应继续留给后续证据，而不是为了完成专项回归提前“算成 PASS”。

### NOTE-03｜Visual binary 未在本次 GPT 审核中逐像素复核

归档包含两张坐标图，artifact/validation 显示可重复生成且 Planner 已做可读性检查；本次独立审核主要核对文本、machine-readable assessment、source register 与 validation，没有把二进制图像视觉品质作为本轮 PASS 的决定性依据。P04 进入细粒度街区后，Owner-facing visual 应重新成为强审核项。

---

## 6. Final Decision

> **PASS_WITH_NOTES — MP-P03M 验证了 minecraft-planner v0.4 的核心升级。**

特别是以下行为已经被证明：

1. `unknown natural convenience ≠ settlement blocker`；
2. `constraint → proportionate mitigation → residual constraint` 可以实际改变结论；
3. Actor / rights / veto 会进入空间因果；
4. Planner knowledge 不会自动泄漏给历史行动者；
5. Flow 会与 stock / buffer / rhythm / resilience 一起考虑；
6. Growth 能产生反馈而不是只做单向阶段链；
7. 适应能力不会被误用为“任何地方都能建”的万能豁免。

**Recommendation：不修改 v0.4，进入 MP-P04 DISTRICT。**
