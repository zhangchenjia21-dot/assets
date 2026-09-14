# 复现与核验

脚本只读 revision154 和 WB-002R-R1 历史缓存，不打开存档，不运行 Minecraft / Builder。运行于 Python 3 + NumPy 2.3.5 + Pillow 12.3.0；地图字体为 Windows `C:/Windows/Fonts/msyh.ttc`。脚本是任务外围复现代码，没有运行期业务模块、跨层或跨模块调用，不为形式创建空架构层。

从本目录以 PowerShell 执行；替换 `$py` 为可用 Python。输出必须使用独立 Local-only 文件夹，勿指定任何游戏或存档目录。

```powershell
$py = 'C:/Users/MRVHREVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$raw = 'D:/Games/Minecraft/AI工程/发布/assets/minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/raw-or-queryable'
$out = 'D:/Games/Minecraft/AI工程/研究缓存/CIV-001-MID-L1P/review-rebuild'
& $py -X utf8 './区域证据复现.py' --raw-cache $raw --output $out
& $py -X utf8 './区域规划制图.py' --cache $out --output "$out/maps"
& $py -X utf8 './区域交付核验.py' --cache $out --output "$out/checks.json"
& $py -X utf8 './主案封存核验.py' --verify
```

`regional-analysis.json` 应与 `../evidence/regional-analysis.json` 完全相同。地图同字体/依赖环境应逐字节相同；`maps.json`记录哈希，检查独立输出的6张PNG与 `../visual/`。核验脚本读取已交付地图；独立重渲染比对应另做文件哈希比较。跨平台字体变化不能称位图字节重现，但不得改变地理像素映射。

完整 SQLite / NPZ 不上传；其 SHA256 固定在 source-register 和复现入口，脚本用 SQLite `mode=ro`。Local-only 生成 context-map / regional-map NPZ。Git review bundle 保留事实聚合、20条图路径、1438条界边见证和搜索 RLE，以便无需原存档进行审核。分析用阈值只装配人为提出的搜索假说，不以程序替代 Planner 的中心选择。

Primary Freeze 前使用 `主案封存核验.py --freeze` 一次；之后只允许 `--verify`。Primary 清单不包含封存清单自身，也不包含稍后 Legacy / completion / delivery verification；它们不能修改已封存主案。`.gitattributes` 禁用本目录换行转换，Git blob 与工作文件可以按SHA256核对。
