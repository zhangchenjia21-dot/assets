# Owner 观察核验（刷新后快照解释，待独立审核）

Owner 真人观察完整保留为 Observed-by-Owner。以下把指定 NGEO-009 的机器观测、派生指标与解释分开；没有要求 Owner 必须与这份范围定义一致。

| 假说 | 初步 verdict | 依据与限度 |
|---|---|---|
| H-01 温带 / 枯树环境 | PARTIALLY_SUPPORTED | 稀疏树冠、savanna/arid_highlands、无 jungle 支持非高密雨林印象；温带气候和枯树占优没有充分结构证据。dead_bush 不等于 dead tree。 |
| H-02 多山少平原 | NOT_SUPPORTED | 指定主岛 median Y66，操作性 flat 67.65%，严格阈值仍54.13%；东侧独立陆体较高，可能对应更广视野，但不能混算。 |
| H-03 西低东高 | PARTIALLY_SUPPORTED | 西/东 median Y65/67，r=0.337，约+0.491Y/100X；属温和梯度，局部反例明显。 |
| H-04 西侧两个岛片集中平地 | PARTIALLY_SUPPORTED | 西半更平缓，但东半也有广泛平地；南北两翼是同一岛，中央似岛陆片是接东岸的半岛。Owner 具体两个参照未给坐标，对应仍未知。 |
| H-05 三个潜在部族区域 | NOT_SUPPORTED | 对指定主岛，2～5类数值比较未建立三个稳定离散区域；自然 substrate 支持为 WEAK。不创建“部族区”。 |

这些 verdict 是显式模型解释，不由代码阈值自动晋升。机器可读版本为 `profile/owner-hypothesis-evaluation.json`，其中逐项列出 observation、metric refs 与 interpretation。H-03 地形趋势另按 Task enum 记为 PARTIAL。

一个 SIRZ 研究单元并不宣称没有自然差异：海岸、savanna 基质、南侧稍高的 arid_highlands 和洞口局部起伏均在机器层保留。它表示本轮尚不足以画出2～5个可靠、离散的内部自然区界。

本轮还没有完全调查东侧较大陆体，更不能否定 Owner 对另一尺度区域的整体空间感受。后续是否需要澄清具体视点或另查东侧范围，应由 GPT / Owner 审核后决定。本任务不自行扩大为文明设计。
