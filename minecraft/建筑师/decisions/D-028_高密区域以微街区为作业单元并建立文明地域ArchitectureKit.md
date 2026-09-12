# D-028｜高密区域以微街区为作业单元，并建立文明 / 地域 Architecture Kit

日期：2026-09-12
状态：**OWNER DIRECTION / ACTIVE**

## 背景

MD-001P-R1 已确认 Middle 是 CIV-001 中 territory-wide 平均建成强度和土地利用强度最高的一域，G1 是高频门户社区。

MD-001S1 进一步完成了当前真实存档的单建筑级局部 Site Gate，得到 S1 / S2 / S3 三个约 570–605 格的候选包络。

Owner 随后明确指出：

1. 对 G1 / N1 这类建筑密集区域，**单建筑逐栋设计与施工并不是最合适的作业单元**；应优先对一个小片区的多个建筑、街巷、院落和公共 / 后勤空间进行整体设计。
2. 同一文明 / 地域后续建筑应复用已经形成的建筑特点、构造规则和模板，以保持风格一致并降低重复设计成本。

## 决策 1｜作业单元随聚落密度变化

不再把“单栋建筑”设为所有场景的默认 Design / Build unit。

### 低密 / 独立场景

可继续以单栋建筑为主要作业单元，例如：

- 独立农庄；
- 山地孤立工坊；
- 神殿 / 塔 / 桥头设施；
- 单独庄园或特殊公共建筑。

### 中密场景

优先以 compound / courtyard cluster 为作业单元：

- 主体建筑 + 附属房；
- 共享院；
- 服务入口；
- 小段道路 / 围合界面。

### 高密场景

G1、N1 等紧凑街区，默认以：

> **Micro-District / Urban Ensemble / 微街区建筑组团**

作为 Architecture Design unit。

一个微街区应同时考虑：

- 多个独立建筑体量；
- 主次建筑关系；
- 街巷与转角；
- 共享院 / 半公共空间；
- 装卸与后勤；
- 居民日常出入口；
- 地形高差与排水；
- 建筑之间的视线、屋顶、山墙与天际线关系；
- 后续街区继续生长的接口。

**高密 ≠ 一次把整个 G1 全部建满。** 每次只选择一个可审核的微街区作为 major target。

## 决策 2｜整体设计，分批 world-write

“建筑组团一起作业”指：

> **一个片区一次性完成整体设计与空间协调。**

不意味着一次性无边界写入世界。

实际施工仍遵循 bounded world-write：

```text
整片 Urban Ensemble 统一设计
→ terrain / circulation preparation
→ anchor building(s)
→ secondary buildings
→ shared courtyard / lanes / service interfaces
→ landscape / details
→ final district review
```

每个写入批次必须可验证、可停止、可回退。

因此：

> **Design unit 可以是微街区；Write batch 仍然可以很小。**

这不违反“小批次 ≠ 小建筑 / 小项目”的既有原则。

## 决策 3｜建立 Architecture Kit，而不是复制同一栋房子

风格一致性的复用单位不应仅按“生物种族”划分。

CIV-001 的 West / Middle / East 都是人类，但存在有意的地域建筑差异，因此正式组织层级为：

```text
CIV-001 Shared Architectural DNA
        ↓
Regional Kit: WEST / MIDDLE / EAST
        ↓
Settlement / Site-specific adaptation
```

### Architecture Kit 至少包含

#### A. Shared CIV DNA

- 基础建造技术；
- 共同材料逻辑；
- 构造亲缘关系；
- 尺度与比例习惯；
- 共通细部语言；
- 明确禁止的现代 / 异文明组合。

#### B. Regional Kit

以 Middle 为例，应保存：

- stone base / timber upper 等构造体系；
- 墙体与结构 bay 习惯；
- 层高范围与层间关系；
- 屋顶类型 / 坡度 / 山墙语言；
- 门窗比例与 opening hierarchy；
- 店屋、短仓、工坊住宅、旅宿、院墙 / 门洞等 typology skeleton；
- street-edge / setback / corner rules；
- shared courtyard / service yard 规则；
- 装卸门、仓门、楼梯、拱廊、雨棚、阳台等可复用模块；
- palette family，而不是每栋重新从零挑方块；
- 结构 / facade / roof / detail 的 variation knobs；
- forbidden combinations。

### Template 的含义

模板必须是：

> **可参数化、可变形、可按场地适配的 typology / module。**

不得变成：

> **整栋建筑原样复制粘贴。**

相同街区中的建筑应“像同一个地方的人建的”，但不能像复制出来的五栋同款住宅。

## 决策 4｜Architecture Kit 的版本化积累

Kit 采用版本化演进：

```text
AB-001 Architecture Grammar
→ Regional Architecture Kit v0.x
→ 首个真实设计 / 建造成果
→ GPT + Owner review
→ 把成功模式回写 Kit v1.x
→ 后续同文明 / 同地域直接复用
```

每次被接受的建筑或街区都可以新增：

- proven modules；
- proven proportions；
- proven palette combinations；
- terrain adaptation patterns；
- failed patterns / do-not-repeat lessons。

这样后续建设速度应逐步提高，而不是每次从白纸开始。

## 对 MD-001S1 的处理

MD-001S1 当前读取得到的 S1 / S2 / S3：

- 继续保留为 current-world 地形、浅层地下、通行、排水和现状 evidence；
- **不自动提升为单栋建筑 Site**；
- S1 的 570 格推荐包络不再约束下一阶段必须只设计一栋建筑；
- 后续可把 S1 作为 G1 微街区中的地形锚点 / anchor pocket 使用。

## G1 下一阶段

下一阶段不创建“G1 首栋 Architecture Design”。

改为：

> **MD-001U1｜G1 Gateway Micro-District + Middle Architecture Kit v0.1**

目标是：

1. 在 G1 中基于当前世界 evidence 选择一个可审核微街区；
2. 多栋建筑 + 街巷 + 共享空间统一设计；
3. 建立可供 Middle 后续重复使用的 Architecture Kit v0.1；
4. 仍然 `world writes = 0`，先完成设计与预览；
5. Owner / GPT 接受后，再按 bounded phases 施工。

## 约束

- revision 154 不变；
- MD-001P-R1 总规不变；
- political threshold / through-clearance 不得占用；
- 不把 Alliance Commons 纳入中域街区；
- 不为模板统一而牺牲 terrain fit；
- 不为了“组团”一次性填满整个 G1；
- 未经后续授权，`world writes = 0`。
