class Vitals:
    """
    Vida e fome do jogador, sem dependência da Ursina (testável).
    O tempo avança via tick(dt), chamado a cada frame.
    """

    def __init__(
        self,
        max_health: int = 20,
        max_hunger: int = 20,
        hunger_decay_interval: float = 40.0,
        starvation_interval: float = 4.0,
        starvation_damage: int = 1,
    ):
        self.max_health = max_health
        self.health = max_health
        self.max_hunger = max_hunger
        self.hunger = max_hunger

        self.hunger_decay_interval = hunger_decay_interval  # segundos para perder 1 de fome
        self.starvation_interval = starvation_interval      # segundos entre danos por fome zerada
        self.starvation_damage = starvation_damage

        self._hunger_timer = 0.0
        self._starvation_timer = 0.0

    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    def tick(self, dt: float):
        """Avança o tempo: consome fome e aplica dano quando ela chega a zero."""
        if self.is_dead:
            return

        self._hunger_timer += dt
        while self._hunger_timer >= self.hunger_decay_interval:
            self._hunger_timer -= self.hunger_decay_interval
            self.hunger = max(0, self.hunger - 1)

        if self.hunger > 0:
            self._starvation_timer = 0.0
            return

        self._starvation_timer += dt
        while self._starvation_timer >= self.starvation_interval and not self.is_dead:
            self._starvation_timer -= self.starvation_interval
            self.damage(self.starvation_damage)

    def damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)

    def eat(self, food_value: int):
        self.hunger = min(self.max_hunger, self.hunger + food_value)