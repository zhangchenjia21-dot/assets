# M01｜From-Zero Historical Building Generalization — 归档

Runner: **DEEPSEEK-M01** ｜ Skill: **minecraft-builder v1.10** ｜ 日期: 2026-09-12

模型能力基准 M01 的完整成果归档：从零研究、原创设计并建造一座约 1500 年前后的
北德汉萨城市**市政厅兼交易大厅**（Rathaus und Kaufhaus der Stadt Wiethmar，虚构城市）。

**交付状态：`FINISHED`**（未标 `VERIFIED`；真实客户端感知验证在本工具链下不可用，见 Completion Report §9）。

---

## 快速导航

| 想了解 | 看这里 |
|--------|--------|
| 结论、Gates、验证结果、限制 | `evidence/Completion_Report.md` |
| 为什么这样设计 | `design/02_Architectural_Intent.md` |
| 研究来源与提取结论 | `research/01_研究记录.md` |
| 施工代码（Builder Core） | `tools/建筑生成器.mjs` |
| 施工代码（Finishing 五 Pass） | `tools/精修.mjs` |
| 实际使用的 Skill 原文 | `_skill_SKILL_v1.10.md` |
| 逐格验证结果 | `evidence/verify-report.json` |
| 不依赖图像的结构断言 | `evidence/结构闭合与附着性核验.md` |
| 视图证据（24 张同机位 PNG） | `evidence/views/` |
| 精确剖面 / 平面 | `evidence/preview/section-*.txt`、`plan-y*.txt` |
| 复现命令 | 本文 §复现 |

---

## 主要结果

| 项 | 值 |
|----|----|
| 测试世界 | `MB-V110-M01-DS-汉萨市政厅`（全新 26.2 超平坦，关闭结构生成，生成器回读 `FlatLevelSource`） |
| 最终方块数 | **30 253**（世界实测，已双向核对） |
| 状态种类 | 62 |
| 施工阶段 | Builder Core 8 个（S1–S8）+ Finishing 5 个 Pass（F1–F5） |
| 正向逐格比对 | 30 253 格，**不一致 0** |
| 反向多余方块 | 26 245 格，**全部为超平坦默认地层**，无旧几何残留 |
| 关键路径净空 | 10 条，9 条完全通过 + 1 条检查器口径边界（见 Completion Report §6.2B） |
| Repair 轮次 | 14 项真实缺陷，均记录在 Completion Report §8 |

### Skill 版本证据

| 项 | 值 |
|----|----|
| 来源 | `zhangchenjia21-dot/Vibe-Coding` → `skill/codex/minecraft-builder/SKILL.md` |
| SHA256 | `1C719DB419F51410BA894D9731AB2026E68B4BBCB73B9C092863DFB5EDD85F9E` |
| 行数 / 字节 | 1188 行 / 52396 字节 |
| 版本确认 | 首行 `# minecraft-builder v1.10` |

> 会话内置 skill 为 v1.0（6242 字节），**未**用于本任务。

---

## 目录结构

```
MB-M01-DS/
├── _fetch_skill_v110.mjs          Skill 原文获取脚本（经本地代理 + TLS 隧道）
├── _skill_SKILL_v1.10.md          实际使用的 Skill 原文（SHA256 见上）
├── SHA256.json                    全部归档文件的 SHA256 清单
├── research/
│   ├── 01_研究记录.md              6 项真实历史/类型学来源与提取结论
│   ├── blocks_schema.json         从 26.2 客户端 jar 提取的 1198 个方块状态 schema
│   └── palette.json               1555 个候选状态的合法性验证结果映射
├── design/
│   └── 02_Architectural_Intent.md Purpose / Users / Site / Program / Space Graph /
│                                  Hierarchy+Sequence / Plan+Section / Structure / Form+MC Translation
├── tools/                         全部可复核施工与核验代码
│   ├── 提取方块schema.mjs          从 jar 提取权威状态定义
│   ├── 验证调色板.mjs              真实世界放置候选状态
│   ├── 解码调色板.mjs              解码扫描 → 状态合法性映射
│   ├── 几何核心.mjs                方块写入、冲突检测、分层绘制、状态合法性断言、出图
│   ├── 设计参数.mjs                控制线、材料语言、拱券几何
│   ├── 建筑生成器.mjs              S1–S8 全部施工代码
│   ├── 精修.mjs                    F1–F5 五个 Finishing Pass 全部代码
│   ├── 蓝本.mjs                    Core / Finishing 阶段装配
│   ├── 构建.mjs                    CLI：report / create / build / rebuild / rebuild-core
│   ├── 基线.mjs                    SPATIAL_COMPLETE 基线与 Frozen Core 记录
│   ├── 结构自检.mjs                悬空检测、Movement Envelope、空间连通体积
│   ├── 核验世界.mjs                全卷双向比对 + 结构自检
│   ├── 体素渲染.mjs                扫描/蓝图 → PNG
│   ├── 预览.mjs                    蓝本预览渲染
│   ├── 视图证据.mjs                12 机位同机位视图生成
│   └── 执行器.mjs                  离线执行器封装（含瞬时错误重试）
└── evidence/
    ├── Completion_Report.md        完整交付报告（含限制与未验证边界）
    ├── 结构闭合与附着性核验.md      不依赖图像的结构断言
    ├── world-identity.json         世界身份与创建/重建作业
    ├── verify-report.json          双向比对、悬空、路径净空、空间成立性
    ├── palette-G0-*.json           调色板验证原始证据
    ├── baseline/                   SPATIAL_COMPLETE 基线（Core 报告、Frozen Core、基线世界）
    ├── preview/                    蓝本报告 + ASCII 剖面 / 平面
    └── views/                      24 张同机位 PNG（baseline 12 + final 12）+ 两份 manifest
```

