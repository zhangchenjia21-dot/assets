# TT-002R｜Middle–East Terrain-Assisted Boundary Refinement

**REFINED_DRAFT / AWAITING GPT + OWNER ACCEPTANCE**。这是局部精修候选，不是新 Canon，不授权中域规划或建筑施工。

先读 [分段报告](reports/中域东域边界地形精修.md)，再看 [地形叠图](visual/terrain-overlay.png) 与 [变化图](visual/diff.png)。`boundary-delta.json` 保存面积、两种方向的变化量、精确欧氏位移和逐行地形见证；`validation/` 保存覆盖、拓扑、来源、地形统计和复现校验。

## 输入与交付

- `input/owner-draft-rev153.json`：Owner 本次附件的原样副本。
- `baseline-owner-draft.json`：按任务包要求保留的同字节 baseline，不重复清理 66 格。
- `refined-draft.json`：revision 154，完整六类逐格 RLE，待 GPT + Owner 接受。
- `boundary-delta.json`：只改 Middle ↔ East 主边界的审计记录。
- `visual/before.png`、`after.png`、`diff.png`、`terrain-overlay.png`：相同坐标框的主边界比较图；1 像素对应 1 block，白色原线与青色候选线重合时显示青色。

输入 SHA256：`4fce4c14295ba3f5dd760e31b8a1e3f63fe139002c9eb427ff8d4648a6aef2e6`。schema=`civ-territories/1`，revision=153，source.id=`94fc4687358a9fd5dd542997538822bfdba7b83bd76c4825fd84bd0116ea3d21`。每条 run 为 `[z,x0,x1,categoryIndex]`，两端包含；水域不出现，未分配类别不等于水域。

附件内 D-020 的路径文字有损坏，未改写附件；通过本项目唯一 D-020 文件及完全匹配的 SHA256、字节数核对来源。原始路径与解析后的路径都记入 summary。其余引用路径与哈希直接验证。

## 方法边界

模型先查看高程、坡度与 relief 诊断图，指定内谷东缘 Z1895–2090 为有明确坡折支持的局部段。程序只在这段的 Owner 主边界每行 ±48 格内比较候选；S1/S2/S6/S7/S8 不自动重分。

评分同时使用 16 格东西高差、slope8、relief32 和 Owner 偏移惩罚。近似同分时优先靠近原线；不使用平滑、曲率、面积均衡或单一等高线。逐行候选必须保留有效陆地、近岸保护与既有拓扑。分段选择和参数属于可审核的 Interpretive 判断，不声称自然地理给出了唯一政治线。

主线指共享边图中最大的端点连通分量；其余边界小环完全保留。所有新主线单位边中点及变化列中心都对旧主线单位闭边计算欧氏最近距离。`boundary-delta` 同时报告全主线（含未动部分）和仅发生偏移部分，避免零位移掩盖局部变化。

## 使用与复现

可在 TT-001 工具中载入 refined-draft.json 查看；需先解锁 Middle / East，否则导入会按工具契约拒绝改动。此操作不等于接受。后续任务应引用经 Owner 接受版本的文件哈希，不直接引用本候选作为正式 Canon。

环境：Python 3.12、numpy 2.3.5、Pillow 12.3.0、Windows 微软雅黑。脚本属于研究外围，不导入任何前序工程内部模块。执行：

```text
python -X utf8 tooling/边界精修.py
python -X utf8 tooling/交付核验.py
```

生成器只读取 baseline、R1 本地 `observed.sqlite` / `derived.npz`、WB-003R movement-corridors 和已接受公地几何。完整 raw、诊断中间 NPZ 与开始时源清单留在 `D:/Games/Minecraft/AI工程/研究缓存/建筑师/TT-002R`，不上传 GitHub。源清单是本次执行的历史审计起点，缺失时不可伪造历史 seal。预先恢复 R1 缓存后可重建轻量结果；缺缓存不能替代为重扫世界。

## 限制

`world writes = 0`；`new world block reads = 0`；`broad rescan = 0`。使用既有缓存 epoch，不宣称与当前运行存档同步。地形比较中的坡度 NaN 不参与评分和均值，有限样本 n 单列。保守 L1 诊断带只是统计子集；最终位移使用真实欧氏边距离。

现有 WB-003R 折线是地形成本研究证据，不是正式道路或通行实测。保持谷地地表连通并不保证车辆通行、完整流域归属或政治合理性。局部阶梯与接回原线的位置必须由 GPT 和 Owner 目视复核；本任务不自行通过接受门。
