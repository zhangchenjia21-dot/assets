/** T03 专用编排。只通过正式公开接口写入唯一目标；导出为只读保存区块。 */
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {gunzipSync} from 'node:zlib';import crypto from 'node:crypto';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url)),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落',evidence=path.join(dir,'证据');fs.mkdirSync(evidence,{recursive:true});
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),write=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,(_,a)=>typeof a==='bigint'?String(a):a,2));
const [command,n='1']=process.argv.slice(2),scene=read(path.join(dir,'场景.json'));
function identity(){
 const d=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data,g=readNBT(fs.readFileSync(path.join(world,'data/minecraft/world_gen_settings.dat')));
 if(d.LevelName!==scene.world||g.data.generate_structures!==0||g.data.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('TARGET_IDENTITY_OR_GENERATION_BLOCKER');
 write(path.join(evidence,'世界身份.json'),{world,name:d.LevelName,game_type:d.GameType,generation:g});
}
if(command==='check'||command==='run'){
 const job=read(path.join(dir,'作业',n.padStart(2,'0')+'.json'));if(job.world_path!==world)throw Error('TARGET_PATH_BLOCKER');
 if(job.create){if(fs.existsSync(world))throw Error('NEW_WORLD_ALREADY_EXISTS');}else{identity();await worldStatus(world);}
 const folder=fs.readdirSync(path.join(dir,'蓝图')).find(f=>f.startsWith(n.padStart(2,'0')+'-')),coords=new Map();let tiles=0;
 for(const file of fs.readdirSync(path.join(dir,'蓝图',folder))){const bp=JSON.parse(gunzipSync(fs.readFileSync(path.join(dir,'蓝图',folder,file))));checkBlueprint(bp,{previewOnly:true});for(const[x,y,z,p]of bp.blocks)coords.set((x+bp.origin.x)*65536+(y+bp.origin.y)*256+z+bp.origin.z,bp.palette[p]);tiles++;}
 const count=coords.size,native=inspectBlockStates(scene.palette);const invalid=Object.entries(native).filter(([,v])=>!v.valid);if(invalid.length)throw Error('INVALID_PALETTE '+JSON.stringify(invalid));
 job.samples=[];
 for(const ph of job.phases){for(const[x,y,z,X,Y,Z,p]of ph.operations)for(let a=x;a<=X;a++)for(let b=y;b<=Y;b++)for(let c=z;c<=Z;c++){const k=a*65536+b*256+c;if(coords.get(k)!==ph.palette[p])throw Error('CANONICAL_OPERATION_MISMATCH');coords.delete(k);}ph.palette=ph.palette.map(s=>native[s].variants['0/none']);const a=ph.operations[0];if(job.samples.length<32)job.samples.push([a[0],a[1],a[2],ph.palette[a[6]]]);}
 if(coords.size)throw Error('CANONICAL_COVERAGE_MISSING');write(path.join(evidence,`阶段${n}-蓝图核对.json`),{tiles,blocks:count,canonical_operations_equal:true});console.log('CHECK',tiles,count);
 if(command==='run'){const result=await execute(job);identity();write(path.join(evidence,`阶段${n}-执行.json`),result);console.log(JSON.stringify({world:result.world_path,changed_blocks:result.changed_blocks,save_completed:result.save_completed,shutdown_verified:result.shutdown_verified,job_directory:result.job_directory}));}
}else if(command==='read'){
 await worldStatus(world);identity();const r=new RegionReader(world),[w,h,d]=scene.size,b=Buffer.alloc(w*h*d),palette=[],indices=new Map();
 for(let x=0;x<w;x++)for(let y=0;y<h;y++)for(let z=0;z<d;z++){const s=r.get(x,y+scene.y0,z);if(s===null)throw Error('MISSING_SAVED_CHUNK');if(!indices.has(s)){indices.set(s,palette.length);palette.push(s);if(palette.length>256)throw Error('EXPORT_PALETTE_LIMIT');}b[(x*h+y)*d+z]=indices.get(s);}
 fs.writeFileSync(path.join(evidence,`阶段${n}.bin`),b);write(path.join(evidence,`阶段${n}.json`),{world,size:scene.size,y0:scene.y0,palette,sha256:crypto.createHash('sha256').update(b).digest('hex'),source:'saved chunks / RegionReader',time:new Date().toISOString()});console.log('READ',b.length,palette.length);
}else throw Error('UNKNOWN_OPERATION');
