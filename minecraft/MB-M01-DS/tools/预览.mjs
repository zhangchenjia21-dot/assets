// 预览渲染：从当前蓝本生成多机位透视图，供 Builder Core 设计判断与基线/终稿同机位对比。
import fs from 'node:fs';
import path from 'node:path';
import { generateBlueprint } from './蓝本.mjs';
import { fromBuilder, render, writePNG } from './体素渲染.mjs';
import { PROJECT } from './执行器.mjs';

const outDir = path.join(PROJECT, 'evidence/preview');
fs.mkdirSync(outDir, { recursive: true });
const b = generateBlueprint();
const vol = fromBuilder(b);
console.log('体素范围: x ' + vol.bounds.x1 + '..' + vol.bounds.x2 + ' y ' + vol.bounds.y1 + '..' + vol.bounds.y2 + ' z ' + vol.bounds.z1 + '..' + vol.bounds.z2);

const VIEWS = {
  // 城市接近：自广场西南方向看主立面（大楼梯门廊 + 拱廊 + 山墙）
  'A-城市接近': { eye: [-30, 14, -46], target: [12, 10, 22], fov: 58 },
  // 正面：自广场正对建筑北面
  'B-正面': { eye: [-4, 12, -34], target: [14, 10, 22], fov: 62 },
  // 整体体量：斜俯视（可见屋面与山墙）
  'C-整体体量': { eye: [-46, 46, -44], target: [14, 12, 22], fov: 52 },
  // 侧后方：自北院看后勤翼与南立面
  'D-后勤侧': { eye: [52, 22, 58], target: [16, 9, 22], fov: 60 },
  // 近景：门廊入口
  'E-门廊近景': { eye: [-10, 5, -16], target: [4, 5, -2], fov: 70 },
  // 剖面透视：南墙以上略去时用高视点看内部（近似 section 透视）
  'F-俯视平面感': { eye: [14, 78, 22], target: [14, 0, 22], fov: 55, up: [0, 0, -1] },
};

for (const [name, v] of Object.entries(VIEWS)) {
  const t0 = Date.now();
  const img = render(vol, { width: 1100, height: 720, background: [168, 196, 224], fog: { near: 30, far: 140, color: [180, 205, 230], strength: 0.85 }, ...v });
  const f = path.join(outDir, `preview-${name}.png`);
  writePNG(f, img);
  console.log(name + '  ' + Math.round((Date.now() - t0) / 100) / 10 + 's  -> ' + f);
}
