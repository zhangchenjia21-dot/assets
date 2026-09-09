"""独立并查集重建全ROI干陆/水区间图，与生产队列遍历的分量一一比较。"""
import json,sys
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tooling'))
from L1_器件层.区域指标计算器 import load_observed
from L1_器件层.源快照保护器 import write_json

def validate():
    a,_,_=load_observed(ROOT/'raw-or-queryable/observed.sqlite');m=np.load(ROOT/'raw-or-queryable/derived.npz');wet=a['water_y']!=-32768;indices=np.arange(wet.size).reshape(wet.shape);reports=[]
    for mask,key in [(~wet,'land_component'),(wet,'water_component')]:
        parent=list(range(wet.size));rank=bytearray(wet.size)
        def find(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        for axis in (0,1):
            p=[slice(None),slice(None)];q=p.copy();p[axis]=slice(None,-1);q[axis]=slice(1,None);p=tuple(p);q=tuple(q)
            connected=mask[p]&mask[q]
            if key=='water_component':connected &= np.maximum(a['water_bottom'][p],a['water_bottom'][q])<=np.minimum(a['water_y'][p],a['water_y'][q])
            for i,j in zip(indices[p][connected],indices[q][connected]):
                i=find(int(i));j=find(int(j))
                if i==j:continue
                if rank[i]<rank[j]:i,j=j,i
                parent[j]=i
                if rank[i]==rank[j]:rank[i]+=1
        production=m[key].ravel();label_to_root={};root_to_label={}
        for i in np.flatnonzero(mask):
            root=find(int(i));label=int(production[i])
            if label in label_to_root:assert label_to_root[label]==root,'production falsely joined disconnected columns'
            else:label_to_root[label]=root
            if root in root_to_label:assert root_to_label[root]==label,'production falsely split connected columns'
            else:root_to_label[root]=label
        reports.append({'layer':key,'components':len(label_to_root),'columns':int(mask.sum()),'bijection':'PASS'})
    write_json(ROOT/'validation/topology-independent.json',{'status':'PASS','method':'Independent union-find over every dry/wet column; water edge requires vertical interval overlap; compares bijection to BFS labels','layers':reports});print('independent full topology PASS',flush=True)
if __name__=='__main__':validate()
