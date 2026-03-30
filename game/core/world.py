from ursina import *
from game.textures import T_GRASS_SIDE, T_DIRT, T_STONE
from perlin_noise import PerlinNoise

world_parent = Entity()
placed_blocks = {}

noise = PerlinNoise(octaves=4)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=T_GRASS_SIDE):
        super().__init__(
            parent=world_parent,
            position=position,
            model="cube",
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=1,
            collider="box"
        )

def get_texture_for_height(y):
    if y < 0:
        return T_STONE
    elif y == 0:
        return T_DIRT
    else:
        return T_GRASS_SIDE

def get_height(x, z, scale=20, amplitude=6):
    value = noise([x / scale, z / scale])
    normalized = (value + 1) / 2
    return int(normalized * amplitude)

def create_world(size=16, max_height=8):
    global placed_blocks

    for c in list(world_parent.children):
        destroy(c)
    placed_blocks.clear()

    for x in range(-size, size):
        for z in range(-size, size):

            height = get_height(x, z)

            for y in range(-2, height + 1):

                # Escolher textura baseada na altura
                if y == height:
                    tex = T_GRASS_SIDE
                elif y > height - 3:
                    tex = T_DIRT
                else:
                    tex = T_STONE

                Voxel(position=(x, y, z), texture=tex)