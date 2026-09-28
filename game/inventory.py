from typing import Callable, Optional
from ursina import *
import game.textures as textures
from game.blocks import get_block
from game.items import get_item
from game.core.container import (
    LEFT, RIGHT, Container, CraftingGrid, ItemStack, PlayerInventory, click, quick_move,
)

# Tamanho de 1 pixel das texturas de GUI no espaço da UI (altura da tela = 1)
HOTBAR_PIXEL = 0.0036
INVENTORY_PIXEL = 0.0045

HOTBAR_SIZE = 9
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

def get_display_name(item_id: Optional[str]) -> str:
    """Nome de um bloco ou item para mostrar ao jogador."""
    thing = get_block(item_id) or get_item(item_id) if item_id else None
    return thing.name if thing else (item_id or "")

def _shift_held() -> bool:
    return bool(held_keys["shift"] or held_keys["left shift"] or held_keys["right shift"])

def _control_held() -> bool:
    return bool(held_keys["control"] or held_keys["left control"] or held_keys["right control"])

class ItemIcon(Entity):
    """Ícone de um bloco/item com a quantidade no canto inferior direito."""

    def __init__(self, size: float, **kwargs):
        super().__init__(model="quad", scale=size, **kwargs)
        self.item_id = ""   # diferente de None para o primeiro set_item sempre aplicar
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
        amount = amount if item_id else 0
        if item_id == self.item_id and amount == self.amount:
            return  # nada mudou: evita trocar a textura a cada frame
        self.item_id = item_id
        self.amount = amount
        self.texture = get_icon_texture(item_id)
        self.visible = self.texture is not None
        self.amount_text.text = str(amount) if item_id and amount > 1 else ""

    def set_stack(self, stack: Optional[ItemStack]):
        if stack:
            self.set_item(stack.id, stack.count)
        else:
            self.set_item(None)

    def clear(self):
        self.set_item(None)

