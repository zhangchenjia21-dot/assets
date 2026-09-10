"""持Win32只读共享句柄保护已有文件；完整前后inventory另行检测新增文件。"""
import ctypes,hashlib,json
from pathlib import Path

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def fingerprint(root):
    return {p.relative_to(root).as_posix():{'sha256':digest(p),'size':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in sorted(root.rglob('*')) if p.is_file()}

class ReadGuard:
    def __init__(self,root):
        self.root=Path(root);self.handles=[];self.api=ctypes.WinDLL('kernel32',use_last_error=True)
        self.api.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
        self.api.CreateFileW.restype=ctypes.c_void_p;self.api.CloseHandle.argtypes=[ctypes.c_void_p]
    def __enter__(self):
        try:
            for p in sorted(self.root.rglob('*')):
                if not p.is_file():continue
                h=self.api.CreateFileW(str(p),0x80000000,1,None,3,0,None)
                if h==ctypes.c_void_p(-1).value:raise OSError(ctypes.get_last_error(),'不能取得只读锁: '+str(p))
                self.handles.append(h)
            return self
        except BaseException:
            self.__exit__();raise
    def __exit__(self,*args):
        for h in self.handles:self.api.CloseHandle(h)
        self.handles.clear()
