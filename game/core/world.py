from ursina import *
from game.textures import T_GRASS, T_DIRT, T_STONE

world_parent = Entity()
placed_blocks = {}

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=T_GRASS):
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
        return T_GRASS

def create_world(size=8, height=4):
    global placed_blocks

    for c in list(world_parent.children):
        destroy(c)
    placed_blocks.clear()

    for x in range(-size, size):
        for z in range(-size, size):
            for y in range(-1, height):
                
                tex = get_texture_for_height(y)

                Voxel(position=(x, y, z), texture=tex)

def noise(x, z):
    return (math.sin(x * 2.3 + z * 1.7) * 0.5 + 0.5)