from ursina import *
from game.blocks import get_block
from perlin_noise import PerlinNoise

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
CHUNK_SIZE  = 16   # blocos por chunk (X e Z)
RENDER_DIST = 2    # chunks visíveis em cada direção a partir do jogador

noise = PerlinNoise(octaves=4)

world_parent  = Entity()
placed_blocks: dict[tuple, str] = {}   # (x,y,z) → block_id string
_chunk_entities: dict[tuple, Entity] = {}  # (cx,cz) → entity da mesh
_surface_colliders: list = []  

# ---------------------------------------------------------------------------
# Geração de altura
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Faces do cubo — direção, normal, vértices, UV, vizinho
# ---------------------------------------------------------------------------
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
        Vec3( _HALF, -_HALF,  _HALF),
        Vec3( _HALF,  _HALF,  _HALF),
        Vec3(-_HALF,  _HALF,  _HALF),
    ]),
    ("back",   ( 0,  0, -1), [
        Vec3( _HALF, -_HALF, -_HALF),
        Vec3(-_HALF, -_HALF, -_HALF),
        Vec3(-_HALF,  _HALF, -_HALF),
        Vec3( _HALF,  _HALF, -_HALF),
    ]),
    ("right",  ( 1,  0,  0), [
        Vec3( _HALF, -_HALF,  _HALF),
        Vec3( _HALF, -_HALF, -_HALF),
        Vec3( _HALF,  _HALF, -_HALF),
        Vec3( _HALF,  _HALF,  _HALF),
    ]),
    ("left",   (-1,  0,  0), [
        Vec3(-_HALF, -_HALF, -_HALF),
        Vec3(-_HALF, -_HALF,  _HALF),
        Vec3(-_HALF,  _HALF,  _HALF),
        Vec3(-_HALF,  _HALF, -_HALF),
    ]),
]

# UV de um quad inteiro
_QUAD_UVS = [
    Vec2(0, 0),
    Vec2(1, 0),
    Vec2(1, 1),
    Vec2(0, 1),
]

# 2 triângulos por quad (índices dentro dos 4 vértices da face)
_QUAD_TRIS = [0, 1, 2, 2, 3, 0]

# ---------------------------------------------------------------------------
# Resolução de textura por face
# ---------------------------------------------------------------------------
def _face_texture(block, face_name: str):
    """Retorna a textura correta de acordo com o nome da face."""
    tex_map = block.textures          # dict com top/bottom/side
    if face_name == "top":
        return tex_map.get("top") or tex_map.get("side")
    elif face_name == "bottom":
        return tex_map.get("bottom") or tex_map.get("side")
    else:   # front / back / right / left  → side
        return tex_map.get("side") or tex_map.get("top")

# ---------------------------------------------------------------------------
# Construção de mesh por grupo de textura dentro de um chunk
# ---------------------------------------------------------------------------
def _build_chunk_mesh(cx: int, cz: int) -> Entity:
    """
    Constrói uma Entity por textura única dentro do chunk.
    Retorna um Entity-pai que agrupa todas as sub-meshes.
    """
    x0 = cx * CHUNK_SIZE
    z0 = cz * CHUNK_SIZE

    # Acumula vértices/UVs/triângulos separados por textura
    tex_buckets: dict = {}   # texture_object → {verts, uvs, tris}

    for x in range(x0, x0 + CHUNK_SIZE):
        for z in range(z0, z0 + CHUNK_SIZE):
            if (x, 0, z) not in placed_blocks:
                continue

            # Encontra todas as alturas ocupadas nessa coluna
            ys = [pos[1] for pos in placed_blocks if pos[0] == x and pos[2] == z]

            for y in ys:
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

                    bucket = tex_buckets.setdefault(tex, {"verts": [], "uvs": [], "tris": []})

                    base_idx = len(bucket["verts"])
                    for v, uv in zip(verts, _QUAD_UVS):
                        bucket["verts"].append(Vec3(v.x + x, v.y + y, v.z + z))
                        bucket["uvs"].append(uv)
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
            triangles=data["tris"],
            mode="triangle",
        )
        Entity(
            parent=parent_entity,
            model=mesh,
            texture=tex,
            color=color.white,
        )

    # Colisão simplificada: um único box collider por chunk
    # (para interação precisa usa Voxel individual — ver nota abaixo)
    return parent_entity

# ---------------------------------------------------------------------------
# Voxel interativo (para raycasting de colocação/quebra de bloco)
# ---------------------------------------------------------------------------
class Voxel(Entity):
    """
    Entidade invisível usada apenas para colisão/raycast.
    A parte visual fica na mesh do chunk.
    """
    def __init__(self, position=(0, 0, 0), block_id: str = "stone"):
        block = get_block(block_id)
        if block is None:
            raise ValueError(f"Block '{block_id}' não encontrado.")
        super().__init__(
            parent=world_parent,
            position=position,
            model="cube",
            origin_y=0.5,
            color=color.clear,          # invisível — a mesh do chunk renderiza
            collider="box",
            visible=False,
        )
        self.block_id = block_id

def _spawn_surface_colliders():
    global _surface_colliders
 
    for col in _surface_colliders:
        destroy(col)
    _surface_colliders.clear()
 
    # Mapa de altura máxima por coluna (x, z)
    surface_map: dict[tuple, int] = {}
    for (x, y, z) in placed_blocks:
        key = (x, z)
        if key not in surface_map or y > surface_map[key]:
            surface_map[key] = y
 
    for (x, z), top_y in surface_map.items():
        # 3 camadas de topo: suporta desníveis e escadas naturais
        for dy in range(3):
            y = top_y - dy
            if (x, y, z) in placed_blocks:
                e = Entity(
                    parent=world_parent,
                    position=(x, y, z),
                    model="cube",
                    collider="box",
                    visible=False,
                    color=color.clear,
                )
                _surface_colliders.append(e)

# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------
def create_world(size: int = 16, max_height: int = 8):
    """
    Gera o mundo inteiro, popula placed_blocks e constrói as meshes por chunk.
    size  = raio em blocos a partir da origem (gera [-size, size) em X e Z).
    """
    global placed_blocks, _chunk_entities

    # Limpa tudo
    for c in list(world_parent.children):
        destroy(c)
    placed_blocks.clear()
    _chunk_entities.clear()
    _surface_colliders.clear()

    # 1 — Preenche placed_blocks com IDs de bloco
    for x in range(-size, size):
        for z in range(-size, size):
            h = get_height(x, z)
            for y in range(-2, h + 1):
                placed_blocks[(x, y, z)] = _block_id_for_layer(y, h)

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

    _spawn_surface_colliders()
    
    return get_height(0, 0)


def rebuild_chunk_at(world_pos: tuple):
    """Reconstrói o chunk que contém a posição (x, y, z). Útil ao quebrar/colocar blocos."""
    x, y, z = world_pos
    cx = int(x) // CHUNK_SIZE
    cz = int(z) // CHUNK_SIZE
    key = (cx, cz)
    if key in _chunk_entities:
        destroy(_chunk_entities[key])
    _chunk_entities[key] = _build_chunk_mesh(cx, cz)