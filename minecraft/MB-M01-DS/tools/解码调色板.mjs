// 调色板验证（第 2 步）：解码 world RLE 扫描，得到"我方请求的状态 → Minecraft 实际状态"映射。
// 输出 research/palette.json：施工代码据此使用真实生效的状态（含自动连接规范化后的形态）。
import fs from 'node:fs';
import path from 'node:path';

const PROJECT = 'D:/Games/Minecraft/AI工程/MB-V110-M01-DS';
const gridFile = process.argv[2] || fs.readdirSync(path.join(PROJECT, 'jobs')).filter((f) => f.startsWith('_调色板网格-')).sort().pop();
const grid = JSON.parse(fs.readFileSync(path.join(PROJECT, 'jobs', gridFile), 'utf8'));
const sc = grid.scan;
const bounds = sc.bounds;
const palette = sc.palette;
const runs = sc.runs;

// 重建坐标 -> 调色板索引
const nx = bounds.x2 - bounds.x1 + 1;
const ny = bounds.y2 - bounds.y1 + 1;
const nz = bounds.z2 - bounds.z1 + 1;
const total = nx * ny * nz;
const idxAt = new Map();
let pos = 0;
for (const [offset, len, pi] of runs) {
  for (let k = 0; k < len; k++) {
    const lin = offset + k;
    const y = bounds.y1 + Math.floor(lin / (nz * nx));
    const rem = lin % (nz * nx);
    const z = bounds.z1 + Math.floor(rem / nx);
    const x = bounds.x1 + (rem % nx);
    idxAt.set(x + ',' + y + ',' + z, palette[pi]);
  }
  pos += len;
}
if (pos !== total) console.error('警告: RLE 长度 ' + pos + ' 与体积 ' + total + ' 不一致');

const mapping = {};
const notConverted = [];
const converted = [];
const missing = [];
const warnings = [];
for (const [key, meta] of grid.cells) {
  const observed = idxAt.get(key);
  if (!observed) { missing.push(meta.intended); continue; }
  mapping[meta.intended] = observed;
  if (observed === meta.intended) notConverted.push(meta.intended);
  else converted.push({ intended: meta.intended, observed });
  // 方块种类发生变化的视为异常（说明该状态被游戏替换）
  const idOf = (s) => s.slice(0, s.indexOf('[') < 0 ? undefined : s.indexOf('['));
  if (idOf(observed) !== idOf(meta.intended)) warnings.push({ intended: meta.intended, observed, kind: 'BLOCK_CHANGED' });
}

const out = {
  generated_from_job: grid.job_directory,
  generated_at: new Date().toISOString(),
  total_requested: grid.cells.length,
  exact: notConverted.length,
  normalized: converted.length,
  missing: missing.length,
  block_changed: warnings.length,
  skipped_by_policy: grid.skipped,
  warnings,
  mapping,
  normalized_detail: converted,
};
fs.writeFileSync(path.join(PROJECT, 'research/palette.json'), JSON.stringify(out, null, 1));
console.log('请求状态 ' + out.total_requested + '  完全一致 ' + out.exact + '  被规范化 ' + out.normalized + '  缺失 ' + out.missing + '  方块被替换 ' + out.block_changed);
if (warnings.length) { console.log('方块被替换的前 20 条:'); for (const w of warnings.slice(0, 20)) console.log('  ' + w.intended + ' -> ' + w.observed); }
console.log('\n被规范化的明细（应主要为 wall / fence / stair / pane 的自动连接）:');
for (const c of converted.slice(0, 30)) console.log('  ' + c.intended + '\n    -> ' + c.observed);
