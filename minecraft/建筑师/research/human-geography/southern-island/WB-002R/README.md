# WB-002R｜Southern Island Regional Reconnaissance

**PASS-CANDIDATE / READY FOR INDEPENDENT REVIEW**。Owner 确认退出后已重新读取当前世界，311 根独立 raw-column 核验通过。首轮读取后的外部写入、首轮快照与刷新基线分别保留；不声称整个跨窗口期间世界始终未变。最终封口见 `validation/source-audit.json`，本状态不代替 GPT 独立审核。

研究对象为任务指定 `NGEO-009` 及 source ROI X=-800..415、Z=1376..2655；扩展 0 格。不是整个更大南部地块，也没有把 Owner 的“两个岛片/三个区域”作为事实先验。

## 已形成的事实层

- 刷新后的当前 1-block 观测：1,556,480 columns / 6,080 chunks / 12 regions。
- 4-block 植被样点：97,280 柱，逐 Y 记录过滤地表以上至 raw top 的 canopy/trunk/ground vegetation 数量；不估算树数或生态物种。
- `observed.sqlite` 是本轮原始观测，`regional-profile.sqlite` 是主查询库；完整源 chunk/region lineage、原始/过滤表层、高程、原始/过滤 surface biome、材料、实际水区间均可回溯。
- 派生地形类、连通分量、实际 RLE 成员、2～5 类数值候选与模型裁定独立保存。最终仅保留一个 SIRZ 研究参考单元，不宣称已建立清晰离散内部区界。
- `world writes = 0`。两次受保护读取窗口内世界均未变，V1 / NG-2 / NG-3 自任务起始始终 immutable；窗口之间的外部变化见 `manifest/epoch-transition.json`，当前事实绑定 `manifest/current-source-before.json`。

## 结果与尺度

指定主岛为 C 形低岛：575,363 干陆柱，median Y66，p90 Y71，max Y79。LOW_RELIEF_FLAT 67.65%，GENTLE_SLOPE 15.49%。这两个操作性指标不是 buildable land。

主要 biome 是 savanna / arid_highlands / beach。东半部略高于西半部，但两侧都存在广泛低起伏地面。北、南两翼由西侧陆地相连；中间看似独立的陆片连接的是另一个触 ROI 东边界的陆体，后者 max Y168，不能与主岛混为一谈。

这些范围差异是理解 Owner 印象的关键。对 Owner 所说“两个岛片”的对应仍不确定，因为没有具体视点坐标；本轮明示候选参照与实际连接路径，不假装识别其原始视点。H-01/03/04 为 PARTIALLY_SUPPORTED，H-02/05 对指定主岛为 NOT_SUPPORTED；不是对未完整调查的东侧较大陆体作判断。

## 查询

在 WB-002R 目录运行，查询仅需 Python 标准库：

```powershell
python tooling/Bootstrap/区域命令.py coordinate --x -248 --z 2056
python tooling/Bootstrap/区域命令.py zone --id SIRZ-001
python tooling/Bootstrap/区域命令.py low-relief --x -248 --z 2056 --radius 64
python tooling/Bootstrap/区域命令.py context --x -248 --z 2056 --radius 64
python tooling/Bootstrap/区域命令.py hypotheses
```

坐标命中实际单柱；附近对象按 RLE 成员距离，不能用 bbox 代替。radius 非负；ROI 外返回 OUTSIDE_STUDY_AREA，未知 ID 返回 JSON error。context 不产生人文或建筑内容。

## 复现

Python 3.12 + numpy 2.3.5 / Pillow 12.3.0 / nbtlib 2.0.4；只读世界保护要求 Windows，地图字体为 Arial。本任务工具从 NG-2 解码器/NG-3 只读保护逻辑创建独立版本，历史文件不修改，也不 import 历史内部层。

```powershell
python tooling/Bootstrap/区域命令.py derive
python tooling/Bootstrap/区域命令.py relations
python tooling/Bootstrap/区域命令.py build
python tooling/Bootstrap/区域命令.py views
python tooling/测试/区域查询验证.py
python tooling/测试/区域重建验证.py
python tooling/测试/区域拓扑独立验证.py
```

当前成果已有两个 epoch。`read` / `refresh` 均拒绝覆盖已存在的各自基线；不要重置初始指纹。`seal --world <绝对路径>` 核对当前 epoch 的源 inventory/hash/size/mtime，并核对历史 evidence 自第一次读取以来始终不变。原始柱核验命令为 `python tooling/测试/原始柱独立核验.py <存档绝对路径>`；只读锁仍是必需的，不启动游戏。

最终 SQLite 超过 GitHub 单文件限制；以 `区域归档命令.py archive` 生成 lossless gzip + SHA256 + round-trip，拉取后先执行 `python tooling/Bootstrap/区域归档命令.py restore` 恢复标准文件名。哈希与完整性证据在 `manifest/store.json`；首轮旧快照也保留压缩归档及独立哈希。运行时间仅在 source manifest/audit；核心库保留固定 snapshot as-of，重建不生成新时间戳。

`terrain-position-proxies.json` 公开本低岛局部高地（Y≥72）、低地（Y≤65）与 65×65 窗内上部位置代理。这些不是山脉、脊线或可通行路径的确认，也不替代实际 slope/relief/step。

## 架构与边界

L0 定义范围/字段/材料代理；L1 负责柱解码、保护、指标、查询、地图；L2 编排读取、派生、关系与汇编；L3 是公开入口。Bootstrap/测试是外围，依赖向下，无跨历史模块内部调用。JSON/JSONL 和地图为派生阅读/交换视图；世界始终是原始事实源。

不创建文明、种族、部族、国家、政治边界，不进入 Architecture Bible / Build。本研究不恢复任何文明空间分配。下一步仅为 GPT 独立审核。
