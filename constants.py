import time

import arcade
import arcade.gl.geometry as geo
import arcade.gl as gl


class Constants:

    SCREEN_SIZE: tuple[int, int] = (976, 480)
    OSCILLOSCOPE_SIZE: tuple[int, int] = (549, 299)
    OSCILLOSCOPE_POS: tuple[int, int] = (282, 252)
    MORSE_SIZE: tuple[int, int] = (549, 71)
    MORSE_POS: tuple[int, int] = (282, 438)
    FREQUENCIES: tuple[float, float, float, float, float] = (0.5, 1.0, 1.5, 2.0, 3.0)
    BASIC_GEO: gl.Geometry
    TEXTURE_PROG: gl.Program

    TWIN_COLOR: tuple[float, float, float] = [1.0, 0.0, 0.0]
    PLAYER_COLOR: tuple[float, float, float] = [0.2, 1.0, 0.0]

    WAVE_SPEED: float = 1/3

    EFFECTS = True
    SCREEN_GLOW = False


CONSTANTS = Constants()


class Timer:

    def __init__(self):
        self.global_time = 0
        self.local_time = 360
        self.time_step = 1
        self.delta_time = 0
        self.delta_local_time = 0
        self.run = True

    def begin(self):
        self.global_time = 0
        self.local_time = 360

    def update_time(self, delta_time):
        self.delta_time = delta_time
        self.global_time += self.delta_time
        self.delta_local_time = delta_time*self.time_step*self.run
        self.local_time += self.delta_local_time

    def get_global_time(self):
        return time.time() - self.global_time

    def set_time_step(self, new_step):
        self.time_step = new_step

    def pause(self):
        self.run = False

    def un_pause(self):
        self.run = True

    def local_time_since(self, start_time):
        return self.local_time - start_time

    def global_time_since(self, start_time):
        return self.global_time - start_time


TIMER = Timer()


class SoundPlayer:
    SOUNDS: dict[arcade.Sound] = {
        "hurt": None,
        "morse": None,
        "wave_down": None,
        "wave_up": None,
        "suggest": None,
        "pulse": None,
        "invalid": None,
        'level4': None,
        'level4_warn': None
    }

    def __init__(self):
        self.volume = 1.0

    def setup(self):
        for wave in SoundPlayer.SOUNDS:
            SoundPlayer.SOUNDS[wave] = arcade.load_sound(f":resource:/sounds/{wave}.wav", streaming=False)

    def change(self, volume):
        self.volume = min(max(0.0, volume), 1.0)

    def play_sound(self, name):
        sound: arcade.Sound = SOUNDS.SOUNDS.get(name)
        if sound is not None:
            return sound.play(self.volume)
        return None

    def stop_sound(self, name, player):
        if player is not None:
            SoundPlayer.SOUNDS[name].stop(player)
        return None


SOUNDS = SoundPlayer()


def init_constants(ctx: arcade.ArcadeContext):
    """
    Since some constants require the arcade context they must be created after initialisation.
    """

    Constants.BASIC_GEO = geo.quad_2d_fs()
    Constants.TEXTURE_PROG = ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                              fragment_shader=":resource:/shaders/texture_frag.glsl")
    SOUNDS.setup()

