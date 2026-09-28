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

def max_stack_for(item_id: str) -> int:
    """Itens com durabilidade (ferramentas) não empilham; o resto empilha até 64."""
    item = ITEMS.get(item_id)
    if item and "durability" in item.attributes:
        return 1
    return 64

# Materiais das ferramentas: prefixo do ID -> (nome, multiplicador de mineração, durabilidade)
TOOL_TIERS = {
    "wooden": ("Madeira", 2, 59),
    "stone": ("Pedra", 4, 131),
    "iron": ("Ferro", 6, 250),
    "golden": ("Ouro", 12, 32),
    "diamond": ("Diamante", 8, 1561),
}

# Tipo de ferramenta -> nome (as espadas são registradas à parte)
TOOL_TYPES = {
    "pickaxe": "Picareta",
    "axe": "Machado",
    "shovel": "Pá",
    "hoe": "Enxada",
}

def _register_tools():
    for prefix, (material, speed, durability) in TOOL_TIERS.items():
        for tool_type, tool_name in TOOL_TYPES.items():
            item_id = f"{prefix}_{tool_type}"
            register_item(item_id, Item(
                name=f"{tool_name} de {material}",
                texture=tex_module.items[item_id],
                item_type=ITEM_TYPE_TOOL,
                tool_type=tool_type,
                mining_speed=speed,
                durability=durability,
            ))

def load_all_items():
    register_item("apple", Item(
        name="Maçã",
        texture=tex_module.items["apple"],
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("banana", Item(
        name="Banana",
        texture=tex_module.items["banana"],
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("carrot", Item(
        name="Cenoura",
        texture=tex_module.items["carrot"],
        item_type=ITEM_TYPE_FOOD,
        hunger=4,
    ))

    register_item("corn", Item(
        name="Milho",
        texture=tex_module.items["corn"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("beef", Item(
        name="Carne Bovina",
        texture=tex_module.items["beef"],
        item_type=ITEM_TYPE_FOOD,
        hunger=7,
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

    register_item("flint", Item(
        name="Sílex",
        texture=tex_module.items["flint"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("bowl", Item(
        name="Tijela",
        texture=tex_module.items["bowl"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("iron_ingot", Item(
        name="Barra de Ferro",
        texture=tex_module.items["iron_ingot"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("gold_ingot", Item(
        name="Barra de Ouro",
        texture=tex_module.items["gold_ingot"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("coal", Item(
        name="Carvão",
        texture=tex_module.items["coal"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("diamond", Item(
        name="Diamante",
        texture=tex_module.items["diamond"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("wooden_sword", Item(
        name="Espada de Madeira",
        texture=tex_module.items["wooden_sword"],
        item_type=ITEM_TYPE_TOOL,
        tool_type="sword",
        damage=4,
        durability=59
    ))

    register_item("stone_sword", Item(
        name="Espada de Pedra",
        texture=tex_module.items["stone_sword"],
        item_type=ITEM_TYPE_TOOL,
        tool_type="sword",
        damage=5,
        durability=140
    ))

    register_item("iron_sword", Item(
        name="Espada de Ferro",
        texture=tex_module.items["iron_sword"],
        item_type=ITEM_TYPE_TOOL,
        tool_type="sword",
        damage=6,
        durability=350
    ))

    register_item("diamond_sword", Item(
        name="Espada de Diamante",
        texture=tex_module.items["diamond_sword"],
        item_type=ITEM_TYPE_TOOL,
        tool_type="sword",
        damage=7,
        durability=1560
    ))

    register_item("stick", Item(
        name="Graveto",
        texture=tex_module.items["stick"],
        item_type=ITEM_TYPE_TOOL,
        damage=2,
    ))

    register_item("arrow", Item(
        name="Flecha",
        texture=tex_module.items["arrow"],
        item_type=ITEM_TYPE_TOOL,
    ))

    register_item("firework_rocket", Item(
        name="Fogos de Artifício",
        texture=tex_module.items["firework_rocket"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("sugar", Item(
        name="Açucar",
        texture=tex_module.items["sugar"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("sugar_cane", Item(
        name="Cana de Açucar",
        texture=tex_module.items["sugar_cane"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    register_item("saddle", Item(
        name="Sela",
        texture=tex_module.items["saddle"],
        item_type=ITEM_TYPE_UTILITY,
    ))

    _register_tools()