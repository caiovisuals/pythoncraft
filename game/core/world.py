from ursina import *
from game.blocks import get_block
from perlin_noise import PerlinNoise

CHUNK_SIZE = 16
world_parent = Entity()
placed_blocks = {}

noise = PerlinNoise(octaves=4)

class Chunk(Entity):
    def __init__(self, cx, cz, parent):
        super().__init__(parent=parent)
        self.cx = cx
        self.cz = cz
        self.build()

class Voxel(Entity):
    def __init__(self, position=(0,0,0), block=None):
        if block is None:
            raise ValueError("Um bloco válido deve ser fornecido")
        
        texture = block.textures.get("side", None)

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

def get_height(x, z, scale=20, amplitude=6):
    value = noise([x / scale, z / scale])
    normalized = (value + 1) / 2
    return int(normalized * amplitude)

def select_block_for_height(y, height):
    """Retorna o ID do bloco apropriado para cada camada"""
    if y == height:
        return get_block("grass")
    elif y > height - 3:
        return get_block("dirt")
    else:
        return get_block("stone")

def create_world(size=16, max_height=8):
    global placed_blocks

    for c in list(world_parent.children):
        destroy(c)
    placed_blocks.clear()

    for x in range(-size, size):
        for z in range(-size, size):
            height = get_height(x, z)

            for y in range(-2, height + 1):
                block = select_block_for_height(y, height)
                voxel = Voxel(position=(x, y, z), block=block)
                placed_blocks[(x, y, z)] = voxel