"""仅解码预先选定柱，不生成区块；标量主读与独立向量解包逐样本比对。"""
import io,gzip,zlib
import numpy as np
import nbtlib
class ColumnReader:
    def __init__(self,world):self.world=world;self.cache={};self.checked=0
    def chunk(self,cx,cz):
        key=(cx,cz)
        if key not in self.cache:
            p=self.world/'dimensions/minecraft/overworld/region'/f'r.{cx//32}.{cz//32}.mca'
            with p.open('rb') as f:
                f.seek(((cz%32)*32+cx%32)*4);loc=int.from_bytes(f.read(4),'big');assert loc
                f.seek((loc>>8)*4096);size=int.from_bytes(f.read(4),'big');kind=f.read(1)[0];raw=f.read(size-1)
            if kind&128:raw=(p.parent/f'c.{cx}.{cz}.mcc').read_bytes()
            if kind&127==2:raw=zlib.decompress(raw)
            elif kind&127==1:raw=gzip.decompress(raw)
            elif kind&127!=3:raise ValueError('unsupported compression')
            d=nbtlib.File.parse(io.BytesIO(raw));assert int(d['DataVersion'])==4903 and str(d['Status'])=='minecraft:full'
            assert (int(d['xPos']),int(d['zPos']))==key
            self.cache[key]=d
        return self.cache[key]
    def read(self,x,z,top):
        d=self.chunk(x//16,z//16);sections={int(s['Y']):s for s in d['sections']};blocks=[];decoded={}
        for y in range(-60,top+1):
            s=sections.get(y//16);name='minecraft:air'
            if s is not None and 'block_states' in s:
                p=s['block_states'];pal=p['palette'];bits=max(4,(len(pal)-1).bit_length());idx=(y%16)*256+(z%16)*16+x%16;words=p.get('data')
                code=0 if words is None else ((int(words[idx//(64//bits)])&((1<<64)-1))>>((idx%(64//bits))*bits))&((1<<bits)-1)
                name=str(pal[code]['Name'])
                # 独立向量索引验证主读的长字边界，不调用标量位提取公式。
                if y//16 not in decoded:
                    if words is None:codes=np.zeros(4096,dtype=np.int32)
                    else:
                        data=np.asarray(words,dtype=np.int64).view(np.uint64);ii=np.arange(4096,dtype=np.uint64);per=64//bits
                        codes=((data[ii//per]>>((ii%per)*np.uint64(bits)))&np.uint64((1<<bits)-1)).astype(np.int32)
                    decoded[y//16]=[str(v['Name']) for v in pal],codes
                names,codes=decoded[y//16];assert names[codes[idx]]==name;self.checked+=1
            blocks.append(name)
        return blocks
