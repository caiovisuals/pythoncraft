import math

# Dimensões do jogador (iguais às do Minecraft)
PLAYER_WIDTH = 0.6
PLAYER_HEIGHT = 1.8          # em pé
PLAYER_SNEAK_HEIGHT = 1.5    # agachado
PLAYER_EYE_HEIGHT = 1.62
PLAYER_SNEAK_EYE_HEIGHT = 1.27

# Agachado, o jogador não desce de bordas mais altas que isso
SNEAK_EDGE_DROP = 0.6
SNEAK_EDGE_STEP = 0.05

# Folga para o jogador não ficar "encostado" exatamente na face do bloco
_SKIN = 1e-4
# Tolerância ao detectar sobreposição (menor que _SKIN, absorve erros de ponto flutuante)
_EPS = 1e-7
# Maior deslocamento por passo, para não atravessar blocos em quedas rápidas
_MAX_STEP = 0.45

def block_overlaps_player(block_pos, player_pos, width: float = PLAYER_WIDTH, height: float = PLAYER_HEIGHT) -> bool:
    """
    Verifica se um bloco ocupa o mesmo espaço que o jogador.
    Blocos são cubos 1x1x1 centrados na posição; o jogador é uma caixa
    com os pés em player_pos, largura `width` e altura `height`.
    """
    bx, by, bz = block_pos
    px, py, pz = player_pos
    reach = 0.5 + width / 2
    return (
        abs(bx - px) < reach
        and abs(bz - pz) < reach
        and by + 0.5 > py
        and by - 0.5 < py + height
    )

def _block_range(low: float, high: float) -> range:
    """Coordenadas inteiras dos blocos (centrados no inteiro) que tocam o intervalo aberto (low, high)."""
    return range(math.floor(low + 0.5 + _EPS), math.ceil(high - 0.5 - _EPS) + 1)

def overlapping_blocks(pos, width: float, height: float, is_solid) -> list:
    """Blocos sólidos que intersectam a caixa do jogador com os pés em `pos`."""
    px, py, pz = pos
    half = width / 2
    return [
        (x, y, z)
        for x in _block_range(px - half, px + half)
        for y in _block_range(py, py + height)
        for z in _block_range(pz - half, pz + half)
        if is_solid((x, y, z))
    ]

def collides(pos, width: float, height: float, is_solid) -> bool:
    return bool(overlapping_blocks(pos, width, height, is_solid))

def _move_axis(pos: list, axis: int, delta: float, width: float, height: float, is_solid) -> bool:
    """Move em um único eixo, parando na face do primeiro bloco. Retorna True se bateu."""
    if delta == 0:
        return False

    pos[axis] += delta
    blocks = overlapping_blocks(pos, width, height, is_solid)
    if not blocks:
        return False

    # Encosta na face do bloco mais próximo na direção do movimento
    if axis == 1:
        near, far = 0.0, height         # pés / topo da cabeça
    else:
        near, far = -width / 2, width / 2
    if delta > 0:
        face = min(b[axis] for b in blocks) - 0.5
        pos[axis] = face - far - _SKIN
    else:
        face = max(b[axis] for b in blocks) + 0.5
        pos[axis] = face - near + _SKIN
    return True

def _limit_at_edge(pos, axis: int, delta: float, width: float, height: float, is_solid) -> float:
    """
    Agachado (estilo Minecraft): reduz o movimento horizontal enquanto
    ele levaria o jogador para fora da borda do bloco em que está apoiado.
    """
    def has_ground(d):
        probe = list(pos)
        probe[axis] += d
        probe[1] -= SNEAK_EDGE_DROP
        return collides(probe, width, height, is_solid)

    while delta != 0 and not has_ground(delta):
        if abs(delta) <= SNEAK_EDGE_STEP:
            return 0.0
        delta -= math.copysign(SNEAK_EDGE_STEP, delta)
    return delta

def move_and_collide(pos, delta, width: float, height: float, is_solid, stop_at_edges: bool = False):
    """
    Move a caixa do jogador por `delta` resolvendo colisões com os blocos,
    um eixo por vez (Y, depois X e Z), como no Minecraft.

    `stop_at_edges` impede cair das bordas (usado ao agachar no chão).
    Retorna (nova_posição, colidiu) onde colidiu = [bateu_x, bateu_y, bateu_z].
    """
    pos = [float(pos[0]), float(pos[1]), float(pos[2])]
    hit = [False, False, False]

    # Divide movimentos grandes em passos menores para não atravessar blocos
    steps = max(1, math.ceil(max(abs(d) for d in delta) / _MAX_STEP))
    step = [d / steps for d in delta]

    for _ in range(steps):
        for axis in (1, 0, 2):
            d = step[axis]
            if hit[axis]:
                continue
            if stop_at_edges and axis != 1:
                d = _limit_at_edge(pos, axis, d, width, height, is_solid)
            if _move_axis(pos, axis, d, width, height, is_solid):
                hit[axis] = True

    return pos, hit