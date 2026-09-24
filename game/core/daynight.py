import math

DAY_SKY = (0.53, 0.76, 1.0)
SUNSET_SKY = (0.98, 0.56, 0.33)
NIGHT_SKY = (0.02, 0.03, 0.08)

MIN_LIGHT = 0.22   # luz mínima à noite (o mundo não fica totalmente preto)

def _lerp(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(x + (y - x) * t for x, y in zip(a, b))

def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    t = min(1.0, max(0.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3 - 2 * t)

class DayNightCycle:
    """
    Relógio do dia, sem dependência da Ursina (testável).
    time_of_day vai de 0 a 1: 0 = meia-noite, 0.25 = nascer do sol,
    0.5 = meio-dia, 0.75 = pôr do sol.
    """

    def __init__(self, day_length: float = 600.0, start_time: float = 0.3):
        self.day_length = day_length   # segundos de um dia completo
        self.time_of_day = start_time % 1.0

    def tick(self, dt: float):
        self.time_of_day = (self.time_of_day + dt / self.day_length) % 1.0

    @property
    def sun_angle(self) -> float:
        """Ângulo do sol em radianos: 0 no horizonte leste, pi/2 no meio-dia."""
        return 2 * math.pi * (self.time_of_day - 0.25)

    @property
    def sun_height(self) -> float:
        """-1 à meia-noite, 0 no horizonte, 1 ao meio-dia."""
        return math.sin(self.sun_angle)

    @property
    def daylight(self) -> float:
        """0 à noite, 1 de dia, com transição suave perto do horizonte."""
        return _smoothstep(-0.15, 0.25, self.sun_height)

    @property
    def light_level(self) -> float:
        return MIN_LIGHT + (1 - MIN_LIGHT) * self.daylight

    @property
    def is_night(self) -> bool:
        return self.daylight < 0.5

    @property
    def sky_color(self) -> tuple:
        """Cor do céu (r, g, b) de 0 a 1, com tom alaranjado no nascer/pôr do sol."""
        base = _lerp(NIGHT_SKY, DAY_SKY, self.daylight)
        sunset = max(0.0, 1 - abs(self.sun_height) / 0.25) * 0.7
        return _lerp(base, SUNSET_SKY, sunset)