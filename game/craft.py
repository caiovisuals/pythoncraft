from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

Grid = List[List[Optional[str]]]
Shape = Tuple[Tuple[Optional[str], ...], ...]

@dataclass(frozen=True)
class Recipe:
    """
    Receita com formato (`shape`, linhas de IDs ou None) ou sem formato
    (`ingredients`, a ordem não importa). Receitas com formato podem ser
    feitas em qualquer posição da grade e também espelhadas.
    """
    result: str
    count: int = 1
    shape: Optional[Shape] = None
    ingredients: Tuple[str, ...] = field(default=())

    @property
    def shapeless(self) -> bool:
        return self.shape is None

    @property
    def mirrored(self) -> Optional[Shape]:
        return tuple(tuple(reversed(row)) for row in self.shape) if self.shape else None

    @property
    def width(self) -> int:
        return len(self.shape[0]) if self.shape else 0

    @property
    def height(self) -> int:
        return len(self.shape) if self.shape else 0

def shaped(result: str, pattern: List[str], key: Dict[str, str], count: int = 1) -> Recipe:
    """Receita com formato: cada caractere de `pattern` vira um ID de `key` (espaço = vazio)."""
    shape = tuple(tuple(key[ch] if ch != " " else None for ch in row) for row in pattern)
    return Recipe(result=result, count=count, shape=_trim(shape))

def shapeless(result: str, ingredients: List[str], count: int = 1) -> Recipe:
    return Recipe(result=result, count=count, ingredients=tuple(sorted(ingredients)))

def _trim(grid) -> Shape:
    """Recorta a grade para o menor retângulo que contém todos os itens."""
    rows = [r for r, row in enumerate(grid) if any(row)]
    cols = [c for row in grid for c, cell in enumerate(row) if cell]
    if not rows:
        return ()
    return tuple(
        tuple(grid[r][c] for c in range(min(cols), max(cols) + 1))
        for r in range(min(rows), max(rows) + 1)
    )

# Materiais das ferramentas: prefixo do ID -> ID do material
TOOL_MATERIALS = {
    "wooden": "wood",
    "stone": "cobblestone",
    "iron": "iron_ingot",
    "golden": "gold_ingot",
    "diamond": "diamond",
}

TOOL_PATTERNS = {
    "pickaxe": ["MMM", " S ", " S "],
    "axe": ["MM", "MS", " S"],
    "shovel": ["M", "S", "S"],
    "hoe": ["MM", " S", " S"],
    "sword": ["M", "M", "S"],
}

RECIPES: Dict[str, Recipe] = {
    "wood": shapeless("wood", ["oak_log"], count=4),
    "stick": shaped("stick", ["W", "W"], {"W": "wood"}, count=4),
    "crafting_table": shaped("crafting_table", ["WW", "WW"], {"W": "wood"}),
    "bowl": shaped("bowl", ["W W", " W "], {"W": "wood"}, count=4),
    "bread": shaped("bread", ["WWW"], {"W": "wheat"}),
    "sugar": shapeless("sugar", ["sugar_cane"]),
}

# Ferramentas sem textura (e por isso sem item registrado)
_MISSING_TOOLS = {"golden_sword"}

for _prefix, _material in TOOL_MATERIALS.items():
    for _tool, _pattern in TOOL_PATTERNS.items():
        _id = f"{_prefix}_{_tool}"
        if _id in _MISSING_TOOLS:
            continue
        RECIPES[_id] = shaped(_id, _pattern, {"M": _material, "S": "stick"})

def find_recipe(grid: Grid) -> Optional[Recipe]:
    """Receita que corresponde à grade (de qualquer tamanho), ou None."""
    items = sorted(cell for row in grid for cell in row if cell)
    if not items:
        return None
    shape = _trim(grid)
    for recipe in RECIPES.values():
        if recipe.shapeless:
            if tuple(items) == recipe.ingredients:
                return recipe
        elif shape == recipe.shape or shape == recipe.mirrored:
            return recipe
    return None

def check_craft(grid: Grid) -> Optional[Tuple[str, int]]:
    """(ID do resultado, quantidade) da receita que corresponde à grade, ou None."""
    recipe = find_recipe(grid)
    return (recipe.result, recipe.count) if recipe else None