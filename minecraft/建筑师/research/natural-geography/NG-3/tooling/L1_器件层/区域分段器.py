"""生成可审阅的数值分段，不负责地貌语义promotion。水样本屏障不能被小斑合并跨越。"""
from collections import deque,Counter
import numpy as np

def components(mask):
    labels=np.zeros(mask.shape,np.int32);count=0
    for z,x in zip(*np.where(mask)):
        if labels[z,x]:continue
        count+=1;labels[z,x]=count;q=deque([(int(z),int(x))])
        while q:
            a,b=q.popleft()
            for c,d in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                if 0<=c<mask.shape[0] and 0<=d<mask.shape[1] and mask[c,d] and not labels[c,d]:labels[c,d]=count;q.append((c,d))
    return labels,count

def segment(rows):
    gx0=min(r['gx'] for r in rows);gz0=min(r['gz'] for r in rows)
    shape=(max(r['gz'] for r in rows)-gz0+1,max(r['gx'] for r in rows)-gx0+1)
    h=np.full(shape,np.nan);water=np.zeros(shape);relief=np.zeros(shape)
    for r in rows:
        j,i=r['gz']-gz0,r['gx']-gx0;h[j,i]=r['elevation'];water[j,i]=r['water'];relief[j,i]=r['relief']
    valid=np.isfinite(h);wet=(water>=0.6)&valid;land=valid&~wet
    # 320格窗口降低64格阈值碎片；仅陆地值参与均值，避免水位把山麓压低。
    sums=np.zeros(shape);counts=np.zeros(shape);lo=np.full(shape,np.inf);hi=np.full(shape,-np.inf)
    ph=np.pad(h,2,constant_values=np.nan);pm=np.pad(land,2)
    for dz in range(5):
        for dx in range(5):
            a=ph[dz:dz+shape[0],dx:dx+shape[1]];m=pm[dz:dz+shape[0],dx:dx+shape[1]]
            sums+=np.where(m,a,0);counts+=m;lo=np.minimum(lo,np.where(m,a,np.inf));hi=np.maximum(hi,np.where(m,a,-np.inf))
    smooth=np.divide(sums,counts,out=np.zeros(shape),where=counts>0);regional_relief=np.where(counts,hi-lo,0)
    bands=np.where(smooth>=280,3,np.where(smooth>=140,2,np.where(regional_relief>=40,1,0)));bands[~land]=-1
    units=np.zeros(shape,np.int32);offset=0
    for band in range(4):
        labels,n=components(land&(bands==band));units[labels>0]=labels[labels>0]+offset;offset+=n
    # 小于64采样格的接壤斑归并到已有相邻单元，优先共享边和近似高程；孤立岛斑保持未解。
    while True:
        ids,sizes=np.unique(units[units>0],return_counts=True);changed=False
        for id,size in sorted(zip(ids,sizes),key=lambda v:(v[1],v[0])):
            if size>=64 or not np.any(units==id):continue
            mask=units==id;neighbors=Counter()
            for dz,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                for z,x in zip(*np.where(mask)):
                    zz,xx=z+dz,x+dx
                    if 0<=zz<shape[0] and 0<=xx<shape[1] and units[zz,xx]>0 and units[zz,xx]!=id:neighbors[int(units[zz,xx])]+=1
            if neighbors:
                mean=float(np.mean(h[mask]));other=min(neighbors,key=lambda n:(abs(float(np.mean(h[units==n]))-mean)/100-neighbors[n],n))
                units[mask]=other;changed=True
        if not changed:break
    ids,sizes=np.unique(units[units>0],return_counts=True)
    for id,size in zip(ids,sizes):
        if size<64:units[units==id]=-1
    wl,wn=components(wet)
    for id,size in zip(*np.unique(wl[wl>0],return_counts=True)):
        if size<16:wl[wl==id]=-1
    return {'height':h,'water_fraction':water,'land_units':units,'water_units':wl,'smoothed_height':smooth,'regional_relief':regional_relief,'numeric_bands':bands,'origin':np.array([gx0,gz0])}
