// 调试4：洞口洪泛边界追踪——从短廊南端 (-109,44) 向隧道洪泛，看断在哪一格
import fs from 'node:fs';

function 加载(p) {
  const r = JSON.parse(fs.readFileSync(p + '/result.json', 'utf8'));
  const s = r.scan, b = s.bounds;
  const W = b.x2 - b.x1 + 1, D = b.z2 - b.z1 + 1, H = b.y2 - b.y1 + 1;
  const grid = new Array(W * D * H);
  for (const [off, len, pi] of s.runs) for (let i = 0; i < len; i++) grid[off + i] = pi;
  return (x, y, z) => {
    if (x < b.x1 || x > b.x2 || z < b.z1 || z > b.z2 || y < b.y1 || y > b.y2) return 'minecraft:air';
    return s.palette[grid[((y - b.y1) * D + (z - b.z1)) * W + (x - b.x1)]];
  };
}
const C = 加载('D:/Games/Minecraft/AI工程/AI-Offline/jobs/2026-09-09T08-50-08-264Z-57685216-025a-4f2f-b54c-217dc13deef0');

const 可立 = new Set(['stone_bricks', 'stone', 'andesite', 'tuff', 'cobblestone', 'mossy_cobblestone', 'gravel',
  'grass_block', 'dirt', 'clay', 'white_concrete', 'light_gray_concrete', 'dark_oak_planks', 'polished_andesite',
  'bedrock', 'stone_brick_stairs', 'deepslate_tile_stairs', 'dark_oak_stairs'].map(s => 'minecraft:' + s));
const 是半砖 = n => n.includes('slab') && n.includes('type=bottom');
function 立足(x, z) {
  for (let g = 66; g >= 62; g--) {
    const b = C(x, g, z);
    const b0 = b.replace(/\[.*\]$/, '');
    const 实 = 可立.has(b0) || 是半砖(b) || (b.includes('stairs') && b.includes('half=bottom'));
    if (!实) continue;
    if (C(x, g + 1, z) === 'minecraft:air' && C(x, g + 2, z) === 'minecraft:air') return g;
  }
  return null;
}
// 沿 x=-109 从 z=40 到 z=62 逐格打印立足高
for (let z = 40; z <= 62; z++) {
  const g = 立足(-109, z);
  console.log('z' + String(z).padStart(3), 'x-109 立足g=' + (g === null ? '无' : g),
    '| y63=' + C(-109, 63, z).replace('minecraft:', '').replace(/\[.*\]/, ''),
    'y64=' + C(-109, 64, z).replace('minecraft:', '').replace(/\[.*\]/, ''),
    'y65=' + C(-109, 65, z).replace('minecraft:', '').replace(/\[.*\]/, ''));
}
