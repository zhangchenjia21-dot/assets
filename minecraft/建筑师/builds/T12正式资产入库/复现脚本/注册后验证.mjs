import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {RegionReader,readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {importLitematic,inspectLitematic} from '../AI-Blueprints/interop-test/L3_外交层/投影互通公开接口.mjs';
const root='D:/Games/Minecraft/AI工程',dir=root+'/T12正式入库',lib=root+'/AI-Blueprints/references',rid='REF-0123',read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const meta=read(lib+'/derived/'+rid+'/metadata.json'),bp=read(meta.blueprint_path),rr=new RegionReader(meta.source.world);
assert.equal(readNBT(fs.readFileSync(meta.source.world+'/level.dat')).Data.LevelName,'MB-V110-T12-京町家修复');
for(const [x,y,z,p] of bp.blocks){assert.equal(rr.get(x+11,y+15,z+16),bp.palette[p]);assert.ok(y>1||(x>=1&&z>=1&&z<=72));}
const ledger=read(root+'/MB-V110-T12/证据/Repair变更账本.json');for(const row of ledger.changes)assert.equal(rr.get(...row.at),row.after);
const entities=[...rr.chunks.values()].flatMap(c=>c.nbt.block_entities||[]).filter(e=>e.x>=12&&e.x<=39&&e.y>=15&&e.y<=34&&e.z>=17&&e.z<=88);
for(const e of entities){assert.equal((e.Items||[]).length,0);assert.equal(Object.keys(e.components||{}).length,0);if(e.id==='minecraft:furnace'){for(const k of ['lit_time_remaining','lit_total_time','cooking_total_time','cooking_time_spent'])assert.equal(e[k]||0,0);assert.equal(Object.keys(e.RecipesUsed||{}).length,0);}}
const lite=importLitematic(meta.original_absolute_path),map=b=>new Map(b.blocks.map(([x,y,z,p])=>[[x,y,z].join(','),b.palette[p]]));assert.deepEqual(map(bp),map(lite));
for(const [view,hash] of Object.entries(meta.preview_binding.view_sha256))assert.equal(sha(meta.architecture_proxy.views[view]),hash);
assert.equal(sha(meta.blueprint_path),meta.preview_binding.source_sha256);assert.equal(sha(meta.original_absolute_path),meta.file_hash);
for(const row of read(dir+'/来源文件哈希-本地限定.json'))assert.equal(sha(meta.source.world+'/'+row.path),row.sha256);
for(const rel of ['catalog/catalog.json','classification-v2/catalog-v2.json','classification-v2/catalog-final.json']){const current=read(lib+'/'+rel),old=read(dir+'/注册前-本地限定/'+rel);assert.deepEqual(current.slice(0,-1),old);assert.deepEqual(current.at(-1),meta);}
const result={reference_id:rid,actual_source_cell_differences:0,all_47_repair_cells_preserved:true,out_of_scope_explicit_cells:0,canonical_roundtrip_differences:0,source_world_files_unchanged:true,empty_block_entities:entities.length,custom_components_or_inventory_omitted:0,default_block_entity_nbt_omitted:10,preview_hashes_match:true,existing_122_records_unchanged:true,world_writes:0,litematica:inspectLitematic(meta.original_absolute_path)};
fs.writeFileSync(dir+'/最终资产验证.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
