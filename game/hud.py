from ursina import *
import game.textures as textures

class HUD(Entity):
    """
    HUD do jogador em primeira pessoa.
    Exibe corações de vida (esquerda) e ícones de fome (direita),
    alinhados logo acima da hotbar.
    """

    MAX_HEARTS = 10   # 10 ícones = 20 HP (cada coração = 2 HP)
    MAX_HUNGER = 10   # 10 ícones = 20 fome
    ICON_SCALE = 0.032
    ICON_GAP   = 0.037
    ROW_Y      = -0.40   # altura vertical no espaço da UI

    def __init__(self, player_ref=None):
        super().__init__(parent=camera.ui, enabled=False)
        self.player_ref = player_ref

        self.hearts       : list[Entity] = []
        self.hunger_icons : list[Entity] = []

        self._build_hearts()
        self._build_hunger()

    # Construção dos ícones

    def _build_hearts(self):
        """Cria os ícones de coração (lado esquerdo da tela)."""
        start_x = -0.46

        for i in range(self.MAX_HEARTS):
            icon = Entity(
                parent=self,
                model="quad",
                texture=textures.T_HEART,
                scale=(self.ICON_SCALE, self.ICON_SCALE),
                position=(start_x + i * self.ICON_GAP, self.ROW_Y),
                color=color.red,
            )
            self.hearts.append(icon)

    def _build_hunger(self):
        """
        Cria os ícones de fome (lado direito da tela, espelhado).
        Enquanto não houver textura de fome, usa o coração em laranja.
        """
        start_x = 0.46

        for i in range(self.MAX_HUNGER):
            icon = Entity(
                parent=self,
                model="quad",
                texture=textures.T_HEART,   # substituir por T_HUNGER quando existir
                scale=(self.ICON_SCALE, self.ICON_SCALE),
                position=(start_x - i * self.ICON_GAP, self.ROW_Y),
                color=color.orange,
            )
            self.hunger_icons.append(icon)

    # Atualização a cada frame

    def update(self):
        if not self.enabled or not self.player_ref:
            return

        self._refresh_hearts()
        self._refresh_hunger()

    def _refresh_hearts(self):
        """Atualiza opacidade dos corações conforme o HP atual."""
        hp         = self.player_ref.health
        hp_max     = self.player_ref.max_health
        filled     = round((hp / hp_max) * self.MAX_HEARTS)

        for i, heart in enumerate(self.hearts):
            if i < filled:
                heart.color = color.red
                heart.alpha = 1.0
            else:
                heart.color = color.gray
                heart.alpha = 0.35

    def _refresh_hunger(self):
        """Atualiza opacidade dos ícones de fome conforme a fome atual."""
        hunger     = self.player_ref.hunger
        hunger_max = self.player_ref.max_hunger
        filled     = round((hunger / hunger_max) * self.MAX_HUNGER)

        for i, icon in enumerate(self.hunger_icons):
            if i < filled:
                icon.color = color.orange
                icon.alpha = 1.0
            else:
                icon.color = color.gray
                icon.alpha = 0.35

    # Helpers públicos
    
    def attach_player(self, player_ref):
        """Liga o HUD a um novo PlayerController após re-spawn."""
        self.player_ref = player_ref

    def show(self):
        self.enabled = True

    def hide(self):
        self.enabled = False