import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
import {readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),name='MB-V11-T01-苏州园林';
const world=path.resolve('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves',name);
const index=Number(process.argv[2]);if(![1,2,3,4].includes(index))throw Error('阶段编号不支持');
// 每次写入只允许本测试路径；已有世界再核验 Minecraft 持久化名称和生成类型。
if(path.basename(world)!==name||world.includes('建筑师'))throw Error('TEST_WORLD_TARGET_MISMATCH');
if(index===1){if(fs.existsSync(world))throw Error('TEST_WORLD_ALREADY_EXISTS');}
else{await worldStatus(world);const level=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data;if(level.LevelName!==name)throw Error('TEST_WORLD_NAME_MISMATCH:'+level.LevelName);}
const manifest=JSON.parse(fs.readFileSync(path.join(root,'阶段清单.json'),'utf8'));
// 本批次无旋转和镜像，Canonical Blueprint 直接展开为公开 run-job 格式；状态由 Minecraft 原生注册表解析。
let phases;if(index<=3)phases=manifest.stages[index-1].files.map(file=>{const b=JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));checkBlueprint(b,{previewOnly:true});return{palette:b.palette,operations:b.blocks.map(([x,y,z,p])=>[x+b.origin.x,y+b.origin.y,z+b.origin.z,p])};});else phases=JSON.parse(fs.readFileSync(path.join(root,'修正批次.json'),'utf8'));
const job={world_path:world,phases,samples:[[38,63,149,'minecraft:smooth_stone']],...(index===1?{create:{type:'superflat',seed:1101,generator_options:{biome:'minecraft:plains',layers:[{block:'minecraft:bedrock',height:1},{block:'minecraft:dirt',height:126},{block:'minecraft:grass_block',height:1}],structure_overrides:[]}},spawn:[38,64,146]}:{})};
if(index===1)job.samples=[[105,64,117,'minecraft:stone_bricks']];
const jobPath=path.join(root,`作业-${index}.json`);fs.writeFileSync(jobPath,JSON.stringify(job));
fs.writeFileSync(path.join(root,`写入目标-${index}.json`),JSON.stringify({name,world_path:world,stage:index,job_sha256:crypto.createHash('sha256').update(fs.readFileSync(jobPath)).digest('hex'),time:new Date().toISOString()},null,2));
const result=await execute(job);fs.writeFileSync(path.join(root,`结果-${index}.json`),JSON.stringify(result,null,2));console.log(JSON.stringify({status:result.status,changed:result.changed_blocks,shutdown:result.shutdown_verified,job:result.job_directory}));
