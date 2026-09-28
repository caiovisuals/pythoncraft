from typing import Callable, Iterable, NamedTuple, Optional

from game.craft import check_craft

MAX_STACK = 64

LEFT = "left"
RIGHT = "right"

class ItemStack(NamedTuple):
    """Uma pilha de itens. Imutável: alterações criam uma pilha nova."""
    id: str
    count: int

def _with_count(stack: ItemStack, count: int) -> Optional[ItemStack]:
    """A mesma pilha com outra quantidade (None se zerar)."""
    return stack._replace(count=count) if count > 0 else None

class Container:
    """
    Slots de itens sem dependência da Ursina (testável).
    `stack_limit(item_id)` diz quantos itens cabem numa pilha daquele item e
    `accepts(index, item_id)` diz se um slot aceita um item (ex.: armadura).
    `version` muda a cada alteração, para a UI saber quando se redesenhar.
    """

    def __init__(
        self,
        size: int,
        stack_limit: Optional[Callable[[str], int]] = None,
        accepts: Optional[Callable[[int, str], bool]] = None,
    ):
        self.slots: list[Optional[ItemStack]] = [None] * size
        self.stack_limit = stack_limit or (lambda item_id: MAX_STACK)
        self._accepts = accepts
        self.version = 0

    def __len__(self) -> int:
        return len(self.slots)

    def get(self, index: int) -> Optional[ItemStack]:
        return self.slots[index]

    def set(self, index: int, stack: Optional[ItemStack]):
        if stack is not None and stack.count <= 0:
            stack = None
        self.slots[index] = stack
        self.version += 1

    def accepts(self, index: int, item_id: str) -> bool:
        return self._accepts(index, item_id) if self._accepts else True

    def clear(self):
        self.slots = [None] * len(self.slots)
        self.version += 1

    def drain(self) -> list[ItemStack]:
        """Esvazia o contêiner e retorna as pilhas que estavam nele."""
        stacks = [stack for stack in self.slots if stack]
        self.clear()
        return stacks

    def count(self, item_id: str) -> int:
        return sum(stack.count for stack in self.slots if stack and stack.id == item_id)

    def remove_from(self, index: int, amount: int = 1) -> Optional[ItemStack]:
        """Tira até `amount` itens do slot e retorna o que foi tirado."""
        stack = self.slots[index]
        if stack is None or amount <= 0:
            return None
        taken = min(amount, stack.count)
        self.set(index, _with_count(stack, stack.count - taken))
        return ItemStack(stack.id, taken)

    def space_for(self, item_id: str, indices: Optional[Iterable[int]] = None) -> int:
        """Quantos itens desse tipo ainda cabem nos slots indicados."""
        limit = self.stack_limit(item_id)
        space = 0
        for i in self._indices(indices):
            if not self.accepts(i, item_id):
                continue
            stack = self.slots[i]
            if stack is None:
                space += limit
            elif stack.id == item_id:
                space += max(0, limit - stack.count)
        return space

    def add(self, item_id: str, count: int = 1, indices: Optional[Iterable[int]] = None) -> int:
        """Completa as pilhas existentes e depois ocupa slots vazios. Retorna o que sobrou."""
        order = list(self._indices(indices))
        limit = self.stack_limit(item_id)

        for i in order:
            stack = self.slots[i]
            if count <= 0:
                break
            if stack and stack.id == item_id and stack.count < limit:
                added = min(count, limit - stack.count)
                self.set(i, _with_count(stack, stack.count + added))
                count -= added

        for i in order:
            if count <= 0:
                break
            if self.slots[i] is None and self.accepts(i, item_id):
                added = min(count, limit)
                self.set(i, ItemStack(item_id, added))
                count -= added

        return count

    def _indices(self, indices: Optional[Iterable[int]]) -> Iterable[int]:
        return range(len(self.slots)) if indices is None else indices

