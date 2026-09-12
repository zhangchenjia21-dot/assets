import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {importLitematic,exportLitematic,compareLitematic,previewImported} from '../AI-Blueprints/interop-test/L3_外交层/投影互通公开接口.mjs';
import {ProjectStore} from '../AI-Blueprints/interop-test/../../AI-Preview/L3_外交层/预览公开接口.mjs';
import {encodeNBT,decodeNBT,tag,compound,list,plain} from '../AI-Blueprints/interop-test/L1_器件层/NBT编码器.mjs';
import {packStates,unpackStates} from '../AI-Blueprints/interop-test/L1_器件层/投影位流转换器.mjs';
const ev='D:/Games/Minecraft/AI工程/T12正式入库/互通回归证据';
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'v6a-'));
const bp=(dimensions,palette,blocks,metadata={})=>({schema_version:1,origin:{x:0,y:0,z:0},dimensions,rotation:0,mirror:'none',palette,blocks,metadata:{name:'互通状态夹具',...metadata}});
const registry={entries:[{identifier:'minecraft:stone'},{identifier:'minecraft:air'}]};
function cycle(value,name){const a=path.join(temp,name+'.litematic'),b=path.join(temp,name+'-roundtrip.litematic');exportLitematic(value,a,{dataVersion:4903});const imported=importLitematic(a,{registry});exportLitematic(imported,b);assert.equal(compareLitematic(a,b).status,'PASS');return{a,b,imported};}

