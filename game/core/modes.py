from typing import Optional

from game.blocks import get_block

class GameMode:
    """
    Regras de um modo de jogo. O main.py só pergunta ao modo o que fazer
    ao quebrar/colocar blocos e ao aplicar dano/fome.

    `hotbar` precisa ter: selected_item, add_item(id, n), consume_selected(n), set_items(ids).
    `vitals` é um game.core.vitals.Vitals.
    """

    id = ""
    name = ""
    uses_vitals = False           # vida/fome ativas e visíveis no HUD
    starting_hotbar: list = []

    def setup_hotbar(self, hotbar):
        hotbar.set_items(self.starting_hotbar)

    # Blocos

    def block_to_place(self, hotbar) -> Optional[str]:
        """Bloco que será colocado com o slot selecionado (None = não coloca nada)."""
        item_id = hotbar.selected_item
        if item_id and get_block(item_id):
            return item_id
        return None

    def on_block_placed(self, hotbar):
        pass

    def on_block_broken(self, block_id: str, hotbar):
        pass

    # Vida e fome

    def tick_vitals(self, vitals, dt: float):
        if self.uses_vitals:
            vitals.tick(dt)

    def apply_damage(self, vitals, amount: int):
        if self.uses_vitals:
            vitals.damage(amount)

class CreativeMode(GameMode):
    """Blocos infinitos, sem drops, sem dano e sem fome."""

    id = "creative"
    name = "Criativo"
    uses_vitals = False
    starting_hotbar = [
        "grass",
        "dirt",
        "stone",
        "cobblestone",
        "wood",
        "glass",
        "obsidian",
        "ice",
        "limestone",
    ]

class SurvivalMode(GameMode):
    """Começa sem nada: quebrar blocos dá itens e colocar blocos gasta itens."""

    id = "survival"
    name = "Survival"
    uses_vitals = True
    starting_hotbar = []

    def on_block_placed(self, hotbar):
        hotbar.consume_selected(1)

    def on_block_broken(self, block_id: str, hotbar):
        block = get_block(block_id)
        drop = block.drop_id if block else None
        if drop:
            hotbar.add_item(drop, 1)

MODES = {mode.id: mode for mode in (CreativeMode(), SurvivalMode())}

def get_mode(mode_id: str) -> GameMode:
    return MODES[mode_id]