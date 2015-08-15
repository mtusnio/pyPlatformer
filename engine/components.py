__author__ = 'Maverick'
import pygame
from engine.math import Vector2
import tiledmap
import logging
import sys


class BaseComponent(object):
    """
    :type game_object: engine.GameObject
    """
    def __init__(self, **kwargs):
        self.game_object = None

    def update(self):
        """
        Runs once per frame before rendering
        """
        pass


class Camera(BaseComponent):
    """
    :type fov: float
    """
    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.fov = kwargs.get("fov", 80)


class Renderable(BaseComponent):
    """
    :type should_render: bool
    """
    def __init__(self, **kwargs):
        super(Renderable, self).__init__(**kwargs)
        self.should_render = True


class SpriteRenderer(Renderable):
    """
    :type image_path: str
    :type image: pygame.Surface
    """
    def __init__(self, **kwargs):
        super(SpriteRenderer, self).__init__(**kwargs)
        if "image" not in kwargs:
            image_path = kwargs.get("path", None)
            self.image = pygame.image.load(image_path) if image_path is not None else None
        else:
            self.image = kwargs.get("image", None)


class Transform(BaseComponent):
    """
    :type position: Vector2
    :type rotation: float
    :type scale: float
    """
    def __init__(self, **kwargs):
        super(Transform, self).__init__(**kwargs)
        self._position = kwargs.get("position", Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.scale = kwargs.get("scale", 1)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.x = value.x
        self._position.y = value.y
        self._position.epsilon = value.epsilon


class BoundingRectangle(BaseComponent):
    """
    Base class for all bounding rectangles that we need to calculate
    """
    def __init__(self, **kwargs):
        super(BoundingRectangle, self).__init__(**kwargs)

    @property
    def rectangle(self):
        raise NotImplementedError()


class SpriteBoundingRectangle(BoundingRectangle):
    """
    Bounding rectangle calculated using the sprite image
    """
    def __init__(self, **kwargs):
        super(SpriteBoundingRectangle, self).__init__(**kwargs)

    @property
    def rectangle(self):
        return self.game_object.get_component(SpriteRenderer).image.get_rect(center=self.game_object.transform.position)


class Collider(BaseComponent):
    """
    Collider class which can expanded for custom collisions, by default uses BoundingRectangle
    on both objects to check for collisions.
    """
    def __init__(self, **kwargs):
        super(Collider, self).__init__(**kwargs)

    def check_collision(self, game_object):
        """
        Checks collision between object holding this component and supplied game object
        :param engine.GameObject game_object: Game object which we might be colliding with
        :return bool: True if this object collides with game_object
        """
        my_rectangle = self.game_object.get_component(BoundingRectangle)
        other_rectangle = game_object.get_component(BoundingRectangle)
        if my_rectangle is None or other_rectangle is None:
            return False
        return my_rectangle.rectangle.colliderect(other_rectangle.rectangle)


class TiledMap(Renderable):
    """
    :type map_path: str
    :type map: tiledmap.TiledMap
    """
    def __init__(self, **kwargs):
        super(TiledMap, self).__init__(**kwargs)
        map_path = kwargs.get("path", None)
        self.map = tiledmap.load(map_path) if map_path is not None else None

    def is_position_in_map(self, position):
        """
        Checks if the supplied world position is within map's bounds
        :param Vector2 position: World position
        :return: True if position is within map's bounds, False otherwise
        """
        relative_pos = position - self.game_object.transform.position
        if position[0] < 0 or position[1] < 0:
            return False

        if position[0] > self.map.tilewidth * self.map.width:
            return False

        if position[1] > self.map.tileheight * self.map.height:
            return False

        return True

    def is_tile_in_map(self, x, y):
        """
        Checks if the x/y tile coordinates are within bounds of the map
        :param int x:
        :param int y:
        :return: True if the tile is within map bounds
        """
        if x < 0 or y < 0:
            return False

        if x >= self.map.tilewidth or y >= self.map.tileheight:
            return False

        return True

    def get_tile_for_position(self, position, extrapolate = False):
        """
        Returns x/y tile coordinates for specified world position
        :param Vector2 position: World position
        :param bool extrapolate: If set to True it will return return potential out of bound tiles
        :return: Tuple containing x/y coordinates
        """
        if extrapolate is not True and not self.is_position_in_map(position):
            raise ValueError("Position is out of map")

        relative_position = position - self.game_object.transform.position
        return int(relative_position[0] // self.map.tilewidth), int(relative_position[1] // self.map.tileheight)

    def get_rectangle_for_tile(self, x, y):
        """
        Returns a rectangle which covers the tile at provided coordinates
        :type x int
        :type y int
        :rtype pygame.Rect
        """
        if not self.is_tile_in_map(x, y):
            raise ValueError("Position is out of map")

        return pygame.Rect((x * self.map.tilewidth, y * self.map.tileheight), (self.map.tilewidth, self.map.tileheight))

    def fill_scene_with_objects(self):
        """
        Fills this object's scene with objects as described by tiled_map
        """
        import game.components as game_components
        from engine import GameObject

        tiled_map = self.map
        scene = self.game_object.scene
        for group in tiled_map.visible_object_groups:
            for obj in tiled_map.layers[group]:
                game_object = GameObject()
                obj_position = Vector2(obj.x + obj.image.get_width()/2, obj.y + obj.image.get_height()/2)
                game_object.add_components(Transform(position=obj_position))
                if obj.image is not None:
                    game_object.add_components(SpriteRenderer(image=obj.image), SpriteBoundingRectangle())

                obj_components = obj.properties.get("components", "")
                for component_name in obj_components.split(";"):
                    component_class = None
                    module = sys.modules[__name__]
                    if hasattr(module, component_name):
                        component_class = getattr(module, component_name)
                    elif hasattr(game_components, component_name):
                        component_class = getattr(game_components, component_name)

                    if component_class is not None:
                        game_object.add_components(component_class())
                    else:
                        logging.warning("Could not find class: '{0}'".format(component_name))

                scene.add_object(game_object)


class TiledMapCollider(Collider):
    def __init__(self, **kwargs):
        super(TiledMapCollider, self).__init__(**kwargs)

    def check_collision(self, game_object):
        tiled_map = self.game_object.get_component(TiledMap)
        bounding_rect = game_object.get_component(BoundingRectangle)

        if tiled_map is None or bounding_rect is None:
            return False

        rect = bounding_rect.rectangle
        top_left = tiled_map.get_tile_for_position(Vector2(rect.topleft), True)
        bottom_right = tiled_map.get_tile_for_position(Vector2(rect.bottomright), True)

        for x in xrange(top_left[0], bottom_right[0] + 1):
            for y in xrange(top_left[1], bottom_right[1] + 1):
                tile_rect = tiled_map.get_rectangle_for_tile(x, y)
                return tile_rect.colliderect(rect)

        return False


