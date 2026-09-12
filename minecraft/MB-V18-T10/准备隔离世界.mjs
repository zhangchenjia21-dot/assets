import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import zlib from 'node:zlib';
import {snapshot,qualifyExistingWorld} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(new URL(import.meta.url).pathname).replace(/^\/([A-Z]:)/,'$1');
const R=decodeURIComponent(root),source='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V17-T09-罗马浴场',instance=R+'/实例',target=instance+'/saves/MB-V18-T10-罗马浴场精修',runtime=path.dirname(path.dirname(source));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function inventory(d){const out={};function walk(p){for(const e of fs.readdirSync(p,{withFileTypes:true})){const f=path.join(p,e.name);if(e.isSymbolicLink())throw Error('SYMLINK');if(e.isDirectory())walk(f);else out[path.relative(d,f)]=hash(fs.readFileSync(f));}}walk(d);return out;}
const write=(n,v)=>fs.writeFileSync(R+'/证据/'+n,JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2));
fs.mkdirSync(R+'/证据',{recursive:true});const resume=process.argv[2]==='resume-verified-copy';if(fs.existsSync(target)&&!resume)throw Error('TARGET_ALREADY_EXISTS');
const d=readNBT(fs.readFileSync(source+'/level.dat')).Data;if(d.LevelName!=='MB-V17-T09-罗马浴场')throw Error('SOURCE_IDENTITY');
const before=resume?JSON.parse(fs.readFileSync(R+'/证据/来源文件基准.json')):inventory(source);if(JSON.stringify(before)!==JSON.stringify(inventory(source)))throw Error('SOURCE_CHANGED');if(!resume)write('来源文件基准.json',before);
if(!resume)await snapshot(source,target);const copied=inventory(target);for(const [p,h] of Object.entries(before))if(p!=='session.lock'&&copied[p]!==h)throw Error('COPY_MISMATCH');
// 仅更改副本 level.dat 的唯一 LevelName 字符串标签；不写任何 region/POI/entity 数据。
const f=target+'/level.dat',raw=zlib.gunzipSync(fs.readFileSync(f));function tag(s){const name=Buffer.from('LevelName'),val=Buffer.from(s),b=Buffer.alloc(1+2+name.length+2+val.length);b[0]=8;b.writeUInt16BE(name.length,1);name.copy(b,3);b.writeUInt16BE(val.length,3+name.length);val.copy(b,5+name.length);return b;}
const old=tag(d.LevelName),next=tag('MB-V18-T10-罗马浴场精修'),i=raw.indexOf(old);if(i<0||raw.indexOf(old,i+1)>=0)throw Error('LEVELNAME_NOT_UNIQUE');fs.writeFileSync(f,zlib.gzipSync(Buffer.concat([raw.subarray(0,i),next,raw.subarray(i+old.length)])));
if(readNBT(fs.readFileSync(f)).Data.LevelName!=='MB-V18-T10-罗马浴场精修')throw Error('TARGET_NAME');
for(const n of ['mods','config'])fs.cpSync(runtime+'/'+n,instance+'/'+n,{recursive:true,errorOnExist:true,force:false});
write('复制与身份.json',{source,target,source_name:d.LevelName,target_name:'MB-V18-T10-罗马浴场精修',copy_hash_verified:true,metadata_change:'LevelName only',profile_source:runtime});
const q=await qualifyExistingWorld(target,instance,R+'/资格验证客户端');write('运行配置资格.json',q);
const after=inventory(source);write('来源复制后核验.json',{unchanged:JSON.stringify(before)===JSON.stringify(after),files:Object.keys(before).length});if(JSON.stringify(before)!==JSON.stringify(after))throw Error('SOURCE_CHANGED');console.log('T10 isolated and qualified');
