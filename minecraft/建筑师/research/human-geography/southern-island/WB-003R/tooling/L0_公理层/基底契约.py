"""样区只是研究口径，不划定三域政治边界；代价和材料类别不是经济价值。"""
BOUNDS=(-800,1376,2463,3487)
SCHEMA='economic-access-substrate/1.0'
SOIL={'minecraft:grass_block','minecraft:dirt','minecraft:coarse_dirt','minecraft:rooted_dirt','minecraft:podzol','minecraft:mycelium','minecraft:mud'}
SEDIMENT={'minecraft:sand','minecraft:red_sand','minecraft:gravel','minecraft:clay'}
ORE={'coal','iron','copper','gold','redstone','lapis','diamond','emerald'}
def ore_kind(name):
    stem=name.split(':')[-1]
    for kind in sorted(ORE):
        if stem in (kind+'_ore','deepslate_'+kind+'_ore'):return kind
    return None
def domains(a,m):
    return {'W':m['west'].astype(bool),'M':m['east'].astype(bool)&(a['x']<640)&(a['exposed_y']<=120),'E':m['east'].astype(bool)&(a['x']>=640)&(a['exposed_y']>=140)}
