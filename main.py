import os
import sys
from pathlib import Path

# Os assets são carregados com caminhos relativos à raiz do projeto
os.chdir(Path(__file__).resolve().parent)

from ursina import *

app = Ursina()

from game.core.player import PlayerController
from game.core.physics import block_overlaps_player
from game.core.state import State, game
from game.core.modes import get_mode
from game.core.world import create_world, clear_world, break_block, place_block, get_block_at, set_light_level
from game.graphics.lighting import DayNightLighting
from game.graphics.particles import spawn_particles
from game.inventory import Hotbar, InventoryScreen
from game.textures import load_all_textures
from game.items import load_all_items
from game.entities import load_all_entities
from game.blocks import load_all_blocks
from game.hud import HUD
from game.sounds import play_break_block, play_place_block
import game.textures as textures
import game.ui as ui

# Rode com `python main.py --debug` para habilitar atalhos de desenvolvimento
DEBUG = "--debug" in sys.argv

REACH = 6  # distância máxima para quebrar/colocar blocos

window.title = "pythoncraft - bycaiovisuals"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

load_all_textures()
load_all_items()
load_all_entities()
load_all_blocks()

cross = Sprite(
    parent=camera.ui,
    texture=textures.gui["crosshair"],
    pixel_perfect=True,
    scale=0.25,
    color=color.white,
    double_sided=True,
    enabled=False,
)

# A UI do jogador é criada uma única vez e reaproveitada entre partidas/respawns
hotbar = Hotbar(enabled=False)
inventory_screen = InventoryScreen()
hud = HUD()

MENU_BACKGROUND = window.color
lighting = DayNightLighting(set_light_level)
lighting.enabled = False
lighting.set_visible(False)
window.color = MENU_BACKGROUND

spawn_point = Vec3(0, 0, 0)

def _set_game_ui_visible(visible: bool):
    cross.enabled = visible
    hotbar.enabled = visible
    if visible:
        hud.show(show_vitals=game.mode.uses_vitals)
    else:
        hud.hide()
        inventory_screen.enabled = False

def _spawn_player():
    game.player = PlayerController(hotbar=hotbar, inventory_screen=inventory_screen, mode=game.mode)
    game.player.position = spawn_point
    game.player.on_death_callback = _on_player_death

    hud.attach_player(game.player)
    _set_game_ui_visible(True)
    mouse.locked = True

def _destroy_player():
    if game.player:
        destroy(game.player)
        game.player = None
    hud.attach_player(None)

def _try_break_block():
    """Quebra o bloco apontado pelo crosshair (click esquerdo)."""
    hit = raycast(camera.world_position, camera.forward, distance=REACH, ignore=[game.player])
    if not hit.hit:
        return

    # Posição do bloco atingido = ponto de impacto recuado pela normal
    bx = round(hit.world_point.x - hit.world_normal.x * 0.5)
    by = round(hit.world_point.y - hit.world_normal.y * 0.5)
    bz = round(hit.world_point.z - hit.world_normal.z * 0.5)

    block_id = get_block_at((bx, by, bz))
    if break_block((bx, by, bz)):
        game.mode.on_block_broken(block_id, hotbar)
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
    hit = raycast(camera.world_position, camera.forward, distance=REACH, ignore=[game.player])
    if not hit.hit:
        return

    # Posição adjacente = ponto de impacto avançado pela normal
    bx = round(hit.world_point.x + hit.world_normal.x * 0.5)
    by = round(hit.world_point.y + hit.world_normal.y * 0.5)
    bz = round(hit.world_point.z + hit.world_normal.z * 0.5)

    # Não deixa colocar bloco dentro do jogador (pés ou cabeça)
    if block_overlaps_player((bx, by, bz), game.player.position):
        return

    block_id = game.mode.block_to_place(hotbar)
    if block_id and place_block((bx, by, bz), block_id):
        game.mode.on_block_placed(hotbar)
        play_place_block()

def _on_player_death():
    if game.is_(State.PLAYING):
        game.change(State.DEAD)

def start_game(mode_id: str):
    game.mode = get_mode(mode_id)
    game.change(State.LOADING)
    game.change(State.PLAYING)

def _respawn():
    game.change(State.PLAYING)

def quit_to_menu():
    game.change(State.MENU)

# Reações da máquina de estados

def _enter_loading(previous):
    """Gera o mundo e prepara a hotbar do modo escolhido."""
    global spawn_point
    ui.menu_panel.enabled = False

    surface_y = create_world(size=16, max_height=8)
    spawn_point = Vec3(0, surface_y + 3, 0)
    game.mode.setup_hotbar(hotbar)
    hotbar.select(0)

    lighting.cycle.time_of_day = 0.3  # começa de manhã
    lighting.set_visible(True)
    lighting.apply()

def _enter_playing(previous):
    if previous == State.LOADING:
        _spawn_player()
    elif previous == State.DEAD:
        # Renasce no ponto inicial, mantendo o mundo
        _destroy_player()
        _spawn_player()
    elif previous == State.PAUSED:
        ui.set_settings_visible(False)
        game.player.enabled = True
        mouse.locked = True
    lighting.enabled = True

def _enter_paused(previous):
    ui.set_settings_visible(True)
    game.player.enabled = False
    mouse.locked = False
    lighting.enabled = False  # o tempo para enquanto pausado

def _enter_dead(previous):
    _set_game_ui_visible(False)
    mouse.locked = False
    ui.show_death_screen()

def _exit_dead(next_state):
    """Renasce no ponto inicial, mantendo o mundo."""
    ui.hide_death_screen()

def _enter_menu(previous):
    """Sai da partida: remove jogador e mundo e volta ao menu principal."""
    ui.set_settings_visible(False)
    _destroy_player()
    _set_game_ui_visible(False)
    clear_world()

    lighting.enabled = False
    lighting.set_visible(False)
    window.color = MENU_BACKGROUND

    ui.menu_panel.enabled = True
    mouse.locked = False

game.on_enter(State.LOADING, _enter_loading)
game.on_enter(State.PLAYING, _enter_playing)
game.on_enter(State.PAUSED, _enter_paused)
game.on_enter(State.DEAD, _enter_dead)
game.on_exit(State.DEAD, _exit_dead)
game.on_enter(State.MENU, _enter_menu)

ui.build_main_menu(start_game)
ui.build_death_screen(_respawn, quit_to_menu)

def input(key):
    if game.is_(State.PAUSED):
        if key == "escape":
            game.change(State.PLAYING)
        return

    if not game.is_(State.PLAYING):
        return

    player = game.player

    if key == "escape":
        if player.inventory_enabled:
            player.toggle_inventory()
            cross.enabled = True
        else:
            game.change(State.PAUSED)
        return

    if DEBUG and key == "r":
        quit_to_menu()
        return

    player.handle_input(key)
    cross.enabled = not player.inventory_enabled

    if player.inventory_enabled:
        return

    if key == "left mouse down":
        _try_break_block()

    elif key == "right mouse down":
        _try_place_block()

    # Scroll da hotbar
    elif key == "scroll up":
        hotbar.hotbar.scroll(1)

    elif key == "scroll down":
        hotbar.hotbar.scroll(-1)

    # Atalhos numéricos 1-9 para selecionar slot da hotbar
    elif len(key) == 1 and key in "123456789":
        hotbar.hotbar.select(int(key) - 1)

app.run()