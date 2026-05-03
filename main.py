from ursina import *
from ursina.shaders import basic_lighting_shader
import time

app = Ursina()

from game.core.player import PlayerController
from game.core.player import Inventory
from game.core.player import Hotbar
from game.core.world import create_world, world_parent, break_block, place_block
from game.graphics.particles import spawn_particles
from game.textures import load_all_textures
from game.items import load_all_items
from game.entities import load_all_entities
from game.blocks import load_all_blocks
from game.hud import HUD
import game.textures as textures
import game.ui as ui

window.title = "pythoncraft - bycaiovisuals"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

load_all_textures()
load_all_items()
load_all_entities()
load_all_blocks()

HOTBAR_BLOCKS = [
    "grass",
    "dirt",
    "stone",
    "cobblestone",
    "wood",
    "glass",
    "obsidian",
    "ice",
    "limestone",
]

cross = Sprite(
    parent=camera.ui, 
    texture=textures.T_CROSS,
    pixel_perfect=True, 
    scale=0.25, 
    color=color.white,
    double_sided=True
)
cross.enabled = False
cross.alpha = 1

inventory = Inventory()
hotbar = Hotbar()
hud = HUD()

inventory.enabled = False
hotbar.enabled = False

player = None
toggle_cooldown = 0

def _try_break_block():
    """Quebra o bloco apontado pelo crosshair (click esquerdo)."""
    hit = raycast(camera.world_position, camera.forward, distance=6, ignore=[player])
    if not hit.hit:
        return
 
    # Posição do bloco atingido = ponto de impacto recuado pela normal
    bx = round(hit.world_point.x - hit.world_normal.x * 0.5)
    by = round(hit.world_point.y - hit.world_normal.y * 0.5)
    bz = round(hit.world_point.z - hit.world_normal.z * 0.5)
 
    if break_block((bx, by, bz)):
        from game.sounds import play_break_block
        play_break_block()
        # Partículas de quebra no ponto de impacto
        spawn_particles(
            position=hit.world_point,
            count=8,
            color=color.brown,
            scale=0.08,
            spread=0.3,
            lifetime=0.5,
            gravity=True,
        )
 
 
def _try_place_block():
    """Coloca o bloco selecionado na hotbar adjacente ao bloco apontado (click direito)."""
    hit = raycast(camera.world_position, camera.forward, distance=6, ignore=[player])
    if not hit.hit:
        return
 
    # Posição adjacente = ponto de impacto avançado pela normal
    bx = round(hit.world_point.x + hit.world_normal.x * 0.5)
    by = round(hit.world_point.y + hit.world_normal.y * 0.5)
    bz = round(hit.world_point.z + hit.world_normal.z * 0.5)
 
    # Não deixa colocar bloco dentro do jogador
    player_pos = Vec3(round(player.x), round(player.y), round(player.z))
    if Vec3(bx, by, bz) == player_pos:
        return
 
    selected_block = HOTBAR_BLOCKS[player.hotbar.selected % len(HOTBAR_BLOCKS)]
 
    if place_block((bx, by, bz), selected_block):
        from game.sounds import play_place_block
        play_place_block()

def _on_player_death():
    cross.enabled = False
    hotbar.enabled = False
    hud.hide()
    ui.show_death_screen()


def _respawn():
    global player
    ui.hide_death_screen()

    children = world_parent.children[:]
    for i in range(0, len(children), 50):
        for c in children[i:i+50]:
            destroy(c)

    if player:
        destroy(player)
        player = None

    start_game()

def start_game():
    global player

    ui.hide_death_screen()
    surface_y = create_world(size=16, max_height=8)
    player = PlayerController()

    player.position = Vec3(0, surface_y + 3, 0)
    player.on_death_callback = _on_player_death

    mouse.locked = True
    ui.menu_panel.enabled = False

    cross.enabled = True
    hotbar.enabled = True
    inventory.enabled = True
    hud.attach_player(player)
    hud.show()

ui.build_main_menu(start_game)
ui.build_death_screen(_respawn)

def input(key):
    global player, toggle_cooldown
    if time.time() - toggle_cooldown < 0.1:
        return
    toggle_cooldown = time.time()
    if key == "escape":
        if ui.menu_panel.enabled:
            return
        ui.toggle_settings_panel()
        if player:
            player.enabled = not ui.settings_panel.enabled

    if key == "r":
        ui.menu_panel.enabled = True
        ui.settings_panel.enabled = False
        mouse.locked = False

        children = world_parent.children[:]
        batch_size = 50
        for i in range(0, len(children), batch_size):
            for c in children[i:i+batch_size]:
                destroy(c)

        if player:
            destroy(player)
            player = None

    if player:
        player.handle_input(key)

        if not player.inventory_enabled:
 
            if key == "left mouse down":
                _try_break_block()
 
            elif key == "right mouse down":
                _try_place_block()
 
            # Scroll da hotbar
            elif key == "scroll up":
                player.hotbar.scroll(1)
 
            elif key == "scroll down":
                player.hotbar.scroll(-1)
 
            # Atalhos numéricos 1-9 para selecionar slot da hotbar
            for n in range(1, 10):
                if key == str(n):
                    player.hotbar.select(n - 1)

app.run()
