import arcade
import arcade.key
from random import randint
import time
from arcade.geometry import check_for_collision

BLOCK_SIZE = 20

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4


class MainCharacter(arcade.AnimatedWalkingSprite):
    """can jump 5 block"""
    def __init__(self, map, scale, bullet_pic):
        self.map = map
        x, y = self.map.get_x_y_position(self.map.has_player_at)

        super().__init__(scale, center_x=x, center_y=y)

        # set texture
        self.stand_right_textures = []
        self.stand_left_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        # direction will check if character hits wall or not
        self.direction_x = self.check_direction_x()
        self.direction_y = self.check_direction_y()
        self.next_direction_x = DIR_STILL
        self.next_direction_y = DIR_STILL

        self.is_dead = False

        self.current_hp_lvl = 3
        self.current_weapon_lvl = 3
        self.current_key = 0
        self.current_super_magic_potion = 0

        self.bullet_pic = bullet_pic
        self.bullet_sprite_list = arcade.SpriteList()

    def check_direction_x(self):
        if self.change_x == 0:
            return DIR_STILL
        elif self.change_x > 0:
            return DIR_RIGHT
        elif self.change_x < 0:
            return DIR_LEFT

    def check_direction_y(self):
        if self.change_y == 0:
            return DIR_STILL
        elif self.change_y > 0:
            return DIR_UP
        elif self.change_y < 0:
            return DIR_DOWN

    def init_walk_right_and_left(self, *args):
        """Right is default, left is mirrored"""
        for i in args:
            self.walk_right_textures.append(arcade.load_texture(i))
            self.walk_left_textures.append(arcade.load_texture(i, mirrored=True))

    def init_stand_right_and_left(self, filename):
        """Right is default, left is mirrored"""
        self.stand_right_textures.append(arcade.load_texture(filename))
        self.stand_left_textures.append(arcade.load_texture(filename, mirrored=True))

    def restart_statuses(self):
        self.current_hp_lvl = 3
        self.current_weapon_lvl = 3
        self.current_key = 0
        self.current_super_magic_potion = 0

    def set_up_position(self):
        x, y = self.map.get_x_y_position(self.map.has_player_at)
        self.center_x = x
        self.center_y = y

    def set_map(self, map):
        self.map = map

    def restart(self):
        self.set_up_position()
        self.restart_statuses()
        self.is_dead = False

    def is_hit_by(self, sprite):
        return check_for_collision(sprite, self)

    def calculate_damage(self, bullet):
        """cal bullet damage and update status"""
        if 0 < self.current_hp_lvl:
            self.current_hp_lvl -= bullet.damage

    def update_status(self):
        if self.current_hp_lvl == 0:
            self.is_dead = True

    def attack(self):
        bullet = Bullet(self.bullet_pic)
        bullet.change_x = 5
        bullet.damage = self.current_weapon_lvl * 100
        bullet.center_y = self.center_y
        if self.direction_x == DIR_LEFT:
            bullet.right = self.left
            bullet.change_x = -bullet.change_x
        else:
            bullet.left = self.right
            bullet.change_x = abs(bullet.change_x)

        bullet.first_center_x = bullet.center_x
        bullet.distance *= self.current_weapon_lvl
        # bullet.distance = 200
        self.bullet_sprite_list.append(bullet)


