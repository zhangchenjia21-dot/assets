// 同机位视图证据：从真实存档扫描数据渲染多机位透视图（替代真实客户端截图的公认限制见 Completion Report）。
// 用法：
//   node tools/视图证据.mjs baseline "SPATIAL_COMPLETE 基线"   —— 从基线快照目录扫描
//   node tools/视图证据.mjs final "完成后"                     —— 从当前正式世界扫描
import fs from 'node:fs';
import path from 'node:path';
import { decodeScan, render, writePNG } from './体素渲染.mjs';
import { runJob, PROJECT, WORLD } from './执行器.mjs';

const tag = process.argv[2] || 'view';
const label = process.argv[3] || '';
// 允许通过第 4 个参数指定世界路径（用于 FINISHING 前的 baseline 快照）
const worldPath = process.argv[4] || WORLD;
const outDir = path.join(PROJECT, 'evidence/views');
fs.mkdirSync(outDir, { recursive: true });
console.log('世界: ' + worldPath);

// 扫描整个建筑与场地：z 分三块以规避 1e6 体素上限
const BOX = { x1: -24, x2: 46, y1: -7, y2: 50, z1: -22, z2: 56 };
const CUTS = [[-22, 3], [4, 29], [30, 56]];
const parts = [];
for (const [za, zb] of CUTS) {
  const r = runJob({ scan: { x1: BOX.x1, y1: BOX.y1, z1: za, x2: BOX.x2, y2: BOX.y2, z2: zb } }, { label: `视图扫描-${za}`, worldPath });
  parts.push(decodeScan(r.result.scan));
  console.log(`  扫描 z=${za}..${zb}: 非空气 ${r.result.scan.non_air}  耗时 ${Math.round(r.result.wall_seconds)}s`);
}
// 合并为单一卷
const nx = parts[0].nx, ny = parts[0].ny, nz = parts.reduce((a, p) => a + p.nz, 0);
const grid = new Array(nx * ny * nz).fill('minecraft:air');
let zoff = 0;
for (const p of parts) {
  for (let y = 0; y < ny; y++) for (let z = 0; z < p.nz; z++) for (let x = 0; x < nx; x++) {
    grid[y * nz * nx + (z + zoff) * nx + x] = p.grid[y * p.nz * nx + z * nx + x];
  }
  zoff += p.nz;
}
const vol = { grid, nx, ny, nz, bounds: { x1: BOX.x1, y1: BOX.y1, z1: BOX.z1, x2: BOX.x2, y2: BOX.y2, z2: BOX.z2 } };
console.log(`  合并体素卷 ${nx}×${ny}×${nz}`);

const VIEWS = {
  '1-城市接近_正面': { eye: [-48, 16, -30], target: [10, 11, 20], fov: 48 },
  '2-整体体量_斜俯视': { eye: [-64, 58, -40], target: [12, 12, 20], fov: 44 },
  '3-市场侧拱廊': { eye: [-14, 6, 4], target: [6, 4, 24], fov: 68 },
  '4-入口门廊与大楼梯': { eye: [-6, 6, -22], target: [6, 6, -2], fov: 66 },
  '5-拱廊内看交易厅': { eye: [-24, 4, 22], target: [10, 3, 22], fov: 72 },
  '6-交易厅内景（南跨）': { eye: [9, 3, 40], target: [9, 3, 6], fov: 74 },
  '7-上层大厅内景': { eye: [14, 11, 40], target: [11, 9, 4], fov: 74 },
  '8-主楼梯与井道': { eye: [9, 9, 14], target: [9, 3, 4], fov: 76 },
  '9-北侧后勤院': { eye: [42, 14, 36], target: [20, 8, 12], fov: 60 },
  '10-山墙与钟塔细部': { eye: [-26, 30, -24], target: [12, 24, 20], fov: 46 },
  '11-背街与后勤立面': { eye: [40, 12, 60], target: [18, 8, 24], fov: 58 },
  '12-俯视平面': { eye: [12, 96, 22], target: [12, 0, 22], fov: 50, up: [0, 0, -1] },
};

const manifest = { tag, label, world: WORLD, scan_bounds: BOX, captured_at: new Date().toISOString(), files: [] };
for (const [name, v] of Object.entries(VIEWS)) {
  const img = render(vol, { width: 1280, height: 800, background: [176, 202, 228], fog: { near: 40, far: 190, color: [186, 208, 230], strength: 0.8 }, ...v });
  const f = path.join(outDir, `${tag}-${name}.png`);
  writePNG(f, img);
  manifest.files.push({ view: name, file: path.basename(f), eye: v.eye, target: v.target, fov: v.fov });
  console.log('  ' + name);
}
fs.writeFileSync(path.join(outDir, `${tag}-manifest.json`), JSON.stringify(manifest, null, 1));
fs.writeFileSync(path.join(PROJECT, `jobs/_volume-${tag}.json`), JSON.stringify({ nx, ny, nz, bounds: vol.bounds }));
console.log('证据目录: ' + outDir);
