# 本地快照复算与轻量审核

Windows Python3，NumPy2.3.5、Pillow12.3.0、nbtlib2.0.4；字体Microsoft YaHei。首次当前读取仅复制所选容器，以GENERIC_READ / FILE_SHARE_READ句柄拒绝已有写入/删除；后续均从相同快照解码，没有Minecraft加载/保存。

以下从本目录运行。缓存缺失时应报告MISSING_LOCAL_CACHE，不要拿今天世界覆盖旧epoch。完整snapshot/current.npz只Local-only、PRESERVE_LOCAL，见evidence/raw-cache-manifest.json。重放默认拒绝自动新采集；`--capture`是新epoch显式操作，本任务已结束后不得以此偷偷刷新主案。

```powershell
$py='C:/Users/MRVHREVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:MID_A_REPO='D:/Games/Minecraft/AI工程/发布/assets-CIV-001-L0P'
$env:MID_A_CACHE='D:/Games/Minecraft/AI工程/研究缓存/CIV-001-MID-A-L2P'
$env:MID_A_L1_CACHE='D:/Games/Minecraft/AI工程/研究缓存/CIV-001-MID-L1P/rebuild'
$env:MID_A_OUTPUT="$env:MID_A_CACHE/review-rebuild"
$env:MID_A_CHECK_OUTPUT="$env:MID_A_CACHE/review-checks.json"
New-Item -ItemType Directory -Path $env:MID_A_OUTPUT -Force | Out-Null
Copy-Item -LiteralPath '../MOVEMENT-PUBLIC-SPACE-SKELETON.json' -Destination "$env:MID_A_OUTPUT/MOVEMENT-PUBLIC-SPACE-SKELETON.json"
& $py -X utf8 './当前局部采集.py'
& $py -X utf8 './城市空间推导.py'
& $py -X utf8 './通行可达核验.py'
& $py -X utf8 './城市规划制图.py'
& $py -X utf8 './城市交付核验.py'
& $py -X utf8 './主案封存核验.py' --verify
```

前四脚本独立输出review-rebuild；交付核验脚本针对仓库主产物与缓存相互核验。复算的evidence五份派生文件和access-probes及六图应与主案对应文件逐字节相同。同环境已实际通过；跨平台字体变化不保证位图哈希，地理成员不得变化。

本地分析的完整current-surface-runs.json和shallow-exceptions.json不提交Git；Git中surface-witnesses为16格格点+每材质前三条，浅层为按状态分层见证与计数，风险/城市/片区RLE完整。源NBT中的自然材料可能人工放置，白名单差异不自动裁定人造建筑。植被剥离协议与旧研究不同会影响exposed_y，不能把差值直接称新增施工。

脚本为任务外围复现代码，无新增运行期业务模块或跨模块内部调用；NBT填充long算法独立实现自已验证World-Survey原理。没有runtime服务、Builder或raw世界写入器。模型先提出候选/角色和密度假说，程序仅装配/测量，不是自动语义规划器。
