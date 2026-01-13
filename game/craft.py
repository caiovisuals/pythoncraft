from game.textures import items
from typing import List, Optional

RECIPES = {
    "diamond_sword": {
        "pattern": [
            [None, "diamond", None],
            [None, "diamond", None],
            [None, "stick", None],
        ],
        "result": "diamond_sword",
    },
    "iron_sword": {
        "pattern": [
            [None, "iron", None],
            [None, "iron", None],
            [None, "stick", None],
        ],
        "result": "iron_sword",
    },
    "stone_sword": {
        "pattern": [
            [None, "stone", None],
            [None, "stone", None],
            [None, "stick", None],
        ],
        "result": "stone_sword",
    },
}

def check_craft(grid: List[List[Optional[str]]]) -> Optional[str]:
    for recipe_name, recipe in RECIPES.items():
        pattern = recipe["pattern"]
        match = True
        for y in range(3):
            for x in range(3):
                if pattern[y][x] != grid[y][x]:
                    match = False
                    break
            if not match:
                break
        if match:
            return recipe["result"]
    return None