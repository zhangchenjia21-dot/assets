/**
 * 步骤3 厅堂水榭：澄心堂（湖心岛，四面长窗歇山）、涵碧榭（东湾水榭，门东面湖，
 * 台基半入水）、花厅（南门内，前后门户）；并开影壁中央过道以通花厅。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 厅堂, 长窗带 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';
const J = new 作业();

// ── 澄心堂（湖心岛主堂，四面长窗面水）──
厅堂(J, 0, -6, 5, 3, { 四面: true, 门向: 'south' });

// ── 涵碧榭（东湾，门东朝岸、西面湖）──
厅堂(J, 46, 2, 3, 2, { 四面: true, 门向: 'east', 墙高: 4 });

// ── 花厅（南门内，门南开向入口、北开向湖）──
厅堂(J, 0, 52, 5, 2, { 门向: 'south' });
// 北门（通北侧湖岸/游廊）手工开：2 宽 × 3 高
for (let y = 地面; y <= 地面 + 2; y++) { J.放(0, y, 50, 'minecraft:air'); J.放(1, y, 50, 'minecraft:air'); }
// 南门（入口）由厅堂已开；再开影壁中央过道（2×2）以通花厅
for (let y = 地面; y <= 地面 + 1; y++) { J.放(-1, y, 58, 'minecraft:air'); J.放(0, y, 58, 'minecraft:air'); J.放(1, y, 58, 'minecraft:air'); }
// 影壁过道两侧补砖雕框
J.放(-2, 地面 + 1, 58, 'minecraft:tuff'); J.放(2, 地面 + 1, 58, 'minecraft:tuff');

// ── 自检采样 ──
const samples = [
  [-5, 地面 + 2, -5, 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]'], // 澄心堂西山墙长窗(非柱行)
  [0, 地面 - 1, -8, 'minecraft:stone_bricks'],  // 澄心堂台基
  [44, 地面 + 1, 4, 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]'], // 涵碧榭南墙长窗(非柱位)
  [46, 地面 - 1, 5, 'minecraft:stone_bricks'],  // 涵碧榭台基（入水面）
  [-2, 地面 + 2, 54, 'minecraft:dark_oak_log[axis=y]'], // 花厅南墙柱
  [0, 地面, 58, 'minecraft:air'],               // 影壁中央过道
  [0, 地面 + 2, 50, 'minecraft:air'],           // 花厅北门
  [0, 地面 - 1, 52, 'minecraft:stone_bricks'],  // 花厅台基
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -20, x2: 56, z1: -20, z2: 62, y1: 58, y2: 72 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤3.json'), JSON.stringify(job));
console.log('步骤3 ops=', J.operations.length, 'palette=', J.palette.length);
