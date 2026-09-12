import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';
import {qualifyExistingWorld} from '../AI-Offline/L3_外交层/离线执行接口.mjs';import {readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const R=path.dirname(fileURLToPath(import.meta.url)),source='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V17-T09-罗马浴场',target=R+'/实例/saves/MB-V18-T10-罗马浴场精修';
const baseline=JSON.parse(fs.readFileSync(R+'/证据/来源文件基准.json'));const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
for(const [p,h] of Object.entries(baseline)){if(sha(source+'/'+p)!==h)throw Error('SOURCE_CHANGED');if(!['session.lock','level.dat'].includes(p)&&sha(target+'/'+p)!==h)throw Error('COPY_CHANGED '+p);}
const a=readNBT(fs.readFileSync(source+'/level.dat')),b=readNBT(fs.readFileSync(target+'/level.dat'));if(b.Data.LevelName!=='MB-V18-T10-罗马浴场精修')throw Error('NAME');b.Data.LevelName=a.Data.LevelName;const json=o=>JSON.stringify(o,(_,v)=>typeof v==='bigint'?String(v):v);if(json(a)!==json(b))throw Error('METADATA_DIFF');
const write=(n,v)=>fs.writeFileSync(R+'/证据/'+n,json(v));write('复制与身份.json',{source,target,source_files_unchanged:true,copy_exact_except_LevelName_and_lock:true,runtime_profile_source:path.dirname(path.dirname(source))});
console.log('Clone content and metadata verified');const q=await qualifyExistingWorld(target,R+'/实例',R+'/资格验证客户端');write('运行配置资格.json',q);console.log('Qualified');
