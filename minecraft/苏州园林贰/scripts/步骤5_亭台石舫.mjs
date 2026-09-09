/**
 * 步骤5 亭台石舫：三岛亭（湖心亭/荷风亭/笠亭）、西岸观鱼亭、
 * 土山至乐亭/舒啸亭（垫台找平）、东北绿漪亭、盆景园茅亭、西湾香洲石舫。
 * 山顶亭先用台基填垫出平台再立亭；石舫卧西湾水面，艏朝东，尾楼二层+中舱硬山+艏凉棚。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 方亭, 硬山顶, 长窗带 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();

// ── 三岛亭 ──
方亭(J, -38, -6, 3);   // 湖心亭（岛A，主景）
方亭(J, -70, 10, 2);   // 荷风亭（岛B）
方亭(J, 16, -30, 2);   // 笠亭（岛C）

// ── 西岸观鱼亭（-72,-26，临水）──
方亭(J, -72, -26, 3);

// ── 至乐亭（土山1 峰顶 -115,-30，山高10 → 垫台至 y73，亭基 74）──
J.盒(-119, 68, -34, -111, 73, -26, M.台基);
方亭(J, -115, -30, 3, { 基y: 74 });

// ── 舒啸亭（土山2 峰 -108,8，山高7 → 垫台至 y70，亭基 71）──
J.盒(-111, 66, 5, -105, 70, 11, M.台基);
方亭(J, -108, 8, 3, { 基y: 71 });

// ── 东北绿漪亭（96,-86）与盆景园茅亭（50,-92）──
方亭(J, 96, -86, 3);
方亭(J, 50, -92, 3);

// ── 香洲石舫（西湾，x-98..-86, z14..18，卧水，艏东）──
// 船体：水线下石身 y62 + 甲板 y63；艏两格收分
J.盒(-98, 62, 14, -88, 62, 18, M.驳岸);
J.盒(-98, 63, 14, -88, 63, 18, M.台基);
J.盒(-87, 62, 15, -86, 62, 17, M.驳岸);   // 艏收窄
J.盒(-87, 63, 15, -86, 63, 17, M.台基);
// 尾楼（西端二层）：粉墙身 + 长窗 + 楼板 + 硬山顶
J.盒(-98, 64, 15, -95, 66, 17, M.粉墙);
J.盒(-97, 65, 15, -96, 65, 15, 'minecraft:air'); // 尾楼南窗洞
J.盒(-98, 67, 14, -95, 67, 18, M.梁);           // 楼板
for (let x = -98; x <= -95; x++) { J.放(x, 68, 15, M.梁); J.放(x, 68, 17, M.梁); }
长窗带(J, -97, 69, 15, -96, 69, 15); 长窗带(J, -97, 69, 17, -96, 69, 17);
J.放(-98, 68, 16, M.梁); J.放(-95, 68, 16, M.梁);
J.放(-98, 69, 16, 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]');
J.放(-95, 69, 16, 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]');
硬山顶(J, -96.5 | 0, 70, 16, 3, 3, true); // 尾楼顶（cx=-97）
// 中舱：粉墙小屋 + 硬山顶
J.盒(-93, 64, 15, -90, 66, 17, M.粉墙);
J.盒(-92, 64, 17, -91, 65, 17, 'minecraft:air'); // 中舱南门
硬山顶(J, -92 | 0, 67, 16, 3, 3, true);
// 艏凉棚：四柱 + 平瓦顶
for (const [px, pz] of [[-88, 15], [-88, 17], [-86, 15], [-86, 17]]) J.盒(px, 64, pz, px, 66, pz, M.柱);
J.盒(-89, 67, 14, -85, 67, 18, M.瓦面);
// 登船跳板：北岸 → 舷侧
J.放(-92, 63, 13, 'minecraft:stone_slab[type=bottom,waterlogged=false]');
J.放(-92, 63, 12, 'minecraft:stone_slab[type=bottom,waterlogged=false]');

// ── 自检采样 ──
const samples = [
  [-41, 地面, -9, 'minecraft:dark_oak_log[axis=y]'],  // 湖心亭角柱
  [-72, 地面, 8, 'minecraft:dark_oak_log[axis=y]'],   // 荷风亭角柱（hx2 → 角 x-72,z8）
  [16, 地面 - 1, -32, 'minecraft:stone_bricks'],      // 笠亭台基
  [-75, 地面, -29, 'minecraft:dark_oak_log[axis=y]'], // 观鱼亭角柱（hx3 → 角 x-75,z-29）
  [-115, 73, -30, 'minecraft:stone_bricks'],          // 至乐亭垫台面
  [-118, 74, -33, 'minecraft:dark_oak_log[axis=y]'],  // 至乐亭角柱
  [-111, 71, 5, 'minecraft:dark_oak_log[axis=y]'],    // 舒啸亭角柱（hx3 → 角 x-111,z5）
  [96, 地面 - 1, -89, 'minecraft:stone_bricks'],      // 绿漪亭台基
  [47, 地面, -95, 'minecraft:dark_oak_log[axis=y]'],  // 茅亭角柱
  [-96, 63, 16, 'minecraft:stone_bricks'],            // 石舫甲板
  [-92, 64, 15, 'minecraft:white_concrete'],          // 中舱壁
  [-92, 65, 17, 'minecraft:air'],                     // 中舱南门
  [-88, 65, 15, 'minecraft:dark_oak_log[axis=y]'],    // 凉棚柱
];
J.校对(samples);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -140, x2: 100, z1: -100, z2: 30, y1: 62, y2: 82 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤5.json'), JSON.stringify(job));
console.log('步骤5 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
