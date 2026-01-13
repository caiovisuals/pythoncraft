from game.textures import items as TEXTURE_ITEMS

ITEM_TYPE_TOOL = "tool"
ITEM_TYPE_FOOD = "food"
ITEM_TYPE_BLOCK = "block"

class Item:
    def __init__(self, name: str, texture: str, item_type: str, **attributes):
        self.name = name
        self.texture = texture
        self.type = item_type
        self.attributes = attributes

    def __repr__(self):
        return f"<Item {self.name} ({self.type})>"

ITEMS = {}

def register_item(id: str, item: Item):
    ITEMS[id] = item

def get_item(id: str):
    return ITEMS.get(id, None)

def load_all_items():
    register_item("apple", Item(
        name="Maçã",
        texture=TEXTURE_ITEMS["apple"],
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("stone_sword", Item(
        name="Espada de Pedra",
        texture=TEXTURE_ITEMS["stone_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=5,
        durability=131
    ))

    register_item("iron_sword", Item(
        name="Espada de Ferro",
        texture=TEXTURE_ITEMS["iron_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=6,
        durability=250
    ))

    register_item("diamond_sword", Item(
        name="Espada de Diamante",
        texture=TEXTURE_ITEMS["diamond_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=7,
        durability=1561
    ))

    register_item("stick", Item(
        name="Graveto",
        texture=TEXTURE_ITEMS["stick"],
        item_type=ITEM_TYPE_TOOL,
        damage=2,
    ))