from typing import Optional
from ursina import *
import game.textures as textures
from game.blocks import get_block
from game.items import get_item

# Tamanho de 1 pixel das texturas de GUI no espaço da UI (altura da tela = 1)
HOTBAR_PIXEL = 0.0036
INVENTORY_PIXEL = 0.0045

HOTBAR_SIZE = 9
MAX_STACK = 64
HOTBAR_WIDTH_PX = 182
HOTBAR_HEIGHT_PX = 22

# Centro vertical da hotbar, com 2px de margem da borda inferior
HOTBAR_Y = -0.5 + (HOTBAR_HEIGHT_PX / 2 + 2) * HOTBAR_PIXEL
HOTBAR_TOP = HOTBAR_Y + HOTBAR_HEIGHT_PX / 2 * HOTBAR_PIXEL
HOTBAR_LEFT = -HOTBAR_WIDTH_PX / 2 * HOTBAR_PIXEL

def get_icon_texture(item_id: Optional[str]):
    """Textura usada como ícone de um bloco ou item."""
    if not item_id:
        return None
    block = get_block(item_id)
    if block:
        return block.textures.get("side") or block.textures.get("top")
    item = get_item(item_id)
    if item:
        return item.texture
    return None

class ItemIcon(Entity):
    """Ícone de um bloco/item com a quantidade no canto inferior direito."""

    def __init__(self, size: float, **kwargs):
        super().__init__(model="quad", scale=size, **kwargs)
        self.item_id = None
        self.amount = 0
        self.amount_text = Text(
            parent=self,
            text="",
            origin=(0.5, -0.5),
            position=(0.5, -0.5, -0.01),
            scale=6,
        )
        self.set_item(None)

    def set_item(self, item_id: Optional[str], amount: int = 1):
        self.item_id = item_id
        self.amount = amount if item_id else 0
        self.texture = get_icon_texture(item_id)
        self.visible = self.texture is not None
        self.amount_text.text = str(amount) if item_id and amount > 1 else ""

    def clear(self):
        self.set_item(None)

