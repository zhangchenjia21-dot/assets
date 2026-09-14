// 本脚本只生成离线设计文件；没有世界执行器、存档访问或施工入口。
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8').replace(/^\uFEFF/,''));
const write=(n,v)=>fs.writeFileSync(path.join(root,n),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');
const b=read('inputs/BDP-01.json'),s=read('inputs/场地事实切片.json');
const ground=new Map(s.columns.map(c=>[`${c[0]},${c[1]}`,c[3]]));
const vox=new Map();
const colors={stone:'#938a78',wood:'#775039',plaster:'#d4c3a1',roof:'#4f6267',glass:'#8caeb0',metal:'#53514c',bed:'#ac6751',water:'#608896'};
function put(x,y,z,material='stone',role='wall',shape='cube',facing=null){vox.set(`${x},${y},${z}`,{x,y,z,material,role,shape,...(facing?{facing}:{})});}
function clear(x,y,z){vox.delete(`${x},${y},${z}`);}
function fill(x0,x1,y0,y1,z0,z1,material,role){for(let x=x0;x<=x1;x++)for(let y=y0;y<=y1;y++)for(let z=z0;z<=z1;z++)put(x,y,z,material,role);}
function floor(x0,x1,z0,z1,y,material='stone',role='floor'){
 for(let x=x0;x<=x1;x++)for(let z=z0;z<=z1;z++){
  const gy=ground.get(`${x},${z}`);if(gy===undefined)throw Error('outside observed parcel');
  for(let h=gy+1;h<y;h++)put(x,h,z,'stone','shallow_plinth');put(x,y,z,material,role);
 }
}
// 意图已确定：独立家庭走廊连接高两格的住屋，作坊不作为家庭必经空间。
floor(754,759,1626,1631,131);floor(760,767,1624,1629,133);
for(let x=754;x<=759;x++)for(let z=1626;z<=1631;z++)if(x===754||x===759||z===1626||z===1631)fill(x,x,132,135,z,z,'stone','workshop_wall');
for(let x=760;x<=767;x++)for(let z=1624;z<=1629;z++)if(x===760||x===767||z===1624||z===1629){
 fill(x,x,134,137,z,z,'stone','house_wall');fill(x,x,138,140,z,z,'plaster','upper_infill');
}
fill(757,757,132,134,1627,1630,'wood','work_family_partition');
// 两条独立入口，门洞净高三格；门扇待深化，模型保留敞口而不冒称可运行门。
for(const x of [755,758])for(let y=132;y<=134;y++)clear(x,y,1631);
for(const x of [759,760])for(let y=132;y<=137;y++)clear(x,y,1628);
put(759,132,1628,'stone','split_level_stair','stair','east');
put(760,133,1628,'stone','split_level_stair','stair','east');
put(760,132,1628,'stone','stair_support');
// 二层木楼板，四级楼梯的洞口覆盖整段头部轨迹。
fill(761,766,137,137,1625,1628,'wood','upper_floor');
for(let x=762;x<=765;x++)clear(x,137,1625);
for(let x=762;x<=765;x++)put(x,134+x-762,1625,'wood','internal_stair','stair','east');
for(let x=762;x<=765;x++)for(let y=134;y<134+x-762;y++)put(x,y,1625,'wood','stair_stringer');
// 木柱落在石基上；梁对应小跨度与屋顶受力，不为立面贴饰。
for(const x of [760,767])for(const z of [1624,1629])fill(x,x,138,140,z,z,'wood','post');
for(const x of [760,764,767])fill(x,x,140,140,1624,1629,'wood','roof_tie');
// 较高住屋双坡硬屋面；所有檐口均在显式 mask 内。
for(let x=760;x<=767;x++)for(let z=1624;z<=1629;z++){
 const rise=Math.min(z-1624,1629-z), y=141+rise;
 put(x,y,z,'roof','house_roof','stair',z<=1626?'south':'north');
 if(x===760||x===767)for(let h=141;h<y;h++)put(x,h,z,'plaster','gable');
}
// 作坊靠住屋低檐单坡，东端抬高；横梁由石墙承担。
for(let x=754;x<=759;x++)for(let z=1626;z<=1631;z++){
 const y=136+Math.floor((x-754)/2);put(x,y,z,'roof','workshop_roof',(x-754)%2?'cube':'slab');
 if(z===1626||z===1631||x===759)for(let h=136;h<y;h++)put(x,h,z,'stone','workshop_gable');
}
// 院落等面积移位到西侧低肩，连续三格宽；不在院上覆屋面。
floor(751,753,1627,1632,130,'stone','yard_floor');
floor(754,759,1632,1632,131,'stone','private_landing');
put(754,131,1632,'stone','yard_step','stair','east');
// 原有 24 格 apron 保留，不圈入封闭房间；仅局部接地铺装。
for(const [x,z] of b.spatial_envelope.private_frontage_apron.cells){const gy=ground.get(`${x},${z}`);put(x,gy,z,'stone','apron_floor');}
// 低肩 132 接口候选：路线从现状公共面进入，最终公共标高仍 HOLD。
for(const [x,z] of [[755,1633],[756,1633],[757,1633],[757,1632],[758,1632]])floor(x,x,z,z,131,'stone','private_landing');
// 真实活动占位：工作台、批件架、独立走道，家务不靠穿工位完成。
put(755,132,1627,'wood','repair_bench');put(756,132,1627,'metal','small_vise');
put(755,132,1629,'wood','batch_storage');
put(766,134,1625,'wood','clean_water_storage');put(766,134,1626,'stone','cooking_hearth');
put(765,134,1626,'wood','food_preparation');put(766,134,1627,'wood','food_storage');
put(764,134,1627,'wood','dining_table','slab');
// 烟道在住屋西北墙内上升，与木楼板错开；不把家庭炊火扩大为锻炉。
fill(767,767,134,144,1626,1626,'stone','chimney');
// 睡眠与卫生均在二层，两个床位只是尺度假设，不创作户籍。
for(const x of [761,763])for(const z of [1627,1628])put(x,138,z,'bed','sleeping_place','slab');
put(761,138,1625,'wood','linen_storage');
for(const z of [1627,1628])put(764,138,z,'wood','privacy_screen','screen');
put(765,138,1628,'wood','sealed_waste','slab');put(766,138,1628,'stone','wash_basin','slab');
// 窗与室内活动对应；不假设场外取景权。
for(const [x,y,z] of [[754,133,1628],[767,135,1628],[765,135,1629],[762,139,1629],[767,139,1627],[763,139,1624]])put(x,y,z,'glass','window');
// 楼梯边采用细护栏，占位不侵入一格净宽。
for(let x=762;x<=765;x++)put(x,138,1626,'wood','stair_guard','rail');
// 两个干式收集容器只表达雨水预留，没有 water 方块或外排管。
for(const x of [756,757])put(x,132,1625,'water','rain_reservation','vessel');
const routes=[
 {id:'R-FAMILY',role:'public interface → independent family passage → living',surface:[[757,1633,132],[757,1632,132],[758,1632,132],[758,1631,132],[758,1630,132],[758,1629,132],[758,1628,132],[759,1628,132.5],[759.5,1628,133],[760,1628,133.5],[760.5,1628,134],[761,1628,134],[762,1628,134]]},
 {id:'R-WORK',role:'private apron → handover → repair',surface:[[755,1633,132],[755,1632,132],[755,1631,132],[755,1630,132],[756,1630,132],[756,1629,132],[756,1628,132]]},
 {id:'R-YARD',role:'family threshold → private landing → yard; not workshop',surface:[[758,1631,132],[758,1632,132],[757,1632,132],[756,1632,132],[755,1632,132],[754.5,1632,132],[754,1632,131.5],[753,1632,131],[752,1632,131],[752,1631,131],[752,1630,131],[752,1629,131],[752,1628,131]]},
 {id:'R-UP',role:'living → four-rise internal stair → bedroom landing',surface:[[762,1628,134],[762,1627,134],[762,1626,134],[761,1626,134],[761,1625,134],[762,1625,134.5],[762.5,1625,135],[763,1625,135.5],[763.5,1625,136],[764,1625,136.5],[764.5,1625,137],[765,1625,137.5],[765.5,1625,138],[766,1625,138],[766,1626,138]]},
 {id:'R-SLEEP',role:'upper landing → bed side',surface:[[766,1625,138],[766,1626,138],[765,1626,138],[764,1626,138],[763,1626,138],[762,1626,138],[762,1627,138],[762,1628,138]]},
 {id:'R-HYGIENE',role:'upper landing → screened hygiene',surface:[[766,1625,138],[766,1626,138],[766,1627,138],[765,1627,138]]}
];
const spaces=[{id:'AP',name:'门前缓冲',cells:b.spatial_envelope.private_frontage_apron.cells.length,area:24},{id:'W',name:'小修理净室',bounds:[755,756,1627,1630],surface:132,gross_clear_area:8,furniture_cells:3},{id:'C',name:'家庭独立廊',bounds:[758,758,1627,1630],surface:132,gross_clear_area:4},{id:'L',name:'炊食起居与楼梯',bounds:[761,766,1625,1628],surface:134,gross_clear_area:24},{id:'B',name:'睡眠及储物',bounds:[761,763,1627,1628],surface:138},{id:'H',name:'屏隔洗涤卫生',bounds:[765,766,1627,1628],surface:138,gross_clear_area:4},{id:'Y',name:'家庭露天小院',bounds:[751,753,1627,1632],surface:131,gross_clear_area:18}];
const model={format:'MP-I01R review voxel model v1',revision:'r1',authority:'UNFROZEN_ARCHITECTURE_DESIGN',world_writes:0,world_write_authorization:false,coordinate_semantic:'world x,y,z; y is block bottom; all integers index unit columns; shaped voxels carry collision/render boxes',blocks:[...vox.values()],palette:colors,spaces,routes,roof_and_services:{rain:'dry reservation only; gutter/downpipe and finite storage/overflow sizing unresolved before freeze',roof_top_y:144,chimney_top_y:145},status:'CONCEPT_DESIGN_WITH_INTERFACE_HOLD',regression_verdict:'NOT_ASSIGNED'};
write('设计体素.json',model);
console.log(JSON.stringify({blocks:model.blocks.length,spaces:spaces.length,routes:routes.length}));
