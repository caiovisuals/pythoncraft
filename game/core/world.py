from ursina import *
from game.blocks import get_block
from perlin_noise import PerlinNoise
import random

# Configurações
CHUNK_SIZE  = 16   # blocos por chunk (X e Z)
RENDER_DIST = 10    # chunks visíveis em cada direção a partir do jogador
WORLD_BOTTOM = -3  # camada mais baixa do mundo

noise = PerlinNoise(octaves=4)

world_parent  = Entity()
placed_blocks: dict[tuple, str] = {}   # (x,y,z) → block_id string
_chunk_entities: dict[tuple, Entity] = {}  # (cx,cz) → entity da mesh
_colliders: dict[tuple, Entity] = {}      # (x,y,z) → colisor invisível do bloco
_light_level = 1.0                         # brilho do mundo (ciclo dia/noite)

_NEIGHBOR_OFFSETS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

# Geração de altura
def get_height(x: int, z: int, scale: float = 20, amplitude: int = 6) -> int:
    value = noise([x / scale, z / scale])
    return int(((value + 1) / 2) * amplitude)

def _block_id_for_layer(y: int, surface_y: int) -> str:
    if y == surface_y:
        return "grass"
    elif y > surface_y - 3:
        return "dirt"
    else:
        return "stone"

# Faces do cubo — direção, normal, vértices, UV, vizinho
#  Cada face: (nome, vizinho_offset, vértices em ordem quad, rotação_euler_para_UV)
#  Os vértices já estão em espaço local do bloco (centro = 0,0,0).

_HALF = 0.5

_FACES = [
    # name,   offset,       4 vértices (x,y,z)
    ("top",    ( 0,  1,  0), [
        Vec3(-_HALF,  _HALF, -_HALF),
        Vec3( _HALF,  _HALF, -_HALF),
        Vec3( _HALF,  _HALF,  _HALF),
        Vec3(-_HALF,  _HALF,  _HALF),
    ]),
    ("bottom", ( 0, -1,  0), [
        Vec3(-_HALF, -_HALF,  _HALF),
        Vec3( _HALF, -_HALF,  _HALF),
        Vec3( _HALF, -_HALF, -_HALF),
        Vec3(-_HALF, -_HALF, -_HALF),
    ]),
    ("front",  ( 0,  0,  1), [
        Vec3(-_HALF, -_HALF,  _HALF),
        Vec3(-_HALF,  _HALF,  _HALF),
        Vec3( _HALF,  _HALF,  _HALF),
        Vec3( _HALF, -_HALF,  _HALF),
    ]),
    ("back",   ( 0,  0, -1), [
        Vec3( _HALF, -_HALF, -_HALF),
        Vec3( _HALF,  _HALF, -_HALF),
        Vec3(-_HALF,  _HALF, -_HALF),
        Vec3(-_HALF, -_HALF, -_HALF),
    ]),
    ("right",  ( 1,  0,  0), [
        Vec3( _HALF, -_HALF,  _HALF),
        Vec3( _HALF,  _HALF,  _HALF),
        Vec3( _HALF,  _HALF, -_HALF),
        Vec3( _HALF, -_HALF, -_HALF),
    ]),
    ("left",   (-1,  0,  0), [
        Vec3(-_HALF, -_HALF, -_HALF),
        Vec3(-_HALF,  _HALF, -_HALF),
        Vec3(-_HALF,  _HALF,  _HALF),
        Vec3(-_HALF, -_HALF,  _HALF),
    ]),
]

# UV de um quad inteiro
_QUAD_UVS = [
    Vec2(0, 0),
    Vec2(1, 0),
    Vec2(1, 1),
    Vec2(0, 1),
]

_SIDE_UVS = [
    Vec2(1, 0),
    Vec2(1, 1),
    Vec2(0, 1),
    Vec2(0, 0),
]

# 2 triângulos por quad (índices dentro dos 4 vértices da face)
_QUAD_TRIS = [0, 1, 2, 2, 3, 0]

# Iluminação básica por face (como no Minecraft): topo claro, laterais e fundo mais escuros
_FACE_SHADE = {
    "top": 1.0,
    "front": 0.8,
    "back": 0.8,
    "right": 0.65,
    "left": 0.65,
    "bottom": 0.5,
}

