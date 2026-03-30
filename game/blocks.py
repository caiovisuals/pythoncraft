from game import textures as tex_module

BLOCK_TYPE_SOLID = "solid"
BLOCK_TYPE_INTERACTIVE = "interactive"
BLOCK_TYPE_LIQUID = "liquid"

class Block:
    def __init__(self, name: str, texture, block_type: str = BLOCK_TYPE_SOLID, hardness: float = 1, transparent: bool = False, **attributes):
        self.name = name
        self.texture = texture
        self.type = block_type
        self.hardness = hardness
        self.transparent = transparent
        self.attributes = attributes

    def __repr__(self):
        return f"<Block {self.name} ({self.type})>"

BLOCKS = {}

def register_block(id: str, block: Block):
    BLOCKS[id] = block

def get_block(id: str):
    return BLOCKS.get(id)

def load_all_blocks():
    register_block("grass", Block(
        name="Grama",
        texture=tex_module.blocks["grass_side"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=1
    ))

    register_block("dirt", Block(
        name="Terra",
        texture=tex_module.blocks["dirt"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=1
    ))

    register_block("stone", Block(
        name="Pedra",
        texture=tex_module.blocks["stone"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=3
    ))

    register_block("cobblestone", Block(
        name="Pedregulho",
        texture=tex_module.blocks["cobblestone"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=3
    ))

    register_block("wood", Block(
        name="Madeira",
        texture=tex_module.blocks["wood"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=2
    ))

    register_block("water", Block(
        name="Àgua",
        texture=tex_module.blocks["water"],
        block_type=BLOCK_TYPE_LIQUID,
        transparent=True
    ))

    register_block("lava", Block(
        name="Lava",
        texture=tex_module.blocks["lava"],
        block_type=BLOCK_TYPE_LIQUID
    ))

    register_block("crafting_table", Block(
        name="Mesa de Trabalho",
        texture=tex_module.blocks["crafting_table_side"],
        block_type=BLOCK_TYPE_INTERACTIVE,
        hardness=2
    ))