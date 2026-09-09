"""闭区间研究范围；自然指标不得解释成人文分区或施工许可。"""
SCHEMA='southern-island-group-profile/1.0'
BASE='bc96aa5'
BOUNDS=(-800,1376,415,2655)
AIR={'minecraft:air','minecraft:cave_air','minecraft:void_air'}
WATER={'minecraft:water','minecraft:kelp','minecraft:kelp_plant','minecraft:seagrass','minecraft:tall_seagrass','minecraft:bubble_column'}
ICE={'minecraft:ice','minecraft:packed_ice','minecraft:blue_ice','minecraft:frosted_ice'}
PLANTS={'minecraft:short_grass','minecraft:tall_grass','minecraft:short_dry_grass','minecraft:tall_dry_grass','minecraft:snow','minecraft:dead_bush','minecraft:sugar_cane','minecraft:bamboo','minecraft:cactus','minecraft:small_dripleaf','minecraft:big_dripleaf','minecraft:big_dripleaf_stem','minecraft:pink_petals','minecraft:leaf_litter','minecraft:lily_pad'}
def vegetation(name):
    return name in AIR or name in PLANTS or any(s in name for s in ('leaves','_log','_wood','fern','flower','vine','moss_carpet','sapling','azalea','mushroom','_roots'))
def artificial(name):
    return any(s in name for s in ('_planks','_stairs','_slab','_bricks','_door','_fence','_glass','concrete','_rail','_torch','_sign','_carpet')) or name in {'minecraft:farmland','minecraft:dirt_path','minecraft:chest','minecraft:crafting_table','minecraft:barrel','minecraft:stone_bricks'}
def plant_category(name):
    if 'leaves' in name:return 'leaf'
    if '_log' in name or '_wood' in name:return 'trunk'
    if name=='minecraft:dead_bush' or 'dry_grass' in name:return 'dry_ground_vegetation'
    if name in AIR:return 'air'
    if vegetation(name):return 'other_vegetation'
    return 'other'

def material_category(name):
    """仅粗分方块材料，未知名称保留OTHER；不能用于判断自然/人工来源。"""
    if name in WATER:return 'WATER'
    if name in ICE or name in ('minecraft:snow','minecraft:snow_block'):return 'ICE_SNOW'
    if vegetation(name):return 'VEGETATION_OR_AIR'
    if name in {'minecraft:grass_block','minecraft:dirt','minecraft:coarse_dirt','minecraft:rooted_dirt','minecraft:podzol','minecraft:mycelium','minecraft:dirt_path','minecraft:mud','minecraft:clay','minecraft:sand','minecraft:red_sand','minecraft:gravel'}:return 'SOIL_SEDIMENT'
    if any(t in name for t in ('stone','granite','diorite','andesite','deepslate','tuff','calcite','basalt','terracotta')):return 'ROCK_LIKE'
    return 'OTHER'
