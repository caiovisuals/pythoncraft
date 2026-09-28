from ursina import *
from game.core.vitals import Vitals
from game.core.physics import (
    FallTracker,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SNEAK_HEIGHT,
    PLAYER_EYE_HEIGHT,
    PLAYER_SNEAK_EYE_HEIGHT,
    collides,
    move_and_collide,
)
from game.core.world import is_liquid_at, is_solid_at
from game.sounds import play_hit

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
        self.fall_tracker = FallTracker()
        self.mode = mode

        self.hotbar = hotbar
        self.inventory_screen = inventory_screen
        self.screen = None

        self.on_death_callback = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def health(self) -> int:
        return self.vitals.health

    @property
    def hunger(self) -> int:
        return self.vitals.hunger

    @property
    def inventory_enabled(self) -> bool:
        """True enquanto alguma tela (inventário, mesa de trabalho...) está aberta."""
        return self.screen is not None

    def open_screen(self, screen):
        """Abre uma tela de contêiner: o jogador para e o mouse fica livre."""
        if self.screen:
            self.close_screen()
        self.screen = screen
        screen.open()
        self.enabled = False
        mouse.locked = False

    def close_screen(self, resume: bool = True):
        """Fecha a tela aberta. Com resume=False o jogador continua parado (ex.: ao morrer)."""
        if not self.screen:
            return
        self.screen.close()
        self.screen = None
        if resume:
            self.enabled = True
            mouse.locked = True

    def toggle_inventory(self):
        """Abre o inventário, ou fecha a tela que estiver aberta"""
        if self.screen:
            self.close_screen()
        else:
            self.open_screen(self.inventory_screen)

    def handle_input(self, key):
        """Função para gerenciar inputs do jogador"""

        if key == "e":
            self.toggle_inventory()

    def take_damage(self, amount: int):
        """Aplica dano ao jogador (ignorado no Criativo)"""
        before = self.vitals.health
        self.mode.apply_damage(self.vitals, amount)
        if self.vitals.health < before:
            play_hit()
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

        damage = self.fall_tracker.update(self.y, self.grounded, self._in_liquid())
        if damage:
            self.take_damage(damage)

    def _in_liquid(self) -> bool:
        """True se os pés ou o corpo estão dentro de um líquido."""
        x, z = round(self.x), round(self.z)
        feet = floor(self.y + 0.5 + 0.01)
        body = floor(self.y + 0.5 + self.height / 2)
        return is_liquid_at((x, feet, z)) or is_liquid_at((x, body, z))

    def _update_camera_height(self, dt: float):
        """Desce/sobe a câmera suavemente ao agachar/levantar."""
        target = PLAYER_SNEAK_EYE_HEIGHT if self.sneaking else PLAYER_EYE_HEIGHT
        self.camera_pivot.y = lerp(self.camera_pivot.y, target, min(1, dt * 15))

    def update(self):
        if self.vitals.is_dead:
            return
        real_dt = time.dt
        dt = min(real_dt, MAX_PHYSICS_DT)

        self._update_look()
        self._update_sneak()
        self._update_movement(dt)
        if self.vitals.is_dead:
            return
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