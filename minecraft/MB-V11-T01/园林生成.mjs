import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';

// 本任务复现入口只生成蓝图，不接触存档。阶段差分保持明确的方块来源。
const root=path.dirname(fileURLToPath(import.meta.url));
const vox=new Map(), stages=[], components=[], routes=[];
let delta=new Map();
const key=(x,y,z)=>`${x},${y},${z}`;
function set(x,y,z,s){x=Math.round(x);y=Math.round(y);z=Math.round(z);s=s.startsWith('minecraft:')?s:'minecraft:'+s;const k=key(x,y,z);vox.set(k,s);delta.set(k,s);}
function box(x1,y1,z1,x2,y2,z2,s){for(let y=y1;y<=y2;y++)for(let z=z1;z<=z2;z++)for(let x=x1;x<=x2;x++)set(x,y,z,s);}
function ell(cx,cy,cz,rx,ry,rz,s,rough=0){for(let y=Math.floor(cy-ry);y<=cy+ry;y++)for(let z=Math.floor(cz-rz);z<=cz+rz;z++)for(let x=Math.floor(cx-rx);x<=cx+rx;x++){let d=((x-cx)/rx)**2+((y-cy)/ry)**2+((z-cz)/rz)**2;if(d<=1+rough*Math.sin(x*1.7+y*.9+z*2.3))set(x,y,z,s);}}
function line(a,b,r,s){let n=Math.ceil(Math.max(...a.map((v,i)=>Math.abs(v-b[i])))*1.5);for(let t=0;t<=n;t++){let p=a.map((v,i)=>v+(b[i]-v)*t/n);ell(...p,r,r,r,s);}}
function top(x,z){for(let y=91;y>=57;y--){let s=vox.get(key(x,y,z));if(s&&!s.endsWith(':air')&&!s.includes('leaves')&&!s.includes('water'))return y;}return 63;}
function stage(name){const groups=new Map();for(const[k,s]of delta){let[x,y,z]=k.split(',').map(Number),gx=Math.floor(x/48)*48,gz=Math.floor(z/48)*48,g=key(gx,0,gz);if(!groups.has(g))groups.set(g,{schema_version:1,origin:{x:gx,y:56,z:gz},dimensions:{x:48,y:48,z:48},palette:[],blocks:[],metadata:{name,task:'MB-V11-T01',content_omissions:[]}});let b=groups.get(g),p=b.palette.indexOf(s);if(p<0){p=b.palette.length;b.palette.push(s);}b.blocks.push([x-gx,y-56,z-gz,p]);}
 fs.mkdirSync(path.join(root,'蓝图'),{recursive:true});let files=[];let i=0;for(const b of groups.values()){checkBlueprint(b,{previewOnly:true});let file=`蓝图/${stages.length+1}-${++i}.json`;fs.writeFileSync(path.join(root,file),JSON.stringify(b));files.push(file);}stages.push({name,files,changed:delta.size});delta=new Map();}

