import unittest
from collections import defaultdict

import game.textures as textures
from game import blocks, items
from game.core.modes import CreativeMode, SurvivalMode
from game.core.vitals import Vitals

class FakeHotbar:
    """Hotbar mínima com a mesma interface usada pelos modos."""

    def __init__(self, stacks=None):
        self.stacks = stacks or []
        self.selected = 0

    @property
    def selected_item(self):
        if self.selected < len(self.stacks):
            return self.stacks[self.selected][0]
        return None

    def set_items(self, items):
        self.stacks = [(item, 1) for item in items]

    def consume_selected(self, amount=1):
        item_id, count = self.stacks[self.selected]
        if count - amount > 0:
            self.stacks[self.selected] = (item_id, count - amount)
        else:
            self.stacks.pop(self.selected)
        return True

class ModesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        textures.blocks = defaultdict(lambda: None)
        textures.items = defaultdict(lambda: None)
        blocks.BLOCKS.clear()
        items.ITEMS.clear()
        blocks.load_all_blocks()
        items.load_all_items()

    def test_creative_starts_with_blocks_and_never_consumes(self):
        mode, hotbar = CreativeMode(), FakeHotbar()
        mode.setup_hotbar(hotbar)
        self.assertEqual(mode.block_to_place(hotbar), "grass")
        mode.on_block_placed(hotbar)
        self.assertEqual(hotbar.stacks[0], ("grass", 1))

    def test_creative_has_no_drops(self):
        self.assertEqual(CreativeMode().block_drops("stone"), [])

    def test_creative_breaks_instantly(self):
        self.assertEqual(CreativeMode().break_time(blocks.get_block("obsidian")), 0)

    def test_creative_ignores_damage_and_hunger(self):
        mode, vitals = CreativeMode(), Vitals()
        mode.apply_damage(vitals, 100)
        mode.tick_vitals(vitals, 10_000)
        self.assertEqual((vitals.health, vitals.hunger), (20, 20))

    def test_survival_starts_empty(self):
        mode, hotbar = SurvivalMode(), FakeHotbar()
        mode.setup_hotbar(hotbar)
        self.assertIsNone(mode.block_to_place(hotbar))

    def test_survival_drops(self):
        mode = SurvivalMode()
        self.assertEqual(mode.block_drops("grass"), [("dirt", 1)])          # grama dropa terra
        self.assertEqual(mode.block_drops("stone"), [("cobblestone", 1)])   # pedra dropa pedregulho
        self.assertEqual(mode.block_drops("oak_log"), [("oak_log", 1)])     # tronco dropa ele mesmo
        self.assertEqual(mode.block_drops("coal_ore"), [("coal", 1)])
        self.assertEqual(mode.block_drops("oak_leaves"), [])                # folhas não dropam nada

    def test_survival_break_time_uses_the_right_tool(self):
        mode = SurvivalMode()
        stone = blocks.get_block("stone")
        by_hand = mode.break_time(stone)
        self.assertGreater(by_hand, 0)
        self.assertAlmostEqual(mode.break_time(stone, items.get_item("stone_pickaxe")), by_hand / 4)
        # Machado não acelera pedra
        self.assertAlmostEqual(mode.break_time(stone, items.get_item("stone_axe")), by_hand)

    def test_survival_placing_consumes(self):
        mode, hotbar = SurvivalMode(), FakeHotbar([("dirt", 2)])
        self.assertEqual(mode.block_to_place(hotbar), "dirt")
        mode.on_block_placed(hotbar)
        mode.on_block_placed(hotbar)
        self.assertIsNone(mode.block_to_place(hotbar))

    def test_items_that_are_not_blocks_cannot_be_placed(self):
        mode, hotbar = SurvivalMode(), FakeHotbar([("apple", 1)])
        self.assertIsNone(mode.block_to_place(hotbar))

    def test_survival_applies_damage_and_hunger(self):
        mode, vitals = SurvivalMode(), Vitals(hunger_decay_interval=1)
        mode.apply_damage(vitals, 3)
        mode.tick_vitals(vitals, 2)
        self.assertEqual((vitals.health, vitals.hunger), (17, 18))

if __name__ == "__main__":
    unittest.main()