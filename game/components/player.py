__author__ = 'Maverick'
from engine import components, Input
from engine.input import BindingDoesNotExist
from engine.math import Vector2, Rect
from engine.math.functions import sign
import logging


class Player(components.BaseComponent):
    GRAVITY_PER_SECOND = 825
    MOVEMENT_PER_SECOND = 1700
    JUMP_SPEED = 700

    MAX_VERTICAL_SPEED = 1200
    MAX_HORIZONTAL_SPEED = 500

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.flying = True
        self.velocity = Vector2(0, 0)
        self.applied_velocity = Vector2(0, 0)

    def update(self):
        player = self.game_object
        camera = player.scene.camera
        camera.transform.position = player.transform.position

        tiled_map = player.scene.get_object_of_type(components.TiledMap)
        if tiled_map is None:
            return

        if not tiled_map.is_position_in_map(player.transform.position):
            return

        dt = self.game_object.scene.dt
        self._handle_input(dt)
        self._handle_collisions(tiled_map, dt)

    def _handle_input(self, dt):
        try:
            binding_pressed = False
            if Input.is_binding_pressed("left"):
                binding_pressed = True
                self.velocity.x -= self.MOVEMENT_PER_SECOND * dt
            if Input.is_binding_pressed("right"):
                binding_pressed = True
                self.velocity.x += self.MOVEMENT_PER_SECOND * dt

            if not binding_pressed:
                sigma = sign(self.velocity.x)
                self.velocity.x -= sigma * min(self.MOVEMENT_PER_SECOND * dt, abs(self.velocity.x))

            if Input.is_binding_pressed("jump"):
                if not self.flying:
                    self.velocity.y = -self.JUMP_SPEED
                    self.flying = True

        except BindingDoesNotExist as e:
            logging.warning("Binding not found: " + str(e))

    def _handle_collisions(self, tiled_map, dt):
        epsilon = 0.75
        transform = self.game_object.transform
        position = transform.position
        bounding_rectangle = self.game_object.get_component(components.BoundingRectangle).rectangle

        if not self.flying:
            test_rectangle = bounding_rectangle.move(Vector2(0, 3))
            map_tiles = tiled_map.get_tiles_for_area(test_rectangle, collidable=True)
            if len(map_tiles) == 0:
                self.flying = True

        if self.flying:
            self.velocity.y += self.GRAVITY_PER_SECOND * dt

        # Velocity clamping
        self.velocity.x = sorted((-self.MAX_HORIZONTAL_SPEED, self.velocity.x, self.MAX_HORIZONTAL_SPEED))[1]
        self.velocity.y = sorted((-self.MAX_VERTICAL_SPEED, self.velocity.y, self.MAX_VERTICAL_SPEED))[1]

        # Map collision tests
        tiled_map = self.game_object.scene.get_object_of_type(components.TiledMap)
        dt_velocity = self.velocity * dt

        if self.velocity.x != 0:
            horizontal_rectangle = bounding_rectangle.move(Vector2(dt_velocity.x + epsilon * sign(dt_velocity.x), 0))
            self._horizontal_collision(horizontal_rectangle, tiled_map, dt_velocity)

        if self.flying:
            vertical_rectangle = bounding_rectangle.move(Vector2(0, dt_velocity.y))
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

        self.applied_velocity = dt_velocity
        transform.position = position + self.applied_velocity

    def _horizontal_collision(self, rectangle, tiled_map, dt_velocity):
        if len(tiled_map.get_tiles_for_area(rectangle, collidable=True)) > 0:
            self.velocity.x = 0
            dt_velocity.x = 0