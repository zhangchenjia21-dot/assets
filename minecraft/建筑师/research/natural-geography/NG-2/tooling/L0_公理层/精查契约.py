"""坐标为方块闭区间；地形代理、水方块观测与高层解释不得混为同一事实。"""
SCHEMA='ng-002-refinement/1.0'
BASE_COMMIT='4b9b1f7e600708ff67e1ef2f844a9d3de0ba2242'
TARGETS={
 'SITE-002':{'bounds':[-6080,-2048,-5217,-1057],'reason':'山脊高点两侧各约400格，覆盖鞍部假说的四向高低地形；必要处追加通道逐列读取。'},
 'SITE-005':{'bounds':[-3328,-5888,-2561,-4993],'reason':'V1谷底成员bounds外扩，包含两侧谷壁及纵向上下游形态，不用biome定义谷。'},
 'SITE-015':{'bounds':[-1472,-3968,-193,-2817],'reason':'覆盖平坦低地及四侧水岸和起伏地形；只量化局部连片面积，不冒充整个GEO面积。'},
 'SITE-014':{'bounds':[-5120,-1376,-4385,-545],'reason':'V1台面bounds外扩约250格，包含完整局部台面与周缘高差。'},
 'SITE-017':{'bounds':[1792,-2624,3647,-1089],'reason':'从代表点向西延伸至山麓、向东延伸至更高山体，覆盖纵向山带；不承诺整个GEO闭合。'},
 'SITE-019':{'bounds':[256,-1728,1855,-705],'reason':'V1水体成员bounds外扩256格，用逐列水区间验证狭窄出口及两侧岸线；边界出口触发继续沿连接方向检查。','topology':True},
 'SITE-003':{'bounds':[-800,1376,415,2655],'reason':'覆盖V1岛体成员与周围至少96格水环；逐列陆地分量触边时不得确认闭合岛体。','topology':True},
 'SITE-011':{'bounds':[-832,-4480,191,-3585],'reason':'围绕候选湾点覆盖凹岸和外水域，不依据单cell邻居；完整水柱连接与岸线形状共同判定。','topology':True}
}
AIR={'minecraft:air','minecraft:cave_air','minecraft:void_air'}
WATER={'minecraft:water','minecraft:kelp','minecraft:kelp_plant','minecraft:seagrass','minecraft:tall_seagrass','minecraft:bubble_column'}
ICE={'minecraft:ice','minecraft:packed_ice','minecraft:blue_ice','minecraft:frosted_ice'}
PLANTS={'minecraft:short_grass','minecraft:tall_grass','minecraft:short_dry_grass','minecraft:tall_dry_grass','minecraft:snow','minecraft:dead_bush','minecraft:sugar_cane','minecraft:bamboo','minecraft:cactus','minecraft:small_dripleaf','minecraft:big_dripleaf','minecraft:big_dripleaf_stem','minecraft:pink_petals','minecraft:leaf_litter','minecraft:lily_pad'}

def vegetation(name):
    return name in AIR or name in PLANTS or any(s in name for s in ('leaves','_log','_wood','fern','flower','vine','moss_carpet','sapling','azalea','mushroom','_roots'))

def artificial(name):
    """只标记有直接材料依据的疑点；这不是人类施工来源判定器。"""
    return any(s in name for s in ('_planks','_stairs','_slab','_bricks','_door','_fence','_glass','concrete','_rail','_torch','_sign','_carpet')) or name in {'minecraft:farmland','minecraft:dirt_path','minecraft:chest','minecraft:crafting_table','minecraft:barrel','minecraft:stone_bricks'}
