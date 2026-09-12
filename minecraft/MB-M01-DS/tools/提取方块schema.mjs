// 从 Minecraft 26.2 客户端 jar 提取权威方块状态 schema（方块名 -> 属性 -> 取值顺序）
// 用途：生成规范状态字符串，避免猜测属性顺序导致解析失败。
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const JAR = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/26.2-Fabric 0.19.5.jar';
const OUT = process.argv[2] || 'blocks_schema.json';

// 用 PowerShell 内联解压（避免依赖第三方 zip 库）
const ps = `
Add-Type -AssemblyName System.IO.Compression.FileSystem
$jar = '${JAR.replace(/\//g, '\\')}'
$out = '${path.resolve(OUT).replace(/\//g, '\\')}.raw'
if (Test-Path $out) { Remove-Item -Recurse -Force $out }
New-Item -ItemType Directory -Force -Path $out | Out-Null
$z = [System.IO.Compression.ZipFile]::OpenRead($jar)
foreach ($e in $z.Entries) {
  if ($e.FullName -like 'assets/minecraft/blockstates/*.json' -and $e.Length -gt 0) {
    $dest = Join-Path $out ([System.IO.Path]::GetFileName($e.FullName))
    [System.IO.Compression.ZipFileExtensions]::ExtractToFile($e, $dest, $true)
  }
}
$z.Dispose()
Write-Output 'ok'
`;
const rawDir = path.resolve(OUT) + '.raw';
execFileSync('pwsh', ['-NoProfile', '-Command', ps], { stdio: 'inherit' });

const schema = {};
for (const f of fs.readdirSync(rawDir)) {
  if (!f.endsWith('.json')) continue;
  const name = 'minecraft:' + f.replace(/\.json$/, '');
  let data;
  try {
    data = JSON.parse(fs.readFileSync(path.join(rawDir, f), 'utf8'));
  } catch {
    continue;
  }
  const props = {};
  const variants = data.variants ? Object.keys(data.variants) : [];
  const parts = data.multipart ? data.multipart.flatMap((p) => (p.when ? flattenWhen(p.when) : [])) : [];
  for (const key of [...variants, ...parts]) {
    for (const kv of key.split(',')) {
      const [k, v] = kv.split('=');
      if (!k || v === undefined) continue;
      const kk = k.trim();
      if (!props[kk]) props[kk] = new Set();
      props[kk].add(v.trim());
    }
  }
  const out = {};
  for (const [k, set] of Object.entries(props)) out[k] = [...set].sort();
  schema[name] = { properties: out, default: data.variants ? Object.keys(data.variants)[0] : null };
}

function flattenWhen(when) {
  if (Array.isArray(when)) return when.flatMap(flattenWhen);
  if (when.OR) return when.OR.flatMap(flattenWhen);
  if (when.AND) return when.AND.flatMap(flattenWhen);
  if (typeof when === 'object') return [Object.entries(when).map(([k, v]) => `${k}=${v}`).join(',')];
  return [];
}

fs.writeFileSync(OUT, JSON.stringify(schema, null, 1));
console.log('blocks=' + Object.keys(schema).length + ' -> ' + OUT);
