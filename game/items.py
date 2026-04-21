from game import textures as tex_module
from typing import Dict, Optional

ITEM_TYPE_TOOL = "tool"
ITEM_TYPE_FOOD = "food"
ITEM_TYPE_BLOCK = "block"
ITEM_TYPE_UTILITY = "utility"

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
        texture=tex_module.items["apple"],
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("carrot", Item(
        name="Cenoura",
        texture=tex_module.items["carrot"],
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("porkchop", Item(
        name="Costeleta de Porco",
        texture=tex_module.items["porkchop"],
        item_type=ITEM_TYPE_FOOD,
        hunger=7,
    ))

    register_item("bread", Item(
        name="Pão",
        texture=tex_module.items["bread"],
        item_type=ITEM_TYPE_FOOD,
        hunger=5,
    ))

    register_item("book", Item(
        name="Livro",
        texture=tex_module.items["book"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("wheat_seeds", Item(
        name="Sementes de Trigo",
        texture=tex_module.items["wheat_seeds"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("wheat", Item(
        name="Trigo",
        texture=tex_module.items["wheat"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("stone_sword", Item(
        name="Espada de Pedra",
        texture=tex_module.items["stone_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=5,
        durability=140
    ))

    register_item("iron_sword", Item(
        name="Espada de Ferro",
        texture=tex_module.items["iron_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=6,
        durability=350
    ))

    register_item("diamond_sword", Item(
        name="Espada de Diamante",
        texture=tex_module.items["diamond_sword"],
        item_type=ITEM_TYPE_TOOL,
        damage=7,
        durability=1560
    ))

    register_item("stick", Item(
        name="Graveto",
        texture=tex_module.items["stick"],
        item_type=ITEM_TYPE_TOOL,
        damage=2,
    ))