// 世界核验：扫描真实存档，与蓝本逐格比对，并执行结构自检（悬空 / 通路 / 空间成立性）。
import fs from 'node:fs';
import path from 'node:path';
import { generateBlueprint } from './蓝本.mjs';
import { decodeScan, fromBuilder } from './体素渲染.mjs';
import { makeSolid, checkFloating, walkPath, compartmentVolume } from './结构自检.mjs';
import { runJob, PROJECT, WORLD } from './执行器.mjs';
import { G, M } from './设计参数.mjs';
import { canonical } from './几何核心.mjs';

const mode = process.argv[2] || 'verify';
const b = generateBlueprint();
const rep = b.report();

// 扫描范围：整个建筑与场地（分两块，规避 1e6 体素上限）；y 必须覆盖到蓝本最高点
const BOX = { x1: -24, x2: 46, y1: -6, y2: 50, z1: -22, z2: 56 };
const HALF = 16;
const scans = [
  { label: 'scan-A', scan: { x1: BOX.x1, y1: BOX.y1, z1: BOX.z1, x2: BOX.x2, y2: BOX.y2, z2: HALF } },
  { label: 'scan-B', scan: { x1: BOX.x1, y1: BOX.y1, z1: HALF + 1, x2: BOX.x2, y2: BOX.y2, z2: BOX.z2 } },
];

// 世界回读：一次作业同时取两块扫描
const job = { scan: scans[0].scan, phases: [] };
const resA = runJob({ scan: scans[0].scan }, { label: '核验-A' });
console.log('扫描 A: status=' + resA.result.status + ' 体积=' + resA.result.scan.volume + ' 非空气=' + resA.result.scan.non_air + ' 耗时=' + Math.round(resA.result.wall_seconds) + 's');
const resB = runJob({ scan: scans[1].scan }, { label: '核验-B' });
console.log('扫描 B: status=' + resB.result.status + ' 体积=' + resB.result.scan.volume + ' 非空气=' + resB.result.scan.non_air + ' 耗时=' + Math.round(resB.result.wall_seconds) + 's');

// 合并两块扫描为一个体素卷
const A = decodeScan(resA.result.scan), Bv = decodeScan(resB.result.scan);
const nx = A.nx, ny = A.ny, nz = A.nz + Bv.nz;
const grid = new Array(nx * ny * nz).fill('minecraft:air');
for (let y = 0; y < ny; y++) for (let z = 0; z < A.nz; z++) for (let x = 0; x < nx; x++) {
  grid[y * nz * nx + z * nx + x] = A.grid[y * A.nz * nx + z * nx + x];
  grid[y * nz * nx + (z + A.nz) * nx + x] = Bv.grid[y * Bv.nz * nx + z * nx + x];
}
const vol = { grid, nx, ny, nz, bounds: { x1: BOX.x1, y1: BOX.y1, z1: BOX.z1, x2: BOX.x2, y2: BOX.y2, z2: BOX.z2 } };
console.log('合并体素卷: ' + nx + '×' + ny + '×' + nz + ' = ' + grid.length);

// ---------- 1. 与蓝本比对 ----------
// Minecraft 会自动补全 waterlogged / powered 等属性；比对只要求"蓝本显式声明的属性"一致 + 方块种类相同。
function stateProps(s) {
  const i = s.indexOf('[');
  if (i < 0) return { id: s, props: new Map() };
  const id = s.slice(0, i);
  const props = new Map(s.slice(i + 1, -1).split(',').map((kv) => kv.split('=')));
  return { id, props };
}
function stateMatches(blueprint, world) {
  const a = stateProps(blueprint), c = stateProps(world);
  if (a.id !== c.id) return false;
  for (const [k, v] of a.props) if (c.props.get(k) !== v) return false;
  return true;
}

let mismatch = 0, checked = 0, extra = 0;
const diffs = [];
const extraByState = new Map();
for (const [k, st] of b.cells) {
  const [x, y, z] = k.split(',').map(Number);
  if (x < BOX.x1 || x > BOX.x2 || y < BOX.y1 || y > BOX.y2 || z < BOX.z1 || z > BOX.z2) continue;
  checked++;
  const ix = x - BOX.x1, iy = y - BOX.y1, iz = z - BOX.z1;
  const actual = grid[iy * nz * nx + iz * nx + ix];
  if (!stateMatches(st, actual)) { mismatch++; if (diffs.length < 20) diffs.push({ pos: [x, y, z], blueprint: st, world: actual }); }
}
// 反向：世界里的多余方块（蓝本未声明的非空气格）→ 用于发现旧几何残留
for (let i = 0; i < grid.length; i++) {
  const w = grid[i];
  if (!w || w === 'minecraft:air') continue;
  const y = Math.floor(i / (nz * nx)), rem = i % (nz * nx);
  const z = Math.floor(rem / nx), x = rem % nx;
  const bp = b.get(BOX.x1 + x, BOX.y1 + y, BOX.z1 + z);
  if (bp === undefined || bp === 'minecraft:air') { extra++; extraByState.set(w, (extraByState.get(w) || 0) + 1); }
}
console.log('\n=== 蓝本 ↔ 世界 双向比对 ===');
console.log('正向（蓝本 → 世界）比对格数: ' + checked + '   不一致: ' + mismatch);
console.log('反向（世界多余方块，应为 0）: ' + extra);
for (const [s, n] of [...extraByState].sort((a, c) => c[1] - a[1]).slice(0, 8)) console.log('   ' + String(n).padStart(5) + '  ' + s);
for (const d of diffs) console.log('   ' + d.pos.join(',') + '  蓝本 ' + d.blueprint + '  世界 ' + d.world);

