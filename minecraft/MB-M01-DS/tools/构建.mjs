// ============================================================================
// 施工入口（CLI）：
//   node tools/构建.mjs report        仅生成并自检（不写世界），输出报告与 ASCII 剖面
//   node tools/构建.mjs create [S..]  新建独立测试世界并写入首阶段
//   node tools/构建.mjs build S..     把指定阶段写入已登记世界
//   node tools/构建.mjs build all     依次写入全部阶段
// ============================================================================
import fs from 'node:fs';
import path from 'node:path';
import { AIR } from './几何核心.mjs';
import { spawnSync } from 'node:child_process';
import { fromBuilder, sliceY, sliceZ, sliceX } from './体素渲染.mjs';
import { runJob, PROJECT, WORLD } from './执行器.mjs';
import { generateBlueprint, STAGES } from './蓝本.mjs';

const cmd = process.argv[2] || 'report';
const b = generateBlueprint();
const outDir = path.join(PROJECT, 'evidence/preview');
fs.mkdirSync(outDir, { recursive: true });

/** Windows 上 session.lock 可能被占用；交给 pwsh 删除以避免 Node 递归删除的稳定性问题。 */
function removeDir(dir) {
  if (!fs.existsSync(dir)) return;
  const q = (s) => "'" + String(s).replace(/'/g, "''") + "'";
  const p = spawnSync('pwsh', ['-NoProfile', '-Command',
    `Remove-Item -LiteralPath ${q(dir)} -Recurse -Force -ErrorAction SilentlyContinue; if (Test-Path -LiteralPath ${q(dir)}) { exit 1 } else { exit 0 }`],
    { stdio: 'inherit' });
  if (fs.existsSync(dir)) {
    const tmp = dir + '.deleting-' + Date.now();
    fs.renameSync(dir, tmp);
    spawnSync('pwsh', ['-NoProfile', '-Command', `Remove-Item -LiteralPath ${q(tmp)} -Recurse -Force -ErrorAction SilentlyContinue`], { stdio: 'inherit' });
  }
  if (fs.existsSync(dir)) throw new Error('WORLD_DELETE_FAILED: ' + dir);
}

if (cmd === 'report') {
  const rep = b.report();
  console.log('=== 蓝本报告 ===');
  console.log('方块数: ' + rep.blocks + '   状态种类: ' + rep.distinctStates);
  console.log('范围: x ' + rep.bounds.minX + '..' + rep.bounds.maxX + '  y ' + rep.bounds.minY + '..' + rep.bounds.maxY + '  z ' + rep.bounds.minZ + '..' + rep.bounds.maxZ);
  console.log('冲突(非预期二次写入): ' + rep.conflicts + '   显式覆盖: ' + rep.overrides + '   分层重绘: ' + rep.paintOver);
  console.log('阶段: ' + rep.stages.map(([k, v]) => k + '=' + v).join('  '));
  console.log('覆盖原因统计: ' + rep.overridesByReason.map(([k, v]) => k + '×' + v).join(', '));
  console.log('主要方块:');
  for (const [st, n] of rep.top.slice(0, 16)) console.log('   ' + String(n).padStart(7) + '  ' + st);
  if (rep.conflicts) {
    console.log('冲突明细（前 20）:');
    for (const x of b.conflicts.slice(0, 20)) console.log('   ' + x.stage + ' ' + x.pos.join(',') + '  ' + x.from + ' -> ' + x.to);
  }
  fs.writeFileSync(path.join(outDir, 'blueprint-report.json'), JSON.stringify({ report: rep, conflicts: b.conflicts.slice(0, 200), overrides: b.overrides.slice(0, 2000) }, null, 1));
  const vol = fromBuilder(b);
  fs.writeFileSync(path.join(outDir, 'section-z22.txt'), sliceZ(vol, 22, { x1: -1, x2: 27, y1: -6, y2: 34 }));
  fs.writeFileSync(path.join(outDir, 'section-z8.txt'), sliceZ(vol, 8, { x1: -1, x2: 27, y1: -6, y2: 34 }));
  fs.writeFileSync(path.join(outDir, 'section-x12.txt'), sliceX(vol, 12, { z1: -10, z2: 50, y1: -6, y2: 34 }));
  fs.writeFileSync(path.join(outDir, 'plan-y1.txt'), sliceY(vol, 1, { x1: -6, x2: 27, z1: -12, z2: 50 }));
  fs.writeFileSync(path.join(outDir, 'plan-y7.txt'), sliceY(vol, 7, { x1: -6, x2: 27, z1: -12, z2: 50 }));
  console.log('\n=== 剖面 z=22（南北向，向北为右）===');
  console.log(fs.readFileSync(path.join(outDir, 'section-z22.txt'), 'utf8'));
} else if (cmd === 'create') {
  const first = process.argv[3] || STAGES[0];
  const phase = b.phases({ stages: [first] });
  console.log('创建世界: ' + WORLD + '   首阶段: ' + first);
  const { result, stamp, jobDirectory } = runJob(
    { create: { type: 'superflat', seed: 20260912 }, spawn: [10, 1, -14], phases: [phase] },
    { label: '创建世界+' + first }
  );
  console.log('作业 ' + stamp + ' status=' + result.status + ' generator=' + result.generator + ' 写入=' + result.changed_blocks + ' 耗时=' + Math.round(result.wall_seconds) + 's');
  console.log('作业目录: ' + jobDirectory);
  fs.writeFileSync(path.join(PROJECT, 'evidence/world-identity.json'), JSON.stringify({
    world_path: WORLD, created_job: jobDirectory, stamp, generator: result.generator,
    status: result.status, changed_blocks: result.changed_blocks, world_path_reported: result.world_path, first_stage: first,
  }, null, 1));
} else if (cmd === 'rebuild') {
  // 阶段几何改动后，旧世界的方块不会被自动清除；此处做"备份 → 删除 → 全新重建"的确定性重来。
  const { backupWorld, restoreWorld } = await import('./执行器.mjs');
  const snaps = path.join(PROJECT, 'snapshots');
  fs.mkdirSync(snaps, { recursive: true });
  const snapPath = path.join(snaps, 'pre-rebuild-' + new Date().toISOString().replace(/[:.]/g, '-'));
  let bk = null;
  if (fs.existsSync(WORLD)) {
    console.log('1) 备份当前世界到 ' + snapPath);
    const bk = backupWorld(snapPath);
    console.log('   文件 ' + bk.files + '  哈希校验 ' + bk.sha256_verified);
  } else {
    console.log('1) 世界目录不存在，跳过备份（首次创建或已清理）');
  }
  console.log('2) 删除旧世界目录');
  removeDir(WORLD);
  const all = b.phases({});
  console.log('3) 全新创建并一次写入全部阶段：调色板 ' + all.palette.length + ' 种，操作 ' + all.operations.length + ' 条');
  const { result, stamp, jobDirectory } = runJob(
    { create: { type: 'superflat', seed: 20260912 }, spawn: [10, 1, -14], phases: [all] },
    { label: '全新重建' }
  );
  console.log('   作业 ' + stamp + ' status=' + result.status + ' generator=' + result.generator + ' 写入=' + result.changed_blocks + ' 耗时=' + Math.round(result.wall_seconds) + 's');
  fs.writeFileSync(path.join(PROJECT, 'evidence/world-identity.json'), JSON.stringify({
    world_path: WORLD, created_job: jobDirectory, stamp, generator: result.generator,
    status: result.status, changed_blocks: result.changed_blocks, world_path_reported: result.world_path,
    rebuild_backup: fs.existsSync(snapPath) ? { path: snapPath, files: bk?.files, sha256_verified: bk?.sha256_verified } : null,
    rebuilt_at: new Date().toISOString(), stages: STAGES,
  }, null, 1));
  console.log('世界身份证据: evidence/world-identity.json');
} else if (cmd === 'rebuild-core') {
  // 全新重建为 SPATIAL_COMPLETE 状态（只写 Builder Core 阶段），用于生成 Finishing 前基线证据。
  const { CORE_STAGES } = await import('./蓝本.mjs');
  const { backupWorld } = await import('./执行器.mjs');
  const snaps = path.join(PROJECT, 'snapshots');
  fs.mkdirSync(snaps, { recursive: true });
  const snapPath = path.join(snaps, 'pre-rebuild-core-' + new Date().toISOString().replace(/[:.]/g, '-'));
  if (fs.existsSync(WORLD)) {
    console.log('1) 备份当前世界到 ' + snapPath);
    const bk = backupWorld(snapPath);
    console.log('   文件 ' + bk.files + '  哈希校验 ' + bk.sha256_verified);
  } else console.log('1) 世界目录不存在，跳过备份');
  console.log('2) 删除旧世界目录');
  removeDir(WORLD);
  const all = b.phases({ stages: CORE_STAGES });
  console.log('3) 全新创建并写入 Builder Core 阶段：调色板 ' + all.palette.length + ' 种，操作 ' + all.operations.length + ' 条');
  const { result, stamp, jobDirectory } = runJob(
    { create: { type: 'superflat', seed: 20260912 }, spawn: [10, 1, -14], phases: [all] },
    { label: 'SPATIAL_COMPLETE基线' }
  );
  console.log('   作业 ' + stamp + ' status=' + result.status + ' 写入=' + result.changed_blocks + ' 耗时=' + Math.round(result.wall_seconds) + 's');
  fs.writeFileSync(path.join(PROJECT, 'evidence/baseline/baseline-world.json'), JSON.stringify({
    world_path: WORLD, job: jobDirectory, stamp, stage: 'SPATIAL_COMPLETE',
    changed_blocks: result.changed_blocks, generator: result.generator, captured_at: new Date().toISOString(),
  }, null, 1));
} else if (cmd === 'build') {
  const targets = process.argv.slice(3);
  const list = targets[0] === 'all' ? STAGES : targets;
  for (const stage of list) {
    const phase = b.phases({ stages: [stage] });
    const anyAir = phase.palette.includes(AIR);
    console.log('--- 阶段 ' + stage + '：调色板 ' + phase.palette.length + ' 种，操作 ' + phase.operations.length + ' 条' + (anyAir ? '（含清除）' : ''));
    const { result, stamp, jobDirectory } = runJob({ phases: [phase] }, { label: '建造-' + stage });
    console.log('    ' + stamp + ' status=' + result.status + ' 写入=' + result.changed_blocks + ' 不符=' + result.mismatches + ' 耗时=' + Math.round(result.wall_seconds) + 's');
    if (result.status !== 'PASS') { console.error('阶段失败，停止。作业目录: ' + jobDirectory); process.exit(1); }
  }
  console.log('全部阶段完成。');
}
