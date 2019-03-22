"""
Physics engines for top-down or platformers.
"""
# pylint: disable=too-many-arguments, too-many-locals, too-few-public-methods

from arcade.geometry import check_for_collision_with_list
from arcade.geometry import check_for_collision
from arcade.sprite import Sprite
from arcade.sprite_list import SpriteList

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

SAFE_SPACE = 1


class PhysicsEngineSimple:
    """
    This class will move everything, and take care of collisions.
    """

    def __init__(self, player_sprite: Sprite, walls: SpriteList):
        """
        Constructor.
        """
        assert(isinstance(player_sprite, Sprite))
        assert(isinstance(walls, SpriteList))
        self.player_sprite = player_sprite
        self.walls = walls

        self.player_sprite.direction_x = self.player_sprite.check_direction_x()
        self.player_sprite.direction_y = self.player_sprite.check_direction_y()
        self.player_sprite.next_direction_x = DIR_STILL
        self.player_sprite.next_direction_y = DIR_STILL

    def update(self):
        """
        Move everything and resolve collisions.
        """

        # print(self.player_sprite.direction_x, 'dir_x')
        # print(self.player_sprite.next_direction_x, 'next_dir_x')

        # --- Move in the x direction
        self.player_sprite.center_x += self.player_sprite.change_x

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(self.player_sprite,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point plus or minus safe space
        if len(hit_list) > 0:
            # print('collision!!')
            if self.player_sprite.direction_x == DIR_RIGHT:
                for item in hit_list:
                    # print(self.player_sprite.right, 'x>0')
                    self.player_sprite.right = item.left - SAFE_SPACE
                    # print(self.player_sprite.right, 'x>0')
            elif self.player_sprite.direction_x == DIR_LEFT:
                for item in hit_list:
                    # print(self.player_sprite.left, 'x<0')
                    self.player_sprite.left = item.right + SAFE_SPACE
                    # print(self.player_sprite.left, 'x<0')
            # else:
            #     print("Error, collision while player wasn't moving._x")
        else:
            self.player_sprite.direction_x = self.player_sprite.next_direction_x

        # --- Move in the y direction
        self.player_sprite.center_y += self.player_sprite.change_y

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(self.player_sprite,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point plus or minus safe space
        if len(hit_list) > 0:
            if self.player_sprite.direction_y == DIR_UP:
                for item in hit_list:
                    self.player_sprite.top = item.bottom - SAFE_SPACE
            elif self.player_sprite.direction_y == DIR_DOWN:
                for item in hit_list:
                    self.player_sprite.bottom = item.top + SAFE_SPACE
            # else:
            #     print("Error, collision while player wasn't moving._y")
        else:
            self.player_sprite.direction_y = self.player_sprite.next_direction_y
