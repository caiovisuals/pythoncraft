from game import textures as tex_module

BLOCK_TYPE_SOLID = "solid"
BLOCK_TYPE_INTERACTIVE = "interactive"
BLOCK_TYPE_LIQUID = "liquid"

class Block:
    def __init__(self, name: str, texture=None, textures: dict = None, block_type: str = BLOCK_TYPE_SOLID, hardness: float = 1, transparent: bool = False, **attributes):
        self.name = name
        if textures:
            self.textures = textures
        else:
            self.textures = {
                "top": texture,
                "bottom": texture,
                "side": texture
            }
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
        textures={
            "top": tex_module.blocks["grass_top"],
            "bottom": tex_module.blocks["dirt"],
            "side": tex_module.blocks["grass_side"]
        },
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

    register_block("limestone", Block(
        name="Calcário",
        texture=tex_module.blocks["limestone"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=2.5
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

    register_block("petroleum", Block(
        name="Petróleo",
        texture=tex_module.blocks["petroleum"],
        block_type=BLOCK_TYPE_LIQUID
    ))

    register_block("oak_leaves", Block(
        name="Folhas de Carvalho",
        texture=tex_module.blocks["oak_leaves"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=1
    ))

    register_block("ice", Block(
        name="Gelo",
        texture=tex_module.blocks["ice"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=2
    ))
    
    register_block("deepslate", Block(
        name="Ardósia Profunda",
        texture=tex_module.blocks["deepslate"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=2
    ))

    register_block("obsidian", Block(
        name="Obsidiana",
        texture=tex_module.blocks["obsidian"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=8
    ))

    register_block("glass", Block(
        name="Vidro",
        texture=tex_module.blocks["glass"],
        block_type=BLOCK_TYPE_SOLID,
        hardness=1.5
    ))

    register_block("crafting_table", Block(
        name="Mesa de Trabalho",
        textures={
            "top": tex_module.blocks["crafting_table_top"],
            "bottom": tex_module.blocks["crafting_table_bottom"],
            "side": tex_module.blocks["crafting_table_side"]
        },
        block_type=BLOCK_TYPE_INTERACTIVE,
        hardness=2
    ))