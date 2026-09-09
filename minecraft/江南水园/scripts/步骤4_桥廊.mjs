/**
 * 步骤4 桥廊（可通行性关键）：曲桥×3（南/东/西）、石拱桥（西屿）、小飞虹廊桥、
 * 西水巷石拱桥×4、抄手游廊、芥舟石舫（含跳板码头上岸）。自检含通行洪泛。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 游廊, 曲桥, 石拱桥, 硬山顶, 栏杆带 } from './园林库.mjs';
import { 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';
const J = new 作业();

// ── 曲桥：南岸→湖心 / 东岸→东岛→湖心 / 西岛→湖心 ──
曲桥(J, [[0, 30], [0, 1]]);
曲桥(J, [[50, 4], [33, 4], [33, -2], [8, -2]]);
曲桥(J, [[-25, -6], [-9, -6]]);
// ── 石拱桥：西岸(河街)→西岛 ──
石拱桥(J, -6, -53, -31, 'x', 3, 2);
// ── 小飞虹廊桥：北岸→湖心北 ──
游廊(J, [[0, -34], [0, -13]]);
// ── 抄手游廊：花厅→南岸 ──
游廊(J, [[0, 50], [0, 31]]);
// ── 西水巷石拱桥×4：接通两岸 ──
for (const z of [-30, 2, 32, 50]) 石拱桥(J, z, -59, -53, 'x', 3, 2);

// ── 芥舟石舫（西湾内）：甲板西端靠岸上船，尾舱在东段，南北两缘做舷栏 ──
J.盒(-50, 地面 - 1, -14, -42, 地面 - 1, -8, M.台基); // 甲板 x -50..-42
J.盒(-46, 地面, -13, -42, 地面 + 2, -9, M.梁);       // 尾舱 x -46..-42
J.盒(-45, 地面, -12, -43, 地面 + 2, -10, 'minecraft:air'); // 舱内
J.盒(-46, 地面 + 1, -12, -46, 地面 + 1, -10, 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]'); // 西窗朝前甲板
J.放(-42, 地面, -11, 'minecraft:air'); J.放(-42, 地面 + 1, -11, 'minecraft:air'); // 舱门向东（船头）
硬山顶(J, -44, 地面 + 3, -11, 3, 3, true);
const 舷 = [];
for (let x = -50; x <= -42; x++) { 舷.push([x, -14]); 舷.push([x, -8]); } // 仅南北舷栏，西端留上船口
栏杆带(J, 舷, 地面);

// ── 河房西改过街楼：沿西岸步道开南北穿行廊 ──
for (const cz of [-44, 34]) for (let x = -61; x <= -60; x++) for (let z = cz - 2; z <= cz + 2; z++) for (let y = 地面; y <= 地面 + 2; y++) J.放(x, y, z, 'minecraft:air');

// ── 连通渠桥 & 南岛汀步 & 门槛石校正 ──
石拱桥(J, -53, -5, 1, 'z', 3, 2);          // 跨连通渠，接通两岸河街
for (let z = 25; z >= 14; z--) J.放(3, 63, z, 'minecraft:stone_slab[type=bottom,waterlogged=false]'); // 南岛汀步（1宽，无栏）
for (const x of [-1, 0, 1]) { J.放(x, 63, 63, M.地面砖); J.放(x, 64, 63, 'minecraft:air'); } // 过门石放平（y63），与地面同层

// ── 河街栏杆在桥口/河房门处开缺口（保证上下桥与入户）──
for (const z of [-30, 2, 32, 50]) { J.放(-53, 地面, z, 'minecraft:air'); J.放(-59, 地面, z, 'minecraft:air'); } // 水巷桥两端
for (const z of [-45, -44, -43, 33, 34, 35]) J.放(-59, 地面, z, 'minecraft:air'); // 西岸河房门

const samples = [
  [0, 地面 - 1, 15, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥A桥面（水面）
  [26, 地面 - 1, -2, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 曲桥B穿东岛
  [-42, 地面 + 1, -6, 'minecraft:stone_bricks'],  // 石拱桥拱顶
  [0, 地面 - 1, -25, 'minecraft:stone_bricks'],   // 小飞虹廊桥板
  [-56, 地面 + 1, -30, 'minecraft:stone_bricks'], // 水巷桥拱顶
  [-48, 地面 - 1, -12, 'minecraft:stone_bricks'], // 石舫前甲板（上船口内侧）
  [-46, 地面 + 2, -11, 'minecraft:dark_oak_planks'], // 尾舱西墙
  [-60, 地面, -44, 'minecraft:air'],               // 河房西过街廊
  [0, 地面 + 5, -30, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 小飞虹廊桥脊板
  [-52, 地面 + 1, -2, 'minecraft:stone_bricks'],  // 连通渠桥拱顶
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -64, x2: 64, z1: -64, z2: 64, y1: 62, y2: 76 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤4.json'), JSON.stringify(job));
console.log('步骤4 ops=', J.operations.length, 'palette=', J.palette.length);
