# D-015｜AB-001P1 三席议会中心岛 Site Gate 授权

状态：**OWNER DIRECTION / ACTIVE AUTHORIZATION**

日期：2026-09-10

## 目的

为 CIV-001 第一座 Canon Build 候选——三席议事大厅——完成建造前的 Site Gate。

Owner 已批准三席议会相关建筑优先位于其所称“西部平岛的中心岛”，但该称呼尚未映射为唯一机器坐标。本授权只允许定位与局部观察，不允许建筑设计落地或 Minecraft world write。

## 授权范围

允许：

- 复用 WB-002R-R1 / WB-003R 现有地形、水陆与通达性证据；
- 读取当前 `建筑师` world 做 bounded / read-only site verification；
- 识别 Owner referent 可能对应的 landform / component / local sector；
- 形成局部高程、坡度、岸线、面积、主要视线、进出方向、现有植被 / 人工内容等 Site Context；
- 若无法唯一映射，形成 2–3 个最合理候选供 Owner 选择。

禁止：

- 猜测并静默固定中心岛坐标；
- 施工、清树、整地、建路、放方块；
- 设计完整联盟政治中心；
- 把 Site candidate 自动变成 Build authorization；
- broad regional rescan。

`world writes = 0`。

## 完成条件

必须得到以下之一：

1. `UNIQUE_MAPPING_SUPPORTED`：Owner referent 可由空间证据高置信唯一对应，并形成完整 Site Context；
2. `OWNER_SELECTION_REQUIRED`：存在多个合理对应，输出候选对比并停止，等待 Owner 选择；
3. `INSUFFICIENT_EVIDENCE`：无法可靠定位，说明缺口并停止。

不得为了“完成任务”强行选择。

## 后续

只有 Site Gate 被 GPT / Owner 接受后，才进入三席议事大厅具体 Architecture Design；设计完成后仍需单独 world-write 授权才能施工。
