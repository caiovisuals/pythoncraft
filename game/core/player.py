from ursina import *
from game.core.vitals import Vitals
from game.core.physics import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SNEAK_HEIGHT,
    PLAYER_EYE_HEIGHT,
    PLAYER_SNEAK_EYE_HEIGHT,
    collides,
    move_and_collide,
)
from game.core.world import is_solid_at

MAX_PHYSICS_DT = 1 / 30

class PlayerController(Entity):
    """
    Jogador em primeira pessoa com colisão estilo Minecraft: uma caixa de
    0.6 x 1.8 x 0.6 (1.5 de altura agachado) testada direto contra a grade
    de blocos, então ele nunca entra dentro de um bloco.
    """
    def __init__(self, hotbar, inventory_screen, mode, **kwargs):
        super().__init__()

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.camera_pivot = Entity(parent=self, y=PLAYER_EYE_HEIGHT)
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 110
        mouse.locked = True
        self.mouse_sensitivity = Vec2(55, 55)

        self.speed = 5
        self.sneak_speed_multiplier = 0.3
        self.gravity = 32            # blocos/s²
        self.max_fall_speed = 60     # blocos/s
        self.jump_height = 1.25      # blocos (dá para subir em 1 bloco)
        self.velocity_y = 0.0
        self.grounded = False
        self.sneaking = False

        self.vitals = Vitals(max_health=20, max_hunger=20)
        self.mode = mode

        self.hotbar = hotbar
        self.inventory_screen = inventory_screen
        self.inventory_enabled = False

        self.on_death_callback = None

        for key, value in kwargs.items():
            setattr(self, key, value)

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

    def unstuck(self):
        """Sobe o jogador até ele não estar mais dentro de um bloco (ex.: ao nascer)."""
        for _ in range(256):
            if not collides(self.position, self.width, self.height, is_solid_at):
                return
            self.y = floor(self.y + 0.5) + 0.5

    def _update_look(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

    def _update_sneak(self):
        """Agacha enquanto o Shift estiver pressionado; só levanta se houver espaço acima."""
        wants_sneak = bool(held_keys["shift"] or held_keys["left shift"] or held_keys["right shift"])
        if wants_sneak:
            self.sneaking = True
        elif self.sneaking and not collides(self.position, self.width, PLAYER_HEIGHT, is_solid_at):
            self.sneaking = False
        self.height = PLAYER_SNEAK_HEIGHT if self.sneaking else PLAYER_HEIGHT

    def _update_movement(self, dt: float):
        direction = Vec3(
            self.forward * (held_keys["w"] - held_keys["s"])
            + self.right * (held_keys["d"] - held_keys["a"])
        ).normalized()
        speed = self.speed * (self.sneak_speed_multiplier if self.sneaking else 1)

        if self.grounded and held_keys["space"]:
            self.velocity_y = sqrt(2 * self.gravity * self.jump_height)
            self.grounded = False

        self.velocity_y = max(self.velocity_y - self.gravity * dt, -self.max_fall_speed)

        delta = (direction.x * speed * dt, self.velocity_y * dt, direction.z * speed * dt)
        new_pos, hit = move_and_collide(
            self.position, delta, self.width, self.height, is_solid_at,
            stop_at_edges=self.sneaking and self.grounded,
        )
        self.position = Vec3(*new_pos)

        if hit[1]:
            # Bateu no chão (caindo) ou no teto (subindo)
            self.grounded = self.velocity_y < 0
            self.velocity_y = 0.0
        else:
            self.grounded = False

    def _update_camera_height(self, dt: float):
        """Desce/sobe a câmera suavemente ao agachar/levantar."""
        target = PLAYER_SNEAK_EYE_HEIGHT if self.sneaking else PLAYER_EYE_HEIGHT
        self.camera_pivot.y = lerp(self.camera_pivot.y, target, min(1, dt * 15))

    def update(self):
        real_dt = time.dt
        dt = min(real_dt, MAX_PHYSICS_DT)

        self._update_look()
        self._update_sneak()
        self._update_movement(dt)
        self._update_camera_height(dt)

        self.mode.tick_vitals(self.vitals, real_dt)
        if self.vitals.is_dead:
            self.on_death()

    def on_enable(self):
        mouse.locked = True
        # Restaura a câmera caso ela tenha sido movida enquanto o jogador estava desativado
        if hasattr(self, "camera_pivot") and hasattr(self, "_original_camera_transform"):
            camera.parent = self.camera_pivot
            camera.transform = self._original_camera_transform

    def on_disable(self):
        mouse.locked = False
        self._original_camera_transform = camera.transform
        camera.world_parent = scene

    def on_destroy(self):
        self.on_disable()
    
    def on_death(self):
        """Chamado quando o jogador morre"""
        self.enabled = False
        mouse.locked = False
        if self.on_death_callback:
            self.on_death_callback()