/** 仅绑定 T04 新测试世界；每次操作核对身份，所有写入走既有正式离线接口。 */
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {gunzipSync} from 'node:zlib';import crypto from 'node:crypto';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
const R=path.dirname(fileURLToPath(import.meta.url)),E=path.join(R,'证据'),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V13-T04-山脊城堡';fs.mkdirSync(E,{recursive:true});
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),write=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2));
const [cmd,n='01']=process.argv.slice(2),scene=read(path.join(R,'场景.json'));
function identity(){const d=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data,g=readNBT(fs.readFileSync(path.join(world,'data/minecraft/world_gen_settings.dat'))).data;if(d.LevelName!==scene.world||g.generate_structures!==0||g.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('WORLD_IDENTITY_BLOCKER');write(path.join(E,'世界身份.json'),{world,name:d.LevelName,game_type:d.GameType,generation:g});}
if(cmd==='run'||cmd==='check'){
 const job=read(path.join(R,'作业',n+'.json'));if(job.world_path!==world)throw Error('PATH_BLOCKER');
 if(job.create){if(fs.existsSync(world))throw Error('NEW_WORLD_ALREADY_EXISTS');}else {identity();await worldStatus(world);}
 const native=inspectBlockStates(scene.palette);if(scene.palette.some(p=>!native[p]?.valid))throw Error('INVALID_PALETTE');
 const m=new Map();let tiles=0;
 for(const f of fs.readdirSync(path.join(R,'蓝图',n))){const bp=JSON.parse(gunzipSync(fs.readFileSync(path.join(R,'蓝图',n,f))));checkBlueprint(bp,{previewOnly:true});for(const[x,y,z,p]of bp.blocks)m.set(((x+bp.origin.x)*256+y+bp.origin.y)*256+z+bp.origin.z,bp.palette[p]);tiles++;}
 const count=m.size;job.samples=[];
 for(const phase of job.phases){for(const[x,y,z,X,Y,Z,p]of phase.operations)for(let a=x;a<=X;a++)for(let b=y;b<=Y;b++)for(let c=z;c<=Z;c++){const key=(a*256+b)*256+c;if(m.get(key)!==phase.palette[p])throw Error('CANONICAL_MISMATCH');m.delete(key);}phase.palette=phase.palette.map(p=>native[p].variants['0/none']);if(job.samples.length<30){const a=phase.operations[0];job.samples.push([a[0],a[1],a[2],phase.palette[a[6]]]);}}
 if(m.size)throw Error('CANONICAL_MISSING');write(path.join(E,n+'-预检.json'),{tiles,blocks:count,canonical_equal:true});console.log('CHECK',n,count);
 if(cmd==='run'){const r=await execute(job);identity();write(path.join(E,n+'-执行.json'),r);console.log(JSON.stringify({blocks:r.changed_blocks,saved:r.save_completed,closed:r.shutdown_verified}));}
}else if(cmd==='read'){
 await worldStatus(world);identity();const rr=new RegionReader(world),[w,h,d]=scene.size,buf=Buffer.alloc(w*h*d),pal=[],ids=new Map();
 for(let x=0;x<w;x++)for(let y=0;y<h;y++)for(let z=0;z<d;z++){const s=rr.get(x,y+scene.y0,z);if(s===null)throw Error('MISSING_CHUNK');if(!ids.has(s)){ids.set(s,pal.length);pal.push(s);}if(pal.length>256)throw Error('PALETTE_LIMIT');buf[(x*h+y)*d+z]=ids.get(s);}
 fs.writeFileSync(path.join(E,n+'.bin'),buf);write(path.join(E,n+'.json'),{world,size:scene.size,y0:scene.y0,palette:pal,sha256:crypto.createHash('sha256').update(buf).digest('hex'),source:'saved chunk readback',time:new Date().toISOString()});console.log('READ',buf.length);
}else throw Error('UNKNOWN_COMMAND');
