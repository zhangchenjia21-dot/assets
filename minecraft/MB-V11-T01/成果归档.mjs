import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {gzipSync,gunzipSync} from 'node:zlib';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),dest=path.resolve(root,'../发布/assets/minecraft/MB-V11-T01');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const raw=fs.readFileSync(path.join(root,'存档回读方块.json')),gz=gzipSync(raw,{level:9});if(!gunzipSync(gz).equals(raw))throw Error('压缩回读不一致');
fs.writeFileSync(path.join(root,'存档回读方块.json.gz'),gz);fs.mkdirSync(dest,{recursive:true});
const files=['Completion Report.md','研究与设计.md','复核说明.md','园林生成.mjs','阶段施工.mjs','存档审计.mjs','局部修正.mjs','空间绘制.py','成果归档.mjs','阶段清单.json','修正批次.json','存档回读方块.json.gz'];
for(let i=1;i<=4;i++)for(const prefix of['结果','审计','写入目标','作业'])files.push(`${prefix}-${i}.json`);
for(const f of files)fs.copyFileSync(path.join(root,f),path.join(dest,f));
// 当前 Windows Node 的 cpSync 在目录复制时进程异常退出，按显式目录枚举复制普通文件。
function copyDir(src,dst){fs.mkdirSync(dst,{recursive:true});for(const e of fs.readdirSync(src,{withFileTypes:true})){const a=path.join(src,e.name),b=path.join(dst,e.name);if(e.isDirectory())copyDir(a,b);else if(e.isFile())fs.copyFileSync(a,b);else throw Error('任务归档不接受链接');}}
const blueprintFiles=new Set(JSON.parse(fs.readFileSync(path.join(root,'阶段清单.json'),'utf8')).stages.flatMap(s=>s.files));
fs.mkdirSync(path.join(dest,'蓝图'),{recursive:true});
for(const f of blueprintFiles)fs.copyFileSync(path.join(root,f),path.join(dest,f));
for(const f of fs.readdirSync(path.join(dest,'蓝图')))if(!blueprintFiles.has('蓝图/'+f))fs.unlinkSync(path.join(dest,'蓝图',f));
for(const d of['最终','实建阶段1','实建阶段2','实建阶段3'])copyDir(path.join(root,'证据',d),path.join(dest,'证据',d));
const entries=[];function visit(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,e.name);if(e.isDirectory())visit(file);else if(e.name!=='SHA256SUMS.json')entries.push({file:path.relative(dest,file).replaceAll('\\','/'),sha256:hash(fs.readFileSync(file)),bytes:fs.statSync(file).size});}}visit(dest);
const manifest={world_data_is_not_full_save:true,uncompressed_sha256:hash(raw),compressed_sha256:hash(gz),uncompressed_bytes:raw.length,files:entries};fs.writeFileSync(path.join(dest,'SHA256SUMS.json'),JSON.stringify(manifest,null,2));fs.copyFileSync(path.join(dest,'SHA256SUMS.json'),path.join(root,'SHA256SUMS.json'));console.log({files:entries.length,raw_bytes:raw.length,gzip_bytes:gz.length,destination:dest});
