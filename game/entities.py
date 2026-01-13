from textures import entities as entity_textures

class EntityData:
    def __init__(self, name: str, texture, type: str):
        self.name = name
        self.texture = texture
        self.type = type

ANIMALS = {
    "cow": EntityData("Cow", entity_textures["cow"], "animals"),
    "horse_black": EntityData("Horse Black", entity_textures["horse_black"], "animals"),
    "horse_brown": EntityData("Horse Brown", entity_textures["horse_brown"], "animals"),
    "horse_chestnut": EntityData("Horse Chestnut", entity_textures["horse_chestnut"], "animals"),
    "horse_creamy": EntityData("Horse Creamy", entity_textures["horse_creamy"], "animals"),
    "pig": EntityData("Pig", entity_textures["pig"], "animals"),
    "sheep": EntityData("Sheep", entity_textures["sheep"], "animals"),
}

ENTITIES = {}

def load_all_entities():
    ENTITIES.clear()
    ENTITIES.update(ANIMALS)