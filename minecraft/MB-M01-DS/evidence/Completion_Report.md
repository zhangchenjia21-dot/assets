# Completion Report｜M01 From-Zero Historical Building Generalization

Runner ID: **DEEPSEEK-M01**
测试主题: 从零研究、原创设计并建造一座约 1500 年前后的北德汉萨城市市政厅兼交易大厅
Skill: **minecraft-builder v1.10**（原文使用，未修改、未删减、未改写为简化版）
世界: **MB-V110-M01-DS-汉萨市政厅**（全新 26.2 超平坦，关闭结构生成）
交付状态: **`FINISHED`**（当前工具能力下）；未验证边界见 §9

---

## 1. 环境与版本信息

| 项 | 值 |
|----|----|
| Harness | DeepSeek Harness（DSH Web GUI） |
| Model | deepseek-flash |
| 日期 | 2026-09-12 |
| Minecraft | 26.2（Fabric Loader 0.19.5） |
| 执行器 | AI-Offline 离线执行器（Fabric 服务端 26.2 + WorldEdit 7.4.5 + offline-executor.jar） |
| Java | Temurin OpenJDK 25.0.4.1+1 |
| 施工模式 | `NEW_WORLD_FACTORY`（新建独立世界；批写 → 完整回读 → 保存 → 关闭 → 锁释放核验） |

### Skill 来源与 hash

| 项 | 值 |
|----|----|
| 来源 | `zhangchenjia21-dot/Vibe-Coding`，`skill/codex/minecraft-builder/SKILL.md` |
| 读取方式 | 经本地代理 + TLS 隧道下载 `raw.githubusercontent.com`（HTTP 200，52396 字节） |
| 本地副本 | `_skill_SKILL_v1.10.md` |
| **SHA256** | `1C719DB419F51410BA894D9731AB2026E68B4BBCB73B9C092863DFB5EDD85F9E` |
| 版本确认 | 首行 `# minecraft-builder v1.10`；共 **1188 行** |
| 说明 | 会话内置 skill 为 v1.0（6242 字节），**未**用于本任务；全程按 v1.10 原文执行 |

---

## 2. 世界身份（测试隔离证据）

| 项 | 值 |
|----|----|
| 世界路径 | `D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V110-M01-DS-汉萨市政厅` |
| 创建方式 | 离线执行器 `create: {type:"superflat", seed:20260912}`；执行器固定写入 `generate-structures=false` |
| 生成器回读 | `FlatLevelSource` |
| 出生点 | (10, 1, −14) —— 市场广场前，正对建筑主入口 |
| 创建/重建作业 | 见 `evidence/world-identity.json` |
| 隔离声明 | 未进入、未读取、未修改 `建筑师` 正式存档、T01—T12 世界、其它模型本轮 M01 世界 |

---

## 3. Layer A｜研究与设计

- **研究记录**: `research/01_研究记录.md` —— 6 项真实来源：
  Lueger《Lexikon der gesamten Technik》Rathaus 条目；de.wikipedia《Rathaus Stralsund》《Rathaus (Lübeck)》；
  Götzinger《Reallexicon der Deutschen Altertümer》Kaufhaus 条目；Europäische Route der Backsteingotik
  Jüterbog 条目；History Hit Lübeck Town Hall。
  提取的关键类型学事实：**底层交易大厅 / 上层议事大厅的功能分层**、**市场侧拱廊属制度空间（摊位、市秤、
  司法）**、**Rathaus 与 Kaufhaus 合体**、**Kaufkammer 租用制与 Kaufhaus-Meister 职官体系**、
  **不同色砖砌展示墙**。
- **Architectural Intent**: `design/02_Architectural_Intent.md`（Purpose / Users / Site / Context / Program /
  Space Graph / Hierarchy+Sequence / Plan+Section / Structure+Material / Form+Minecraft Translation）。
- **原创性**：未复制任何单一真实建筑的平面或立面；**未使用任何 REF / Litematic / Blueprint 作为主体建筑**，
  全部 30 253 个方块由本项目生成器逐格生成。

---

## 4. Builder Core｜施工阶段

