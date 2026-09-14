// 工程外围复现脚本：只计算模型已经选定的几何，不生成规划判断。
export function inPolygon(x,z,poly){let yes=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const [ax,az]=poly[i],[bx,bz]=poly[j];if((az>z)!==(bz>z)&&x<(bx-ax)*(z-az)/(bz-az)+ax)yes=!yes;}return yes;}
export function distance(x,z,points){let d=Infinity;for(let i=1;i<points.length;i++){const [a,b]=points[i-1],[c,e]=points[i],dx=c-a,dz=e-b,t=Math.max(0,Math.min(1,((x-a)*dx+(z-b)*dz)/(dx*dx+dz*dz)));d=Math.min(d,Math.hypot(x-a-t*dx,z-b-t*dz));}return d;}
export const key=c=>c.slice(0,2).join(',');
export function mask(poly){let cells=[];for(let z=Math.floor(Math.min(...poly.map(p=>p[1])));z<Math.ceil(Math.max(...poly.map(p=>p[1])));z++)for(let x=Math.floor(Math.min(...poly.map(p=>p[0])));x<Math.ceil(Math.max(...poly.map(p=>p[0])));x++)if(inPolygon(x+.5,z+.5,poly))cells.push([x,z]);return cells;}
export function area(poly){return Math.abs(poly.reduce((s,a,i)=>{let b=poly[(i+1)%poly.length];return s+a[0]*b[1]-b[0]*a[1];},0))/2;}
