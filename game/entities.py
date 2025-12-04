from ursina import load_texture

class EntityData:
    def __init__(self, name, texture, type):
        self.name = name
        self.texture = texture
        self.type = type


def load_entity_texture(path):
    return load_texture(f"assets/textures/entities/{path}")

T_COW     = load_entity_texture("cow/cow.png")
T_HORSE     = load_entity_texture("horse/horse.png")
T_PIG     = load_entity_texture("pig/pig.png")
T_SHEEP     = load_entity_texture("sheep/sheep.png")

ANIMALS = {
    "cow": EntityData("Cow", T_COW, "animals"),
    "horse": EntityData("Horse", T_HORSE, "animals"),
    "pig": EntityData("Pig", T_PIG, "animals"),
    "sheep": EntityData("Sheep", T_SHEEP, "animals"),
}

ENTITIES = {}

def load_all_entities():
    ENTITIES.clear()
    ENTITIES.update(ANIMALS)