| 阶段 | 内容 | 方块 |
|------|------|------|
| S1-场地与台基 | 广场所地、主通道、排水沟与集水坑、巷道、台基勒脚、北院与水井 | 11 648 |
| S2-地窖 | 地窖地面、墙壳、砖墩、三道筒拱、隔墙、地窖梯 | 3 187 |
| S3-交易层 | 拱廊柱列与筒拱、南/北/端墙、中列柱、交易厅两道筒拱、后勤翼 | 4 576 |
| S4-楼板与披檐 | 木楼板（梁 + 搁栅）、拱廊披檐、上层地坪、柱头托臂 | 3 347 |
| S5-上层大厅 | 上层外墙、南向 3 樘大窗、后墙 2 樘、山墙窗、**阶梯山墙**、辅助房间 | 4 994 |
| S6-屋面 | 两坡屋面（约 54°）、屋脊压顶、檐口滴水、屋面通风缝 | 8 236 |
| S7-屋脊钟塔 | 钟塔（百叶通风层）、塔尖、阁楼木梯 | 178 |
| S8-开口与主楼梯 | 拱廊→交易厅门洞、北穿通、后勤门、地窖口、**主楼梯**、入口门廊 | 1 376 |

**Core 合计 29 192 方块**（SPATIAL_COMPLETE 基线，`evidence/baseline/`）。

---

## 5. Finishing｜五个 Pass（v1.10 §17）

| Pass | 内容 | 方块 |
|------|------|------|
| F1-功能精修 | Kaufkammern 摊位（台面+货桶+招牌）、**市秤**（秤座/秤链/秤盘/灯/标识）、账房（账桌/账册台/烛台/账册箱）、过秤间台秤、看守室、后勤储物成组、地窖酒桶/盐箱/粮桶、大厅长桌长凳、议事厅/市长室/金库（铁门）/法院厅、楼梯与井口扶手 | 235 |
| F2-建筑收口 | 墙脚收边（**跳过门洞**）、上层墙脚、拱廊柱脚与柱头线脚、檐口线脚、山墙压顶、檐沟、3 处落水管与散水、隅石、门廊隅石 | 559 |
| F3-材质与环境 | 受潮带（北面强/南面弱，**按朝向**）、檐下滴水痕、人流踩踏磨损（门槛/楼梯口/通道中线）、烟熏、维修补砌、沟边苔藓、台基边草、边缘碎石、井边湿地与蕨 | 154 |
| F4-构图与氛围 | 拱廊吊灯（每开间 1 盏，光随柱列节奏）、交易厅吊灯（光随墩列）、大厅灯（**东端 Focal 密、西端 Quiet 疏**）、前厅灯、门廊壁灯与吊灯、后勤灯、地窖灯、**市徽浮雕**、山墙绿釉砖饰带 | 170 |
| F5-Restraint | 删除后半段重复摊位 6 组、过量灯具 5 盏、入口前杂草（保持入口礼仪性净空） | 11 |

**最终 30 253 方块 / 62 种状态。**

---

## 6. Gates｜各门结果

### 6.1 Design / Massing / Section / Tectonic Gate — **PASS**

剖面证据（`evidence/preview/section-z22.txt`、`section-x08.txt`、`section-x12.txt`、`plan-y1.txt`、`plan-y7.txt`）：
- **剖面成立**：交易层起拱 y=4、拱腹 y=5（净高 4 格）；楼板 y=5–6；大厅地坪 y=7；檐口 y=17；屋脊 y=30；山墙顶 y=36。
- **结构驱动外形**：一层砖墩 + 纵向筒拱的柱网节奏（墩距 6 格）直接决定了拱廊开间与交易厅跨度；
  上层为**无柱木屋架大厅**（跨度 19 格），屋脊沿东西向贯通，两端形成阶梯山墙。
- **主次体量**：主体 + 北侧后勤翼 + 入口门廊 + 屋脊钟塔，非"方盒贴皮"。
- 忽略材质与小构件后轮廓仍可读。

### 6.2 Construction Closure & Clearance Gate — **PASS**（含 1 处检查器口径边界）

**A. Ground Contact / Support Closure** — 全卷扫描 1200 处"无支承"标记，逐类核对后**全部为有意构造**
（屋面出檐、拱廊披檐、楼板梁端与搁栅、托臂、井口护栏、楼梯扶手、拱券石），无一是生成遗漏。**PASS**。

**B. Movement Envelope Clearance** — 10 条关键路线逐格 1×2 碰撞体净空检查：
9 条完全通过；1 条（主楼梯最后一级）报告 `STEP_TOO_HIGH`，逐格实测标高为
`1,1,2,3,4,5,6,6(半砖顶 6.5),7`，实际为连续 0.5 格与 1 格踏步，**玩家可正常上行**；
该条源于检查器对半砖平台的最低落脚面判定，属**判定口径边界**而非几何缺陷（详见 §9.3）。
核验中发现并已 Repair 的真实缺陷见 §8。

**C. Edge Closure Walk / Scan** — 墙脚、门槛、建筑与铺地交界、楼梯上下口在剖面与体量核验中逐点检查；
台基（勒脚 + 顶面）沿建筑外缘连续闭合；无封闭空洞、无悬空几何体（子代理像素级取证交叉确认）。

