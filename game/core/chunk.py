from ursina import Entity
from game.voxel import Voxel

CHUNK_SIZE = 16

class Chunk(Entity):
    def __init__(self, cx, cz, parent):
        super().__init__(parent=parent)
        self.cx = cx
        self.cz = cz
        self.build()

    def build(self):
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                Voxel(
                    position=(
                        self.cx * CHUNK_SIZE + x,
                        0,
                        self.cz * CHUNK_SIZE + z
                    ),
                    parent=self
                )