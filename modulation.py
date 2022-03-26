from math import cos, pi
import random

import arcade

from modulation_graphic import ModulationRenderer
from constants import Constants, TIMER


FREQUENCY_KNOB_ANGLES = [135, 90, 45, 0, -45]


def equation(x, peak, frequency):
    wave_in = 1 if 0 <= x <= frequency else 0
    return 0.5*peak*(-cos(2*pi*x/frequency)+1) * wave_in


class ModulationHandler:

    def __init__(self, window: arcade.Window):
        self.window = window

        # --- SPRITES --- #

        self.frequency_knob = arcade.Sprite(":resource:/graphics/Knob_96px.png", scale=0.25,
                                            center_x=689, center_y=240)
        self.frequency_case = arcade.Sprite(":resource:/graphics/Knob_Case_128px.png", scale=0.25,
                                            center_x=689, center_y=240)

        self.peak_knob = arcade.Sprite(":resource:/graphics/Knob_96px.png", scale=0.25,
                                       center_x=835, center_y=240)
        self.peak_case = arcade.Sprite(":resource:/graphics/Knob_Case_128px.png", scale=0.25,
                                       center_x=835, center_y=240)

        self.pulse_button = arcade.Sprite(":resource:/graphics/Button_32px.png", scale=0.25,
                                          center_x=649, center_y=149)
        self.pulse_case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                                        center_x=649, center_y=149)

        self.modulation_graphics = arcade.SpriteList()
        self.glow_graphics = arcade.SpriteList()
        self.modulation_graphics.extend([self.frequency_knob, self.peak_knob, self.frequency_case, self.peak_case,
                                         self.pulse_button, self.pulse_case])

        # --- GAMEPLAY ---

        self.frequency = 0
        self.peak = 1

        self.wave_shift = 0.0

        self.twin_waves: list[tuple[float, int, float, float]] = [(0, 0, 0, 0) for _ in range(5)]
        self.player_waves: list[tuple[float, int, float]] = [(0, 0, 0) for _ in range(17)]

        self.frequency_knob.angle = FREQUENCY_KNOB_ANGLES[self.frequency]

        self.wave_peak = 0

        # --- GRAPHICAL ---

        self.renderer = ModulationRenderer(self.window)

    def on_key_press(self, symbol):
        if symbol == arcade.key.LEFT:
            self.frequency = max(self.frequency - 1, 0)
            self.frequency_knob.angle = FREQUENCY_KNOB_ANGLES[self.frequency]
        elif symbol == arcade.key.RIGHT:
            self.frequency = min(self.frequency + 1, 4)
            self.frequency_knob.angle = FREQUENCY_KNOB_ANGLES[self.frequency]
        elif symbol == arcade.key.UP:
            self.peak = 1
            self.peak_knob.angle = 0
        elif symbol == arcade.key.DOWN:
            self.peak = -1
            self.peak_knob.angle = 90
        elif symbol == arcade.key.SPACE:
            if (self.player_waves[0][0] == 0 or
                    TIMER.local_time_since(self.player_waves[0][2]) >= Constants.FREQUENCIES[self.player_waves[0][1]]):
                self.modulation_graphics.remove(self.pulse_button)
                self.glow_graphics.append(self.pulse_button)
                self.player_waves.pop(-1)
                self.player_waves.insert(0, (self.peak, self.frequency, TIMER.local_time))

    def on_key_release(self, symbol):
        if symbol == arcade.key.SPACE:
            if self.pulse_button in self.glow_graphics:
                self.modulation_graphics.append(self.pulse_button)
                self.glow_graphics.remove(self.pulse_button)

    def on_draw(self):
        self.modulation_graphics.draw(pixelated=True)

    def on_glow_draw(self):
        if self.window.bloom.blur_count or TIMER.local_time % 0.5 > 0.25:
            self.glow_graphics.draw()

        self.renderer.draw()

        for index, wave in enumerate(self.twin_waves):
            freq = Constants.FREQUENCIES[wave[1]]
            i = (index - self.wave_shift)
            if 150*i < Constants.OSCILLOSCOPE_POS[0]+Constants.OSCILLOSCOPE_SIZE[0]/2:
                arcade.draw_point(7 + 50 * (3 * i + freq/2),
                                  Constants.OSCILLOSCOPE_POS[1] + wave[0] * Constants.OSCILLOSCOPE_SIZE[1] * 5 / 12,
                                  arcade.color.RED, 5)
                arcade.draw_point(7 + 150 * i, Constants.OSCILLOSCOPE_POS[1], arcade.color.RED, 5)
                arcade.draw_point(7 + 50 * (3 * i + freq), Constants.OSCILLOSCOPE_POS[1], arcade.color.RED, 5)

        player_color = [int(n*255) for n in Constants.PLAYER_COLOR]
        arcade.draw_point(7+50*3-Constants.FREQUENCIES[self.frequency]*25,
                          Constants.OSCILLOSCOPE_POS[1]+self.peak*Constants.OSCILLOSCOPE_SIZE[1]*5/12,
                          player_color, 5)
        arcade.draw_point(7+50*3, Constants.OSCILLOSCOPE_POS[1], player_color, 5)
        arcade.draw_point(7+50*3-Constants.FREQUENCIES[self.frequency]*50,
                          Constants.OSCILLOSCOPE_POS[1], player_color, 5)

        for wave in [n for n in self.player_waves if n[0]]:
            front_pos = TIMER.local_time_since(wave[-1])*3*Constants.WAVE_SPEED * 50 + 157
            freq = Constants.FREQUENCIES[wave[1]]
            peak = wave[0]
            arcade.draw_point(front_pos-freq*25, Constants.OSCILLOSCOPE_POS[1]+peak*Constants.OSCILLOSCOPE_SIZE[1]*5/12,
                              player_color, 5)
            arcade.draw_point(front_pos, Constants.OSCILLOSCOPE_POS[1], player_color, 5)
            arcade.draw_point(front_pos-freq*50, Constants.OSCILLOSCOPE_POS[1], player_color, 5)

    def on_update(self):
        self.wave_shift += TIMER.delta_local_time*Constants.WAVE_SPEED
        if self.wave_shift >= 1:
            self.wave_shift -= 1
            self.twin_waves.pop(0)
            self.twin_waves.append((random.randint(-1, 1), 2, 0, 0))

        if 0 <= self.wave_shift <= 5/6:
            twin_wave = 1
            t_x = (self.wave_shift + (1 / 6)) * 3
        else:
            twin_wave = 2
            t_x = (self.wave_shift - (5 / 6)) * 3

        t_peak = self.twin_waves[twin_wave][0]
        t_frequency = Constants.FREQUENCIES[self.twin_waves[twin_wave][1]]

        p_peak = 0
        p_frequency = Constants.FREQUENCIES[0]
        p_x = 0
        for wave in self.player_waves[:2]:
            if not wave[0]:
                break
            time_since = TIMER.local_time_since(wave[-1])
            p_frequency = Constants.FREQUENCIES[wave[1]]
            if (0.5+p_frequency) >= time_since*3*Constants.WAVE_SPEED >= 0.5:
                p_peak = wave[0]
                p_x = (time_since-0.5)*3*Constants.WAVE_SPEED
                break

        twin_height = equation(t_x, t_peak, t_frequency)
        player_height = equation(p_x, p_peak, p_frequency)

        total_height = twin_height + player_height
        if abs(total_height) > self.wave_peak and abs(twin_height) > 0:
            self.wave_peak = abs(total_height)

        if t_x > t_frequency:
            if self.wave_peak > 0.2:
                self.window.menu_manager.health_manager.damage()
            self.wave_peak = 0

        for wave in self.player_waves[::-1]:
            if TIMER.local_time_since(wave[-1]) > (8+Constants.FREQUENCIES[wave[1]])/3/Constants.WAVE_SPEED:
                self.player_waves.remove(wave)
                self.player_waves.append((0, 0, 0))
            else:
                break

        self.renderer.render(self.twin_waves, self.player_waves, (self.peak, Constants.FREQUENCIES[self.frequency]),
                             self.wave_shift)
