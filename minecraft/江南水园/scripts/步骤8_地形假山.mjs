/**
 * 步骤8 地形与主假山（整改"全无起伏"）：
 * 北后山立一座湖石主假山（主峰 12 格，多峰带孔窍），山体开洞（x=4）、
 * 东/南坡设盘旋蹬道（逐格升 1，Δ≤1 可登顶），峰顶方亭（台基即平顶）；
 * 东岸、南岸各造 1~2 格缓坡土丘，给全园竖向起伏；同址补植。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 方亭 } from './园林库.mjs';
import { 水体, 岛内 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';
const J = new 作业();
const 首 = {};
const 记 = (k, x, y, z, b) => { if (!首[k]) 首[k] = [x, y, z, b]; };
const 石材 = [M.湖石1, M.湖石2, M.湖石3, M.湖石4, M.湖石5];
const 选石 = (x, y, z) => 石材[((x * 7 + z * 3 + y * 5) >>> 0) % 石材.length];

// 平台（方亭台基范围）先定为 12 高
const 平x1 = 7, 平x2 = 13, 平z1 = -55, 平z2 = -49, 峰高 = 12;
const H = new Map();
for (let x = -8; x <= 26; x++) for (let z = -58; z <= -44; z++) {
  const e = ((x - 9) / 18) ** 2 + ((z + 51) / 8) ** 2; if (e > 1) continue;
  let h = 0;
  for (const [px, pz, ph, sig] of [[10, -52, 12, 5], [2, -56, 9, 4], [20, -56, 8, 4], [24, -50, 7, 3]]) h = Math.max(h, ph * Math.exp(-(((x - px) ** 2 + (z - pz) ** 2) / (2 * sig * sig))));
  h *= Math.max(0, 1.1 - e);
  h += (((x * 7349 + z * 15161) >>> 0) % 100) / 100 * 1.4 - 0.7;
  const hi = Math.max(0, Math.round(h));
  if (hi >= 1) H.set(x + ',' + z, hi);
}
// 峰顶平台压平（台基范围）
for (let x = 平x1; x <= 平x2; x++) for (let z = 平z1; z <= 平z2; z++) H.set(x + ',' + z, 峰高);
// 蹬道格加高（确保支撑到达其高）
const 蹬 = [[10, -44, 1, 'south'], [10, -45, 2, 'south'], [10, -46, 3, 'south'], [10, -47, 4, 'south'], [10, -48, 5, 'south'],
  [11, -48, 6, 'west'], [12, -48, 7, 'west'], [13, -48, 8, 'west'], [14, -48, 9, 'west'], [14, -49, 10, 'north'], [14, -50, 11, 'north']];
for (const [x, z, h] of 蹬) if (h > (H.get(x + ',' + z) || 0)) H.set(x + ',' + z, h);
H.set('13,-50', 峰高); // 蹬道登顶落点（平台边）

// 堆岩体（多孔）
for (const [k, hi] of H) {
  const [x, z] = k.split(',').map(Number);
  for (let y = 地面; y < 地面 + hi; y++) {
    if (y >= 地面 + hi - 2 && ((x * 31 + z * 17 + y * 13) >>> 0) % 100 < 13) continue;
    J.放(x, y, z, 选石(x, y, z));
  }
}
// 凿洞（x=4，南面隧道 + 内室）
for (let z = -44; z >= -47; z--) { J.放(4, 地面, z, 'minecraft:air'); J.放(4, 地面 + 1, z, 'minecraft:air'); }
for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) if (dx * dx + dz * dz <= 5) for (let y = 地面; y <= 地面 + 2; y++) J.放(4 + dx, y, -49 + dz, 'minecraft:air');

// 蹬道踏步（在岩体顶铺石阶）
const 梯 = (f) => `minecraft:stone_brick_stairs[facing=${f},half=bottom,shape=straight,waterlogged=false]`;
for (const [x, z, h, f] of 蹬) J.放(x, 地面 + h - 1, z, 梯(f));

// 峰顶方亭
方亭(J, 10, -52, 2, { 基y: 地面 + 峰高 });
记('顶亭', 10, 地面 + 峰高 - 1, -52, M.台基);

// ── 缓坡土丘（1~2 格，草+湖石）──
function 土丘(J, cx, cz, rx, rz, maxh) {
  for (let x = cx - rx; x <= cx + rx; x++) for (let z = cz - rz; z <= cz + rz; z++) {
    if (水体(x, z) || 岛内(x, z)) continue;
    const e = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2; if (e > 1) continue;
    const h = Math.max(0, Math.round(maxh * (1 - e) + (((x * 13 + z * 29) >>> 0) % 100) / 100 * 0.8));
    for (let y = 地面; y < 地面 + h; y++) J.放(x, y, z, (y === 地面 + h - 1) ? ((x + z) & 1 ? M.湖石3 : M.草) : M.土);
  }
}
土丘(J, 38, -22, 7, 5, 2);
土丘(J, 16, 32, 6, 4, 2);

// ── 补植（假山/土丘松点缀）──
for (const [x, z] of [[4, -48], [20, -50]]) J.放(x, H.get(x + ',' + z) ? 地面 + H.get(x + ',' + z) : 地面 + 1, z, M.松干);

const samples = [
  [10, 地面 + 8, -52, 选石(10, 地面 + 8, -52)],                    // 主峰岩体
  [4, 地面, -44, 'minecraft:air'],                                  // 山洞洞口
  [14, 地面 + 8, -48, 梯('west')],                                  // 蹬道踏步(h9)
  [10, 地面 + 峰高 - 1, -52, 'minecraft:stone_bricks'],             // 峰顶台基
  [10, 地面 + 峰高, -52, 'minecraft:air'],                          // 峰顶亭内
  [38, 地面 + 1, -22, 'minecraft:grass_block[snowy=false]'],        // 东岸土丘顶
  [16, 地面 + 1, 32, 'minecraft:grass_block[snowy=false]'],         // 南岸土丘顶
];
const job = { world_path: 世界, phases: [J.阶段()], samples,
  scan: { x1: -64, x2: 64, z1: -64, z2: 64, y1: 62, y2: 82 } };
fs.writeFileSync(path.join(根, '..', '施工', '步骤8.json'), JSON.stringify(job));
console.log('步骤8 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
