T_GRASS = None
T_DIRT  = None
T_STONE = None
T_WOOD  = None
T_CROSS = None

def load_all_textures():
    from ursina import load_texture
    global T_GRASS, T_DIRT, T_STONE, T_WOOD, T_CROSS

    T_GRASS = load_texture('assets/textures/blocks/grass.png')
    T_DIRT  = load_texture('assets/textures/blocks/dirt.png')
    T_STONE = load_texture('assets/textures/blocks/stone.png')
    T_WOOD  = load_texture('assets/textures/blocks/wood.png')
    T_CROSS = load_texture('assets/textures/gui/crosshair.png')