// ---------- 2. 结构自检 ----------
const solid = makeSolid(vol);
console.log('\n=== 悬空 / 支承闭合 ===');
const floating = checkFloating(solid);
console.log('可疑无支承方块: ' + floating.length);
const floatByState = new Map();
for (const [, , , s] of floating) floatByState.set(s, (floatByState.get(s) || 0) + 1);
for (const [s, n] of [...floatByState].sort((a, c) => c[1] - a[1]).slice(0, 10)) console.log('   ' + String(n).padStart(5) + '  ' + s);
for (const f of floating.slice(0, 12)) console.log('   位置 ' + f.slice(0, 3).join(',') + '  ' + f[3]);

console.log('\n=== 主要路径（Movement Envelope，逐格真实碰撞包络）===');
// 路径格式：[x, z, 预期可行走高度 y]；取点对应实际门洞与梯段位置
const paths = {
  '广场→门前台阶→门廊': [[4, -14, 0], [4, -12, 0], [4, -11, 1], [4, -10, 1], [4, -9, 1], [4, -6, 1], [4, -4, 1]],
  '门廊→拱廊→东端（沿 x=5 通行带）': [[5, -4, 1], [5, -1, 1], [5, 3, 1], [5, 10, 1], [5, 20, 1], [5, 30, 1], [5, 40, 1], [5, 46, 1]],
  '拱廊→交易厅（中门 z=26）': [[5, 26, 1], [7, 26, 1], [8, 26, 1], [10, 26, 1], [12, 26, 1], [14, 26, 1], [16, 26, 1], [19, 26, 1], [21, 26, 1], [23, 26, 1]],
  '交易厅→主楼梯→上层大厅': [[9, 11, 1], [9, 9, 1], [9, 8, 2], [9, 7, 3], [9, 6, 4], [9, 5, 5], [9, 4, 6], [9, 3, 6], [9, 2, 7], [12, 2, 7]],
  '上层大厅东西贯通': [[12, 4, 7], [12, 12, 7], [12, 22, 7], [12, 32, 7], [12, 41, 7]],
  '交易厅东西贯通（南跨）': [[9, 40, 1], [9, 30, 1], [9, 22, 1], [9, 14, 1], [9, 11, 1]],
  '交易厅东西贯通（北跨）': [[15, 40, 1], [15, 30, 1], [15, 20, 1], [15, 10, 1], [15, 3, 1]],
  '北侧后勤穿通': [[21, 40, 1], [21, 30, 1], [21, 25, 1], [21, 13, 1], [21, 5, 1]],
  '上层辅助房间（北侧）': [[22, 14, 7], [22, 15, 7], [22, 16, 7], [22, 17, 7]],
  '地窖梯（自交易层下行）': [[9, 33, 1], [9, 32, 0], [9, 31, 0], [9, 30, 0], [9, 29, -1], [9, 28, -2], [9, 26, -4]],
};
for (const [name, p] of Object.entries(paths)) {
  const r = walkPath(solid, p, { name, maxRise: 1 });
  console.log('  ' + name + ': ' + (r.issues.length ? '问题 ' + r.issues.length : 'OK') + ' / ' + r.steps + ' 点');
  for (const it of r.issues.slice(0, 6)) console.log('      ' + it.kind + ' @ ' + it.at.join(',') + '  ' + it.detail);
}

console.log('\n=== 空间成立性 ===');
const comps = {
  '拱廊（拱廊内净空）': { x1: 3, x2: 5, y1: 1, y2: 4, z1: 2, z2: 46 },
  '交易厅南跨': { x1: 8, x2: 10, y1: 1, y2: 3, z1: 2, z2: 42 },
  '交易厅北跨': { x1: 14, x2: 17, y1: 1, y2: 3, z1: 2, z2: 42 },
  '上层大厅': { x1: 8, x2: 18, y1: 8, y2: 15, z1: 3, z2: 42 },
  '上层辅助房间': { x1: 21, x2: 23, y1: 8, y2: 11, z1: 3, z2: 41 },
  '地窖': { x1: 8, x2: 22, y1: -3, y2: -2, z1: 3, z2: 41 },
  '门廊内部': { x1: 1, x2: 7, y1: 2, y2: 5, z1: -7, z2: -3 },
};
for (const [name, c] of Object.entries(comps)) {
  const v = compartmentVolume(solid, c);
  console.log('  ' + name + ': 空气 ' + v.air + '  最大连通 ' + v.largest + '  孤立口袋 ' + v.pockets);
}

fs.writeFileSync(path.join(PROJECT, 'evidence/verify-report.json'), JSON.stringify({
  blueprint: { blocks: rep.blocks, conflicts: rep.conflicts, states: rep.distinctStates, bounds: rep.bounds },
  scans: [resA.result.scan.bounds, resB.result.scan.bounds],
  job_directories: [resA.jobDirectory, resB.jobDirectory],
  compare: { checked, mismatch, diffs },
  floating: { count: floating.length, top: [...floatByState].slice(0, 20), samples: floating.slice(0, 60) },
  paths: Object.fromEntries(Object.entries(paths).map(([n, p]) => [n, walkPath(solid, p, { name: n })])),
  compartments: Object.fromEntries(Object.entries(comps).map(([n, c]) => [n, compartmentVolume(solid, c)])),
}, null, 1));
console.log('\n证据: evidence/verify-report.json');
