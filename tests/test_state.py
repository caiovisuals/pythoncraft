import unittest
from game.core.state import GameState, InvalidTransition, State

class GameStateTest(unittest.TestCase):
    def test_starts_in_menu(self):
        self.assertTrue(GameState().is_(State.MENU))

    def test_full_game_flow(self):
        game = GameState()
        for state in (State.LOADING, State.PLAYING, State.PAUSED, State.PLAYING,
                      State.DEAD, State.PLAYING, State.MENU):
            game.change(state)
            self.assertTrue(game.is_(state))

    def test_invalid_transition_raises(self):
        game = GameState()
        with self.assertRaises(InvalidTransition):
            game.change(State.PLAYING)  # precisa passar por LOADING
        game.change(State.LOADING)
        game.change(State.PLAYING)
        game.change(State.DEAD)
        with self.assertRaises(InvalidTransition):
            game.change(State.PAUSED)  # não dá para pausar morto
        with self.assertRaises(InvalidTransition):
            game.change(State.DEAD)

    def test_callbacks_receive_previous_and_next_state(self):
        game = GameState()
        calls = []
        game.on_exit(State.MENU, lambda nxt: calls.append(("exit menu", nxt)))
        game.on_enter(State.LOADING, lambda prev: calls.append(("enter loading", prev)))
        game.change(State.LOADING)
        self.assertEqual(calls, [("exit menu", State.LOADING), ("enter loading", State.MENU)])

    def test_state_changes_before_enter_callbacks(self):
        game = GameState()
        seen = []
        game.on_enter(State.LOADING, lambda prev: seen.append(game.state))
        game.change(State.LOADING)
        self.assertEqual(seen, [State.LOADING])

if __name__ == "__main__":
    unittest.main()