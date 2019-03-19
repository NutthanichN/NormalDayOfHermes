import arcade
from models_zeus_vs_typhon2 import Character, Map, MapDrawer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
SPRITE_SCALE = 0.75

MOVEMENT_VX = 5
JUMP_VY = 10
GRAVITY = 1

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_UP: (0, 1),
               DIR_RIGHT: (1, 0),
               DIR_DOWN: (0, -1),
               DIR_LEFT: (-1, 0)}

KEY_MAP = {arcade.key.UP: DIR_UP,
           arcade.key.DOWN: DIR_DOWN,
           arcade.key.LEFT: DIR_LEFT,
           arcade.key.RIGHT: DIR_RIGHT}


class CaveWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        """
        BISTRE_BROWN = (150, 113, 23)
        BROWN_NOSE = (107, 68, 35)
        DARK_BROWN = (101, 67, 33)
        DONKEY_BROWN = (102, 76, 40)
        OTTER_BROWN = (101, 67, 33)
        PULLMAN_BROWN = (100, 65, 23)
        RUDDY_BROWN = (187, 101, 40) *
        SADDLE_BROWN = (139, 69, 19) **
        TUSCAN_BROWN = (111, 78, 55)
        ZINNWALDITE_BROWN = (44, 22, 8)
        """
        arcade.set_background_color(arcade.color.SADDLE_BROWN)

        self.hermes_sprite = Character('images/Hermes/Hermes_right_55x86_w1.png', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                       SPRITE_SCALE)

        self.map1_1 = MapDrawer('map/map1_1.txt', 'images/block_20.PNG', 'images/block_20.PNG')
        self.physics_engine_platform = arcade.PhysicsEnginePlatformer(self.hermes_sprite,
                                                                      self.map1_1.platform_sprite_list,
                                                                      GRAVITY)
        self.physics_engine_wall = arcade.PhysicsEngineSimple(self.hermes_sprite,
                                                              self.map1_1.wall_sprite_list,)

    def update(self, delta):
        self.hermes_sprite.update()
        self.physics_engine_wall.update()
        self.physics_engine_platform.update()

    def on_draw(self):
        arcade.start_render()

        self.hermes_sprite.draw()
        self.map1_1.wall_sprite_list.draw()
        self.map1_1.platform_sprite_list.draw()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.hermes_sprite.change_x = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][0]
            # self.hermes_sprite.change_y = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][1]
            if key == arcade.key.UP:
                if self.physics_engine_platform.can_jump():
                    self.hermes_sprite.change_y = JUMP_VY * DIR_OFFSETS[KEY_MAP[key]][1]
        # print(self.hermes_sprite.change_x)

        # not quite work
        # else:
        #     if key == arcade.key.UP and key == arcade.key.RIGHT:
        #         self.hermes_sprite.change_x = MOVEMENT_VX * DIR_OFFSETS[DIR_RIGHT][0]
        #     elif key == arcade.key.UP and key == arcade.key.LEFT:
        #         self.hermes_sprite.change_x = MOVEMENT_VX * DIR_OFFSETS[DIR_LEFT][1]
        #
        #     if self.physics_engine_platform.can_jump():
        #         self.hermes_sprite.change_y = JUMP_VY * DIR_OFFSETS[KEY_MAP[key]][1]

    def on_key_release(self, key, key_modifiers):
        # if key == arcade.key.UP or key == arcade.key.DOWN:
        #     self.hermes_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.hermes_sprite.change_x = 0


def main():
    window = CaveWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()