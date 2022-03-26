import arcade

from constants import Constants, SOUNDS, TIMER


class SettingManager:

    KNOB_ANGLES = (180, 90, 0, 270)
    SWITCH_TEXTURE = ()

    def __init__(self, window, neighbors, knob, case, manager):
        self.left_neighbor, self.right_neighbor = neighbors
        self.manager = manager
        self.window = window

        self.knob = knob
        self.case = case

        self.can_switch = True

    def on_key_press(self, symbol):
        if symbol == arcade.key.A and self.can_switch:
            self.manager.switch(self.left_neighbor)
        elif symbol == arcade.key.D and self.can_switch:
            self.manager.switch(self.right_neighbor)
        elif symbol == arcade.key.W:
            self.key_up()
        elif symbol == arcade.key.S:
            self.key_down()

    def key_up(self):
        pass

    def key_down(self):
        pass

    def on_update(self):
        self.window.default_update()

    def on_draw(self):
        pass

    def on_glow_draw(self):
        self.case.draw()


class MorseKnob(SettingManager):

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 3
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = 2
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_down(self):
        self.index = 3
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]


class PowerSwitch(SettingManager):

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        TIMER.pause()

    def key_up(self):
        TIMER.un_pause()
        self.knob.texture = SettingManager.SWITCH_TEXTURE[0]

    def key_down(self):
        TIMER.pause()
        self.knob.texture = SettingManager.SWITCH_TEXTURE[1]


class SpeedKnob(SettingManager):
    SPEED_VALUES = (0.25, 0.5, 0.75, 1.0)

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 3
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = min(self.index + 1, 3)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        TIMER.set_time_step(SpeedKnob.SPEED_VALUES[self.index])

    def key_down(self):
        self.index = max(self.index - 1, 0)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        TIMER.set_time_step(SpeedKnob.SPEED_VALUES[self.index])


class ChancesKnob(SettingManager):
    CHANCE_VALUES = (1, 3, 6, 9)

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 1
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = min(self.index + 1, 3)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_down(self):
        self.index = max(self.index - 1, 0)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]


class SoundKnob(SettingManager):
    SOUND_VALUES = (0.0, 1/3, 2/3, 1.0)

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 3
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = min(self.index + 1, 3)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        SOUNDS.change(SoundKnob.SOUND_VALUES[self.index])

    def key_down(self):
        self.index = max(self.index - 1, 0)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        SOUNDS.change(SoundKnob.SOUND_VALUES[self.index])


class GlowKnob(SettingManager):
    GLOW_VALUES = (0, 1, 3, 5)

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 3
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = min(self.index + 1, 3)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        self.window.bloom.blur_count = GlowKnob.GLOW_VALUES[self.index]

    def key_down(self):
        self.index = max(self.index - 1, 0)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        self.window.bloom.blur_count = GlowKnob.GLOW_VALUES[self.index]


class EffectSwitch(SettingManager):

    def key_up(self):
        self.knob.texture = SettingManager.SWITCH_TEXTURE[0]

    def key_down(self):
        self.knob.texture = SettingManager.SWITCH_TEXTURE[1]


class ColorKnob(SettingManager):
    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 1
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = 1
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        Constants.PLAYER_COLOR = [0.0, 1.0, 0.0]

    def key_down(self):
        self.index = 0
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        Constants.PLAYER_COLOR = [0.0, 0.2, 1.0]


