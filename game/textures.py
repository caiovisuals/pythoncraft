from ursina import load_texture

T_GRASS = None
T_DIRT  = None
T_STONE = None
T_WOOD  = None
T_CRAFTING_TABLE_TOP = None
T_CRAFTING_TABLE_SIDE = None

T_COW = None
T_HORSE_BLACK = None
T_HORSE_BROWN = None
T_HORSE_CHESTNUT = None
T_HORSE_CREAMY = None
T_PIG = None
T_SHEEP = None
T_SHEEP_FUR = None
T_PLAYER = None

T_APPLE = None
T_DIAMOND_SWORD = None
T_IRON_SWORD = None
T_STONE_SWORD = None
T_STICK = None

T_CROSS = None
T_HOTBAR = None
T_SELECTED_ITEM = None
T_HEART = None
T_PROTECTION = None
T_BLOCK_BACKGROUND = None
T_INVENTORY = None

blocks = {}
entities = {}
items = {}
gui = {}

def load_all_textures():
    global T_GRASS, T_DIRT, T_STONE, T_WOOD, T_CRAFTING_TABLE_TOP, T_CRAFTING_TABLE_SIDE
    global T_COW, T_HORSE_BLACK, T_HORSE_BROWN, T_HORSE_CHESTNUT, T_HORSE_CREAMY, T_PIG, T_SHEEP, T_SHEEP_FUR, T_PLAYER
    global T_APPLE, T_DIAMOND_SWORD, T_IRON_SWORD, T_STONE_SWORD, T_STICK
    global T_CROSS, T_HOTBAR, T_SELECTED_ITEM, T_HEART, T_PROTECTION, T_BLOCK_BACKGROUND, T_INVENTORY

    global blocks, entities, items, gui

    T_GRASS = load_texture('assets/textures/blocks/grass.png')
    T_DIRT  = load_texture('assets/textures/blocks/dirt.png')
    T_STONE = load_texture('assets/textures/blocks/stone.png')
    T_WOOD  = load_texture('assets/textures/blocks/wood.png')
    T_CRAFTING_TABLE_TOP = load_texture('assets/textures/blocks/crafting_table_top.png')
    T_CRAFTING_TABLE_SIDE  = load_texture('assets/textures/blocks/crafting_table_side.png')

    blocks = {
        "grass": T_GRASS,
        "dirt": T_DIRT,
        "stone": T_STONE,
        "wood": T_WOOD,
        "crafting_table_top": T_CRAFTING_TABLE_TOP,
        "crafting_table_side": T_CRAFTING_TABLE_SIDE,
    }

    T_COW = load_texture('assets/textures/entities/cow/cow.png')
    T_HORSE_BLACK = load_texture('assets/textures/entities/horse/horse_black.png')
    T_HORSE_BROWN = load_texture('assets/textures/entities/horse/horse_brown.png')
    T_HORSE_CHESTNUT = load_texture('assets/textures/entities/horse/horse_chestnut.png')
    T_HORSE_CREAMY = load_texture('assets/textures/entities/horse/horse_creamy.png')
    T_PIG = load_texture('assets/textures/entities/pig/pig.png')
    T_SHEEP  = load_texture('assets/textures/entities/sheep/sheep.png')
    T_SHEEP_FUR  = load_texture('assets/textures/entities/sheep/sheep_fur.png')
    T_PLAYER = load_texture('assets/textures/entities/player.png')

    entities = {
        "cow": T_COW,
        "horse_black": T_HORSE_BLACK,
        "horse_brown": T_HORSE_BROWN,
        "horse_chestnut": T_HORSE_CHESTNUT,
        "horse_creamy": T_HORSE_CREAMY,
        "pig": T_PIG,
        "sheep": T_SHEEP,
        "sheep_fur": T_SHEEP_FUR,
        "player": T_PLAYER,
    }

    T_APPLE = load_texture('assets/textures/items/apple.png')
    T_DIAMOND_SWORD = load_texture('assets/textures/items/diamond_sword.png')
    T_IRON_SWORD = load_texture('assets/textures/items/iron_sword.png')
    T_STONE_SWORD = load_texture('assets/textures/items/stone_sword.png')
    T_STICK = load_texture('assets/textures/items/stick.png')

    items = {
        "apple": T_APPLE,
        "diamond_sword": T_DIAMOND_SWORD,
        "iron_sword": T_IRON_SWORD,
        "stone_sword": T_STONE_SWORD,
        "stick": T_STICK,
    }

    T_CROSS = load_texture('assets/textures/gui/crosshair.png')
    T_HOTBAR = load_texture('assets/textures/gui/hotbar.png')
    T_SELECTED_ITEM = load_texture('assets/textures/gui/selected_item.png')
    T_HEART = load_texture('assets/textures/gui/heart.png')
    T_PROTECTION = load_texture('assets/textures/gui/protection.png')
    T_BLOCK_BACKGROUND = load_texture('assets/textures/gui/block_background.png')
    T_INVENTORY = load_texture('assets/textures/gui/container/inventory.png')

    gui = {
        "cross": T_CROSS,
        "hotbar": T_HOTBAR,
        "selected_item": T_SELECTED_ITEM,
        "heart": T_HEART,
        "protection": T_PROTECTION,
        "block_background": T_BLOCK_BACKGROUND,
        "inventory": T_INVENTORY,
    }
