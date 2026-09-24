import unittest
from collections import defaultdict
from pathlib import Path

import game.textures as textures
from game import blocks, items
from game.craft import RECIPES

ROOT = Path(__file__).resolve().parents[1]

def _fake_texture_dict():
    # Os registros só guardam a referência da textura; não é preciso carregá-las de verdade
    return defaultdict(lambda: None)

class RegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        textures.blocks = _fake_texture_dict()
        textures.items = _fake_texture_dict()
        blocks.BLOCKS.clear()
        items.ITEMS.clear()
        blocks.load_all_blocks()
        items.load_all_items()

    def test_recipes_use_registered_ids(self):
        known = set(blocks.BLOCKS) | set(items.ITEMS)
        for name, recipe in RECIPES.items():
            with self.subTest(recipe=name):
                self.assertIn(recipe["result"], known)
                for row in recipe["pattern"]:
                    for cell in row:
                        if cell is not None:
                            self.assertIn(cell, known)

class TextureFilesTest(unittest.TestCase):
    """Garante que todo nome de textura usado nos registros existe em assets/."""

    def _used_names(self, module, loader):
        used = set()

        class Recorder(dict):
            def __missing__(self, key):
                used.add(key)
                return None

        setattr(textures, module, Recorder())
        blocks.BLOCKS.clear()
        items.ITEMS.clear()
        loader()
        return used

    def test_block_textures_exist(self):
        folder = ROOT / "assets/textures/blocks"
        for name in self._used_names("blocks", blocks.load_all_blocks):
            real = textures.BLOCK_ALIASES.get(name, name)
            with self.subTest(texture=name):
                self.assertTrue((folder / f"{real}.png").is_file())

    def test_item_textures_exist(self):
        folder = ROOT / "assets/textures/items"
        for name in self._used_names("items", items.load_all_items):
            with self.subTest(texture=name):
                self.assertTrue((folder / f"{name}.png").is_file())

if __name__ == "__main__":
    unittest.main()