class PlayerInventory(Container):
    """
    Inventário do jogador: 36 slots, os 9 primeiros são a hotbar.
    Armadura e mão secundária ficam em contêineres próprios.
    """

    HOTBAR = range(0, 9)
    MAIN = range(9, 36)

    def __init__(self, stack_limit: Optional[Callable[[str], int]] = None):
        super().__init__(36, stack_limit)
        # Ainda não há itens de armadura, então os slots de armadura não aceitam nada
        self.armor = Container(4, lambda item_id: 1, accepts=lambda index, item_id: False)
        self.offhand = Container(1, stack_limit)

    def add(self, item_id: str, count: int = 1, indices: Optional[Iterable[int]] = None) -> int:
        # Hotbar primeiro, como no Minecraft
        return super().add(item_id, count, list(self.HOTBAR) + list(self.MAIN) if indices is None else indices)

    def drain_all(self) -> list[ItemStack]:
        """Esvazia inventário, armadura e mão secundária (usado ao morrer)."""
        return self.drain() + self.armor.drain() + self.offhand.drain()

class CraftingGrid(Container):
    """Grade de crafting quadrada (2x2 no inventário, 3x3 na mesa de trabalho)."""

    def __init__(self, width: int, stack_limit: Optional[Callable[[str], int]] = None):
        super().__init__(width * width, stack_limit)
        self.width = width

    def rows(self) -> list[list[Optional[str]]]:
        ids = [stack.id if stack else None for stack in self.slots]
        return [ids[r * self.width:(r + 1) * self.width] for r in range(self.width)]

    def result(self) -> Optional[ItemStack]:
        match = check_craft(self.rows())
        return ItemStack(*match) if match else None

    def _consume_ingredients(self):
        for i, stack in enumerate(self.slots):
            if stack:
                self.set(i, _with_count(stack, stack.count - 1))

    def take_result(self, cursor: Optional[ItemStack]) -> Optional[ItemStack]:
        """Pega o resultado com o cursor (clique no slot de resultado). Retorna o novo cursor."""
        result = self.result()
        if result is None:
            return cursor
        if cursor is None:
            self._consume_ingredients()
            return result
        if cursor.id == result.id and cursor.count + result.count <= self.stack_limit(result.id):
            self._consume_ingredients()
            return _with_count(cursor, cursor.count + result.count)
        return cursor

    def craft_all(self, target: Container, indices: Optional[Iterable[int]] = None) -> int:
        """Crafta o máximo possível direto para `target` (Shift+clique). Retorna quantas vezes craftou."""
        indices = None if indices is None else list(indices)
        crafted = 0
        for _ in range(MAX_STACK):
            result = self.result()
            if result is None or target.space_for(result.id, indices) < result.count:
                break
            target.add(result.id, result.count, indices)
            self._consume_ingredients()
            crafted += 1
        return crafted

def click(container: Container, index: int, cursor: Optional[ItemStack], button: str = LEFT) -> Optional[ItemStack]:
    """
    Clique num slot com `cursor` sendo a pilha presa ao mouse. Retorna o novo cursor.
    Esquerdo: pega a pilha, larga tudo, junta com a do slot ou troca.
    Direito: pega metade, ou larga um item só.
    """
    slot = container.get(index)

    if cursor is None:
        if slot is None:
            return None
        if button == RIGHT:
            half = (slot.count + 1) // 2
            container.set(index, _with_count(slot, slot.count - half))
            return ItemStack(slot.id, half)
        container.set(index, None)
        return slot

    if not container.accepts(index, cursor.id):
        return cursor

    limit = container.stack_limit(cursor.id)
    amount = 1 if button == RIGHT else cursor.count

    if slot is None:
        placed = min(amount, limit)
        container.set(index, ItemStack(cursor.id, placed))
        return _with_count(cursor, cursor.count - placed)

    if slot.id == cursor.id:
        placed = min(amount, limit - slot.count)
        if placed <= 0:
            return cursor
        container.set(index, _with_count(slot, slot.count + placed))
        return _with_count(cursor, cursor.count - placed)

    # Itens diferentes: troca o cursor com o slot
    if cursor.count > limit:
        return cursor
    container.set(index, cursor)
    return slot

def quick_move(source: Container, index: int, target: Container, indices: Optional[Iterable[int]] = None) -> bool:
    """Move a pilha do slot para `target` (Shift+clique). O que não couber fica no slot."""
    stack = source.get(index)
    if stack is None:
        return False
    left = target.add(stack.id, stack.count, indices)
    if left == stack.count:
        return False
    source.set(index, _with_count(stack, left))
    return True