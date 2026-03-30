from ursina import Audio
import random
import os

# Função para carregar o caminho completo do arquivo
def load_sound(filename):
    return os.path.join('assets', 'sounds', filename)

BREAK_BLOCK_SOUND = load_sound("break_block.ogg")
PLACE_BLOCK_SOUND = load_sound("place_block.ogg")

STEP_SOUND = load_sound("step.ogg")
HIT_SOUNDS = [
    load_sound("hit1.ogg"),
    load_sound("hit2.ogg"),
    load_sound("hit3.ogg"),
]
JUMP_SOUND = load_sound("jump.ogg")

def play_sound(sound_file, volume=1.0, pitch_range=(1.0, 1.0)):
    """
    Toca um som com volume e pitch opcional.
    pitch_range: tuple(min_pitch, max_pitch) para variação aleatória.
    """
    pitch = random.uniform(pitch_range[0], pitch_range[1])
    return Audio(sound_file, autoplay=True, volume=volume, pitch=pitch)

def play_break_block():
    play_sound(BREAK_BLOCK_SOUND, volume=0.8, pitch_range=(0.9, 1.1))

def play_place_block():
    play_sound(PLACE_BLOCK_SOUND, volume=0.7, pitch_range=(0.95, 1.05))

def play_step():
    play_sound(STEP_SOUND, volume=0.5, pitch_range=(0.9, 1.1))

def play_hit():
    sound = random.choice(HIT_SOUNDS)
    play_sound(sound, volume=0.5, pitch_range=(0.9, 1.0))

def play_jump():
    play_sound(JUMP_SOUND, volume=0.6, pitch_range=(0.95, 1.05))