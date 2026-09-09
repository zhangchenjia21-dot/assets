// 只读校验：当前存档文件是否与指定作业 backup.json 清单逐字节一致
// 用法: node scripts/校验存档.mjs <job目录或backup.json路径>
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const 存档 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const 入 = process.argv[2];
const 清单路径 = 入.endsWith('.json') ? 入 : path.join(入, 'backup.json');
const 清单 = JSON.parse(fs.readFileSync(清单路径, 'utf8'));

let 异 = 0;
for (const it of 清单.inventory) {
  const rel = it.path.split('\\').join('/');
  const p = path.join(存档, rel);
  if (!fs.existsSync(p)) { console.log('缺失', rel); 异++; continue; }
  const h = crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
  if (h !== it.sha256) { console.log('不一致', rel); 异++; }
}
console.log(异 === 0 ? 'VERIFIED: 当前存档与清单逐字节一致' : `MISMATCH: 差异 ${异} 处`);
process.exit(异 === 0 ? 0 : 1);
