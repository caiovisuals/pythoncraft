from game.textures import items as TEXTURE_ITEMS
from typing import Dict, Optional

ITEM_TYPE_TOOL = "tool"
ITEM_TYPE_FOOD = "food"
ITEM_TYPE_BLOCK = "block"

class Item:
    def __init__(self, name: str, texture: str, item_type: str, **attributes):
        self.name = name
        self.texture = texture
        self.type = item_type
        self.attributes = attributes or {}

    def __repr__(self):
        return f"<Item {self.name} ({self.type})>"

ITEMS: Dict[str, Item] = {}

def register_item(id: str, item: Item):
    if id in ITEMS:
        raise ValueError(f"Item '{id}' já registrado.")
    ITEMS[id] = item

def get_item(id: str) -> Optional[Item]:
    return ITEMS.get(id)

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
        durability=140
    ))

    register_item("iron_sword", Item(
        name="Espada de Ferro",
        texture=TEXTURE_ITEMS["iron_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=6,
        durability=350
    ))

    register_item("diamond_sword", Item(
        name="Espada de Diamante",
        texture=TEXTURE_ITEMS["diamond_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=7,
        durability=1560
    ))

    register_item("stick", Item(
        name="Graveto",
        texture=TEXTURE_ITEMS["stick"],
        item_type=ITEM_TYPE_TOOL,
        damage=2,
    ))