const hills=[[56,48,21,28,13],[72,63,18,23,9],[40,70,15,23,7],[144,26,23,15,5],[25,30,13,16,4]];
function ground(x,z){let h=0;for(const[cx,cz,rx,rz,a]of hills){let d=((x-cx)/rx)**2+((z-cz)/rz)**2;h=Math.max(h,a*Math.max(0,1-d)**.8);}return 63+Math.round(h);}
function water(x,z){return ((x-107)/39)**2+((z-78)/29)**2<1+.13*Math.sin(x*.12+z*.06)||((x-138)/14)**2+((z-103)/20)**2<1||((x-83)/16)**2+((z-57)/16)**2<1;}
// 平板仅为画布；池床开挖，叠山与台地在同一阶段形成。
for(let z=0;z<=148;z++)for(let x=0;x<=184;x++){
 const h=ground(x,z);if(water(x,z)){box(x,59,z,x,61,z,'clay');set(x,62,z,'water[level=0]');box(x,63,z,x,64,z,'air');}
 else{box(x,63,z,x,h,z,'dirt');set(x,h,z,'grass_block');if([[1,0],[-1,0],[0,1],[0,-1]].some(([a,b])=>water(x+a,z+b)))set(x,h,z,(x+z)%4?'stone':'andesite');}
}
// 偏心岛山分割主池的视线，水路保持连通。
for(let z=54;z<=74;z++)for(let x=103;x<=124;x++)if(((x-114)/11)**2+((z-64)/10)**2<1){box(x,60,z,x,64,z,'stone');set(x,65,z,'grass_block');}
function hall(name,cx,cz,w,d,fy,roofH=6){let x1=cx-Math.floor(w/2),x2=cx+Math.floor(w/2),z1=cz-Math.floor(d/2),z2=cz+Math.floor(d/2);box(x1-1,fy-1,z1-1,x2+1,fy,z2+1,'stone_bricks');box(x1,fy+1,z1,x2,fy+5,z2,'air');for(let x=x1;x<=x2;x+=Math.max(4,Math.floor(w/3)))for(let z of[z1,z2])box(x,fy+1,z,x,fy+5,z,'dark_oak_log[axis=y]');for(let x of[x1,x2])for(let z of[z1,z2])box(x,fy+1,z,x,fy+5,z,'dark_oak_log[axis=y]');box(x1,fy+5,z1,x2,fy+5,z2,'dark_oak_planks');box(x1+1,fy+5,z1+1,x2-1,fy+5,z2-1,'air');
 for(let z=z1-2;z<=z2+2;z++){let dz=Math.abs(z-cz),half=Math.floor(d/2)+2;for(let x=x1-2;x<=x2+2;x++){let slope=w<=13?Math.max(dz/half,Math.abs(x-cx)/(Math.floor(w/2)+2)):dz/half;let y=fy+6+Math.round((1-slope)*roofH)+(slope===1?1:0);set(x,y,z,'deepslate_tiles');if(dz===0&&w>13)set(x,y+1,z,'polished_blackstone_bricks');}}
 components.push({name,type:'building',bounds:[x1-2,fy-1,z1-2,x2+2,fy+7+roofH,z2+2],floor:fy,entry:[cx,fy+1,z2+1]});}
