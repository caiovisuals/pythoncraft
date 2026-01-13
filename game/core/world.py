from ursina import *
from game.textures import T_GRASS, T_DIRT, T_STONE

world_parent = Entity()

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=T_GRASS):
        super().__init__(
            parent=world_parent,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=1,
            collider='box'
        )

def create_test_world(size=8, height=4):
    for c in world_parent.children[:]:
        destroy(c)

    for x in range(-size, size):
        for z in range(-size, size):
            for y in range(-1, height):
                if y < 0:
                    tex = T_STONE
                elif y == 0:
                    tex = T_DIRT
                else:
                    tex = T_GRASS
                Voxel(position=(x, y, z), texture=tex)
