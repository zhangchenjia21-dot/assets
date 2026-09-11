# Deployable Asset Library · V6E

原创树木与敞棚可声明 `metadata.asset_contract`：`kind` 为 `TREE` 或 `OPEN_SHELTER`，显式 `anchor` 为最低实体平面的根部/柱脚，`front` 为作者定义的放置朝向，不冒称检测到门。敞棚额外声明连续 `route`（最低平面两格净空）和至少四个连续支柱顶点 `supports`。L1 校验实体接地和这些标注，L2 随原生方块变换同步变换契约，L3 原创晋升入口使用它；无此契约的房屋保持原验证。资产不包含地表，使用时仍需核对支承地形和净空。

这是 Reference 的独立晋升层。`assets/AST-xxxx/blueprint.json` 是源 normalized Canonical Blueprint 的逐字节副本，不改原件、不重新设计。`source.json` 保留 REF ID、源路径、SHA256、作者、URL 和许可证；unknown 保持 unknown。分类变化不会改变 AST ID，也不会自动更新资产分类快照。

## 入口

在 `D:\Games\Minecraft` 执行：

```text
node AI-Blueprints/library/Bootstrap/资产命令.mjs promote-reference REF-0004
node AI-Blueprints/library/Bootstrap/资产命令.mjs inspect-asset AST-0001
node AI-Blueprints/library/Bootstrap/资产命令.mjs search-assets 查询.json
node AI-Blueprints/library/Bootstrap/资产命令.mjs planner-asset AST-0001
node AI-Blueprints/library/Bootstrap/资产命令.mjs instantiate-asset AST-0001 实例参数.json
node AI-Blueprints/library/Bootstrap/资产命令.mjs preview-asset AST-0001 预览参数.json
node AI-Blueprints/library/Bootstrap/资产命令.mjs analyze-terrain 实例.json 地形高度图.json
node AI-Blueprints/library/Bootstrap/资产预览入口.mjs
```

搜索参数：`{"use":"residential","style":"medieval","scale":["small","medium"],"status":"READY","terrain_mode":"RIGID"}`。字段间 AND，字段值数组 OR，只接受五个明确字段。

实例参数：`{"rotation":90,"mirror":"x","geometry_only":false,"target_anchor":[100,64,200],"output":"D:/Games/Minecraft/AI工程/AI-Blueprints/library/state/instance.json"}`。output 文件不得已存在；实例文件是 `{blueprint, placement, omissions, ...}`，其中 blueprint 是唯一 Canonical Schema。target_anchor 是变换后入口脚底中心的目标坐标，平移量必须为整数；双门中心含半格时目标也应保留该半格。不提供位置时 origin=0，适合离线预览。

公开 JS 入口 `L3_外交层/资产公开接口.mjs` 提供晋升、读取、搜索、实例化、Planner 契约、地形分析、只读预览。CLI 不包含 deploy/approve 命令。

## 状态与边界

- READY：当前 vanilla 26.2 方块注册表、容量、朝向和锚点满足技术复用条件。
- READY_WITH_CONTENT_OMISSIONS：全部方块位置及完整 block state 可保留，但原 Block Entity NBT 不恢复；Minecraft 创建默认实体。仅允许 Bridge 已经逐状态运行时验证的白名单，实例逐位置记录 `metadata.content_omissions`，并记录源 region 的 `auxiliary_content_omissions`。来源 NBT 仍在资产原 Blueprint 中。若能力证明被撤回，实例化重新检查并拒绝旧 READY 声明。
- READY_GEOMETRY_ONLY：使用时必须明确 `geometry_only=true`。未验证的方块实体位置继续明确省略；已经通过白名单的基础方块会保留并记录内容省略。实体及计划 tick 等非 Block Entity payload 不会因该白名单而自动恢复。逐坐标记录 `omissions`，不会用另一材料替换。原完整结构和附属 NBT 仍保存在资产 blueprint.json。
- NEEDS_REVIEW：主朝向/锚点不唯一或特殊场地。只能 `preview_only=true` 生成预览，普通实例化拒绝。
- NOT_DEPLOYABLE：非法/缺失 runtime 状态、V3 20k 事务或 V5 包络限制等问题。未知 Mod 不崩溃、不被替换，可保留资产和原因。

Asset READY **不是某个存档中的施工批准**。正式施工仍须提供真实场地、完整功能意图，经过 V5 原有功能校验、MCP 校验和 Owner 对具体 revision/hash 的批准；本模块不伪造两层/楼梯标注来绕过 V5。既有 V5 对外来资产的 FAIL 在此预览中表示尚未做场地和功能验收，不代表旋转或显示失败。当前阶段没有世界写接口。

## 坐标、状态与放置

- 坐标顺序：mirror X/Z → 绕 Y 顺时针旋转 → 重新映射到非负局部包络 → 按 anchor 平移；实例全局 `rotation=0, mirror=none`，所有状态和坐标已烘焙。
- 原生 Java 器件只 bootstrap 本机 vanilla 26.2 注册表，通过 `BlockState.mirror/rotate` 和 CODEC 严格验证，绝不打开世界。当前没有加载第三方 Mod 注册表，缺失 Mod 显式不可部署。
- 实例将多 Region 的原有相对位置作为一个 Canonical 坐标空间变换。源 region/NBT 留在资产文件，实例不冒充已变换原始实体 NBT。实例的 `.litematic` 导出按当前 DataVersion 新建几何 region；原作者保留。
- 主朝向只接受最低层、同方向、连续单/双门及向外两格净空射线证据。多个分离入口、无门或特殊场地保持审查状态，不用历史 proxy 默认方向冒充主朝向。
- footprint 是全部非空气方块的二维投影，包含屋檐；ground_contact_mask 只包含最低实际方块平面。实例省略方块实体后重新计算实际占地。clearance 是原建筑实际包络外加水平 1 格、顶部 1 格余量。
- RIGID 保持主体，仅平移；FOUNDATION_FILL 只声明未来最大 2 格支撑补高策略，本轮不填方块；CUSTOM_REQUIRED 必须专门选址。地形分析只比较传入 heightmap 接触列，树木和已有建筑冲突仍需完整扫描。

## 原生器件与验证

首次安装/源码改变时运行 `pwsh -NoProfile -File AI-Blueprints/library/Bootstrap/编译原生变换.ps1`。本机已编译，JDK 与游戏库均来自已有环境，没有下载新程序。缓存绑定 Java 源及 runtime 配置；更换游戏版本需重新编译并重新审核资产，不能沿用旧 READY 结论。

`npm test --prefix AI-Blueprints/library` 执行资产契约验收。详细证据在 `AI-Test/Deployable-Assets-V6E/evidence`。预览服务仅监听 `127.0.0.1:43825`，使用冻结 V5 的 HTML/JS/模型资源，只有 GET，无批准路由。原版本 Gallery 仍在 43824，二者数据层互不写入。

ID 在单写锁下先永久保留，再发布四个文件，失败允许留空号。崩溃遗留 `state/promotion.lock` 或 `.staging` 时应人工检查，不能自动删除以掩盖未完成发布。
