import unittest
from game.core.physics import block_overlaps_player

class BlockOverlapsPlayerTest(unittest.TestCase):
    # Jogador em pé sobre o bloco (0, 0, 0): pés em y = 0.5
    PLAYER = (0, 0.5, 0)

    def test_block_at_feet_overlaps(self):
        self.assertTrue(block_overlaps_player((0, 1, 0), self.PLAYER))

    def test_block_at_head_overlaps(self):
        self.assertTrue(block_overlaps_player((0, 2, 0), self.PLAYER))

    def test_block_above_head_is_free(self):
        self.assertFalse(block_overlaps_player((0, 3, 0), self.PLAYER))

    def test_ground_block_is_free(self):
        self.assertFalse(block_overlaps_player((0, 0, 0), self.PLAYER))

    def test_neighbor_block_is_free(self):
        self.assertFalse(block_overlaps_player((1, 1, 0), self.PLAYER))

    def test_player_between_blocks_overlaps_both(self):
        player = (0.5, 0.5, 0)
        self.assertTrue(block_overlaps_player((0, 1, 0), player))
        self.assertTrue(block_overlaps_player((1, 1, 0), player))

if __name__ == "__main__":
    unittest.main()