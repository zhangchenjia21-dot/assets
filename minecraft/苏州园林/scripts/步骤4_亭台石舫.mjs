/**
 * 步骤4 亭台石舫：雪香云蔚亭（东岛）、荷风四面亭（西岛）、梧竹幽居（东岸月洞方亭）、
 * 绿漪亭（东北竹丛）、小沧浪亭（西南湾岸）、香洲石舫（西岸，船头入水）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 方亭, 硬山顶, 栏杆带 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业();

方亭(J, -8, -14, 2);              // 雪香云蔚亭（东岛）
方亭(J, -40, -4, 2);              // 荷风四面亭（西岛）
方亭(J, 20, -10, 3, { 月洞墙: true }); // 梧竹幽居（四面满月洞）
方亭(J, 84, -64, 2);              // 绿漪亭
方亭(J, -52, 26, 2);              // 小沧浪亭

// ── 香洲石舫：船身 x -74..-62, z -8..-4，尾舱+中棚+码头 ──
const 舱x1 = -74, 船头x = -62, 舷z1 = -8, 舷z2 = -4;
J.盒(-74, 地面 - 1, 舷z1, -64, 地面 - 1, 舷z2, M.台基); // 主甲板（y63）
J.盒(-63, 地面 - 1, -7, -62, 地面 - 1, -5, M.台基);     // 船头收窄
const 甲板 = new Set();
for (let x = -74; x <= -64; x++) for (let z = 舷z1; z <= 舷z2; z++) 甲板.add(x + ',' + z);
for (let x = -63; x <= -62; x++) for (let z = -7; z <= -5; z++) 甲板.add(x + ',' + z);
// 舷边栏杆
const 舷栏 = [];
for (const k of 甲板) { const [x, z] = k.split(',').map(Number);
  if (![ [1,0],[-1,0],[0,1],[0,-1] ].every(([dx,dz]) => 甲板.has((x+dx)+','+(z+dz)))) 舷栏.push([x, z]); }
栏杆带(J, 舷栏, 地面);
// 尾舱（x -74..-70, 5×5 船楼，硬山顶）
J.盒(-74, 地面, -8, -70, 地面 + 2, -4, M.梁);          // 舱体
J.盒(-73, 地面, -7, -71, 地面 + 2, -5, 'minecraft:air'); // 舱内空
J.盒(-74, 地面 + 1, -7, -74, 地面 + 1, -5, 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]'); // 西窗
J.盒(-70, 地面, -6, -70, 地面 + 1, -6, 'minecraft:air'); // 舱门向东
硬山顶(J, -72, 地面 + 3, -6, 3, 3, true);
// 中舱凉棚：四柱 + 平瓦棚
for (const [px, pz] of [[-69, -8], [-69, -4], [-65, -8], [-65, -4]]) J.盒(px, 地面, pz, px, 地面 + 2, pz, M.柱);
J.盒(-69, 地面 + 3, -8, -65, 地面 + 3, -4, M.瓦檐);
// 船头灯 + 船尾码头
J.放(-62, 地面, -6, M.灯);
J.盒(-75, 地面 - 1, -7, -75, 地面 - 1, -5, M.台基);

const samples = [
  [-10, 地面, -16, 'minecraft:dark_oak_log[axis=y]'],   // 雪香云蔚亭角柱
  [-8, 地面 + 4, -14, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 亭顶面
  [20, 地面 + 1, -13, 'minecraft:air'],                  // 梧竹幽居月洞
  [-66, 地面 - 1, -6, 'minecraft:stone_bricks'],         // 石舫甲板（临水）
  [-72, 地面, -8, 'minecraft:dark_oak_planks'],          // 尾舱壁
  [-70, 地面, -6, 'minecraft:air'],                      // 舱门
  [82, 地面, -66, 'minecraft:dark_oak_log[axis=y]'],     // 绿漪亭角柱
  [-52, 地面 - 1, 26, 'minecraft:stone_bricks'],         // 小沧浪台基
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -80, x2: 90, z1: -70, z2: 32, y1: 62, y2: 74 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤4.json'), JSON.stringify(job));
console.log('步骤4 ops=', J.operations.length, 'palette=', J.palette.length);
