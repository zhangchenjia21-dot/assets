import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {RegionReader,readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {exportLitematic,importLitematic,inspectLitematic,compareLitematic} from '../AI-Blueprints/interop-test/L3_外交层/投影互通公开接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
const root='D:/Games/Minecraft/AI工程',out=root+'/T12正式入库',world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V110-T12-京町家修复';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');const save=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,(_,v)=>typeof v==='bigint'?String(v):v,2));
// 最终游戏副本是唯一提取源；冻结所有文件哈希，前后必须相等，禁止启动世界。
function hashes(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?hashes(path.join(dir,e.name)):[{path:path.relative(world,path.join(dir,e.name)).replaceAll('\\','/'),sha256:sha(fs.readFileSync(path.join(dir,e.name)))}]);}
const before=hashes(world),level=readNBT(fs.readFileSync(world+'/level.dat'));assert.equal(level.Data.LevelName,'MB-V110-T12-京町家修复');assert.equal(level.Data.DataVersion,4903);
const rr=new RegionReader(world),min={x:11,y:15,z:16},dimensions={x:29,y:20,z:74},palette=[],blocks=[],pmap=new Map();
// 低两层只保留地界内的直接 ground interface；上部包络容纳完整出檐，不携带北街延伸。
for(let y=15;y<=34;y++)for(let z=16;z<=89;z++)for(let x=11;x<=39;x++){
 if(y<=16&&(x<12||z<17||z>88))continue;
 const s=rr.get(x,y,z);assert.notEqual(s,null);if(!pmap.has(s)){pmap.set(s,palette.length);palette.push(s);}blocks.push([x-11,y-15,z-16,pmap.get(s)]);
}
const entities=[];for(const chunk of rr.chunks.values())for(const e of chunk.nbt.block_entities||[])if(e.x>=12&&e.x<=39&&e.y>=15&&e.y<=34&&e.z>=17&&e.z<=88)entities.push(e);
const nonempty=entities.filter(e=>(e.Items?.length||e.items?.length||0)>0);assert.equal(nonempty.length,0,'NONEMPTY_CONTAINER_REQUIRES_TYPED_PRESERVATION');
const regions=[{name:'GroundInterface',position:{x:1,y:0,z:1},size:{x:28,y:2,z:72},extra_tags:{}},{name:'MachiyaCompound',position:{x:0,y:2,z:0},size:{x:29,y:18,z:74},extra_tags:{}}];
const bp={schema_version:1,metadata:{name:'江户后期京都呉服商町家院落',description:'Owner approved T12 final repaired compound; reference only, no Canon placement authorization.',source_kind:'AI_ORIGINAL',source_world:world,source_bounds:{min,max:{x:39,y:34,z:89}},content_omissions:[{kind:'block_entity_nbt',count:entities.length,reason:'原生默认容器方块状态保留；空容器方块实体 NBT 不由当前世界提取管线导出；没有库存物品。'}],litematica:{format_version:7,sub_version:1,minecraft_data_version:4903,regions,warnings:[]}},origin:{x:0,y:0,z:0},dimensions,rotation:0,mirror:'none',palette,blocks};
checkBlueprint(bp,{previewOnly:true});save(out+'/blueprint.json',bp);
const lite=out+'/京町家修复.litematic',round=out+'/roundtrip.litematic';exportLitematic(bp,lite,{dataVersion:4903});const reread=importLitematic(lite);exportLitematic(reread,round);const comp=compareLitematic(lite,round);assert.equal(comp.unintended_differences,0);
const a=new Map(bp.blocks.map(([x,y,z,p])=>[[x,y,z].join(','),bp.palette[p]])),b=new Map(reread.blocks.map(([x,y,z,p])=>[[x,y,z].join(','),reread.palette[p]]));assert.deepEqual(a,b);assert.deepEqual(reread.origin,bp.origin);assert.deepEqual(reread.dimensions,bp.dimensions);
assert.deepEqual(hashes(world),before);save(out+'/来源文件哈希-本地限定.json',before);
save(out+'/提取验证.json',{world,name:level.Data.LevelName,data_version:4903,source_files:before.length,source_files_unchanged:true,source_manifest_sha256:sha(Buffer.from(JSON.stringify(before))),bounds:{min,max:{x:39,y:34,z:89}},dimensions,ground_interface:'X12..39 Y15..16 Z17..88',explicit_blocks:blocks.length,occupied_blocks:blocks.filter(r=>palette[r[3]]!=='minecraft:air').length,region_count:2,blueprint_sha256:sha(fs.readFileSync(out+'/blueprint.json')),litematic_sha256:sha(fs.readFileSync(lite)),block_entity_count:entities.length,block_entity_types:entities.map(e=>({id:e.id,x:e.x,y:e.y,z:e.z,keys:Object.keys(e),inventory_items:(e.Items||e.items||[]).length})),block_entity_nbt_exported:false,roundtrip:comp,canonical_explicit_cell_differences:0,world_writes:0,inspection:inspectLitematic(lite)});
console.log(JSON.stringify({dimensions,explicit:blocks.length,occupied:blocks.filter(r=>palette[r[3]]!=='minecraft:air').length,block_entities:entities.length,entity_keys:entities.map(e=>Object.keys(e)),roundtrip:comp.status}));
