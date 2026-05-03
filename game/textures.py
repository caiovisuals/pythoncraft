from ursina import load_texture

T_PLAYER = None
T_PLAYER_FEMININE = None

T_GRASS_TOP = None
T_GRASS_SIDE = None
T_DIRT  = None
T_ROOTED_DIRT = None
T_LATO_DIRT = None
T_STONE = None
T_LIMESTONE = None
T_COBBLESTONE = None
T_WOOD  = None
T_CRAFTING_TABLE_TOP = None
T_CRAFTING_TABLE_SIDE = None
T_CRAFTING_TABLE_BOTTOM = None
T_GLASS = None
T_OBSIDIAN = None
T_OAK_LEAVES = None
T_ICE = None
T_DEEPSLATE = None
T_WATER_FLOW = None
T_WATER_STILL = None
T_LAVA_FLOW = None
T_LAVA_STILL = None
T_FIRE = None
T_PETROLEUM = None

T_COW = None
T_HORSE_BLACK = None
T_HORSE_BROWN = None
T_HORSE_CHESTNUT = None
T_HORSE_CREAMY = None
T_PIG = None
T_PALE_PIG = None
T_SPOTTED_PIG = None
T_SHEEP = None
T_SHEEP_FUR = None
T_CHICKEN = None
T_PLAYER = None

T_APPLE = None
T_BANANA = None
T_CARROT = None
T_CORN = None
T_BEEF = None
T_PORKCHOP = None
T_BREAD = None
T_BOOK = None
T_WHEAT_SEEDS = None
T_WHEAT = None
T_FLINT = None
T_BOWL = None
T_DIAMOND_SWORD = None
T_IRON_SWORD = None
T_STONE_SWORD = None
T_WOODEN_SWORD = None
T_STICK = None
T_ARROW = None

T_CROSS = None
T_HOTBAR = None
T_SELECTED_ITEM = None
T_HEART = None
T_PROTECTION = None
T_BLOCK_BACKGROUND = None
T_INVENTORY = None

player = {}
blocks = {}
entities = {}
items = {}
gui = {}