class MenuManager:

    def __init__(self, window):
        self.window = window
        self.menu_buttons = arcade.SpriteList()

        SettingManager.SWITCH_TEXTURE = (arcade.load_texture(":resource:/graphics/Switch_On_45x52px.png"),
                                         arcade.load_texture(":resource:/graphics/Switch_Off_45x52px.png"))

        # MORSE KNOB
        sprite = arcade.Sprite(":resource:/graphics/Knob_32px.png", scale=0.25,
                               center_x=593, center_y=351)
        case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                             center_x=593, center_y=351)
        self.menu_buttons.extend([sprite, case])
        self.morse_knob = MorseKnob(window, [None, None], sprite, case, self)

        # POWER SWITCH
        sprite = arcade.Sprite(":resource:/graphics/Switch_Off_45x52px.png", scale=0.25,
                               center_x=34.5, center_y=37)
        case = arcade.Sprite(":resource:/graphics/Switch_Case_51x58px.png", scale=0.25,
                             center_x=34.5, center_y=37)
        self.menu_buttons.extend([sprite, case])
        self.power_switch = PowerSwitch(window, [self.morse_knob, None], sprite, case, self)
        self.morse_knob.right_neighbor = self.power_switch

        # SPEED KNOB
        sprite = arcade.Sprite(":resource:/graphics/Knob_32px.png", scale=0.25,
                               center_x=115, center_y=37)
        case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                             center_x=115, center_y=37)
        self.menu_buttons.extend([sprite, case])
        self.speed_knob = SpeedKnob(window, [self.power_switch, None], sprite, case, self)
        self.power_switch.right_neighbor = self.speed_knob

        # CHANCES KNOB
        sprite = arcade.Sprite(":resource:/graphics/Knob_32px.png", scale=0.25,
                               center_x=206, center_y=37)
        case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                             center_x=206, center_y=37)
        self.menu_buttons.extend([sprite, case])
        self.chances_knob = ChancesKnob(window, [self.speed_knob, self.morse_knob], sprite, case, self)
        self.speed_knob.right_neighbor = self.chances_knob

        # SOUND KNOB
        sprite = arcade.Sprite(":resource:/graphics/Knob_32px.png", scale=0.25,
                               center_x=354, center_y=37)
        case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                             center_x=354, center_y=37)
        self.menu_buttons.extend([sprite, case])
        self.sound_knob = SoundKnob(window, [self.chances_knob, None], sprite, case, self)
        self.chances_knob.right_neighbor = self.sound_knob

        # GLOW KNOB
        sprite = arcade.Sprite(":resource:/graphics/Knob_32px.png", scale=0.25,
                               center_x=445, center_y=37)
        case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                             center_x=445, center_y=37)
        self.menu_buttons.extend([sprite, case])
        self.glow_knob = GlowKnob(window, [self.sound_knob, None], sprite, case, self)
        self.sound_knob.right_neighbor = self.glow_knob

        # EFFECTS SWITCH
        sprite = arcade.Sprite(":resource:/graphics/Switch_On_45x52px.png", scale=0.25,
                               center_x=523.5, center_y=37)
        case = arcade.Sprite(":resource:/graphics/Switch_Case_51x58px.png", scale=0.25,
                             center_x=523.5, center_y=37)
        self.menu_buttons.extend([sprite, case])
        self.effects_switch = EffectSwitch(window, [self.glow_knob, None], sprite, case, self)
        self.glow_knob.right_neighbor = self.effects_switch

        # COLOR BLIND KNOB
        sprite = arcade.Sprite(":resource:/graphics/Knob_32px.png", scale=0.25,
                               center_x=943, center_y=32)
        case = arcade.Sprite(":resource:/graphics/Knob_Case_48px.png", scale=0.25,
                             center_x=943, center_y=32)
        self.menu_buttons.extend([sprite, case])
        self.color_knob = ColorKnob(window, [self.effects_switch, self.morse_knob], sprite, case, self)
        self.effects_switch.right_neighbor = self.color_knob
        self.morse_knob.left_neighbor = self.color_knob

        self.current = self.power_switch
        self.menu_buttons.remove(self.current.case)

    def on_update(self):
        self.current.on_update()

    def switch(self, manager):
        self.menu_buttons.append(self.current.case)
        self.current = manager
        self.menu_buttons.remove(self.current.case)

    def on_key_press(self, symbol):
        self.current.on_key_press(symbol)

    def on_draw(self):
        self.menu_buttons.draw(pixelated=True)
        self.current.on_draw()

    def on_glow_draw(self):
        self.current.on_glow_draw()