# Resolução de textura por face
def _face_texture(block, face_name: str):
    """Retorna a textura correta de acordo com o nome da face."""
    tex_map = block.textures          # dict com top/bottom/side
    if face_name == "top":
        return tex_map.get("top") or tex_map.get("side")
    elif face_name == "bottom":
        return tex_map.get("bottom") or tex_map.get("side")
    else:   # front / back / right / left  → side
        return tex_map.get("side") or tex_map.get("top")

# Construção de mesh por grupo de textura dentro de um chunk
def _build_chunk_mesh(cx: int, cz: int) -> Entity:
    """
    Constrói uma Entity por textura única dentro do chunk.
    Retorna um Entity-pai que agrupa todas as sub-meshes.
    """
    x0 = cx * CHUNK_SIZE
    z0 = cz * CHUNK_SIZE

    # Acumula vértices/UVs/triângulos separados por textura
    tex_buckets: dict = {}   # texture_object → {verts, uvs, tris}

    # Pré-computa mapa de coluna → lista de y, limitado ao chunk (O(n) total)
    col_map: dict[tuple, list] = {}
    for (bx, by, bz) in placed_blocks:
        if x0 <= bx < x0 + CHUNK_SIZE and z0 <= bz < z0 + CHUNK_SIZE:
            key = (bx, bz)
            if key not in col_map:
                col_map[key] = []
            col_map[key].append(by)

    for x in range(x0, x0 + CHUNK_SIZE):
        for z in range(z0, z0 + CHUNK_SIZE):
            if (x, z) not in col_map:
                continue

            for y in col_map[(x, z)]:
                block_id = placed_blocks.get((x, y, z))
                if block_id is None:
                    continue
                block = get_block(block_id)
                if block is None:
                    continue

                for face_name, (dx, dy, dz), verts in _FACES:
                    nx, ny, nz = x + dx, y + dy, z + dz

                    # Só renderiza face se o vizinho estiver vazio (face culling)
                    if placed_blocks.get((nx, ny, nz)) is not None:
                        neighbor_block = get_block(placed_blocks[(nx, ny, nz)])
                        # Blocos opacos ocultam a face — blocos transparentes não
                        if neighbor_block and not neighbor_block.transparent:
                            continue

                    tex = _face_texture(block, face_name)
                    if tex is None:
                        continue

                    bucket = tex_buckets.setdefault(tex, {"verts": [], "uvs": [], "tris": [], "colors": []})
                    shade = _FACE_SHADE[face_name]
                    face_color = color.Color(shade, shade, shade, 1)

                    base_idx = len(bucket["verts"])
                    uvs = _QUAD_UVS if face_name in ("top", "bottom") else _SIDE_UVS
                    for v, uv in zip(verts, uvs):
                        bucket["verts"].append(Vec3(v.x + x, v.y + y, v.z + z))
                        bucket["uvs"].append(uv)
                        bucket["colors"].append(face_color)
                    for t in _QUAD_TRIS:
                        bucket["tris"].append(base_idx + t)

    # Cria o entity-pai do chunk
    parent_entity = Entity(parent=world_parent)

    for tex, data in tex_buckets.items():
        if not data["verts"]:
            continue
        mesh = Mesh(
            vertices=data["verts"],
            uvs=data["uvs"],
            colors=data["colors"],
            triangles=data["tris"],
            mode="triangle",
        )
        Entity(
            parent=parent_entity,
            model=mesh,
            texture=tex,
            color=color.Color(_light_level, _light_level, _light_level, 1),
        )

    return parent_entity

def is_exposed(pos: tuple, blocks: dict) -> bool:
    """
    Um bloco precisa de colisor quando algum vizinho está vazio, ou seja,
    quando o jogador pode encostar nele ou mirar nele.
    O "vizinho" abaixo da camada mais baixa do mundo não conta.
    """
    x, y, z = pos
    for dx, dy, dz in _NEIGHBOR_OFFSETS:
        ny = y + dy
        if ny < WORLD_BOTTOM:
            continue
        if (x + dx, ny, z + dz) not in blocks:
            return True
    return False

