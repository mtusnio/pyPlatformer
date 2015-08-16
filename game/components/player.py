__author__ = 'Maverick'
from engine import components, Input
from engine.input import BindingDoesNotExist
import logging


class Player(components.BaseComponent):
    GRAVITY = 320.0

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.flying = True

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
            if Input.is_binding_pressed("left"):
                transform.position[0] -= 400 * dt
            if Input.is_binding_pressed("right"):
                transform.position[0] += 400 * dt
        except BindingDoesNotExist as e:
            logging.warning("Binding not found: " + str(e))

        if not self.flying:
            x, y = tiled_map.get_tile_for_position(position)
            if not tiled_map.get_tile_properties(x, y + 1)["collidable"]:
                self.flying = True

        if self.flying:
            transform.position[1] += self.GRAVITY * dt

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
