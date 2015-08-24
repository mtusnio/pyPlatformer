__author__ = 'Maverick'

from engine.components import BaseComponent, BoundingRectangle, StaticBoundingRectangle, TiledMap, SpriteRenderer
from engine.math import Vector2
from engine.math.functions import sign


class CharacterController(BaseComponent):
    DEFAULT_GRAVITY = 825

    def __init__(self, gravity=DEFAULT_GRAVITY):
        super(CharacterController, self).__init__()
        self.flying = True
        self.velocity = Vector2(0, 0)
        self.applied_velocity = Vector2(0, 0)
        self.gravity = gravity

    def update(self):
        tiled_map = self.game_object.scene.get_object_of_type(TiledMap)

        if tiled_map is None:
            return

        if not tiled_map.is_position_in_map(self.game_object.transform.position):
            return

        self._handle_collisions(tiled_map, self.game_object.scene.dt)

    def _handle_collisions(self, tiled_map, dt):
        epsilon = 1
        transform = self.game_object.transform
        position = transform.position
        bounding_rectangle = self.game_object.get_component(BoundingRectangle).rectangle
        sprite_renderer = self.game_object.get_component(SpriteRenderer)
        if not self.flying:
            test_rectangle = bounding_rectangle.move(Vector2(0, 3))
            map_tiles = tiled_map.get_tiles_for_area(test_rectangle, collidable=True)
            if len(map_tiles) == 0:
                self.flying = True

        if self.flying:
            self.velocity.y += self.gravity * dt

        # Map collision tests
        tiled_map = self.game_object.scene.get_object_of_type(TiledMap)
        dt_velocity = self.velocity * dt

        if self.velocity.x != 0:
            horizontal_rectangle = bounding_rectangle.move(Vector2(dt_velocity.x + epsilon * sign(dt_velocity.x), 0))
            self._horizontal_collision(horizontal_rectangle, tiled_map, dt_velocity)

        if self.flying:
            vertical_rectangle = bounding_rectangle.move(Vector2(0, dt_velocity.y + epsilon * sign(dt_velocity.y)))
            tiles = tiled_map.get_tiles_for_area(vertical_rectangle, collidable=True)
            if len(tiles) > 0:
                if self.velocity.y < 0:
                    self.velocity.y = -self.velocity.y/2
                else:
                    tile = min(tiles, key=lambda t: t.y)
                    position.y = tiled_map.get_rectangle_for_tile(tile).top - bounding_rectangle.height/2 - epsilon
                    self.flying = False
                    self.velocity.y = 0
                dt_velocity.y = self.velocity.y * dt

        if self.velocity.x != 0:
            move_rectangle = bounding_rectangle.move(Vector2(dt_velocity.x + epsilon * sign(dt_velocity.x), dt_velocity.y))
            self._horizontal_collision(move_rectangle, tiled_map, dt_velocity)

        self._handle_animations()

        self.applied_velocity = dt_velocity
        transform.position = position + self.applied_velocity

    def _horizontal_collision(self, rectangle, tiled_map, dt_velocity):
        if len(tiled_map.get_tiles_for_area(rectangle, collidable=True)) > 0:
            self.velocity.x = 0
            dt_velocity.x = 0

    def _handle_animations(self):
        sprite_renderer = self.get_component(SpriteRenderer)

        if self.velocity.x < 0:
            sprite_renderer.horizontal_flip = True
        elif self.velocity.x > 0:
            sprite_renderer.horizontal_flip = False

        if not self.flying:
            if self.velocity.x != 0:
                if not self.flying:
                    sprite_renderer.play_animation("walk", True)
            else:
                sprite_renderer.play_animation("stand", True)
        else:
            sprite_renderer.play_animation("jump", True)