def _update_collider(pos: tuple):
    """Cria ou remove o colisor de uma posição conforme ela esteja exposta."""
    needs_collider = pos in placed_blocks and is_exposed(pos, placed_blocks)
    has_collider = pos in _colliders

    if needs_collider and not has_collider:
        _colliders[pos] = Entity(
            parent=world_parent,
            position=pos,
            model="cube",
            collider="box",
            visible=False,
            color=color.clear,
        )
    elif has_collider and not needs_collider:
        destroy(_colliders.pop(pos))

def _spawn_all_colliders():
    """Cria colisores para todos os blocos expostos (usado ao gerar o mundo)."""
    for pos in placed_blocks:
        _update_collider(pos)

def _update_colliders_around(pos: tuple):
    """Atualiza o colisor da posição editada e dos 6 vizinhos."""
    x, y, z = pos
    _update_collider(pos)
    for dx, dy, dz in _NEIGHBOR_OFFSETS:
        _update_collider((x + dx, y + dy, z + dz))

# Geração de árvores e minérios

def _place_tree(x: int, surface_y: int, z: int):
    """Planta uma árvore de carvalho simples no ponto (x, surface_y, z)."""
    trunk_height = random.randint(4, 6)

    for dy in range(1, trunk_height + 1):
        placed_blocks[(x, surface_y + dy, z)] = "oak_log"

    top_y = surface_y + trunk_height
    for dy in range(-1, 3):
        radius = 2 if dy < 1 else 1
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if dx == 0 and dz == 0 and dy < 1:
                    continue  # tronco já colocado
                pos = (x + dx, top_y + dy, z + dz)
                if pos not in placed_blocks:
                    placed_blocks[pos] = "oak_leaves"


def _generate_trees(surface_map: dict, seed: int):
    """Espalha árvores aleatoriamente sobre a superfície."""
    rng = random.Random(seed)
    positions = list(surface_map.keys())
    rng.shuffle(positions)

    min_distance = 8
    spawn_clearance = 3
    placed_trees = []

    # 1 árvore a cada 20 colunas; não planta na borda
    for (x, z) in positions:
        if rng.random() > 0.05:
            continue
        if abs(x) <= spawn_clearance and abs(z) <= spawn_clearance:
            continue
        sy = surface_map[(x, z)]
        if placed_blocks.get((x, sy, z)) != "grass":
            continue
        too_close = False
        for (tx, tz) in placed_trees:
            if (x - tx)**2 + (z - tz)**2 < min_distance**2:
                too_close = True
                break
        if too_close:
            continue

        _place_tree(x, sy, z)
        placed_trees.append((x, z))


def _generate_ores(surface_map: dict, seed: int):
    """Insere veios de minério nas camadas de pedra."""
    rng = random.Random(seed + 1)

    ore_table = [
        # (block_id, prob_por_bloco, y_max_relativo_superficie)
        ("coal_ore",    0.04, -2),
        ("iron_ore",    0.02, -4),
        ("gold_ore",    0.01, -6),
        ("diamond_ore", 0.004, -8),
    ]

    for (x, y, z), block_id in list(placed_blocks.items()):
        if block_id != "stone":
            continue
        sy = surface_map.get((x, z), 0)
        for ore_id, prob, max_rel_y in ore_table:
            if y <= sy + max_rel_y and rng.random() < prob:
                placed_blocks[(x, y, z)] = ore_id
                break


# API pública
def clear_world():
    """Remove todos os blocos, meshes e colisores do mundo."""
    for c in list(world_parent.children):
        destroy(c)
    placed_blocks.clear()
    _chunk_entities.clear()
    _colliders.clear()

