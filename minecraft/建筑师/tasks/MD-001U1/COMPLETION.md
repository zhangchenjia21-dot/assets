# MD-001U1｜Completion

**DESIGN IMPLEMENTATION COMPLETED / AWAITING GPT + OWNER REVIEW**

完成日期：2026-09-13（Asia/Shanghai）。执行起点：`d06eb07b3725d11744c6715259823a7ef031c156`。遵循Task Packet、D-028、accepted MD-001P-R1与当前minecraft-builder v1.10，设计单位为一个微街区。

## 交付

- [G1 Urban Ensemble](../../planning/CIV-001/MIDDLE/G1/MD-001U1/README.md)：精确包络 **1,310格**、**5栋**独立体量、主体占地 **487格 / 37.18%**、毛楼面 **1,046格**；共用生活院、独立装卸、居民通道、台地适配、排水/水卫占位与分期。
- [Middle Kit v0.1](../../architecture/civilizations/CIV-001/kits/MIDDLE/v0.1/README.md)：5条共享DNA、16条地域规则、15个模块、6类骨架、4组palette、6条变化规则和禁配说明。每条均标成熟度，无建成/Owner接受或正式资产注册条目。
- [总平面](../../planning/CIV-001/MIDDLE/G1/MD-001U1/visual/01-top-plan.png)、2条同尺度剖面、分层平面、屋顶/skyline、生长分期、4个离线三维视图与Kit总览，共10张图。机器数据、设计实体模型、复现脚本与validation齐备。

## 证据与核验

正式存档5个相关身份/局部容器的SHA256、大小、mtime仍与MD-001S1快照一致，复用其current-world evidence；只从同一快照扩读本包络及4格缓冲，**1,902列 / 24,726次浅层体素查询**，无列明人工材料、空腔、水或熔岩异常。完整raw留本地，Git只留manifest、摘要、几何与审阅图。

主体、屋顶/雨棚投影均在G1和design envelope内，不占threshold、through-clearance或保护面。102项受保护输入哈希保持不变。5条楼梯、18条指定室内/外路线的简化净空检查无剩余冲突；修订了仓内货架、雨棚柱、邻栋维护间距、陡屋面连接、烟道穿透与客房入口。22项设计数据/模型/图在同输入重建中保持字节一致；所有交付JSON可解析、PNG可打开，图面已目视核查。详见 [validation](../../planning/CIV-001/MIDDLE/G1/MD-001U1/validation/README.md)。

轻量设计/Kit包约 **1.1 MiB**，低于15MiB目标。未上传存档、region/entity/POI、完整逐列raw、Mod或凭据。current仅机械更新为等待审核；revision154、MD-001P-R1、前序evidence与World Canon未修改。

## 限制与停止

这不是实机建成品。实际Minecraft碰撞/门状态、驮运动物/车辆、最终材料纹理、夜间照明与流体稳定性均未验证；室外设计标高还需后续有界blockstate编译。饮水来源、排水容量及接纳条件尚未确认，不能宣布具备入住条件。12个木/叶冲突片段未处理，未来world-write前仍须复查存档、实体、树冠和基础体积。

**world writes = 0；broad rescan = 0；正式世界runtime launches = 0。** 本轮最多为指定实例的PREVIEW_VALIDATED，不是Stage/Product/Build PASS。按授权commit + push至assets/main、核对远端HEAD后停止，交GPT + Owner独立审核；不得自动开始施工。
