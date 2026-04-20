from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from game.inventory import Inventory, Hotbar
import game.textures as textures
from ursina import mouse
import time

def uv_rect(x, y, w, h, tex_w=64, tex_h=64):
    return [
        (x/tex_w, 1 - y/tex_h),
        ((x+w)/tex_w, 1 - y/tex_h),
        ((x+w)/tex_w, 1 - (y+h)/tex_h),
        (x/tex_w, 1 - (y+h)/tex_h),
    ]
class PlayerModel(Entity):
    def __init__(self, texture):
        super().__init__()

class FirstPersonArm(Entity):
    def __init__(self, texture):
        arm_uv = [
            uv_rect(44,20,4,12),
            uv_rect(52,20,4,12),
            uv_rect(40,20,4,12),
            uv_rect(48,20,4,12),
            uv_rect(44,16,4,4),
            uv_rect(48,16,4,4),
        ]

        self.arm.parent = self

        self.arm.scale = (0.3,0.8,0.3)
        self.arm.position = (0.6,-0.6,1)
        self.arm.rotation = (20,0,0)

class PlayerController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 0.5
        self.speed = 5
        self.jump_height = 1.5

        self.mouse_sensitivity = [55, 55]

        self.max_health = 20
        self.health = self.max_health

        self.max_hunger = 20
        self.hunger = self.max_hunger 
        self.hunger_decay_rate = 40
        self.last_hunger_tick = time.time()

        self.inventory = Inventory()
        self.hotbar = Hotbar()
        self.inventory_enabled = False

        self.last_toggle_time = 0
        self.toggle_delay  = 0.2

    def toggle_inventory(self):
        """Abre ou fecha o inventário"""
        self.inventory.toggle()
        self.inventory_enabled = self.inventory.visible

        self.enabled = not self.inventory_enabled
        mouse.locked = not self.inventory_enabled

    def handle_input(self, key):
        """Função para gerenciar inputs do jogador"""
        now = time.time()

        if now - self.last_toggle_time < self.toggle_delay:
            return
        
        if key == "e":
            self.toggle_inventory()
            self.last_toggle_time = now
    
    def take_damage(self, amount):
        """Aplica dano ao jogador"""
        self.health = max(0, self.health - amount)

        if self.health <= 0:
            self.on_death()

    def eat(self, food_value):
        self.hunger = min(self.max_hunger, self.hunger + food_value)

    def update(self):
        super().update()
        if time.time() - self.last_hunger_tick > self.hunger_decay_rate:
            self.hunger = max(0, self.hunger - 1)
            self.last_hunger_tick = time.time()

        if self.hunger == 0:
            self.take_damage(1)

    def heal(self, amount):
        """Cura o jogador"""
        self.health = min(self.max_health, self.health + amount)
    
    def on_death(self):
        """Chamado quando o jogador morre"""
        print("Você morreu!")