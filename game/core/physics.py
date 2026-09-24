PLAYER_WIDTH = 0.6
PLAYER_HEIGHT = 1.8

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