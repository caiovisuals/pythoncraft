from pathlib import Path
from PIL import Image
from ursina import load_texture, Texture

TEXTURES_DIR = Path("assets/textures")

# Dicionários preenchidos por load_all_textures(), indexados pelo nome do arquivo (sem .png)
player: dict = {}
blocks: dict = {}
entities: dict = {}
items: dict = {}
gui: dict = {}

# Nomes alternativos para texturas animadas/variações
BLOCK_ALIASES = {
    "fire": "fire_0",
}

def _load(path: Path):
    """Carrega uma textura. Retorna None (com aviso) se o arquivo não existir."""
    if not path.is_file():
        print(f"[textures] arquivo não encontrado: {path.as_posix()}")
        return None
    return load_texture(path.as_posix())

def _load_folder(folder: Path, recursive: bool = False) -> dict:
    """Carrega todos os .png de uma pasta, usando o nome do arquivo como chave."""
    pattern = "**/*.png" if recursive else "*.png"
    return {p.stem: _load(p) for p in sorted(folder.glob(pattern))}

def _crop(path: Path, box: tuple):
    """Recorta um pedaço de uma sprite sheet e retorna como textura."""
    if not path.is_file():
        print(f"[textures] arquivo não encontrado: {path.as_posix()}")
        return None
    image = Image.open(path).convert("RGBA").crop(box)
    return Texture(image)

def load_all_textures():
    global player, blocks, entities, items, gui

    player = {
        "player": _load(TEXTURES_DIR / "entities/player/player_male.png"),
        "player_feminine": _load(TEXTURES_DIR / "entities/player/player_feminine.png"),
    }

    blocks = _load_folder(TEXTURES_DIR / "blocks")
    for alias, name in BLOCK_ALIASES.items():
        blocks[alias] = blocks.get(name)

    entities = _load_folder(TEXTURES_DIR / "entities", recursive=True)
    entities["player"] = player["player"]

    items = _load_folder(TEXTURES_DIR / "items")

    gui_dir = TEXTURES_DIR / "gui"
    sprites_dir = gui_dir / "container/sprites"

    gui = {
        "crosshair": _load(gui_dir / "crosshair.png"),
        "hotbar": _load(gui_dir / "hotbar.png"),
        "selected_item": _load(gui_dir / "selected_item.png"),
        "protection": _load(gui_dir / "protection.png"),
        "block_background": _load(gui_dir / "block_background.png"),
        "survival_inventory": _load(gui_dir / "container/survival-inventory.png"),
        "slot": _load(sprites_dir / "slot.png"),
        "slot_highlight_back": _load(sprites_dir / "slot_highlight_back.png"),
        "slot_highlight_front": _load(sprites_dir / "slot_highlight_front.png"),
        "slot_helmet": _load(sprites_dir / "slot/helmet.png"),
        "slot_chestplate": _load(sprites_dir / "slot/chestplate.png"),
        "slot_leggings": _load(sprites_dir / "slot/leggings.png"),
        "slot_boots": _load(sprites_dir / "slot/boots.png"),
        # heart.png é uma sprite sheet 26x9: contorno | cheio | metade
        "heart_container": _crop(gui_dir / "heart.png", (0, 0, 9, 9)),
        "heart_full": _crop(gui_dir / "heart.png", (9, 0, 18, 9)),
        "heart_half": _crop(gui_dir / "heart.png", (18, 0, 27, 9)),
    }