/**
 * 步骤10 全园终验（零施工）：四象限只读扫描 + 关键构件回读。
 * 产出 施工/步骤10a~d.json（无 phases，仅 samples+scan），
 * 由 scripts/检查.mjs 汇总解码：水面不变量 + 动线洪泛连通 + 全景顶视图。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';

const 象限 = {
  a西北: {
    scan: { x1: -141, x2: 0, z1: -121, z2: 0, y1: 56, y2: 92 },
    samples: [
      [-120, 82, 66, 'minecraft:dark_oak_log[axis=y]'],   // 卧云亭角柱
      [-118, 74, -33, 'minecraft:dark_oak_log[axis=y]'],  // 至乐亭角柱（cx±3）
      [-30, 64, 52, 'minecraft:dark_oak_log[axis=y]'],    // 涵碧堂檐柱
      [-20, 63, 48, 'minecraft:stone_bricks'],            // 月台
      [-30, 63, -40, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥②面
      [-78, 63, -48, 'minecraft:stone_bricks'],           // 廊桥中亭平台
      [-20, 62, -20, 'minecraft:water[level=0]'],         // 主池水面
      [-118, 81, 68, 'minecraft:stone_bricks'],           // 假山峰顶平台
      [-109, 64, 60, 'minecraft:air'],                    // 山洞内室
    ],
  },
  b东北: {
    scan: { x1: 1, x2: 141, z1: -121, z2: 0, y1: 56, y2: 92 },
    samples: [
      [-24, 68, -59, 'minecraft:dark_oak_log[axis=y]'],   // 远翠阁二层檐柱（局部在 x≤0 侧，采 x=1 以东其余构件）
      [71, 64, -15, 'minecraft:dark_oak_log[axis=y]'],    // 五峰仙馆檐柱
      [91, 64, 12, 'minecraft:dark_oak_log[axis=y]'],     // 揖峰轩檐柱
      [118, 65, -32, 'minecraft:tuff'],                   // 冠云峰实心基段（选石公式=tuff）
      [47, 64, -95, 'minecraft:dark_oak_log[axis=y]'],    // 茅亭角柱
      [-20, 64, -72, 'minecraft:white_concrete'],         // 北部花墙身（局部 x<1，此点 x=-20 仅作跨区回读）
    ],
  },
  c西南: {
    scan: { x1: -141, x2: 0, z1: 1, z2: 121, y1: 56, y2: 92 },
    samples: [
      [-108, 66, 78, 'minecraft:light_gray_concrete'],    // 假山次峰岩体（选石公式）
      [-111, 71, 5, 'minecraft:dark_oak_log[axis=y]'],    // 舒啸亭角柱
      [-96, 63, 16, 'minecraft:stone_bricks'],            // 石舫甲板
      [-60, 63, 46, 'minecraft:stone_bricks'],            // 南岸步道石板
      [-16, 65, 64, 'minecraft:air'],                     // 涵碧堂南门
      [-72, 63, -26, 'minecraft:stone_bricks'],           // 观鱼亭台基（岛B 西北角）
    ],
  },
  d东南: {
    scan: { x1: 1, x2: 141, z1: 1, z2: 121, y1: 56, y2: 92 },
    samples: [
      [23, 65, 52, 'minecraft:air'],                      // 绿荫轩东门
      [62, 65, 22, 'minecraft:white_concrete'],           // 林泉馆墙身
      [104, 66, 95, 'minecraft:air'],                     // 小院月洞门
      [116, 65, 120, 'minecraft:air'],                    // 园门洞
      [112, 63, 115, 'minecraft:stone_bricks'],           // 门厅台基前檐（石砖）
      [60, 63, -10, 'minecraft:stone_bricks'],            // 东部联系廊面（跨 z<1 回读）
    ],
  },
};

for (const [名, q] of Object.entries(象限)) {
  const job = { world_path: 世界, phases: [], samples: q.samples, scan: q.scan };
  const 出 = path.join(根, '..', '施工', `步骤10${名[0]}.json`);
  fs.writeFileSync(出, JSON.stringify(job));
  console.log('已生成', 出, 'samples=', q.samples.length);
}