class Monster(arcade.Sprite):
    MARGIN_Y = 20
    MOVEMENT_VX = 3

    TEXTURE_RIGHT = 0
    TEXTURE_LEFT = 1

    def __init__(self, filename, map, bullet_pic):
        super().__init__()

        self.textures = []
        texture_right = arcade.load_texture(filename)
        self.textures.append(texture_right)
        texture_left = arcade.load_texture(filename, mirrored=True)
        self.textures.append(texture_left)

        self.set_texture(self.TEXTURE_RIGHT)

        self.map = map
        self.hp = 2000
        self.is_dead = False

        self.change_x = self.MOVEMENT_VX

        self.bullet_pic = bullet_pic
        self.bullet_sprite_list = arcade.SpriteList()

    def set_hp(self, hp):
        self.hp = hp

    def adjust_center_y(self):
        # self.center_y += abs((self.center_y - self.bottom) - BLOCK_SIZE)
        self.center_y += self.MARGIN_Y

    def is_hit_by(self, player):
        return check_for_collision(player, self)

    def is_on_platform(self):
        for p in self.map.platform_sprite_list:
            if not p.is_ramp:
                if p.center_y <= self.bottom <= p.top and p.left <= self.center_x <= p.right:
                    return True
        print('not on platform')
        return False

    def attack(self):
        bullet = Bullet(self.bullet_pic)
        bullet.change_x = 7
        bullet.damage = 1
        bullet.distance = 200
        bullet.center_y = self.center_y
        if self.change_x < 0:
            bullet.right = self.left
            bullet.change_x = -bullet.change_x
        else:
            bullet.left = self.right
            bullet.change_x = abs(bullet.change_x)

        self.bullet_sprite_list.append(bullet)

    def calculate_damage(self, bullet):
        """cal bullet damage and update status"""
        if 0 < self.hp:
            self.hp -= bullet.damage

    def draw_hp(self):
        arcade.draw_text(f"{self.hp}", self.left, self.top + 5, arcade.color.BLACK)

    def update(self):
        # if there is no platform just move to another direction
        if not self.is_on_platform():
            self.change_x = -self.change_x

        # set texture
        if self.change_x < 0:
            self.set_texture(self.TEXTURE_LEFT)
        else:
            self.set_texture(self.TEXTURE_RIGHT)

        self.center_x += self.change_x


class Bullet(arcade.Sprite):
    TEXTURE_RIGHT = 0
    TEXTURE_LEFT = 1

    def __init__(self, filename):
        super().__init__(filename)

        self.textures = []
        texture_right = arcade.load_texture(filename)
        self.textures.append(texture_right)
        texture_left = arcade.load_texture(filename, mirrored=True)
        self.textures.append(texture_left)

        self.set_texture(self.TEXTURE_RIGHT)

        # default --> later set in player's class
        self.damage = 0

        # default
        self.first_center_x = 0
        self.distance = 50

        # default
        self.change_x = 0

    def update(self):
        # kill itself
        if abs(self.center_x - self.first_center_x) == self.distance:
            self.kill()

        # set texture
        if self.change_x < 0:
            self.set_texture(self.TEXTURE_LEFT)
        else:
            self.set_texture(self.TEXTURE_RIGHT)

        self.center_x += self.change_x


class Platform(arcade.Sprite):
    TRAP_MARGIN = 5

    def __init__(self, filename):
        super().__init__(filename)

        self.is_ramp = False

        self.trap_left = False
        self.trap_right = False
        self.trap_top = False
        self.trap_bottom = False

    def set_trap(self, left, right, top, bottom):
        self.trap_left = left
        self.trap_right = right
        self.trap_top = top
        self.trap_bottom = bottom

    def init_trap_center(self, x, y):
        self.center_x = x
        self.center_y = y

        if self.trap_left:
            self.center_x -= self.TRAP_MARGIN
        if self.trap_right:
            self.center_x += self.TRAP_MARGIN
        if self.trap_top:
            self.center_y += self.TRAP_MARGIN
        if self.trap_bottom:
            self.center_y -= self.TRAP_MARGIN


class Item(arcade.Sprite):
    HOVER_MARGIN = 5

    def __init__(self, filename):
        super().__init__(filename)

        self.key = False
        self.add_hp = False
        self.add_weapon_ability = False
        self.stun_monster = False


