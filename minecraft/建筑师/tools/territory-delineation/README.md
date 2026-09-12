# TT-001｜南部岛屿群领土划界工作台

状态：READY FOR INDEPENDENT REVIEW。工具测试完成，Owner 实际划界和 GPT 独立审核尚未进行。

用桌面 Edge / Chrome 双击本目录 `index.html`，无需服务器、安装包、网络或 Minecraft。首次加载完整格网与 QA 需要短暂计算。建议窗口宽度至少 1280 px；较窄窗口可横向滚动。运行时只在浏览器内存中编辑，不访问或写入存档。

## 开始编辑

1. 全图核对底图。金色轮廓为 D-020 accepted Commons，紫色为 accepted east connector；参考轮廓不会随草稿改变。
2. 选择西域、中域、东域、公地、未分配或争议区。公地和中域默认锁定，锁定同时禁止移入及移出。要在其他位置绘制中域，先主动取消中域锁。
3. 滚轮以光标为中心缩放；中键拖动或选择“平移”。“1:1”一屏幕像素对应一格，“逐格 8×”进一步放大。坐标显示 X / Z，北为负 Z、东为正 X。
4. 画笔参数 1 只编辑一个 block-column；参数 r 的实际圆盘半径为 r−1 格。快速拖动补齐经过的列。矩形两端均包含；擦除恢复 UNASSIGNED。所有操作只影响有效陆地，水域与研究范围外不可编辑。笔画释放时显示最终着色；矩形拖动时显示范围。
5. 撤销 / 重做对应完整笔画或导入事务。Ctrl+Z / Ctrl+Shift+Z 可用；输入框内不接管快捷键。历史最多 100 次或约 24 MiB，最新一次即使超出预算仍保留。撤销恢复原事务，不受之后改变的类别锁限制。
6. 经常“保存草稿 JSON”。关闭页面会丢失未保存内容；下载完成后请确认文件存在。重新打开后用文件选择框载入草稿，涉及锁定类别变更时需先检查并解锁。

## 确认与导出

“导出草稿 ZIP”保留 DRAFT 状态。“确认选择并导出 ZIP”要求先更新 QA、填写 Owner 署名并确认当前发现，结果标记 OWNER_CONFIRMED。任何编辑会取消勾选；不会自动分配未分配格或解决争议。Owner 署名是人工选择记录，不是数字签名，也不是对已接受参考边界变更的自动批准。

ZIP 解压后有且仅有以下交付路径：

- `data/territories/current.json`：完整无损逐格归属、来源哈希、状态、时间、署名。
- `data/territories/preview.png`：完整 3264×2112 领土栅格；一像素一列，水域透明。颜色见下表。底图阴影不混入分类预览。
- `data/territories/areas.md`：各类别精确列数。
- `data/territories/adjacency.json`：类别顺序和对称接壤矩阵，单位是共享陆地边数。
- `data/territories/qa.md`：未分配、争议、accepted 改动、碎片与飞地候选详情。

下载不会直接覆盖仓库。将需要交付的 ZIP 解压到选定成果目录，连同来源和 QA 交审核。后续规划 / 建筑任务引用经 Owner 确认的 `current.json` 文件哈希及 `source.id`；只有经项目批准的提升流程才可进入 `world/`。本工具不改当前 World Canon，不授权建筑。

|索引|类别|颜色|
|---:|---|---|
|0|ALLIANCE_COMMONS|#e2bd66|
|1|WEST_DOMAIN|#5cbd98|
|2|MIDDLE_DOMAIN|#ae93dc|
|3|EAST_DOMAIN|#e88e69|
|4|UNASSIGNED|#9ba9b8|
|5|DISPUTED|#ef6e98|

## 数据契约

schema = `civ-territories/1`。`runs` 每项是 `[z,x0,x1,categoryIndex]`，两端包含，block(x,z) 占据 `[x,x+1) × [z,z+1)`。每个有效陆地列必须出现恰好一次，水域不出现。查询某坐标：找到 `z` 相同且 `x0 ≤ x ≤ x1` 的 run；类别索引映射到 `categories`。没有 run 表示水域 / 范围外，不等于 UNASSIGNED。

导入必须 schema、类别顺序、bounds、source.id 一致，且全覆盖、无重叠、无水域、无非法类别；失败不会部分修改当前草稿。文件上限 50 MiB。accepted 参考几何保存在预加载中，current 中的归属可在主动解锁后调整；QA 会报告差异格数，原始参考始终不变。

## 来源与初始状态

复用 WB-002R-R1 缓存的 `derived.npz` / `observed.sqlite` 和 AB-001P1R 已接受 RLE；哈希与完整来源路径列于 `预加载/manifest.json`。没有 whole-region 世界重扫，也没有新世界 block 读取。

研究范围 X=[−800,2463]，Z=[1376,3487]，有效陆地 2,256,681 列。初始 Commons 92,124；中域 connector 13,661；UNASSIGNED 2,150,896；其余 0。没有 suggested_draft_v0，也没有新增人文领土推断。`examples/initial-state/` 是这套初始几何的示例 DRAFT 导出，未被认定为正式领土选择。

**CACHED_EPOCH_ONLY：** 开始时存档文件被占用，未取得世界封口锁；因此本轮仅使用既有缓存，不宣称与当前运行世界同步。验证记录见 `validation/freshness.json`。现有 research / world Canon / architecture 经前后哈希审计保持不变。`world writes = 0` 指本任务行为，不声称游戏进程没有写入世界。

## QA 解释

四邻接连通；角接不算接壤。相同类别每个不连通分量计为一片，最大片之外为 secondary components；面积小于 64 格计为碎片。飞地候选指不接触水域或研究边界、且仅被一个其他类别包围的连通片。自然离岛可能合理，以上数字不自动构成错误，也不裁决政治边界。未分配 / 争议区均参与相同几何计算。接壤只数陆地共享单位边，不将海峡或水路视为接壤。

地形阴影从缓存 exposed_y / slope8 派生，仅作视觉参考；biome 颜色是稳定哈希配色，图例列出原始名称，不用于判定族群、农业产量或通行成本。

## 复现与结构

浏览器运行无第三方依赖。外围构建脚本使用 Python 3.12 + numpy + Pillow，仅读取本地既有缓存；完整 raw 不入 Git。`构建/预加载生成.py build` 重建 preload；init / seal 用于本轮源保护审计（init 拒绝覆盖已有审计起点）。原缓存必须按其既有恢复说明在原位置可用。

Node 执行 `node 测试/边界回归.cjs`。浏览器测试：`node 测试/浏览器验收.cjs`，需要 Playwright，可用 `PLAYWRIGHT_MODULE` / `BROWSER_EXECUTABLE` 指定本机模块及浏览器；默认路径为本次执行环境。ZIP / PNG 交叉验证用 `python 测试/导出校验.py`。测试临时文件不提交。

L0 固定类别 / 格网契约 → L1 状态器、几何 QA、编码器 → L2 导出流程 → L3 公开编辑接口；Bootstrap 负责 DOM / canvas。依赖只向下，UI 仅从 L3 读取状态副本和调用事务。构建、测试、文档位于四层之外。

当前限制：单人内存编辑，无自动保存 / 多人合并；QA 在主线程短暂计算，处理完整区域时可能停顿；Owner 实际使用尚待验收。单页版本没有海量历史无限保留或自动改写文件权限。
