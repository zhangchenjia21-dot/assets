import test from 'node:test';import assert from 'node:assert/strict';
import {validateNonBuilding} from '../L1_器件层/非房屋资产校验器.mjs';
const tree=()=>({dimensions:{x:3,y:4,z:3},palette:['minecraft:jungle_log[axis=y]','minecraft:jungle_leaves[persistent=true]'],blocks:[[1,0,1,0],[1,1,1,0],[1,2,1,0],[1,3,1,1]],metadata:{asset_contract:{kind:'TREE',anchor:[1,0,1],front:'SOUTH'}}});
test('树根及冠层必须接地且锚点有效',()=>{assert.equal(validateNonBuilding(tree()).rooted_blocks,4);let b=tree();b.blocks.splice(1,1);assert.throws(()=>validateNonBuilding(b),/UNROOTED/);b=tree();b.metadata.asset_contract.anchor=[0,0,0];assert.throws(()=>validateNonBuilding(b),/ANCHOR/);});
test('不明类型不能跳过建筑校验',()=>{const b=tree();b.metadata.asset_contract.kind='BUILDING';assert.throws(()=>validateNonBuilding(b),/CONTRACT/);});
test('敞棚必须有通道和连续支柱',()=>{const b=tree();b.metadata.asset_contract.kind='OPEN_SHELTER';assert.throws(()=>validateNonBuilding(b),/ROUTE/);b.metadata.asset_contract.route=[[1,0,1],[1,0,2],[2,0,2]];assert.throws(()=>validateNonBuilding(b),/BLOCKED/);});
