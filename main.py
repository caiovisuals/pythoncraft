# main.py
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Carregar texturas (coloque as imagens em assets/textures/)
T_GRASS = load_texture('assets/textures/blocks/grass.png')
T_DIRT  = load_texture('assets/textures/blocks/dirt.png')
T_STONE = load_texture('assets/textures/blocks/stone.png')
T_WOOD = load_texture('assets/textures/blocks/wood.png')
T_CROSS = load_texture('assets/textures/gui/crosshair.png')

window.title = 'pythoncraft - bycaiovisuals'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False   # esconde o botão de fechar padrão
window.fps_counter.enabled = True

# Crosshair
cross = Sprite(parent=camera.ui, texture=T_CROSS, pixel_perfect=True, scale=0.02)

# --- Menu inicial ---
menu_panel = Entity(parent=camera.ui, enabled=True)
title = Text('pythoncraft', parent=menu_panel, scale=3, y=0.25, x=0)
subtitle = Text('bycaiovisuals', parent=menu_panel, y=0.1, scale=0.8, color=color.gray, x=0)
def on_play():
    menu_panel.enabled = False
    start_game()
play_btn = Button('Jogar', parent=menu_panel, scale=(0.25, 0.08), y=-0.05, on_click=on_play)
# Botões de sair/config (opcionais)
def on_quit():
    application.quit()
quit_btn = Button('Sair', parent=menu_panel, scale=(0.12,0.06), y=-0.20, x=0.18, color=color.lime, on_click=on_quit)

# --- Painel de configurações (toggle com ESC) ---
settings_panel = WindowPanel(title='Configurações', enabled=False, content=(
    Text('Volume: (mock)', enabled=True),
    Text('Sensibilidade: (mock)', enabled=True),
), scale=(0.6, 0.6))
settings_panel.parent = camera.ui
settings_panel.y = 0

def toggle_settings():
    settings_panel.enabled = not settings_panel.enabled
    # desbloqueia cursor quando painel ativo
    mouse.locked = not settings_panel.enabled
    if settings_panel.enabled:
        # se quiser pausar o jogo, ajuste aqui
        pass

# --- Mundo / blocos ---
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=T_GRASS):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=1
        )
        self.collider = 'box'

# Função para criar um mundo pequeno de teste
world_parent = Entity()

def create_test_world(size=8, height=4):
    # limpa
    for c in world_parent.children[:]:
        destroy(c)
    # camada base de stone/dirt/grass
    for x in range(-size, size):
        for z in range(-size, size):
            # algumas camadas
            for y in range(-1, height):
                if y < 0:
                    tex = T_STONE
                elif y == 0:
                    tex = T_DIRT
                else:
                    tex = T_GRASS
                Voxel(position=(x, y, z), texture=tex).parent = world_parent

# Primeiro jogador/controller
player = None
def start_game():
    global player
    # criar mundo simples
    create_test_world(size=12, height=2)
    # criar controller (FirstPersonController já implementa movimento + mouse)
    player = FirstPersonController()
    player.gravity = 0.5
    mouse.locked = True

# Input global
def input(key):
    global player
    # Menu atalho ESC no menu também fecha app? aqui toggla settings se já estiver em jogo
    if key == 'escape':
        # se menu está ativo (não iniciou o jogo), fazer nada
        if menu_panel.enabled:
            # se quiser fechar menu com ESC: application.quit()
            return
        toggle_settings()
        if player:
            player.enabled = not settings_panel.enabled

    # E: abre/fecha inventário
    if key == 'e':
        if player:  # só funciona se o jogo estiver rodando
            inventory.toggle()
            if inventory.visible:
                player.enabled = False  # pausa player
            else:
                player.enabled = True  

    # Exemplo: tecla R para reabrir menu inicial (debug)
    if key == 'r':
        menu_panel.enabled = True
        settings_panel.enabled = False
        mouse.locked = False
        # cleanup world and player
        for c in world_parent.children[:]:
            destroy(c)
        if player:
            destroy(player)
            player = None

# ============================================================
#                       INVENTÁRIO
# ============================================================

class InventorySlot(Button):
    def __init__(self, index, texture=None, amount=0, **kwargs):
        super().__init__(
            model='quad',
            texture=texture,
            scale=(0.08, 0.08),
            color=color.white,
            **kwargs
        )
        self.index = index
        self.amount = amount
        self.item_texture = texture
        
        self.amount_text = Text(
            text=str(amount) if amount > 1 else '',
            parent=self,
            scale=1,
            y=-0.03
        )

    def set_item(self, texture, amount=1):
        self.item_texture = texture
        self.texture = texture
        self.amount = amount
        self.amount_text.text = str(amount) if amount > 1 else ''

    def clear(self):
        self.item_texture = None
        self.texture = None
        self.amount = 0
        self.amount_text.text = ''

# ---------------- INVENTORY ----------------
class Inventory(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)

        self.bg = Entity(parent=self, model='quad', color=color.rgba(0, 0, 0, 150),
                         scale=(0.95, 0.45), y=-0.3)

        self.slots = []
        cols = 9
        rows = 3
        start_x = -0.40
        start_y = -0.28

        for r in range(rows):
            for c in range(cols):
                index = r * cols + c
                slot = InventorySlot(
                    index=index,
                    parent=self,
                    x=start_x + c * 0.09,
                    y=start_y + r * 0.09
                )
                self.slots.append(slot)

        self.visible = False

    def toggle(self):
        self.visible = not self.visible
        self.enabled = self.visible
        mouse.locked = not self.visible

    def add_item(self, texture, amount=1):
        for slot in self.slots:
            if slot.item_texture == texture:
                slot.set_item(texture, slot.amount + amount)
                return

        for slot in self.slots:
            if slot.item_texture is None:
                slot.set_item(texture, amount)
                return


# ---------------- HOTBAR ----------------
class Hotbar(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        self.bg = Entity(model='quad', parent=self,
                         color=color.rgba(0, 0, 0, 170),
                         y=-0.45, scale=(0.40, 0.08))

        self.slots = []
        start_x = -0.18

        for i in range(9):
            slot = InventorySlot(
                index=i,
                parent=self,
                x=start_x + i * 0.045,
                y=-0.45
            )
            self.slots.append(slot)

        self.selected = 0
        self.update_selection()

    def update_selection(self):
        for i, slot in enumerate(self.slots):
            slot.color = color.azure if i == self.selected else color.white


hotbar = Hotbar()
inventory = Inventory()

# Start app
app.run()
