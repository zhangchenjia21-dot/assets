# D-018｜Council Centerland 联盟公地与中域交割

状态：**OWNER APPROVED / ACTIVE DECISION / EXACT BOUNDARY ACCEPTED BY D-020**

日期：2026-09-10

## 1. Owner 土地规则

Candidate A 是东部山地主岛向西伸入 C 形海湾的低地陆体，原 A 实际干陆：**105,785 blocks²**。

Owner 明确：

> **Candidate A 除了最东侧与右侧主岛连接的陆颈 / 连接带之外，其余主体陆地全部属于联盟公用土地。**

不得：

- 在 A 内部再套一个更小的椭圆公地；
- 为达到某个面积百分比反向裁地；
- 为追求数学椭圆裁掉主体自然海岸。

去掉东侧连接带后，剩余主体本身在玩家视觉上就是近似椭圆 / 卵形“中心岛”。

## 2. AB-001P1R 精确边界

P1R implementation：

`723f9217c75b2e53a83d895904dfafb58e7a6c8a`

Independent Review：

`../research/build-sites/CIV-001/AB-001P1R/独立审核.md`

Acceptance：

`D-020_AB-001P1R联盟公地精确边界接受.md`

当前接受的规划切口：

```text
Alliance Commons = A ∩ (X <= 88)
Middle-Domain connector = A ∩ (X >= 89)
```

政治边界平面：`X=89`。

实际共享陆地接口：`Z=1726..1774`，48 条单位边。

## 3. 精确面积

- Alliance Commons：**92,124 blocks²**；
- East connector：**13,661 blocks²**；
- Candidate A：**105,785 blocks²**。

验证：

```text
Commons ∪ connector = A
Commons ∩ connector = empty
Commons connected components = 1
connector connected components = 1
```

因此 Alliance Commons 约占 A 的绝大多数，符合 Owner“连接带之外整个主体都是公地”的原意。

## 4. 政治空间关系

```text
西域（湾对岸 C 形低岛）
        ↕ 水面联系
联盟公地｜Alliance Commons
= 92,124 格 A 主体
≈ 玩家视觉上的椭圆 / 卵形中心陆体
        ↔ X=89 政治接口
中域｜13,661 格东侧连接带 + 东岛西部低地 / 坡麓
        →
东域｜东部山地核心
```

西域不在 Commons 之外另建立 A 内主权飞地；三域通过联盟制度共同拥有 Commons。

## 5. 边界性质

X=89 是 Minecraft 栅格上的政治 / 地籍规划约定，不代表：

- 自然界存在一条无限精确的断界；
- 必须筑墙；
- 必须挖沟或开水道；
- 必须把边界做成明显人工直线。

未来进入可见建筑 / 景观设计时，可通过道路、界石、低墙、树列、院落边缘或其它前现代方式 Just-in-time 表达，也可以在部分地段保持边界不可见。

## 6. Program / Capacity

旧的 22k–32k / 55k–65k Commons 等面积假设全部失效。

当前唯一有效总面积：

> **Alliance Commons = 92,124 blocks²**

最新容量规划入口：

`../architecture/civilizations/CIV-001/Council-Centerland-Program-Capacity.md`

建筑密度、大厅尺度和其它功能均必须从该真实面积重新推导。

## 7. 小批次施工

即使 Commons 总面积达到 92,124 格，仍继续：

> **一个 world-write Task = 一个主要建筑 / 一个主要空间目标 + 必需最小接口。**

总体政治中心可以预先做容量与关系规划，但不得一次性交给 Codex 全部施工。

`world writes = 0`。
