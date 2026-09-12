import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';import {spawnSync} from 'node:child_process';
import {snapshot,qualifyExistingWorld,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const R=path.dirname(fileURLToPath(import.meta.url)),src='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V19-T11-京町家',instance='D:/Games/Minecraft/.minecraft/versions/MB-V110-T12-隔离实例',dst=instance+'/saves/MB-V110-T12-京町家修复';
const write=(n,v)=>fs.writeFileSync(R+'/证据/'+n,JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2));
function hashes(dir){let out={};for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.isSymbolicLink())throw Error('SYMLINK');const f=path.join(dir,e.name);if(e.isDirectory())for(const [k,v]of Object.entries(hashes(f)))out[e.name+'/'+k]=v;else out[e.name]=crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');}return out;}
fs.mkdirSync(R+'/证据',{recursive:true});if(fs.existsSync(dst)||fs.existsSync(instance))throw Error('DEST_EXISTS');
if(readNBT(fs.readFileSync(src+'/level.dat')).Data.LevelName!=='MB-V19-T11-京町家')throw Error('SOURCE_IDENTITY');
await worldStatus(src);const before=hashes(src);write('来源世界文件哈希.json',before);
await snapshot(src,dst);const copy=hashes(dst);for(const [f,h]of Object.entries(before))if(f!=='session.lock'&&copy[f]!==h)throw Error('COPY_MISMATCH');
const rename=spawnSync('C:/Users/MRVHREVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',[R+'/重命名副本.py'],{encoding:'utf8',windowsHide:true});if(rename.status!==0)throw Error(rename.stderr);
if(readNBT(fs.readFileSync(dst+'/level.dat')).Data.LevelName!==path.basename(dst))throw Error('DEST_IDENTITY');
for(const n of ['mods','config'])fs.cpSync(path.resolve(R,'../AI-Offline/runtime',n),path.join(instance,n),{recursive:true,errorOnExist:true,force:false});
write('复制验证.json',{source:src,destination:dst,source_files:Object.keys(before).length,copy_byte_identical_except_lock:true,name_changed_only:true});
const qualification=await qualifyExistingWorld(dst,instance,R+'/隔离资格验证');write('资格验证摘要.json',{status:qualification.status,world_path:qualification.world_path,qualification:qualification.qualification});
if(JSON.stringify(before)!==JSON.stringify(hashes(src)))throw Error('SOURCE_CHANGED');
write('来源未改验证.json',{source:src,all_files_hash_identical:true,includes_session_lock:true,world_writes:0});console.log('T12 independent copy qualified; source hash unchanged');
