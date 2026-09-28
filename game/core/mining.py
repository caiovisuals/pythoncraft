from typing import Optional

SECONDS_PER_HARDNESS = 0.75   # tempo para quebrar 1 de dureza com a mão
BREAK_COOLDOWN = 0.25         # pausa entre um bloco e o próximo ao segurar o clique

def break_time(hardness: float, block_tool: Optional[str] = None, tool_type: Optional[str] = None, tool_speed: float = 1.0) -> float:
    """
    Segundos para quebrar um bloco: dureza ÷ multiplicador da ferramenta.
    A ferramenta só acelera se for do tipo certo para o bloco (picareta em pedra, machado em madeira...).
    """
    if hardness <= 0:
        return 0.0
    speed = tool_speed if block_tool and tool_type == block_tool else 1.0
    return hardness * SECONDS_PER_HARDNESS / max(speed, 1e-6)

class MiningProgress:
    """
    Progresso de quebra do bloco mirado, sem dependência da Ursina (testável).
    Trocar de alvo reinicia o progresso; soltar o clique chama reset().
    """

    def __init__(self, cooldown: float = BREAK_COOLDOWN):
        self.cooldown = cooldown
        self.target = None
        self.duration = 0.0
        self.elapsed = 0.0
        self._cooldown_left = 0.0

    @property
    def progress(self) -> float:
        """0 a 1."""
        if self.target is None:
            return 0.0
        if self.duration <= 0:
            return 1.0
        return min(1.0, self.elapsed / self.duration)

    def reset(self):
        self.target = None
        self.elapsed = 0.0
        self.duration = 0.0

    def tick(self, dt: float, target, duration: float) -> bool:
        """Avança a quebra de `target`. Retorna True no frame em que o bloco quebra."""
        if self._cooldown_left > 0:
            self._cooldown_left = max(0.0, self._cooldown_left - dt)
            return False

        if target != self.target:
            self.target = target
            self.elapsed = 0.0
        self.duration = duration
        self.elapsed += dt

        if self.elapsed >= self.duration:
            self.reset()
            self._cooldown_left = self.cooldown
            return True
        return False