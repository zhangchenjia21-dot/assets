"""只解析顶层 Status/DataVersion；跳过 NBT 数组载荷，避免为覆盖审计逐方块解码。"""
import gzip
import struct
import zlib

def top_metadata(data):
    def u16(p):return int.from_bytes(data[p:p+2],'big')
    def i32(p):return struct.unpack_from('>i',data,p)[0]
    def skip_string(p):return p+2+u16(p)
    def skip(kind,p):
        if kind in (1,2,3,4,5,6):return p+{1:1,2:2,3:4,4:8,5:4,6:8}[kind]
        if kind in (7,11,12):
            n=i32(p)
            if n<0:raise ValueError('negative array length')
            return p+4+n*{7:1,11:4,12:8}[kind]
        if kind==8:return skip_string(p)
        if kind==9:
            subtype=data[p];n=i32(p+1);p+=5
            if n<0:raise ValueError('negative list length')
            if subtype in (1,2,3,4,5,6):return p+n*{1:1,2:2,3:4,4:8,5:4,6:8}[subtype]
            for _ in range(n):p=skip(subtype,p)
            return p
        if kind==10:
            while data[p]:
                subtype=data[p];p=skip(subtype,skip_string(p+1))
            return p+1
        raise ValueError(f'unsupported NBT tag {kind}')
    if data[0]!=10:raise ValueError('expected NBT compound')
    p=skip_string(1);result={}
    while data[p]:
        kind=data[p];n=u16(p+1);name=data[p+3:p+3+n];p+=3+n
        if name in (b'Status',b'DataVersion',b'xPos',b'zPos'):
            if kind==8:result[name.decode()]=data[p+2:p+2+u16(p)].decode('utf-8')
            elif kind==3:result[name.decode()]=i32(p)
            else:raise ValueError('unexpected metadata type')
        p=skip(kind,p)
        if len(result)==4:return result
        if p>=len(data):raise ValueError('truncated NBT')
    raise ValueError('missing chunk status metadata')

def region_metadata(path,rows):
    data=path.read_bytes()
    result=[]
    for cx,cz,sector,n,t in rows:
        p=sector*4096;size=int.from_bytes(data[p:p+4],'big');compression=data[p+4]
        payload=data[p+5:p+4+size]
        if compression&128:payload=(path.parent/f'c.{cx}.{cz}.mcc').read_bytes()
        kind=compression&127
        if kind==1:payload=gzip.decompress(payload)
        elif kind==2:payload=zlib.decompress(payload)
        elif kind!=3:raise ValueError(f'unsupported compression {kind}')
        m=top_metadata(payload)
        if (m['xPos'],m['zPos'])!=(cx,cz):raise ValueError('chunk position mismatch')
        if m['DataVersion']!=4903:raise ValueError('unverified chunk DataVersion')
        result.append((cx,cz,m['Status'],m['DataVersion']))
    return result
