import fs from 'node:fs';import assert from 'node:assert/strict';
import {importLitematic} from '../AI-Blueprints/interop-test/L3_外交层/投影互通公开接口.mjs';
const dir='D:/Games/Minecraft/AI工程/T12正式入库',rows=JSON.parse(fs.readFileSync(dir+'/native-litematica-load.json')),results=[];
for(const r of rows){const bp=importLitematic(dir+'/'+r.file),min=bp.metadata.litematica.enclosing_min;
 const expected=new Map(bp.blocks.filter(b=>!['minecraft:air','minecraft:cave_air','minecraft:void_air'].includes(bp.palette[b[3]])).map(([x,y,z,p])=>[[x+min.x,y+min.y,z+min.z].join(','),bp.palette[p]]));
 const actual=new Map(r.states.map(b=>[[b.x,b.y,b.z].join(','),b.state]));assert.deepEqual(actual,expected);
 results.push({file:r.file,regions:r.regions,blocks:actual.size,full_state_differences:0,status:'PASS',world_opened:false});}
fs.writeFileSync(dir+'/原生回读验证.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results));
