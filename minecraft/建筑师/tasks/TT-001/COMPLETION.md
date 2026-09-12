# TT-001｜Territory Delineation Tool for CIV-001

状态：**READY FOR INDEPENDENT REVIEW**。工具实现和技术验证完成；未代替 Owner 进行领土选择，未宣告产品验收或 Canon 接受。

执行授权：Owner 本轮明确请求；当前 main 无 TT-001 TASK.md。以 `21cb02b4bf5b99fc0d668c67e4533345e221915c` 为起点，不覆盖 MD-001R 当前任务或并行项目提交。

## 交付

工具与说明：[`tools/territory-delineation/`](../../tools/territory-delineation/README.md)，入口 [`index.html`](../../tools/territory-delineation/index.html)。桌面 Edge / Chrome 直接打开即可，无服务器或运行时依赖。

支持六类逐 block-column 归属、画笔、擦除、矩形、撤销 / 重做、类别锁、有效陆地约束；提供陆水轮廓、地形阴影、biome、accepted Commons / connector 精确轮廓与当前领土图层。公地和 connector 分别预载到 ALLIANCE_COMMONS 与 MIDDLE_DOMAIN 并锁定，其余陆地 UNASSIGNED。

QA 包含面积、未分配、争议、四邻接连通片、面积小于 64 格碎片、飞地候选、共享陆地单位边接壤矩阵，以及 accepted geometry 改动列数。几何提示不自动裁决人文边界。

草稿 JSON 可完整重新载入；同源、全覆盖、无水域、无重叠及锁定检查先于任何替换。ZIP 同次导出 current.json、preview.png、areas.md、adjacency.json、qa.md，路径均为 `data/territories/`。Owner 署名和当前 QA 确认后可导出 OWNER_CONFIRMED；没有自动写入项目 Canon。

[`examples/initial-state/`](../../tools/territory-delineation/examples/initial-state/) 是初始几何的 DRAFT 示例，不是 Owner 最终选择。未生成推测性 suggested_draft_v0。

## 数据与边界

复用 WB-002R-R1 observed / derived 本地缓存、AB-001P1R RLE 与 D-020；没有 broad rescan。有效陆地 2,256,681 列：Commons 92,124；中域 connector 13,661；未分配 2,150,896；西域、东域、争议均 0。每列精确归属，未用 bounds 或椭圆代替 accepted geometry。

**world writes = 0；new world block reads = 0。** 开始时存档文件占用导致只读封口锁不可得，因此底图标为 CACHED_EPOCH_ONLY / NOT_VERIFIED_WORLD_IN_USE；工具与导出不宣称当前运行世界已同步。该限制在 UI、README、导出来源与 freshness 记录中保留。

V1 / NG-2 / NG-3 / R1 等全部 research、当前 world Canon、architecture 前后哈希审计不变。没有设计建筑或施工，没有新增文明 / 部族 / 正式领土设定。

## 验证

见工具 `validation/`：

- Node 回归：单格、陆水 / 类别锁、矩形、撤销重做、原子导入拒绝、完整真实 RLE 往返、面积、飞地与对称接壤。
- Edge headless `file://`：无页面异常；真实鼠标单格、矩形、撤销重做、底图切换、草稿下载与文件载入、正式确认门槛和两种 ZIP 导出。
- Python 独立解压：ZIP CRC、五条路径、状态、面积、PNG 一像素一列的分类计数、导出 revision 一致与接壤对称。
- preload 确定性重建哈希一致；源审计不变。工作台截图已目视检查。

四层检查：业务契约 L0；状态 / QA / 编码 L1；导出流程 L2；公开接口 L3；Bootstrap / 测试 / 构建为外围。UI 通过 L3 操作，渲染状态为副本，无向上依赖或跨模块内部直连。

完整 raw 不提交；仅工具、约 3 MiB 预加载、示例与轻量验证。总 payload 见 `validation/交付体积.json`，低于 15 MiB 目标。

## 已知限制与交回

单人浏览器内存编辑，需要主动下载保存；历史有预算上限，完整区域 QA 可能短暂停顿。运行时底图与当前存档未复核。Owner 实际使用、最终领土选择和 GPT 独立审核待进行。

完成 scoped commit + push 至 assets/main 并核对远端 HEAD 后停止；不继续 MD-001R、Architecture Bible 或 Build。
