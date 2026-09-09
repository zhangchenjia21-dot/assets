/**
 * 步骤3 中部厅堂：涵碧堂（四面厅+临水月台）、明瑟楼（二层楼阁）、
 * 绿荫轩（入口序列尽端敞轩）、远翠阁（北岸二层阁，门面南临池）。
 * 月台挑出占个别水缘格，为设计内亲水平台；曲桥1 将在步骤7 落于月台北缘缺口。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 厅堂, 栏杆带 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();

// ── 涵碧堂：四面厅 29×13，c(-16,58)，门面北向池 ──
厅堂(J, -16, 58, 14, 6, { 四面: true, 门向: 'north' });
// 南面补门（通南岸步道）
J.盒(-16, 地面, 64, -15, 地面 + 2, 64, 'minecraft:air');
// 临水月台：x-26..-8, z47..51（北缘留 x-17..-15 缺口接曲桥1）
J.盒(-26, 地面 - 1, 47, -8, 地面 - 1, 51, M.台基);
const 栏 = [];
for (let x = -26; x <= -8; x++) if (x < -17 || x > -15) 栏.push([x, 47]);
for (let z = 48; z <= 51; z++) { 栏.push([-26, z]); 栏.push([-8, z]); }
栏杆带(J, 栏, 地面);

// ── 明瑟楼：二层楼阁，c(-46,54)，门面北 ──
厅堂(J, -46, 54, 7, 6, { 楼: true, 门向: 'north' });

// ── 绿荫轩：敞轩 c(18,52)，门面东（接入口曲廊）──
厅堂(J, 18, 52, 5, 4, { 门向: 'east' });

// ── 远翠阁：北岸二层阁 c(-18,-54)，门面南临池 ──
厅堂(J, -18, -54, 6, 5, { 楼: true, 门向: 'south' });

// ── 自检采样 ──
const samples = [
  [-30, 地面, 52, 'minecraft:dark_oak_log[axis=y]'],   // 涵碧堂檐柱
  [-29, 地面 + 1, 52, 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]'], // 四面长窗
  [-16, 地面 + 1, 64, 'minecraft:air'],                // 涵碧堂南门
  [-20, 地面 - 1, 48, 'minecraft:stone_bricks'],       // 月台面
  [-26, 地面, 49, 'minecraft:dark_oak_fence[east=false,north=true,south=true,waterlogged=false,west=false]'], // 月台西栏杆（南北连）
  [-46, 地面 + 3, 54, 'minecraft:dark_oak_planks'],    // 明瑟楼二层楼板
  [23, 地面 + 1, 52, 'minecraft:air'],                 // 绿荫轩东门
  [-24, 地面 + 4, -59, 'minecraft:dark_oak_log[axis=y]'], // 远翠阁二层檐柱
  [-18, 地面 + 1, -49, 'minecraft:air'],               // 远翠阁南门
];

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -60, x2: 30, z1: -66, z2: 70, y1: 63, y2: 82 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤3.json'), JSON.stringify(job));
console.log('步骤3 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