hall('听荷厅',105,117,27,13,64,5);
hall('入园门厅',38,139,15,7,63,3);
hall('山顶小亭',57,47,9,7,76,3);
hall('水心亭',114,64,9,7,65,3);
hall('东岸水榭',152,89,9,13,64,4);
hall('西院书斋',30,105,17,9,64,4);
hall('竹院小轩',159,34,13,7,67,3);
// 主树偏向水岸与围墙布置；分枝冠团尺寸随各自的空间职责变化。
function tree(name,x,z,h,r,lean=2,leaf='oak_leaves'){let y=ground(x,z)+1;line([x,y,z],[x+lean,y+h*.64,z-1],1.1,'oak_log[axis=y]');let branches=[[-.75,-.2,.62],[.65,-.5,.74],[-.2,.65,.8],[.55,.55,.9],[0,0,1]];for(let i=0;i<branches.length;i++){let[a,b,c]=branches[i],end=[x+lean+a*r*.8,y+h*c-2,z+b*r];line([x+lean*.6,y+h*.45,z],end,.65,'oak_log[axis=y]');ell(end[0],end[1]+1,end[2],r*(i===4?.65:.64),h*.17,r*.61,`${leaf}[persistent=true]`,.11);}components.push({name,type:'tree',bounds:[x-r-2,y,z-r-2,x+r+lean+2,y+h+2,z+r+2],role:'canopy / enclosure / framed view'});}
tree('入口偏冠香樟',25,123,16,10,3);tree('西院古树',15,94,20,12,3);tree('西山背景一',34,45,18,10,-2);tree('西山背景二',43,24,22,12,4);tree('北缘高冠',87,24,21,12,-2);tree('北缘副树',106,26,16,9,2);tree('东北林冠',131,18,18,11,2);tree('东南水岸柳',144,120,14,9,-4,'azalea_leaves');tree('东界主树',174,74,20,12,-2);tree('东界副树',174,106,16,9,-2);tree('西南院外',13,132,15,8,2);tree('北岸框景树',100,42,14,8,-3);tree('东院树',177,29,16,9,-2);
// Macro 预览修订：西岸土崖改为与山体相连的叠石岸，南部留白改为两处可辨认的庭院。
for(let z=35;z<96;z++)for(let x=55;x<90;x++)if(!water(x,z)&&[[1,0],[2,0],[0,1],[0,-1]].some(([a,b])=>water(x+a,z+b))){let h=ground(x,z);box(x,62,z,x,h,z,(x+z)%3?'andesite':'stone');if(h>68&&z%5<3)box(x+1,63,z,x+1,h-2,z,'stone');}
box(23,63,133,55,63,146,'smooth_stone');box(8,63,100,40,63,111,'gravel');
for(let z=129;z<=143;z++)for(let x=77;x<=132;x++)if(((x-104)/29)**2+((z-137)/8)**2<1)set(x,63,z,'gravel');
tree('南院疏影一',77,141,10,6,1);tree('南院疏影二',93,144,8,5,-2);tree('南院疏影三',123,142,11,6,-1);tree('东南围合树',165,137,17,11,-3);tree('西北林缘',15,30,16,9,2);tree('西北林下',13,51,11,7,1);
// 水岸柳的下垂枝梢以窄叶束形成区别于香樟团冠的轮廓。
for(const[x,z,y]of[[137,119,76],[144,113,77],[150,119,75],[145,126,76],[137,124,74]])for(let j=0;j<5;j++)set(x,y-j,z,'azalea_leaves[persistent=true]');
stage('Macro：山水、主树与建筑体量');

function walk(name,pts,width=3){let cells=new Map();for(let i=1;i<pts.length;i++){let a=pts[i-1],b=pts[i],n=Math.max(Math.abs(b[0]-a[0]),Math.abs(b[2]-a[2]),1);for(let j=0;j<=n;j++){let x=Math.round(a[0]+(b[0]-a[0])*j/n),z=Math.round(a[2]+(b[2]-a[2])*j/n),y=Math.round(a[1]+(b[1]-a[1])*j/n);for(let dz=-Math.floor(width/2);dz<=Math.floor(width/2);dz++)for(let dx=-Math.floor(width/2);dx<=Math.floor(width/2);dx++)cells.set(`${x+dx},${z+dz}`,[x+dx,y,z+dz]);}}
 for(const[x,y,z]of cells.values()){let old=ground(x,z);box(x,Math.min(old,y),z,x,y,z,'stone');set(x,y,z,'smooth_stone');box(x,y+1,z,x,y+3,z,'air');}routes.push({name,points:pts,width,cells:[...cells.values()]});}
