/**
 * 步骤3 厅堂楼阁：远香堂（四面厅·主厅）、卅六鸳鸯馆（西园主厅）、
 * 见山楼（两层楼阁，池西北临水）、秫香馆（东区厅堂）、玲珑馆（枇杷园内）。
 * 附：远香堂南临水平台与台阶。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 厅堂, 栏杆带 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业();

// ── 远香堂：25×11 四面厅，歇山顶，坐北朝南临水 ──
厅堂(J, -20, -62, 12, 5, { 四面: true, 门向: 'south' });
// 南临水平台（鉴石平台）：x -28..-12, z -53..-47
J.盒(-28, 地面 - 1, -53, -12, 地面 - 1, -47, M.台基);
const 平台栏 = [];
for (let x = -28; x <= -12; x++) 平台栏.push([x, -47]);       // 南缘临水栏干
for (let z = -53; z <= -47; z++) { 平台栏.push([-28, z]); 平台栏.push([-12, z]); }
栏杆带(J, 平台栏, 地面);
// 平台入口留在 z=-53 与台基相接处；台基南缘阶石
for (let x = -22; x <= -19; x++) J.放(x, 地面 - 1, -55, 'minecraft:stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]');

// ── 卅六鸳鸯馆：15×11 封闭厅，西园中部 ──
厅堂(J, -89, 28, 7, 5, { 门向: 'south' });

// ── 见山楼：11×9 两层楼阁，池西北临水 ──
厅堂(J, -64, -40, 5, 4, { 门向: 'south', 楼: true });

// ── 秫香馆：13×9 封闭厅，东区 ──
厅堂(J, 62, -40, 6, 4, { 门向: 'south' });

// ── 玲珑馆：9×7 小厅，枇杷园内 ──
厅堂(J, 50, 54, 4, 3, { 门向: 'west' });

// ── 自检采样 ──
const 玻璃X = 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]';
const samples = [
  [-20, 地面 - 1, -62, 'minecraft:stone_bricks'],   // 远香堂台基
  [-19, 地面 + 1, -67, 玻璃X],                       // 北檐长窗（z1=-67）
  [-32, 地面, -67, 'minecraft:dark_oak_log[axis=y]'], // 西北角柱
  [-20, 地面, -57, 'minecraft:air'],                 // 南门洞（z2=-57）
  [-91, 地面, 23, 'minecraft:white_concrete'],       // 鸳鸯馆北墙（非柱非窗）
  [-64, 地面 + 6, -36, 玻璃X],                       // 见山楼二层南窗
  [61, 地面 + 3, -36, 'minecraft:white_concrete'],   // 秫香馆墙顶（非柱位）
  [50, 地面 - 1, 54, 'minecraft:stone_bricks'],      // 玲珑馆台基
];
// 屋面抽查：远香堂檐口（y=68, 悬挑后南檐线 z=-62+7=-55+? 以 eave hz+2=7 → 南檐 z=-62+7=-55）
samples.push([-20, 地面 + 4, -55, 'minecraft:deepslate_tile_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]']);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 100, z1: -84, z2: 84, y1: 63, y2: 78 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤3.json'), JSON.stringify(job));
console.log('步骤3 ops=', J.operations.length, 'palette=', J.palette.length);
