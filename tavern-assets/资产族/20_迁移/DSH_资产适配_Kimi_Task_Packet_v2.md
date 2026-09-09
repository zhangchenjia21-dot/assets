# Kimi Task Packet｜剩余资产 DSH-native 适配 v2（全量收口）

- **Task ID**：STA-ADAPT-02
- **类型**：内容 / 语义适配（非 Runtime 重构）
- **Owner**：Kimi Code（Executor）；Independent Review 由项目所有者另行指派
- **Repo**：`zhangchenjia21-dot/sillytavern-assets`（private）
- **Branch**：新建 `dsh-adaptation-kimi-v2`
- **Base HEAD**：`68f345ab21d374640e7b886bdbd48bf44c789817`（即 `dsh-adaptation-kimi-v1` 当前 HEAD；v1 已通过验收，作为本次工作的基线与范例）

## Outcome

把仓库中**剩余全部 18 个内容资产**适配为适合 **The World on DeepSeek Harness (DSH)** 的 DSH-native Source Assets，使仓库全部世界包、人物卡、拓展包完成同标准收口。

## Why Now

v1 已完成汉末三国世界包、36 张汉末人物卡、8 个拓展包的适配并通过验收。项目所有者已确认该扩围为正式授意方向。剩余资产仍带旧第二版 SillyTavern Runtime 机制语言（每文件 15–56 处），不完成收口则资产库处于双标准并存状态，无法整体进入 The World 试用。

## Authority / Source Manifest

1. 本 Task Packet；
2. v1 任务包：`资产族/汉末三国_天下未定/20_迁移/DSH_资产适配_Kimi_Task_Packet_v1.md`（适配方向、产品决策保留清单、验收标准全文仍然有效，本包不重复展开）；
3. v1 已适配资产 = 目标文体与结构的直接范例；
4. 项目所有者口头裁定（2026-08-24）：v1 超清单扩围为正式授意，本次为剩余资产全量收口。

## Read First（最小充分工作集）

1. 仓库根 `AGENTS.md`
2. `资产族/AGENTS.md`
3. 本 Task Packet
4. `资产族/汉末三国_天下未定/20_迁移/DSH_资产适配_Kimi_Task_Packet_v1.md`
5. 范例三份（各代表一类资产的适配后形态）：
   - `世界包/汉末三国_天下未定_World_Pack_v0.2.3.md`
   - `人物卡/汉末三国/CC-BATCH-01/曹操__Character_Card__v0.1.2.md`
   - `拓展包/通用拓展包/战斗核心_Expansion_Pack_v0.1.md`
6. 目标资产原文

## Files To Adapt（18 个，全量清单）

### World Pack（1）
1. `世界包/埃瑟维亚_诸界余辉_World_Pack_v0.1.3.md`（4193 行）

### Character Cards（10）
2–11. `人物卡/诸界余辉/CC-01` 至 `CC-10` 全部 10 张（各 564–617 行）

### Expansions（7）
12. `拓展包/通用拓展包/名望与社会评价核心_Expansion_Pack_v0.1.md`
13. `拓展包/通用拓展包/家族与亲缘核心_Expansion_Pack_v0.1.md`
14. `拓展包/通用拓展包/政治与公共权力核心_Expansion_Pack_v0.1.md`
15. `拓展包/通用拓展包/组织与任职核心_Expansion_Pack_v0.1.2.md`
16. `拓展包/通用拓展包/魔法族/魔法基础_Expansion_Pack_v0.3.md`（2990 行）
17. `拓展包/通用拓展包/魔法族/神术与信仰_Expansion_Pack_v0.2.1.md`（3631 行）
18. `拓展包/通用拓展包/魔法族/战斗魔法_Expansion_Pack_v0.3.md`（2255 行）

## DEC（沿用 v1，此处仅列对本次最关键的）

- **DEC-01** 目标架构 = DSH + World Core + Persistent Workspace + Source Assets。不得假设 Creator / asset-spec / Resolver / Bootstrap / World OS / Atomic Commit / typed Event / compiler / Owner Registry / UI binding 存在。
- **DEC-02** Source Assets = 赛前可复用素材；`games/<game-id>/` = 活的局内现实；局内变化永不回写 Source。
- **DEC-03** `GM / Source / System knows X != NPC knows X`。人物卡不授予 NPC 全量 Source 知识；每份资产都要让 GM 容易问"这个人为什么会知道？"。
- **DEC-04** 拓展包只加可玩机制域，不重建 Runtime；可选包须玩家显式选择才激活；不得新增 Required / Recommended / Optional 机器依赖元数据。
- **DEC-05** 机制不得拍平成纯 lore。保留真正改善游玩的机制区分；数值只在真正改善游玩时保留。
- **DEC-06** Markdown-first，强模型推理为默认；语义引导优先于流程机械。

## 诸界余辉 / 魔法族专项适配指引（相对 v1 的新增语义）

诸界余辉是虚构奇幻世界，没有真实历史，但同样的边界语义适用，按下述对应关系处理：

