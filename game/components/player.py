__author__ = 'Maverick'
from engine import components, Input
from engine.input import BindingDoesNotExist
from engine.math import Vector2, Rect
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
        self._applied_velocity = Vector2(0, 0)

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
            x, y = tiled_map.get_tile_for_position(position)
            if not tiled_map.get_tile_properties(x, y + 1)["collidable"]:
                self.flying = True

        if self.flying:
            self.velocity.y += self.GRAVITY_PER_SECOND * dt

        # Velocity clamping
        self.velocity.x = sorted((-self.MAX_HORIZONTAL_SPEED, self.velocity.x, self.MAX_HORIZONTAL_SPEED))[1]
        self.velocity.y = sorted((-self.MAX_VERTICAL_SPEED, self.velocity.y, self.MAX_VERTICAL_SPEED))[1]

        self._applied_velocity = self.velocity * dt
        transform.position = position + self._applied_velocity

    def collide(self, game_object, *rectangles):
        bounding_rectangle = self.game_object.get_component(components.BoundingRectangle).rectangle
        transform = self.game_object.transform
        position = transform.position

        if game_object.has_component(components.TiledMapCollider):
            remaining_rectangles = list(rectangles)
            prev_velocity = self._applied_velocity
            prev_position = bounding_rectangle.move(-prev_velocity)

            horizontal_rectangle = prev_position.move(Vector2(prev_velocity.x, 0))
            horizontal_collision = horizontal_rectangle.collidelistall(remaining_rectangles)
            if len(horizontal_collision) > 0:
                rectangle = remaining_rectangles[horizontal_collision[0]]
                if position.x < rectangle.centerx:
                    position.x = rectangle.left - bounding_rectangle.width/2 - 2
                else:
                    position.x = rectangle.right + bounding_rectangle.width/2 + 2
                self.velocity.x = 0
                remaining_rectangles = [x for y,x in enumerate(remaining_rectangles) if y not in horizontal_collision]

            upper_rectangles = [rect for rect in remaining_rectangles if bounding_rectangle.top < rect.bottom
                                    and bounding_rectangle.bottom > rect.bottom]
            lower_rectangles = [rect for rect in remaining_rectangles if bounding_rectangle.bottom > rect.top
                                    and bounding_rectangle.top < rect.top]

            if self.flying:
                vertical_rectangle = prev_position.move(Vector2(0, prev_velocity.y))

                lower_collisions = vertical_rectangle.collidelistall(lower_rectangles)
                if len(lower_collisions) > 0:
                    rectangle = lower_rectangles[lower_collisions[0]]
                    position.y = rectangle.top - bounding_rectangle.height/2 - 2
                    self.flying = False
                    self.velocity.y = 0

                upper_collisions = vertical_rectangle.collidelistall(upper_rectangles)
                if len(upper_collisions) > 0:
                    rectangle = upper_rectangles[upper_collisions[0]]
                    position.y = rectangle.bottom + bounding_rectangle.height/2 + 2
                    self.velocity.y = abs(self.velocity.y)

                remaining_rectangles = [x for y, x in enumerate(rectangles) if y not in lower_collisions
                                        and y not in upper_collisions]

