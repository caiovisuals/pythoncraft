from ursina import *

class InventorySlot(Button):
    def __init__(self, index, texture=None, amount=0, **kwargs):
        super().__init__(
            model='quad',
            texture=texture,
            scale=(0.08, 0.08),
            color=color.white,
            **kwargs
        )
        self.index = index
        self.amount = amount
        self.item_texture = texture
      
        self.amount_text = Text(
            text=str(amount) if amount > 1 else '',
            parent=self,
            scale=1,
            y=-0.03
        )

    def set_item(self, texture, amount=1):
        self.item_texture = texture
        self.texture = texture
        self.amount = amount
        self.amount_text.text = str(amount) if amount > 1 else ''

    def clear(self):
        self.item_texture = None
        self.texture = None
        self.amount = 0
        self.amount_text.text = ''


class Inventory(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)

        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.rgba(0, 0, 0, 150),
            scale=(0.95, 0.45),
            y=-0.3,
        )

        self.slots = []
        cols = 9
        rows = 3
        for r in range(rows):
            for c in range(cols):
                slot = InventorySlot(
                    index=r * cols + c,
                    parent=self,
                    x=-0.40 + c * 0.09,
                    y=-0.28 + r * 0.09
                )
                self.slots.append(slot)

        self.visible = False

    def toggle(self):
        self.visible = not self.visible
        self.enabled = self.visible
        mouse.locked = not self.visible

    def add_item(self, texture, amount=1):
        for slot in self.slots:
            if slot.item_texture == texture:
                slot.set_item(texture, slot.amount + amount)
                return
        
        for slot in self.slots:
            if slot.item_texture is None:
                slot.set_item(texture, amount)
                return


class Hotbar(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        self.bg = Entity(
            model='quad',
            parent=self,
            color=color.rgba(0, 0, 0, 170),
            y=-0.45,
            scale=(0.40, 0.08)
        )

        self.slots = []
        for i in range(9):
            slot = InventorySlot(
                index=i,
                parent=self,
                x=-0.18 + i * 0.045,
                y=-0.45
            )
            self.slots.append(slot)

        self.selected = 0
        self.update_selection()

    def update_selection(self):
        for i, slot in enumerate(self.slots):
            slot.color = color.azure if i == self.selected else color.white
