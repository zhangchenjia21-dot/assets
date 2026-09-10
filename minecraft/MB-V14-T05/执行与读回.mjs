/** T05 唯一世界入口；新建拒绝覆盖，既有目标核验名称、生成方式和结构开关。 */
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {gunzipSync} from 'node:zlib';import crypto from 'node:crypto';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
const R=path.dirname(fileURLToPath(import.meta.url)),E=path.join(R,'证据'),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V14-T05-森林圣所';fs.mkdirSync(E,{recursive:true});const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),write=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2));const [cmd,n='01']=process.argv.slice(2),s=read(path.join(R,'场景.json'));
function identity(){const d=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data,g=readNBT(fs.readFileSync(path.join(world,'data/minecraft/world_gen_settings.dat'))).data;if(d.LevelName!==s.world||g.generate_structures!==0||g.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('TARGET_IDENTITY_BLOCKER');write(path.join(E,'世界身份.json'),{world,name:d.LevelName,game_type:d.GameType,generation:g});}
if(cmd==='run'||cmd==='check'){
 const job=read(path.join(R,'作业',n+'.json'));if(job.world_path!==world)throw Error('PATH_BLOCKER');if(job.create){if(fs.existsSync(world))throw Error('NEW_WORLD_EXISTS');}else{identity();await worldStatus(world);}
 const native=inspectBlockStates(s.palette);if(s.palette.some(p=>!native[p]?.valid))throw Error('PALETTE_BLOCKER');const coords=new Map();let tiles=0;
 for(const file of fs.readdirSync(path.join(R,'蓝图',n))){const bp=JSON.parse(gunzipSync(fs.readFileSync(path.join(R,'蓝图',n,file))));checkBlueprint(bp,{previewOnly:true});for(const[x,y,z,p]of bp.blocks)coords.set(((x+bp.origin.x)*256+y+bp.origin.y)*256+z+bp.origin.z,bp.palette[p]);tiles++;}
 const count=coords.size;job.samples=[];
 for(const ph of job.phases){for(const[x,y,z,X,Y,Z,p]of ph.operations)for(let a=x;a<=X;a++)for(let b=y;b<=Y;b++)for(let c=z;c<=Z;c++){const k=(a*256+b)*256+c;if(coords.get(k)!==ph.palette[p])throw Error('BLUEPRINT_OPERATION_MISMATCH');coords.delete(k);}ph.palette=ph.palette.map(p=>native[p].variants['0/none']);if(job.samples.length<30){const a=ph.operations[0];job.samples.push([a[0],a[1],a[2],ph.palette[a[6]]]);}}
 if(coords.size)throw Error('BLUEPRINT_COVERAGE');write(path.join(E,n+'-预检.json'),{tiles,blocks:count,equivalent:true});console.log('CHECK',n,count);
 if(cmd==='run'){const result=await execute(job);identity();write(path.join(E,n+'-执行.json'),result);console.log(JSON.stringify({blocks:result.changed_blocks,saved:result.save_completed,closed:result.shutdown_verified}));}
}else if(cmd==='read'){
 await worldStatus(world);identity();const rr=new RegionReader(world),[w,h,d]=s.size,b=Buffer.alloc(w*h*d),palette=[],ids=new Map();
 for(let x=0;x<w;x++)for(let y=0;y<h;y++)for(let z=0;z<d;z++){const p=rr.get(x,y+s.y0,z);if(p===null)throw Error('MISSING_CHUNK');if(!ids.has(p)){ids.set(p,palette.length);palette.push(p);}if(palette.length>256)throw Error('PALETTE_OVERFLOW');b[(x*h+y)*d+z]=ids.get(p);}
 fs.writeFileSync(path.join(E,n+'.bin'),b);write(path.join(E,n+'.json'),{world,size:s.size,y0:s.y0,palette,sha256:crypto.createHash('sha256').update(b).digest('hex'),source:'saved chunks / read-only',time:new Date().toISOString()});console.log('READ',b.length);
}else throw Error('UNKNOWN_COMMAND');