def create_world(size: int = 16, max_height: int = 8):
    """
    Gera o mundo inteiro, popula placed_blocks e constrói as meshes por chunk.
    size  = raio em blocos a partir da origem (gera [-size, size) em X e Z).
    """
    clear_world()
    # 1 — Preenche placed_blocks com IDs de bloco
    surface_map: dict[tuple, int] = {}
    for x in range(-size, size):
        for z in range(-size, size):
            h = get_height(x, z)
            surface_map[(x, z)] = h
            for y in range(WORLD_BOTTOM, h + 1):
                placed_blocks[(x, y, z)] = _block_id_for_layer(y, h)

    # 1.5 Gera árvores e minérios sobre o terreno base
    world_seed = noise.seed if hasattr(noise, "seed") else 42
    _generate_trees(surface_map, world_seed)
    _generate_ores(surface_map, world_seed)

    # 2 — Determina chunks envolvidos
    chunk_set: set[tuple] = set()
    for (x, y, z) in placed_blocks:
        cx = x // CHUNK_SIZE
        cz = z // CHUNK_SIZE
        chunk_set.add((cx, cz))

    # 3 — Constrói mesh por chunk
    for (cx, cz) in chunk_set:
        entity = _build_chunk_mesh(cx, cz)
        _chunk_entities[(cx, cz)] = entity

    _spawn_all_colliders()
    
    return get_top_y(0, 0)

def get_top_y(x: int, z: int) -> int:
    """Altura do bloco mais alto na coluna (x, z)."""
    column = [by for (bx, by, bz) in placed_blocks if bx == x and bz == z]
    return max(column) if column else get_height(x, z)

def set_light_level(level: float):
    """
    Ajusta o brilho de todas as malhas do mundo (0 a 1).
    A Ursina desliga a herança de cor entre entidades, então a cor é aplicada em cada malha.
    """
    global _light_level
    if abs(level - _light_level) < 0.005:
        return
    _light_level = level
    light = color.Color(level, level, level, 1)
    for chunk in _chunk_entities.values():
        for mesh_entity in chunk.children:
            mesh_entity.color = light

def get_block_at(pos: tuple) -> str | None:
    """ID do bloco na posição (x, y, z), ou None se estiver vazia."""
    return placed_blocks.get((int(pos[0]), int(pos[1]), int(pos[2])))

def break_block(pos: tuple) -> bool:
    """
    Remove o bloco na posição (x, y, z) do mundo.
    Reconstrói o chunk afetado. Retorna True se o bloco existia.
    """
    x, y, z = int(pos[0]), int(pos[1]), int(pos[2])
    key = (x, y, z)
    if key not in placed_blocks:
        return False
    del placed_blocks[key]
    rebuild_chunk_at(key)
    _update_colliders_around(key)
    return True
 
 
def place_block(pos: tuple, block_id: str) -> bool:
    """
    Coloca um bloco na posição (x, y, z) do mundo.
    Reconstrói o chunk afetado. Retorna True se a posição estava vazia.
    """
    x, y, z = int(pos[0]), int(pos[1]), int(pos[2])
    key = (x, y, z)
    if key in placed_blocks:
        return False
    if get_block(block_id) is None:
        return False
    placed_blocks[key] = block_id
    rebuild_chunk_at(key)
    _update_colliders_around(key)
    return True

def chunks_to_rebuild(world_pos: tuple) -> set:
    """
    Chunks afetados por uma edição em (x, y, z): o próprio chunk e, se o bloco
    estiver na borda, o chunk vizinho (cuja face encostada pode aparecer/sumir).
    """
    x, _, z = (int(v) for v in world_pos)
    cx, cz = x // CHUNK_SIZE, z // CHUNK_SIZE
    chunks = {(cx, cz)}
    lx, lz = x % CHUNK_SIZE, z % CHUNK_SIZE
    if lx == 0:
        chunks.add((cx - 1, cz))
    elif lx == CHUNK_SIZE - 1:
        chunks.add((cx + 1, cz))
    if lz == 0:
        chunks.add((cx, cz - 1))
    elif lz == CHUNK_SIZE - 1:
        chunks.add((cx, cz + 1))
    return chunks

def rebuild_chunk_at(world_pos: tuple):
    """Reconstrói o(s) chunk(s) afetado(s) por uma edição em (x, y, z)."""
    for key in chunks_to_rebuild(world_pos):
        if key in _chunk_entities:
            destroy(_chunk_entities[key])
        _chunk_entities[key] = _build_chunk_mesh(*key)