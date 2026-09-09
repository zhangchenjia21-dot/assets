/**
 * 步骤2 围墙门径与河街：外墙粉墙黛瓦、南门门楼（硬山顶）、影壁；
 * 西水巷两岸河街（石板铺地+临水栏杆）；临河河房×4（两两对望）；
 * 北岸望月台（石台+方亭）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 墙段, 硬山顶, 方亭, 栏杆带, 长窗带 } from './园林库.mjs';
import { 水体, 岸线 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';
const J = new 作业();

// ── 外围墙（南门处留 3 宽口）──
墙段(J, -63, -63, 63, -63, 4); // 北
墙段(J, -63, 63, 63, 63, 4);   // 南（其后裁门）
墙段(J, -63, -63, -63, 63, 4); // 西
墙段(J, 63, -63, 63, 63, 4);   // 东
// 裁南门洞：x -1..1, y64..66 挖空；保留 67 作过梁
for (let x = -1; x <= 1; x++) for (let y = 地面; y <= 地面 + 2; y++) J.放(x, y, 63, 'minecraft:air');
J.放(0, 地面, 63, M.地面砖); J.放(-1, 地面, 63, M.地面砖); J.放(1, 地面, 63, M.地面砖); // 过门石
// 门楼（硬山顶）：柱、梁、脊
for (const [px, pz] of [[-3, 63], [3, 63]]) J.盒(px, 地面, pz, px, 地面 + 3, pz, M.柱);
J.盒(-4, 地面 + 3, 63, 4, 地面 + 3, 63, M.梁);
硬山顶(J, 0, 地面 + 4, 63, 5, 2, true);
J.放(-1, 地面, 61, M.灯); J.放(2, 地面, 61, M.灯);

// ── 影壁（z=58）──
墙段(J, -7, 58, 7, 58, 3);
J.盒(-7, 地面, 58, -7, 地面 + 2, 58, 'minecraft:tuff');
J.盒(7, 地面, 58, 7, 地面 + 2, 58, 'minecraft:tuff');
J.盒(-7, 地面 + 2, 58, 7, 地面 + 2, 58, 'minecraft:tuff');
J.盒(-3, 地面 + 1, 58, 3, 地面 + 1, 58, 'minecraft:tuff');

// ── 西水巷两岸河街（石板 + 临水栏杆）──
for (let x = -53; x <= -48; x++) for (let z = -54; z <= 58; z++) if (!水体(x, z) && !岸线(x, z)) J.放(x, 地面 - 1, z, M.地面砖);
for (let x = -62; x <= -59; x++) for (let z = -54; z <= 58; z++) if (!水体(x, z) && !岸线(x, z)) J.放(x, 地面 - 1, z, M.地面砖);
// 两岸临水栏杆（连续式，沿运河两缘）
const 东栏 = [], 西栏 = [];
for (let z = -54; z <= 58; z++) { 东栏.push([-53, z]); 西栏.push([-59, z]); }
栏杆带(J, 东栏, 地面); 栏杆带(J, 西栏, 地面);

// ── 临河河房（两岸各二，门朝水巷）──
function 河房(J, cx, cz, 门向, hx = 1, hz = 2) {
  const x1 = cx - hx, x2 = cx + hx, z1 = cz - hz, z2 = cz + hz;
  J.盒(x1 - 1, 地面 - 1, z1 - 1, x2 + 1, 地面 - 1, z2 + 1, M.台基);
  for (let y = 地面; y < 地面 + 4; y++) {
    for (let x = x1; x <= x2; x++) { J.放(x, y, z1, M.粉墙); J.放(x, y, z2, M.粉墙); }
    for (let z = z1 + 1; z <= z2 - 1; z++) { J.放(x1, y, z, M.粉墙); J.放(x2, y, z, M.粉墙); }
  }
  J.盒(x1, 地面, z1, x1, 地面 + 3, z1, M.柱); J.盒(x2, 地面, z1, x2, 地面 + 3, z1, M.柱);
  J.盒(x1, 地面, z2, x1, 地面 + 3, z2, M.柱); J.盒(x2, 地面, z2, x2, 地面 + 3, z2, M.柱);
  // 面水窗（柱间玻璃）
  if (门向 === 'west') J.盒(x1, 地面 + 1, z1 + 1, x1, 地面 + 2, z2 - 1, 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]');
  if (门向 === 'east') J.盒(x2, 地面 + 1, z1 + 1, x2, 地面 + 2, z2 - 1, 'minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=true]');
  // 门（面水侧中央 1×2）
  if (门向 === 'west') { J.放(x1, 地面, cz, 'minecraft:air'); J.放(x1, 地面 + 1, cz, 'minecraft:air'); }
  if (门向 === 'east') { J.放(x2, 地面, cz, 'minecraft:air'); J.放(x2, 地面 + 1, cz, 'minecraft:air'); }
  硬山顶(J, cx, 地面 + 4, cz, hx + 1, hz + 1, true);
}
河房(J, -49, -44, 'west'); // 东岸北河房
河房(J, -49, 34, 'west');  // 东岸南河房
河房(J, -60, -44, 'east');  // 西岸北河房
河房(J, -60, 34, 'east');   // 西岸南河房

// ── 北岸望月台 ──
J.盒(12, 地面 - 1, -40, 20, 地面 - 1, -32, M.台基); // 石台
方亭(J, 16, -36, 2);
J.放(16, 地面, -33, M.灯);

// ── 自检采样 ──
const samples = [
  [-1, 地面 + 1, 63, 'minecraft:air'],        // 南门洞
  [-7, 地面 + 1, 58, 'minecraft:tuff'],        // 影壁框
  [-49, 地面, -44, 'minecraft:air'],           // 东岸北河房门
  [-49, 地面 - 1, -44, 'minecraft:stone_bricks'], // 河房台基/河街
  [-53, 地面, -47, 'minecraft:dark_oak_fence[east=false,north=true,south=true,waterlogged=false,west=false]'], // 河街栏杆中点
  [16, 地面 - 1, -36, 'minecraft:stone_bricks'], // 望月台
  [14, 地面, -38, 'minecraft:dark_oak_log[axis=y]'], // 望月亭角柱
  [40, 地面, -63, 'minecraft:white_concrete'], // 北墙
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -63, x2: 63, z1: -63, z2: 63, y1: 58, y2: 72 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤2.json'), JSON.stringify(job));
console.log('步骤2 ops=', J.operations.length, 'palette=', J.palette.length);
