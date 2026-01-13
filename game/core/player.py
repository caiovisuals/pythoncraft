from ursina.prefabs.first_person_controller import FirstPersonController

class PlayerController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 0.5
        self.speed = 5
        self.jump_height = 1.5

        self.inventory = Inventory()
        self.hotbar = Hotbar()
        self.inventory_enabled = False

        self.toggle_cooldown = 0

    def toggle_inventory(self):
        """Abre ou fecha o inventário"""
        self.inventory.toggle()
        self.inventory_enabled = self.inventory.visible
        self.enabled = not self.inventory_enabled

    def handle_input(self, key):
        """Função para gerenciar inputs do jogador"""
        if time.time() - self.toggle_cooldown < 0.1:
            return
        self.toggle_cooldown = time.time()

        if key == 'e':
            self.toggle_inventory()
