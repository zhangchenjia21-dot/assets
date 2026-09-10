/** 软件几何审计：只绘制给定保存区块，不生成不存在的景物，不冒充客户端截图。 */
import fs from 'node:fs';const c=JSON.parse(fs.readFileSync(process.argv[2],'utf8').replace(/^\uFEFF/,'')),v=fs.readFileSync(c.volume),[W,H,D]=c.size,[rw,rh]=c.res;
const norm=a=>{const n=Math.hypot(...a);return a.map(x=>x/n)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const f=norm(c.target.map((x,i)=>x-c.eye[i])),r=norm(cross(f,[0,1,0])),u=cross(r,f),eye=[c.eye[0],c.eye[1]-56,c.eye[2]],scale=Math.tan(c.fov*Math.PI/360),sun=norm([-.5,1,.35]);
function box(o,d,b){let lo=-Infinity,hi=Infinity,n=[0,1,0];for(let i=0;i<3;i++){if(Math.abs(d[i])<1e-9){if(o[i]<b[i]||o[i]>b[i+3])return null;continue;}let a=(b[i]-o[i])/d[i],z=(b[i+3]-o[i])/d[i],nn=[0,0,0];nn[i]=d[i]>0?-1:1;if(a>z)[a,z]=[z,a];if(a>lo){lo=a;n=nn;}hi=Math.min(hi,z);if(lo>hi)return null;}return hi<0?null:{t:Math.max(0,lo),n};}
const forms=c.palette.map(p=>{
 if(/:(air|cave_air|void_air)$/.test(p))return [];
 if(/fern|short_grass|lily_of_the_valley|allium|blue_orchid/.test(p))return [[.1,0,.46,.9,.7,.54],[.46,0,.1,.54,.7,.9]];
 if(p.includes('_slab'))return [[0,0,0,1,.5,1]];
 if(p.includes('_stairs')){const a=[0,0,0,1,.5,1],b=[0,.5,0,1,1,1];if(p.includes('facing=north'))b[5]=.5;else if(p.includes('facing=south'))b[2]=.5;else if(p.includes('facing=east'))b[0]=.5;else b[3]=.5;return[a,b];}
 if(p.includes('_fence')){const b=[[.36,0,.36,.64,1.5,.64]];for(const y of [.4,.8]){if(p.includes('east=true'))b.push([.5,y,.44,1,y+.15,.56]);if(p.includes('west=true'))b.push([0,y,.44,.5,y+.15,.56]);if(p.includes('north=true'))b.push([.44,y,0,.56,y+.15,.5]);if(p.includes('south=true'))b.push([.44,y,.5,.56,y+.15,1]);}return b;}
 return [[0,0,0,1,1,1]];
});
function ray(o,d,max=600,shadow=false){const en=box(o,d,[0,0,0,W,H,D]);if(!en)return null;let t=en.t+1e-5;const p=o.map((x,i)=>x+d[i]*t),cell=p.map(Math.floor),step=d.map(x=>x>0?1:-1),delta=d.map(x=>Math.abs(1/x)),next=d.map((x,i)=>t+((x>0?cell[i]+1:cell[i])-p[i])/x);
 for(let count=0;count<1000&&t<max;count++){const[x,y,z]=cell;if(x<0||x>=W||y<0||y>=H||z<0||z>=D)return null;const id=v[(x*H+y)*D+z];if(forms[id].length&&!(shadow&&/fern|grass|allium|orchid|lily/.test(c.palette[id]))){let hit=null;for(const b of forms[id]){const a=box(o,d,b.map((q,i)=>q+cell[i%3]));if(a&&a.t>=t-1e-4&&(!hit||a.t<hit.t))hit=a;}if(hit)return{...hit,id};}let a=next[0]<next[1]?(next[0]<next[2]?0:2):(next[1]<next[2]?1:2);t=next[a];next[a]+=delta[a];cell[a]+=step[a];}return null;}
const out=Buffer.alloc(rw*rh*3),sky=[177,203,207];
for(let y=0;y<rh;y++)for(let x=0;x<rw;x++){
 const sx=(2*(x+.5)/rw-1)*scale*rw/rh,sy=(1-2*(y+.5)/rh)*scale,d=norm(f.map((a,i)=>a+sx*r[i]+sy*u[i])),hit=ray(eye,d);let color=sky;
 if(hit){const p=eye.map((a,i)=>a+d[i]*hit.t+hit.n[i]*.006);let light=.76+.24*Math.max(0,hit.n.reduce((a,b,i)=>a+b*sun[i],0));if(ray(p,sun,60,true))light*=.78;if(c.palette[hit.id].includes('shroomlight'))light=1;const fog=Math.min(.18,hit.t/1000);color=c.colors[hit.id].map((a,i)=>a*light*(1-fog)+sky[i]*fog);}
 const k=(y*rw+x)*3;for(let i=0;i<3;i++)out[k+i]=Math.round(color[i]);
}fs.writeFileSync(c.output,Buffer.concat([Buffer.from(`P6\n${rw} ${rh}\n255\n`),out]));
