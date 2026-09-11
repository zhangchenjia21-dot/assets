/** T06 唯一写入入口：先确认精确目标、冻结蓝图与原生状态；不得覆盖同名既有世界。 */
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {gunzipSync} from 'node:zlib';import {fileURLToPath} from 'node:url';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {RegionReader,readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
const R=path.dirname(fileURLToPath(import.meta.url)),E=path.join(R,'证据'),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T06-规则宫苑';fs.mkdirSync(E,{recursive:true});
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),write=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2));const s=read(path.join(R,'场景.json'));const[cmd,n]=process.argv.slice(2);
function identity(){const d=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data,g=readNBT(fs.readFileSync(path.join(world,'data/minecraft/world_gen_settings.dat'))).data;if(d.LevelName!=='MB-V15-T06-规则宫苑'||g.generate_structures!==0||g.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('TARGET_IDENTITY_BLOCKER');write(path.join(E,'世界身份.json'),{world,name:d.LevelName,generation:g});}
if(cmd==='run'||cmd==='check'){
 const job=read(path.join(R,'作业',n+'.json'));if(job.world_path!==world)throw Error('TARGET_PATH_BLOCKER');if(job.create){if(fs.existsSync(world))throw Error('NEW_WORLD_EXISTS');}else{identity();await worldStatus(world);}
 const native=inspectBlockStates(s.palette);if(s.palette.some(p=>!native[p]?.valid))throw Error('INVALID_PALETTE');const map=new Map();let tiles=0;
 for(const f of fs.readdirSync(path.join(R,'蓝图',n))){const bp=JSON.parse(gunzipSync(fs.readFileSync(path.join(R,'蓝图',n,f))));checkBlueprint(bp,{previewOnly:true});for(const[x,y,z,p]of bp.blocks){const key=((x+bp.origin.x)*128+y+bp.origin.y)*320+z+bp.origin.z;if(map.has(key))throw Error('OVERLAPPING_BLUEPRINT');map.set(key,bp.palette[p]);}tiles++;}
 const blocks=map.size;job.samples=[];
 for(const phase of job.phases){for(const[x,y,z,X,Y,Z,p]of phase.operations)for(let a=x;a<=X;a++)for(let b=y;b<=Y;b++)for(let c=z;c<=Z;c++){const k=(a*128+b)*320+c;if(map.get(k)!==phase.palette[p])throw Error('CANONICAL_OPERATION_MISMATCH');map.delete(k);}phase.palette=phase.palette.map(p=>native[p].variants['0/none']);if(job.samples.length<25){const a=phase.operations[0];job.samples.push([a[0],a[1],a[2],phase.palette[a[6]]]);}}
 if(map.size)throw Error('CANONICAL_COVERAGE_MISMATCH');write(path.join(E,n+'-预检.json'),{tiles,blocks,equivalent:true});console.log('CHECK',n,blocks);
 if(cmd==='run'){const result=await execute(job);identity();write(path.join(E,n+'-执行.json'),result);console.log(JSON.stringify({blocks:result.changed_blocks,saved:result.save_completed,closed:result.shutdown_verified}));}
}else if(cmd==='read'){
 await worldStatus(world);identity();const rr=new RegionReader(world),[W,H,D]=s.size,b=Buffer.alloc(W*H*D),P=[],ids=new Map();
 for(let x=0;x<W;x++)for(let y=0;y<H;y++)for(let z=0;z<D;z++){const p=rr.get(x,y+s.y0,z);if(p===null)throw Error('UNGENERATED_CHUNK');if(!ids.has(p)){ids.set(p,P.length);P.push(p);}if(P.length>256)throw Error('PALETTE_OVERFLOW');b[(x*H+y)*D+z]=ids.get(p);}
 fs.writeFileSync(path.join(E,n+'.bin'),b);write(path.join(E,n+'.json'),{world,size:s.size,y0:s.y0,palette:P,source:'saved chunks; read only',time:new Date().toISOString(),sha256:crypto.createHash('sha256').update(b).digest('hex')});console.log('READ',b.length);
}else throw Error('UNKNOWN_COMMAND');
