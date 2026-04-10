from ursina import *
from ursina.shaders import basic_lighting_shader
import time

app = Ursina()

from game.core.player import PlayerController
from game.core.world import create_world, world_parent
from game.graphics.particles import spawn_particles
from game.textures import load_all_textures
from game.items import load_all_items
from game.entities import load_all_entities
from game.blocks import load_all_blocks
from game.textures import T_CROSS
import game.ui as ui
from game.inventory import Inventory, Hotbar

window.title = "pythoncraft - bycaiovisuals"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

load_all_textures()
load_all_items()
load_all_entities()
load_all_blocks()

cross = Sprite(parent=camera.ui, texture=T_CROSS, pixel_perfect=True, scale=0.02, alpha_mode="blend")
cross.enabled = False

inventory = Inventory()
inventory.enabled = False

hotbar = Hotbar()
hotbar.enabled = False

player = None
toggle_cooldown = 0

def start_game():
    global player

    create_world(size=16, max_height=8)
    player = PlayerController()

    mouse.locked = True
    ui.menu_panel.enabled = False

    cross.enabled = True
    hotbar.enabled = True
    inventory.enabled = True

ui.build_main_menu(start_game)

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

app = Ursina()
app.run()
