"""复用 V1 的 Win32 只读共享语义：所有已有源文件拒绝写入和删除，原始目录不落盘。"""
import ctypes
import hashlib
import json

def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def fingerprint(root):
    result={}
    for p in sorted(root.rglob('*')):
        if p.is_file():
            with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
            s=p.stat();result[p.relative_to(root).as_posix()]={'size':s.st_size,'mtime_ns':s.st_mtime_ns,'sha256':h}
    return result

class ReadGuard:
    def __init__(self,root):
        self.root=root;self.handles=[];self.api=ctypes.WinDLL('kernel32',use_last_error=True)
        self.api.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
        self.api.CreateFileW.restype=ctypes.c_void_p;self.api.CloseHandle.argtypes=[ctypes.c_void_p]
    def __enter__(self):
        try:
            for p in sorted(self.root.rglob('*')):
                if p.is_file():
                    h=self.api.CreateFileW(str(p),0x80000000,1,None,3,0,None)
                    if h==ctypes.c_void_p(-1).value:raise OSError(ctypes.get_last_error(),'只读保护失败: '+str(p))
                    self.handles.append(h)
            return self
        except BaseException:
            self.__exit__(None,None,None);raise
    def __exit__(self,*args):
        for h in self.handles:self.api.CloseHandle(h)
        self.handles.clear()