walk('入园藏露',[ [38,63,151],[38,63,132],[49,63,132],[55,63,120],[64,63,113],[80,63,116],[85,63,126],[105,64,126],[105,64,117] ],3);
walk('西岸环路',[[55,63,120],[48,63,102],[49,64,88],[60,65,79],[69,64,72],[73,63,50],[86,63,39],[105,63,37],[126,64,40],[145,64,52]],3);
walk('东岸环路',[[145,64,52],[157,64,63],[158,64,77],[152,64,89],[155,64,104],[151,63,119],[134,63,129],[114,63,133],[88,63,130],[64,63,113]],3);
walk('西院游廊',[[49,63,132],[45,63,122],[30,64,120],[30,64,105],[25,64,94],[25,64,75],[32,65,66],[40,67,65]],3);
walk('登山回望',[[49,64,88],[41,67,78],[43,69,68],[52,72,66],[61,74,57],[57,76,47]],3);
walk('山后下行',[[57,76,47],[64,73,35],[75,68,34],[86,63,39]],3);
walk('曲桥入岛',[[145,64,52],[136,64,52],[131,65,59],[125,65,59],[121,65,64],[114,65,64]],3);
walk('竹院支路',[[145,64,52],[153,66,44],[159,67,34],[172,66,36]],3);
// 主池通透，复廊沿岸收窄视域，不在池中网格划分。
function gallery(points,y=64){for(let i=1;i<points.length;i++){let a=points[i-1],b=points[i],n=Math.max(Math.abs(b[0]-a[0]),Math.abs(b[1]-a[1]));for(let t=0;t<=n;t++){let x=Math.round(a[0]+(b[0]-a[0])*t/n),z=Math.round(a[1]+(b[1]-a[1])*t/n);let alongX=Math.abs(b[0]-a[0])>Math.abs(b[1]-a[1]);for(let o=-3;o<=3;o++)set(x+(alongX?0:o),y+5+Math.max(0,2-Math.abs(o)),z+(alongX?o:0),'deepslate_tiles');if(t%7===0)for(let o of[-2,2])box(x+(alongX?0:o),y+1,z+(alongX?o:0),x+(alongX?0:o),y+4,z+(alongX?o:0),'dark_oak_log[axis=y]');}}}
gallery([[25,94],[25,75]],64);gallery([[157,63],[157,77]],64);
// 外墙是宅园的城市边界；内部屏墙与月洞门负责先藏后露。
box(0,64,0,184,68,0,'white_concrete');box(0,64,148,184,68,148,'white_concrete');box(0,64,0,0,68,148,'white_concrete');box(184,64,0,184,68,148,'white_concrete');
box(0,69,0,184,69,0,'deepslate_tiles');box(0,69,148,184,69,148,'deepslate_tiles');box(0,69,0,0,69,148,'deepslate_tiles');box(184,69,0,184,69,148,'deepslate_tiles');box(36,64,148,40,68,148,'air');
box(31,64,130,44,68,130,'white_concrete');box(30,69,130,45,69,130,'deepslate_tiles');
box(63,64,117,63,68,138,'white_concrete');box(63,69,117,63,69,138,'deepslate_tiles');for(let z=120;z<=126;z++)for(let y=64;y<=69;y++)if(((z-123)/3.5)**2+((y-66)/3.5)**2<=1)set(63,y,z,'air');
box(143,64,24,143,69,43,'white_concrete');box(143,70,24,143,70,43,'deepslate_tiles');
box(8,64,114,39,67,114,'white_concrete');box(8,68,114,39,68,114,'deepslate_tiles');box(28,65,114,32,68,114,'air');
box(72,64,145,138,67,145,'white_concrete');box(72,68,145,138,68,145,'deepslate_tiles');
// 叠石采用互相错位的峰、洞、隙，不以独立石球填充绿地。
for(const[cx,cz,h,rx,rz]of[[66,79,8,6,5],[73,70,6,5,7],[80,55,8,5,5],[45,55,10,6,5],[32,70,7,4,5],[130,79,4,3,4]]){let y=ground(cx,cz);ell(cx,y+h*.35,cz,rx,h*.65,rz,'andesite',.2);ell(cx+2,y+h*.7,cz-1,rx*.6,h*.45,rz*.6,'stone',.16);ell(cx-1,y+2,cz,2,2,rz+1,'air');}
// 竹丛按照空间开口分为数团，主路径保留两格以上净空。
for(const[cx,cz,rx,rz]of[[150,23,5,6],[169,45,7,8],[171,56,5,6],[17,70,5,10],[33,115,4,3],[20,17,10,6],[17,59,6,8],[57,139,5,5]])for(let z=cz-rz;z<=cz+rz;z++)for(let x=cx-rx;x<=cx+rx;x++)if(((x-cx)/rx)**2+((z-cz)/rz)**2<1&&((x*19+z*31)%7===0)){let y=ground(x,z),h=6+Math.abs((x*7+z*3)%6);if(routes.some(r=>r.cells.some(c=>Math.abs(c[0]-x)<2&&Math.abs(c[2]-z)<2)))continue;for(let j=1;j<=h;j++)set(x,y+j,z,`bamboo[age=1,leaves=${j>h-3?'large':'none'},stage=1]`);}
// 叠石后的最后一次净空处理形成可穿行的山径，不让后置山石截断已有游线。
for(const r of routes.filter(r=>['西岸环路','西院游廊','登山回望','山后下行'].includes(r.name)))for(const[x,y,z]of r.cells)box(x,y+1,z,x,y+3,z,'air');
// 高差处采用实体楼梯，玩家无需沿整格台阶连续跳跃。
for(const r of routes.filter(r=>['登山回望','山后下行','竹院支路'].includes(r.name))){let floors=new Map(r.cells.map(c=>[`${c[0]},${c[2]}`,c[1]]));for(const[x,y,z]of r.cells)for(const[dx,dz,facing]of[[1,0,'west'],[-1,0,'east'],[0,1,'north'],[0,-1,'south']])if(floors.get(`${x+dx},${z+dz}`)===y-1){set(x,y,z,`stone_brick_stairs[facing=${facing},half=bottom,shape=straight,waterlogged=false]`);break;}}
stage('Meso：游线、复廊、叠石、竹林与屏墙');

