/**
 * 步骤7 桥梁：曲桥①（岛A南 → 涵碧堂月台北缘缺口）、曲桥②（岛A北 → 北岸步道）、
 * 石拱①（岛C东 → 东岸，矢高3）、石拱②（跨活泼泼地溪，衔接北岸-西岸廊断口）。
 * 曲桥为石梁平桥（桥脚落水），石拱为砖拱（栏板随拱起伏、两端踏步）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, 曲桥, 石拱桥 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();

// 曲桥①：岛A南缘 (-38,2) 三折 → 月台北缘 (-16,46)
曲桥(J, [[-38, 2], [-38, 14], [-24, 14], [-24, 26], [-12, 26], [-12, 40], [-16, 40], [-16, 46]]);
// 曲桥②：岛A北缘 (-38,-14) 两折 → 北岸步道 (-24,-44)
曲桥(J, [[-38, -14], [-38, -26], [-30, -26], [-30, -40], [-24, -40], [-24, -44]]);
// 石拱①：岛C东 (21,-30) → 东岸 (40,-30)
石拱桥(J, -30, 21, 40, 'x', 3, 3);
// 石拱②：跨活泼泼地溪 (-96, z-46..-38)
石拱桥(J, -96, -46, -38, 'z', 3, 3);

// ── 自检采样 ──
const samples = [
  [-38, 63, 14, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥①面
  [-30, 63, -40, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥②面
  [-30, 62, -40, 'minecraft:stone'],                                     // 曲桥②水中桥脚
  [30, 66, -30, 'minecraft:stone_bricks'],                               // 石拱①拱顶
  [40, 63, -30, 'minecraft:stone_bricks'],                               // 石拱①东端桥头（s=长 末端台面）
  [-96, 66, -42, 'minecraft:stone_bricks'],                              // 石拱②拱顶
];
J.校对(samples);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 45, z1: -55, z2: 50, y1: 59, y2: 70 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤7.json'), JSON.stringify(job));
console.log('步骤7 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
