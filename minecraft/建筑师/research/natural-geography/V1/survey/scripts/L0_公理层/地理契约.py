"""V1 采样值只代表实际采样柱；64 格单元覆盖不等于逐格实测。"""
SCHEMA = 'natural-geography-survey/1.0'
ALGORITHM = 'coarse64-v1.1-full-boundary'
STEP = 64
AIR = {'minecraft:air', 'minecraft:cave_air', 'minecraft:void_air'}
WATER = {'minecraft:water', 'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:bubble_column'}

def packed(values, index, bits):
    """4903 的紧凑数组在每个 long 内填充，值不得跨越 long 边界。"""
    per = 64 // bits
    return (int(values[index // per]) & ((1 << 64) - 1)) >> ((index % per) * bits) & ((1 << bits) - 1)

def palette_value(container, index, minimum):
    palette = container['palette']
    if len(palette) == 1:
        return palette[0]
    return palette[packed(container['data'], index, max(minimum, (len(palette) - 1).bit_length()))]

def neighbors(p):
    x, z = p
    return ((x-1,z),(x+1,z),(x,z-1),(x,z+1))