### 6.3 Spatial Completion Gate — **PASS**

Upstream Defect Test（若完全不加家具/props/做旧，是否已是完整、合理、可使用的空间）：**是**。
- 拱廊净空全连通；上层大厅 3183 格**全连通**（孤立口袋 0）；交易厅北跨 323 格全连通。
- 三套流线（公众 / 货流 / 议会）均有实际对应的门洞、楼梯与通道。
- 状态设为 `SPATIAL_COMPLETE`，并保存了**可比较的 pre-Finishing 基线**：
  `evidence/baseline/baseline-world.json`、`core-baseline-report.json`、`frozen-core-baseline.json`，
  以及同机位基线视图 `evidence/views/baseline-*.png`。

### 6.4 Finishing Completion Gate — **PASS**

- **Coverage**：Focal（主入口门廊、市徽、市秤、主楼梯、大厅东端）/ Supporting（交易厅摊位、账房、过秤间、
  法院厅）/ Quiet（东西端与后勤房间）均已按角色处理；Quiet 区通过墙脚、铺地、光暗与维护状态保持完整，
  不是未处理的毛坯。
- **Perceptual Delta**：`evidence/views/` 提供 **baseline 与 final 同机位 12 视图**（相机参数逐字段相同，
  见两份 `manifest.json`），可直接比对 Core → 成品的变化。
- **Restraint Balance**：Restraint 删除 11 处冗余（重复摊位、过量灯具、入口前杂草），未误删支持空间身份的
  必要信息。
- **Evidence Standard**：未以"修改方块数""Pass 已执行"代替判断；以同机位视图 + 逐格结构核验为准。

### 6.5 最终状态

按 v1.10 §26：`FINISHED`（已完成与 Scope 重要性匹配的玩家尺度精修：用途、建筑收口、材质时间层、光、
Micro 与 Restraint；已通过 Finishing Completion Gate；Finishing 后 Construction Closure & Clearance Gate
不处于失败状态）。

**未标记 `VERIFIED`**：因为真实客户端感知验证与真实碰撞模拟在本工具链下不可用（见 §9）。

---

## 7. Verification｜验证方法与结果

### 7.1 全卷双向逐格比对（最强证据）

对 x −24..46、y −6..50、z −22..56 做三块 RLE 扫描并解码为体素卷：

| 项 | 结果 |
|----|------|
| 正向（蓝本 → 世界） | 30 253 格，**不一致 0** |
| 反向（世界非空气 → 蓝本是否声明） | 26 245 格，**全部为超平坦默认地层**（dirt 25 732 + grass_block 513） |
| 结论 | 世界与蓝本逐格一致；**无旧几何残留、无未声明的多余结构** |

### 7.2 调色板合法性

1555 个候选状态经真实世界放置 + 回读验证（`evidence/palette-G0-*.json`）：
- 1420 条被 Minecraft 规范化，**0 条发生方块种类替换**（全部只是 `waterlogged` / `powered` 补全与属性排序）；
- 69 个涉及未验收方块实体的状态被执行器策略拒绝并剔除（均为非必要装饰件）；
- 施工实际使用的 **62 种状态全部合法**。

### 7.3 Phase Protection

`evidence/baseline/frozen-core-baseline.json` 记录了 Frozen Core 的关键点（Space Graph 边、屋脊、檐口、
主入口门槛）；Finishing 后逐点复核，**未修改任何 Frozen 语义**。Finishing 的全部写入均通过
`override` 记录理由（共 2188 条），可按理由分类审计（见 `evidence/preview/blueprint-report.json`）。

---

## 8. 本轮真实暴露的问题与 Repair 记录（共 14 项）

