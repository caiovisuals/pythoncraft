from ursina import Button, destroy
from game.textures import T_GRASS

class Voxel(Button):
    def __init__(self, position, parent):
        super().__init__(
            parent=parent,
            position=position,
            model="cube",
            texture=T_GRASS,
            collider="box"
        )

    def input(self, key):
        if self.hovered and key == "left mouse down":
            destroy(self)