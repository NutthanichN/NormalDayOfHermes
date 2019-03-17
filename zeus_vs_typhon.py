import arcade
from models_zeus_vs_typhon import World, Character

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class MapDrawer:
    def __init__(self, map):
        self.map = map
        self.width = self.map.width
        self.height = self.map.height

        self.wall_sprite = arcade.Sprite('images/block_40.PNG')

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.map.has_wall_at(r, c):
                    self.draw_sprite(self.wall_sprite, r, c)

    def get_sprite_position(self, r, c):
        r = r - 1
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x, y


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

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
        self.hermes_sprite = ModelSprite('images/Hermes/Hermes_right_w1.PNG', model=self.world.hermes)
        self.map_drawer = MapDrawer(self.world.map1_1)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()

        self.map_drawer.draw()
        self.hermes_sprite.draw()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)


def main():
    window = CaveWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()