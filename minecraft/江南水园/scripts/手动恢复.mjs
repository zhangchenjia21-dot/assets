/**
 * 手动恢复：robocopy 镜像 + 官方 inventory 哈希校验。
 * 用于执行器自动 restore 受 cpSync 原生崩溃影响时的灾难恢复。
 * 用法：node 手动恢复.mjs <备份目录> <备份清单backup.json>
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import { inventory } from '../../AI-Offline/L1_器件层/存档快照器.mjs';

const [, , backup, manifestPath] = process.argv;
// 世界路径从备份清单取，避免写死不同工程导致误写其他存档
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const world = manifest.world_path;
if (!world || !/苏州园林|江南水园/.test(world)) throw new Error('路径保护: ' + world);
// robocopy 镜像（排除 session.lock）；退出码 <8 即成功
const rc = spawnSync('robocopy', [backup, world, '/MIR', '/XF', 'session.lock', '/NFL', '/NDL', '/NJH', '/NJS'], { stdio: 'pipe' });
if (rc.status === null || rc.status >= 8) { console.log('ROBOCOPY_FAIL code=' + rc.status); process.exit(1); }
const a = inventory(world), m = manifest.inventory;
const ok = JSON.stringify(a) === JSON.stringify(m);
console.log(ok ? `RESTORE_VERIFIED files=${a.length}` : 'RESTORE_MISMATCH');
if (!ok) {
  const mm = new Map(m.map(r => [r.path, r.sha256]));
  for (const r of a) if (mm.get(r.path) !== r.sha256) console.log('DIFF', r.path);
  const am = new Set(a.map(r => r.path));
  for (const r of m) if (!am.has(r.path)) console.log('MISSING', r.path);
  process.exitCode = 1;
}
