"""16/4/19 add monster, monster can move only on platform, try to change map (still ugly code)
26/4/19 22:00-00:34 don't forget to make monster die next time"""
import arcade
from models_zeus_vs_typhon2 import MainCharacter, MapDrawer, Status
import my_physics
from pyglet import clock
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


class CaveWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.SADDLE_BROWN)

        # init maps
        self.maps = set_up_maps('map/first_scene.txt', 'map/map1_1.txt', 'map/map1_2.txt',
                                'map/map2_1.txt', 'map/map2_2.txt',
                                'map/map3_1.txt', 'map/map3_2.txt',
                                'map/end_scene.txt')
        self.current_map = self.maps[0]

        # init player
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
        # init physics engine
        self.physics_engines = None
        self.set_up_physics_engines(self.hermes_sprite, self.current_map)

        # init status(drawer)
        self.status = Status(SCREEN_WIDTH, SCREEN_HEIGHT, self.hermes_sprite, self.current_map,
                             'images/hp_lvl_20.png', 'images/weapon_lvl_20.png', 'images/key_18x19.PNG')

        # game state
        self.check_attack_time = 0
        self.game_end = False
        self.god_mode = False

    def set_up_physics_engines(self, player, current_map):
        self.physics_engines = my_physics.PhysicsEngine(player, current_map.wall_sprite_list,
                                                        current_map.platform_sprite_list, GRAVITY)

    def change_map(self, forward):
        next_index = self.maps.index(self.current_map) + 1
        previous_index = self.maps.index(self.current_map) - 1
        if forward:
            if next_index <= len(self.maps) - 1:
                self.current_map = self.maps[next_index]
            else:
                # print("Can't move forward")
                return
        else:
            if previous_index >= 0:
                self.current_map = self.maps[previous_index]
            else:
                # print("Can't move backward")
                return

        self.hermes_sprite.map = self.current_map
        self.hermes_sprite.set_up_position()

        self.set_up_physics_engines(self.hermes_sprite, self.current_map)

    def restart(self):
        self.game_end = False
        self.maps = set_up_maps('map/first_scene.txt', 'map/map1_1.txt', 'map/map1_2.txt',
                                'map/map2_1.txt', 'map/map2_2.txt',
                                'map/map3_1.txt', 'map/map3_2.txt',
                                'map/end_scene.txt')
        self.current_map = self.maps[0]
        self.hermes_sprite.map = self.current_map
        self.hermes_sprite.set_up_position()
        self.set_up_physics_engines(self.hermes_sprite, self.current_map)
        self.hermes_sprite.restart()

    def draw_game_over_text(self):
        arcade.draw_text('Game Over', 320, SCREEN_HEIGHT // 2,
                         arcade.color.BLACK, 50)
        arcade.draw_text("Press [ENTER] to restart", 280, (SCREEN_HEIGHT // 2) - 50,
                         arcade.color.BLACK, 30)

    def draw_you_win_text(self):
        arcade.draw_text('You win!!', 320, SCREEN_HEIGHT // 2,
                         arcade.color.BLACK, 50)
        arcade.draw_text("Press [ENTER] to restart", 280, (SCREEN_HEIGHT // 2) - 50,
                         arcade.color.BLACK, 30)

    def draw_instruction_text(self):
        arcade.draw_text('How to play:', 100, SCREEN_HEIGHT - 200,
                         arcade.color.BLACK, 25)
        arcade.draw_text('Press [ < ] button to move left', 100, SCREEN_HEIGHT - 250,
                         arcade.color.BLACK, 20)
        arcade.draw_text('Press [ > ] button to move right', 100, SCREEN_HEIGHT - 300,
                         arcade.color.BLACK, 20)
        arcade.draw_text('Press [ ^ ] button to jump', 100, SCREEN_HEIGHT - 350,
                         arcade.color.BLACK, 20)
        arcade.draw_text('Press [SPACEBAR] to attack', 100, SCREEN_HEIGHT - 400,
                         arcade.color.BLACK, 20)
        arcade.draw_text('::: Press [ENTER] to start game :::', 140, SCREEN_HEIGHT - 550,
                         arcade.color.BLACK, 25)

    def draw_welcome_text(self):
        arcade.draw_text('Normal Day of Hermes', 150, SCREEN_HEIGHT - 80,
                         arcade.color.BLACK, 50)

    def update(self, delta):
        if not self.game_end:
            if not self.hermes_sprite.is_dead:
                # manage collected items
                hit_items = arcade.check_for_collision_with_list(self.hermes_sprite, self.current_map.items_sprite_list)
                if len(hit_items) > 0:
                    for i in hit_items:
                        self.current_map.items_sprite_list.remove(i)
                        self.status.check_and_set_player_status(i)
                        i.kill()

                # manage enter door
                for door in self.current_map.door_sprite_list:
                    if door.has_player(self.hermes_sprite) and door.active:
                        # if door.is_last_door:
                        #     self.game_end = True
                        # print('Enter door')
                        self.change_map(True)

                # manage monster
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

                        # case player's bullet hit monster's bullet
                        for player_bullet in self.hermes_sprite.bullet_sprite_list:
                            for monster_bullet in self.current_map.monster.bullet_sprite_list:
                                if arcade.check_for_collision(player_bullet, monster_bullet):
                                    player_bullet.kill()
                                    monster_bullet.kill()

                        self.current_map.monster.update()
                        self.current_map.monster.bullet_sprite_list.update()
                    else:
                        self.current_map.monster = None

                # update player
                self.hermes_sprite.update_animation()
                self.hermes_sprite.update_status()
                self.hermes_sprite.bullet_sprite_list.update()
                # self.hermes_sprite.update()

                # update physics engine
                self.physics_engines.update()

                # update map
                self.current_map.wall_sprite_list.update()
                self.current_map.platform_sprite_list.update()
                self.current_map.door_sprite_list.update()
                self.current_map.items_sprite_list.update()
                self.current_map.collected_item_sprite_list.update()

                # print(self.hermes_sprite.change_x, 'change x')
                # print(self.hermes_sprite.position)
            else:
                # case player die
                return
                # print('Die!!')
                # self.hermes_sprite.is_dead = False
        else:
            # case player pass all map
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

        if self.maps.index(self.current_map) == 0:
            self.draw_welcome_text()
            self.draw_instruction_text()
        elif self.maps.index(self.current_map) > 0:
            self.status.draw()
            if self.current_map == self.maps[-1]:
                self.draw_you_win_text()

        if self.hermes_sprite.is_dead:
            self.draw_game_over_text()

        # if self.game_end:
        #     self.draw_you_win_text()

        if self.god_mode:
            arcade.draw_text('God mode', 25, SCREEN_HEIGHT - 20, arcade.color.BLACK, 12)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.hermes_sprite.change_x = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][0]
            # self.hermes_sprite.change_y = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][1]
            self.hermes_sprite.next_direction_x = KEY_MAP[key]

        if key == arcade.key.UP:
            if self.physics_engines.can_jump():
                self.hermes_sprite.change_y = JUMP_VY * DIR_OFFSETS[KEY_MAP[key]][1]
                self.hermes_sprite.next_direction_y = KEY_MAP[key]

        if key == arcade.key.SPACE:
            if time.time() - self.check_attack_time >= 1:
                self.hermes_sprite.attack()
                self.check_attack_time = time.time()

        if key == arcade.key.R:
            # print('Before:')
            # print('all items: ', list(self.current_map.items_sprite_list))
            if self.god_mode:
                self.restart()
            # self.current_map.restart()
            # print('After:')
            # print('all items: ', list(self.current_map.items_sprite_list))
            # print('========================================================================')

        if key == arcade.key.ENTER:
            if self.maps.index(self.current_map) == 0:
                self.change_map(True)
            else:
                if self.god_mode or self.game_end or self.hermes_sprite.is_dead:
                    self.restart()

        if key == arcade.key.X:
            if self.god_mode:
                self.change_map(True)

        if key == arcade.key.Z:
            if self.god_mode:
                self.change_map(False)

        if key == arcade.key.G:
            self.god_mode = True
        elif key == arcade.key.N:
            self.god_mode = False

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