test('NBT 保留所有数值类型、长整数和 Java modified UTF 中文/代理对',()=>{const t=compound({name:tag(8,'中文\0🏰'),long:tag(4,'-9223372036854775808'),arr:tag(12,['9223372036854775807','-1']),bytes:tag(7,[-128,127]),short:tag(2,-32768),float:tag(5,1.25),double:tag(6,2.125),ints:tag(11,[-2,4]),list:list(10,[{id:tag(8,'test')}])});assert.deepEqual(decodeNBT(encodeNBT(t)).root,t);assert.throws(()=>decodeNBT(Buffer.from([10,0,0,8,0,1,65])),/TRUNCATED/);});
test('连续位流 2..10 bits 跨 long 边界与截断拒绝',()=>{for(const size of [1,3,5,17,42,65,129,326,700]){const input=Uint32Array.from({length:257},(_,i)=>(i*31)%size);assert.deepEqual(unpackStates(packStates(input,size),size,input.length),input);}assert.throws(()=>unpackStates([],3,9),/LENGTH/);});
test('常见完整 building states 不改变 facing / half / shape / axis',()=>{
 const states=[];for(const facing of ['north','east','south','west'])for(const half of ['top','bottom'])for(const shape of ['straight','inner_left','inner_right','outer_left','outer_right'])states.push(`minecraft:oak_stairs[facing=${facing},half=${half},shape=${shape},waterlogged=false]`);
 for(const type of ['top','bottom','double'])states.push(`minecraft:stone_slab[type=${type},waterlogged=false]`);
 for(const facing of ['north','east','south','west'])for(const half of ['upper','lower'])states.push(`minecraft:oak_door[facing=${facing},half=${half},hinge=left,open=false,powered=false]`);
 for(const half of ['top','bottom'])states.push(`minecraft:oak_trapdoor[facing=east,half=${half},open=true,powered=false,waterlogged=false]`);
 for(const axis of ['x','y','z']){states.push(`minecraft:oak_log[axis=${axis}]`);states.push(`minecraft:quartz_pillar[axis=${axis}]`);}
 states.push('minecraft:oak_fence[east=true,north=false,south=true,waterlogged=false,west=false]','minecraft:cobblestone_wall[east=low,north=tall,south=none,up=true,waterlogged=false,west=none]');
 const value=bp({x:states.length,y:1,z:1},states,states.map((_,i)=>[i,0,0,i]),{note:'需保留此中文 metadata 🏰'}),r=cycle(value,'states');assert.deepEqual(r.imported.blocks.map(v=>r.imported.palette[v[3]]),states);assert.equal(r.imported.metadata.note,value.metadata.note);fs.copyFileSync(r.a,ev+'/building-states-fixture.litematic');
});
test('多 Region 负 Size、负 Position 与间隙保持，原点不偏移',()=>{
 const regions=[{name:'负向区',position:{x:-2,y:0,z:4},size:{x:-2,y:2,z:-3},extra_tags:{}},{name:'右区',position:{x:1,y:0,z:2},size:{x:2,y:2,z:3},extra_tags:{}}];
 const blocks=[];for(const x of [0,1,4,5])for(let y=0;y<2;y++)for(let z=0;z<3;z++)blocks.push([x,y,z,(x+y+z)%2]);
 const value=bp({x:6,y:2,z:3},['minecraft:stone','minecraft:oak_log[axis=x]'],blocks,{litematica:{regions,minecraft_data_version:4903}});value.origin={x:-3,y:0,z:2};
 const r=cycle(value,'multi');assert.deepEqual(r.imported.origin,value.origin);assert.equal(r.imported.blocks.length,24);assert.deepEqual(r.imported.metadata.litematica.regions.map(r=>r.position),regions.map(r=>r.position));fs.copyFileSync(r.a,ev+'/multi-region-fixture.litematic');
});
test('重叠 Region 相同内容可合并，不同内容明确拒绝',()=>{
 const value=bp({x:1,y:1,z:1},['minecraft:stone'],[[0,0,0,0]],{litematica:{minecraft_data_version:4903,regions:[{name:'a',position:{x:0,y:0,z:0},size:{x:1,y:1,z:1},extra_tags:{}},{name:'b',position:{x:0,y:0,z:0},size:{x:1,y:1,z:1},extra_tags:{}}]}}),r=cycle(value,'overlap');assert.equal(r.imported.blocks.length,1);
 const doc=decodeNBT(fs.readFileSync(r.a));doc.root.value.Regions.value.b.value.BlockStatePalette.value.value[1].Name=tag(8,'minecraft:dirt');const file=temp+'/conflict.litematic';fs.writeFileSync(file,encodeNBT(doc.root));assert.throws(()=>importLitematic(file),/OVERLAPPING_REGION_CONFLICT/);
});
test('实体与方块实体保留带类型 NBT，未知 Mod 不崩溃且明确标记',()=>{
 const extras={TileEntities:list(10,[{id:tag(8,'minecraft:chest'),x:tag(3,0),y:tag(3,0),z:tag(3,0),Items:list(10,[])}]),Entities:list(10,[{id:tag(8,'minecraft:armor_stand'),Pos:list(6,[0,0,0])}])};
 const value=bp({x:1,y:1,z:1},['absentmod:stone[facing=north]'],[[0,0,0,0]],{litematica:{minecraft_data_version:4903,regions:[{name:'a',position:{x:0,y:0,z:0},size:{x:1,y:1,z:1},extra_tags:extras}]}}),r=cycle(value,'entities');
 for(const code of ['BLOCK_ENTITY_UNSUPPORTED','ENTITY_UNSUPPORTED','UNRESOLVED_BLOCK'])assert.ok(r.imported.metadata.litematica.warnings.some(v=>v.code===code));assert.deepEqual(r.imported.metadata.litematica.regions[0].extra_tags.TileEntities,extras.TileEntities);assert.deepEqual(r.imported.metadata.litematica.regions[0].extra_tags.Entities,extras.Entities);
});
test('V5 稀疏坐标、显式空气、origin 和 metadata 往返；禁止覆盖文件和未烘焙旋转',()=>{
 const value=bp({x:3,y:3,z:3},['minecraft:stone','minecraft:air'],[[1,1,1,0],[2,2,2,1]],{component_map:{'1,1,1':'walls','2,2,2':'roof'}});value.origin={x:1080,y:64,z:-1258};const r=cycle(value,'sparse');assert.deepEqual(r.imported.origin,value.origin);assert.deepEqual(r.imported.blocks.map(v=>v.slice(0,3)),value.blocks.map(v=>v.slice(0,3)));assert.deepEqual(r.imported.metadata.component_map,value.metadata.component_map);assert.throws(()=>exportLitematic(value,r.a,{dataVersion:4903}),/EEXIST/);assert.throws(()=>exportLitematic({...value,rotation:90},temp+'/rotated',{dataVersion:4903}),/旋转/);
});
test('导入预览使用 V5 原存储，缺少实装验证始终禁用批准',()=>{
 const r=cycle(bp({x:1,y:1,z:1},['minecraft:stone'],[[0,0,0,0]]),'preview');const store=new ProjectStore(temp+'/projects');const m=previewImported(r.imported,'import-test',{store});assert.equal(m.status,'VALIDATION_FAILED');assert.equal(m.approval,null);assert.deepEqual(store.blueprint('import-test'),r.imported);
});
test('语义比较能识别状态变化而非仅计数',()=>{const v=bp({x:1,y:1,z:1},['minecraft:oak_log[axis=x]'],[[0,0,0,0]]),a=cycle(v,'diffa').a;v.palette=['minecraft:oak_log[axis=y]'];const b=cycle(v,'diffb').a;const d=compareLitematic(a,b);assert.equal(d.status,'FAIL');assert.equal(d.unintended_differences,1);assert.equal(d.original.total_blocks,d.roundtrip.total_blocks);});
test('10k / 50k 方块真实导入导出耗时记录',()=>{const results=[];for(const [x,y,z] of [[25,16,25],[50,20,50]]){const blocks=Array.from({length:x*y*z},(_,i)=>[i%x,Math.floor(i/(x*z)),Math.floor(i/x)%z,i%2]);const value=bp({x,y,z},['minecraft:stone','minecraft:oak_log[axis=z]'],blocks);const file=temp+'/'+blocks.length+'.litematic';let t=performance.now();exportLitematic(value,file,{dataVersion:4903});const export_ms=performance.now()-t;t=performance.now();const imported=importLitematic(file);const import_ms=performance.now()-t;assert.equal(imported.blocks.length,blocks.length);results.push({blocks:blocks.length,export_ms,import_ms,compressed_bytes:fs.statSync(file).size});}fs.writeFileSync(ev+'/performance-fixtures.json',JSON.stringify(results,null,2));});