def load_all_textures():
    global T_PLAYER, T_PLAYER_FEMININE
    global T_GRASS_SIDE, T_GRASS_TOP, T_DIRT, T_ROOTED_DIRT, T_LATO_DIRT, T_STONE, T_LIMESTONE, T_COBBLESTONE, T_WOOD, T_CRAFTING_TABLE_TOP, T_CRAFTING_TABLE_SIDE, T_GLASS, T_OBSIDIAN, T_OAK_LEAVES, T_ICE, T_DEEPSLATE
    global T_WATER, T_LAVA, T_PETROLEUM
    global T_COW, T_HORSE_BLACK, T_HORSE_BROWN, T_HORSE_CHESTNUT, T_HORSE_CREAMY, T_PIG, T_PALE_PIG, T_SPOTTED_PIG, T_SHEEP, T_SHEEP_FUR, T_PLAYER
    global T_APPLE, T_BANANA, T_CARROT, T_CORN, T_BEEF, T_PORKCHOP, T_BREAD, T_BOOK, T_WHEAT_SEEDS, T_WHEAT, T_DIAMOND_SWORD, T_IRON_SWORD, T_STONE_SWORD, T_WOODEN_SWORD, T_STICK
    global T_CROSS, T_HOTBAR, T_SELECTED_ITEM, T_HEART, T_PROTECTION, T_BLOCK_BACKGROUND, T_INVENTORY

    global player, blocks, entities, items, gui

    T_PLAYER = load_texture('assets/textures/entities/player/player_male.png')
    T_PLAYER_FEMININE = load_texture('assets/textures/entities/player/player_feminine.png')

    player = {
        "player": T_PLAYER,
        "player_feminine": T_PLAYER_FEMININE,
    }

    T_GRASS_TOP = load_texture('assets/textures/blocks/grass_top.png')
    T_GRASS_SIDE = load_texture('assets/textures/blocks/grass_side.png')
    T_DIRT  = load_texture('assets/textures/blocks/dirt.png')
    T_ROOTED_DIRT  = load_texture('assets/textures/blocks/rooted_dirt.png')
    T_LATO_DIRT  = load_texture('assets/textures/blocks/lato_dirt.png')
    T_STONE = load_texture('assets/textures/blocks/stone.png')
    T_LIMESTONE = load_texture('assets/textures/blocks/limestone.png')
    T_COBBLESTONE = load_texture('assets/textures/blocks/cobblestone.png')
    T_WOOD  = load_texture('assets/textures/blocks/wood.png')
    T_CRAFTING_TABLE_TOP = load_texture('assets/textures/blocks/crafting_table_top.png')
    T_CRAFTING_TABLE_SIDE  = load_texture('assets/textures/blocks/crafting_table_side.png')
    T_CRAFTING_TABLE_BOTTOM = load_texture('assets/textures/blocks/crafting_table_bottom.png')
    T_GLASS = load_texture('assets/textures/blocks/glass.png')
    T_OBSIDIAN = load_texture('assets/textures/blocks/obsidian.png')
    T_OAK_LEAVES = load_texture('assets/textures/blocks/oak_leaves.png')
    T_ICE = load_texture('assets/textures/blocks/ice.png')
    T_DEEPSLATE = load_texture('assets/textures/blocks/deepslate.png')
    T_WATER = load_texture('assets/textures/blocks/water.png')
    T_LAVA = load_texture('assets/textures/blocks/lava.png')
    T_PETROLEUM = load_texture('assets/textures/blocks/petroleum.png')

    blocks = {
        "grass_top": T_GRASS_TOP,
        "grass_side": T_GRASS_SIDE,
        "dirt": T_DIRT,
        "rooted_dirt": T_ROOTED_DIRT,
        "lato_dirt": T_LATO_DIRT,
        "stone": T_STONE,
        "limestone": T_LIMESTONE,
        "cobblestone": T_COBBLESTONE,
        "wood": T_WOOD,
        "crafting_table_top": T_CRAFTING_TABLE_TOP,
        "crafting_table_side": T_CRAFTING_TABLE_SIDE,
        "crafting_table_bottom": T_CRAFTING_TABLE_BOTTOM,
        "glass": T_GLASS,
        "obsidian": T_OBSIDIAN,
        "oak_leaves": T_OAK_LEAVES,
        "ice": T_ICE,
        "deepslate": T_DEEPSLATE,
        "water": T_WATER,
        "lava": T_LAVA,
        "petroleum": T_PETROLEUM,
    }

    T_COW = load_texture('assets/textures/entities/cow/cow.png')
    T_HORSE_BLACK = load_texture('assets/textures/entities/horse/horse_black.png')
    T_HORSE_BROWN = load_texture('assets/textures/entities/horse/horse_brown.png')
    T_HORSE_CHESTNUT = load_texture('assets/textures/entities/horse/horse_chestnut.png')
    T_HORSE_CREAMY = load_texture('assets/textures/entities/horse/horse_creamy.png')
    T_PIG = load_texture('assets/textures/entities/pig/pig.png')
    T_PALE_PIG = load_texture('assets/textures/entities/pig/pale_pig.png')
    T_SPOTTED_PIG = load_texture('assets/textures/entities/pig/spotted_pig.png')
    T_SHEEP  = load_texture('assets/textures/entities/sheep/sheep.png')
    T_SHEEP_FUR  = load_texture('assets/textures/entities/sheep/sheep_fur.png')
    T_CHICKEN = load_texture('assets/textures/entities/chicken/chicken.png')
    T_PLAYER = load_texture('assets/textures/entities/player.png')

    entities = {
        "cow": T_COW,
        "horse_black": T_HORSE_BLACK,
        "horse_brown": T_HORSE_BROWN,
        "horse_chestnut": T_HORSE_CHESTNUT,
        "horse_creamy": T_HORSE_CREAMY,
        "pig": T_PIG,
        "pale_pig": T_PALE_PIG,
        "spotted_pig": T_SPOTTED_PIG,
        "sheep": T_SHEEP,
        "sheep_fur": T_SHEEP_FUR,
        "chicken": T_CHICKEN,
        "player": T_PLAYER,
    }

    T_APPLE = load_texture('assets/textures/items/apple.png')
    T_BANANA = load_texture('assets/textures/items/banana.png')
    T_CARROT = load_texture('assets/textures/items/carrot.png')
    T_CORN = load_texture('assets/textures/items/corn.png')
    T_BEEF = load_texture('assets/textures/items/beef.png')
    T_PORKCHOP = load_texture('assets/textures/items/porkchop.png')
    T_BREAD = load_texture('assets/textures/items/bread.png')
    T_BOOK = load_texture('assets/textures/items/book.png')
    T_WHEAT_SEEDS = load_texture('assets/textures/items/wheat_seeds.png')
    T_WHEAT = load_texture('assets/textures/items/wheat.png')
    T_FLINT = load_texture('assets/textures/items/flint.png')
    T_BOWL = load_texture('assets/textures/items/bowl.png')
    T_DIAMOND_SWORD = load_texture('assets/textures/items/diamond_sword.png')
    T_IRON_SWORD = load_texture('assets/textures/items/iron_sword.png')
    T_STONE_SWORD = load_texture('assets/textures/items/stone_sword.png')
    T_WOODEN_SWORD = load_texture('assets/textures/items/wooden_sword.png')
    T_STICK = load_texture('assets/textures/items/stick.png')
    T_ARROW = load_texture('assets/textures/items/arrow.png')

    items = {
        "apple": T_APPLE,
        "banana": T_BANANA,
        "carrot": T_CARROT,
        "corn": T_CORN,
        "beef": T_BEEF,
        "porkchop": T_PORKCHOP,
        "bread": T_BREAD,
        "book": T_BOOK,
        "wheat_seeds": T_WHEAT_SEEDS,
        "wheat": T_WHEAT,
        "flint": T_FLINT,
        "bowl": T_BOWL,
        "diamond_sword": T_DIAMOND_SWORD,
        "iron_sword": T_IRON_SWORD,
        "stone_sword": T_STONE_SWORD,
        "wooden_sword": T_WOODEN_SWORD,
        "stick": T_STICK,
        "arrow": T_ARROW,
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