| # | 问题 | 发现方式 | 处理 |
|---|------|----------|------|
| 1 | `plate()` 参数顺序误用，楼层被铺满 | 剖面 ASCII 自检 | 修正并加注释 |
| 2 | **旧几何残留**（改几何后旧方块未清除） | 全卷**反向**比对 | 新增 `rebuild`（备份→删除→全新重建）+ 固化双向比对 |
| 3 | 拱顶填充算法把拱腹以下填实，交易厅净高仅剩 1 格 | Movement Envelope | 重写筒拱填充模型，净高恢复 4 格 |
| 4 | 楼板主梁横跨楼梯井，切断梯段净空 | Movement Envelope | 断开井道上方主梁 + 加梁端托臂 |
| 5 | 入口门套伸至室外台阶，形成 4 格高挡墙 | Movement Envelope | `portalX` 增加 `frameSide`，外墙入口只做内侧门套 |
| 6 | 拱廊披檐与楼板重叠 | 冲突检测 | 楼板限定主体范围，披檐只覆盖拱廊 |
| 7 | 地窖井口挖掉了梯段本身 | 手动探测 | 井口范围移到梯段顶端 |
| 8 | 门廊前墙覆盖了门前台阶 | 手动探测 | 前墙与台阶重新对位 |
| 9 | Finishing 墙脚带封堵门洞 | 冲突/覆盖审计 | `solidAt()` 判定，只处理砖墙面 |
| 10 | `M.stoneLight` 键不存在导致状态为 undefined（执行器报 `JsonNull`） | 执行器失败 + 新增 `INVALID_STATE` 断言 | 改为 `M.light`；断言保留为常设检查 |
| 11 | 摊位与主楼梯、市秤与通行带位置冲突 | Movement Envelope | 摊位 z 起点后移、市秤移至拱廊西端开间 |
| 12 | 广场草丛侵入拱廊通行带；排水沟与拱廊重叠 | Movement Envelope | 植被与排水沟移至广场侧 |
| 13 | 地窖口盖板阻断下行净空 | Movement Envelope | 井口敞开 |
| 14 | 山墙压顶写入 undefined | 报告审计 | 增加存在性判断 |

---

## 9. 已知限制与未验证边界（诚实报告）

1. **真实客户端感知未验证。** 本 Harness 无客户端控制/截图工具。视图证据为软件体素渲染，
   **不含真实材质贴图、光照模型、方块模型细节（玻璃不透明；楼梯、栅栏、墙、铁栏杆按整块立方体光栅化——
   本轮已把楼梯改进为按 facing 的近似半高台阶）、FOV 与移动尺度体验**，不能替代实机检查。

2. **内景视图可读性受限。** 子代理对 12 张 PNG 做了像素级反解取证（100.0% 几何像素可在 2.5 RGB 内反解回
   渲染器模型），结论：**无封闭空洞、无悬空几何体**；但内景视图（6/7/8）因缺乏方块模型与光照而信息密度低，
   不能单独支撑"重要二层空间 / 垂直交通"的感知判断。已用精确剖面/平面文本证据互补
   （`evidence/结构闭合与附着性核验.md`）。

3. **主楼梯最后一级的检查器口径边界。** 见 §6.2 B。逐格标高实测连续，但检查器报告 1 处 `STEP_TOO_HIGH`；
   未做真实 walk-through 消除该歧义。

4. **碰撞验证为体素近似。** 使用 1×2 保守碰撞包络 + 1 格台阶假设，未模拟 Minecraft 真实 step-height
   （0.6 格）与半砖/楼梯的精细碰撞盒。

5. **悬空扫描为启发式分类。** 1200 处标记经人工分类判定为有意构造，但不是结构受力分析。

6. **地窖与阁楼未做完整可达性闭环验证。** 地窖三道筒拱空间连通（36 格空气 / 最大连通 9 格），
   但未见完整照明与第二疏散路径；阁楼仅经木梯到达，未验证净空。

7. **未做流体稳定性验证。** 场地仅一处 4 格水源水井，不构成水道系统；无 Water Module 验证对象。

8. **钟塔附着性**：屏幕空间呈"孤岛"是相机高度（eye y=30 ≈ 屋脊）造成的剪影效应；
   几何证据（塔底 y=31 与屋脊 y=30 竖向相邻）与双向逐格比对共同排除悬空，详见
   `evidence/结构闭合与附着性核验.md` §3。

9. **未注册任何新资产，未进入 `建筑师` 正式存档，未修改 minecraft-builder Skill。**

---

## 10. 视图证据（同机位 baseline ↔ final）

`evidence/views/` 含 12 机位 × 2 状态 = 24 张 PNG，相机参数逐字段相同（两份 `manifest.json` 可核对）：

| 视图 | 对应要求 |
|------|----------|
| `*-1-城市接近_正面.png` | 城市接近 / 正面 |
| `*-2-整体体量_斜俯视.png` | 整体体量 |
| `*-3-市场侧拱廊.png`、`*-5-拱廊内看交易厅.png` | 主要公共空间 |
| `*-7-上层大厅内景.png` | 重要二层空间 |
| `*-8-主楼梯与井道.png` | 垂直交通 |
| `*-9-北侧后勤院.png`、`*-11-背街与后勤立面.png` | 后勤 / 次要空间 |
| `*-4-入口门廊与大楼梯.png`、`*-10-山墙与钟塔细部.png` | 近景建筑细部 |
| `*-6-交易厅内景（南跨）.png`、`*-12-俯视平面.png` | 补充 |

