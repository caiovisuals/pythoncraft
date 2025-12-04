from ursina import load_texture

ITEM_TYPE_TOOL = "tool"
ITEM_TYPE_FOOD = "food"
ITEM_TYPE_BLOCK = "block"

class Item:
    def __init__(self, name: str, texture: str, item_type: str, **attributes):
        self.name = name
        self.texture = load_texture(texture)
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
        texture="assets/textures/items/apple.png",
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("stone_sword", Item(
        name="Espada de Pedra",
        texture="assets/textures/items/stone_sword.png",
        item_type=ITEM_TYPE_TOOL,
        damage=5,
        durability=131
    ))

    register_item("iron_sword", Item(
        name="Espada de Ferro",
        texture="assets/textures/items/iron_sword.png",
        item_type=ITEM_TYPE_TOOL,
        damage=6,
        durability=250
    ))

    register_item("diamond_sword", Item(
        name="Espada de Diamante",
        texture="assets/textures/items/diamond_sword.png",
        item_type=ITEM_TYPE_TOOL,
        damage=7,
        durability=1561
    ))
