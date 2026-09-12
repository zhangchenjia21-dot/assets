# LABELING_NOTES — 123 张蓝图 Taxonomy 落标记录
> 生成：`scripts/build_labels.py`（确定性规则，可复跑）。主信号 = V6C2 人工+规则审核分类（`references/classification-v2/catalog-final.json`），几何交叉验证来自 P1 元数据。
## 方法
- **Style**：取 V6C2 `styles` 中置信度最高标签，经 `STYLE_MAP` 映射到本 taxonomy（medieval/fortified→Medieval，rustic/cottage→Rustic，fantasy/high_fantasy→Fantasy，japanese→Japanese，chinese→Chinese，european/desert/classical→Other）；top 置信度 < 0.55 或几何强冲突 → **Unknown** 并记录。
- **Function**：按 `primary_use` + `secondary_use` 规则映射（见脚本 `map_function`）；primary_use=unknown → Unknown。候选类无载具而样本存在 ship/airship/dock，新增 **Vehicle** 类（n=7，记录在案）；候选类 **Bridge** 无样本，不硬建。
- **置信度**：high ≥0.70 / medium 0.55–0.70 / low <0.55（继承 V6C2 数值置信度，几何弱支持时下调一档）。
- **label_basis**：existing metadata = 直接继承 V6C2；mixed = 几何交叉验证参与（支持或下调）；本库未发生纯 geometry/manual signal 提拔。

## 类别样本量

### Style

| 类别 | n |
|---|---:|
| Unknown | 56 |
| Rustic | 20 |
| Medieval | 19 |
| Fantasy | 10 |
| Other | 7 |
| Japanese | 7 |
| Chinese | 4 |

### Function

| 类别 | n |
|---|---:|
| Residential | 23 |
| Decoration | 22 |
| Castle | 14 |
| Tower | 13 |
| Religious | 10 |
| Workshop | 7 |
| Vehicle | 7 |
| Unknown | 6 |
| Inn | 5 |
| Civic | 4 |
| Gate | 3 |
| Blacksmith | 3 |
| Farm | 3 |
| Mixed-use | 2 |
| Warehouse | 1 |

## 降级记录（5 条）

| ref_id | 类型 | 原因 |
|---|---|---|
| REF-0016 | style | chinese@0.48 < 0.55 → Unknown |
| REF-0017 | style | chinese@0.48 < 0.55 → Unknown |
| REF-0035 | style | chinese@0.48 < 0.55 → Unknown |
| REF-0076 | style | japanese@0.48 < 0.55 → Unknown |
| REF-0096 | style | desert@0.48 < 0.55 → Unknown |

## 全量标签表（123 行，完整不截断）

