# MD-001U1｜核验与复现

## 证据入口

- `source-freshness-before.json` / `source-freshness-after.json`：正式存档5个相关文件的只读哈希/时间戳核对；不是全存档完整性证明。
- `source-inputs.json`：受保护总规、Site Gate、World/Decision输入与本轮读取的 minecraft-builder v1.10 哈希。
- `local-context.json`：1,902列有界浅层、材料计数、人工/空腔分类结果与木叶块位。
- `raw-cache-manifest.json`：完整raw仍留本地，source epoch/hash可追溯。
- `design-qa.json`：指定门前/楼层路线、踏步/落脚样本的简化净空检查。
- `spatial-relations.json`：主体和屋顶投影、邻间、开放地连通、R1上下文。
- `delivery-check.json`：复现哈希、JSON/PNG检查、受保护文件封口与体积。
- `CRITIC.md`：模型自检、实际修订、不能被数字检查替代的设计判断。

RLE为`[z,x_start,x_end]`包含端点。设计实体为`a=[x,y,z]`,`b=[x,y,z]`的半开盒；floor字段是站立面Y，不能当作方块底Y。实体颜色只用于图示，不是完整blockstate。所有图X/Z等比例；剖面水平/垂直不夸张。斜视是正交三维设计审阅，非真实玩家FOV。

## 本机复现

在本目录的上一级（MD-001U1）执行：

```text
python -X utf8 tooling/街区设计编译.py
python -X utf8 tooling/场地关系核验.py
python -X utf8 tooling/地域模板编译.py
python -X utf8 tooling/街区审阅制图.py
python -X utf8 tooling/交付封口核验.py
```

现有Python含numpy/Pillow；nbtlib2.0.4由前序只读解析器使用既有第三方目录，不安装Mod、不启动游戏。当前实际Python路径：`C:/Users/MRVHREVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`。中文字体使用Windows `msyh.ttc`。

依赖本地 `D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001S1/` 的snapshot/capture/surface缓存。读取器仅复用前序研究外围脚本的Reader，不调用其capture/surface写出函数，不重跑/覆盖前序evidence。当前源哈希变化会拒绝编译；届时须另做最小刷新与lineage，不能静默以新世界替换历史样本。缺失原cache应报告MISSING_LOCAL_CACHE，Git轻量包不包含完整raw。

封口脚本默认核验而非反复全量重绘。`--rebuild`才执行一次同输入模型/地图重建比较；freshness时间字段不参与确定性哈希。Windows字体版本或渲染库不同可能改变PNG字节，不能据此推断几何变化，须分别比较JSON与像素。

## 检查边界

净空检查对室内/外路线以0.3格半径、1.9格高度检查设计实体；楼梯踏步用0.2格采样半径排除自身踏步实体，查其它实体和护栏。**这不是完整连续Minecraft碰撞模拟**，也不检验驮运动物或车辆。室外插值标高与铺装实体是工程意图，尚需有界blockstate编译为合法台阶/坡道，不能称真实可走道路。

场内排水仅检查线位、单调invert、不穿主体和局部出水条带；未模拟流体、容量、暴雨或污水处理。人工分类仅为列明材质，不能证明不存在玩家放置的天然材料。Kit的PROPOSED条目不借其它实例的检查升级。

本轮工具是研究/设计工程外围，未新增运行时模块或跨层内部依赖。无向上依赖、无不明包装层；新增业务脚本中文命名，协议文件按Task Packet保留英文。`world writes = 0`。
