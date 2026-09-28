import math
import random
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
breaking: list = []   # estágios da rachadura ao quebrar um bloco (0 = começo)

BREAKING_STAGES = 10

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

def _crack_pixels(size: int, seed: int) -> list:
    """
    Pixels das rachaduras em ordem de crescimento: várias linhas tortas saindo
    do centro, avançando um passo de cada vez em todas elas.
    """
    rng = random.Random(seed)
    walks = []
    for _ in range(7):
        walks.append([size / 2 + rng.uniform(-2, 2), size / 2 + rng.uniform(-2, 2), rng.uniform(0, 2 * math.pi)])

    pixels, seen = [], set()
    for _ in range(size):
        for walk in walks:
            walk[2] += rng.uniform(-0.7, 0.7)
            walk[0] += math.cos(walk[2])
            walk[1] += math.sin(walk[2])
            p = (int(walk[0]), int(walk[1]))
            if 0 <= p[0] < size and 0 <= p[1] < size and p not in seen:
                seen.add(p)
                pixels.append(p)
    return pixels

def _make_breaking_stages(stages: int = BREAKING_STAGES, size: int = 16, seed: int = 7) -> list:
    """Gera as texturas de rachadura (não há imagens delas em assets/)."""
    pixels = _crack_pixels(size, seed)
    result = []
    for stage in range(stages):
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        visible = pixels[: max(1, len(pixels) * (stage + 1) // stages)]
        for p in visible:
            image.putpixel(p, (20, 20, 20, 200))
        result.append(Texture(image))
    return result

def load_all_textures():
    global player, blocks, entities, items, gui, breaking

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
        "crafter": _load(gui_dir / "container/crafter.png"),
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

    breaking = _make_breaking_stages()