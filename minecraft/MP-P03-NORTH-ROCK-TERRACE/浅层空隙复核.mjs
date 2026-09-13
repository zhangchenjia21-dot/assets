/** 对本轮几何范围逐柱只读复核，不填洞、不创建区块，不解释空隙的人工/自然来源。 */
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {RegionReader} from '../../../../AI-Offline/L3_外交层/存档读取接口.mjs';
const R=path.dirname(fileURLToPath(import.meta.url)),C=path.resolve(R,'../../../..','MP-P03-cache');
const raw=JSON.parse(fs.readFileSync(path.join(C,'surface.json'),'utf8'));const reader=new RegionReader(path.join(C,'readonly-snapshot'));
const points=[];let total=0;
for(const [x,z,,y] of raw.columns){if(x<744||x>884||z<1576||z>1672)continue;total++;const gaps=[];for(let dy=1;dy<=16;dy++){const s=reader.get(x,y-dy,z);if(s==='minecraft:air'||s==='minecraft:cave_air'||s==='minecraft:void_air')gaps.push(y-dy);}if(gaps.length)points.push({x,z,surface_y:y,void_y:gaps,minimum_cover_blocks:y-Math.max(...gaps)});}
fs.writeFileSync(path.join(R,'evidence/shallow-void-columns.json'),JSON.stringify({bounds:[744,1576,884,1672],depth:16,columns_checked:total,void_columns:points,authority:'OBSERVED_BLOCK_STATE',origin:'UNRESOLVED_NATURAL_OR_ARTIFICIAL',limitations:['只查地面下16格；深层、区外和结构稳定性未证','空气状态不等于应填补缺陷；本轮只规划避让']},null,2)+'\n');
console.log(JSON.stringify({total,void_columns:points.length,bounds:points.length?[Math.min(...points.map(p=>p.x)),Math.min(...points.map(p=>p.z)),Math.max(...points.map(p=>p.x)),Math.max(...points.map(p=>p.z))]:null}));
