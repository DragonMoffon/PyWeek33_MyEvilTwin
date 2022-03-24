import arcade
import arcade.gl.geometry as geo
import arcade.gl as gl


class Constants:

    SCREEN_SIZE: tuple[int, int] = (976, 480)
    OSCILLOSCOPE_SIZE: tuple[int, int] = (550, 300)
    OSCILLOSCOPE_POS: tuple[int, int] = (282, 252)
    OSCILLOSCOPE_ENEMY_SIZE: tuple[int, int] = (400, 300)
    OSCILLOSCOPE_ENEMY_POS: tuple[int, int] = (356, 252)
    OSCILLOSCOPE_PLAYER_SIZE: tuple[int, int] = (200, 300)
    OSCILLOSCOPE_PLAYER_POS: tuple[int, int] = (106, 252)
    BASIC_GEO: gl.Geometry
    TEXTURE_PROG: gl.Program


CONSTANTS = Constants()


def init_constants(ctx: arcade.ArcadeContext):
    """
    Since some constants require the arcade context they must be created after initialisation.
    """

    Constants.BASIC_GEO = geo.quad_2d_fs()
    Constants.TEXTURE_PROG = ctx.load_program(vertex_shader=":resource:/shaders/texture_vert.glsl",
                                              fragment_shader=":resource:/shaders/texture_frag.glsl")
