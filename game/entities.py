from assets.textures import entities as tex_module

ENTITY_TYPE_PASSIVE   = "passive"
ENTITY_TYPE_NEUTRAL   = "neutral"
ENTITY_TYPE_HOSTILE   = "hostile"

ENTITY_HEALTH = {
    'cow': 10, 'pig': 10, 'sheep': 8, 'chicken': 4,
    'horse_black': 15, 'horse_brown': 15, 'horse_chestnut': 15, 'horse_creamy': 15,
}

class EntityData:
    def __init__(self, name: str, texture, entity_type: str, health: int = 10, **attributes):
        self.name = name
        self.texture = texture
        self.type = entity_type
        self.health = ENTITY_HEALTH.get(name.lower(), health)
        self.attributes = attributes

ANIMALS = {
    "cow": EntityData("Cow", tex_module.entities["cow"], "animals"),
    "horse_black": EntityData("Horse Black", tex_module.entities["horse_black"], "animals"),
    "horse_brown": EntityData("Horse Brown", tex_module.entities["horse_brown"], "animals"),
    "horse_chestnut": EntityData("Horse Chestnut", tex_module.entities["horse_chestnut"], "animals"),
    "horse_creamy": EntityData("Horse Creamy", tex_module.entities["horse_creamy"], "animals"),
    "pig": EntityData("Pig", tex_module.entities["pig"], "animals"),
    "sheep": EntityData("Sheep", tex_module.entities["sheep"], "animals"),
}

ENTITIES = {}

def register_entity(id: str, entity: EntityData):
    ENTITIES[id] = entity

def load_all_entities():
    ENTITIES.clear()
    ENTITIES.update(ANIMALS)

    for id, entity in ANIMALS.items():
        register_entity(id, entity)

def get_entity(entity_id: str):
    """Retorna uma entidade pelo ID"""
    return ENTITIES.get(entity_id, None)