> `jobs/`（约 75 次离线作业的中间产物）与 `snapshots/`（27 个 pre-rebuild 存档快照）
> **未纳入归档**：前者是执行器临时产物，后者是游戏存档数据，按归档规范不上传。
> 关键作业与结果已摘录到 `evidence/`。

---

## 建筑概要

- **身份**：市议会 + 交易厅同体。议会占据交易厅上层，因此"上楼"就是"进入权力"。
- **竖向**：地窖（酒/盐/粮）→ 交易层（Kaufhalle，带市场侧拱廊）→ 议事层（Ratsstube / Kanzlei /
  Schatzkammer / 法院厅）→ 大厅层（Festsaal）→ 阁楼 → 屋脊钟塔。
- **结构**：一层砖墩 + 纵向筒拱的承重防火层，墩距 6 格决定拱廊开间与交易厅跨度；
  二层为无柱木屋架大厅（跨度 19 格），屋脊沿东西向贯通，两端形成阶梯山墙。
- **三套流线**：公众（广场 → 门廊 → 主楼梯 → 大厅）；货流（北院 → 过秤间 → 交易厅 → 地窖）；
  议会（后勤门 → 后穿通 → 服务梯 → 议事层）。
- **制度空间**：市场侧拱廊设摊位与**市秤**（公秤必须在公共可达处）；上层设议事厅、市长室、
  带铁门的金库、法院厅。

---

## 复现

需要正式离线执行器（`AI-Offline`）与 Minecraft 26.2 / Fabric 0.19.5 运行时。

```bash
node tools/构建.mjs report                  # 生成蓝本并自检（不写世界）
node tools/构建.mjs rebuild-core            # 重建为 SPATIAL_COMPLETE（Finishing 前基线）
node tools/视图证据.mjs baseline "基线"      # 生成基线同机位视图
node tools/构建.mjs rebuild                 # 重建为 FINISHED
node tools/核验世界.mjs                      # 全卷双向比对 + 结构自检
node tools/视图证据.mjs final "FINISHED"     # 生成同机位终稿视图
```

---

## 必读限制

1. **视图证据不是真实客户端截图。** 本 Harness 无客户端控制/截图工具，用的是从存档扫描数据渲染的
   体素透视（正交/透视 + 朗伯光照 + z-buffer）。**不含真实材质贴图、光照模型、方块模型细节、
   FOV 与移动尺度体验**。渲染器把玻璃画成不透明，楼梯/栏杆按整块立方体光栅化
   （本轮已把楼梯改为按 facing 的半高近似）。
2. **内景视图可读性低**，不能单独支撑"重要二层空间 / 垂直交通"的感知判断；已用精确剖面/平面文本证据互补。
3. **碰撞验证为体素近似**（1×2 保守包络 + 1 格台阶假设），未模拟 Minecraft 真实 step-height 与半砖碰撞盒。
4. **悬空扫描为启发式分类**，不是结构受力分析。
5. 完整限制清单见 `evidence/Completion_Report.md` §9。

---

## 测试纪律声明

- 未读取 T01—T12 Independent Review、Owner 历次反馈、regression reports、过去测试的 Completion Report、
  REF-0123 资料、其它模型本轮 M01 的工作目录/报告/世界。
- 未自行判断本轮 Skill 是否 PASS、未评价自身相对其它模型的优劣、未推断基准排名。
- 未修改 minecraft-builder Skill；未正式注册新资产；未进入 `建筑师` 正式存档。
- 本归档只包含当前任务成果、复现脚本与必要说明；未上传完整游戏存档、备份或凭据。
