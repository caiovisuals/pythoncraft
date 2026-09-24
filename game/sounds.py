from pathlib import Path
from typing import Optional
from ursina import Audio
import random

SOUNDS_DIR = Path("assets/sounds")

def load_sound(filename: str) -> Optional[str]:
    """Retorna o caminho do som, ou None (com aviso) se o arquivo não existir."""
    path = SOUNDS_DIR / filename
    if not path.is_file():
        print(f"[sounds] arquivo não encontrado: {path.as_posix()}")
        return None
    return path.as_posix()

BREAK_BLOCK_SOUND = load_sound("break_block.ogg")
PLACE_BLOCK_SOUND = load_sound("place_block.ogg")
STEP_SOUND = load_sound("step.ogg")
JUMP_SOUND = load_sound("jump.ogg")
HIT_SOUNDS = [
    sound for sound in (
        load_sound("damage/hit1.ogg"),
        load_sound("damage/hit2.ogg"),
        load_sound("damage/hit3.ogg"),
    ) if sound
]

def play_sound(sound_file: Optional[str], volume=1.0, pitch_range=(1.0, 1.0)):
    """
    Toca um som com volume e pitch opcional. Ignora sons ausentes.
    pitch_range: tuple(min_pitch, max_pitch) para variação aleatória.
    """
    pitch = random.uniform(pitch_range[0], pitch_range[1])
    return Audio(sound_file, autoplay=True, auto_destroy=True, volume=volume, pitch=pitch)

def play_break_block():
    play_sound(BREAK_BLOCK_SOUND, volume=0.8, pitch_range=(0.9, 1.1))

def play_place_block():
    play_sound(PLACE_BLOCK_SOUND, volume=0.7, pitch_range=(0.95, 1.05))

def play_step():
    play_sound(STEP_SOUND, volume=0.5, pitch_range=(0.9, 1.1))

def play_hit():
    if HIT_SOUNDS:
        play_sound(random.choice(HIT_SOUNDS), volume=0.5, pitch_range=(0.9, 1.0))

def play_jump():
    play_sound(JUMP_SOUND, volume=0.6, pitch_range=(0.95, 1.05))