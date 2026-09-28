from typing import Optional

from game.blocks import get_block
from game.core.mining import break_time

class GameMode:
    """
    Regras de um modo de jogo. O main.py só pergunta ao modo o que fazer
    ao quebrar/colocar blocos e ao aplicar dano/fome.

    `hotbar` precisa ter: selected_item, consume_selected(n), set_items(ids).
    `vitals` é um game.core.vitals.Vitals.
    """

    id = ""
    name = ""
    uses_vitals = False           # vida/fome ativas e visíveis no HUD
    drops_items = False
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

    def block_drops(self, block_id: str) -> list[tuple[str, int]]:
        """Itens (id, quantidade) que caem no chão ao quebrar o bloco."""
        if not self.drops_items:
            return []
        block = get_block(block_id)
        drop = block.drop_id if block else None
        return [(drop, 1)] if drop else []

    def break_time(self, block, tool=None) -> float:
        """Segundos para quebrar `block` segurando `tool` (um Item ou None)."""
        if block is None:
            return 0.0
        attributes = tool.attributes if tool else {}
        return break_time(
            block.hardness,
            block_tool=block.tool,
            tool_type=attributes.get("tool_type"),
            tool_speed=attributes.get("mining_speed", 1.0),
        )

    # Vida e fome

    def tick_vitals(self, vitals, dt: float):
        if self.uses_vitals:
            vitals.tick(dt)

    def apply_damage(self, vitals, amount: int):
        if self.uses_vitals:
            vitals.damage(amount)

class CreativeMode(GameMode):
    """Blocos infinitos, quebra instantânea, sem drops, sem dano e sem fome."""

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

    def break_time(self, block, tool=None) -> float:
        return 0.0

class SurvivalMode(GameMode):
    """Começa sem nada: quebrar blocos dá itens e colocar blocos gasta itens."""

    id = "survival"
    name = "Survival"
    uses_vitals = True
    drops_items = True
    starting_hotbar = []

    def on_block_placed(self, hotbar):
        hotbar.consume_selected(1)

MODES = {mode.id: mode for mode in (CreativeMode(), SurvivalMode())}

def get_mode(mode_id: str) -> GameMode:
    return MODES[mode_id]