| ref_id | 名称 | style_label | style_conf | function_label | function_conf | label_basis | V6C2 style(top@conf) | V6C2 primary_use | notes |
|---|---|---|---|---|---|---|---|---|---|
| REF-0001 | 丁香树坛 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0002 | 世界之塔 | Medieval | medium | Tower | high | mixed | medieval@0.64 | landmark | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；landmark+tower → Tower；几何交叉验证：height_ratio=2.25 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0003 | 中世纪农舍 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 4、楼层 3 支持居住 |
| REF-0004 | 中世纪四层小屋 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 2、楼层 4 支持居住 |
| REF-0005 | 中世纪大门守卫房 | Medieval | medium | Gate | medium | mixed | medieval@0.64 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+gatehouse/wall → Gate |
| REF-0006 | 中世纪工具匠铺 | Rustic | high | Blacksmith | high | mixed | rustic@0.79 | industrial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；industrial+blacksmith → Blacksmith |
| REF-0007 | 中世纪工坊 | Rustic | high | Workshop | high | mixed | rustic@0.79 | industrial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；industrial（生产建筑）→ Workshop |
| REF-0008 | 中世纪异世界酒馆 | Rustic | high | Inn | medium | mixed | rustic@0.79 | commercial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；commercial+tavern/inn → Inn |
| REF-0009 | 中世纪据点_小 | Medieval | high | Castle | high | mixed | fortified@0.8 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0010 | 中世纪海港小屋 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 3、楼层 2 支持居住 |
| REF-0011 | 中世纪酒馆_二 | Rustic | high | Inn | medium | mixed | rustic@0.79 | commercial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；commercial+tavern/inn → Inn |
| REF-0012 | 中世纪酿酒厂 | Rustic | high | Workshop | high | mixed | rustic@0.79 | industrial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；industrial（生产建筑）→ Workshop |
| REF-0013 | 中世纪门楼 | Medieval | medium | Gate | medium | mixed | medieval@0.64 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+gatehouse/wall → Gate |
| REF-0014 | 中世纪面包房 | Rustic | high | Workshop | high | mixed | rustic@0.79 | industrial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；industrial（生产建筑）→ Workshop |
| REF-0015 | 中式塔楼 | Chinese | high | Tower | high | mixed | chinese@0.72 | landmark | 几何交叉验证：stair_count=1064，屋顶构件存在；landmark+tower → Tower；几何交叉验证：height_ratio=2.33 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0016 | 中式小亭 | Unknown | low | Decoration | high | existing metadata | chinese@0.48 | landscape | V6C2 top style=chinese 置信度 0.48 低于 0.55，降级 Unknown；landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0017 | 中式灯笼路灯 | Unknown | low | Unknown | low | existing metadata | chinese@0.48 | unknown | V6C2 top style=chinese 置信度 0.48 低于 0.55，降级 Unknown；primary_use=unknown 或无证据 |
| REF-0018 | 中式青蛇飞艇 | Chinese | high | Vehicle | medium | mixed | chinese@0.72 | transport | 几何交叉验证：stair_count=49，屋顶构件存在；transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0019 | 云杉树_中_三 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0020 | 伦布里奇要塞 | Medieval | high | Castle | high | mixed | fortified@0.8 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0021 | 八角塔 | Medieval | medium | Tower | medium | mixed | medieval@0.64 | landmark | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；landmark+tower → Tower；几何交叉验证弱支持：height_ratio=1.27 <1.65 |
| REF-0022 | 六角亭 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0023 | 农田_一 | Unknown | low | Farm | high | mixed | unknown@0.2 | agricultural | primary_use=agricultural；几何交叉验证：植被/装饰族占比支持农田景观 |
| REF-0024 | 冥界之门 | Fantasy | high | Decoration | high | existing metadata | fantasy@0.72 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0025 | 利登赛特要塞 | Medieval | high | Castle | high | mixed | fortified@0.8 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0026 | 利维坦号 | Unknown | low | Vehicle | medium | existing metadata | unknown@0.2 | transport | transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0027 | 剑士工会 | Medieval | medium | Civic | medium | mixed | medieval@0.64 | civic | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=civic（含 arena，公共集会） |
| REF-0028 | 南瓜屋 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证：门 2、楼层 1 支持居住 |
| REF-0029 | 双人农田木屋 | Unknown | low | Farm | medium | mixed | unknown@0.2 | agricultural | primary_use=agricultural；几何交叉验证弱支持：植被占比不高 |
| REF-0030 | 双层L型农田木屋 | Medieval | medium | Farm | medium | mixed | medieval@0.64 | agricultural | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=agricultural；几何交叉验证弱支持：植被占比不高 |
| REF-0031 | 双羽木飞船 | Unknown | low | Vehicle | medium | existing metadata | unknown@0.2 | transport | transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0032 | 哈利卡纳苏斯陵墓 | Unknown | low | Decoration | medium | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0033 | 哨塔_小 | Medieval | medium | Tower | medium | mixed | medieval@0.64 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+tower → Tower；几何交叉验证：height_ratio=1.67 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0034 | 唐屋_大 | Chinese | high | Castle | high | mixed | chinese@0.72 | landmark | 几何交叉验证：stair_count=711，屋顶构件存在；landmark+palace → Castle（纪念性大型建筑群并入，记录在案）；几何交叉验证：石质主体支持 |
| REF-0035 | 唐屋_小 | Unknown | low | Castle | medium | mixed | chinese@0.48 | landmark | V6C2 top style=chinese 置信度 0.48 低于 0.55，降级 Unknown；landmark+palace → Castle（纪念性大型建筑群并入，记录在案）；几何交叉验证：石质主体支持 |
| REF-0036 | 四兵器铁匠铺 | Unknown | low | Blacksmith | high | existing metadata | unknown@0.2 | industrial | industrial+blacksmith → Blacksmith |
| REF-0037 | 圣亨格勒大教堂 | Other | high | Religious | high | existing metadata | european@0.72 | religious | V6C2 tag=european 映射 Other（候选类不细分）；primary_use=religious |
| REF-0038 | 圣埃德大教堂 | Other | high | Religious | high | existing metadata | european@0.72 | religious | V6C2 tag=european 映射 Other（候选类不细分）；primary_use=religious |
| REF-0039 | 圣彼得里教堂_德国汉堡 | Other | high | Religious | high | existing metadata | european@0.72 | religious | V6C2 tag=european 映射 Other（候选类不细分）；primary_use=religious |
| REF-0040 | 地中海岛屿小屋 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证：门 2、楼层 1 支持居住 |
| REF-0041 | 壁炉小屋 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 1、楼层 2 支持居住 |
| REF-0042 | 大圣诞树 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0043 | 大型中世纪酒馆 | Rustic | high | Inn | medium | mixed | rustic@0.79 | commercial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；commercial+tavern/inn → Inn |
| REF-0044 | 大型奇幻农舍 | Fantasy | high | Residential | medium | mixed | fantasy@0.72 | residential | primary_use=residential；几何交叉验证：门 5、楼层 1 支持居住 |
| REF-0045 | 大教堂 | Unknown | low | Religious | medium | existing metadata | unknown@0.2 | religious | primary_use=religious |
| REF-0046 | 女巫小屋 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证：门 2、楼层 2 支持居住 |
| REF-0047 | 宁静港湾 | Unknown | low | Vehicle | medium | existing metadata | unknown@0.2 | transport | transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0048 | 守卫塔 | Unknown | low | Tower | medium | mixed | unknown@0.2 | military | military+tower → Tower；几何交叉验证：height_ratio=2.00 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0049 | 小公园橡树 | Unknown | low | Decoration | medium | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0050 | 小镇市政厅 | Medieval | medium | Civic | medium | mixed | medieval@0.64 | civic | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=civic（含 arena，公共集会） |
| REF-0051 | 小雪人 | Unknown | low | Decoration | low | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0052 | 山川高塔 | Unknown | low | Tower | high | mixed | unknown@0.2 | landmark | landmark+tower → Tower；几何交叉验证：height_ratio=4.04 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0053 | 巨型云杉塔 | Unknown | low | Tower | high | mixed | unknown@0.2 | landmark | landmark+tower → Tower；几何交叉验证：height_ratio=2.30 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0054 | 帆船_小_红白色_二 | Unknown | low | Vehicle | medium | existing metadata | unknown@0.2 | transport | transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0055 | 平原晶塔 | Fantasy | high | Tower | high | mixed | fantasy@0.72 | landmark | landmark+tower → Tower；几何交叉验证：height_ratio=4.44 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0056 | 幻想风蓝色飞艇 | Fantasy | high | Vehicle | medium | existing metadata | fantasy@0.72 | transport | transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0057 | 开花巨树一_大 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0058 | 开花巨树二_大 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0059 | 德鲁伊小屋 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证：门 8、楼层 1 支持居住 |
| REF-0060 | 拉面馆 | Unknown | low | Workshop | medium | existing metadata | unknown@0.2 | commercial | commercial+shop/market → Workshop（零售并入作坊，记录在案） |
| REF-0061 | 摆摊 | Unknown | low | Workshop | medium | existing metadata | unknown@0.2 | commercial | commercial+shop/market → Workshop（零售并入作坊，记录在案） |
| REF-0062 | 教堂_二 | Medieval | medium | Religious | high | mixed | medieval@0.64 | religious | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=religious |
| REF-0063 | 斗兽场 | Other | high | Civic | high | existing metadata | classical@0.78 | civic | V6C2 tag=classical 映射 Other（候选类不细分）；primary_use=civic（含 arena，公共集会） |
| REF-0064 | 旋风忍术修道院 | Unknown | low | Religious | high | existing metadata | unknown@0.2 | religious | primary_use=religious |
| REF-0065 | 日式仓库 | Japanese | high | Warehouse | high | mixed | japanese@0.72 | industrial | 几何交叉验证：stair_count=107，屋顶构件存在；industrial+warehouse → Warehouse |
| REF-0066 | 日式宝塔 | Japanese | high | Tower | medium | mixed | japanese@0.72 | landmark | 几何交叉验证：stair_count=1436，屋顶构件存在；landmark+tower → Tower；几何交叉验证弱支持：height_ratio=1.20 <1.65 |
| REF-0067 | 日式宫殿 | Japanese | high | Castle | high | mixed | japanese@0.72 | landmark | 几何交叉验证：stair_count=3398，屋顶构件存在；landmark+palace → Castle（纪念性大型建筑群并入，记录在案）；几何交叉验证：石质主体支持 |
| REF-0068 | 日式寺院 | Japanese | high | Religious | high | mixed | japanese@0.72 | religious | 几何交叉验证：stair_count=653，屋顶构件存在；primary_use=religious |
| REF-0069 | 日式门楼 | Japanese | high | Gate | medium | mixed | japanese@0.72 | military | 几何交叉验证：stair_count=1100，屋顶构件存在；military+gatehouse/wall → Gate |
| REF-0070 | 晶化木屋 | Fantasy | high | Residential | medium | mixed | fantasy@0.72 | residential | primary_use=residential；几何交叉验证弱支持：门 9、楼层 UNKNOWN 信号弱 |
| REF-0071 | 月宫 | Chinese | high | Castle | high | mixed | chinese@0.72 | landmark | 几何交叉验证：stair_count=780，屋顶构件存在；landmark+palace → Castle（纪念性大型建筑群并入，记录在案）；几何交叉验证：石质主体支持 |
| REF-0072 | 杜鹃花树_普通_十一 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0073 | 林中地精小屋 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证：门 2、楼层 1 支持居住 |
| REF-0074 | 森林观测塔 | Unknown | low | Tower | high | mixed | unknown@0.2 | landmark | landmark+tower → Tower；几何交叉验证：height_ratio=2.00 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0075 | 樱花日式民家 | Rustic | medium | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证弱支持：木石占比与特征均不明显；primary_use=residential；几何交叉验证弱支持：门 0、楼层 1 信号弱 |
| REF-0076 | 樱花町屋 | Unknown | low | Residential | medium | mixed | japanese@0.48 | residential | V6C2 top style=japanese 置信度 0.48 低于 0.55，降级 Unknown；primary_use=residential；几何交叉验证弱支持：门 0、楼层 UNKNOWN 信号弱 |
| REF-0077 | 欧式酒馆 | Other | high | Inn | medium | existing metadata | european@0.72 | commercial | V6C2 tag=european 映射 Other（候选类不细分）；commercial+tavern/inn → Inn |
| REF-0078 | 水之庄园 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 2、楼层 2 支持居住 |
| REF-0079 | 水池小凉亭 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0080 | 池塘樱花树 | Unknown | low | Unknown | low | existing metadata | unknown@0.2 | unknown | primary_use=unknown 或无证据 |
| REF-0081 | 沙漠建筑_射箭场 | Other | high | Mixed-use | medium | existing metadata | desert@0.72 | mixed_use | V6C2 tag=desert 映射 Other（候选类不细分）；primary_use=mixed_use |
| REF-0082 | 沙漠建筑_铁匠铺 | Other | high | Blacksmith | medium | existing metadata | desert@0.72 | industrial | V6C2 tag=desert 映射 Other（候选类不细分）；industrial+blacksmith → Blacksmith |
| REF-0083 | 沼泽地村庄 | Medieval | medium | Unknown | low | mixed | medieval@0.64 | unknown | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=unknown 或无证据 |
| REF-0084 | 沼泽城 | Unknown | low | Unknown | low | existing metadata | unknown@0.2 | unknown | primary_use=unknown 或无证据 |
| REF-0085 | 法师居所 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 2、楼层 1 支持居住 |
| REF-0086 | 法术学院 | Fantasy | high | Civic | medium | existing metadata | fantasy@0.72 | civic | primary_use=civic（含 arena，公共集会） |
| REF-0087 | 泰姬陵 | Unknown | low | Castle | high | mixed | unknown@0.2 | landmark | landmark+palace → Castle（纪念性大型建筑群并入，记录在案）；几何交叉验证：石质主体支持 |
| REF-0088 | 海晶石白色小教堂 | Unknown | low | Religious | medium | existing metadata | unknown@0.2 | religious | primary_use=religious |
| REF-0089 | 深板岩地狱门 | Unknown | low | Decoration | medium | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0090 | 深板岩城堡 | Medieval | high | Castle | high | mixed | fortified@0.8 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0091 | 灰熊要塞 | Medieval | medium | Castle | medium | mixed | medieval@0.64 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0092 | 玫瑰堡 | Fantasy | high | Residential | high | mixed | fantasy@0.8 | residential | primary_use=residential；几何交叉验证：门 9、楼层 1 支持居住 |
| REF-0093 | 白塔天守阁 | Japanese | high | Castle | medium | mixed | japanese@0.72 | military | 几何交叉验证：stair_count=1018，屋顶构件存在；military+castle/keep → Castle；几何交叉验证弱支持：石质占比不高 |
| REF-0094 | 白桦木商铺 | Rustic | high | Workshop | medium | mixed | rustic@0.79 | commercial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；commercial+shop/market → Workshop（零售并入作坊，记录在案） |
| REF-0095 | 白桦树_中_三 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0096 | 白色沙漠小帐篷 | Unknown | low | Decoration | high | existing metadata | desert@0.48 | landscape | V6C2 top style=desert 置信度 0.48 低于 0.55，降级 Unknown；landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0097 | 监守者地狱门 | Unknown | low | Decoration | low | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0098 | 石质小教堂 | Unknown | low | Religious | medium | existing metadata | unknown@0.2 | religious | primary_use=religious |
| REF-0099 | 石质教堂 | Unknown | low | Religious | high | existing metadata | unknown@0.2 | religious | primary_use=religious |
| REF-0100 | 秘境药师 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证：门 1、楼层 1 支持居住 |
| REF-0101 | 童话花园地块 | Fantasy | high | Decoration | medium | existing metadata | fantasy@0.72 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0102 | 精灵领袖之树 | Fantasy | high | Residential | medium | mixed | fantasy@0.86 | residential | primary_use=residential；几何交叉验证弱支持：门 0、楼层 1 信号弱 |
| REF-0103 | 糖果城堡 | Unknown | low | Castle | medium | mixed | unknown@0.2 | military | military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0104 | 红白小宫殿 | Unknown | low | Castle | high | mixed | unknown@0.2 | landmark | landmark+palace → Castle（纪念性大型建筑群并入，记录在案）；几何交叉验证：石质主体支持 |
| REF-0105 | 绞刑架 | Unknown | low | Decoration | medium | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0106 | 羽蛇神雕像 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0107 | 茶坊 | Rustic | high | Inn | medium | mixed | rustic@0.79 | commercial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；commercial+tavern/inn → Inn |
| REF-0108 | 菲木静居 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证弱支持：门 10、楼层 UNKNOWN 信号弱 |
| REF-0109 | 蔓生精灵庄园 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证弱支持：门 0、楼层 2 信号弱 |
| REF-0110 | 观星者月宿 | Unknown | low | Unknown | low | existing metadata | unknown@0.2 | unknown | primary_use=unknown 或无证据 |
| REF-0111 | 许愿之塔 | Medieval | medium | Tower | high | mixed | medieval@0.64 | landmark | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；landmark+tower → Tower；几何交叉验证：height_ratio=2.87 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0112 | 诡异菌树_五 | Unknown | low | Decoration | high | existing metadata | unknown@0.2 | landscape | landscape（tree/garden/pavilion 等景观）→ Decoration |
| REF-0113 | 象牙城堡 | Medieval | high | Castle | high | mixed | fortified@0.8 | military | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；military+castle/keep → Castle；几何交叉验证：石质主体支持 |
| REF-0114 | 运输空港 | Unknown | low | Vehicle | medium | existing metadata | unknown@0.2 | transport | transport（ship/airship/dock）→ 新增类 Vehicle |
| REF-0115 | 部落巢穴 | Unknown | low | Residential | medium | mixed | unknown@0.2 | residential | primary_use=residential；几何交叉验证弱支持：门 0、楼层 1 信号弱 |
| REF-0116 | 钟楼_二 | Medieval | medium | Unknown | low | mixed | medieval@0.64 | unknown | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=unknown 或无证据 |
| REF-0117 | 闪长岩安山岩棺椁 | Unknown | low | Decoration | medium | existing metadata | unknown@0.2 | landmark | landmark（statue/portal/mausoleum 等纪念物）→ Decoration |
| REF-0118 | 阿特拉斯护腕之塔 | Medieval | medium | Tower | medium | mixed | medieval@0.64 | landmark | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；landmark+tower → Tower；几何交叉验证弱支持：height_ratio=1.18 <1.65 |
| REF-0119 | 风车房 | Rustic | high | Workshop | medium | mixed | rustic@0.79 | industrial | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；industrial（生产建筑）→ Workshop |
| REF-0120 | 高等精灵之塔 | Fantasy | high | Tower | high | mixed | fantasy@0.72 | landmark | landmark+tower → Tower；几何交叉验证：height_ratio=2.46 ≥1.65（V6C2 tower 规则同阈值） |
| REF-0121 | 魔幻中世纪小屋 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证弱支持：门 1、楼层 UNKNOWN 信号弱 |
| REF-0122 | 魔法空岛小屋 | Rustic | high | Residential | medium | mixed | rustic@0.79 | residential | 几何交叉验证：木石主导或 timber_frame/stone_base 特征支持；primary_use=residential；几何交叉验证：门 3、楼层 1 支持居住 |
| REF-0123 | 江户后期京都呉服商町家院落 | Japanese | high | Mixed-use | high | mixed | japanese@1.0 | mixed_use | 几何交叉验证：stair_count=1488，屋顶构件存在；primary_use=mixed_use |
