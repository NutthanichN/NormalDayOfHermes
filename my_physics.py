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


class PhysicsEngine:
    def __init__(self, player_sprite: Sprite, walls: SpriteList, platforms: SpriteList,
                 gravity_constant: float = 0.5):
        """
        Constructor.
        """
        assert(isinstance(player_sprite, Sprite))
        assert(isinstance(walls, SpriteList))
        assert (isinstance(platforms, SpriteList))
        self.player_sprite = player_sprite
        self.walls = walls
        self.platforms = platforms

        self.gravity_constant = gravity_constant

        self.player_sprite.direction_x = self.player_sprite.check_direction_x()
        self.player_sprite.direction_y = self.player_sprite.check_direction_y()
        self.player_sprite.next_direction_x = DIR_STILL
        self.player_sprite.next_direction_y = DIR_STILL

    def check_and_solve_walls_hit(self):
        hit_list = \
            check_for_collision_with_list(self.player_sprite,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point plus or minus safe space
        # x axis
        if len(hit_list) > 0:
            # print('collision!!')
            if self.player_sprite.direction_x == DIR_RIGHT:
                for item in hit_list:
                    # print(self.player_sprite.right, 'x>0')

                    # print(item.trap_left)
                    if item.trap_left:
                        self.player_sprite.is_dead = True
                        # print(item.trap_left)

                    self.player_sprite.right = item.left - SAFE_SPACE
                    # print(self.player_sprite.right, 'x>0')
            elif self.player_sprite.direction_x == DIR_LEFT:
                for item in hit_list:
                    # print(self.player_sprite.left, 'x<0')

                    # print(item.trap_right)
                    if item.trap_right:
                        self.player_sprite.is_dead = True
                        # print(item.trap_right)

                    self.player_sprite.left = item.right + SAFE_SPACE
                    # print(self.player_sprite.left, 'x<0')
            else:
                pass
            #     print("Error, collision while player wasn't moving._x")
        else:
            # update player direction only if player doesn't hit wall
            self.player_sprite.direction_x = self.player_sprite.next_direction_x

        hit_list = \
            check_for_collision_with_list(self.player_sprite,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point plus or minus safe space
        # y axis
        if len(hit_list) > 0:
            # print('collision!!')
            if self.player_sprite.direction_y == DIR_UP:
                for item in hit_list:
                    # print(self.player_sprite.top, 'y>0')

                    self.player_sprite.top = item.bottom - SAFE_SPACE
                    # print(self.player_sprite.top, 'y>0')
            elif self.player_sprite.direction_y == DIR_DOWN:
                for item in hit_list:
                    # print(self.player_sprite.bottom, 'y<0')

                    self.player_sprite.bottom = item.top + SAFE_SPACE
                    # print(self.player_sprite.bottom, 'y<0')
            else:
                pass
            #     print("Error, collision while player wasn't moving._y")
        else:
            # update player direction only if player doesn't hit wall
            self.player_sprite.direction_y = self.player_sprite.next_direction_y

    def can_jump(self) -> bool:
        """
        Method that looks to see if there is a floor under
        the player_sprite. If there is a floor, the player can jump
        and we return a True.
        """
        # --- Move in the y direction
        self.player_sprite.center_y -= 2

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(self.player_sprite,
                                          self.platforms)

        self.player_sprite.center_y += 2

        if len(hit_list) > 0:
            return True
        else:
            return False

    def check_and_solve_platforms_hit(self):
        # Check for wall hit
        hit_list = check_for_collision_with_list(self.player_sprite, self.platforms)

        # If we hit a wall, move so the edges are at the same point
        # y axis
        if len(hit_list) > 0:
            if self.player_sprite.change_y > 0:
                # print('change_y > 0')
                # print('===================================')
                for item in hit_list:
                    self.player_sprite.top = min(item.bottom,
                                                 self.player_sprite.top)

                    if item.trap_bottom:
                        self.player_sprite.is_dead = True

                # print(f"Spot X ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
            elif self.player_sprite.change_y < 0:
                # print('change_y < 0')
                # print('----------------------------')
                for item in hit_list:
                    while check_for_collision(self.player_sprite, item):
                        # self.player_sprite.bottom = item.top <- Doesn't work for ramps
                        # print('**************work here**************')
                        self.player_sprite.bottom += 0.25

                        if item.trap_top:
                            self.player_sprite.is_dead = True

                    # moving platform
                    if item.change_x != 0:
                        self.player_sprite.center_x += item.change_x
                # print(f"Spot Y ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
            else:
                pass
                # TODO: The code below can't execute, as "item" doesn't
                # exist. In theory, this condition should never be arrived at.
                # Collision while player wasn't moving, most likely
                # moving platform.
                # if self.player_sprite.center_y >= item.center_y:
                #     self.player_sprite.bottom = item.top
                # else:
                #     self.player_sprite.top = item.bottom
            self.player_sprite.change_y = min(0.0, hit_list[0].change_y)  # moving platform??

        # print(f"Spot B ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
        self.player_sprite.center_y = round(self.player_sprite.center_y, 2)
        # print(f"Spot Q ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        # --- Move in the x direction
        # self.player_sprite.center_x += self.player_sprite.change_x

        check_again = True
        while check_again:
            check_again = False
            # Check for wall hit
            hit_list = check_for_collision_with_list(self.player_sprite, self.platforms)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                change_x = self.player_sprite.change_x
                if change_x > 0:
                    for item in hit_list:
                        # print(f"Spot 1 ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
                        # See if we can "run up" a ramp
                        self.player_sprite.center_y += change_x
                        if len(check_for_collision_with_list(self.player_sprite, self.platforms)) > 0:
                            self.player_sprite.center_y -= change_x
                            self.player_sprite.right = min(item.left, self.player_sprite.right)
                            # print(f"Spot R ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
                            check_again = True
                            break
                        # else:
                        # print("Run up ok 1")
                        # print(f"Spot 2 ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

                elif change_x < 0:
                    for item in hit_list:
                        # See if we can "run up" a ramp
                        self.player_sprite.center_y -= change_x
                        if len(check_for_collision_with_list(self.player_sprite, self.platforms)) > 0:
                            # Can't run up the ramp, reverse
                            self.player_sprite.center_y += change_x
                            self.player_sprite.left = max(item.right, self.player_sprite.left)
                            # print(f"Reverse 1 {item.right}, {self.player_sprite.left}")
                            # Ok, if we were shoved back to the right, we need to check this whole thing again.
                            check_again = True
                            break
                        # print(f"Spot 4 ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

                else:
                    print("Error, collision while player wasn't moving.\n"
                          "Make sure you aren't calling multiple updates, like "
                          "a physics engine update and an all sprites list update.")

            # print(f"Spot E ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        for platform in self.platforms:
            if platform.change_x != 0 or platform.change_y != 0:
                platform.center_x += platform.change_x

                if platform.boundary_left is not None \
                        and platform.left <= platform.boundary_left:
                    platform.left = platform.boundary_left
                    if platform.change_x < 0:
                        platform.change_x *= -1

                if platform.boundary_right is not None \
                        and platform.right >= platform.boundary_right:
                    platform.right = platform.boundary_right
                    if platform.change_x > 0:
                        platform.change_x *= -1

                if check_for_collision(self.player_sprite, platform):
                    if platform.change_x < 0:
                        self.player_sprite.right = platform.left
                    if platform.change_x > 0:
                        self.player_sprite.left = platform.right

                platform.center_y += platform.change_y

                if platform.boundary_top is not None \
                        and platform.top >= platform.boundary_top:
                    platform.top = platform.boundary_top
                    if platform.change_y > 0:
                        platform.change_y *= -1

                if platform.boundary_bottom is not None \
                        and platform.bottom <= platform.boundary_bottom:
                    platform.bottom = platform.boundary_bottom
                    if platform.change_y < 0:
                        platform.change_y *= -1

        # self.player_sprite.center_x = round(self.player_sprite.center_x, 2)
        # print(f"Spot C ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
        # print()

    def update(self):
        # --- Move in the x direction
        self.player_sprite.center_x += self.player_sprite.change_x

        # --- Add gravity
        self.player_sprite.change_y -= self.gravity_constant

        # --- Move in the y direction
        self.player_sprite.center_y += self.player_sprite.change_y

        self.check_and_solve_walls_hit()
        self.check_and_solve_platforms_hit()