- **T0 边界**：正史 / 设定（canon）定义开局前的世界；开局后未来开放，game-local reality 高于 canon 默认轨迹；不存在"剧情修正力"。
- **神与超自然**："神是真实角色，不是作者视角"必须保留并强化——神的知识同样有其世界内来源与边界，不是 GM 全知的传声筒。
- **魔法机制**：魔法族三包共 8876 行，是本次最大工作量。保留魔法层级、术式标准化、施法裁定、反应窗口、神术与信仰的社会机制等**可玩语义**；删除的是运行时管路（Handoff、Resolver 契约、typed 字段、UI/Module 绑定、机器校验表），不是机制深度。
- **法术目录不是行为白名单**：这一原则必须保留，与 The World 的 Unlimited Attempt 一致。
- **人物卡 `Dependencies:` 机器字段**：删除，改为自然语言的"与哪些资产配合更好"段落（参照 v1 汉末人物卡处理方式）。
- **政治与公共权力核心**：与已适配的《政争与势力》语义对齐——政治行为遵循利益、身份、关系、信息与当前条件；不得留下统一合法性分数 / 确定性状态机写法。

## Allowed Scope

- 在原路径原地修改上述 18 个文件；
- 在 `资产族/20_迁移/`（新建家族中立目录）提交本 Task Packet 副本作为首个 commit；
- 修正目标文件内部指向已删除结构的直接断引用。

## Prohibited Scope（NON）

- **NON-01** 不得修改 `main`；不得在 v1 分支上继续提交；
- **NON-02** 不得修改 `zhangchenjia21-dot/the-world`；
- **NON-03** 不得重命名文件、不得提升资产版本号、不得归档旧文件；
- **NON-04** 不得触碰 v1 已适配的 45 个资产（断引用修正除外）；
- **NON-05** 不得修改资产族治理文档（`00_资产成员索引`、`01_资产组合总蓝图`、`03_当前版本锁`、`10_创作规范/` 等）——治理文档与版本锁同步属于发布治理，另行裁定；
- **NON-06** 不得发明新的 universal schema / manifest / validator / runtime；
- **NON-07** 不得删除世界深度换取篇幅——删工程包袱，不删世界内容。

## Deliverables

1. 18 个原地适配完成的资产文件；
2. 逻辑分组 commit（建议顺序：本 Task Packet → 诸界余辉 World Pack → CC-01~05 → CC-06~10 → 通用拓展包 4 个 → 魔法族 3 包 → 跨资产一致性清理）；
3. Final Report（格式见下）。

## Acceptance Gates

PASS 仅当全部为真（沿用 v1 标准，含奇幻世界对应项）：

- [ ] 资产不再依赖旧 SillyTavern Runtime 架构即可使用（Resolver / Bootstrap / Creator / Handoff / Ownership Map / typed / Owner Registry 等关键词正文零残留，修订说明中的元描述除外）；
- [ ] DSH GM 能直接理解每份文件如何使用；
- [ ] 诸界余辉 World Pack 保持世界深度（魔法文明、社会、地理、纪元内容不得因旧文件长而被删成短 prompt）；
- [ ] 人物卡保留独特人格与设定根基，知识结构对齐 v1 七段式；
- [ ] 拓展包保留真实可玩机制（魔法层级 / 裁定流程 / 反应窗口等），不是只有描述；
- [ ] Source truth vs game-local truth 清晰；canon 不是强制未来；
- [ ] NPC（含神、系统）知识来源清晰；
- [ ] 可选拓展包不静默激活；
- [ ] 未新增 universal schema / manifest / validator / runtime；
- [ ] 中文行文比旧版更干净、更本土自然；
- [ ] 每份文件带与 v1 同格式的 Revision Notes，version 字段不变。

## Validation

适配为内容任务，无自动化测试。最低验证命令：

```bash
# 旧机制语言残留扫描（应只剩修订说明元描述）
grep -rn -i -E "Resolver|Bootstrap|World OS|asset-spec|Creator|Handoff|Ownership Map|Resolution Contract|Program Authority|typed mutation|Atomic Commit|Owner Registry" 世界包/埃瑟维亚* 人物卡/诸界余辉/ 拓展包/通用拓展包/名望* 拓展包/通用拓展包/家族* 拓展包/通用拓展包/政治* 拓展包/通用拓展包/组织* 拓展包/通用拓展包/魔法族/

# 版本号未变核验（逐文件与 base 对比 frontmatter version 字段）
```

## Git / Integration

- 从 `68f345ab21d374640e7b886bdbd48bf44c789817` 新建 `dsh-adaptation-kimi-v2`；
- 不 merge 到 main；不开 PR；
- push 前 re-check 远端 HEAD，不得旧基线覆盖新提交；
- Final Report 给出 base HEAD、final HEAD、commit 清单。

## Stop / Return Conditions

出现以下情况立即停止并返回，不得自行裁决：

- 发现目标文件与 v1 已适配资产存在语义冲突，无法在资产层面安全解决；
- 魔法族三包中发现某机制删除与否会实质改变产品语义（升级为所有者裁定）；
- 需要改动 Prohibited Scope 中任何一项才能完成任务。

## Final Report 格式

```markdown
## Result
PASS | PARTIAL | BLOCKED

## Files Adapted
- path（18 个全列）

## Main Changes
- 移除的旧 runtime 假设
- 保留 / 强化的玩法语义
- 中文本地化改进

## Cross-asset Decisions
- 依赖关系变化（Dependencies 字段处理）
- 知识边界变化
- canon / T0 边界处理

## Git
- base HEAD / final HEAD / commits

## Remaining
- 留待所有者裁定的问题
```

完成后由项目所有者安排 Independent Review，通过前不视为可进入 The World。
