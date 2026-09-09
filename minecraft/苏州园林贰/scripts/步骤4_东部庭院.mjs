/**
 * 步骤4 东部庭院群：五峰仙馆（全区最大厅堂，门面西）、林泉耆硕馆（鸳鸯厅，门面北）、
 * 揖峰轩（门面北）、冠云楼（冠云峰庭院北，二层，门面南）、冠云亭（庭院西南）、
 * 五峰仙馆与林泉馆之间的分区隔墙（月洞门+漏窗）。
 * 冠云峰立峰本身属步骤8 假山。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 厅堂, 方亭, 墙段, 月洞门, 漏窗 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();

// ── 五峰仙馆：27×15 大厅，c(84,-8)，歇山顶，门面西朝中部 ──
厅堂(J, 84, -8, 13, 7, { 门向: 'west' });

// ── 林泉耆硕馆（鸳鸯厅）：c(66,28)，门面北 ──
厅堂(J, 66, 28, 8, 6, { 门向: 'north' });

// ── 揖峰轩：c(96,16)，门面北 ──
厅堂(J, 96, 16, 5, 4, { 门向: 'north' });

// ── 冠云楼：冠云峰庭院北，二层，c(118,-46)，门面南望峰 ──
厅堂(J, 118, -46, 6, 4, { 楼: true, 门向: 'south' });

// ── 冠云亭：庭院西南角方亭 c(108,-22) ──
方亭(J, 108, -22, 3);

// ── 五峰仙馆/林泉馆分区隔墙（z=8，x58..100，高5）──
墙段(J, 58, 8, 100, 8, 5);
月洞门(J, 78, 8, 'x');
[64, 70, 88, 94].forEach((x, i) => 漏窗(J, x, 8, 'x', 地面, i % 3));

// ── 自检采样 ──
const samples = [
  [71, 地面, -15, 'minecraft:dark_oak_log[axis=y]'],   // 五峰仙馆檐柱
  [71, 地面 + 1, -8, 'minecraft:air'],                 // 五峰仙馆西门
  [62, 地面 + 1, 22, 'minecraft:white_concrete'],      // 林泉馆北墙身（隔一开一之闭间）
  [66, 地面 + 1, 22, 'minecraft:air'],                 // 林泉馆北门
  [91, 地面, 12, 'minecraft:dark_oak_log[axis=y]'],    // 揖峰轩檐柱
  [118, 地面 + 3, -46, 'minecraft:dark_oak_planks'],   // 冠云楼二层楼板
  [105, 地面, -25, 'minecraft:dark_oak_log[axis=y]'],  // 冠云亭亭柱
  [78, 地面 + 2, 8, 'minecraft:air'],                  // 隔墙月洞门洞心
  [63, 地面 + 1, 8, 'minecraft:tuff'],                 // 隔墙漏窗框（式0隅纹 x-1 位）
];
J.校对(samples);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: 50, x2: 140, z1: -60, z2: 70, y1: 63, y2: 84 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤4.json'), JSON.stringify(job));
console.log('步骤4 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