class Hotbar(Entity):
    """
    Hotbar usando as texturas gui/hotbar.png e gui/selected_item.png.
    Mostra os 9 primeiros slots do PlayerInventory, que é a fonte da verdade.
    """

    def __init__(self, inventory: PlayerInventory, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        px = HOTBAR_PIXEL
        self.inventory = inventory
        self._seen_version = -1

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
        self.refresh()

    @staticmethod
    def slot_x(index: int) -> float:
        # Cada slot tem 20px; o centro do primeiro fica a 11px da borda esquerda
        return HOTBAR_LEFT + (11 + 20 * index) * HOTBAR_PIXEL

    def refresh(self):
        for i, icon in enumerate(self.icons):
            icon.set_stack(self.inventory.get(i))
        self._seen_version = self.inventory.version

    def update(self):
        if self.inventory.version != self._seen_version:
            self.refresh()

    @property
    def items(self) -> list:
        return [stack.id if stack else None for stack in self.stacks_raw]

    @property
    def stacks_raw(self) -> list:
        return [self.inventory.get(i) for i in range(HOTBAR_SIZE)]

    @property
    def stacks(self) -> list:
        """Lista de (item_id, quantidade) de cada slot."""
        return [(stack.id, stack.count) if stack else (None, 0) for stack in self.stacks_raw]

    @property
    def selected_stack(self) -> Optional[ItemStack]:
        return self.inventory.get(self.selected)

    @property
    def selected_item(self) -> Optional[str]:
        stack = self.selected_stack
        return stack.id if stack else None

    def set_items(self, items: list):
        """Esvazia o inventário e coloca 1 de cada item na hotbar."""
        self.inventory.drain_all()
        for i, item_id in enumerate(items[:HOTBAR_SIZE]):
            if item_id:
                self.inventory.set(i, ItemStack(item_id, 1))
        self.refresh()

    def add_item(self, item_id: str, amount: int = 1) -> int:
        """Guarda o item no inventário (hotbar primeiro). Retorna o que sobrou."""
        left = self.inventory.add(item_id, amount)
        self.refresh()
        return left

    def consume_selected(self, amount: int = 1) -> bool:
        """Gasta itens do slot selecionado. Retorna False se não houver o suficiente."""
        stack = self.selected_stack
        if stack is None or stack.count < amount:
            return False
        self.inventory.remove_from(self.selected, amount)
        self.refresh()
        return True

    def take_selected(self, whole_stack: bool = False) -> Optional[ItemStack]:
        """Tira 1 item (ou a pilha toda) do slot selecionado, para jogar no chão."""
        stack = self.selected_stack
        if stack is None:
            return None
        taken = self.inventory.remove_from(self.selected, stack.count if whole_stack else 1)
        self.refresh()
        return taken

    def select(self, index: int):
        self.selected = index % HOTBAR_SIZE
        self.selector.x = self.slot_x(self.selected)

    def scroll(self, direction: int):
        self.select(self.selected - direction)

# Tipos de slot numa tela de contêiner
SLOT_INVENTORY = "inventory"   # inventário principal ou hotbar
SLOT_GRID = "grid"             # grade de crafting
SLOT_RESULT = "result"         # resultado do crafting (só dá para tirar)
SLOT_EQUIPMENT = "equipment"   # armadura e mão secundária

class SlotView:
    """Liga um ícone na tela a um slot de um Container."""

    def __init__(self, container: Container, index: int, icon: ItemIcon, kind: str, half_size: float):
        self.container = container
        self.index = index
        self.icon = icon
        self.kind = kind
        self.half_size = half_size

    @property
    def stack(self) -> Optional[ItemStack]:
        if self.kind == SLOT_RESULT:
            return self.container.result()
        return self.container.get(self.index)

class ContainerScreen(Entity):
    """
    Tela com slots de itens desenhada sobre uma textura de GUI de 176x166.
    Posições dos slots em pixels da textura (canto superior esquerdo da área 16x16).

    Controles (como no Minecraft):
    - clique esquerdo: pega/larga/junta/troca a pilha; arrastar e soltar em outro slot também funciona
    - clique direito: pega metade da pilha, ou larga um item só
    - Shift+clique: move a pilha entre hotbar e inventário (no resultado, crafta tudo)
    - clicar fora da janela joga a pilha do cursor no chão (direito: um item)
    - Q sobre um slot joga um item no chão (Ctrl+Q: a pilha toda)
    """

    TEX_W, TEX_H = 176, 166
    MAIN_SLOTS = [(8 + 18 * c, 84 + 18 * r) for r in range(3) for c in range(9)]
    HOTBAR_SLOTS = [(8 + 18 * c, 142) for c in range(9)]

    def __init__(self, inventory: PlayerInventory, texture_name: str, on_drop: Optional[Callable] = None, **kwargs):
        super().__init__(parent=camera.ui, enabled=False, **kwargs)
        px = INVENTORY_PIXEL
        self.inventory = inventory
        self.on_drop = on_drop       # on_drop(item_id, count): joga itens no chão
        self.grid: Optional[CraftingGrid] = None
        self.cursor: Optional[ItemStack] = None
        self.slots: list[SlotView] = []
        self._press_slot: Optional[SlotView] = None
        self._picked_on_press = False

        # Escurece o jogo atrás da tela
        self.shade = Entity(parent=self, model="quad", color=color.rgba(0, 0, 0, 0.45), scale=(4, 2), z=0.02)

        self.bg = Entity(
            parent=self,
            model="quad",
            texture=textures.gui[texture_name],
            scale=(self.TEX_W * px, self.TEX_H * px),
            z=0.01,
        )

        for i, (x, y) in enumerate(self.MAIN_SLOTS):
            self.add_slot(inventory, PlayerInventory.MAIN[i], x, y)
        for i, (x, y) in enumerate(self.HOTBAR_SLOTS):
            self.add_slot(inventory, PlayerInventory.HOTBAR[i], x, y)

        # Destaque branco translúcido sobre o slot com o mouse em cima
        self.highlight = Entity(parent=self, model="quad", color=color.rgba(1, 1, 1, 0.35), scale=16 * px, z=-0.03, enabled=False)

        # Pilha presa ao mouse e nome do item sob o mouse
        self.cursor_icon = ItemIcon(parent=self, size=16 * px, z=-0.05)
        self.tooltip = Text(parent=self, text="", scale=0.9, origin=(-0.5, -0.5), z=-0.06, background=True, enabled=False)

    # Montagem

    def slot_position(self, sx: float, sy: float) -> Vec3:
        px = INVENTORY_PIXEL
        cx, cy = sx + 8, sy + 8
        return Vec3((cx - self.TEX_W / 2) * px, (self.TEX_H / 2 - cy) * px, -0.02)

    def add_slot(self, container: Container, index: int, sx: float, sy: float, kind: str = SLOT_INVENTORY, size_px: int = 16) -> SlotView:
        """Cria um slot na posição (sx, sy) da textura. `size_px` é a área clicável (o slot de resultado é maior)."""
        icon = ItemIcon(parent=self, size=16 * INVENTORY_PIXEL, position=self.slot_position(sx, sy))
        view = SlotView(container, index, icon, kind, size_px / 2 * INVENTORY_PIXEL)
        self.slots.append(view)
        return view

    def add_crafting_grid(self, width: int, left: int, top: int, result: tuple):
        """Grade de crafting `width`x`width` a partir de (left, top) e slot de resultado em `result`."""
        self.grid = CraftingGrid(width, self.inventory.stack_limit)
        for r in range(width):
            for c in range(width):
                self.add_slot(self.grid, r * width + c, left + 18 * c, top + 18 * r, SLOT_GRID)
        rx, ry, size = result
        self.add_slot(self.grid, -1, rx, ry, SLOT_RESULT, size_px=size)

    # Abrir e fechar

    def open(self):
        self.enabled = True
        self.refresh()

    def close(self):
        """Devolve o cursor e a grade de crafting ao inventário; o que não couber cai no chão."""
        leftovers = []
        if self.cursor:
            leftovers.append(self.cursor)
            self.cursor = None
        if self.grid:
            leftovers += self.grid.drain()
        for stack in leftovers:
            left = self.inventory.add(stack.id, stack.count)
            if left:
                self._drop(stack.id, left)
        self._press_slot = None
        self.enabled = False

    # Estado e desenho

    def slot_under_mouse(self) -> Optional[SlotView]:
        mx, my = mouse.x, mouse.y
        for view in self.slots:
            p = view.icon.position
            if abs(mx - p.x) <= view.half_size and abs(my - p.y) <= view.half_size:
                return view
        return None

    def mouse_outside(self) -> bool:
        px = INVENTORY_PIXEL
        return abs(mouse.x) > self.TEX_W / 2 * px or abs(mouse.y) > self.TEX_H / 2 * px

    def refresh(self):
        for view in self.slots:
            view.icon.set_stack(view.stack)
        self.cursor_icon.set_stack(self.cursor)

    def update(self):
        self.refresh()
        self.cursor_icon.position = Vec3(mouse.x, mouse.y, -0.05)

        view = self.slot_under_mouse()
        if view is None:
            self.highlight.enabled = False
            self.tooltip.enabled = False
            return

        p = view.icon.position
        self.highlight.position = Vec3(p.x, p.y, -0.03)
        self.highlight.enabled = True

        stack = view.stack
        self.tooltip.enabled = bool(stack) and self.cursor is None
        if self.tooltip.enabled:
            if self.tooltip.text != get_display_name(stack.id):
                self.tooltip.text = get_display_name(stack.id)
                self.tooltip.create_background()
            self.tooltip.position = Vec3(mouse.x + 0.02, mouse.y + 0.02, -0.06)

    # Input

    def input(self, key):
        if key == "left mouse down":
            self._press(LEFT)
        elif key == "right mouse down":
            self._press(RIGHT)
        elif key == "left mouse up":
            self._release()
        elif key == "q":
            self._drop_hovered(whole_stack=_control_held())
        else:
            return
        self.refresh()

    def _press(self, button: str):
        view = self.slot_under_mouse()
        self._press_slot = view
        self._picked_on_press = False

        if view is None:
            if self.cursor and self.mouse_outside():
                amount = self.cursor.count if button == LEFT else 1
                self._drop(self.cursor.id, amount)
                left = self.cursor.count - amount
                self.cursor = self.cursor._replace(count=left) if left > 0 else None
            return

        if view.kind == SLOT_RESULT:
            if _shift_held():
                self.grid.craft_all(self.inventory, self._inventory_order_from_outside())
            else:
                self.cursor = self.grid.take_result(self.cursor)
            return

        if _shift_held() and self.cursor is None:
            self._quick_move(view)
            return

        had_cursor = self.cursor is not None
        self.cursor = click(view.container, view.index, self.cursor, button)
        self._picked_on_press = not had_cursor and self.cursor is not None

    def _release(self):
        """Arrastar e soltar: pegou a pilha num slot e soltou o botão em outro."""
        start, self._press_slot = self._press_slot, None
        if not self._picked_on_press or self.cursor is None:
            return
        view = self.slot_under_mouse()
        if view is None or view is start or view.kind == SLOT_RESULT:
            return
        self.cursor = click(view.container, view.index, self.cursor, LEFT)

    def _inventory_order_from_outside(self) -> list:
        """Ordem para guardar itens que vêm da grade/equipamento: inventário principal e depois hotbar."""
        return list(PlayerInventory.MAIN) + list(PlayerInventory.HOTBAR)

    def _quick_move(self, view: SlotView):
        if view.kind == SLOT_INVENTORY:
            target = PlayerInventory.MAIN if view.index in PlayerInventory.HOTBAR else PlayerInventory.HOTBAR
            quick_move(view.container, view.index, self.inventory, target)
        else:
            quick_move(view.container, view.index, self.inventory, self._inventory_order_from_outside())

    def _drop_hovered(self, whole_stack: bool):
        view = self.slot_under_mouse()
        if view is None or view.kind == SLOT_RESULT or self.cursor is not None:
            return
        stack = view.stack
        if stack is None:
            return
        taken = view.container.remove_from(view.index, stack.count if whole_stack else 1)
        if taken:
            self._drop(taken.id, taken.count)

    def _drop(self, item_id: str, count: int):
        if self.on_drop and count > 0:
            self.on_drop(item_id, count)

class InventoryScreen(ContainerScreen):
    """Inventário de sobrevivência (gui/container/survival-inventory.png) com crafting 2x2."""

    ARMOR_SLOTS = [(8, 8 + 18 * r) for r in range(4)]
    ARMOR_ICONS = ["slot_helmet", "slot_chestplate", "slot_leggings", "slot_boots"]
    OFFHAND_SLOT = (77, 62)

    def __init__(self, inventory: PlayerInventory, on_drop: Optional[Callable] = None, **kwargs):
        super().__init__(inventory, "survival_inventory", on_drop, **kwargs)
        px = INVENTORY_PIXEL

        for i, ((sx, sy), icon_name) in enumerate(zip(self.ARMOR_SLOTS, self.ARMOR_ICONS)):
            # Silhueta da peça de armadura no fundo do slot
            Entity(parent=self, model="quad", texture=textures.gui.get(icon_name), scale=16 * px, position=self.slot_position(sx, sy) + Vec3(0, 0, 0.005))
            self.add_slot(inventory.armor, i, sx, sy, SLOT_EQUIPMENT)
        self.add_slot(inventory.offhand, 0, *self.OFFHAND_SLOT, SLOT_EQUIPMENT)

        self.add_crafting_grid(2, left=98, top=18, result=(154, 28, 16))

class CraftingTableScreen(ContainerScreen):
    """Mesa de trabalho (gui/container/crafter.png) com crafting 3x3."""

    def __init__(self, inventory: PlayerInventory, on_drop: Optional[Callable] = None, **kwargs):
        super().__init__(inventory, "crafter", on_drop, **kwargs)
        # O slot de resultado da textura é uma caixa de 26px em (129, 30)
        self.add_crafting_grid(3, left=26, top=17, result=(134, 35, 26))