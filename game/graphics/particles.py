from ursina import Entity, color, Vec3, random, destroy, sequence, Func, time

class Particle(Entity):
    def __init__(self, position=(0,0,0), color=color.white, scale=0.1, velocity=(0,1,0), lifetime=1.0, gravity=False, **kwargs):
        super().__init__(
            parent=kwargs.get('parent', None),
            position=position,
            model='quad',  # simples quad para partícula
            color=color,
            scale=scale,
            billboard=True  # sempre de frente para a câmera
        )
        self.velocity = Vec3(*velocity)
        self.lifetime = lifetime
        self.gravity = gravity
        self.start_time = time.time()
    
    def update(self):
        dt = time.dt
        # movimento da partícula
        self.position += self.velocity * dt
        if self.gravity:
            self.velocity.y -= 9.81 * dt  # simula gravidade simples
        # destrói quando o tempo de vida acabar
        if time.time() - self.start_time > self.lifetime:
            destroy(self)

def spawn_particles(position, count=10, color=color.white, scale=0.1, spread=0.5, lifetime=1.0, gravity=False, parent=None):
    """Cria várias partículas com pequenas variações de velocidade"""
    for _ in range(count):
        velocity = Vec3(
            random.uniform(-spread, spread),
            random.uniform(0, spread),
            random.uniform(-spread, spread)
        )
        Particle(
            position=position,
            color=color,
            scale=random.uniform(scale*0.5, scale*1.5),
            velocity=velocity,
            lifetime=random.uniform(lifetime*0.8, lifetime*1.2),
            gravity=gravity,
            parent=parent
        )
