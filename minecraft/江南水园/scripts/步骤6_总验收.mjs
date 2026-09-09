/**
 * 步骤6 总验收：零施工阶段，关键构件抽样回读 + 全园扫描（y62..80），
 * 供 通行检查.mjs 做全园可通行性洪泛复核。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, 地面, 水面 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';
const J = new 作业();

// 复用步骤5中记录的荷盖采样（确定性）
const 步5 = JSON.parse(fs.readFileSync(path.join(根, '..', '施工', '步骤5.json'), 'utf8'));
const 荷样 = 步5.samples.find(s => String(s[3]).includes('lily_pad'));

const samples = [
  [0, 地面 + 9, -6, 'minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]'], // 澄心堂正脊(y73)
  [46, 地面 - 1, -1, 'minecraft:stone_bricks'],  // 涵碧榭台基（入水，未被曲桥覆盖）
  [24, 地面 - 1, -6, 'minecraft:stone_bricks'], // 一镜亭台基
  [4, 地面 - 1, 12, 'minecraft:stone_bricks'],  // 笠亭台基
  [-48, 地面 - 1, -12, 'minecraft:stone_bricks'], // 石舫前甲板
  [0, 地面 - 1, 15, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥A桥面
  [-42, 地面 + 1, -6, 'minecraft:stone_bricks'], // 西屿石拱桥拱顶
  [-52, 地面 + 1, -2, 'minecraft:stone_bricks'], // 连通渠桥拱顶
  [0, 地面 + 5, -30, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 小飞虹脊板
  [-52, 地面 - 1, 10, 'minecraft:stone_bricks'], // 河街石板
  [-8, 地面 - 1, 60, 'minecraft:stone_bricks'],  // 入口花街收边
  [-60, 地面, -44, 'minecraft:air'],             // 河房西过街廊
  [0, 地面, 58, 'minecraft:air'],                // 影壁过道
];
if (荷样) samples.push(荷样);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -64, x2: 64, z1: -64, z2: 64, y1: 62, y2: 80 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤6.json'), JSON.stringify(job));
console.log('步骤6 验收 samples=', samples.length);
