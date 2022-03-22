import arcade
import arcade.gl.geometry as geo

from constants import Constants


class ModulationRenderer:

    def __init__(self, window: arcade.Window, color: tuple[float, float, float],
                 frame_width: int, frame_height: int, v_scale: float, render_pos: tuple[int, int]):
        self.frame_size = (frame_width, frame_height)
        self.vertical_scale = v_scale  # The max percent of frame size / 2 which the wave may reach

        self.window = window

        self.modulation_texture = window.ctx.texture(self.frame_size, dtype='f2')
        self.framebuffer = window.ctx.framebuffer(color_attachments=self.modulation_texture)

        self.modulation_program = window.ctx.load_program(vertex_shader=":resource:/shaders/base_vert.glsl",
                                                          fragment_shader=":resource:/shaders/modulation_frag.glsl")
        self.modulation_program['wave_max'] = int(frame_height//2 * v_scale), frame_height//2
        self.modulation_program['color'] = color

        self.wave_data: list[float] = [0 for _ in range(10)]

        self.draw_prog = window.ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                                 fragment_shader=":resource:/shaders/texture_draw_HDR_frag.glsl")
        self.draw_area = geo.quad_2d((2*frame_width/Constants.SCREEN_SIZE[0], 2*frame_height/Constants.SCREEN_SIZE[1]),
                                     ((2*render_pos[0])/Constants.SCREEN_SIZE[0]-1, (2*render_pos[1])/Constants.SCREEN_SIZE[1]-1))

    def adjust_wave_data(self, new_data):
        self.wave_data = new_data
        # self.modulation_program['wave_data'] = new_data

    def render(self):
        self.framebuffer.use()
        Constants.BASIC_GEO.render(self.modulation_program)
        self.window.game_framebuffer.use()

    def draw(self):
        self.modulation_texture.use(0)

        self.draw_area.render(self.draw_prog)
