from math import cos, pi

import arcade
import pyglet.gl as gl

from constants import init_constants, Constants, TIMER, SOUNDS
from effects.gaussian_blur import GpuGlow
from modulation import ModulationHandler
from menu import MenuManager
from morse import MorseManager


class GameApp(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_SIZE[0], Constants.SCREEN_SIZE[1], "EXPERIMENT TWIN SIGNAL")
        init_constants(self.ctx)
        self.game_screen = arcade.Sprite(":resource:/graphics/Game Screen Two.png", scale=0.25,
                                         center_x=Constants.SCREEN_SIZE[0]//2, center_y=Constants.SCREEN_SIZE[1]//2)
        self.win_glow = arcade.Sprite(":resource:/graphics/Win_Glow.png",
                                      center_x=Constants.SCREEN_SIZE[0]//2, center_y=Constants.SCREEN_SIZE[1]//2)
        self.fin = arcade.Sprite(":resource:/graphics/Fin_19x16px.png",
                                 center_x=Constants.SCREEN_SIZE[0]//2, center_y=Constants.SCREEN_SIZE[1]//2)

        self.base_texture = self.ctx.texture(size=self.get_size(), dtype='f2')
        self.hdr_texture = self.ctx.texture(size=self.get_size(), dtype='f2')
        self.game_framebuffer = self.ctx.framebuffer(color_attachments=[self.base_texture, self.hdr_texture])
        self.final_prog = self.ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                                fragment_shader=":resource:/shaders/hdr_frag.glsl")
        self.final_prog['scene'] = 0
        self.final_prog['bloomBlur'] = 1
        self.final_prog['exposure'] = 2.0

        self.vignettes = arcade.SpriteList()
        self.bloom = GpuGlow(self, self.get_size())

        self.modulation_handler = ModulationHandler(self)
        self.menu_manager = MenuManager(self)

        self.morse_manager = MorseManager(self, ["resources/morse_text/command.txt", "resources/morse_text/twin.txt"])

        self.fade = -1
        self.pulse = -1
        self.win_fade = -1
        self.dead = False

        self.power = False
        self.win = False
        self.finished = False

    def on_update(self, delta_time: float):
        TIMER.update_time(delta_time)
        if self.win and self.win_fade < 0:
            Constants.SCREEN_GLOW = True
            Constants.EFFECTS = True
            self.vignettes.clear()
            self.win_fade = TIMER.global_time
            TIMER.pause()
            self.morse_manager.show = True

        if (self.finished and self.morse_manager.morse_signals[1].playing == -1 and
                self.morse_manager.morse_signals[0].playing == -1):
            self.morse_manager.show = False

        if self.fade >= 0 and TIMER.global_time_since(self.fade) > 1:
            self.final_prog['exposure'] = 0
            self.fade = -1
            TIMER.pause()
            self.morse_manager.show = True
            if self.modulation_handler.level != 4:
                self.morse_manager.morse_signals[1].override_message((0.0, '0'))
                self.morse_manager.morse_signals[0].override_message((0.0, '1011011001010101001011001100010101010010110010101011001000110101101100110110110010101100011010100110110110011010010001011011001000101010100101100101010110010001101010100100100110100010101010010100110001010011000101001010100010110010110101001011010100011010110110011011011001010110010110100010101101001011001010110010110101001100'))
            elif self.modulation_handler.level == 4:
                self.morse_manager.morse_signals[0].override_message((0.0, '0'))
                self.morse_manager.morse_signals[1].override_message((0.0, '101001100010101010010110011010100011001101101100011010101001000110101001101101100110100100'))

        self.morse_manager.on_update()
        self.menu_manager.on_update()

    def default_update(self):
        self.modulation_handler.on_update()

    def die(self):
        if not self.dead:
            self.fade = TIMER.global_time
            self.dead = True

    def damaged(self):
        self.pulse = TIMER.global_time
        Constants.SCREEN_GLOW = True

    def on_draw(self):
        self.game_framebuffer.use()
        self.game_framebuffer.clear((0.0, 0.0, 0.0, 0.0))

        glow = Constants.SCREEN_GLOW and Constants.EFFECTS
        gl.glColorMaski(1, glow, glow, glow, glow)
        if self.pulse >= 0:
            self.final_prog['exposure'] = -cos(6*pi*TIMER.global_time_since(self.pulse))+3
            if TIMER.global_time_since(self.pulse) > 1/3:
                self.final_prog['exposure'] = 2.0
                self.pulse = -1
                if self.menu_manager.health_manager.health_range > 0:
                    Constants.SCREEN_GLOW = False

        self.game_screen.draw(pixelated=True)

        self.menu_manager.on_draw()

        self.modulation_handler.on_draw()
        gl.glColorMaski(1, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)

        self.menu_manager.on_glow_draw()

        self.modulation_handler.on_glow_draw()

        self.morse_manager.on_glow_draw()

        self.use()
        self.clear()

        self.bloom.process(self.hdr_texture)

        self.base_texture.use(0)
        self.hdr_texture.use(1)

        if self.fade >= 0:
            time_since = TIMER.global_time_since(self.fade)
            if time_since <= 1:
                self.final_prog['exposure'] = 2 - (time_since*2)
        elif self.win_fade >= 0:
            time_since = TIMER.global_time_since(self.win_fade)
            if time_since <= 10:
                self.win_glow.alpha = int(255*time_since/10)
            if time_since <= 10:
                self.final_prog['exposure'] = 2 + time_since

        # render the hdr textures to the screen using a screen sized geometry
        Constants.BASIC_GEO.render(self.final_prog)

        if self.win_fade > 0:
            self.win_glow.draw(pixelated=True)
            self.fin.draw(pixelated=True)

        self.morse_manager.on_after_draw()

        if Constants.EFFECTS:
            self.vignettes.draw(pixelated=True)

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