配套精确文本证据：`evidence/preview/section-z22.txt`、`section-x08.txt`、`section-x12.txt`、
`plan-y1.txt`、`plan-y7.txt`、`blueprint-report.json`。

---

## 11. 可复核材料清单

```
MB-V110-M01-DS/
├── _skill_SKILL_v1.10.md             实际使用的 Skill 原文（SHA256 见 §1）
├── research/
│   ├── 01_研究记录.md                 6 项真实历史/类型学来源与提取结论
│   ├── blocks_schema.json             从 26.2 客户端 jar 提取的 1198 个方块状态 schema
│   └── palette.json                   1555 个候选状态的合法性验证结果
├── design/02_Architectural_Intent.md
├── tools/
│   ├── 提取方块schema.mjs              从 jar 提取权威状态定义
│   ├── 验证调色板.mjs / 解码调色板.mjs   真实世界放置 + 回读验证
│   ├── 几何核心.mjs                    方块写入、冲突检测、分层绘制、**状态合法性断言**、出图
│   ├── 设计参数.mjs                    控制线、材料语言、拱券几何
│   ├── 建筑生成器.mjs                  S1–S8 全部施工代码（主要可复核材料）
│   ├── 精修.mjs                        F1–F5 五个 Finishing Pass 全部代码
│   ├── 蓝本.mjs                        Core / Finishing 阶段装配
│   ├── 构建.mjs                        CLI：report / create / build / rebuild / rebuild-core
│   ├── 基线.mjs                        SPATIAL_COMPLETE 基线与 Frozen Core 记录
│   ├── 结构自检.mjs                    悬空检测、Movement Envelope、空间连通体积
│   ├── 核验世界.mjs                    全卷双向比对 + 结构自检
│   ├── 体素渲染.mjs                    扫描/蓝图 → PNG
│   └── 视图证据.mjs                    12 机位同机位视图生成
├── evidence/
│   ├── world-identity.json             世界身份与创建/重建作业
│   ├── palette-G0-*.json               调色板验证原始证据
│   ├── verify-report.json              双向比对、悬空、路径、空间成立性
│   ├── 结构闭合与附着性核验.md          不依赖图像的结构断言
│   ├── baseline/                       SPATIAL_COMPLETE 基线（Core 报告、Frozen Core、基线世界）
│   ├── preview/                        蓝本报告、ASCII 剖面与平面
│   ├── views/                          24 张同机位视图（baseline / final）+ 两份 manifest
│   └── Completion_Report.md            本文件
└── snapshots/                          各次 pre-rebuild 存档快照（SHA256 校验通过）
```

复现：
```bash
node tools/构建.mjs report                  # 生成蓝本并自检（不写世界）
node tools/构建.mjs rebuild-core            # 重建为 SPATIAL_COMPLETE（Finishing 前）
node tools/构建.mjs rebuild                 # 重建为 FINISHED
node tools/核验世界.mjs                      # 全卷双向比对 + 结构自检
node tools/视图证据.mjs final "FINISHED"     # 生成同机位视图
```

---

## 12. 运行指标

| 项 | 值 |
|----|----|
| Builder Core 阶段 | 8 个（S1–S8） |
| Finishing Pass | 5 个（F1 功能 / F2 建筑收口 / F3 材质环境 / F4 构图氛围 / F5 Restraint） |
| 离线作业总数 | 约 75 次（含调色板验证、迭代重建、核验扫描、视图扫描） |
| 单次作业墙钟时间 | 16–20 s（加载 + 批写 + 回读 + 保存 + 关闭） |
| 最终方块数 | **30 253**（世界实测值，已双向核对） |
| 最终状态种类 | 62 |
| 生成器蓝本操作 | 5 021 条合并操作 |
| Agent turns / tool calls / token / cost | Harness 未提供该统计，无法记录 |

为质量付出的主要成本是**迭代重建**（每次几何修正都做"备份 → 删除 → 全新重建"，以避免旧几何残留，
共 14 轮 Repair）。未为了降低指标而牺牲质量。

---

## 13. 测试纪律声明

- 未读取 T01—T12 Independent Review、Owner 历次反馈、regression reports、过去测试的 Completion Report、
  REF-0123 资料、其它模型本轮 M01 的工作目录/报告/世界。
- 未自行判断本轮 Skill 是否 PASS、未评价自身相对其它模型的优劣、未推断基准排名。
- 未修改 minecraft-builder Skill；未正式注册新资产；未进入 `建筑师` 正式存档。
- 本报告只陈述真实施工状态、发现的问题与已知限制。
