# D-029｜MD-001U1 作为 Pre-Settlement-Planner 实验基线冻结

日期：2026-09-13
状态：**GPT REVIEW ACCEPTED / EXPERIMENTAL BASELINE / NO BUILD**

## 决策

MD-001U1（G1 Gateway Micro-District + Middle Architecture Kit v0.1）完成后，经 GPT 独立审核，判定：

> **TECHNICAL PASS_WITH_NOTES / PRE-SETTLEMENT-PLANNER EXPERIMENTAL BASELINE**

本轮成果不进入 world-write，也不作为最终聚落规划或最终建筑群设计。

原因不是其技术质量不足，而是项目现已识别出更上游的 Settlement Planning 层缺失。未来在新的 `minecraft-settlement-planner` Skill 完成并经测试验证后，Middle 的聚落因果规划将重新编译，届时 G1 / N1 / district / building program / growth sequence / movement / parcel 等下游内容可能改变。

## 为什么保留 MD-001U1

MD-001U1 仍具有高价值，作为旧流程的完整终点样本：

- 1,310 格 coherent micro-district envelope；
- 5 栋独立体量；
- 主体 footprint 487 格 / 37.18%；
- 多建筑统一的 plan / section / circulation / shared courtyard / loading / terrain adaptation；
- 完整 3D preview 与机器 QA；
- `Middle Architecture Kit v0.1`。

它适合在新 Skill 完成后做 A/B regression：

> 旧流程（地形 / 总规 → 微街区设计）
> vs.
> 新流程（文明 / 势力 / Anchor / Growth Sequence / Movement / Parcel → 微街区设计）。

如果新 Settlement Planner 不能在因果性、空间生长逻辑和 building demand 上明显优于此 baseline，则 Skill 不应被视为成功。

## 对 Middle Kit v0.1 的处理

`architecture/civilizations/CIV-001/kits/MIDDLE/v0.1/` 保留，但定位为：

> **CANDIDATE SEED / PROVISIONAL DESIGN VOCABULARY**

不删除，不自动升级为正式地方传统，不注册为可直接施工 prefab。

其中：

- Shared DNA；
- construction ranges；
- module vocabulary；
- typology skeleton；
- variation rules；
- forbidden combinations；

可作为未来新规划流程的输入和对照。

新的 Settlement Planner 产出 Middle settlement causal plan 后，应重审：

- 哪些 typology 实际被文明 / 聚落需求支持；
- 哪些 module 仍适合；
- 哪些尺度 / 组合需要调整；
- 是否形成 `Middle Kit v0.2`。

只有真实建成并经 Owner 接受的模式才能进入 `BUILT_AND_OWNER_ACCEPTED`。

## 技术审核摘要

MD-001U1 的机器 QA / Critic 支持：

- design envelope 未越出 G1；
- political threshold / through-clearance / reserve 未被主体或屋檐侵占；
- 5 条楼梯简化检查无失败；
- 18 条主要室内外路线简化检查无失败；
- 共享开放地保持连通；
- 设计包含独立居民与货物流线；
- `world writes = 0`。

但明确未完成：

- Minecraft 真实 blockstate collision；
- pack-animal / vehicle movement envelope；
- in-game walk-through；
- lighting；
- fluid updates / drainage capacity；
- confirmed drinking-water source；
- final tree conflict resolution；
- deep subsurface / build-time freshness checks。

因此不得升级为 Build PASS。

## 关键方法论发现

MD-001U1 已能构造一个合理微街区，但其“先仓铺、后旅舍修理、再服务屋”仍被明确标注为**设计形成模型 / 拟定分期，而不是世界历史事实**。

这正是新 Settlement Planner 必须补齐的能力：

> Growth Sequence 应在 Architecture Design 之前由文明、势力、制度、经济、地形、交通和历史因果推导，而不是建筑群成型后再追加解释。

## 冻结与保留层级

继续保留 / 冻结：

- Natural geography / current-world evidence；
- CIV-001 minimal Canon；
- Alliance Commons；
- Owner territory partition + TT-002R revision 154；
- D-025 三域平均密度与空间性格方向。

等待新 Settlement Planner 重跑 / 重新验证：

- MD-001P-R1 的 P1–P5 规划逻辑；
- N1/N2/N3/N4/G1 settlement hierarchy；
- corridor / land-use / settlement program；
- growth sequence / anchor hierarchy / parcel logic；
- MD-001S1 单体 Site 结论；
- MD-001U1 micro-district envelope 与 5 栋 building program。

这些成果保留为 lineage / regression evidence，不删除。

## 当前路线

```text
冻结 MD-001U1 实验基线
→ 完成并验证 minecraft-settlement-planner Skill
→ 以 Middle 作为第一个正式重编译案例
→ 重新生成 Settlement Causal Plan
→ 与旧 MD-001P / MD-001U1 做 A/B 审核
→ Owner 接受新的 settlement plan
→ 再进入 Architecture Kit 校准 + minecraft-builder 设计
→ bounded world-write
```

在新 Settlement Planner 被接受前：

> **Build world-write = NOT AUTHORIZED。**
