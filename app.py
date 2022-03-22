from numpy import frombuffer, savetxt, reshape


import arcade
import arcade.gl as gl
import random

from constants import init_constants, Constants
from modulation_graphic import ModulationRenderer
from effects.gaussian_blur import GpuGlow


class GameApp(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_SIZE[0], Constants.SCREEN_SIZE[1], "EXPERIMENT TERMINAL")
        init_constants(self.ctx)
        self.game_screen = arcade.Sprite(":resource:/graphics/Game Screen Two.png", scale=0.25,
                                         center_x=Constants.SCREEN_SIZE[0]//2, center_y=Constants.SCREEN_SIZE[1]//2)

        self.base_texture = self.ctx.texture(size=self.get_size(), dtype='f2')
        self.hdr_texture = self.ctx.texture(size=self.get_size(), dtype='f2')
        self.game_framebuffer = self.ctx.framebuffer(color_attachments=[self.base_texture, self.hdr_texture])
        self.final_prog = self.ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                                fragment_shader=":resource:/shaders/hdr_frag.glsl")
        self.final_prog['scene'] = 0
        self.final_prog['bloomBlur'] = 1
        self.final_prog['exposure'] = 1.0
        self.bloom = GpuGlow(self, self.get_size())

        self.enemy_modulation = ModulationRenderer(self, (1.0, 0.0, 0.0),
                                                   Constants.OSCILLOSCOPE_SIZE[0], Constants.OSCILLOSCOPE_SIZE[1], 0.8,
                                                   Constants.OSCILLOSCOPE_POS)
        self.enemy_modulation.adjust_wave_data([random.uniform(-1, 1) for _ in range(10)])
        self.enemy_modulation.render()

    def on_draw(self):
        self.game_framebuffer.use()
        self.game_framebuffer.clear((0.0, 0.0, 0.0, 1.0))
        self.game_screen.draw(pixelated=True)
        self.enemy_modulation.draw()

        self.use()
        self.clear()

        self.bloom.process(self.hdr_texture)

        # self.base_texture.use(0)
        self.hdr_texture.use(0)

        # just render the texture to the screen using a screen sized geometry
        Constants.BASIC_GEO.render(Constants.TEXTURE_PROG)

        # Constants.BASIC_GEO.render(self.final_prog)


def run():
    window = GameApp()
    window.run()
