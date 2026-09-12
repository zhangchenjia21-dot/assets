# BLUEPRINT_MANIFEST — 参考蓝图全量清单

- 蓝图总数：**123**
- 数据来源：`references\catalog\catalog.json`（OBSERVED，只读）
- 生成脚本：`scripts/build_manifest.py`
- 字段说明：尺寸为 `x×y×z`（方块格）；style tags 来自 catalog 的 `styles`（tag:confidence），仅列出置信度 ≥0.5 的标签。

| ref_id | 文件名 | 名称 | 尺寸 (x×y×z) | block_count | compatibility | primary_use | style tags |
|---|---|---|---|---|---|---|---|
| REF-0001 | 丁香树坛 | 丁香树坛 | 14×15×15 | 555 | LEGACY_SAFE | landscape | — |
| REF-0002 | 世界之塔 | 世界之塔 | 55×124×52 | 19651 | LEGACY_SAFE | landmark | medieval:0.64 |
| REF-0003 | 中世纪农舍 | 中世纪农舍 | 15×14×19 | 1387 | LEGACY_SAFE | residential | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0004 | 中世纪四层小屋 | 中世纪四层小屋 | 21×21×23 | 2440 | MIGRATED | residential | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0005 | 中世纪大门守卫房 | 中世纪大门守卫房 | 17×32×48 | 2442 | LEGACY_SAFE | military | medieval:0.64 |
| REF-0006 | 中世纪工具匠铺 | 中世纪工具匠铺 | 25×21×29 | 3654 | MIGRATED | industrial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0007 | 中世纪工坊 | 中世纪工坊 | 34×26×31 | 4381 | MIGRATED | industrial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0008 | 中世纪异世界酒馆 | 中世纪异世界酒馆 | 31×26×31 | 5608 | MIGRATED | commercial | medieval:0.64, rustic:0.79, cottage:0.69, fantasy:0.72 |
| REF-0009 | 中世纪据点_小 | 中世纪据点_小 | 63×49×51 | 28442 | LEGACY_SAFE | military | fortified:0.80, medieval:0.72 |
| REF-0010 | 中世纪海港小屋 | 中世纪海港小屋 | 19×26×16 | 2203 | LEGACY_SAFE | residential | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0011 | 中世纪酒馆_二 | 中世纪酒馆_二 | 57×51×54 | 12576 | MIGRATED | commercial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0012 | 中世纪酿酒厂 | 中世纪酿酒厂 | 42×46×67 | 13062 | MIGRATED | industrial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0013 | 中世纪门楼 | 中世纪门楼 | 47×63×51 | 9587 | MIGRATED | military | medieval:0.64 |
| REF-0014 | 中世纪面包房 | 中世纪面包房 | 71×69×63 | 17839 | MIGRATED | industrial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0015 | 中式塔楼 | 中式塔楼 | 21×49×21 | 4877 | LEGACY_SAFE | landmark | chinese:0.72, east_asian:0.72 |
| REF-0016 | 中式小亭 | 中式小亭 | 21×27×22 | 751 | MIGRATED | landscape | — |
| REF-0017 | 中式灯笼路灯 | 中式灯笼路灯 | 3×10×7 | 34 | MIGRATED | unknown | — |
| REF-0018 | 中式青蛇飞艇 | 中式青蛇飞艇 | 19×20×35 | 1101 | MIGRATED | transport | chinese:0.72, east_asian:0.72 |
| REF-0019 | 云杉树_中_三 | 云杉树_中_三 | 16×45×15 | 1603 | LEGACY_SAFE | landscape | — |
| REF-0020 | 伦布里奇要塞 | 伦布里奇要塞 | 67×23×58 | 10318 | LEGACY_SAFE | military | fortified:0.80 |
| REF-0021 | 八角塔 | 八角塔 | 63×98×77 | 19009 | LEGACY_SAFE | landmark | medieval:0.64 |
| REF-0022 | 六角亭 | 六角亭 | 37×32×35 | 4013 | LEGACY_SAFE | landscape | — |
| REF-0023 | 农田_一 | 农田_一 | 9×10×22 | 318 | LEGACY_SAFE | agricultural | — |
| REF-0024 | 冥界之门 | 冥界之门 | 74×63×66 | 14557 | MIGRATED | landmark | fantasy:0.72 |
| REF-0025 | 利登赛特要塞 | 利登赛特要塞 | 44×39×52 | 11261 | LEGACY_SAFE | military | fortified:0.80 |
| REF-0026 | 利维坦号 | 利维坦号 | 192×187×110 | 61591 | MIGRATED | transport | — |
| REF-0027 | 剑士工会 | 剑士工会 | 51×48×55 | 11341 | MIGRATED | civic | medieval:0.64 |
| REF-0028 | 南瓜屋 | 南瓜屋 | 50×79×101 | 58123 | MIGRATED | residential | — |
| REF-0029 | 双人农田木屋 | 双人农田木屋 | 23×12×23 | 1218 | MIGRATED | agricultural | — |
| REF-0030 | 双层L型农田木屋 | 双层L型农田木屋 | 36×17×33 | 2954 | LEGACY_SAFE | agricultural | medieval:0.64 |
| REF-0031 | 双羽木飞船 | 双羽木飞船 | 35×34×92 | 10581 | LEGACY_SAFE | transport | — |
| REF-0032 | 哈利卡纳苏斯陵墓 | 哈利卡纳苏斯陵墓 | 122×60×170 | 69320 | LEGACY_SAFE | landmark | — |
| REF-0033 | 哨塔_小 | 哨塔_小 | 9×15×9 | 340 | LEGACY_SAFE | military | medieval:0.64 |
| REF-0034 | 唐屋_大 | 唐屋_大 | 93×43×84 | 36818 | LEGACY_SAFE | landmark | chinese:0.72, east_asian:0.72 |
| REF-0035 | 唐屋_小 | 唐屋_小 | 44×21×26 | 5080 | LEGACY_SAFE | landmark | — |
| REF-0036 | 四兵器铁匠铺 | 四兵器铁匠铺 | 134×71×164 | 59962 | MIGRATED | industrial | — |
| REF-0037 | 圣亨格勒大教堂 | 圣亨格勒大教堂 | 53×51×37 | 8160 | LEGACY_SAFE | religious | european:0.72 |
| REF-0038 | 圣埃德大教堂 | 圣埃德大教堂 | 53×80×75 | 30538 | LEGACY_SAFE | religious | medieval:0.64, european:0.72 |
| REF-0039 | 圣彼得里教堂_德国汉堡 | 圣彼得里教堂_德国汉堡 | 62×108×83 | 24852 | LEGACY_SAFE | religious | european:0.72 |
| REF-0040 | 地中海岛屿小屋 | 地中海岛屿小屋 | 73×71×75 | 31100 | MIGRATED | residential | — |
| REF-0041 | 壁炉小屋 | 壁炉小屋 | 44×42×52 | 10236 | MIGRATED | residential | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0042 | 大圣诞树 | 大圣诞树 | 23×96×23 | 4934 | LEGACY_SAFE | landscape | — |
| REF-0043 | 大型中世纪酒馆 | 大型中世纪酒馆 | 36×57×73 | 13341 | MIGRATED | commercial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0044 | 大型奇幻农舍 | 大型奇幻农舍 | 57×37×56 | 16035 | MIGRATED | residential | medieval:0.64, fantasy:0.72 |
| REF-0045 | 大教堂 | 大教堂 | 133×53×76 | 43192 | LEGACY_SAFE | religious | — |
| REF-0046 | 女巫小屋 | 女巫小屋 | 38×50×50 | 6636 | MIGRATED | residential | — |
| REF-0047 | 宁静港湾 | 宁静港湾 | 46×47×53 | 5451 | LEGACY_SAFE | transport | — |
| REF-0048 | 守卫塔 | 守卫塔 | 18×36×18 | 1779 | MIGRATED | military | — |
| REF-0049 | 小公园橡树 | 小公园橡树 | 21×16×21 | 1037 | LEGACY_SAFE | landscape | — |
| REF-0050 | 小镇市政厅 | 小镇市政厅 | 61×30×52 | 15149 | MIGRATED | civic | medieval:0.64 |
| REF-0051 | 小雪人 | 小雪人 | 7×9×7 | 106 | LEGACY_SAFE | landmark | — |
| REF-0052 | 山川高塔 | 山川高塔 | 19×101×25 | 7083 | MIGRATED | landmark | — |
| REF-0053 | 巨型云杉塔 | 巨型云杉塔 | 53×122×52 | 43598 | LEGACY_SAFE | landmark | — |
| REF-0054 | 帆船_小_红白色_二 | 帆船_小_红白色_二 | 21×21×7 | 500 | LEGACY_SAFE | transport | — |
| REF-0055 | 平原晶塔 | 平原晶塔 | 9×40×9 | 577 | MIGRATED | landmark | fantasy:0.72 |
| REF-0056 | 幻想风蓝色飞艇 | 幻想风蓝色飞艇 | 99×121×154 | 42602 | LEGACY_SAFE | transport | fantasy:0.72 |
| REF-0057 | 开花巨树一_大 | 开花巨树一_大 | 97×98×62 | 25771 | LEGACY_SAFE | landscape | — |
| REF-0058 | 开花巨树二_大 | 开花巨树二_大 | 69×58×98 | 14573 | LEGACY_SAFE | landscape | — |
| REF-0059 | 德鲁伊小屋 | 德鲁伊小屋 | 48×59×55 | 11061 | MIGRATED | residential | — |
| REF-0060 | 拉面馆 | 拉面馆 | 21×22×19 | 1565 | MIGRATED | commercial | — |
| REF-0061 | 摆摊 | 摆摊 | 11×4×5 | 69 | LEGACY_SAFE | commercial | — |
| REF-0062 | 教堂_二 | 教堂_二 | 82×68×51 | 15283 | MIGRATED | religious | medieval:0.64 |
| REF-0063 | 斗兽场 | 斗兽场 | 55×25×50 | 11518 | LEGACY_SAFE | civic | classical:0.78 |
| REF-0064 | 旋风忍术修道院 | 旋风忍术修道院 | 74×39×76 | 16212 | MIGRATED | religious | — |
| REF-0065 | 日式仓库 | 日式仓库 | 24×18×20 | 2469 | LEGACY_SAFE | industrial | japanese:0.72, east_asian:0.72 |
| REF-0066 | 日式宝塔 | 日式宝塔 | 47×60×50 | 12926 | MIGRATED | landmark | japanese:0.72, east_asian:0.72 |
| REF-0067 | 日式宫殿 | 日式宫殿 | 68×48×72 | 35203 | LEGACY_SAFE | landmark | japanese:0.72, east_asian:0.72 |
| REF-0068 | 日式寺院 | 日式寺院 | 42×37×94 | 10844 | LEGACY_SAFE | religious | japanese:0.72, east_asian:0.72 |
| REF-0069 | 日式门楼 | 日式门楼 | 67×51×34 | 13873 | MIGRATED | military | japanese:0.72, east_asian:0.72 |
| REF-0070 | 晶化木屋 | 晶化木屋 | 51×81×75 | 13648 | MIGRATED | residential | fantasy:0.72 |
| REF-0071 | 月宫 | 月宫 | 69×68×73 | 13390 | LEGACY_SAFE | landmark | chinese:0.72, east_asian:0.72 |
| REF-0072 | 杜鹃花树_普通_十一 | 杜鹃花树_普通_十一 | 14×18×14 | 813 | LEGACY_SAFE | landscape | — |
| REF-0073 | 林中地精小屋 | 林中地精小屋 | 47×23×40 | 6300 | LEGACY_SAFE | residential | — |
| REF-0074 | 森林观测塔 | 森林观测塔 | 22×44×19 | 3986 | MIGRATED | landmark | — |
| REF-0075 | 樱花日式民家 | 樱花日式民家 | 70×37×78 | 13478 | LEGACY_SAFE | residential | rustic:0.79, cottage:0.69, japanese:0.72, east_asian:0.72 |
| REF-0076 | 樱花町屋 | 樱花町屋 | 85×82×83 | 12785 | MIGRATED | residential | — |
| REF-0077 | 欧式酒馆 | 欧式酒馆 | 73×74×52 | 17977 | MIGRATED | commercial | medieval:0.64, european:0.72 |
| REF-0078 | 水之庄园 | 水之庄园 | 49×51×63 | 16600 | MIGRATED | residential | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0079 | 水池小凉亭 | 水池小凉亭 | 15×10×18 | 896 | LEGACY_SAFE | landscape | — |
| REF-0080 | 池塘樱花树 | 池塘樱花树 | 21×20×21 | 3197 | LEGACY_SAFE | unknown | — |
| REF-0081 | 沙漠建筑_射箭场 | 沙漠建筑_射箭场 | 22×11×23 | 2205 | LEGACY_SAFE | mixed_use | desert:0.72 |
| REF-0082 | 沙漠建筑_铁匠铺 | 沙漠建筑_铁匠铺 | 16×20×18 | 1685 | LEGACY_SAFE | industrial | desert:0.72 |
| REF-0083 | 沼泽地村庄 | 沼泽地村庄 | 80×39×82 | 54416 | LEGACY_SAFE | unknown | medieval:0.64 |
| REF-0084 | 沼泽城 | 沼泽城 | 118×142×140 | 81085 | MIGRATED | unknown | — |
| REF-0085 | 法师居所 | 法师居所 | 33×63×46 | 6813 | MIGRATED | residential | medieval:0.64, rustic:0.79, cottage:0.69, fantasy:0.72 |
| REF-0086 | 法术学院 | 法术学院 | 72×65×114 | 30913 | LEGACY_SAFE | civic | fantasy:0.72 |
| REF-0087 | 泰姬陵 | 泰姬陵 | 98×46×98 | 25496 | LEGACY_SAFE | landmark | — |
| REF-0088 | 海晶石白色小教堂 | 海晶石白色小教堂 | 15×23×15 | 1181 | LEGACY_SAFE | religious | — |
| REF-0089 | 深板岩地狱门 | 深板岩地狱门 | 6×6×3 | 79 | LEGACY_SAFE | landmark | — |
| REF-0090 | 深板岩城堡 | 深板岩城堡 | 147×133×148 | 99586 | MIGRATED | military | medieval:0.64, fortified:0.80 |
| REF-0091 | 灰熊要塞 | 灰熊要塞 | 66×38×53 | 27904 | LEGACY_SAFE | military | medieval:0.64 |
| REF-0092 | 玫瑰堡 | 玫瑰堡 | 68×51×43 | 9613 | MIGRATED | residential | fantasy:0.80, rustic:0.78 |
| REF-0093 | 白塔天守阁 | 白塔天守阁 | 82×68×79 | 12189 | MIGRATED | military | japanese:0.72, east_asian:0.72 |
| REF-0094 | 白桦木商铺 | 白桦木商铺 | 16×16×23 | 1919 | LEGACY_SAFE | commercial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0095 | 白桦树_中_三 | 白桦树_中_三 | 31×19×27 | 1331 | LEGACY_SAFE | landscape | — |
| REF-0096 | 白色沙漠小帐篷 | 白色沙漠小帐篷 | 7×8×8 | 170 | LEGACY_SAFE | landscape | — |
| REF-0097 | 监守者地狱门 | 监守者地狱门 | 31×23×32 | 2123 | LEGACY_SAFE | landmark | — |
| REF-0098 | 石质小教堂 | 石质小教堂 | 17×22×16 | 1425 | LEGACY_SAFE | religious | — |
| REF-0099 | 石质教堂 | 石质教堂 | 28×52×42 | 6224 | MIGRATED | religious | — |
| REF-0100 | 秘境药师 | 秘境药师 | 50×61×46 | 8805 | MIGRATED | residential | — |
| REF-0101 | 童话花园地块 | 童话花园地块 | 34×24×34 | 8353 | LEGACY_SAFE | landscape | fantasy:0.72 |
| REF-0102 | 精灵领袖之树 | 精灵领袖之树 | 43×55×37 | 7887 | LEGACY_SAFE | residential | fantasy:0.86 |
| REF-0103 | 糖果城堡 | 糖果城堡 | 59×107×57 | 50430 | LEGACY_SAFE | military | — |
| REF-0104 | 红白小宫殿 | 红白小宫殿 | 34×55×43 | 8998 | MIGRATED | landmark | — |
| REF-0105 | 绞刑架 | 绞刑架 | 9×8×9 | 132 | LEGACY_SAFE | landmark | — |
| REF-0106 | 羽蛇神雕像 | 羽蛇神雕像 | 92×110×84 | 21098 | LEGACY_SAFE | landmark | — |
| REF-0107 | 茶坊 | 茶坊 | 46×41×49 | 5365 | MIGRATED | commercial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0108 | 菲木静居 | 菲木静居 | 92×105×107 | 64027 | MIGRATED | residential | — |
| REF-0109 | 蔓生精灵庄园 | 蔓生精灵庄园 | 54×83×81 | 34446 | MIGRATED | residential | rustic:0.79, cottage:0.69, fantasy:0.72 |
| REF-0110 | 观星者月宿 | 观星者月宿 | 39×64×50 | 5539 | LEGACY_SAFE | unknown | — |
| REF-0111 | 许愿之塔 | 许愿之塔 | 30×86×29 | 7942 | LEGACY_SAFE | landmark | medieval:0.64 |
| REF-0112 | 诡异菌树_五 | 诡异菌树_五 | 8×12×9 | 167 | LEGACY_SAFE | landscape | — |
| REF-0113 | 象牙城堡 | 象牙城堡 | 210×160×263 | 1156099 | MIGRATED | military | fortified:0.80 |
| REF-0114 | 运输空港 | 运输空港 | 81×55×84 | 17926 | MIGRATED | transport | — |
| REF-0115 | 部落巢穴 | 部落巢穴 | 45×51×64 | 4789 | MIGRATED | residential | — |
| REF-0116 | 钟楼_二 | 钟楼_二 | 27×56×25 | 3363 | MIGRATED | unknown | medieval:0.64 |
| REF-0117 | 闪长岩安山岩棺椁 | 闪长岩安山岩棺椁 | 8×7×5 | 76 | MIGRATED | landmark | — |
| REF-0118 | 阿特拉斯护腕之塔 | 阿特拉斯护腕之塔 | 40×47×39 | 6325 | LEGACY_SAFE | landmark | medieval:0.64 |
| REF-0119 | 风车房 | 风车房 | 26×25×20 | 1670 | LEGACY_SAFE | industrial | medieval:0.64, rustic:0.79, cottage:0.69 |
| REF-0120 | 高等精灵之塔 | 高等精灵之塔 | 13×32×13 | 1077 | LEGACY_SAFE | landmark | fantasy:0.72 |
| REF-0121 | 魔幻中世纪小屋 | 魔幻中世纪小屋 | 47×49×66 | 15681 | MIGRATED | residential | medieval:0.64, rustic:0.79, cottage:0.69, fantasy:0.72 |
| REF-0122 | 魔法空岛小屋 | 魔法空岛小屋 | 31×116×31 | 8315 | MIGRATED | residential | medieval:0.64, rustic:0.79, cottage:0.69, fantasy:0.72 |
| REF-0123 | 京町家修复 | 江户后期京都呉服商町家院落 | 29×20×74 | 12188 | CURRENT_NATIVE | mixed_use | japanese:1.00, east_asian:1.00 |
