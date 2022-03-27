from math import cos, pi
import random

import arcade

from modulation_graphic import ModulationRenderer
from constants import Constants, TIMER, SOUNDS


FREQUENCY_KNOB_ANGLES = [135, 90, 45, 0, -45]

LEVEL_RAND = [([0], [0]), ([1], (-1, 0, 1)), ((1, 3, 4), (-1, 1, 1)),
              ((0, 1, 2, 3, 4), (-1, 1)), ((0, 1, 2, 3, 4), (-1, 1))]

LEVEL_DURATIONS = [10.0, 60.0, 90.0, 180.0, float('inf')]


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

        self.peak_sound = ('NONE', None)

        self.sad_counter = 0
        self.level = 0
        self.next_level = 1
        self.start_time = 0

        # --- GRAPHICAL ---

        self.renderer = ModulationRenderer(self.window)

    def on_key_press(self, symbol):
        if symbol == arcade.key.RIGHT:
            self.frequency = max(self.frequency - 1, 0)
            self.frequency_knob.angle = FREQUENCY_KNOB_ANGLES[self.frequency]
        elif symbol == arcade.key.LEFT:
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
                    TIMER.local_time_since(self.player_waves[0][2])*3*Constants.WAVE_SPEED >= Constants.FREQUENCIES[self.player_waves[0][1]]):
                self.modulation_graphics.remove(self.pulse_button)
                self.glow_graphics.append(self.pulse_button)
                self.player_waves.pop(-1)
                self.player_waves.insert(0, (self.peak, self.frequency, TIMER.local_time))
                SOUNDS.play_sound('pulse')
                if self.level == 0 and self.next_level == 4:
                    self.sad_counter += 1
                    if self.sad_counter == 1:
                        SOUNDS.play_sound('level4_warn')
                        self.window.morse_manager.morse_signals[1].override_message((0.0, '101101101001011010100100101100101010010001010001101100101011001010100110001101001101101100110001101010010100100'))
                    elif self.sad_counter == 2:
                        SOUNDS.play_sound('level4')
                        self.window.morse_manager.morse_signals[1].override_message((0.0, '10100010110011011000101010011011011001011010010110100110101101100'))
                        self.level = 4
                        self.next_level = 4
                        Constants.WAVE_SPEED = 1.5/3
            else:
                SOUNDS.play_sound('invalid')

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

    def on_update(self):
        if self.next_level == 4 and self.level == 0 and TIMER.local_time_since(self.start_time) > 20:
            if not self.window.win:
                self.window.win = True
                self.window.morse_manager.morse_signals[0].override_message((0.0, '0'))
                self.window.morse_manager.morse_signals[1].override_message((0.0, '1100101010100101100110100110101100011010110110011011011001010110001011011001000101100101101001000101011010010110100100100'))
            elif (self.window.win and self.window.morse_manager.morse_signals[1].playing == -1 and
                  self.window.morse_manager.morse_signals[0].playing == -1) and not self.window.finished:
                self.window.finished = True
                self.window.morse_manager.morse_signals[1].override_message((0.0, '0'))
                self.window.morse_manager.morse_signals[0].override_message((0.0, '101101100101010100101100110001010101001011001010101100100011010110110011011011001010110001101010011011011001101001000101101100101010100110101101100011010101001001100101101001011001101011011000101011001010100'))
        elif (not (self.next_level == 4 and self.level == 0) and
              self.start_time+LEVEL_DURATIONS[self.level] < TIMER.local_time):
            self.start_time = TIMER.local_time
            if self.level == 0:
                self.level = self.next_level
                self.next_level += 1
            else:
                self.level = 0

        self.wave_shift += TIMER.delta_local_time*Constants.WAVE_SPEED
        if self.wave_shift >= 1:
            self.wave_shift -= 1
            freq_pick, peak_pick = LEVEL_RAND[self.level]
            self.twin_waves.pop(0)
            self.twin_waves.append((random.choice(peak_pick), random.choice(freq_pick), 0, 0))

        if 0 <= self.wave_shift <= 5/6:
            twin_wave = 1
            t_x = (self.wave_shift + (1 / 6)) * 3
            self.peak_sound = ('NONE', SOUNDS.stop_sound(self.peak_sound[0], self.peak_sound[1]))
        else:
            twin_wave = 2
            t_x = (self.wave_shift - (5 / 6)) * 3

        t_peak = self.twin_waves[twin_wave][0]
        t_frequency = Constants.FREQUENCIES[self.twin_waves[twin_wave][1]]

        if self.peak_sound[1] is None and t_x < 0.05:
            sound = {1: 'wave_up', 0: 'NONE', -1: 'wave_down'}
            self.peak_sound = (sound[int(t_peak)], SOUNDS.play_sound(sound[int(t_peak)]))

        if abs(self.wave_shift - 2/3) < 0.005 and self.twin_waves[2][0]:
            SOUNDS.play_sound('suggest')

        p_peak = 0
        p_frequency = Constants.FREQUENCIES[0]
        p_x = 0
        for wave in self.player_waves[:2]:
            if not wave[0]:
                break
            time_since = TIMER.local_time_since(wave[-1])*3*Constants.WAVE_SPEED
            p_frequency = Constants.FREQUENCIES[wave[1]]
            if (0.5+p_frequency) >= time_since >= 0.5:
                p_peak = wave[0]
                p_x = (time_since-0.5)
                break

        twin_height = equation(t_x, t_peak, t_frequency)
        player_height = equation(p_x, p_peak, p_frequency)

        total_height = twin_height + player_height
        if abs(total_height) > self.wave_peak and abs(twin_height) > 0:
            self.wave_peak = abs(total_height)

        if t_x > t_frequency:
            if self.wave_peak > 0.40:
                self.window.menu_manager.health_manager.damage()
            self.wave_peak = 0

        for wave in self.player_waves[::-1]:
            if TIMER.local_time_since(wave[-1]) > (8+Constants.FREQUENCIES[wave[1]])*3*Constants.WAVE_SPEED:
                self.player_waves.remove(wave)
                self.player_waves.append((0, 0, 0))
            else:
                break

        self.renderer.render(self.twin_waves, self.player_waves, (self.peak, Constants.FREQUENCIES[self.frequency]),
                             self.wave_shift)
