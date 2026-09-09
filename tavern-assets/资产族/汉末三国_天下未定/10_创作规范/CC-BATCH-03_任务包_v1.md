# TASK｜STA-CC-BATCH-03｜黄巾大乱时代人物卡生产

- **Type**：content-creation（内容创作，非代码 / 非 Runtime 重构）
- **Owner**：执行 Agent；Independent Review 由项目所有者另行指派
- **Repo**：`zhangchenjia21-dot/sillytavern-assets`
- **Branch**：新建 `cc-batch-03`
- **Base HEAD**：`1179620`（main 当前 HEAD，开始前重新核验）

## Outcome

产出 CC-BATCH-03 全部 **14 张**黄巾大乱时代（184–189）人物卡，全部符合 DSH-native 新创作规范，通过批次级跨卡审核，同步家族索引与版本锁。

## Why Now

旧 S/A 级名单已由 CC-BATCH-01/02（36 卡）完成。本批是第一个按"主时代、次阵营"原则组织的批次，也是新 `创作规范/` 的首次正式应用。184 开局锚点当前几乎无卡可用。

## Authority / Source Manifest

1. 本 Task Packet；
2. `创作规范/DSH-native_创作总规范_v0.1.md`（draft，本项目所有者已批准作为本任务执行依据）；
3. `创作规范/人物卡_创作模板_v0.1.md`（draft，同上）；
4. `资产族/汉末三国_天下未定/10_创作规范/CC-BATCH-03_生产规划_v0.1.md`——名单、逐卡功能定位与测试重点、生产顺序、验收 Gate 以它为准；
5. 范例：`人物卡/汉末三国/CC-BATCH-01/曹操__Character_Card__v0.1.2.md`（目标形态的直接范例）。

不具权威性：`99_归档/` 内的旧规范与旧生产规划（仅历史参考）；任何 Resolver / Bootstrap / Creator / asset-spec 概念。

## Read First（最小充分工作集）

1. 仓库根 `AGENTS.md` 与 `资产族/AGENTS.md`；
2. 本 Task Packet；
3. `创作规范/DSH-native_创作总规范_v0.1.md`、`创作规范/人物卡_创作模板_v0.1.md`；
4. `资产族/汉末三国_天下未定/10_创作规范/CC-BATCH-03_生产规划_v0.1.md`；
5. 范例曹操卡全文；
6. 世界包第四、五章（`世界包/汉末三国_天下未定_World_Pack_v0.2.3.md` 的六个历史阶段与开局锚点 5.1 / 5.2）。

只有在证据不足时才扩大读取；扩大后说明原因。

## 名单（14 张，顺序即生产顺序）

董卓（S 待遇）→ 张角（A）→ 皇甫嵩（A-）→ 刘宏（B+）→ 孙坚（A-）→ 张让（B+）→ 卢植（B+）→ 韩遂（B）→ 何进（B+）→ 刘虞（B）→ 朱儁（B+）→ 张燕（B）→ 陶谦（B）→ 刘焉（B）

逐卡功能定位与测试重点见生产规划第 3 章，**不得跳过**。

## Decision Digest

- **DEC-01** 目标宿主 = The World on DeepSeek Harness。不得假设 Resolver / Bootstrap / Creator / asset-spec / Manifest / Validator 存在。
- **DEC-02** 一人一卡；时间字段最小化（只强制生年）；未知优先于虚构。
- **DEC-03** 不预写未来：本批多数人物在原史中死于 189–200 之间，卡内不得携带其死亡方式与后续政局；原史是来路不是剧本。
- **DEC-04** 知识边界按"凭什么知道"写（模板第七节）；GM / 世界包 / 玩家知道的事不等于人物知道的事。
- **DEC-05** 依赖只用自然语言（可选性声明 / 协同降级双写 / "X 属于《Y》"归属指引）；禁止机器依赖字段与机器元数据。
- **DEC-06** frontmatter 只含人工治理字段；资产间引用一律用 Markdown 相对路径，**禁止 `[[wikilink]]`**。
- **DEC-07** 每卡至少一个日常面 + 一个非功能性互动面（Life Loop 素材）。

## Invariants

