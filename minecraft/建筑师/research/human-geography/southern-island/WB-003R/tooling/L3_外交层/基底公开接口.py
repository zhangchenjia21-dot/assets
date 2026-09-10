"""只读当前世界或已绑定缓存。失败不刷新基线；输出仅限指定cache与review目录。"""
def run(command,out,cache,world):
    if command in ('init','seal'):
        from L2_流程层.源复用流程 import audit
        return audit(out,cache,world,command=='init')
    if command=='sample':
        from L2_流程层.定点采样流程 import sample
        return sample(out,cache,world)
    if command=='derive':
        from L2_流程层.基底汇总流程 import derive
        return derive(out,cache)
    raise ValueError('unknown command')
