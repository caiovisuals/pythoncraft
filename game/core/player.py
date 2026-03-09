from ursina.prefabs.first_person_controller import FirstPersonController
from game.inventory import Inventory, Hotbar
from ursina import mouse
import time

class PlayerController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 0.5
        self.speed = 5
        self.jump_height = 1.5

        self.max_health = 20
        self.health = self.max_health

        self.inventory = Inventory()
        self.hotbar = Hotbar()
        self.inventory_enabled = False

        self.last_toggle_time = 0
        self.toggle_delay  = 0

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
        
        if key == 'e':
            self.toggle_inventory()
            self.last_toggle_time = now
    
    def take_damage(self, amount):
        """Aplica dano ao jogador"""
        self.health = max(0, self.health - amount)

        if self.health <= 0:
            self.on_death()
    
    def heal(self, amount):
        """Cura o jogador"""
        self.health = min(self.max_health, self.health + amount)
    
    def on_death(self):
        """Chamado quando o jogador morre"""
        print("Você morreu!")
        # Aqui você pode adicionar lógica de respawn