- **INV-01** 人格是生成式决策结构，不是标签。名人标签核查：董卓≠魔王、张角≠妖道、刘宏≠昏君、何进≠优柔寡断。
- **INV-02** 共享历史一致：黄巾起事、平叛进程、凉州叛乱的史实归属世界包，人物卡只写个人经历视角，不复制战争年表。
- **INV-03** 关系对称：卢植↔刘备、孙坚↔孙策、刘虞↔公孙瓒、刘焉↔刘璋、董卓↔吕布五组须与既有卡对齐（写卡前读对应既有卡的关系节）。
- **INV-04** 密度优先，不设字数门槛：不做强制压缩，不因卡片短而注水，也不因内容多而机械精简；每节内容必须能改变 GM 的判断。
- **INV-05** `player_character_supported`：董卓、孙坚、张角 = true；刘宏、张让 = false；其余逐卡评估并写明理由。

## Acceptance Gates

- [ ] **AC-01** 14 张卡齐备，八节骨架完整（含第七节知识边界、第八节开局状态与历史边界）；
- [ ] **AC-02** 每张卡过 `人物卡_创作模板` 检查表全部项；
- [ ] **AC-03** 批次级 Gate 全过（生产规划第七章：共享历史 / 关系对称 / 声线收敛 / 未来无污染 / 名人标签 / 索引同步）；
- [ ] **AC-04** 旧 Runtime 语言零残留：`grep -rn -i -E "Resolver|Bootstrap|asset-spec|Creator|Handoff|Ownership Map|typed|Manifest|Validator" 人物卡/汉末三国/CC-BATCH-03/` 无命中（Revision Notes 元描述除外）；
- [ ] **AC-05** 无 wikilink：`grep -rn "\[\[" 人物卡/汉末三国/CC-BATCH-03/` 无命中；
- [ ] **AC-06** 家族 `00_资产成员索引.md` 与 `03_当前版本锁.md` 已同步；
- [ ] **AC-07** 产品价值面：GM 读完每张卡能直接演出这个人（由项目所有者验收，Agent 最高宣布 READY FOR OWNER UAT）。

## Scope

**Allowed**：
- 新建 `人物卡/汉末三国/CC-BATCH-03/`（14 个文件，命名 `人物名__Character_Card__v0.1.md`）；
- 新建 `资产族/汉末三国_天下未定/10_创作规范/CC-BATCH-03_批次索引_v0.1.md`（Roster + 跨卡审核记录）；
- 更新 `资产族/汉末三国_天下未定/00_资产成员索引.md`、`03_当前版本锁.md`；
- 修正既有卡中与本批直接冲突的事实性错误（需在 Final Report 单独列出并说明）。

**Prohibited**：
- **NON-01** 不得修改 `main`；不得 merge、不得开 PR；
- **NON-02** 不得修改 `创作规范/`（发现规范问题记入 Final Report Remaining，由所有者裁定）；
- **NON-03** 不得修改世界包与既有 36 张卡（INV-03 要求读取它们，但只允许按 Allowed 第 4 条修正事实冲突）；
- **NON-04** 不得把 Research Note 交付进仓库（考据浓缩进卡内"可选｜极简史料备注"节）；
- **NON-05** 不得新增名单外人物；不得拆分 / 合并名单人物；
- **NON-06** 不得发明任何机器协议、Schema、Manifest 或运行时指令。

## Deliverables

1. 14 张人物卡（逻辑分组 commit，建议：董卓+张角 → 汉廷四张 → 平叛三将 → 叛乱与地方五张 → 跨卡一致性清理）；
2. 批次索引与跨卡审核记录；
3. 家族索引 / 版本锁同步；
4. Final Report。

## Validation

内容任务，无自动化测试。最低验证命令见 AC-04 / AC-05；另逐卡核对版本号 `v0.1`、frontmatter 最小集、Revision Notes 存在。

## Git / Integration

- 从 `1179620` 新建 `cc-batch-03`；开始前记录 `git status`；
- push 前重新 fetch 核验 origin/main HEAD，HEAD 变化时停止并返回；
- 不 merge 到 main；完成后 push `cc-batch-03`，由所有者安排 Independent Review。

## Stop / Return Conditions

- 生产规划与新规范实质冲突；
- 某张卡的史实处理会实质改变产品语义（如张角超自然口径拿不准）；
- 必须改动 Prohibited Scope 才能完成任务。

## Final Report 格式

```markdown
## Result
PASS | PARTIAL | BLOCKED | READY FOR OWNER UAT

## Files Created
- 14 张卡 + 索引（全列）

## Cross-card Decisions
- 关系对称处理 / 共享历史归属 / 声线区分结果

## Evidence
- AC-04 / AC-05 命令输出摘要
- 逐卡检查表结论

## Git
- base HEAD / final HEAD / branch / commits

## Remaining
- 留待所有者裁定的问题（含对创作规范的反馈）
```
