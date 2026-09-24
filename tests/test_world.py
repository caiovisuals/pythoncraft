import unittest
from game.core.world import CHUNK_SIZE, WORLD_BOTTOM, chunks_to_rebuild, is_exposed

def _solid_cube(size: int) -> dict:
    """Cubo maciço de blocos de pedra começando na camada mais baixa."""
    return {
        (x, y, z): "stone"
        for x in range(size)
        for y in range(WORLD_BOTTOM, WORLD_BOTTOM + size)
        for z in range(size)
    }

class IsExposedTest(unittest.TestCase):
    def test_buried_block_is_not_exposed(self):
        blocks = _solid_cube(3)
        self.assertFalse(is_exposed((1, WORLD_BOTTOM + 1, 1), blocks))

    def test_surface_block_is_exposed(self):
        blocks = _solid_cube(3)
        self.assertTrue(is_exposed((1, WORLD_BOTTOM + 2, 1), blocks))

    def test_world_floor_does_not_count_as_exposed(self):
        blocks = _solid_cube(3)
        self.assertFalse(is_exposed((1, WORLD_BOTTOM, 1), blocks))

    def test_digging_exposes_blocks_deep_underground(self):
        blocks = _solid_cube(5)
        deep = (2, WORLD_BOTTOM + 1, 2)
        self.assertFalse(is_exposed(deep, blocks))
        del blocks[(2, WORLD_BOTTOM + 2, 2)]
        self.assertTrue(is_exposed(deep, blocks))

class ChunksToRebuildTest(unittest.TestCase):
    def test_middle_of_chunk_rebuilds_only_its_chunk(self):
        self.assertEqual(chunks_to_rebuild((5, 0, 5)), {(0, 0)})

    def test_border_rebuilds_neighbor(self):
        self.assertEqual(chunks_to_rebuild((0, 0, 5)), {(0, 0), (-1, 0)})
        self.assertEqual(chunks_to_rebuild((CHUNK_SIZE - 1, 0, 5)), {(0, 0), (1, 0)})

    def test_corner_rebuilds_both_neighbors(self):
        self.assertEqual(chunks_to_rebuild((0, 0, 0)), {(0, 0), (-1, 0), (0, -1)})

    def test_negative_coordinates(self):
        self.assertEqual(chunks_to_rebuild((-1, 3, -5)), {(-1, -1), (0, -1)})

if __name__ == "__main__":
    unittest.main()