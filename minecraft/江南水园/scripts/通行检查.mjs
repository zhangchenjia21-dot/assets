/**
 * 通行检查（多高度洪泛）：解码 result.json 的 scan，逐格求"可站立面"列表（自底向上
 * 每个实心地面且其上一格可通行的高度），从出生点地面洪泛，相邻可走格高度差 ≤1 视为可跨步。
 * 水面/荷盖/围栏/玻璃/树叶/树干为阻挡，拱桥/台阶自动识别（多高度），屋顶为独立高度层不干扰地面。
 * 关键节点以"最低可站面（地面）"是否可达为准。
 * 用法：node 通行检查.mjs <result.json> <出生x> <出生z>
 */
import fs from 'node:fs';

const [, , resultPath, sx, sz] = process.argv;
const result = JSON.parse(fs.readFileSync(resultPath, 'utf8'));
const b = result.scan.bounds;
const [x1, x2, z1, z2, y1, y2] = [b.x1, b.x2, b.z1, b.z2, b.y1, b.y2];
const W = x2 - x1 + 1, D = z2 - z1 + 1, H = y2 - y1 + 1;
const grid = new Array(W * D * H);
const palette = result.scan.palette;
for (const [off, len, pi] of result.scan.runs) for (let i = 0; i < len; i++) grid[off + i] = pi;
const at = (x, y, z) => (x < x1 || x > x2 || z < z1 || z > z2 || y < y1 || y > y2) ? null : palette[grid[((y - y1) * D + (z - z1)) * W + (x - x1)]];

const 阻挡 = (blk) => !blk || blk === 'minecraft:air' || blk === 'minecraft:water[level=0]' || blk === 'minecraft:lily_pad' || /glass_pane|_fence|_leaves|big_dripleaf|bamboo|end_rod/.test(blk);
const 可站 = (blk) => blk === 'minecraft:air' || /_stairs/.test(blk || '') || blk === null;

// 每格的可站面高度列表（自底向上）
const 面 = new Map();
for (let x = x1; x <= x2; x++) for (let z = z1; z <= z2; z++) {
  const ys = [];
  for (let y = y1; y <= y2; y++) if (!阻挡(at(x, y, z)) && 可站(at(x, y + 1, z))) ys.push(y);
  if (ys.length) 面.set(x + ',' + z, ys);
}

const 起点 = [Number(sx), Number(sz)];
const seen = new Set();
const q = [];
const 起点面 = 面.get(起点.join(','));
const 起点y = 起点面 ? 起点面[0] : null; // 用最低可站面
if (起点y !== null) { seen.add(起点.join(',') + '@' + 起点y); q.push([起点[0], 起点[1], 起点y]); }
while (q.length) {
  const [x, z, y] = q.pop();
  for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
    const nx = x + dx, nz = z + dz, k = nx + ',' + nz, ys = 面.get(k);
    if (!ys) continue;
    for (const ny of ys) {
      if (Math.abs(ny - y) > 1) continue;
      const sk = k + '@' + ny;
      if (seen.has(sk)) continue;
      seen.add(sk); q.push([nx, nz, ny]);
    }
  }
}

const 节点 = [
  ['南门', 0, 63], ['花厅', 0, 52], ['影壁过道', 0, 58],
  ['湖心岛(澄心堂)', 0, -6], ['东岛(一镜亭)', 26, -4], ['西岛(沧浪亭)', -28, -6], ['南岛(笠亭)', 4, 12],
  ['涵碧榭', 46, 2], ['芥舟石舫', -48, -12], ['望月台', 16, -36],
  ['河房东', -49, -44], ['河房西', -60, -44], ['河街上', -52, 10], ['河街北', -52, -44],
  ['北岸', 0, -34], ['东岸', 50, 4],
  ['竹院方亭', 50, -52], ['花院方亭', 50, 52], ['东带方亭', 52, -18], ['沿墙石径', 0, -60], ['竹院月洞', 42, -52],
];
let 全达 = true;
for (const [名, x, z] of 节点) {
  const ys = 面.get(x + ',' + z);
  const ok = ys && seen.has(x + ',' + z + '@' + ys[0]); // 以最低面（地面）判可达
  if (!ok) 全达 = false;
  console.log((ok ? '可达' : '不可达') + '  ' + 名 + ' (' + x + ',' + z + ')');
}
console.log('连通状态数=' + seen.size, '全部可达=' + (全达 ? '是' : '否'));
process.exitCode = 全达 ? 0 : 2;
