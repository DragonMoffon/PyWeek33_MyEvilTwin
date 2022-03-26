from math import ceil

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
        self.can_switch = False

    def key_down(self):
        self.index = 3
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        self.can_switch = True


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

    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 1
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = min(self.index + 1, 3)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        self.manager.health_manager.change(self.index)

    def key_down(self):
        self.index = max(self.index - 1, 0)
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        self.manager.health_manager.change(self.index)


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
        Constants.EFFECTS = True

    def key_down(self):
        self.knob.texture = SettingManager.SWITCH_TEXTURE[1]
        Constants.EFFECTS = False


class ColorKnob(SettingManager):
    def __init__(self, window, neighbors, knob, case, manager):
        super().__init__(window, neighbors, knob, case, manager)
        self.index = 1
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]

    def key_up(self):
        self.index = 1
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        Constants.PLAYER_COLOR = [0.0, 1.0, 0.0]
        self.manager.health_manager.switch_colors(0)

    def key_down(self):
        self.index = 0
        self.knob.angle = SettingManager.KNOB_ANGLES[self.index]
        Constants.PLAYER_COLOR = [0.0, 0.2, 1.0]
        self.manager.health_manager.switch_colors(1)


class HealthLights:
    HEALTH_ARRAY = (1, 3, 6, 9)

    LIGHT_TEXTURES = ()

    def __init__(self, window):
        self.window = window
        self.current_chances = HealthLights.HEALTH_ARRAY[1]
        self.chance_range = 1
        self.chances = list(HealthLights.HEALTH_ARRAY)

        self.light_1 = arcade.Sprite(":resource:/graphics/Damage_Light_Green_48px.png", scale=0.25,
                                     center_x=944, center_y=352)
        self.light_2 = arcade.Sprite(":resource:/graphics/Damage_Light_Orange_48px.png", scale=0.25,
                                     center_x=944, center_y=302)
        self.light_3 = arcade.Sprite(":resource:/graphics/Damage_Light_Red_48px.png", scale=0.25,
                                     center_x=944, center_y=252)
        self.lights = arcade.SpriteList()
        self.current_light = self.light_1
        self.lights.extend([self.light_1, self.light_2, self.light_3])

        case_1 = arcade.Sprite(":resource:/graphics/Damage_Case_48px.png", scale=0.25,
                               center_x=944, center_y=352)
        case_2 = arcade.Sprite(":resource:/graphics/Damage_Case_48px.png", scale=0.25,
                               center_x=944, center_y=302)
        case_3 = arcade.Sprite(":resource:/graphics/Damage_Case_48px.png", scale=0.25,
                               center_x=944, center_y=252)

        self.cases = arcade.SpriteList()
        self.cases.extend([case_1, case_2, case_3])

        self.health_range = 3

        self.vignette = 0

    def change(self, new_index):
        last_percent = self.current_chances / HealthLights.HEALTH_ARRAY[self.chance_range]
        new_percent = self.chances[new_index] / HealthLights.HEALTH_ARRAY[new_index]

        self.chance_range = new_index

        if ceil(last_percent*HealthLights.HEALTH_ARRAY[new_index]) < self.chances[new_index]:
            self.current_chances = ceil(last_percent*HealthLights.HEALTH_ARRAY[new_index])
            self.chances[new_index] = self.current_chances
        else:
            self.current_chances = self.chances[new_index]

        if self.chance_range == 0:
            self.light_1.texture = HealthLights.LIGHT_TEXTURES[-1]
            self.light_2.texture = HealthLights.LIGHT_TEXTURES[-1]
            self.light_3.texture = HealthLights.LIGHT_TEXTURES[-1]
        else:
            self.switch_colors(int(Constants.PLAYER_COLOR[-1]))

        self.correct_lights()

    def damage(self):
        self.current_chances -= 1
        self.chances[self.chance_range] -= 1

        if self.current_chances < 0:
            self.window.die()
        else:
            self.window.damaged()

        self.correct_lights()

    def correct_lights(self):
        self.health_range = 3 * self.current_chances / HealthLights.HEALTH_ARRAY[self.chance_range]

        Constants.SCREEN_GLOW = False
        if self.health_range > 2:
            self.current_light = self.light_1
        elif self.health_range > 1:
            self.light_1.alpha = 40
            self.current_light = self.light_2
        elif self.health_range:
            self.light_1.alpha = 40
            self.light_2.alpha = 40
            self.current_light = self.light_3
            if not len(self.window.vignettes):
                self.window.vignettes.append(arcade.Sprite(":resource:/graphics/Danger_Effect.png", scale=0.25,
                                                           center_x=Constants.SCREEN_SIZE[0]//2,
                                                           center_y=Constants.SCREEN_SIZE[1]//2))
        else:
            self.light_1.alpha = 40
            self.light_2.alpha = 40
            self.light_3.alpha = 40
            Constants.SCREEN_GLOW = True
            self.current_light = self.light_3

    def on_draw(self):
        self.cases.draw(pixelated=True)

    def on_glow_draw(self):
        self.lights.draw(pixelated=True)

    def switch_colors(self, mode):
        if mode:
            self.light_1.texture = HealthLights.LIGHT_TEXTURES[2]
            self.light_2.texture = HealthLights.LIGHT_TEXTURES[3]
        else:
            self.light_1.texture = HealthLights.LIGHT_TEXTURES[0]
            self.light_2.texture = HealthLights.LIGHT_TEXTURES[1]


class MenuManager:

    def __init__(self, window):
        self.window = window
        self.menu_buttons = arcade.SpriteList()

        SettingManager.SWITCH_TEXTURE = (arcade.load_texture(":resource:/graphics/Switch_On_45x52px.png"),
                                         arcade.load_texture(":resource:/graphics/Switch_Off_45x52px.png"))

        HealthLights.LIGHT_TEXTURES = (
                        arcade.load_texture(":resource:/graphics/Damage_Light_Green_48px.png"),
                        arcade.load_texture(":resource:/graphics/Damage_Light_Orange_48px.png"),
                        arcade.load_texture(":resource:/graphics/Damage_Light_Blue_48px.png"),
                        arcade.load_texture(":resource:/graphics/Damage_Light_Purple_48px.png"),
                        arcade.load_texture(":resource:/graphics/Damage_Light_Red_48px.png"))

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

        self.health_manager = HealthLights(window)

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
        self.health_manager.on_draw()
        self.current.on_draw()

    def on_glow_draw(self):
        self.health_manager.on_glow_draw()
        if self.glow_knob.index or TIMER.global_time % 0.5 > 0.25:
            self.current.on_glow_draw()
