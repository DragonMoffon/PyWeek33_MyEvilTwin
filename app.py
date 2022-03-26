import arcade
import pyglet.gl as gl

from constants import init_constants, Constants, TIMER
from effects.gaussian_blur import GpuGlow
from modulation import ModulationHandler
from menu import MenuManager


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
        self.final_prog['exposure'] = 2.0
        self.bloom = GpuGlow(self, self.get_size())

        self.modulation_handler = ModulationHandler(self)
        self.menu_manager = MenuManager(self)

    def on_update(self, delta_time: float):
        TIMER.update_time(delta_time)
        self.menu_manager.on_update()

    def default_update(self):
        self.modulation_handler.on_update()

    def on_draw(self):
        self.game_framebuffer.use()
        self.game_framebuffer.clear((0.0, 0.0, 0.0, 0.0))

        gl.glColorMaski(1, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE)
        self.game_screen.draw(pixelated=True)

        self.menu_manager.on_draw()

        self.modulation_handler.on_draw()
        gl.glColorMaski(1, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)

        if self.bloom.blur_count or TIMER.local_time % 0.5 > 0.25:

            self.menu_manager.on_glow_draw()

        self.modulation_handler.on_glow_draw()

        self.use()
        self.clear()

        self.bloom.process(self.hdr_texture)

        self.base_texture.use(0)
        self.hdr_texture.use(1)

        # render the hdr textures to the screen using a screen sized geometry
        Constants.BASIC_GEO.render(self.final_prog)

    def on_key_press(self, symbol: int, modifiers: int):
        if TIMER.run:
            self.modulation_handler.on_key_press(symbol)
        self.menu_manager.on_key_press(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        if TIMER.run:
            self.modulation_handler.on_key_release(symbol)


def run():
    TIMER.begin()
    window = GameApp()
    window.run()
