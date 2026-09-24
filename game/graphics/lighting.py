import math
from typing import Callable
from ursina import Entity, camera, color, scene, time, window, Vec3
from game.core.daynight import DayNightCycle

SKY_DISTANCE = 80   # distância do sol/lua até a câmera
FOG_RANGE = (22, 45)  # neblina linear: começa e termina (esconde a borda do mundo)

class DayNightLighting(Entity):
    """
    Aplica o ciclo dia/noite na cena: cor do céu, neblina, brilho do mundo e sol/lua.
    Só avança o relógio enquanto estiver habilitado (desabilite ao pausar).
    """

    def __init__(self, set_world_light: Callable[[float], None], cycle: DayNightCycle = None, **kwargs):
        super().__init__(**kwargs)
        self.set_world_light = set_world_light  # ajusta o brilho das malhas do mundo
        self.cycle = cycle or DayNightCycle()

        self.sun = Entity(model="quad", color=color.rgb32(255, 236, 140), scale=9, double_sided=True)
        self.moon = Entity(model="quad", color=color.rgb32(220, 225, 240), scale=6, double_sided=True)
        for body in (self.sun, self.moon):
            body.setFogOff()
            body.setBin("background", 0)
            body.setDepthWrite(False)

        scene.fog_density = FOG_RANGE
        self.apply()

    def update(self):
        self.cycle.tick(time.dt)
        self.apply()

    def apply(self):
        """Atualiza cena conforme a hora atual do ciclo."""
        self.set_world_light(self.cycle.light_level)

        sky = color.rgb(*self.cycle.sky_color)
        window.color = sky
        scene.fog_color = sky

        angle = self.cycle.sun_angle
        direction = Vec3(math.cos(angle), math.sin(angle), 0.25)
        center = camera.world_position
        self.sun.position = center + direction * SKY_DISTANCE
        self.moon.position = center - direction * SKY_DISTANCE
        self.sun.look_at(center)
        self.moon.look_at(center)

    def set_visible(self, visible: bool):
        self.sun.enabled = visible
        self.moon.enabled = visible
        scene.fog_density = FOG_RANGE if visible else 0