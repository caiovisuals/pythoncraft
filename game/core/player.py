from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from game.core.vitals import Vitals

class PlayerController(FirstPersonController):
    def __init__(self, hotbar, inventory_screen, mode, **kwargs):
        super().__init__(**kwargs)
        self.cursor.visible = False
        self.gravity = 0.5
        self.speed = 5
        self.jump_height = 1.5
        self.mouse_sensitivity = Vec2(55, 55)

        self.vitals = Vitals(max_health=20, max_hunger=20)
        self.mode = mode

        self.hotbar = hotbar
        self.inventory_screen = inventory_screen
        self.inventory_enabled = False

        self.on_death_callback = None

    @property
    def health(self) -> int:
        return self.vitals.health

    @property
    def hunger(self) -> int:
        return self.vitals.hunger

    def toggle_inventory(self):
        """Abre ou fecha o inventário"""
        self.inventory_enabled = not self.inventory_enabled
        if self.inventory_enabled:
            self.inventory_screen.sync_hotbar(self.hotbar.stacks)
        self.inventory_screen.enabled = self.inventory_enabled

        self.enabled = not self.inventory_enabled
        mouse.locked = not self.inventory_enabled

    def handle_input(self, key):
        """Função para gerenciar inputs do jogador"""

        if key == "e":
            self.toggle_inventory()

    def take_damage(self, amount: int):
        """Aplica dano ao jogador (ignorado no Criativo)"""
        self.mode.apply_damage(self.vitals, amount)
        if self.vitals.is_dead:
            self.on_death()

    def heal(self, amount: int):
        """Cura o jogador"""
        self.vitals.heal(amount)

    def eat(self, food_value: int):
        self.vitals.eat(food_value)

    def update(self):
        real_dt = time.dt
        time.dt = min(real_dt, MAX_PHYSICS_DT)
        try:
            super().update()
        finally:
            time.dt = real_dt

        self.mode.tick_vitals(self.vitals, real_dt)
        if self.vitals.is_dead:
            self.on_death()
    
    def on_death(self):
        """Chamado quando o jogador morre"""
        self.enabled = False
        mouse.locked = False
        if self.on_death_callback:
            self.on_death_callback()