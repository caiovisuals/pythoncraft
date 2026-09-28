import unittest
from game.craft import RECIPES, check_craft, find_recipe

def grid_with(shape, size=3, row=0, col=0):
    """Coloca `shape` (linhas de IDs) dentro de uma grade vazia, a partir de (row, col)."""
    grid = [[None] * size for _ in range(size)]
    for r, line in enumerate(shape):
        for c, cell in enumerate(line):
            grid[row + r][col + c] = cell
    return grid

class CraftTest(unittest.TestCase):
    def test_empty_grid_has_no_result(self):
        self.assertIsNone(check_craft([[None] * 3 for _ in range(3)]))

    def test_every_shaped_recipe_matches_in_any_position(self):
        for name, recipe in RECIPES.items():
            if recipe.shapeless:
                continue
            for row in range(3 - recipe.height + 1):
                for col in range(3 - recipe.width + 1):
                    with self.subTest(recipe=name, row=row, col=col):
                        grid = grid_with(recipe.shape, row=row, col=col)
                        self.assertEqual(check_craft(grid), (recipe.result, recipe.count))

    def test_mirrored_recipes_match(self):
        for name, recipe in RECIPES.items():
            if recipe.shapeless:
                continue
            with self.subTest(recipe=name):
                self.assertEqual(find_recipe(grid_with(recipe.mirrored)), recipe)

    def test_shapeless_recipes_match_anywhere(self):
        grid = [[None] * 3 for _ in range(3)]
        grid[2][1] = "oak_log"
        self.assertEqual(check_craft(grid), ("wood", 4))

    def test_small_recipes_fit_in_2x2_grid(self):
        self.assertEqual(check_craft([["wood", "wood"], ["wood", "wood"]]), ("crafting_table", 1))
        self.assertEqual(check_craft([[None, "wood"], [None, "wood"]]), ("stick", 4))

    def test_3x3_recipes_do_not_fit_in_2x2_grid(self):
        for recipe in RECIPES.values():
            if recipe.shape and (recipe.width > 2 or recipe.height > 2):
                trimmed = [list(row[:2]) for row in recipe.shape[:2]]
                with self.subTest(recipe=recipe.result):
                    self.assertNotEqual(find_recipe(trimmed), recipe)

    def test_recipes_are_unambiguous(self):
        # Nenhuma receita (nem espelhada) pode ser igual a outra
        seen = {}
        for name, recipe in RECIPES.items():
            keys = {recipe.ingredients} if recipe.shapeless else {recipe.shape, recipe.mirrored}
            for key in keys:
                with self.subTest(recipe=name):
                    self.assertNotIn(key, seen, f"{name} é igual a {seen.get(key)}")
            for key in keys:
                seen[key] = name

    def test_extra_items_break_the_recipe(self):
        grid = grid_with([["wood"], ["wood"]])
        grid[2][2] = "dirt"
        self.assertIsNone(check_craft(grid))

    def test_wrong_material_has_no_result(self):
        self.assertIsNone(check_craft(grid_with([["dirt"], ["dirt"], ["stick"]])))

if __name__ == "__main__":
    unittest.main()