// 厅堂侧面保留格扇语汇，主要出入口及观水面不封死。
for(const b of components.filter(c=>c.type==='building'&&c.bounds[3]-c.bounds[0]>17)){let[x1,,z1,x2,,z2]=b.bounds,fy=b.floor;x1+=2;x2-=2;z1+=2;z2-=2;for(let x of[x1,x2]){box(x,fy+1,z1+1,x,fy+2,z2-1,'white_concrete');for(let z=z1+2;z<z2;z+=2)box(x,fy+3,z,x,fy+4,z,'dark_oak_fence');}}
// 曲桥护栏只在侧缘设置，不侵占主行走带。
for(const r of routes.filter(r=>r.name==='曲桥入岛'))for(const[x,y,z]of r.cells){if(water(x,z)&&!r.cells.some(c=>c[0]===x&&c[2]===z-1))set(x,y+1,z,'dark_oak_fence');}
for(let z=51;z<=118;z++)for(let x=70;x<=145;x++){if(water(x,z)&&vox.get(key(x,63,z))==='minecraft:air'&&((x*13+z*17)%53===0)&&((x-104)**2+(z-106)**2<260||(x-76)**2+(z-59)**2<90))set(x,63,z,'lily_pad');}
for(const[cx,cz,rx,rz]of[[11,111,5,8],[69,136,10,4],[169,122,8,7],[105,16,9,4],[28,16,7,5],[164,15,8,3]])for(let z=cz-rz;z<=cz+rz;z++)for(let x=cx-rx;x<=cx+rx;x++)if(((x-cx)/rx)**2+((z-cz)/rz)**2<1&&((x+z)%3!==0)){let y=ground(x,z);set(x,y+1,z,'azalea_leaves[persistent=true]');if((x*3+z)%5===0)set(x,y+2,z,'azalea_leaves[persistent=true]');}
stage('Micro：格扇、桥栏、荷叶与林下层');
fs.writeFileSync(path.join(root,'阶段清单.json'),JSON.stringify({task:'MB-V11-T01',world_name:'MB-V11-T01-苏州园林',bounds:[0,56,0,184,103,151],stages,components,routes},null,2));
fs.writeFileSync(path.join(root,'设计方块.json'),JSON.stringify([...vox].map(([k,s])=>[...k.split(',').map(Number),s])));
console.log(JSON.stringify(stages.map(s=>({name:s.name,tiles:s.files.length,changed:s.changed}))));
