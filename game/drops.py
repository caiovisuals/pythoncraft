import math
import random
from ursina import *
from game.blocks import get_block
from game.inventory import get_icon_texture
from game.core.physics import collides, move_and_collide
from game.core.state import State, game
from game.core.world import get_light_level, is_solid_at

DROP_SIZE = 0.25            # lado da caixa de colisão do item
GRAVITY = 20                # blocos/s²
MAX_FALL_SPEED = 40
GROUND_FRICTION = 10        # quanto a velocidade horizontal cai por segundo no chão
AIR_DRAG = 1

PICKUP_DELAY = 0.5          # segundos até um item quebrado poder ser coletado
THROW_PICKUP_DELAY = 1.5    # itens jogados pelo jogador demoram mais
PICKUP_REACH = 1.0          # a caixa do jogador aumentada por isso em cada direção coleta itens
DESPAWN_TIME = 300          # itens somem depois de 5 minutos
MAX_DT = 1 / 30

_drops: list = []

class ItemDrop(Entity):
    """
    Item solto no chão: um bloco pequeno girando (ou o ícone do item, sempre virado
    para a câmera) que cai com gravidade e é coletado quando o jogador chega perto.
    `position` é o centro da base da caixa de colisão.
    """

    def __init__(self, item_id: str, count: int, position, velocity=(0, 0, 0), pickup_delay: float = PICKUP_DELAY):
        super().__init__(position=position)
        self.item_id = item_id
        self.count = count
        self.velocity = Vec3(*velocity)
        self.pickup_delay = pickup_delay
        self.age = 0.0
        self.grounded = False

        texture = get_icon_texture(item_id)
        if get_block(item_id):
            self.visual = Entity(parent=self, model="cube", texture=texture, scale=DROP_SIZE)
            self.base_y = DROP_SIZE / 2
        else:
            self.visual = Entity(parent=self, model="quad", texture=texture, scale=0.4, billboard=True, double_sided=True)
            self.base_y = 0.2
        self.visual.y = self.base_y

        _drops.append(self)

    def update(self):
        if not game.is_(State.PLAYING):
            return
        dt = min(time.dt, MAX_DT)
        self.age += dt
        if self.age > DESPAWN_TIME:
            self.remove()
            return

        self._update_physics(dt)
        self._animate()
        if self.age >= self.pickup_delay:
            self._try_pickup()

    def _update_physics(self, dt: float):
        # Se um bloco foi colocado em cima do item, empurra ele para cima
        if collides(self.position, DROP_SIZE, DROP_SIZE, is_solid_at):
            self.y = math.floor(self.y + 0.5) + 0.5
            self.velocity = Vec3(0, 0, 0)
            return

        self.velocity.y = max(self.velocity.y - GRAVITY * dt, -MAX_FALL_SPEED)
        delta = (self.velocity.x * dt, self.velocity.y * dt, self.velocity.z * dt)
        new_pos, hit = move_and_collide(self.position, delta, DROP_SIZE, DROP_SIZE, is_solid_at)
        self.position = Vec3(*new_pos)

        if hit[0]:
            self.velocity.x = 0
        if hit[2]:
            self.velocity.z = 0
        if hit[1]:
            self.grounded = self.velocity.y < 0
            self.velocity.y = 0
        else:
            self.grounded = False

        friction = GROUND_FRICTION if self.grounded else AIR_DRAG
        slow = max(0.0, 1 - friction * dt)
        self.velocity.x *= slow
        self.velocity.z *= slow

    def _animate(self):
        self.visual.y = self.base_y + 0.05 + math.sin(self.age * 2.5) * 0.05
        if not self.visual.billboard:
            self.visual.rotation_y = self.age * 60
        light = get_light_level()
        self.visual.color = color.Color(light, light, light, 1)

    def _try_pickup(self):
        player = game.player
        if player is None or player.vitals.is_dead:
            return
        # Caixa do jogador aumentada em PICKUP_REACH (como no Minecraft)
        reach_xz = player.width / 2 + PICKUP_REACH
        if abs(self.x - player.x) > reach_xz or abs(self.z - player.z) > reach_xz:
            return
        if not (player.y - PICKUP_REACH <= self.y <= player.y + player.height + PICKUP_REACH):
            return

        left = player.hotbar.add_item(self.item_id, self.count)
        if left == 0:
            self.remove()
        else:
            self.count = left

    def remove(self):
        if self in _drops:
            _drops.remove(self)
        destroy(self)

def spawn_drop(item_id: str, count: int, position, velocity=None, pickup_delay: float = PICKUP_DELAY) -> ItemDrop:
    """Cria um item no chão. Sem `velocity`, ele dá um pulinho numa direção aleatória."""
    if velocity is None:
        velocity = (random.uniform(-1.5, 1.5), random.uniform(3, 4.5), random.uniform(-1.5, 1.5))
    return ItemDrop(item_id, count, position, velocity, pickup_delay)

def clear_drops():
    """Remove todos os itens do chão (ao sair da partida)."""
    for drop in list(_drops):
        destroy(drop)
    _drops.clear()