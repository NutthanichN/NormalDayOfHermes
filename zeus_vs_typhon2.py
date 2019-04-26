"""16/4/19 add monster, monster can move only on platform, try to change map (still ugly code)
26/4/19 22:00-00:34 don't forget to make monster die and drop item next time"""
import arcade
from models_zeus_vs_typhon2 import MainCharacter, MapDrawer, Status, Monster
import my_physics
from pyglet import clock
import my_physics2
from random import randrange
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 720
SCREEN_TITLE = 'Normal day of Hermes'
BLOCK_SIZE = 20
SPRITE_SCALE = 0.75
# SPRITE_SCALE = 1

MOVEMENT_VX = 3    # 2
JUMP_VY = 11    # 8
GRAVITY = 0.5     # 0.5

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


def set_up_maps(*args):
    block_pic = 'images/block_20.PNG'
    ramp_left_pic = 'images/ramp_left_20.PNG'
    ramp_right_pic = 'images/ramp_right_20.PNG'
    trap_left_pic = 'images/trap_left_30x20.PNG'
    trap_right_pic = 'images/trap_right_30x20.PNG'
    trap_top_pic = 'images/trap_top_20x30.PNG'
    trap_bottom_pic = 'images/trap_bottom_20x30.PNG'
    key_pic = 'images/key_18x19.PNG'
    hp_potion_pic = 'images/hp_potion_18x19.PNG'
    magic_potion_pic = 'images/magic_potion_18x19.PNG'
    super_magic_potion_pic = 'images/super_magic_potion_18x19.PNG'
    door_red_pic = 'images/door_red_60x80.PNG'
    door_green_pic = 'images/door_green_60x80.PNG'
    monster_pic1 = 'images/monsters/Sphinx_right_69x63.PNG'
    monster_pic2 = 'images/monsters/Orthrus_right_89x53.PNG'
    monster_pic3 = 'images/monsters/Chimera_right_90x56.PNG'
    monster_bullet_pic = 'images/monster_bullet_33x12.PNG'

    maps = []
    for map in args:
        map_filename = map
        maps.append(MapDrawer(map_filename, block_pic, block_pic, ramp_left_pic, ramp_right_pic,
                              trap_left_pic, trap_right_pic, trap_top_pic, trap_bottom_pic,
                              key_pic, hp_potion_pic, magic_potion_pic, super_magic_potion_pic,
                              door_red_pic, door_green_pic, monster_pic1, monster_bullet_pic))

    return maps

    # return MapDrawer(map_filename, block_pic, block_pic, ramp_left_pic, ramp_right_pic,
    #                  trap_left_pic, trap_right_pic, trap_top_pic, trap_bottom_pic,
    #                  key_pic, hp_potion_pic, magic_potion_pic, super_magic_potion_pic,
    #                  door_red_pic, door_green_pic)


class CaveWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

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

        # self.map1_1 = MapDrawer('map/map1_1.txt', 'images/block_20.PNG', 'images/block_20.PNG',
        #                         'images/ramp_left_20.PNG', 'images/ramp_right_20.PNG',
        #                         'images/trap_left_30x20.PNG', 'images/trap_right_30x20.PNG',
        #                         'images/trap_top_20x30.PNG', 'images/trap_bottom_20x30.PNG',
        #                         'images/key_18x19.PNG', 'images/hp_potion_18x19.PNG',
        #                         'images/magic_potion_18x19.PNG', 'images/super_magic_potion_18x19.PNG',
        #                         'images/door_red_60x80.PNG', 'images/door_green_60x80.PNG')

        self.maps = set_up_maps('map/map1_1.txt', 'map/map1_2.txt')
        self.current_map = self.maps[0]

        self.hermes_sprite = MainCharacter(self.current_map, SPRITE_SCALE, 'images/player_bullet_33x12.png')
        self.hermes_sprite.init_stand_right_and_left('images/Hermes/Hermes_right_55x86_w1.png')

        self.hermes_sprite.init_walk_right_and_left('images/Hermes/Hermes_right_61x86_w2.png',
                                                    'images/Hermes/Hermes_right_64x86_w3.png',
                                                    'images/Hermes/Hermes_right_61x86_w4.png',
                                                    'images/Hermes/Hermes_right_55x86_w5.png',
                                                    'images/Hermes/Hermes_right_55x86_w6.png',
                                                    'images/Hermes/Hermes_right_51x86_w7.png',
                                                    'images/Hermes/Hermes_right_55x86_w8.png',
                                                    'images/Hermes/Hermes_right_55x86_w9.png')

        # self.physics_engine_platform = None
        # self.physics_engine_wall = None
        self.physics_engines = None
        self.set_up_physics_engines(self.hermes_sprite, self.current_map)

        # self.physics_engines = my_physics2.PhysicsEngine(self.hermes_sprite, self.current_map.wall_sprite_list,
        #                                                  self.current_map.platform_sprite_list, GRAVITY)

        self.status = Status(SCREEN_WIDTH, SCREEN_HEIGHT, self.hermes_sprite, self.current_map,
                             'images/hp_lvl_20.png', 'images/weapon_lvl_20.png', 'images/key_18x19.PNG')

        self.check_attack_time = 0
        self.game_end = False

    def set_up_physics_engines(self, player, current_map):
        # self.physics_engine_platform = my_physics.PhysicsEnginePlatformer(player,
        #                                                                   current_map.platform_sprite_list,
        #                                                                   GRAVITY)
        #
        # self.physics_engine_wall = my_physics.PhysicsEngineSimple(player,
        #                                                           current_map.wall_sprite_list)
        self.physics_engines = my_physics.PhysicsEngine(player, current_map.wall_sprite_list,
                                                        current_map.platform_sprite_list, GRAVITY)

    def change_map(self, next):
        next_index = self.maps.index(self.current_map) + 1
        previous_index = self.maps.index(self.current_map) - 1
        if next:
            if next_index <= len(self.maps) - 1:
                self.current_map = self.maps[next_index]
            else:
                print("Can't move forward")
                return
        else:
            if previous_index >= 0:
                self.current_map = self.maps[previous_index]
            else:
                print("Can't move backward")
                return

        self.hermes_sprite.set_map(self.current_map)
        self.hermes_sprite.set_up_position()

        self.set_up_physics_engines(self.hermes_sprite, self.current_map)

        # if 0 <= self.maps.index(self.current_map) < len(self.maps):
        #     if next and self.maps.index(self.current_map) <= len(self.maps) - 2:
        #         self.current_map = self.maps[self.maps.index(self.current_map) + 1]
        #     elif not next and self.maps.index(self.current_map) >= 0:
        #         self.current_map = self.maps[self.maps.index(self.current_map) - 1]
        #
        #     self.hermes_sprite.set_map(self.current_map)
        #     self.hermes_sprite.set_up_position()
        #     self.set_up_physics_engines(self.hermes_sprite, self.current_map)

    def update(self, delta):
        if not self.game_end:
            if not self.hermes_sprite.is_dead:
                hit_items = arcade.check_for_collision_with_list(self.hermes_sprite, self.current_map.items_sprite_list)
                if len(hit_items) > 0:
                    for i in hit_items:
                        # print(i)
                        # self.map1_1.collected_items_list.append(i)
                        # self.map1_1.items_list.remove(i)

                        # self.map1_1.collected_item_sprite_list.append(i)
                        self.current_map.items_sprite_list.remove(i)
                        # self.map1_1.current_items_sprite_list.remove(i)
                        self.status.check_and_set_player_status(i)
                        i.kill()

                for door in self.current_map.door_sprite_list:
                    if door.has_player(self.hermes_sprite) and door.active:
                        if door.is_last_door:
                            self.game_end = True
                        print('Enter door')
                        self.change_map(True)

                if self.current_map.monster is not None:
                    if not self.current_map.monster.is_dead:
                        if self.hermes_sprite.is_hit_by(self.current_map.monster):
                            self.hermes_sprite.is_dead = True

                        if randrange(100) == 0:
                            self.current_map.monster.attack()

                        # check if player is hir by monster's bullet
                        hit_list1 = arcade.check_for_collision_with_list(self.hermes_sprite,
                                                                         self.current_map.monster.bullet_sprite_list)
                        for m_b in hit_list1:
                            self.hermes_sprite.calculate_damage(m_b)
                            m_b.kill()

                        # check if monster is hit by player's bullet
                        hit_list2 = arcade.check_for_collision_with_list(self.current_map.monster,
                                                                         self.hermes_sprite.bullet_sprite_list)
                        for p_m in hit_list2:
                            self.current_map.monster.calculate_damage(p_m)
                            p_m.kill()

                        self.current_map.monster.update()
                        self.current_map.monster.bullet_sprite_list.update()
                    else:
                        self.current_map.monster = None

                self.hermes_sprite.update_animation()
                self.hermes_sprite.update_status()
                self.hermes_sprite.bullet_sprite_list.update()
                # self.hermes_sprite.update()
                # self.physics_engine_platform.update()
                # self.physics_engine_wall.update()
                self.physics_engines.update()
                # self.monster_sprite.update()

                self.current_map.wall_sprite_list.update()
                self.current_map.platform_sprite_list.update()
                self.current_map.door_sprite_list.update()

                self.current_map.items_sprite_list.update()

                # print(list(self.map1_1.items_sprite_list))
                # print('items_list and collected_items_list')
                # print(self.map1_1.items_list)

                # self.map1_1.current_items_sprite_list.update()
                # print(list(self.map1_1.current_items_sprite_list))

                self.current_map.collected_item_sprite_list.update()
                # print(list(self.map1_1.collected_item_sprite_list))
                # print(self.map1_1.collected_items_list)
                # print('---------------------------------------------------------------------------')

                # self.map1_1.collected_item_sprite_list.update() --> because line 94
                # print('--------------------------------')
                # print(self.hermes_sprite.change_x, 'change x')
                # print(self.hermes_sprite.position)
            else:
                # if player die
                return
                # print('Die!!')
                # self.hermes_sprite.is_dead = False
                # self.hermes_sprite.restart()
        else:
            # player pass all map
            return

    def on_draw(self):
        arcade.start_render()

        self.current_map.door_sprite_list.draw()
        self.hermes_sprite.draw()
        self.hermes_sprite.bullet_sprite_list.draw()
        self.current_map.wall_sprite_list.draw()
        self.current_map.platform_sprite_list.draw()
        self.current_map.items_sprite_list.draw()

        if self.current_map.monster is not None:
            self.current_map.monster.draw()
            self.current_map.monster.draw_hp()
            self.current_map.monster.bullet_sprite_list.draw()
        # text = f"FPS: {clock.get_fps()}"
        # arcade.draw_text(text, 50, SCREEN_HEIGHT//2, arcade.color.RED, 16)
        # print(text)

        self.status.draw()

        if self.hermes_sprite.is_dead:
            arcade.draw_text('Game Over', 320, SCREEN_HEIGHT // 2,
                             arcade.color.BLACK, 50)

        if self.game_end:
            arcade.draw_text('You win!!', 320, SCREEN_HEIGHT // 2,
                             arcade.color.BLACK, 50)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.hermes_sprite.change_x = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][0]
            # self.hermes_sprite.change_y = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][1]
            self.hermes_sprite.next_direction_x = KEY_MAP[key]

        if key == arcade.key.UP:
            # if self.physics_engine_platform.can_jump():
            #     self.hermes_sprite.change_y = JUMP_VY * DIR_OFFSETS[KEY_MAP[key]][1]
            #     self.hermes_sprite.next_direction_y = KEY_MAP[key]
            if self.physics_engines.can_jump():
                self.hermes_sprite.change_y = JUMP_VY * DIR_OFFSETS[KEY_MAP[key]][1]
                self.hermes_sprite.next_direction_y = KEY_MAP[key]

        if key == arcade.key.SPACE:
            if time.time() - self.check_attack_time >= 1:
                self.hermes_sprite.attack()
                self.check_attack_time = time.time()

        if key == arcade.key.R:
            # self.restart = True
            self.hermes_sprite.restart()
            print('Before:')
            print('all items: ', list(self.current_map.items_sprite_list))
            # print('collected items: ', list(self.map1_1.collected_item_sprite_list))
            # print('========================================================================')

            self.current_map.restart()
            print('After:')
            print('all items: ', list(self.current_map.items_sprite_list))
            # print('current items: ', list(self.map1_1.current_items_sprite_list))
            print('========================================================================')

        if key == arcade.key.X:
            self.change_map(True)

        if key == arcade.key.Z:
            self.change_map(False)

    def on_key_release(self, key, key_modifiers):
        # if key == arcade.key.UP or key == arcade.key.DOWN:
        #     self.hermes_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.hermes_sprite.change_x = 0


def main():
    window = CaveWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
