from ursina import *
import random
import time

app = Ursina()

from game.player import PlayerController
from game.textures import load_all_textures
from game.world import create_test_world, world_parent
from game.items import load_all_items, get_item, ITEMS
from game.entities import load_all_entities, ENTITIES
from game.textures import T_CROSS
from game.inventory import Inventory, Hotbar
from game.ui import build_main_menu, toggle_settings_panel, settings_panel, menu_panel

window.title = 'pythoncraft - bycaiovisuals'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

cross = Sprite(parent=camera.ui, texture=T_CROSS, pixel_perfect=True, scale=0.02)

player = None
load_all_textures()
load_all_items()
load_all_entities()
inventory = Inventory()
hotbar = Hotbar()
build_main_menu()

toggle_cooldown = 0

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

    if key == 'e':
        if player:
            inventory.toggle()
            if inventory.visible:
                player.enabled = False
            else:
                player.enabled = True  

    if key == 'r':
        menu_panel.enabled = True
        settings_panel.enabled = False
        mouse.locked = False
        def cleanup_world():
            children = world_parent.children[:]
            batch_size = 50
            for i in range(0, len(children), batch_size):
                for c in children[i:i+batch_size]:
                    destroy(c)
                time.sleep(0.01)
            if player:
                destroy(player)
                player = None
            inventory.visible = False
            inventory.enabled = False
            hotbar.enabled = True
        cleanup_world()

app.run()
