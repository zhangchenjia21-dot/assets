// 检查的是可审查设计几何，不裁定集成回归，不模拟 Minecraft 运行时。
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8').replace(/^\uFEFF/,''));
const write=(n,v)=>fs.writeFileSync(path.join(root,n),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');
const m=read('设计体素.json'),b=read('inputs/BDP-01.json'),s=read('inputs/场地事实切片.json');
function boxes(v){
 const {x,y,z}=v,B=(a,c,d,e,f,g)=>({min:[x+a,y+c,z+d],max:[x+e,y+f,z+g],material:v.material,role:v.role});
 if(v.shape==='slab')return [B(0,0,0,1,.5,1)];
 if(v.shape==='screen')return [B(.4,0,0,.6,2,1)];
 if(v.shape==='rail')return [B(0,0,0,1,1.5,.12)];
 if(v.shape==='vessel')return [B(.1,0,.1,.9,.9,.9)];
 if(v.shape==='stair')return [B(0,0,0,1,.5,1),v.facing==='east'?B(.5,.5,0,1,1,1):v.facing==='south'?B(0,.5,.5,1,1,1):B(0,.5,0,1,1,.5)];
 return [B(0,0,0,1,1,1)];
}
const bs=m.blocks.flatMap(boxes);write('设计几何.json',{units:'Minecraft blocks',authority:'design model only; custom screens/rails require native block-state translation',boxes:bs});
const mask=new Set(b.spatial_envelope.cells.map(c=>c.join(',')));
const protectedCells=new Set(b.interface_baselines.filter(i=>i.interface_id!=='R2-IF-THRESHOLD-1').flatMap(i=>i.local_geometry.cells??[]).map(c=>c.join(',')));
const outside=m.blocks.filter(v=>!mask.has(`${v.x},${v.z}`));
const intrusions=m.blocks.filter(v=>protectedCells.has(`${v.x},${v.z}`));
const yard=m.blocks.filter(v=>v.role==='yard_floor');
const yardCovered=yard.filter(v=>m.blocks.some(w=>w.x===v.x&&w.z===v.z&&w.y>131));
const terrain=new Map(s.columns.map(c=>[`${c[0]},${c[1]}`,c[3]]));
const deepEdits=m.blocks.filter(v=>v.y<terrain.get(`${v.x},${v.z}`));
const issues=[];let poseCount=0;
for(const r of m.routes){
 let hits=[];
 for(let i=0;i<r.surface.length-1;i++){
  const a=r.surface[i],z=r.surface[i+1],count=Math.ceil(Math.hypot(z[0]-a[0],z[1]-a[1])*10)||1;
  for(let q=0;q<=count;q++){
   const t=q/count,x=a[0]+(z[0]-a[0])*t+.5,zz=a[1]+(z[1]-a[1])*t+.5;
   let fy=a[2]+(z[2]-a[2])*t;
   // 踏步横断面用身体投影下最高已设计踏面包络抬高头部检查。
   // 一格搜索只适用于阶梯/楼板，不允许把家具或墙体当可跨越支承；不是自动跨阶模拟。
   const supports=bs.filter(v=>/stair|step|floor|landing/.test(v.role)&&v.min[0]<x+.3-1e-6&&v.max[0]>x-.3+1e-6&&v.min[2]<zz+.3-1e-6&&v.max[2]>zz-.3+1e-6&&v.max[1]<=fy+1.00001&&v.max[1]>=fy-.5);
   fy=Math.max(fy,...supports.map(v=>v.max[1]));
   const bad=bs.filter(v=>v.min[0]<x+.3-1e-6&&v.max[0]>x-.3+1e-6&&v.min[2]<zz+.3-1e-6&&v.max[2]>zz-.3+1e-6&&v.min[1]<fy+1.8-1e-6&&v.max[1]>fy+1e-6);
   if(bad.length)hits.push({at:[+x.toFixed(2),+fy.toFixed(2),+zz.toFixed(2)],roles:[...new Set(bad.map(v=>v.role))]});poseCount++;
  }
 }
 issues.push({route:r.id,sampled_obstructions:hits.length,examples:hits.slice(0,5)});
}
const check={test:'MP-I01R',regression_verdict:'NOT_ASSIGNED — GPT + Owner only',design_state:m.status,world_writes:0,checks:{voxel_count:m.blocks.length,parcel_columns:mask.size,outside_mask:outside.length,protected_mask_intrusions:intrusions.length,private_yard_area:yard.length,yard_roof_intrusions:yardCovered.length,proposed_below_observed_ground:deepEdits.length,route_sample_count:poseCount,route_results:issues},limitations:['No Minecraft client/server/save was opened.','Public 2-wide swept movement and final threshold elevation require PUBLIC-COORDINATOR closure; mask non-overlap alone does not certify them.','Custom screen/rail collision boxes are design requirements, not certified vanilla block-state collision.','Route scan raises the 0.6 x 1.8 body above the highest designed stair/floor intersecting its projection (within one block of nominal route height); this is a head-envelope test, not a step-height or physics test.','Foundation scan covers this proposal footprint, not deep historical clearance.'],freeze_holds:['U-PUBLIC / rainwater outfall and final contact surface','U-GROUND / foundation influence volume and structural assessment','door-state and custom-detail collision translation; handrail/light/ventilation detailing'],integration_review:'AWAITING_GPT_AND_OWNER'};
write('设计核验.json',check);
const esc=t=>String(t).replaceAll('&','&amp;').replaceAll('<','&lt;');
const header=(w,h,title)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="100%" height="100%" fill="#f5f0e7"/><style>text{font-family:'Microsoft YaHei',sans-serif;fill:#243b3c} .small{font-size:13px} .title{font-size:25px;font-weight:bold}</style><text x="28" y="36" class="title">${title}</text>`;
function plan(y,title){
 const k=37,ox=65,oz=92;let out=header(850,700,title);
 const X=x=>ox+(x-750)*k,Z=z=>oz+(z-1623)*k;
 for(const [x,z] of b.spatial_envelope.cells)out+=`<rect x="${X(x)}" y="${Z(z)}" width="${k}" height="${k}" fill="#e4dfd2" stroke="#cbc5b5"/>`;
 for(const [x,z] of b.spatial_envelope.private_frontage_apron.cells)out+=`<rect x="${X(x)}" y="${Z(z)}" width="${k}" height="${k}" fill="#d5ac70" opacity=".5"/>`;
 for(const v of yard)out+=`<rect x="${X(v.x)}" y="${Z(v.z)}" width="${k}" height="${k}" fill="#a5b8a0"/>`;
 for(const v of bs.filter(v=>v.min[1]<=y&&v.max[1]>y))out+=`<rect x="${X(v.min[0])}" y="${Z(v.min[2])}" width="${(v.max[0]-v.min[0])*k}" height="${(v.max[2]-v.min[2])*k}" fill="${m.palette[v.material]}" stroke="#433e35" stroke-width=".5"/>`;
 for(const r of m.routes.filter(r=>r.surface.some(p=>Math.abs(p[2]-y)<2))){const pts=r.surface.filter(p=>Math.abs(p[2]-y)<2).map(p=>`${X(p[0]+.5)},${Z(p[1]+.5)}`).join(' ');out+=`<polyline points="${pts}" fill="none" stroke="${r.id==='R-WORK'?'#c35038':'#225e79'}" stroke-width="3"/>`;}
 const labels=y<133?[['W',755.5,1628.5],['C',758,1629],['Y',751.8,1629]]:y<137?[['L',763,1628],['UP',763,1625],['Y',751.8,1629]]:[['B',761,1627],['H',765,1627],['UP',764,1625]];
 for(const [name,x,z] of labels)out+=`<text x="${X(x+.5)}" y="${Z(z+.5)}" font-size="16" font-weight="bold" paint-order="stroke" stroke="#f5f0e7" stroke-width="3">${name}</text>`;
 for(let x=750;x<=768;x+=2)out+=`<text x="${X(x)}" y="78" class="small">${x}</text>`;
 for(let z=1623;z<=1637;z+=2)out+=`<text x="12" y="${Z(z)+20}" class="small">${z}</text>`;
 out+=`<text x="65" y="650" class="small">北 ↑　橙：保留 apron 24格　绿：移位露天小院 18格　蓝：家庭　红：工作</text><text x="65" y="676" class="small">切片 Y=${y}；格网=1 block。主屋134/138，作坊132，小院131；公共接触标高 HOLD。</text></svg>`;return out;
}
write('平面-下层.svg',plan(134.25,'MP-I01R · 住屋首层 / 作坊路线（双标高见专页）'));
write('平面-作坊.svg',plan(132.25,'MP-I01R · 低肩作坊 / 独立家庭廊'));
write('平面-上层.svg',plan(138.25,'MP-I01R · 上层睡眠 / 卫生 / 楼梯洞口'));
function section(z,title){let out=header(1020,600,title);const X=x=>55+(x-750)*47,Y=y=>525-(y-128)*27;
 for(const [key,gy] of terrain){const [x,zz]=key.split(',').map(Number);if(zz===Math.floor(z))out+=`<rect x="${X(x)}" y="${Y(gy+1)}" width="47" height="${525-Y(gy+1)}" fill="#c7c0af"/>`;}
 for(const v of bs.filter(v=>v.min[2]<=z&&v.max[2]>z))out+=`<rect x="${X(v.min[0])}" y="${Y(v.max[1])}" width="${(v.max[0]-v.min[0])*47}" height="${(v.max[1]-v.min[1])*27}" fill="${m.palette[v.material]}" stroke="#4b463f" stroke-width=".5"/>`;
 for(const y of [131,132,134,138,141,144])out+=`<line x1="45" y1="${Y(y)}" x2="970" y2="${Y(y)}" stroke="#314947" opacity=".25"/><text x="5" y="${Y(y)-3}" class="small">${y}</text>`;
 out+=`<text x="55" y="566" class="small">Z=${z} · 地表事实灰底；设计不向观测地面以下开挖。屋面/家具均为设计几何，不是游戏截图。</text></svg>`;return out;}
write('剖面-家庭横向.svg',section(1628.5,'A–A · 小院 → 作坊/家庭廊 → 双步级 → 起居 → 住屋'));
write('剖面-楼梯.svg',section(1625.5,'B–B · 四级木梯与二层洞口 / 高肩石基'));
// 等轴图来自同一碰撞几何。按面深度排序；不使用生成图片冒充设计证据。
function iso(cut){const polys=[];const project=([x,y,z])=>[510+(x-759)*24-(z-1630)*20,470+(x-759)*9+(z-1630)*11-(y-130)*24];
 for(const v of bs.filter(v=>!cut||v.max[1]<=138)){
  const [x,y,z]=v.min,[a,c,d]=v.max;
  for(const [points,light] of [[[[x,c,z],[a,c,z],[a,c,d],[x,c,d]],1],[[[x,y,d],[a,y,d],[a,c,d],[x,c,d]],.85],[[[a,y,z],[a,y,d],[a,c,d],[a,c,z]],.68]]){
   polys.push({points,light,depth:points.reduce((n,p)=>n+p[0]+p[2]+p[1]*.05,0)/4,color:m.palette[v.material]});
  }
 }
 let out=header(1080,740,cut?'MP-I01R · 屋面/上墙移除的剖切轴测':'MP-I01R · 石基双高程 / 单坡作坊与双坡住屋');
 for(const p of polys.sort((a,b)=>a.depth-b.depth))out+=`<polygon points="${p.points.map(v=>project(v).join(',')).join(' ')}" fill="${p.color}" stroke="#363d39" stroke-width=".35"/><polygon points="${p.points.map(v=>project(v).join(',')).join(' ')}" fill="black" opacity="${1-p.light}"/>`;
 return out+'<text x="28" y="712" class="small">概念设计 · 未冻结 · world writes = 0 · 公共路面、雨水受纳、施工与真实碰撞均未获闭合。</text></svg>';
}
write('体量轴测.svg',iso(false));write('剖切轴测.svg',iso(true));
const svgNames=['体量轴测.svg','平面-作坊.svg','平面-下层.svg','平面-上层.svg','剖面-家庭横向.svg','剖面-楼梯.svg','剖切轴测.svg'];
write('设计预览.html',`<!doctype html><html lang="zh"><meta charset="utf-8"><title>MP-I01R BDP-01 Architecture Design</title><style>body{margin:0;background:#203636;color:#efe9dc;font:16px 'Microsoft YaHei',sans-serif}header{padding:24px 5vw}h1{font-size:30px;margin:0}p{line-height:1.7}nav{display:flex;flex-wrap:wrap;gap:8px;padding:0 5vw 20px}button{padding:10px 16px;background:#ddbc86;border:0;cursor:pointer;border-radius:3px}main{background:#f5f0e7;text-align:center}img{max-width:100%;max-height:78vh}a{color:#efc88a}</style><header><h1>低肩修理户 · BDP-01</h1><p>MP-I01R / Builder v1.11 / Concept design with interface HOLD<br>双标高住屋与作坊；独立家庭廊；18格露天小院。world writes = 0。等轴与剖面均来自同一设计模型。</p></header><nav>${svgNames.map((n,i)=>`<button onclick="document.querySelector('img').src='${n}'">${i+1} ${n.replace('.svg','')}</button>`).join('')}</nav><main><img src="体量轴测.svg" alt="设计图纸"></main><header><a href="建筑设计.md">建筑设计</a> · <a href="设计核验.json">几何核验与限制</a> · <a href="handoff-consumption-record.md">Handoff record</a><p>审核对象为未冻结建筑设计；不宣称建成、可施工或集成回归 PASS / FAIL。</p></header></html>`);
console.log(JSON.stringify(check.checks,null,2));
