import unittest
from game.core.physics import (
    PLAYER_HEIGHT,
    PLAYER_SNEAK_HEIGHT,
    PLAYER_WIDTH,
    block_overlaps_player,
    collides,
    move_and_collide,
)

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

def _world(*blocks):
    solid = set(blocks)
    return lambda pos: pos in solid

def _floor(size=5, y=0):
    return {(x, y, z) for x in range(-size, size + 1) for z in range(-size, size + 1)}

def _move(pos, delta, blocks, height=PLAYER_HEIGHT, **kwargs):
    return move_and_collide(pos, delta, PLAYER_WIDTH, height, _world(*blocks), **kwargs)

class MoveAndCollideTest(unittest.TestCase):
    # Pés sobre o chão (blocos em y = 0 têm o topo em y = 0.5)
    START = (0, 0.5, 0)

    def test_lands_on_ground(self):
        pos, hit = _move((0, 3, 0), (0, -5, 0), _floor())
        self.assertAlmostEqual(pos[1], 0.5, places=3)
        self.assertTrue(hit[1])

    def test_fast_fall_does_not_tunnel_through_block(self):
        pos, hit = _move((0, 20, 0), (0, -30, 0), {(0, 0, 0)})
        self.assertAlmostEqual(pos[1], 0.5, places=3)

    def test_wall_stops_player_at_its_face(self):
        blocks = _floor() | {(2, 1, 0)}
        pos, hit = _move(self.START, (3, 0, 0), blocks)
        self.assertTrue(hit[0])
        self.assertAlmostEqual(pos[0], 1.5 - PLAYER_WIDTH / 2, places=3)
        self.assertFalse(collides(pos, PLAYER_WIDTH, PLAYER_HEIGHT, _world(*blocks)))

    def test_block_at_head_height_blocks_the_player(self):
        # Um bloco "flutuando" na altura da cabeça também é parede
        blocks = _floor() | {(2, 2, 0)}
        pos, hit = _move(self.START, (3, 0, 0), blocks)
        self.assertTrue(hit[0])

    def test_one_block_gap_is_too_low_to_walk_through(self):
        # Buraco de 1 bloco de altura: o jogador (1.8) não passa
        blocks = _floor() | {(2, 2, 0)}
        pos, _ = _move(self.START, (4, 0, 0), blocks)
        self.assertLess(pos[0], 2)

    def test_two_block_gap_is_tall_enough(self):
        blocks = _floor() | {(2, 3, 0)}
        pos, hit = _move(self.START, (3, 0, 0), blocks)
        self.assertFalse(hit[0])
        self.assertAlmostEqual(pos[0], 3)

    def test_ceiling_stops_jump(self):
        blocks = _floor() | {(0, 3, 0)}
        pos, hit = _move(self.START, (0, 2, 0), blocks)
        self.assertTrue(hit[1])
        self.assertAlmostEqual(pos[1] + PLAYER_HEIGHT, 2.5, places=3)

    def test_sneaking_fits_under_1_5_gap(self):
        # Teto a 1.5 acima dos pés: em pé (1.8) não cabe, agachado (1.5) cabe
        ceiling = _world((0, 3, 0))  # face de baixo em y = 2.5
        feet = (0, 1.0, 0)
        self.assertTrue(collides(feet, PLAYER_WIDTH, PLAYER_HEIGHT, ceiling))
        self.assertFalse(collides(feet, PLAYER_WIDTH, PLAYER_SNEAK_HEIGHT, ceiling))

    def test_sneaking_stops_at_edge(self):
        pos, hit = _move(self.START, (3, 0, 0), {(0, 0, 0)}, stop_at_edges=True)
        # O centro pode passar da borda, mas a caixa continua apoiada no bloco
        self.assertLess(pos[0], 0.5 + PLAYER_WIDTH / 2)
        self.assertGreater(pos[0], 0.5)
        self.assertAlmostEqual(pos[1], 0.5)

    def test_without_sneaking_walks_off_edge(self):
        pos, _ = _move(self.START, (3, 0, 0), {(0, 0, 0)})
        self.assertAlmostEqual(pos[0], 3)

    def test_sneaking_walks_freely_on_solid_ground(self):
        pos, _ = _move(self.START, (2, 0, 0), _floor(), stop_at_edges=True)
        self.assertAlmostEqual(pos[0], 2)

if __name__ == "__main__":
    unittest.main()