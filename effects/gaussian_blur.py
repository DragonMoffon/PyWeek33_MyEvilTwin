"""
GPU GAUSSIAN BLUR.
"""
from arcade import Window
import arcade.gl as gl

from constants import Constants


class GpuGlow:
    """
    While it uses the same blur function as a regular blur. The Gpu Glow is expected to be used on texture with mostly
    opaque space around it. The original texture is redrawn over the top. This means, if used properly, it will make
    a blurry outline around the texture giving it a glow. It is used on the Modulation, but the original code was
    written to blur text.
    """

    def __init__(self, window: Window, process_size, blur_count=5):
        self.blur_prog = window.ctx.load_program(vertex_shader=":resource:/shaders/base_vert.glsl",
                                                 fragment_shader=":resource:/shaders/gaussian_frag.glsl")
        self.apply_prog = window.ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                                  fragment_shader=":resource:/shaders/texture_frag.glsl")

        self.process_size = process_size
        self.blur_count = blur_count

        self.texture_1 = window.ctx.texture(process_size, dtype='f2')
        self.texture_2 = window.ctx.texture(process_size, dtype='f2')

        self.framebuffer_1 = window.ctx.framebuffer(color_attachments=self.texture_1)
        self.framebuffer_2 = window.ctx.framebuffer(color_attachments=self.texture_2)

        self.window = window

    def process(self, input_texture: gl.Texture):
        """
        Takes in a texture and gives it a glow.
        WARNING THIS CHANGES THE TEXTURE IN PLACE AND DOES NOT RETURN A COPY.

        :param input_texture: The texture which the glow effect should be applied too.
        """
        self.texture_1.write(input_texture.read())

        # Since we are blurring horizontally then vertically we need to draw to both frame buffers.
        for _ in range(self.blur_count):
            self.framebuffer_2.use()
            self.framebuffer_2.clear()

            self.blur_prog['horizontal'] = 1
            self.texture_1.use(0)
            Constants.BASIC_GEO.render(self.blur_prog)

            self.framebuffer_1.use()
            self.framebuffer_1.clear()

            self.blur_prog['horizontal'] = 0
            self.texture_2.use(0)
            Constants.BASIC_GEO.render(self.blur_prog)

        self.framebuffer_2.use()

        # Re-render the original texture over the top. This helps sell the glow.
        input_texture.use(0)
        Constants.BASIC_GEO.render(Constants.TEXTURE_PROG)

        # Write over the input texture with the newly create texture.
        input_texture.write(self.texture_2.read())

        # finally, return the rendering back to the main window
        self.window.use()
