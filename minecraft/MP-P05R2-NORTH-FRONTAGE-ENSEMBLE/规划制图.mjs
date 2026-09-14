import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const plan=read('planning-data.json'),surface=read('evidence/地表采样.json'),ints=read('interface-baselines.json').interfaces;
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;');
const text=(x,y,s,size=18,fill='#203342',weight=400)=>`<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" font-weight="${weight}">${esc(s)}</text>`;
const head=(w,h,title,sub)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><style>text{font-family:'Microsoft YaHei','Noto Sans CJK SC',sans-serif} .halo{paint-order:stroke;stroke:#fff;stroke-width:5px;stroke-linejoin:round}</style><rect width="100%" height="100%" fill="#f6f4ed"/>${text(50,48,title,29,'#203342',700)}${text(50,81,sub,16)}`;
const write=(f,s)=>{fs.mkdirSync(path.join(dir,'maps'),{recursive:true});fs.writeFileSync(path.join(dir,'maps',f),s+'</svg>');};
const X=x=>70+(x-746)*20,Z=z=>140+(z-1620)*20;
const points=p=>p.map(([x,z])=>`${X(x)},${Z(z)}`).join(' ');
const polygon=(p,fill,stroke,opacity=.35)=>`<polygon points="${points(p)}" fill="${fill}" fill-opacity="${opacity}" stroke="${stroke}" stroke-width="2.5"/>`;
const line=(p,color,width,dash='')=>`<polyline points="${points(p)}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''} stroke-linejoin="round" stroke-linecap="round"/>`;
const cells=(cc,fill,opacity=.8)=>cc.map(([x,z])=>`<rect x="${X(x)}" y="${Z(z)}" width="20" height="20" fill="${fill}" fill-opacity="${opacity}"/>`).join('');
const marker=(x,z,label)=>`<circle cx="${X(x)}" cy="${Z(z)}" r="15" fill="#203342" stroke="white" stroke-width="2"/>${text(X(x)-6,Z(z)+6,label,17,'#fff',700)}`;
function mapBase(title,sub){let s=head(1650,1110,title,sub);for(const c of surface.columns){const gray=Math.max(125,240-(c[3]-127)*11);s+=`<rect x="${X(c[0])}" y="${Z(c[1])}" width="20" height="20" fill="rgb(${gray},${gray+3},${gray})"/>`;}
for(let x=750;x<=795;x+=5)s+=`<path d="M${X(x)},140 V820" stroke="#fff" opacity=".55"/>`+text(X(x)-15,128,x,13);
for(let z=1620;z<=1650;z+=5)s+=`<path d="M70,${Z(z)} H1150" stroke="#fff" opacity=".55"/>`+text(18,Z(z)+5,z,13);
s+=text(70,855,'X → 东；Z ↓ 南。每小格 1 block；标注 Y 为地面方块索引，顶面 = Y+1。',16);
s+=`<path d="M1110,225 V170 l-8,14 m8,-14 l8,14" fill="none" stroke="#203342" stroke-width="3"/>`+text(1099,158,'N',18);
s+=`<path d="M80,888 h100 m-100,-6 v12 m100,-12 v12" stroke="#203342" stroke-width="3"/>`+text(195,894,'5 blocks',16);
return s;}
let s=mapBase('MP-P05R2｜北侧两户混合前沿','URBAN_ENSEMBLE · r1 · 新规划提案叠加真实地表 · world writes = 0 · 等待 GPT + Owner 审核');
const common=ints.find(i=>i.interface_id==='R2-IF-COMMON-EDGE');s+=polygon(common.local_geometry.polygon,'#ffffff','#738996',.22);
for(const i of ints.filter(i=>i.interface_id.includes('LANE')))s+=cells(i.local_geometry.cells,'#70c7db',.5)+line(i.local_geometry.centerline,'#197e9a',2,'6 4');
for(const [idx,p] of plan.parcels.entries()){s+=cells(p.allocation.architectural_search_mask.cells,'#d6a751',.62)+cells(p.allocation.private_open_yard.cells,'#6c9a6e',.95)+cells(p.allocation.private_frontage_apron.cells,'#d48666',.8)+polygon(p.polygon,'none','#714c21',0);s+=line(p.frontage,'#8b3b1d',3);}
for(const i of ints.filter(i=>i.interface_id.includes('THRESHOLD')))s+=line(i.local_geometry.preferred_search_segment,'#c73729',6);
s+=marker(758,1626,'A')+marker(786,1629,'B')+marker(769,1632,'C')+marker(768,1645,'D')+marker(793,1636,'E');
s+=text(X(752),Z(1625),'低肩 Y129–133',16)+text(X(781),Z(1624),'上沿 Y133–136',16);
s+=line([[749,1647],[756,1645],[763,1642]],'#275b6a',4)+text(X(748),Z(1652),'西来先卸 → 手提到户',16);
s+=text(1200,145,'读图顺序',22,'#203342',700);
const notes=[['A｜BDP-01 下肩修理值守户','151 柱；家庭小院 18；门前 24。','较低肩部收件，家庭院不作货场。'],['B｜BDP-02 上沿复核短宿户','118 柱；家庭小院 8；门前 25。','一户 + 最多 2 名短宿者（待设计证明）。'],['C｜LANE-04 共同门前通行','名义宽 2；要求连续净宽 2、净高 3。','不是两户可封闭的联合私院。'],['D｜SPACE-01 卸载—复核共同院','外部直接依赖；两户不重复计地。','卸载、等候错峰；不圈占、不加户。'],['E｜LANE-02 东向轻载出口','名义宽 3；要求净宽 2、净高 3。','门前停步和短宿排队不能吞掉东口。']];
notes.forEach((n,i)=>{let y=192+i*119;s+=text(1200,y,n[0],19,'#203342',700)+text(1200,y+29,n[1],15)+text(1200,y+53,n[2],15);});
s+=text(1200,825,'地块不是整栋建筑轮廓',20,'#8b3b1d',700)+text(1200,856,'金色仅为建筑探索区，不是已定占地。',15)+text(1200,883,'房间、层数、屋顶、结构由 Builder 决定。',15);
const legends=[['#c8cbc7','灰阶：OBSERVED 地表高程'],['#d6a751','金色：PROPOSAL 建筑探索区'],['#6c9a6e','绿色：PROPOSAL 家庭小院'],['#d48666','赭色：PROPOSAL 户内门前缓冲'],['#70c7db','蓝色：PROPOSAL 公共路带'],['#c73729','红段：入口优先搜索段，非门洞']];
legends.forEach(([c,t],i)=>{let x=70+(i%3)*510,y=937+Math.floor(i/3)*36;s+=`<rect x="${x}" y="${y-17}" width="24" height="18" fill="${c}"/>`+text(x+35,y,t,16);});
s+=text(70,1034,'事实：地块表面为石质，无已观测土面/树冠/水面；浅层24格无空气 ≠ 深部安全或供水证明。',16);
s+=text(70,1067,'来源：MP-P04/r1 白名单直接对象；存档相关文件哈希本轮一致；CIV-001 Canon。新几何：MP-P05R2/r1。',15);
write('01-组团与地形.svg',s);

s=mapBase('MP-P05R2｜门前、公共净空与服务接口','设计阶段接口图 · 连续线为规划中心线；蓝色为按中心采样的名义路带，不代替最终净宽验证');
s+=polygon(common.local_geometry.polygon,'#ffffff','#738996',.35);
for(const i of ints.filter(i=>i.interface_id.includes('LANE')))s+=cells(i.local_geometry.cells,'#73cadd',.72)+line(i.local_geometry.centerline,'#00667d',3,'5 4');
for(const p of plan.parcels){s+=polygon(p.polygon,'#dec898','#714c21',.4)+cells(p.allocation.private_open_yard.cells,'#6c9a6e',.9)+cells(p.allocation.private_frontage_apron.cells,'#d48666',.85);}
for(const [idx,i] of ints.filter(i=>i.interface_id.includes('THRESHOLD')).entries()){s+=line(i.local_geometry.preferred_search_segment,'#c73729',7);let p=i.local_geometry.preferred_search_segment[0];s+=marker(p[0],p[1],String(idx+1));}
s+=line([[756,1623],[756,1643]],'#943d85',2,'6 5')+text(X(756)+6,Z(1621),'剖面 B',15,'#943d85');
s+=line([[784,1625],[784,1643]],'#943d85',2,'6 5')+text(X(784)+6,Z(1623),'剖面 C',15,'#943d85');
s+=text(X(767),Z(1636),'纵剖 A 沿 LANE-04',15,'#00667d');
s+=`<circle cx="${X(779.5)}" cy="${Z(1631.5)}" r="6" fill="#5c3b77"/><circle cx="${X(781.5)}" cy="${Z(1634.5)}" r="6" fill="#5c3b77"/>`;
s+=text(1200,145,'固定的是关系和保护范围',22,'#203342',700);
const lines=['1｜低肩门前：优先 X754–758','   现状接触顶面约 Y131–132。','2｜上沿门前：优先 X782–785','   现状接触顶面约 Y136。','','家庭门前：户内消化步级与停留。','公路净空：不得被门扇、货物、檐柱占用。','路面局部 ±1 格为待联合确认的调节范围。','','洁净水/日需：门内接收与储备预留。','污物：户内收集，错开洁净到货时间。','雨水：不得默认排向公共通路；受纳点 HOLD。','外部系统由 PUBLIC-COORDINATOR 协调。','','紫点：深部位置证据，Y81。','不是地表物件，也不是基础可开挖许可。','','入口红段仅为搜索段，可在本户等价移位。','所有公共边缘改动必须携带新 revision。'];
lines.forEach((l,i)=>s+=text(1200,190+i*31,l,15));
s+=text(70,945,'边界：CELL_CENTER_MASK；显式地块列见 BDP。建筑探索区与开放院/门前的面积不重叠。',17);
s+=text(70,980,'公共路带：名义宽与最低净宽分列。斜向落格、转弯和步级由联合设计验证，不宣称实机可通行。',17);
s+=text(70,1015,'当前：CONCEPT_DESIGN_READY。公共接触标高、雨水受纳及实际居住布局在设计冻结前闭合。',17,'#8b3b1d');
s+=text(70,1065,'来源：同图01；完整坐标、地面采样、权利语义、服务责任与 resolve_before 均在直接接口文件。',15);
write('02-门前与公共接口.svg',s);

s=head(1650,1140,'MP-P05R2｜门前纵横剖面基线','原始地形采样 + 规划关系；不绘制建筑楼层、基础、屋顶或最终步级 · world writes = 0');
const prof=read('evidence/公共路纵断面.json').find(p=>p.id==='LANE-04');
let left=90,top=160,w=1450,h=280,xmax=prof.samples.at(-1)[0];
const px=d=>left+d/xmax*w,py=y=>top+h-(y-129)/10*h;
for(let y=130;y<=138;y+=2)s+=`<path d="M${left},${py(y)} H${left+w}" stroke="#c7ceca"/>`+text(35,py(y)+5,y,15);
s+=text(90,126,'A｜沿 LANE-04：低肩 → 两户之间 → 上沿轻载口',21,'#203342',700);
s+=`<polyline points="${prof.samples.map(c=>`${px(c[0])},${py(c[3]+1)}`).join(' ')}" fill="none" stroke="#355c55" stroke-width="4"/>`;
for(const n of [0,9,18,27,prof.samples.length-1]){let c=prof.samples[n];s+=`<circle cx="${px(c[0])}" cy="${py(c[3]+1)}" r="5" fill="#355c55"/>`+text(px(c[0])-20,py(c[3]+1)-15,`Y${c[3]+1}`,15)+text(px(c[0])-25,470,`${c[1]},${c[2]}`,13);}
s+=text(90,507,'绿线 = 观测地面顶面（ground_y+1）。最高相邻采样差1格；这不是最终踏步或移动测试。',17);
function cross(x,z0,z1,title,xoff){const cc=surface.columns.filter(c=>c[0]===x&&c[1]>=z0&&c[1]<=z1).sort((a,b)=>a[1]-b[1]);const baseY=129,xp=z=>xoff+(z-z0)/(z1-z0)*630,yp=y=>855-(y-baseY)*22;let v=text(xoff,566,title,21,'#203342',700);for(let y=130;y<=138;y+=2)v+=`<path d="M${xoff},${yp(y)} h630" stroke="#c7ceca"/>`+text(xoff-36,yp(y)+5,y,14);
for(const p of plan.parcels){for(const [kind,color] of [['private_open_yard','#6c9a6e'],['private_frontage_apron','#d48666'],['architectural_search_mask','#d6a751']])for(const c of p.allocation[kind].cells.filter(c=>c[0]===x&&c[1]>=z0&&c[1]<=z1))v+=`<rect x="${xp(c[1])}" y="590" width="${630/(z1-z0)}" height="25" fill="${color}"/>`;}
v+=`<polyline points="${cc.map(c=>`${xp(c[1])},${yp(c[3]+1)}`).join(' ')}" fill="none" stroke="#355c55" stroke-width="4"/>`;for(let z=z0;z<=z1;z+=4)v+=text(xp(z)-18,881,z,14);v+=text(xoff,916,'Z → 南；水平为真实距离，垂直比例另标 Y。',15);return v;}
s+=cross(756,1623,1643,'B｜X756：家庭小院 → 门内缓冲 → 通路',90);
s+=cross(784,1625,1643,'C｜X784：上沿户 → 门前缓冲 → 东向接口',880);
s+=text(90,974,'横剖顶部色带为规划使用区：绿=私院；金=建筑搜索；赭=门前缓冲。色带不是建筑体量。',17);
s+=text(90,1011,'公共接触面可在现状顶面±1格范围联合探索；Builder 必须把户内外连续性与净宽同时证明。',17);
s+=text(90,1048,'深部保护：另有 Y81 实体位置证据；本图只画近地剖面，不把深部未知区画成可施工实心地层。',17);
s+=text(90,1094,'来源：MP-P04/r1 原始地表/近地调查，相关存档哈希本轮一致；接口提案 MP-P05R2/r1。',15);
write('03-地形与门前剖面.svg',s);
console.log('Created 3 coordinate-based SVG maps.');
