/**
 * 步骤8 总验收：零施工阶段 + 关键构件抽样回读 + 全园扫描（y62..80）。
 * 抽样覆盖：远香堂正脊、笠亭台基、曲桥、石拱桥、月洞门洞、水院、留听阁墙、曲桥A。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, 地面, 水面 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业(); // 空阶段：纯验收

const samples = [
  [-20, 地面 + 9, -62, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 远香堂正脊
  [-58, 地面 + 14, 50, 'minecraft:stone_bricks'],    // 笠亭峰顶台基
  [-40, 地面 - 1, -20, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥B桥面
  [-46, 地面 + 1, 25, 'minecraft:stone_bricks'],     // 石拱桥拱顶
  [-76, 地面, -30, 'minecraft:air'],                 // 西园月洞门洞
  [-46, 水面, 32, 'minecraft:water[level=0]'],       // 小沧浪水院
  [-90, 地面, -7, 'minecraft:white_concrete'],       // 留听阁南墙
  [-12, 地面 - 1, 12, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥A西段
  [-8, 地面 + 4, -14, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 雪香云蔚亭顶
  [88, 地面 + 1, 76, 'minecraft:tuff'],              // 影壁砖雕带
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 100, z1: -84, z2: 84, y1: 62, y2: 80 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤8.json'), JSON.stringify(job));
console.log('步骤8 验收 samples=', samples.length);
