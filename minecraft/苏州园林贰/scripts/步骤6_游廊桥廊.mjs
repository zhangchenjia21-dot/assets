/**
 * 步骤6 游廊系统（对应留园 700 米曲廊）+ 小飞虹廊桥。
 * 廊网：①入口曲廊（小院→绿荫轩，穿东区隔墙）②北岸-西岸廊（远翠阁→石舫码头，穿溪以石拱②衔接步骤7）
 *       ③东部联系廊（五峰仙馆-林泉馆-揖峰轩-冠云庭院）④中轴廊（绿荫轩北连东部网）
 *       ⑤北部田园廊（又一村→盆景园→茅亭）。
 * 小飞虹廊桥：跨西北源水峡 x=-78, z-54..-42，中带歇山顶桥亭（卧波如飞虹）。
 * 穿墙门洞：廊过墙处先廊后洞，洞口 3~5 宽×4 高，洞顶留墙身。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 游廊, 攒尖顶, 栏杆带 } from './园林库.mjs';
import { 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();

// ── ①入口曲廊：小院月洞门(104,95) → 绿荫轩东门(23,52) ──
游廊(J, [[101, 95], [86, 95], [86, 78], [68, 78], [68, 64], [46, 64], [46, 58], [32, 58], [32, 52], [24, 52]]);
J.盒(102, 地面 - 1, 94, 103, 地面 - 1, 96, M.地面砖); // 月洞门西侧接引铺装
// 穿东区隔墙（x=55, z=64 一线）：先廊后洞
J.盒(55, 地面, 62, 55, 地面 + 3, 66, 'minecraft:air');

// ── ②北岸-西岸廊：远翠阁西 → 北岸 → 西绕西北源 → 石舫码头 ──
游廊(J, [[-24, -46], [-42, -46], [-42, -62], [-96, -62], [-96, -52]]);
游廊(J, [[-96, -36], [-96, -12], [-92, -12], [-92, 10]]);
// 石拱②（步骤7 实施 z-46..-38 跨溪段）前的桥头引道铺装
J.盒(-97, 地面 - 1, -51, -95, 地面 - 1, -47, M.地面砖);
J.盒(-97, 地面 - 1, -37, -95, 地面 - 1, -33, M.地面砖);

// ── ③东部联系廊 ──
游廊(J, [[50, -20], [60, -20], [60, 4], [78, 4], [78, 18], [67, 18], [67, 21]]); // A：月洞门(55,-20)→五峰仙馆西→隔墙门→林泉馆北
游廊(J, [[78, 4], [118, 4], [118, -14]]);                                        // B：东延至冠云庭院南门
游廊(J, [[118, -18], [118, -28]]);                                               // 院内望峰廊（端距立峰基座 2 格）
// 穿分区隔墙（z=8, x=78 一线）门洞
J.盒(77, 地面, 8, 79, 地面 + 3, 8, 'minecraft:air');

// ── ④中轴廊：绿荫轩 → 北接东部网 ──
游廊(J, [[32, 52], [50, 52], [50, -20]]);

// ── ⑤北部田园廊：又一村(0,-72) → 盆景园 → 茅亭；西支(-40,-72) → 竹林 ──
游廊(J, [[0, -64], [0, -88], [46, -88], [50, -88]]);
游廊(J, [[-40, -70], [-40, -84]]);

// ── 小飞虹廊桥（x=-78, z-54..-42，卧波跨西北源水峡）──
J.盒(-79, 地面 - 1, -54, -77, 地面 - 1, -42, M.台基); // 甲板
for (const z of [-52, -48, -44]) for (const x of [-79, -77])  // 桥墩
  if (水体(x, z)) for (let y = 59; y < 63; y++) J.放(x, y, z, M.驳岸);
// 廊式桥面：柱每 4 格 + 五格断面瓦顶（檐 y67 / 坡 y68 / 脊板 y69）
for (let z = -54; z <= -42; z++) {
  for (const x of [-79, -77]) if ((z + 54) % 4 === 0) J.盒(x, 地面, z, x, 地面 + 2, z, M.柱);
  J.放(-80, 地面 + 3, z, M.瓦檐); J.放(-76, 地面 + 3, z, M.瓦檐);
  J.放(-79, 地面 + 4, z, 'minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]');
  J.放(-77, 地面 + 4, z, 'minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]');
  J.放(-78, 地面 + 5, z, M.瓦面);
}
// 桥中亭：平台 x-81..-75, z-50..-46，四柱，攒尖顶
J.盒(-81, 地面 - 1, -50, -75, 地面 - 1, -46, M.台基);
for (let x = -81; x <= -75; x++) for (let z = -50; z <= -46; z++)
  if (水体(x, z)) for (let y = 59; y < 63; y++) J.放(x, y, z, M.驳岸);
for (const [px, pz] of [[-81, -50], [-75, -50], [-81, -46], [-75, -46]]) J.盒(px, 地面, pz, px, 地面 + 3, pz, M.柱);
攒尖顶(J, -78, 地面 + 4, -48, 4, 3);
// 桥栏（甲板两缘，亭台处断开）
const 栏 = [];
for (let z = -54; z <= -42; z++) { if (z >= -50 && z <= -46) continue; 栏.push([-80, z]); 栏.push([-76, z]); }
栏杆带(J, 栏, 地面);
// 北端接北岸廊的石板引道
J.盒(-79, 地面 - 1, -60, -77, 地面 - 1, -55, M.地面砖);

// ── 自检采样 ──
const samples = [
  [86, 地面 - 1, 95, 'minecraft:stone_bricks'],       // ①廊面
  [55, 地面 + 1, 64, 'minecraft:air'],                // ①穿墙门洞
  [-60, 地面 - 1, -62, 'minecraft:stone_bricks'],     // ②廊面
  [100, 地面 - 1, 4, 'minecraft:stone_bricks'],       // ③B 廊面
  [118, 地面 - 1, -24, 'minecraft:stone_bricks'],     // ③院内望峰廊
  [0, 地面 - 1, -80, 'minecraft:stone_bricks'],       // ⑤田园廊
  [50, 地面 - 1, 20, 'minecraft:stone_bricks'],       // ④中轴廊
  [-78, 地面 - 1, -48, 'minecraft:stone_bricks'],     // 廊桥中亭平台
  [-75, 地面, -50, 'minecraft:dark_oak_log[axis=y]'], // 桥中亭角柱
  [-78, 地面 + 5, -54, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 廊桥脊板
  [55, 地面 + 1, -20, 'minecraft:air'],               // 外部：东区月洞门（步骤2 已有）
];
J.校对(samples);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 125, z1: -100, z2: 100, y1: 62, y2: 74 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤6.json'), JSON.stringify(job));
console.log('步骤6 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
