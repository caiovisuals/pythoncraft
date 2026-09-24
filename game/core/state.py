from enum import Enum
from typing import Callable

class State(Enum):
    MENU = "menu"
    LOADING = "loading"
    PLAYING = "playing"
    PAUSED = "paused"
    DEAD = "dead"

# Transições permitidas a partir de cada estado
TRANSITIONS: dict[State, set[State]] = {
    State.MENU: {State.LOADING},
    State.LOADING: {State.PLAYING, State.MENU},
    State.PLAYING: {State.PAUSED, State.DEAD, State.MENU},
    State.PAUSED: {State.PLAYING, State.MENU},
    State.DEAD: {State.PLAYING, State.MENU},
}

class InvalidTransition(Exception):
    pass

class GameState:
    def __init__(self):
        self.state = State.MENU
        self.player = None
        self.mode = None
        self._on_enter: dict[State, list[Callable]] = {s: [] for s in State}
        self._on_exit: dict[State, list[Callable]] = {s: [] for s in State}

    def is_(self, state: State) -> bool:
        return self.state == state

    def can_change(self, new_state: State) -> bool:
        return new_state in TRANSITIONS[self.state]

    def change(self, new_state: State):
        """Troca de estado, chamando os callbacks de saída e de entrada."""
        if not self.can_change(new_state):
            raise InvalidTransition(f"{self.state.name} -> {new_state.name}")

        previous = self.state
        for callback in self._on_exit[previous]:
            callback(new_state)
        self.state = new_state
        for callback in self._on_enter[new_state]:
            callback(previous)

    def on_enter(self, state: State, callback: Callable):
        """callback(previous_state) é chamado ao entrar em `state`."""
        self._on_enter[state].append(callback)

    def on_exit(self, state: State, callback: Callable):
        """callback(next_state) é chamado ao sair de `state`."""
        self._on_exit[state].append(callback)

game = GameState()