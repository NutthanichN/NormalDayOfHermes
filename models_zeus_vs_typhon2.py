import arcade
import arcade.key

BLOCK_SIZE = 20

TEXTURE_RIGHT = 0
TEXTURE_LEFT = 1

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4


class Model(arcade.Sprite):
    def __init__(self, filename, x, y, scale):
        super().__init__(filename, scale=scale)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0


class MainCharacter(arcade.AnimatedWalkingSprite):
    def __init__(self, map, scale):
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

        self.death = False

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

    def restart(self):
        x, y = self.map.get_x_y_position(self.map.has_player_at)
        self.center_x = x
        self.center_y = y
        self.death = False


class Platform(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename)

        self.trap_left = False
        self.trap_right = False
        self.trap_top = False
        self.trap_bottom = False

    def set_trap(self, left, right, top, bottom):
        self.trap_left = left
        self.trap_right = right
        self.trap_top = top
        self.trap_bottom = bottom


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
        pass

    def has_player_at(self, r, c):
        return self.map[r][c] == 'p'


class MapDrawer(Map):
    def __init__(self, map_filename, wall_pic, platform_pic,
                 ramp_left_pic, ramp_right_pic,
                 trap_left_pic, trap_right_pic, trap_top_pic, trap_bottom_pic, item_pic=''):

        super().__init__(map_filename)

        # set wall sprite list
        self.wall_sprite_list = arcade.SpriteList()
        self.init_wall_sprite_list(wall_pic)

        # set platform sprite list
        self.platform_sprite_list = arcade.SpriteList()
        self.init_platform_sprite_list(platform_pic, trap_left_pic)
        self.init_ramp_sprite_list(ramp_left_pic, ramp_right_pic)
        self.init_trap(trap_left_pic, trap_right_pic, trap_top_pic, trap_bottom_pic)

        # set item sprite list
        self.item_sprite_list = arcade.SpriteList()
        self.init_item_sprite_list(item_pic)

    def convert_to_x_y(self, r, c):
        r = r - 1
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x, y

    def get_x_y_position(self, func):
        for r in range(self.height):
            for c in range(self.width):
                if func(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    return x, y

    def create_sprite_list(self, pic_filename, lst, func, sprite_obj):
        for r in range(self.height):
            for c in range(self.width):
                if func(r, c):
                    x, y = self.convert_to_x_y(r, c)
                    sprite = sprite_obj(pic_filename)
                    sprite.center_x = x
                    sprite.center_y = y
                    lst.append(sprite)

    def init_wall_sprite_list(self, wall_pic):
        self.create_sprite_list(wall_pic, self.wall_sprite_list, self.has_wall_at, Platform)

    def init_platform_sprite_list(self, platform_pic, trap_pic):
        self.create_sprite_list(platform_pic, self.platform_sprite_list, self.has_platform_at, Platform)

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
                        self.platform_sprite_list.append(ramp_left)
                    else:
                        ramp_right = Platform(ramp_right_pic)
                        ramp_right.points = ((-ramp_right.width // 2, ramp_right.height // 2),
                                             (ramp_right.width // 2, -ramp_right.height // 2),
                                             (-ramp_right.width // 2, -ramp_right.height // 2))
                        ramp_right.right = x + (ramp_right.width // 2)
                        ramp_right.top = y + (ramp_right.height // 2)
                        self.platform_sprite_list.append(ramp_right)

    def set_trap_direction(self, r, c, pic_left, pic_right, pic_top, pic_bottom):
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
                    trap_pic, left, right, top, bottom = self.set_trap_direction(r, c,
                                                                                 pic_left, pic_right,
                                                                                 pic_top, pic_bottom)
                    sprite = Platform(trap_pic)
                    sprite.set_trap(left, right, top, bottom)
                    sprite.center_x = x
                    sprite.center_y = y

                    if trap_pic == pic_left or trap_pic == pic_right:
                        self.wall_sprite_list.append(sprite)
                    elif trap_pic == pic_top or trap_pic == pic_bottom:
                        self.platform_sprite_list.append(sprite)

    def init_item_sprite_list(self, item_pic):
        pass
