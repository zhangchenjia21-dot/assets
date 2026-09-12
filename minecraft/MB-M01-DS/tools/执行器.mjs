// 施工执行器封装：调用官方离线执行器（Bootstrap/世界命令.mjs）。
// 沙箱约束：本环境禁止通过管道捕获子进程输出，因此改用"脚本重定向到文件 + 读文件"的方式。
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export const PROJECT = 'D:/Games/Minecraft/AI工程/MB-V110-M01-DS';
export const CLI = 'D:/Games/Minecraft/AI工程/AI-Offline/Bootstrap/世界命令.mjs';
export const AI_OFFLINE = 'D:/Games/Minecraft/AI工程/AI-Offline';
export const WORLD = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V110-M01-DS-汉萨市政厅';

function psQuote(s) {
  return "'" + String(s).replace(/'/g, "''") + "'";
}

/** 通过 pwsh 重定向调用世界命令.mjs，返回其 stdout（JSON 文本）。 */
function callCli(args) {
  const outFile = path.join(PROJECT, 'jobs', `_cli-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.out`);
  fs.mkdirSync(path.dirname(outFile), { recursive: true });
  const cmd = `& node ${psQuote(CLI)} ${args.map(psQuote).join(' ')} *> ${psQuote(outFile)}; exit $LASTEXITCODE`;
  const p = spawnSync('pwsh', ['-NoProfile', '-Command', cmd], { stdio: 'inherit' });
  const text = fs.existsSync(outFile) ? fs.readFileSync(outFile, 'utf8') : '';
  fs.unlinkSync(outFile);
  if (p.status !== 0) {
    const err = new Error('CLI_FAILED(' + p.status + '): ' + text.slice(-4000));
    err.cliOutput = text;
    throw err;
  }
  return text;
}

/** 执行器自身会检测残留 Java 进程；此处对该瞬时误报做有限重试（不掩盖真实失败）。 */
function callCliRetry(args, attempts = 6) {
  let last;
  for (let i = 0; i < attempts; i++) {
    try {
      return callCli(args);
    } catch (e) {
      last = e;
      const transient = /JAVA_RUNTIME_ACTIVE|EXECUTOR_BUSY|OFFLINE_RUNTIME_FAILED/.test(e.message);
      if (!transient || i === attempts - 1) throw e;
      const wait = 4000 * (i + 1);
      console.error(`  [执行器重试 ${i + 1}/${attempts - 1}] ${e.message.split('\n')[0]} 等待 ${wait}ms`);
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, wait);
    }
  }
  throw last;
}

/** 找出此刻最新的作业目录。 */
function latestJobDir(before) {
  const jobsRoot = path.join(AI_OFFLINE, 'jobs');
  const dirs = fs.readdirSync(jobsRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !before.has(d.name))
    .map((d) => ({ name: d.name, t: fs.statSync(path.join(jobsRoot, d.name)).mtimeMs }))
    .sort((a, b) => b.t - a.t);
  if (!dirs.length) throw new Error('NO_NEW_JOB_DIR');
  return path.join(jobsRoot, dirs[0].name);
}

/**
 * 执行一次离线作业。job 可含 create / phases / samples / scan / spawn / difficulty。
 * 返回 { result, jobDirectory, stdout }；失败时抛错并附带执行器输出。
 */
export function runJob(job, { label = 'job', worldPath = WORLD } = {}) {
  const dir = path.join(PROJECT, 'jobs');
  fs.mkdirSync(dir, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const jobFile = path.join(dir, `${stamp}_${label}.job.json`);
  fs.writeFileSync(jobFile, JSON.stringify({ world_path: worldPath, ...job }, null, 1));
  const jobsRoot = path.join(AI_OFFLINE, 'jobs');
  const before = new Set(fs.existsSync(jobsRoot) ? fs.readdirSync(jobsRoot) : []);
  const stdout = callCliRetry(['run-job', jobFile]);
  const jobDirectory = latestJobDir(before);
  const resultFile = path.join(jobDirectory, 'result.json');
  if (!fs.existsSync(resultFile)) {
    throw new Error('NO_RESULT: ' + jobDirectory + '\n' + stdout.slice(-3000) + '\n' + fs.readFileSync(path.join(jobDirectory, 'stderr.log'), 'utf8').slice(-4000));
  }
  const result = JSON.parse(fs.readFileSync(resultFile, 'utf8'));
  fs.writeFileSync(path.join(dir, `${stamp}_${label}.result.json`), JSON.stringify(result, null, 1));
  return { result, jobDirectory, jobFile, stamp, stdout };
}

export function worldStatus(worldPath = WORLD) {
  return JSON.parse(callCli(['world-status', worldPath]).trim().split('\n').pop());
}

export function backupWorld(dest, worldPath = WORLD) {
  return JSON.parse(callCli(['backup-world', worldPath, dest]).trim().split('\n').pop());
}

export function restoreWorld(snapshot, worldPath = WORLD) {
  return JSON.parse(callCli(['restore-world', worldPath, snapshot]).trim().split('\n').pop());
}
