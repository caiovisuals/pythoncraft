import unittest
from game.core.mining import SECONDS_PER_HARDNESS, MiningProgress, break_time

class BreakTimeTest(unittest.TestCase):
    def test_by_hand(self):
        self.assertAlmostEqual(break_time(2), 2 * SECONDS_PER_HARDNESS)

    def test_right_tool_divides_time(self):
        self.assertAlmostEqual(break_time(2, "pickaxe", "pickaxe", 4), 2 * SECONDS_PER_HARDNESS / 4)

    def test_wrong_tool_does_not_help(self):
        self.assertAlmostEqual(break_time(2, "pickaxe", "axe", 4), 2 * SECONDS_PER_HARDNESS)

    def test_zero_hardness_is_instant(self):
        self.assertEqual(break_time(0), 0)

class MiningProgressTest(unittest.TestCase):
    def test_breaks_after_duration(self):
        mining = MiningProgress(cooldown=0)
        self.assertFalse(mining.tick(0.5, (0, 0, 0), 1.0))
        self.assertAlmostEqual(mining.progress, 0.5)
        self.assertTrue(mining.tick(0.5, (0, 0, 0), 1.0))
        self.assertEqual(mining.progress, 0)

    def test_changing_target_restarts(self):
        mining = MiningProgress(cooldown=0)
        mining.tick(0.9, (0, 0, 0), 1.0)
        self.assertFalse(mining.tick(0.2, (1, 0, 0), 1.0))
        self.assertAlmostEqual(mining.progress, 0.2)

    def test_reset_clears_progress(self):
        mining = MiningProgress(cooldown=0)
        mining.tick(0.9, (0, 0, 0), 1.0)
        mining.reset()
        self.assertFalse(mining.tick(0.2, (0, 0, 0), 1.0))

    def test_instant_break_waits_for_cooldown(self):
        mining = MiningProgress(cooldown=0.25)
        self.assertTrue(mining.tick(0.01, (0, 0, 0), 0))
        self.assertFalse(mining.tick(0.1, (0, 1, 0), 0))
        self.assertFalse(mining.tick(0.1, (0, 1, 0), 0))
        self.assertFalse(mining.tick(0.1, (0, 1, 0), 0))  # termina o cooldown
        self.assertTrue(mining.tick(0.01, (0, 1, 0), 0))

if __name__ == "__main__":
    unittest.main()