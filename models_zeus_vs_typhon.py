import arcade.key

MOVEMENT_SPEED = 5


class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle


class Player(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.change_x = 0
        self.change_y = 0

    def update(self, delta):
        if self.x > self.world.width or self.x < 0:
            # self.x = 0
            self.change_x = 0
        elif self.y > self.world.height or self.y < 0:
            # self.y = 0
            self.change_y = 0

        self.x += self.change_x
        self.y += self.change_y


class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size

        self.hermes = Player(self, width // 2, height // 2)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT:
            self.hermes.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.hermes.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.hermes.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.hermes.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.hermes.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.hermes.change_x = 0

    def update(self, delta):
        self.hermes.update(delta)

