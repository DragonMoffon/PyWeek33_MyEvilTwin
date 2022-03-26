import random

import arcade
import arcade.gl.geometry as geo

from constants import Constants, TIMER


class ModulationRenderer:

    def __init__(self, window: arcade.Window,):
        self.window = window
        self.size = Constants.OSCILLOSCOPE_SIZE
        self.pos = Constants.OSCILLOSCOPE_POS

        self.modulation_texture = window.ctx.texture(Constants.OSCILLOSCOPE_SIZE, dtype='f2')
        self.framebuffer = window.ctx.framebuffer(color_attachments=self.modulation_texture)

        self.modulation_program = window.ctx.load_program(vertex_shader=":resource:/shaders/base_vert.glsl",
                                                          fragment_shader=":resource:/shaders/modulation_frag.glsl")

        self.draw_prog = window.ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                                 fragment_shader=":resource:/shaders/texture_draw_HDR_frag.glsl")

        self.draw_area = geo.quad_2d((2 * self.size[0] / Constants.SCREEN_SIZE[0],
                                      2 * self.size[1] / Constants.SCREEN_SIZE[1]),
                                     (2 * self.pos[0] / Constants.SCREEN_SIZE[0]-1,
                                      2 * self.pos[1] / Constants.SCREEN_SIZE[1]-1))

    def render(self, twin_waves, player_waves, player_wave, shift):

        self.modulation_program['color'] = Constants.PLAYER_COLOR
        self.modulation_program['l_time'] = TIMER.local_time

        self.modulation_program['twin_waves'] = [n for wave in twin_waves for n in wave]
        self.modulation_program['player_waves'] = [n for wave in player_waves for n in wave]
        self.modulation_program['player_wave'] = player_wave

        self.modulation_program['shift'] = shift

        self.framebuffer.use()
        self.framebuffer.clear()
        Constants.BASIC_GEO.render(self.modulation_program)
        self.window.game_framebuffer.use()

    def draw(self):
        self.modulation_texture.use(0)

        self.draw_area.render(self.draw_prog)
