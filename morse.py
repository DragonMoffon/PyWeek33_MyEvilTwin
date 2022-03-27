import random

import arcade
import arcade.gl.geometry as geo

from constants import Constants, TIMER, SOUNDS


class MorseText:
    TEXT_TEXTURES: dict = {}

    def __init__(self):
        MorseText.TEXT_TEXTURES = {
            '1011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 0, 0, 8, 16),
            '11010101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 8, 0, 7, 16),
            '110101101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 15, 0, 7, 16),
            '110101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 22, 0, 7, 16),
            '1': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 29, 0, 5, 16),
            '10101101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 34, 0, 5, 16),
            '1101101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 39, 0, 7, 16),
            '1010101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 46, 0, 7, 16),
            '101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 53, 0, 2, 16),
            '1011011011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 55, 0, 7, 16),
            '1101011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 62, 0, 8, 16),
            '10110101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 70, 0, 5, 16),
            '11011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 75, 0, 9, 16),
            '1101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 84, 0, 7, 16),
            '11011011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 91, 0, 7, 16),
            '101101101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 0, 16, 7, 16),
            '1101101011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 7, 16, 8, 16),
            '101101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 15, 16, 7, 16),
            '10101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 22, 16, 7, 16),
            '11': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 29, 16, 8, 16),
            '101011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 37, 16, 7, 16),
            '10101011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 44, 16, 8, 16),
            '1011011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 52, 16, 9, 16),
            '110101011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 61, 16, 9, 16),
            '1101011011': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 70, 16, 8, 16),
            '110110101': arcade.load_texture(":resource:/graphics/Font_98x32px.png", 78, 16, 7, 16)
        }
        self.base_char_pos = (364, 300)
        self.text_screen = arcade.Sprite(":resource:/graphics/Morse_Screen.png", scale=0.25,
                                         center_x=Constants.SCREEN_SIZE[0] // 2, center_y=Constants.SCREEN_SIZE[1] // 2)

        self.characters = arcade.SpriteList()
        self.next_char_x = 360
        self.next_char_y = 397

    def add_char(self, value, color):
        texture = MorseText.TEXT_TEXTURES.get(value,
                                              MorseText.TEXT_TEXTURES[
                                                  random.choice(list(MorseText.TEXT_TEXTURES))])
        char = arcade.Sprite(center_x=self.next_char_x + texture.width // 2,
                             center_y=self.next_char_y - texture.height // 2)
        char.texture = texture
        char.color = color

        self.next_char_x += char.width + 4
        if self.next_char_x >= 590:
            self.next_char_x = self.base_char_pos[0]
            self.next_char_y -= 17

        self.characters.append(char)
        return char

    def update_char(self, char, value):
        if char in self.characters:
            char_index = self.characters.index(char) + 1
            starting_x = char.center_x - char.width//2
            char.texture = MorseText.TEXT_TEXTURES.get(value,
                                                       MorseText.TEXT_TEXTURES[
                                                           random.choice(list(MorseText.TEXT_TEXTURES))])
            char.center_x = starting_x + char.texture.width//2
            next_x = starting_x + char.width + 4

            for chars in self.characters[char_index:]:
                chars.center_x = next_x + chars.width//2
                next_x += char.width + 4

    def start(self):
        self.next_char_x = self.base_char_pos[0]
        self.next_char_y = self.base_char_pos[1]
        self.characters.clear(deep=False)

    def add_space(self):
        self.next_char_x += 8
        if self.next_char_x >= 578:
            self.next_char_x = self.base_char_pos[0]
            self.next_char_y -= 17

    def draw(self):
        self.text_screen.draw(pixelated=True)
        self.characters.draw(pixelated=True)


class MorseSignal:

    def __init__(self, window, color, messages, text):
        self.window = window
        self.color = [int(n * 255) for n in color]
        self.norm_color = color
        self.messages = messages
        self.message = self.messages[0]
        self.next_message = 0
        self.next_sig = 0
        self.text: MorseText = text

        self.sound = None

        self.current_char = None
        self.current_letter = ''

        self.playing = -1

        self.shift = 0

        self.signals = [0 for _ in range(13)]

        self.morse_texture = window.ctx.texture(Constants.OSCILLOSCOPE_SIZE, dtype='f2')
        self.framebuffer = window.ctx.framebuffer(color_attachments=self.morse_texture)

        self.morse_program = window.ctx.load_program(vertex_shader=":resource:/shaders/base_vert.glsl",
                                                     fragment_shader=":resource:/shaders/morse_frag.glsl")

        self.draw_prog = window.ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                                 fragment_shader=":resource:/shaders/texture_draw_HDR_frag.glsl")

        self.draw_area = geo.quad_2d((2 * Constants.MORSE_SIZE[0] / Constants.SCREEN_SIZE[0],
                                      2 * Constants.MORSE_SIZE[1] / Constants.SCREEN_SIZE[1]),
                                     (2 * Constants.MORSE_POS[0] / Constants.SCREEN_SIZE[0] - 1,
                                      2 * Constants.MORSE_POS[1] / Constants.SCREEN_SIZE[1] - 1))

    def override_message(self, new_message):
        self.text.start()
        self.message = new_message
        self.playing = TIMER.global_time
        self.shift = 0
        self.next_sig = 0
        self.current_char = None
        self.current_letter = ''

    def update(self):
        if self.playing >= 0:
            self.shift += TIMER.delta_time*18
            if self.shift >= 1:
                self.shift -= 1
                if self.next_sig < len(self.message[1]):
                    next_value = self.message[1][self.next_sig]
                    self.next_sig += 1
                    if next_value == '0':
                        self.sound = SOUNDS.stop_sound('morse', self.sound)

                    if next_value != '0':
                        if self.sound is None:
                            self.sound = SOUNDS.play_sound('morse')
                        self.current_letter += next_value
                        if self.current_char is None:
                            self.current_char = self.text.add_char(self.current_letter, self.color)
                        else:
                            self.text.update_char(self.current_char, self.current_letter)
                    elif len(self.current_letter) and self.current_letter[-1] == '0':
                        self.current_char = None
                        self.current_letter = ''
                    elif not len(self.current_letter):
                        self.text.add_space()
                    else:
                        self.current_letter += next_value

                    self.signals.pop(0)
                    self.signals.append(int(next_value))

                elif self.next_sig <= len(self.message[1]) + 13:
                    self.next_sig += 1
                    self.signals.pop(0)
                    self.signals.append(0)
                else:
                    self.playing = -1
                    self.next_sig = 0
                    self.next_message += 1
                    if self.next_message < len(self.messages):
                        self.message = self.messages[self.next_message]
                    else:
                        self.message = (float('inf'), "")
        elif TIMER.local_time >= self.message[0]:
            self.playing = TIMER.global_time
            self.shift = 0
            self.text.start()

    def draw(self):
        self.morse_program['color'] = self.norm_color
        self.morse_program['shift'] = self.shift
        self.morse_program['values'] = self.signals

        self.framebuffer.use()
        self.framebuffer.clear()
        Constants.BASIC_GEO.render(self.morse_program)
        self.window.game_framebuffer.use()

        self.morse_texture.use(0)

        self.draw_area.render(self.draw_prog)


class MorseManager:

    def __init__(self, window, morse_sources):
        self.window = window

        self.morse_text: MorseText = MorseText()
        self.morse_signals: list[MorseSignal] = []

        self.show = False

        for source in morse_sources:
            with open(source) as morse_text:
                lines = morse_text.readlines()
                color = [float(n) for n in lines[0].split(' ')]
                messages = []
                for m in lines[1:]:
                    m = m.strip().split(':')
                    messages.append((float(m[0]), m[1]))
                morse = MorseSignal(window, color, tuple(messages), self.morse_text)
                self.morse_signals.append(morse)

    def on_update(self):
        for signal in self.morse_signals:
            signal.update()

    def on_glow_draw(self):
        for signal in self.morse_signals:
            signal.draw()

    def on_after_draw(self):
        if self.show:
            self.morse_text.draw()
