import unittest
from game.core.vitals import Vitals

class VitalsTest(unittest.TestCase):
    def test_hunger_decays_over_time(self):
        vitals = Vitals(max_hunger=20, hunger_decay_interval=10)
        vitals.tick(9.9)
        self.assertEqual(vitals.hunger, 20)
        vitals.tick(0.2)
        self.assertEqual(vitals.hunger, 19)
        vitals.tick(25)
        self.assertEqual(vitals.hunger, 17)

    def test_starvation_damage_is_periodic_not_per_frame(self):
        vitals = Vitals(max_health=20, starvation_interval=4, starvation_damage=1)
        vitals.hunger = 0
        # 60 frames em 1 segundo não devem causar dano
        for _ in range(60):
            vitals.tick(1 / 60)
        self.assertEqual(vitals.health, 20)
        vitals.tick(3.1)
        self.assertEqual(vitals.health, 19)

    def test_starvation_can_kill(self):
        vitals = Vitals(max_health=2, starvation_interval=1)
        vitals.hunger = 0
        vitals.tick(5)
        self.assertEqual(vitals.health, 0)
        self.assertTrue(vitals.is_dead)

    def test_eating_stops_starvation(self):
        vitals = Vitals(max_health=20, starvation_interval=4)
        vitals.hunger = 0
        vitals.tick(3)
        vitals.eat(4)
        vitals.tick(3)
        self.assertEqual(vitals.health, 20)
        self.assertEqual(vitals.hunger, 4)

    def test_heal_and_eat_are_capped(self):
        vitals = Vitals(max_health=20, max_hunger=20)
        vitals.damage(5)
        vitals.heal(100)
        vitals.eat(100)
        self.assertEqual(vitals.health, 20)
        self.assertEqual(vitals.hunger, 20)

    def test_damage_does_not_go_below_zero(self):
        vitals = Vitals(max_health=20)
        vitals.damage(50)
        self.assertEqual(vitals.health, 0)

if __name__ == "__main__":
    unittest.main()