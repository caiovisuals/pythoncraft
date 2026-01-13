from ursina import *
import random
import time

app = Ursina()

from game.core.player import PlayerController
from game.core.world import create_test_world, world_parent
from game.graphics.particles import spawn_particles
from game.textures import load_all_textures
from game.items import load_all_items, get_item, ITEMS
from game.entities import load_all_entities, ENTITIES
from game.blocks import load_all_blocks, BLOCKS
from game.textures import T_CROSS
from game.inventory import Inventory, Hotbar
from game.ui import build_main_menu, toggle_settings_panel, settings_panel, menu_panel

window.title = 'pythoncraft - bycaiovisuals'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

cross = Sprite(parent=camera.ui, texture=T_CROSS, pixel_perfect=True, scale=0.02)

load_all_textures()
load_all_items()
load_all_entities()
inventory = Inventory()
hotbar = Hotbar()
build_main_menu()

player = None

def start_game():
    global player
    create_test_world(size=16, height=2)
    player = PlayerController()
    mouse.locked = True
    menu_panel.enabled = False

def input(key):
    global player, toggle_cooldown
    if time.time() - toggle_cooldown < 0.1:
        return
    toggle_cooldown = time.time()
    if key == 'escape':
        if menu_panel.enabled:
            return
        toggle_settings_panel()
        if player:
            player.enabled = not settings_panel.enabled

    if key == 'r':
        menu_panel.enabled = True
        settings_panel.enabled = False
        mouse.locked = False

        children = world_parent.children[:]
        batch_size = 50
        for i in range(0, len(children), batch_size):
            for c in children[i:i+batch_size]:
                destroy(c)
            time.sleep(0.01)

        if player:
            destroy(player)
            player = None

    if player:
        player.handle_input(key)

app.run()
