# MD-001S1｜G1 共享周转与生活院 Local Site Gate

**IMPLEMENTATION COMPLETE / RECOMMENDED SITE S1 / AWAITING GPT + OWNER REVIEW**

[完整 Site Gate](SITE-GATE.md) · [三候选对比图](visual/candidate-comparison.png) · [S1 局部图](visual/recommended-site-detail.png)

推荐 S1 东侧高位缓台：570 格 gross usable envelope，地面 Y66–67。另保留 S2 586 格、S3 605 格。不是建筑 footprint、施工范围或设计方案；总规与领土没有改动。

## 当前世界与数据

本轮从真实 `建筑师` 存档捕获局部只读快照（26.2 / DataVersion4903）。完整 identity、UTC 时间、源文件 SHA256 与修改时间见 `current-world-audit.json`。G1 7175 列全部核对，含必要缓冲及通行背景总表层查询10954列；另有精确站立视线采样，不是区域扫描。

当前 G1 相比 accepted cache 有1列 dirt→grass_block 差异，地面与表层高度均未变。原始容器和逐列数据 Local-only，旧 cache 仅用于对比，不代替当前读取。

- `candidates.json`：三个精确 RLE、地形/生活/通行/视觉比较和结论。
- `recommended-site.json`：S1 当前推荐及后续条件。
- `surface-terrain.json`：当前表层统计、抽样见证与旧缓存差异。
- `existing-content-audit.json`：人工材料、树木、block entities、POI、结构记录与实体限制。
- `subsurface-audit.json`：各候选及4格缓冲、地面以下12格连续逐柱检查。
- `access-drainage-audit.json`：步行接近和局部排水见证、闭洼检查、饮水/通行限制。
- `validation/`：源封口、独立高度检查、复现及交付清单。

RLE `[z,x_start,x_end]` 两端包含；block 占据 `[x,x+1)×[z,z+1)`。bounds 只是定位框，不能用框内面积代替实际成员。4格缓冲是调查范围，允许覆盖邻接环境，不是追加可建地。

## 复现

使用现有 Python + numpy/Pillow；nbtlib2.0.4 从 `D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方` 读取，不安装或更改游戏环境。脚本为研究外围，自包含格式解析，不跨用前序模块内部层。

Local Cache：`D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001S1`。

```text
python -X utf8 tooling/当前场地读取.py surface
python -X utf8 tooling/场地候选核查.py
python -X utf8 tooling/场地证据汇编.py
python -X utf8 tooling/场地证据制图.py
python -X utf8 tooling/场地交付核验.py
```

`capture` 模式只用于首次取得当前快照，已有快照会拒绝覆盖；若要新的时间点必须另行保留 lineage，不能静默替换。复现不启动 Minecraft；`场地交付核验.py` 还检查正式源文件是否仍与快照相同，后来存档变化时应报失败而非悄悄宣称最新。

无玩家视角截图；站立眼高的单射线只说明局部遮挡，不代表尚未设计的建筑天际线。现有材料不能证明玩家未放置自然方块。饮水来源、深于12格地下、实际入口/车行仍须后续设计和 pre-build 检查。

`world writes = 0`。Site Gate 经 GPT + Owner 接受后才能另建 Architecture Design Task；本轮不自动开始。
