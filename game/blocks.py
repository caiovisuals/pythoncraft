from game.textures import blocks as BLOCK_TEXTURES

BLOCK_TYPE_SOLID = "solid"
BLOCK_TYPE_DECOR = "decor"
BLOCK_TYPE_INTERACTIVE = "interactive"

class Block:
    def __init__(self, name: str, texture, block_type: str = BLOCK_TYPE_SOLID, **attributes):
        self.name = name
        self.texture = texture
        self.type = block_type
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
        texture=BLOCK_TEXTURES["grass"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=1
    ))

    register_block("dirt", Block(
        name="Terra",
        texture=BLOCK_TEXTURES["dirt"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=1
    ))

    register_block("stone", Block(
        name="Pedra",
        texture=BLOCK_TEXTURES["stone"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=3
    ))

    register_block("wood", Block(
        name="Madeira",
        texture=BLOCK_TEXTURES["wood"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=2
    ))

    register_block("crafting_table", Block(
        name="Mesa de Trabalho",
        texture=BLOCK_TEXTURES["crafting_table_side"],
        block_type=BLOCK_TYPE_INTERACTIVE
    ))