class Hotbar(Entity):
    """Hotbar usando as texturas gui/hotbar.png e gui/selected_item.png."""

    def __init__(self, items: Optional[list] = None, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        px = HOTBAR_PIXEL

        self.bg = Entity(
            parent=self,
            model="quad",
            texture=textures.gui["hotbar"],
            scale=(HOTBAR_WIDTH_PX * px, HOTBAR_HEIGHT_PX * px),
            y=HOTBAR_Y,
        )

        self.icons: list[ItemIcon] = []
        for i in range(HOTBAR_SIZE):
            icon = ItemIcon(
                parent=self,
                size=16 * px,
                position=(self.slot_x(i), HOTBAR_Y, -0.02),
            )
            self.icons.append(icon)

        self.selector = Entity(
            parent=self,
            model="quad",
            texture=textures.gui["selected_item"],
            scale=(24 * px, 22 * px),
            position=(self.slot_x(0), HOTBAR_Y, -0.01),
        )

        self.selected = 0
        self.set_items(items or [])

    @staticmethod
    def slot_x(index: int) -> float:
        # Cada slot tem 20px; o centro do primeiro fica a 11px da borda esquerda
        return HOTBAR_LEFT + (11 + 20 * index) * HOTBAR_PIXEL

    @property
    def items(self) -> list:
        return [icon.item_id for icon in self.icons]

    @property
    def stacks(self) -> list:
        """Lista de (item_id, quantidade) de cada slot."""
        return [(icon.item_id, icon.amount) for icon in self.icons]

    @property
    def selected_item(self) -> Optional[str]:
        return self.icons[self.selected].item_id

    def set_items(self, items: list):
        for i, icon in enumerate(self.icons):
            icon.set_item(items[i] if i < len(items) else None)

    def add_item(self, item_id: str, amount: int = 1) -> int:
        """Empilha o item nos slots existentes e depois nos vazios. Retorna o que sobrou."""
        for icon in self.icons:
            if amount <= 0:
                break
            if icon.item_id == item_id and icon.amount < MAX_STACK:
                added = min(amount, MAX_STACK - icon.amount)
                icon.set_item(item_id, icon.amount + added)
                amount -= added
        for icon in self.icons:
            if amount <= 0:
                break
            if icon.item_id is None:
                added = min(amount, MAX_STACK)
                icon.set_item(item_id, added)
                amount -= added
        return amount

    def consume_selected(self, amount: int = 1) -> bool:
        """Gasta itens do slot selecionado. Retorna False se não houver o suficiente."""
        icon = self.icons[self.selected]
        if icon.item_id is None or icon.amount < amount:
            return False
        remaining = icon.amount - amount
        icon.set_item(icon.item_id if remaining > 0 else None, remaining)
        return True

    def select(self, index: int):
        self.selected = index % HOTBAR_SIZE
        self.selector.x = self.slot_x(self.selected)

    def scroll(self, direction: int):
        self.select(self.selected - direction)

class InventoryScreen(Entity):
    """
    Tela de inventário de sobrevivência (gui/container/survival-inventory.png).
    Posições dos slots em pixels da textura 176x166 (canto superior esquerdo da área 16x16).
    """

    TEX_W, TEX_H = 176, 166

    ARMOR_SLOTS = [(8, 8 + 18 * r) for r in range(4)]
    ARMOR_ICONS = ["slot_helmet", "slot_chestplate", "slot_leggings", "slot_boots"]
    OFFHAND_SLOT = (77, 62)
    CRAFT_SLOTS = [(98 + 18 * c, 18 + 18 * r) for r in range(2) for c in range(2)]
    CRAFT_RESULT_SLOT = (154, 28)
    MAIN_SLOTS = [(8 + 18 * c, 84 + 18 * r) for r in range(3) for c in range(9)]
    HOTBAR_SLOTS = [(8 + 18 * c, 142) for c in range(9)]

    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=False, **kwargs)
        px = INVENTORY_PIXEL

        # Escurece o jogo atrás do inventário
        self.shade = Entity(parent=self, model="quad", color=color.rgba(0, 0, 0, 0.45), scale=(4, 2), z=0.02)

        self.bg = Entity(
            parent=self,
            model="quad",
            texture=textures.gui["survival_inventory"],
            scale=(self.TEX_W * px, self.TEX_H * px),
            z=0.01,
        )

        for (sx, sy), icon_name in zip(self.ARMOR_SLOTS, self.ARMOR_ICONS):
            Entity(
                parent=self,
                model="quad",
                texture=textures.gui.get(icon_name),
                scale=16 * px,
                position=self._slot_position(sx, sy),
            )

        self.armor = [self._make_slot(x, y) for x, y in self.ARMOR_SLOTS]
        self.offhand = self._make_slot(*self.OFFHAND_SLOT)
        self.craft = [self._make_slot(x, y) for x, y in self.CRAFT_SLOTS]
        self.craft_result = self._make_slot(*self.CRAFT_RESULT_SLOT)
        self.main = [self._make_slot(x, y) for x, y in self.MAIN_SLOTS]
        self.hotbar = [self._make_slot(x, y) for x, y in self.HOTBAR_SLOTS]

        self.all_slots = self.armor + [self.offhand] + self.craft + [self.craft_result] + self.main + self.hotbar

        # Destaque branco translúcido sobre o slot com o mouse em cima
        self.highlight = Entity(
            parent=self,
            model="quad",
            color=color.rgba(1, 1, 1, 0.35),
            scale=16 * px,
            z=-0.03,
            enabled=False,
        )

    def _slot_position(self, sx: int, sy: int) -> Vec3:
        px = INVENTORY_PIXEL
        cx, cy = sx + 8, sy + 8
        return Vec3((cx - self.TEX_W / 2) * px, (self.TEX_H / 2 - cy) * px, -0.02)

    def _make_slot(self, sx: int, sy: int) -> ItemIcon:
        icon = ItemIcon(parent=self, size=16 * INVENTORY_PIXEL, position=self._slot_position(sx, sy))
        icon.slot_position = icon.position
        return icon

    def sync_hotbar(self, stacks: list):
        for i, slot in enumerate(self.hotbar):
            item_id, amount = stacks[i] if i < len(stacks) else (None, 0)
            slot.set_item(item_id, amount)

    def update(self):
        # Converte a posição do mouse para o espaço local da tela e acha o slot sob ele
        half = 8 * INVENTORY_PIXEL
        mx, my = mouse.x, mouse.y
        for slot in self.all_slots:
            p = slot.slot_position
            if abs(mx - p.x) <= half and abs(my - p.y) <= half:
                self.highlight.position = Vec3(p.x, p.y, -0.03)
                self.highlight.enabled = True
                return
        self.highlight.enabled = False