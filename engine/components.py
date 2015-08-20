__author__ = 'Maverick'
import pygame
from engine.math import Vector2, Rect
from collections import namedtuple
import tiledmap
import logging
import sys
import ast
import copy


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

    def update_postframe(self):
        """
        Runs once per frame after rendering
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

    def get_collision_shapes(self, game_object):
        """
        Returns a list of rectangles to use for collision detection.
        :param engine.GameObject game_object: Object we are testing collisions against
        :return pygame.Rect:
        """
        return [self.game_object.get_component(BoundingRectangle).rectangle]


class TiledMap(Renderable):
    """
    :type map_path: str
    :type map: tiledmap.TiledMap
    """
    Tile = namedtuple("Tile", ['x', 'y', 'properties'])

    def __init__(self, **kwargs):
        super(TiledMap, self).__init__(**kwargs)
        map_path = kwargs.get("path", None)
        self.map = tiledmap.load(map_path) if map_path is not None else None
        self._collidable_tiles = None

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

    def is_tile_in_map(self, tile):
        """
        Checks if the x/y tile coordinates are within bounds of the map

        :param tuple tile: Tuple containing x/y coordinates
        :return: True if the tile is within map bounds
        """
        x = tile[0]
        y = tile[1]
        if x < 0 or y < 0:
            return False

        if x >= self.map.width or y >= self.map.height:
            return False

        return True

    def get_tile_for_position(self, position, extrapolate=False):
        """
        Returns x/y tile coordinates for specified world position

        :param Vector2 position: World position
        :param bool extrapolate: If set to True it will return return potential out of bound tiles
        :return: Tuple containing x/y coordinates
        """
        if extrapolate is not True and not self.is_position_in_map(position):
            raise ValueError(self.__format_out_of_position(position[0], position[1]))

        relative_position = position - self.game_object.transform.position
        return self._get_tile_tuple(int(relative_position[0] // self.map.tilewidth),
                               int(relative_position[1] // self.map.tileheight))

    def get_tiles_for_area(self, area, extrapolate=False, *properties, **properties_values):
        """
        Finds all tiles that fit within the given area

        :param Rect area: Rectangle within which we want to grab all tiles
        :param bool extrapolate: If true it will also return tiles out of map bounds instead of raising an exception
        :param properties: Filter tiles by properties they must possess
        :param properties_values: Filter tiles by properties and their respective values
        :return list: List of all found tiles in right-down format
        """
        top_left = self.get_tile_for_position(area.topleft, extrapolate)
        # Bottom and right side should always be excluded
        bottom_right_vec = Vector2(area.bottomright[0], area.bottomright[1])
        if int(bottom_right_vec.x) == bottom_right_vec.x:
            bottom_right_vec.x -= 0.3
        if int(bottom_right_vec.y) == bottom_right_vec.y:
            bottom_right_vec.y -= 0.3

        bottom_right = self.get_tile_for_position(bottom_right_vec, extrapolate)

        ret = []
        for x in xrange(top_left[0], bottom_right[0] + 1):
            for y in xrange(top_left[1], bottom_right[1] + 1):
                tile = self._get_tile_tuple(x, y)
                if all(prop in tile.properties for prop in properties):
                    if all(key in tile.properties and tile.properties[key] == value
                                                          for key,value in properties_values.iteritems()):
                        ret.append(tile)

        return ret

    def get_rectangle_for_tile(self, tile):
        """
        Returns a rectangle which covers the tile at provided coordinates

        :param tuple tile: Tuple containing x/y coordinates
        """
        if not self.is_tile_in_map(tile):
            raise ValueError(self.__format_out_of_position(x, y))

        x = tile[0]
        y = tile[1]

        return Rect((x * self.map.tilewidth, y * self.map.tileheight), (self.map.tilewidth, self.map.tileheight))

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

    def _get_tile_tuple(self, x, y):
        properties = dict()
        for layer in self.map.visible_tile_layers:
            layer_properties = None
            try:
                if self.map.get_tile_gid(x, y, layer) != 0:
                    layer_properties = self.map.layers[layer].properties
            except ValueError:
                continue

            if layer_properties is None:
                continue

            for key,value in layer_properties.iteritems():
                try:
                    if value in ["true", "false"]:
                        value = value.title()
                    properties[key] = ast.literal_eval(value)
                except (SyntaxError, ValueError) as e:
                    properties[key] = value

        return self.Tile(x=x, y=y, properties=properties)

    def __format_out_of_position(self, x, y):
        return "Position({0}, {1}) out of map".format(x, y)
