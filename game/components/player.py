__author__ = 'Maverick'
from engine import components, Input
from engine.input import BindingDoesNotExist
from engine.math import Vector2
import logging


class Player(components.BaseComponent):
    GRAVITY_PER_SECOND = 825
    MOVEMENT_PER_SECOND = 1700
    JUMP_SPEED = 500

    MAX_VERTICAL_SPEED = 1200
    MAX_HORIZONTAL_SPEED = 500

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.flying = True
        self.velocity = Vector2(0, 0)

    def update(self):
        player = self.game_object

        camera = player.scene.camera
        camera.transform.position = player.transform.position

        tiled_map = player.scene.get_object_of_type(components.TiledMap)
        if tiled_map is None:
            return

        transform = player.transform
        position = transform.position
        if not tiled_map.is_position_in_map(position):
            return

        dt = self.game_object.scene.dt
        try:
            binding_pressed = False
            if Input.is_binding_pressed("left"):
                binding_pressed = True
                self.velocity[0] -= self.MOVEMENT_PER_SECOND * dt
            if Input.is_binding_pressed("right"):
                binding_pressed = True
                self.velocity[0] += self.MOVEMENT_PER_SECOND * dt

            if not binding_pressed:
                sign = (1, -1)[self.velocity[0] < 0]
                self.velocity[0] -= sign * min(self.MOVEMENT_PER_SECOND * dt, abs(self.velocity[0]))

            if Input.is_binding_pressed("jump"):
                if not self.flying:
                    self.velocity[1] = -self.JUMP_SPEED

        except BindingDoesNotExist as e:
            logging.warning("Binding not found: " + str(e))

        if not self.flying:
            x, y = tiled_map.get_tile_for_position(position)
            if not tiled_map.get_tile_properties(x, y + 1)["collidable"]:
                self.flying = True

        if self.flying:
            self.velocity[1] += self.GRAVITY_PER_SECOND * dt

        # Velocity clamping
        self.velocity[0] = sorted((-self.MAX_HORIZONTAL_SPEED, self.velocity[0], self.MAX_HORIZONTAL_SPEED))[1]
        self.velocity[1] = sorted((-self.MAX_VERTICAL_SPEED, self.velocity[1], self.MAX_VERTICAL_SPEED))[1]

        transform.position = position + self.velocity * dt

    def collide(self, game_object, *rectangles):
        bounding_rectangle = self.game_object.get_component(components.BoundingRectangle).rectangle
        transform = self.game_object.transform
        position = transform.position

        if game_object.has_component(components.TiledMapCollider):
            #upper_rectangles = [rect for rect in rectangles if position - rect.center < 0]
            lower_rectangles = [rect for rect in rectangles if bounding_rectangle.bottom > rect.top]

            if self.flying and len(lower_rectangles) > 0:
                closest_lower = min(lower_rectangles, key=lambda rect: (position - rect.center).length())
                transform.position.y = closest_lower.top - bounding_rectangle.height/2
                self.flying = False
                self.velocity[1] = 0
