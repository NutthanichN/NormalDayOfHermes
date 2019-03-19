import arcade
import arcade.key

MOVEMENT_VX = 5
JUMP_VY = 20
GRAVITY = -1

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

BLOCK_MARGIN = 10
BLOCK_SIZE = 20
CHARACTER_MARGIN_Y = 10       # check this value again


class Character(arcade.Sprite):
    def __init__(self, filename, x, y, scale):
        super().__init__(filename, scale=scale)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

        self.direction = DIR_STILL

    def move(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update(self):
        self.move()


class Map:
    def __init__(self):
        self.map1_1 = ['########################################',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#..............==========..............#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '########################################']

        self.height = len(self.map1_1)
        self.width = len(self.map1_1[0])

    def has_wall_at(self, r, c):
        return self.map1_1[r][c] == '#'

    def has_space_at(self, r, c):
        return self.map1_1[r][c] == '.'

    def has_platform_at(self, r, c):
        return self.map1_1[r][c] == '='

    def r_c_to_x_y(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = (r * BLOCK_SIZE) + BLOCK_SIZE + (BLOCK_SIZE // 2)
        return x, y


class MapDrawer:
    def __init__(self, map, player, filename):
        self.map = map
        self.width = self.map.width
        self.height = self.map.height

        self.player = player

        # set wall sprite list
        self.wall_sprite_list = arcade.SpriteList()
        self.set_wall_sprite_list(filename)

        # set platform sprite list
        self.platform_sprite_list = arcade.SpriteList()
        self.set_platform_sprite_list(filename)

    def set_sprite_list(self, filename, lst, func):
        for r in range(self.height):
            for c in range(self.width):
                if func(r, c):
                    x, y = self.get_sprite_position(r, c)
                    wall_sprite = arcade.Sprite(filename)
                    wall_sprite.center_x = x
                    wall_sprite.center_y = y
                    lst.append(wall_sprite)

    def set_wall_sprite_list(self, filename):
        self.set_sprite_list(filename, self.wall_sprite_list, self.map.has_wall_at)

    def set_platform_sprite_list(self, filename):
        self.set_sprite_list(filename, self.platform_sprite_list, self.map.has_platform_at)

    def set_item_sprite_list(self, filename):
        pass

    def get_sprite_position(self, r, c):
        r = r - 1
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x, y
