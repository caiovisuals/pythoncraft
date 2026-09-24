import unittest
from game.craft import RECIPES, check_craft

EMPTY = [[None] * 3 for _ in range(3)]

class CraftTest(unittest.TestCase):
    def test_empty_grid_has_no_result(self):
        self.assertIsNone(check_craft(EMPTY))

    def test_every_recipe_matches_its_own_pattern(self):
        for name, recipe in RECIPES.items():
            with self.subTest(recipe=name):
                self.assertEqual(check_craft(recipe["pattern"]), recipe["result"])

    def test_patterns_are_unique(self):
        patterns = [str(recipe["pattern"]) for recipe in RECIPES.values()]
        self.assertEqual(len(patterns), len(set(patterns)))

    def test_wrong_material_has_no_result(self):
        grid = [
            [None, "dirt", None],
            [None, "dirt", None],
            [None, "stick", None],
        ]
        self.assertIsNone(check_craft(grid))

if __name__ == "__main__":
    unittest.main()