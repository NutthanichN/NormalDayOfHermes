import arcade
from models_zeus_vs_typhon2 import MainCharacter, MapDrawer, Status
import my_physics
from pyglet import clock

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 720
BLOCK_SIZE = 20
SPRITE_SCALE = 0.75

MOVEMENT_VX = 2
JUMP_VY = 8
GRAVITY = 0.5

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

        self.map1_1 = MapDrawer('map/map1_1.txt', 'images/block_20.PNG', 'images/block_20.PNG',
                                'images/ramp_left_20.PNG', 'images/ramp_right_20.PNG',
                                'images/trap_left_30x20.PNG', 'images/trap_right_30x20.PNG',
                                'images/trap_top_20x30.PNG', 'images/trap_bottom_20x30.PNG',
                                'images/key_18x19.PNG', 'images/hp_potion_18x19.PNG',
                                'images/magic_potion_18x19.PNG', 'images/super_magic_potion_18x19.PNG',
                                'images/door_red_60x80.PNG', 'images/door_green_60x80.PNG')

        self.hermes_sprite = MainCharacter(self.map1_1, SPRITE_SCALE)
        self.hermes_sprite.init_stand_right_and_left('images/Hermes/Hermes_right_55x86_w1.png')

        self.hermes_sprite.init_walk_right_and_left('images/Hermes/Hermes_right_61x86_w2.png',
                                                    'images/Hermes/Hermes_right_64x86_w3.png',
                                                    'images/Hermes/Hermes_right_61x86_w4.png',
                                                    'images/Hermes/Hermes_right_55x86_w5.png',
                                                    'images/Hermes/Hermes_right_55x86_w6.png',
                                                    'images/Hermes/Hermes_right_51x86_w7.png',
                                                    'images/Hermes/Hermes_right_55x86_w8.png',
                                                    'images/Hermes/Hermes_right_55x86_w9.png')

        self.physics_engine_platform = my_physics.PhysicsEnginePlatformer(self.hermes_sprite,
                                                                          self.map1_1.platform_sprite_list,
                                                                          GRAVITY)

        self.physics_engine_wall = my_physics.PhysicsEngineSimple(self.hermes_sprite,
                                                                  self.map1_1.wall_sprite_list,)

        self.status = Status(SCREEN_WIDTH, SCREEN_HEIGHT, self.hermes_sprite, self.map1_1,
                             'images/hp_lvl_20.png', 'images/weapon_lvl_20.png', 'images/key_18x19.PNG')

    def update(self, delta):
        if self.hermes_sprite.is_dead:
            print('Die!!')
            self.hermes_sprite.is_dead = False
            # self.hermes_sprite.restart()

        hit_items = arcade.check_for_collision_with_list(self.hermes_sprite, self.map1_1.items_sprite_list)
        if len(hit_items) > 0:
            for i in hit_items:
                # print(i)
                # self.map1_1.collected_items_list.append(i)
                # self.map1_1.items_list.remove(i)

                # self.map1_1.collected_item_sprite_list.append(i)
                self.map1_1.items_sprite_list.remove(i)
                # self.map1_1.current_items_sprite_list.remove(i)
                self.status.check_and_set_player_status(i)
                i.kill()

        for door in self.map1_1.door_sprite_list:
            if door.has_player(self.hermes_sprite):
                print('Enter door')

        self.hermes_sprite.update_animation()
        self.physics_engine_wall.update()

        self.map1_1.wall_sprite_list.update()
        self.map1_1.platform_sprite_list.update()

        self.map1_1.items_sprite_list.update()
        # print(list(self.map1_1.items_sprite_list))
        # print('items_list and collected_items_list')
        # print(self.map1_1.items_list)

        # self.map1_1.current_items_sprite_list.update()
        # print(list(self.map1_1.current_items_sprite_list))

        self.map1_1.collected_item_sprite_list.update()
        # print(list(self.map1_1.collected_item_sprite_list))
        # print(self.map1_1.collected_items_list)
        # print('---------------------------------------------------------------------------')

        # self.map1_1.collected_item_sprite_list.update() --> because line 94
        # print('--------------------------------')
        # print(self.hermes_sprite.change_x, 'change x')
        # print(self.hermes_sprite.position)

        self.physics_engine_platform.update()

    def on_draw(self):
        arcade.start_render()

        self.map1_1.door_sprite_list.draw()
        self.hermes_sprite.draw()
        self.map1_1.wall_sprite_list.draw()
        self.map1_1.platform_sprite_list.draw()
        self.map1_1.items_sprite_list.draw()
        # text = f"FPS: {clock.get_fps()}"
        # arcade.draw_text(text, 50, SCREEN_HEIGHT//2, arcade.color.RED, 16)
        # print(text)

        self.status.draw()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.hermes_sprite.change_x = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][0]
            # self.hermes_sprite.change_y = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][1]
            self.hermes_sprite.next_direction_x = KEY_MAP[key]

        if key == arcade.key.UP:
            if self.physics_engine_platform.can_jump():
                self.hermes_sprite.change_y = JUMP_VY * DIR_OFFSETS[KEY_MAP[key]][1]
                self.hermes_sprite.next_direction_y = KEY_MAP[key]

        if key == arcade.key.R:
            # self.restart = True
            self.hermes_sprite.restart()
            print('Before:')
            print('all items: ', list(self.map1_1.items_sprite_list))
            # print('collected items: ', list(self.map1_1.collected_item_sprite_list))
            # print('========================================================================')

            self.map1_1.restart()
            print('After:')
            print('all items: ', list(self.map1_1.items_sprite_list))
            # print('current items: ', list(self.map1_1.current_items_sprite_list))
            print('========================================================================')

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
