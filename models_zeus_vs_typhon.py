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



class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle


class Character(Model):
    def __init__(self, world, x, y, map, block_size):
        super().__init__(world, x, y, 0)
        self.vx = 0
        self.vy = 0
        self.is_jump = False

        self.map = map
        self.block_size = block_size

        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

    def move(self, direction):
        # self.change_x = MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        # self.change_y = MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
        self.x += self.vx

        # if self.falling or self.is_jump:
        #     self.y += self.vy
        #     self.vy += GRAVITY
        #     if self.is_falling_on_platform():
        #         self.vy = 0
        #         self.set_on_platform()

        # if not self.is_on_platform():
        #     self.y += self.vy
        #     self.vy += GRAVITY
        #     if self.is_falling_on_platform():
        #         self.vy = 0
        #         self.set_on_platform()

        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

        if not self.is_on_platform():
            self.y += self.vy
            self.vy += GRAVITY

        if self.is_falling_on_platform():
            self.vy = 0
            self.set_on_platform()

    # def jump(self):
    #     if not self.is_jump:
    #         self.is_jump = True
    #         self.vy = JUMP_VY

    def jump(self):
        if self.is_on_platform():
            self.is_jump = True
            self.vy = JUMP_VY

    def get_row_at(self, y):
        return (y - self.block_size) // self.block_size

    def get_col_at(self, x):
        return x // self.block_size

    def check_walls(self, direction):
        new_r = self.get_row_at(self.y) + DIR_OFFSETS[direction][1]
        new_c = self.get_col_at(self.x) + DIR_OFFSETS[direction][0]
        return self.map.has_wall_at(new_r, new_c)

    def check_items(self):
        pass

    def bottom_y(self):
        pass

    def update(self, delta):
        self.direction = self.next_direction

        if not self.check_walls(self.next_direction):
            self.move(self.direction)

    def set_on_platform(self):
        self.is_jump = False

    # def is_on_platform(self):
    #     p_r = self.get_row_at(self.y + CHARACTER_MARGIN_Y)
    #     p_c = self.get_col_at(self.x)
    #     if self.map.has_wall_at(p_r, p_c):
    #         self.falling = False
    #         return True
    #     else:
    #         self.falling = True
    #         return False

    def is_falling_on_platform(self):
        new_r = self.get_row_at(self.y) + DIR_OFFSETS[DIR_DOWN][1]
        c = self.get_col_at(self.x)
        return self.map.has_wall_at(new_r, c)

    def is_on_platform(self):
        new_r = self.get_row_at(self.y) + DIR_OFFSETS[DIR_DOWN][1]
        c = self.get_col_at(self.x)
        # make sure there is platform at lower row
        if self.map.has_wall_at(new_r, c):
            x, new_y = self.map.r_c_to_x_y(new_r, c)

            if x - BLOCK_MARGIN <= x <= x + BLOCK_MARGIN:
                return True

        self.falling = True
        return False


class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Map:
    def __init__(self, world):
        self.map1_1 = ['########################################',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#......................................#',
                       '#..............##########..............#',
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

        self.map1_1_old = ['####################',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '#..................#',
                           '####################']

        self.height = len(self.map1_1)
        self.width = len(self.map1_1[0])

    def has_wall_at(self, r, c):
        return self.map1_1[r][c] == '#'

    def has_space_at(self, r, c):
        return self.map1_1[r][c] == '.'

    def r_c_to_x_y(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = (r * BLOCK_SIZE) + BLOCK_SIZE + (BLOCK_SIZE // 2)
        return x, y


class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size

        self.map1_1 = Map(self)
        self.hermes = Character(self, 40, 50, self.map1_1, self.block_size)

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.hermes.next_direction = KEY_MAP[key]

            self.hermes.vx = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][0]

            if key == arcade.key.UP:
                self.hermes.jump()
            # self.hermes.vy = MOVEMENT_VX * DIR_OFFSETS[KEY_MAP[key]][1]

        # if key == arcade.key.UP:
        #     self.hermes.jump()
        #     # self.hermes.change_y = MOVEMENT_VX
        #     self.hermes.direction = DIR_UP
        # # elif key == arcade.key.DOWN:
        # #     self.hermes.change_y = -MOVEMENT_SPEED
        # #     self.hermes.direction = DIR_DOWN
        # elif key == arcade.key.RIGHT:
        #     self.hermes.vx = MOVEMENT_VX
        #     self.hermes.direction = DIR_RIGHT
        # elif key == arcade.key.LEFT:
        #     self.hermes.vx = -MOVEMENT_VX
        #     self.hermes.direction = DIR_LEFT

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.hermes.vy = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.hermes.vx = 0

    def update(self, delta):
        self.hermes.update(delta)

