from ursina import *
import game.textures as textures
from game.inventory import HOTBAR_PIXEL, HOTBAR_TOP, HOTBAR_LEFT, HOTBAR_WIDTH_PX

class HUD(Entity):
    """
    HUD do jogador em primeira pessoa.
    Exibe corações de vida (esquerda) e ícones de fome (direita),
    alinhados logo acima da hotbar.
    """

    MAX_HEARTS = 10   # 10 ícones = 20 HP (cada coração = 2 HP)
    MAX_HUNGER = 10   # 10 ícones = 20 fome
    ICON_PX = 9       # tamanho do ícone em pixels da GUI
    STEP_PX = 8       # distância entre ícones (se sobrepõem 1px)
    HUNGER_ICON = "mutton"

    def __init__(self, player_ref=None):
        super().__init__(parent=camera.ui, enabled=False)
        self.player_ref = player_ref

        px = HOTBAR_PIXEL
        self.icon_size = self.ICON_PX * px
        self.row_y = HOTBAR_TOP + (3 + self.ICON_PX / 2) * px

        self.vitals_group = Entity(parent=self)

        self.heart_fills: list[Entity] = []
        self.hunger_icons: list[Entity] = []

        self._build_hearts()
        self._build_hunger()

    # Construção dos ícones
    def _build_hearts(self):
        """Contorno + preenchimento (cheio/metade) da sprite sheet gui/heart.png."""
        px = HOTBAR_PIXEL

        for i in range(self.MAX_HEARTS):
            x = HOTBAR_LEFT + (self.ICON_PX / 2 + i * self.STEP_PX) * px
            Entity(
                parent=self.vitals_group,
                model="quad",
                texture=textures.gui["heart_container"],
                scale=self.icon_size,
                position=(x, self.row_y, 0),
            )
            fill = Entity(
                parent=self.vitals_group,
                model="quad",
                texture=textures.gui["heart_full"],
                scale=self.icon_size,
                position=(x, self.row_y, -0.01),
            )
            self.heart_fills.append(fill)

    def _build_hunger(self):
        """Ícones de fome, da direita para a esquerda, usando a textura de um alimento."""
        px = HOTBAR_PIXEL
        right = HOTBAR_LEFT + HOTBAR_WIDTH_PX * px
        for i in range(self.MAX_HUNGER):
            x = right - (self.ICON_PX / 2 + i * self.STEP_PX) * px
            icon = Entity(
                parent=self.vitals_group,
                model="quad",
                texture=textures.items.get(self.HUNGER_ICON),
                scale=self.icon_size,
                position=(x, self.row_y, -0.01),
            )
            self.hunger_icons.append(icon)

    # Atualização a cada frame
    def update(self):
        if not self.player_ref or not self.vitals_group.enabled:
            return

        self._refresh_hearts()
        self._refresh_hunger()

    def _refresh_hearts(self):
        health = self.player_ref.vitals.health
        for i, fill in enumerate(self.heart_fills):
            value = health - i * 2
            if value >= 2:
                fill.texture = textures.gui["heart_full"]
                fill.visible = True
            elif value == 1:
                fill.texture = textures.gui["heart_half"]
                fill.visible = True
            else:
                fill.visible = False

    def _refresh_hunger(self):
        hunger = self.player_ref.vitals.hunger
        for i, icon in enumerate(self.hunger_icons):
            value = hunger - i * 2
            if value >= 2:
                icon.color = color.white
            elif value == 1:
                icon.color = color.gray
            else:
                icon.color = color.rgba(0, 0, 0, 0.4)

    # Helpers públicos
    def attach_player(self, player_ref):
        """Liga o HUD a um novo PlayerController após re-spawn."""
        self.player_ref = player_ref

    def show(self, show_vitals: bool = True):
        self.enabled = True
        self.vitals_group.enabled = show_vitals

    def hide(self):
        self.enabled = False