class Door(arcade.Sprite):
    MARGIN_X = 30
    MARGIN_Y = 40

    RED = 0
    GREEN = 1

    def __init__(self, door_red_pic, door_green_pic):
        super().__init__()

        # add textures
        self.textures = []
        texture_red_light = arcade.load_texture(door_red_pic)
        texture_green_light = arcade.load_texture(door_green_pic)
        self.textures.append(texture_red_light)
        self.textures.append(texture_green_light)

        # default is active
        self.active = True
        self.set_texture(self.GREEN)

    def set_active(self, bool):
        self.active = bool

    def adjust_position(self):
        self.center_y += self.MARGIN_Y - 10

    def has_player(self, player):
        if self.left + (self.MARGIN_X // 2) < player.center_x < self.right - (self.MARGIN_X // 2):
            if self.bottom < player.center_y < self.top:
                return True
            return False
        return False

    def update(self):
        if self.active:
            self.set_texture(self.GREEN)
        else:
            self.set_texture(self.RED)


class Map:
    def __init__(self, map_filename):
        self.map = open(map_filename).read().splitlines()
        self.height = len(self.map)
        self.width = len(self.map[0])

    def has_wall_at(self, r, c):
        return self.map[r][c] == '#'

    def has_space_at(self, r, c):
        return self.map[r][c] == '.'

    def has_platform_at(self, r, c):
        return self.map[r][c] == '='

    def has_ramp(self, r, c):
        return self.map[r][c] == '<' or self.map[r][c] == '>'

    def has_ramp_left_at(self, r, c):
        return self.map[r][c] == '<'

    def has_ramp_right_at(self, r, c):
        return self.map[r][c] == '>'

    def has_trap_at(self, r, c):
        return self.map[r][c] == '_' or self.map[r][c] == '-' \
               or self.map[r][c] == '{' or self.map[r][c] == '}'

    def has_item_at(self, r, c):
        """
        1 = key
        2 = hp_potion
        3 = magic_potion
        4 = super_magic_potion
        """
        return self.map[r][c] == '1' or self.map[r][c] == '2' \
               or self.map[r][c] == '3' or self.map[r][c] == '4'

    def has_player_at(self, r, c):
        return self.map[r][c] == 'p'

    def has_door_at(self, r, c):
        return self.map[r][c] == 'A' or self.map[r][c] == 'D'

    def has_monster_at(self, r, c):
        return self.map[r][c] == 'm'


class MapDrawer(Map):
    def __init__(self, map_filename, wall_pic, platform_pic,
                 ramp_left_pic, ramp_right_pic,
                 trap_left_pic, trap_right_pic, trap_top_pic, trap_bottom_pic,
                 key_pic, hp_potion_pic, magic_potion_pic, super_magic_potion_pic,
                 door_red_pic, door_green_pic, monster_pic, monster_bullet_pic):

        super().__init__(map_filename)

        # items pictures
        self.key_pic = key_pic
        self.hp_potion_pic = hp_potion_pic
        self.magic_potion_pic = magic_potion_pic
        self.super_magic_potion_pic = super_magic_potion_pic

        # set wall sprite list
        self.wall_sprite_list = arcade.SpriteList()
        self.init_wall_sprite_list(wall_pic)

        # set platform sprite list
        self.platform_sprite_list = arcade.SpriteList()
        self.init_platform_sprite_list(platform_pic, trap_left_pic)
        self.init_ramp_sprite_list(ramp_left_pic, ramp_right_pic)
        self.init_trap(trap_left_pic, trap_right_pic, trap_top_pic, trap_bottom_pic)

        # set item sprite list
        self.items_sprite_list = arcade.SpriteList()
        self.collected_item_sprite_list = arcade.SpriteList()
        self.init_item_sprite_list(key_pic, hp_potion_pic, magic_potion_pic, super_magic_potion_pic)

        # set door sprite list
        self.door_sprite_list = arcade.SpriteList()
        self.init_door_sprite_list(door_red_pic, door_green_pic)

        # init monster
        self.monster = self.init_monster_sprite(monster_pic, monster_bullet_pic)

        self.count_time = True

    def convert_to_x_y(self, r, c):
        r = r - 1
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x, y

    def get_x_y_position(self, condition):
        for r in range(self.height):
            for c in range(self.width):
                if condition(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    return x, y

    def _create_sprite_list(self, pic_filename, lst, condition, sprite_obj):
        for r in range(self.height):
            for c in range(self.width):
                if condition(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    sprite = sprite_obj(pic_filename)
                    sprite.center_x = x
                    sprite.center_y = y
                    lst.append(sprite)

    def init_wall_sprite_list(self, wall_pic):
        self._create_sprite_list(wall_pic, self.wall_sprite_list, self.has_wall_at, Platform)

    def init_platform_sprite_list(self, platform_pic, trap_pic):
        self._create_sprite_list(platform_pic, self.platform_sprite_list, self.has_platform_at, Platform)

    def init_ramp_sprite_list(self, ramp_left_pic, ramp_right_pic):
        for r in range(self.height):
            for c in range(self.width):
                if self.has_ramp(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    if self.has_ramp_left_at(r, c):
                        ramp_left = Platform(ramp_left_pic)
                        ramp_left.points = ((-ramp_left.width // 2, -ramp_left.height // 2),
                                            (ramp_left.width // 2, -ramp_left.height // 2),
                                            (ramp_left.width // 2, ramp_left.height // 2))
                        ramp_left.right = x + (ramp_left.width // 2)
                        ramp_left.top = y + (ramp_left.height // 2)
                        ramp_left.is_ramp = True
                        self.platform_sprite_list.append(ramp_left)
                    else:
                        ramp_right = Platform(ramp_right_pic)
                        ramp_right.points = ((-ramp_right.width // 2, ramp_right.height // 2),
                                             (ramp_right.width // 2, -ramp_right.height // 2),
                                             (-ramp_right.width // 2, -ramp_right.height // 2))
                        ramp_right.right = x + (ramp_right.width // 2)
                        ramp_right.top = y + (ramp_right.height // 2)
                        ramp_right.is_ramp = True
                        self.platform_sprite_list.append(ramp_right)

    def set_up_trap_direction(self, r, c, pic_left, pic_right, pic_top, pic_bottom):
        if self.map[r][c] == '_':
            return pic_top, False, False, True, False
        elif self.map[r][c] == '-':
            return pic_bottom, False, False, False, True
        elif self.map[r][c] == '{':
            return pic_left, True, False, False, False
        elif self.map[r][c] == '}':
            return pic_right, False, True, False, False

    def init_trap(self, pic_left, pic_right, pic_top, pic_bottom):
        for r in range(self.height):
            for c in range(self.width):
                if self.has_trap_at(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    trap_pic, left, right, top, bottom = self.set_up_trap_direction(r, c,
                                                                                    pic_left, pic_right,
                                                                                    pic_top, pic_bottom)
                    sprite = Platform(trap_pic)
                    sprite.set_trap(left, right, top, bottom)
                    sprite.init_trap_center(x, y)
                    # sprite.center_x = x
                    # sprite.center_y = y

                    if trap_pic == pic_left or trap_pic == pic_right:
                        self.wall_sprite_list.append(sprite)
                    elif trap_pic == pic_top or trap_pic == pic_bottom:
                        self.platform_sprite_list.append(sprite)

    def set_up_item_pic(self, r, c, key_pic, hp_potion_pic, magic_potion_pic, super_magic_potion_pic):
        if self.map[r][c] == '1':
            return key_pic
        elif self.map[r][c] == '2':
            return hp_potion_pic
        elif self.map[r][c] == '3':
            return magic_potion_pic
        elif self.map[r][c] == '4':
            return super_magic_potion_pic

    def set_up_item_ability(self, r, c, item):
        if self.map[r][c] == '1':
            item.key = True
        elif self.map[r][c] == '2':
            item.add_hp = True
        elif self.map[r][c] == '3':
            item.add_weapon_ability = True
        elif self.map[r][c] == '4':
            num = randint(0, 2)
            if num == 0:
                item.stun_monster = True
            elif num == 1:
                item.add_hp = True
            else:
                item.add_weapon_ability = True

    def init_item_sprite_list(self, key_pic, hp_potion_pic, magic_potion_pic, super_magic_potion_pic):
        for r in range(self.height):
            for c in range(self.width):
                if self.has_item_at(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    item_pic = self.set_up_item_pic(r, c, key_pic, hp_potion_pic,
                                                    magic_potion_pic, super_magic_potion_pic)
                    item = Item(item_pic)
                    item.center_x = x
                    item.center_y = y + item.HOVER_MARGIN
                    self.set_up_item_ability(r, c, item)
                    self.items_sprite_list.append(item)

    def init_door_sprite_list(self, door_red_pic, door_green_pic):
        for r in range(self.height):
            for c in range(self.width):
                if self.has_door_at(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    door = Door(door_red_pic, door_green_pic)
                    # door.set_active(True)
                    door.center_x = x
                    door.center_y = y
                    door.adjust_position()
                    if self.map[r][c] == 'A':
                        door.set_active(True)
                    else:
                        door.set_active(False)
                    self.door_sprite_list.append(door)

    def init_monster_sprite(self, monster_pic, monster_bullet_pic):
        for r in range(self.height):
            for c in range(self.width):
                if self.has_monster_at(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    monster = Monster(monster_pic, self, monster_bullet_pic)
                    monster.center_x = x
                    monster.center_y = y
                    monster.adjust_center_y()
                    return monster

    def restart(self):
        self.items_sprite_list = arcade.SpriteList()
        self.init_item_sprite_list(self.key_pic, self.hp_potion_pic,
                                   self.magic_potion_pic, self.super_magic_potion_pic)
        # for item in self.collected_item_sprite_list:
        #     self.items_sprite_list.append(item)
        #     self.collected_item_sprite_list.remove(item)


class Status:
    MAX_HP_LVL = 8
    MAX_WEAPON_LVL = 6

    def __init__(self, screen_width, screen_height, player, map, hp_lvl_pic, weapon_lvl_pic, key_pic):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.map = map

        # collect pics to variable for reuse
        self.hp_lvl_pic = hp_lvl_pic
        self.weapon_lvl_pic = weapon_lvl_pic

        self.hp_lvl_sprite_list = arcade.SpriteList()
        self.weapon_lvl_sprite_list = arcade.SpriteList()

        self.init_hp_lvl()
        self.init_weapon_lvl()

        self.start_time = time.time()
        self.end_time = None
        self.delta_time = None

    def init_hp_lvl(self):
        # sprite part
        # still use magic number
        x = self.screen_width - 220
        y = self.screen_height - 30
        for i in range(self.MAX_HP_LVL):
            hp = arcade.Sprite(self.hp_lvl_pic)
            new_x = x + BLOCK_SIZE
            hp.center_x = new_x
            hp.center_y = y
            self.hp_lvl_sprite_list.append(hp)
            x = new_x

    def init_weapon_lvl(self):
        # sprite part
        # still use magic number
        x = self.screen_width - 220
        y = self.screen_height - 30 - BLOCK_SIZE
        for i in range(self.MAX_WEAPON_LVL):
            weapon = arcade.Sprite(self.weapon_lvl_pic)
            new_x = x + BLOCK_SIZE
            weapon.center_x = new_x
            weapon.center_y = y
            self.weapon_lvl_sprite_list.append(weapon)
            x = new_x

    def draw_hp_lvl(self):
        # text part
        # still use magic number
        x = self.screen_width - 310
        y = self.screen_height - 40
        arcade.draw_text('HP', x, y, arcade.color.BLACK, font_size=15)

        # current_hp_lvl = arcade.SpriteList()
        # for i in range(self.MAX_HP_LVL):
        for i in range(self.player.current_hp_lvl):
            if i < self.MAX_HP_LVL:
                self.hp_lvl_sprite_list[i].draw()
        #         current_hp_lvl.append(self.hp_lvl_sprite_list[i])
        # current_hp_lvl.draw()

    def draw_weapon_lvl(self):
        # text part
        # still use magic number
        x = self.screen_width - 310
        y = self.screen_height - 40 - BLOCK_SIZE
        arcade.draw_text('Weapon lvl', x, y, arcade.color.BLACK, font_size=15)

        # current_weapon_lvl = arcade.SpriteList()
        # for i in range(self.MAX_WEAPON_LVL):
        for i in range(self.player.current_weapon_lvl):
            if i < self.MAX_WEAPON_LVL:
                self.weapon_lvl_sprite_list[i].draw()
        #         current_weapon_lvl.append(self.weapon_lvl_sprite_list[i])
        # current_weapon_lvl.draw()

    def draw_key_number(self):
        x = self.screen_width - 310
        y = self.screen_height - 40 - (2 * BLOCK_SIZE) - 5
        arcade.draw_text(f'Key x {str(self.player.current_key)}', x, y, arcade.color.BLACK, font_size=15)

    def draw_super_magic_potion_number(self):
        x = self.screen_width - 310 + 80
        y = self.screen_height - 40 - (2 * BLOCK_SIZE) - 5
        arcade.draw_text(f'Super magic potion x {str(self.player.current_super_magic_potion)}',
                         x, y, arcade.color.BLACK, font_size=15)

    def draw_time(self):
        self.delta_time = self.end_time - self.start_time
        hour = self.delta_time // 3600
        minute = (self.delta_time % 3600) // 60
        second = (self.delta_time % 3600) % 60

        x = self.screen_width - 850
        y = self.screen_height - 40 - BLOCK_SIZE
        # print(self.delta_time)
        arcade.draw_text(f'Time {int(hour)}:{int(minute)}:{int(second)}', x, y, arcade.color.BLACK, font_size=15)

    def draw(self):
        self.end_time = time.time()
        self.draw_time()
        self.draw_hp_lvl()
        self.draw_weapon_lvl()
        self.draw_key_number()
        self.draw_super_magic_potion_number()

    def check_and_set_player_status(self, item):
        if item.key:
            self.player.current_key += 1
        elif item.add_hp:
            self.player.current_hp_lvl += 1
        elif item.add_weapon_ability:
            self.player.current_weapon_lvl += 1
        elif item.stun_monster:
            self.player.current_super_magic_potion += 1

# bug --> add magic after hp but it add both hp and magic // now solve