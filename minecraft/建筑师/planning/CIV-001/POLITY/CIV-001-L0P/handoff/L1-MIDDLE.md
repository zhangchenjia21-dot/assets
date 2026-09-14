# CIV-001-L0P-L1-MIDDLE

父版 CIV-001-L0P-r1；L0 POLITY_TERRITORY → L1 REGIONAL_SYSTEM；recipient=minecraft-planner v0.5。HANDOFF_READY / AWAITING PARENT REVIEW。

WHY：把跨水、共同地访问和山前交换的不同负荷组织为紧凑混合服务，同时保有居民日常生活

搜索：全部391,002正式成员，包括Commons东侧connector和向谷地/坡麓延伸的领土；比较不同关系的叠合或分工，不能先锁定某中心

## UPSTREAM_FIXED

- OWNER_CONSTRAINT：revision154与Commons边界不变；world_write_authorization=false
- APPROVED_CANON：三席联盟与地方自治、区域broad role、共同政治地非第四域
- OWNER_CONSTRAINT：D-025 territory-wide Middle > West > East；West生产开敞；East全域分散与最强局部地形适应

## DOWNSTREAM_TO_RESOLVE

- 合并式中心与分工式转换网络何者在权利/地形/节奏下更可信？
- 共同政治访问与货流如何保持兼容，是否需要不同接近关系？
- 实际陆侧/岸侧/跨界有效通达、饮水、居民生活与材料外部性怎样约束容量？
- 如何用非重叠建成假说检验全域密度最高而不推平地形？
- 局部定址前刷新必要当前人工物/水/表层/危险与通行证据，不broad rescan
- 独立选择角色/容量，不承袭旧下游节点

## DOWNSTREAM_ADAPTABLE

- 中心位置、数量、角色合并/分工及地方服务层级
- 等价谷地/坡麓接近选项
- 局部适应及有界外供方式
- 库存/等待的共享或分散与局部容量分配

## cross_package_dependencies

- L1-WEST:R-WM与生活品/成品交换
- COMMONS:R-CM公共访问与土地界面
- L1-EAST:R-ME生产/消费与分段运送

## revision_triggers

- 普通时代、有界局部适应及等价选址仍无法支持某父级关系
- 通行/水/资源/容量证据使角色量级无法成立，或两个固定关系不可兼容
- 地形/人工物的新鲜证据与可见世界兼容性冲突
- Canon/Owner边界方向改变；不能因方便私改

## expected_L1_outputs

- 区域网络与搜索比较，保留真实未决问题
- 有效通达/权利/供给/有界适应证据与不确定性
- 量级收敛与D-025非重叠密度检查
- 跨包接口关系和resilience协调记录
- 向L2递归的Planning Packages，仍非Builder设计

## 容量/输入/边界

工作容量 CAP-M, CAP-L, CAP-X 见 ../capacity-scale.json；search ≠ built fabric ≠ catchment。范围低置信度，组合角色不重复计量。

Actor：A-M/A-U/A-W/A-E/A-C；具体地役/水岸权与分担未决。

适应：水/排水、稳路、局部台地、分段转运；低平约20.2%不是可建上限或下限。

节奏与缓冲：日常居民需求与批次接驳峰值分开，断运缓冲不能全放公共政治地。

父案提出的 R-WM, R-CM, R-ME 为待审关系，**未放进已接受UPSTREAM_FIXED**；父案被接受后才约束子案。实体线路和节点数量不锁定。六维通达与失败依赖须读 ../movement-access-skeleton.json、../RESILIENCE-DEPENDENCIES.md。

地形快照/版本/SHA见 ../evidence/source-register.json；当前实存未证，历史成熟≠已建。地方知识与资源发现不可由全图倒推。新证据如有冲突，先尝试有界适应，按JSON中的最小父对象协议回报；不得自行推翻整个L0。

world_write_authorization=false。不执行此包，等待GPT + Owner审核。
