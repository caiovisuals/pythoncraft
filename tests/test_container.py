import unittest
from game.core.container import (
    LEFT, RIGHT, Container, CraftingGrid, ItemStack, PlayerInventory, click, quick_move,
)

def limit(item_id):
    return 1 if item_id.endswith("pickaxe") else 64

class ContainerAddTest(unittest.TestCase):
    def test_add_merges_then_fills_empty_slots(self):
        box = Container(3)
        box.set(1, ItemStack("dirt", 60))
        self.assertEqual(box.add("dirt", 10), 0)
        self.assertEqual(box.slots, [ItemStack("dirt", 6), ItemStack("dirt", 64), None])

    def test_add_returns_leftover_when_full(self):
        box = Container(1)
        self.assertEqual(box.add("dirt", 70), 6)

    def test_unstackable_items(self):
        box = Container(3, limit)
        self.assertEqual(box.add("iron_pickaxe", 2), 0)
        self.assertEqual(box.count("iron_pickaxe"), 2)
        self.assertEqual(box.slots[2], None)

    def test_version_changes_on_every_edit(self):
        box = Container(2)
        v = box.version
        box.add("dirt")
        self.assertGreater(box.version, v)

    def test_player_inventory_fills_hotbar_first(self):
        inv = PlayerInventory()
        inv.add("dirt", 64 * 10)
        self.assertTrue(all(inv.get(i) for i in inv.HOTBAR))
        self.assertEqual(inv.get(9), ItemStack("dirt", 64))
        self.assertIsNone(inv.get(10))

    def test_armor_slots_accept_nothing_yet(self):
        inv = PlayerInventory()
        self.assertIsNotNone(click(inv.armor, 0, ItemStack("dirt", 1)))
        self.assertIsNone(inv.armor.get(0))

class ClickTest(unittest.TestCase):
    def test_left_click_picks_up_and_places(self):
        box = Container(2)
        box.set(0, ItemStack("dirt", 5))
        cursor = click(box, 0, None, LEFT)
        self.assertEqual((cursor, box.get(0)), (ItemStack("dirt", 5), None))
        cursor = click(box, 1, cursor, LEFT)
        self.assertEqual((cursor, box.get(1)), (None, ItemStack("dirt", 5)))

    def test_left_click_merges_until_full(self):
        box = Container(1)
        box.set(0, ItemStack("dirt", 60))
        cursor = click(box, 0, ItemStack("dirt", 10), LEFT)
        self.assertEqual((cursor, box.get(0)), (ItemStack("dirt", 6), ItemStack("dirt", 64)))

    def test_left_click_swaps_different_items(self):
        box = Container(1)
        box.set(0, ItemStack("dirt", 3))
        cursor = click(box, 0, ItemStack("stone", 7), LEFT)
        self.assertEqual((cursor, box.get(0)), (ItemStack("dirt", 3), ItemStack("stone", 7)))

    def test_right_click_takes_half_rounded_up(self):
        box = Container(1)
        box.set(0, ItemStack("dirt", 5))
        cursor = click(box, 0, None, RIGHT)
        self.assertEqual((cursor, box.get(0)), (ItemStack("dirt", 3), ItemStack("dirt", 2)))

    def test_right_click_places_one(self):
        box = Container(2)
        box.set(1, ItemStack("dirt", 1))
        cursor = click(box, 0, ItemStack("dirt", 3), RIGHT)
        cursor = click(box, 1, cursor, RIGHT)
        self.assertEqual(cursor, ItemStack("dirt", 1))
        self.assertEqual(box.slots, [ItemStack("dirt", 1), ItemStack("dirt", 2)])

    def test_right_click_on_single_item_takes_it(self):
        box = Container(1)
        box.set(0, ItemStack("dirt", 1))
        self.assertEqual(click(box, 0, None, RIGHT), ItemStack("dirt", 1))
        self.assertIsNone(box.get(0))

    def test_cannot_place_more_than_stack_limit(self):
        box = Container(1, limit)
        box.set(0, ItemStack("iron_pickaxe", 1))
        cursor = click(box, 0, ItemStack("iron_pickaxe", 1), LEFT)
        self.assertEqual(cursor, ItemStack("iron_pickaxe", 1))

class QuickMoveTest(unittest.TestCase):
    def test_hotbar_to_main_inside_player_inventory(self):
        inv = PlayerInventory()
        inv.set(0, ItemStack("dirt", 10))
        self.assertTrue(quick_move(inv, 0, inv, inv.MAIN))
        self.assertIsNone(inv.get(0))
        self.assertEqual(inv.get(9), ItemStack("dirt", 10))

    def test_leftover_stays_in_source(self):
        source, target = Container(1), Container(1)
        source.set(0, ItemStack("dirt", 10))
        target.set(0, ItemStack("dirt", 60))
        quick_move(source, 0, target)
        self.assertEqual((source.get(0), target.get(0)), (ItemStack("dirt", 6), ItemStack("dirt", 64)))

class CraftingGridTest(unittest.TestCase):
    def _planks_grid(self, logs):
        grid = CraftingGrid(2)
        grid.set(3, ItemStack("oak_log", logs))
        return grid

    def test_result_uses_recipe_count(self):
        self.assertEqual(self._planks_grid(1).result(), ItemStack("wood", 4))

    def test_take_result_consumes_one_of_each_ingredient(self):
        grid = self._planks_grid(2)
        cursor = grid.take_result(None)
        self.assertEqual(cursor, ItemStack("wood", 4))
        self.assertEqual(grid.get(3), ItemStack("oak_log", 1))
        cursor = grid.take_result(cursor)
        self.assertEqual(cursor, ItemStack("wood", 8))
        self.assertIsNone(grid.result())

    def test_take_result_needs_compatible_cursor(self):
        grid = self._planks_grid(1)
        self.assertEqual(grid.take_result(ItemStack("dirt", 1)), ItemStack("dirt", 1))
        self.assertEqual(grid.get(3), ItemStack("oak_log", 1))

    def test_craft_all_moves_everything_it_can(self):
        grid = self._planks_grid(5)
        inv = PlayerInventory()
        self.assertEqual(grid.craft_all(inv), 5)
        self.assertEqual(inv.count("wood"), 20)
        self.assertIsNone(grid.get(3))

    def test_craft_all_stops_when_target_is_full(self):
        grid = self._planks_grid(5)
        target = Container(1)
        target.set(0, ItemStack("wood", 58))
        self.assertEqual(grid.craft_all(target), 1)
        self.assertEqual(grid.get(3), ItemStack("oak_log", 4))

    def test_3x3_grid_crafts_tools(self):
        grid = CraftingGrid(3, limit)
        for i in (0, 1, 2):
            grid.set(i, ItemStack("wood", 1))
        grid.set(4, ItemStack("stick", 1))
        grid.set(7, ItemStack("stick", 1))
        self.assertEqual(grid.result(), ItemStack("wooden_pickaxe", 1))

if __name__ == "__main__":
    unittest.main()