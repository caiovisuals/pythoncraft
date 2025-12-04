from ursina.prefabs.first_person_controller import FirstPersonController

class PlayerController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 0.5
        self.speed = 5
        self.jump_height = 1.5
