// 仅核对本目录的可重复性、文件完整性与声明边界；不会授予回归结论。
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
const outputs=['设计体素.json','设计几何.json','设计核验.json','设计预览.html','体量轴测.svg','剖切轴测.svg','平面-上层.svg','平面-下层.svg','平面-作坊.svg','剖面-家庭横向.svg','剖面-楼梯.svg'];
const before=outputs.map(hash);
for(const name of ['设计生成.mjs','制图与核验.mjs'])execFileSync(process.execPath,[path.join(root,name)],{cwd:root,stdio:'pipe'});
if(outputs.some((p,i)=>hash(p)!==before[i]))throw Error('non-deterministic or stale artifacts');
const c=JSON.parse(fs.readFileSync(path.join(root,'设计核验.json'),'utf8'));
for(const k of ['outside_mask','protected_mask_intrusions','yard_roof_intrusions','proposed_below_observed_ground'])if(c.checks[k]!==0)throw Error(k);
if(c.checks.private_yard_area!==18||c.world_writes!==0||!c.regression_verdict.startsWith('NOT_ASSIGNED'))throw Error('boundary assertion');
for(const p of ['README.md','建筑设计.md','handoff-consumption-record.md']){
 const text=fs.readFileSync(path.join(root,p),'utf8');
 for(const hit of text.matchAll(/\]\(([^)]+)\)/g))if(!hit[1].includes('://')&&!fs.existsSync(path.join(root,hit[1])))throw Error('broken link '+hit[1]);
}
function files(dir=''){return fs.readdirSync(path.join(root,dir),{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name)):[path.join(dir,e.name)]);}
const list=files().filter(p=>p!=='manifest.json').sort().map(p=>({path:p.replaceAll('\\','/'),bytes:fs.statSync(path.join(root,p)).size,sha256:hash(p)}));
fs.writeFileSync(path.join(root,'manifest.json'),JSON.stringify({test:'MP-I01R',design_state:c.design_state,regression_verdict:'NOT_ASSIGNED',world_writes:0,deterministic_rebuild:true,files:list},null,2)+'\n');
console.log(JSON.stringify({files:list.length,bytes:list.reduce((a,b)=>a+b.bytes,0),deterministic_rebuild:true,regression_verdict:'NOT_ASSIGNED',world_writes:0}));
