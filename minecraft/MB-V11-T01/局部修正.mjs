import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const palette=['minecraft:air','minecraft:dark_oak_log[axis=y]','minecraft:stone_bricks'],operations=[];
// 东岸复廊的外柱移至屋檐下，保留中间三格连续通行带；基座同步落地。
for(const z of[63,70,77])for(const[x,nx]of[[155,154],[159,160]]){for(let y=65;y<=68;y++){operations.push([x,y,z,0]);operations.push([nx,y,z,1]);}operations.push([nx,64,z,2]);}
// 实建透视显示东南峰仍遮蔽山亭回望；仅削低这个明确包络内的石峰，保留岸脚和左侧框景峰。
const world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V11-T01-苏州园林',reader=new RegionReader(world);
for(let z=60;z<=80;z++)for(let x=65;x<=82;x++)if(((x-73)/9)**2+((z-70)/11)**2<1)for(let y=73;y<=87;y++){const s=reader.get(x,y,z);if(s==='minecraft:stone'||s==='minecraft:andesite')operations.push([x,y,z,0]);}
fs.writeFileSync(path.join(root,'修正批次.json'),JSON.stringify([{palette,operations}],null,2));console.log({operations:operations.length});
