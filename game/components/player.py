__author__ = 'Maverick'
from engine import components, Input
from engine.input import BindingDoesNotExist
from engine.math import Vector2, Rect
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

    def update_postframe(self):
        player = self.game_object

        camera = player.scene.camera
        camera.transform.position = player.transform.position

        tiled_map = player.scene.get_object_of_type(components.TiledMap)
        if tiled_map is None:
            return

        transform = player.transform
        position = transform.position
        bounding_rectangle = self.game_object.get_component(components.BoundingRectangle).rectangle

        if not tiled_map.is_position_in_map(position):
            return

        dt = self.game_object.scene.dt
        try:
            binding_pressed = False
            if Input.is_binding_pressed("left"):
                binding_pressed = True
                self.velocity.x -= self.MOVEMENT_PER_SECOND * dt
            if Input.is_binding_pressed("right"):
                binding_pressed = True
                self.velocity.x += self.MOVEMENT_PER_SECOND * dt

            if not binding_pressed:
                sign = (1, -1)[self.velocity.x < 0]
                self.velocity.x -= sign * min(self.MOVEMENT_PER_SECOND * dt, abs(self.velocity.x))

            if Input.is_binding_pressed("jump"):
                if not self.flying:
                    self.velocity.y = -self.JUMP_SPEED
                    self.flying = True

        except BindingDoesNotExist as e:
            logging.warning("Binding not found: " + str(e))

        if not self.flying:
            test_rectangle = bounding_rectangle.move(Vector2(0, 3))
            map_tiles = tiled_map.get_tiles_for_area(test_rectangle)

            found_collidable = False
            for tile in map_tiles:
                if tiled_map.get_tile_properties(tile[0], tile[1])["collidable"]:
                    found_collidable = True
                    break
            if not found_collidable:
                self.flying = True

        if self.flying:
            self.velocity.y += self.GRAVITY_PER_SECOND * dt

        # Velocity clamping
        self.velocity.x = sorted((-self.MAX_HORIZONTAL_SPEED, self.velocity.x, self.MAX_HORIZONTAL_SPEED))[1]
        self.velocity.y = sorted((-self.MAX_VERTICAL_SPEED, self.velocity.y, self.MAX_VERTICAL_SPEED))[1]

        self.applied_velocity = self.velocity * dt
        self.applied_velocity.x = 0 if abs(self.applied_velocity.x) < 2 else self.applied_velocity.x

        transform.position = position + self.applied_velocity

    def collide(self, game_object, *rectangles):
        bounding_rectangle = self.game_object.get_component(components.BoundingRectangle).rectangle
        transform = self.game_object.transform
        position = transform.position

        if game_object.has_component(components.TiledMapCollider):
            prev_rectangle = bounding_rectangle.move(-self.applied_velocity)

            epsilon = 0.5
            for collided in rectangles:
                if prev_rectangle.bottom - collided.top <= epsilon:
                    self.velocity.y = 0
                    self.flying = False
                    position.y = collided.top - bounding_rectangle.height/2 - 1
                    continue
                elif prev_rectangle.top - collided.bottom >= epsilon:
                    self.velocity.y = abs(self.velocity.y)
                    position.y = collided.bottom + bounding_rectangle.height/2 + 1
                    continue

                self.velocity.x = 0
                if position.x < collided.centerx:
                    position.x = collided.left - bounding_rectangle.width/2 - 1
                else:
                    position.x = collided.right + bounding_rectangle.width/2 + 1