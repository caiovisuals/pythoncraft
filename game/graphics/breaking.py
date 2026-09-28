from ursina import *
import game.textures as textures

BAR_WIDTH = 0.08
BAR_HEIGHT = 0.008
BAR_Y = -0.04   # logo abaixo da mira

class BreakingOverlay(Entity):
    """
    Mostra a quebra de um bloco: rachaduras num cubo levemente maior que o bloco
    e uma barra de progresso abaixo da mira.
    """

    def __init__(self):
        super().__init__(model="cube", scale=1.004, color=color.white, enabled=False)
        self._stage = -1

        self.bar_bg = Entity(
            parent=camera.ui,
            model="quad",
            color=color.rgba(0, 0, 0, 0.55),
            scale=(BAR_WIDTH, BAR_HEIGHT),
            y=BAR_Y,
            enabled=False,
        )
        self.bar_fill = Entity(
            parent=camera.ui,
            model="quad",
            origin=(-0.5, 0),
            color=color.rgb32(240, 240, 240),
            scale=(0, BAR_HEIGHT * 0.6),
            position=(-BAR_WIDTH / 2, BAR_Y, -0.01),
            enabled=False,
        )

    def show(self, block_pos: tuple, progress: float):
        stages = textures.breaking
        if stages:
            stage = min(len(stages) - 1, int(progress * len(stages)))
            if stage != self._stage:
                self._stage = stage
                self.texture = stages[stage]
        self.position = block_pos
        self.enabled = True

        self.bar_bg.enabled = True
        self.bar_fill.enabled = True
        self.bar_fill.scale_x = BAR_WIDTH * max(0.0, min(1.0, progress))

    def hide(self):
        if self.enabled:
            self.enabled = False
            self.bar_bg.enabled = False
            self.bar_fill.enabled = False
            self._stage = -1