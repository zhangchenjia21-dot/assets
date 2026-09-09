/**
 * 步骤5 游廊桥梁：入口—枇杷园曲廊、南岸曲廊、西园水廊、小飞虹廊桥（西端湾）、
 * 曲桥 A（东岛—南岸）、曲桥 B（西岛—北岸）、小沧浪水院（水渠+小池）与石拱桥。
 * 附：留听阁（西园配厅，门朝东）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 水面, 池底, 厅堂, 游廊, 曲桥, 石拱桥, 随机 } from './园林库.mjs';
import { 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业();

// ── 留听阁（西园，门朝东向月洞门方向）──
厅堂(J, -90, -10, 4, 3, { 门向: 'east' });

// ── 游廊 ──
游廊(J, [[78, 80], [36, 80], [36, 58], [34, 58]]);        // A：入口→枇杷园月洞门
游廊(J, [[-48, 30], [-20, 30], [0, 30], [8, 30], [8, 44]]); // B：南岸曲廊→听雨轩外
游廊(J, [[-80, 20], [-80, -28], [-78, -28]]);             // C：西园水廊→近月洞门
游廊(J, [[-72, -30], [-72, -18]]);                        // 小飞虹廊桥（贴墙跨水）

// ── 曲桥 ──
曲桥(J, [[-8, -7], [-8, 6], [-12, 6], [-12, 22]]);        // A：东岛—南岸
曲桥(J, [[-40, -10], [-40, -28], [-36, -28], [-36, -44]]); // B：西岛—北岸

// ── 小沧浪水院：引水渠 + 小池 + 石拱桥 ──
const rnd = 随机(77);
const 水院 = (x, z) => (x >= -47 && x <= -45 && z >= 18 && z <= 28) || // 水渠
  (((x + 46) / 6) ** 2 + ((z - 32) / 5) ** 2 <= 1);                    // 小池（中心 -46,32）
for (let x = -54; x <= -38; x++) for (let z = 16; z <= 39; z++) {
  if (!水体(x, z) && 水院(x, z)) {
    J.放(x, 地面 - 1, z, 'minecraft:air');
    for (let y = 水面; y > 池底; y--) J.放(x, y, z, M.水);
    J.放(x, 池底, z, M.黏土);
    J.放(x, 池底 - 1, z, rnd() < 0.3 ? M.碎石 : M.土);
  } else if (!水体(x, z) && (水院(x + 1, z) || 水院(x - 1, z) || 水院(x, z + 1) || 水院(x, z - 1))) {
    // 水院岸线
    const 石 = [M.驳岸, M.湖石2, M.湖石1][Math.floor(rnd() * 3)];
    J.放(x, 地面 - 1, z, 石);
  }
}
石拱桥(J, 25, -50, -42, 'x', 3, 2); // 跨渠：z=25，x -50..-42

const samples = [
  [60, 地面 - 1, 80, 'minecraft:stone_bricks'],   // 廊A地面
  [60, 地面 + 5, 80, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 廊A脊板（底64+柱高3+脊2=69）
  [-8, 地面 - 1, 0, 'minecraft:stone_slab[type=bottom,waterlogged=false]'],  // 曲桥A桥面
  [-72, 地面 - 1, -24, 'minecraft:stone_bricks'], // 小飞虹廊桥板
  [-46, 地面 + 1, 25, 'minecraft:stone_bricks'],  // 石拱桥拱顶（底63+矢2）
  [-46, 水面, 22, 'minecraft:water[level=0]'],    // 水渠通池
  [-90, 地面, -7, 'minecraft:white_concrete'],    // 留听阁南墙（z2=-7）
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 100, z1: -84, z2: 84, y1: 63, y2: 72 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤5.json'), JSON.stringify(job));
console.log('步骤5 ops=', J.operations.length, 'palette=', J.palette.length);
