# CIV-001-MID-A-L2P｜Authority Matrix

状态：**ACTIVE INPUT BASELINE**

核心原则：**规划一整座 MID-A 城市；门户是其内部高繁华片区，不是另一座城。**

## A. OWNER_CONSTRAINT / APPROVED PARENT｜必须继承

- `D-032_MiddleL1接受并确认MID-A为联盟最高密度城市进入L2.md`
- `CIV-001-MID-L1P-r1` 已接受的“两主要中心 + 两地方聚落”区域结构
- MID-A = 中域西侧低地综合主中心
- MID-A = 全联盟建筑密度最高、土地面积利用率最高的城市区域
- gateway / connector 属于 MID-A 城市体系，且因接近 Alliance Commons 而特别繁华
- revision154、Alliance Commons 与 X=89 政治边界不变
- Commons 不是 MID-A 可占用土地；MID-A 只能规划自己一侧的城市与跨界接口关系
- MID-A 不是联盟政治主权中心；政治访问可形成服务需求，但不能推导无限收费 / 检查 / 强制贸易权
- D-025：Middle territory-wide 平均密度最高；MID-A 是这一方向在 settlement 尺度的最高强度表达
- `world writes = 0`

## B. OBSERVED / DERIVED EVIDENCE｜可解释，不得篡改

优先读取：

- accepted L0 / L1 Primary artifacts
- revision154 exact geometry
- accepted Natural / Human Geography evidence
- `CIV-001-MID-L1P/REGIONAL-TERRAIN-SYSTEM.*`
- `CIV-001-MID-L1P/MOVEMENT-ACCESS-NETWORK.*`
- `CIV-001-MID-L1P/evidence/*`

L2 进入实际 settlement 定址，必须进行 **Just-in-time current-world read-only freshness check**：

1. 先用已接受区域证据缩小候选城市核心 / 城市边缘搜索；
2. 再读取实际影响 MID-A 规划的当前表层、植被、人工物、水、浅层地下和通行障碍；
3. 不 broad rescan 整个世界；
4. 记录读取范围、时间与 freshness；
5. 不把旧快照冒充当前状态。

## C. LEGACY / REFERENCE_ONLY｜Primary Freeze 前禁止读取

- 旧 `MD-001P/` 与 P1–P5
- N1 / G1 / N2 / N3 / N4 的旧节点与几何
- 旧 R1–R7 / interfaces
- `MD-001S1` 的 Site 推荐结论
- `MD-001U1` 微街区设计
- Middle Kit v0.1
- 旧 building program / first-build recommendation

Primary MID-A L2 Freeze 后才允许读取这些内容做 A/B comparison。

其中 `MD-001S1` / `MD-001U1` 内的**时间绑定观测事实**可在 Freeze 后作为历史 evidence 复核，但不得连带继承 G1/S1/U1 设计结论。

## D. L2 MUST REDERIVE

- MID-A 精确 settlement extent / urban edge
- 城市核心位置与门户片区关系
- 主要 Anchor hierarchy
- 城市内部历史 Growth Sequence
- primary movement / public-space skeleton
- district formation logic
- density gradient：门户、市场核心、居民混合区、仓储/加工等如何因果分化
- commons / negative space / service-space 逻辑
- water / waste / fire / loading / maintenance 等 settlement-scale requirements
- building demand / program at planning scale
- Architecture Kit Requirements（仅需求，不写具体 Builder 模块）
- L3 recursive planning packages

## E. Scale Firewall

L2 可以决定城市整体结构、主要 movement、district formation、Broad building demand 与密度关系。

L2 不得设计：

- 精确街道方块线
- parcel 精确切分
- 单栋建筑 footprint / Plan / Section / roof / facade
- Architecture Kit 的精确构件 / 方块材料
- Builder blueprint
- world-write
