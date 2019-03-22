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
    def __init__(self, x, y, scale):
        super().__init__(scale, center_x=x, center_y=y)
        self.stand_right_textures = []
        self.stand_left_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        self.direction_x = self.check_direction_x()
        self.direction_y = self.check_direction_y()
        self.next_direction_x = DIR_STILL
        self.next_direction_y = DIR_STILL

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

    def init_walk_left(self, *args):
        for i in args:
            self.walk_left_textures.append(arcade.load_texture(i, mirrored=True))

    def init_walk_right(self, *args):
        for i in args:
            self.walk_right_textures.append(arcade.load_texture(i))

    def init_stand_right(self, filename):
        self.stand_right_textures.append(arcade.load_texture(filename))

    def init_stand_left(self, filename):
        self.stand_left_textures.append(arcade.load_texture(filename, mirrored=True))


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

    def has_item_at(self, r, c):
        pass


class MapDrawer(Map):
    def __init__(self, map_filename, wall_pic, platform_pic, item_pic=''):
        super().__init__(map_filename)

        # set wall sprite list
        self.wall_sprite_list = arcade.SpriteList()
        self.set_wall_sprite_list(wall_pic)

        # set platform sprite list
        self.platform_sprite_list = arcade.SpriteList()
        self.set_platform_sprite_list(platform_pic)

        # set item sprite list
        self.item_sprite_list = arcade.SpriteList()
        self.set_item_sprite_list(item_pic)

    def set_sprite_list(self, pic_filename, lst, func):
        for r in range(self.height):
            for c in range(self.width):
                if func(r, c):
                    x, y = self.get_sprite_position(r, c)
                    wall_sprite = arcade.Sprite(pic_filename)
                    wall_sprite.center_x = x
                    wall_sprite.center_y = y
                    lst.append(wall_sprite)

    def set_wall_sprite_list(self, wall_pic):
        self.set_sprite_list(wall_pic, self.wall_sprite_list, self.has_wall_at)

    def set_platform_sprite_list(self, platform_pic):
        self.set_sprite_list(platform_pic, self.platform_sprite_list, self.has_platform_at)

    def set_item_sprite_list(self, item_pic):
        pass

    def get_sprite_position(self, r, c):
        r = r - 1
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x, y
