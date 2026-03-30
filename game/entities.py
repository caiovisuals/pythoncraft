from game import textures as tex_module

ENTITY_TYPE_PASSIVE   = "passive"
ENTITY_TYPE_NEUTRAL   = "neutral"
ENTITY_TYPE_HOSTILE   = "hostile"

ENTITY_HEALTH = {
    "cow": 10, 
    "pig": 10, 
    "sheep": 8, 
    "horse_black": 15, 
    "horse_brown": 15, 
    "horse_chestnut": 15, 
    "horse_creamy": 15,
}

class EntityData:
    def __init__(self, name: str, texture, entity_type: str, health: int = 10, speed: float = 1.0, **attributes):
        self.name = name
        self.texture = texture
        self.type = entity_type
        self.health = ENTITY_HEALTH.get(name.lower(), health)
        self.speed = speed
        self.attributes = attributes

    def __repr__(self):
        return f"<Entity {self.name} | HP:{self.health} | Speed:{self.speed}>"

ANIMALS = {
    "cow": EntityData("Cow", "cow", ENTITY_TYPE_PASSIVE, speed=0.6),
    "horse_black": EntityData("Horse Black", "horse_black", ENTITY_TYPE_PASSIVE, speed=0.8),
    "horse_brown": EntityData("Horse Brown", "horse_brown", ENTITY_TYPE_PASSIVE, speed=0.8),
    "horse_chestnut": EntityData("Horse Chestnut", "horse_chestnut", ENTITY_TYPE_PASSIVE, speed=0.8),
    "horse_creamy": EntityData("Horse Creamy", "horse_creamy", ENTITY_TYPE_PASSIVE, speed=0.8),
    "pig": EntityData("Pig", "pig", ENTITY_TYPE_PASSIVE, speed=0.6),
    "sheep": EntityData("Sheep", "sheep", ENTITY_TYPE_PASSIVE, speed=0.4),
}

ENTITIES: dict[str, EntityData] = {}

def register_entity(id: str, entity: EntityData):
    ENTITIES[id] = entity

def load_all_entities():
    ENTITIES.clear()

    for id, entity in ANIMALS.items():
        texture_id = entity.texture
        entity.texture = tex_module.entities[texture_id]
        
        register_entity(id, entity)

def get_entity(entity_id: str):
    """Retorna uma entidade pelo ID"""
    return ENTITIES.get(entity_id, None)