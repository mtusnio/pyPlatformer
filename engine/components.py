__author__ = 'Maverick'
import pygame
from engine.math import Vector2, Rect
from collections import namedtuple
from . import tiledmap
import logging
import sys
import ast
import json
import re


class BaseComponent(object):
    """
    :type game_object: engine.GameObject
    :type scene: engine.Scene
    :type transform: engine.components.Transform
    """
    def __init__(self):
        self.game_object = None

    def spawn(self):
        """
        Called at the start of the frame after component's object was initialized in the scene
        """
        pass

    def start(self):
        """
        Called right before the component's first update is run (and thus all objects in this frame have been spawned)
        """
        pass

    def on_add(self):
        """
        Runs immediately after the component was added to a game object
        """
        pass

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

    # Shortcuts so that we don't have to go through game_object every time
    @property
    def scene(self):
        return self.game_object.scene

    @property
    def transform(self):
        return self.game_object.transform

    def get_component(self, cls):
        """
        Same as game_object.get_component
        """
        return self.game_object.get_component(cls)

    def get_components(self, cls):
        """
        Same as game_object.get_components
        """
        return self.game_object.get_components(cls)


class Camera(BaseComponent):
    """
    :type fov: float
    """
    def __init__(self, fov=80):
        super(Camera, self).__init__()
        self.fov = fov


class Renderable(BaseComponent):
    """
    :type should_render: bool
    """
    def __init__(self):
        super(Renderable, self).__init__()
        self.should_render = True


class SpriteRenderer(Renderable):
    """
    :type image: pygame.Surface
    :type horizontal_flip: bool
    :type vertical_flip: bool
    """
    _Animation = namedtuple("_Animation", ["name", "speed", "frames"])

    def __init__(self, image=None, horizontal_flip=False, vertical_flip=False, animation_data=None,
                 default_animation=None):
        super(SpriteRenderer, self).__init__()
        if animation_data is None and default_animation is not None:
            raise ValueError

        if isinstance(image, str):
            self.image = pygame.image.load(image)
        else:
            self.image = image

        self.horizontal_flip = horizontal_flip
        self.vertical_flip = vertical_flip

        self.animation_set_name = None
        self.animations = {}

        self.playing_animation = None
        self.frame_index = None
        self.frame_time = 0.0
        self.animation_looping = False
        self.animation_speed_rate = 1.0

        self.parse_animations(animation_data)
        if default_animation is not None:
            self.play_animation(default_animation)

    @property
    def playing_animation_name(self):
        """
        :return: Empty string if no animation is playing, otherwise name of the animation
        """
        if self.playing_animation is None:
            return ""
        return self.playing_animation.name

    def parse_animations(self, animation_data):
        """
        Parses the specified file/data to recover all possible animations

        :param str, dict animation_data: Loaded animation data or path to json file
        """
        if isinstance(animation_data, str):
            try:
                animation_data = json.load(open(animation_data, 'r'))
            except IOError:
                logging.warning("Could not open {path}".format(path=animation_data))
                animation_data = None
            except ValueError:
                logging.warning("Could not parse {path}".format(path=animation_data))
                animation_data = None

        if animation_data is not None:
            try:
                self.animation_set_name = animation_data["name"]
                self.animations = {}
                for key,value in animation_data.items():
                    if key != "name":
                        data = self._Animation(name=key, speed=value.get("speed", 0), frames=value.get("frames", []))
                        if key in self.animations:
                            raise ValueError

                        for i in range(0, len(data.frames)):
                            coords = data.frames[i].split(" ")
                            data.frames[i] = Rect(int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3]))

                        self.animations[key] = data
            except IndexError as e:
                logging.warning("Could not get animation data index")
                self.animation_set_name = None
                self.animations = {}
            except ValueError as e:
                logging.warning("Faulty animation data: {error}".format(error=e.message))
                self.animation_set_name = None
                self.animations = {}

    def play_animation(self, animation_name, loop=False, speed_rate=1.0, restart=False):
        """
        Plays a selected animation from the parsed set

        :param str animation_name: Name of the animation to play
        :param loop: Loops animation if true
        :param speed_rate: Playback speed of the animation
        :param restart: If true will restart the animation if it's already playing
        """
        if not restart and self.playing_animation_name == animation_name:
            return

        if animation_name in self.animations:
            self.playing_animation = self.animations[animation_name]
            self.frame_index = 0
            self.frame_time = 0.0
            self.animation_looping = loop
            self.animation_speed_rate = speed_rate
            self._update_animation_image()
        else:
            logging.warning("No animation {animation} found".format(animation=animation_name))

    def stop_animation(self):
        """
        Stops any ongoing animation retaining current image as last frame of animation
        """
        self.playing_animation = None
        self.frame_index = 0
        self.frame_time = 0

    def update(self):
        if self.playing_animation is not None:
            animation = self.playing_animation
            self.frame_time += self.game_object.scene.dt

            if self.frame_time >= animation.speed/self.animation_speed_rate:
                old_index = self.frame_index
                if self.animation_looping:
                    self.frame_index = (self.frame_index + 1) % len(animation.frames)
                elif self.frame_index + 1 >= len(animation.frames):
                    self.stop_animation()
                    return
                self.frame_time = 0.0
                if old_index != self.frame_index:
                    self._update_animation_image()

    def _update_animation_image(self):
        parent = self.image.get_parent()
        if parent is not None:
            self.image = parent.subsurface(self.playing_animation.frames[self.frame_index])
        else:
            self.stop_animation()
            logging.warning("Cannot find parent image for animation update")


class Transform(BaseComponent):
    """
    :type position: Vector2
    :type rotation: float
    :type scale: float
    """
    def __init__(self, position=None, rotation=0, scale=1):
        super(Transform, self).__init__()
        if position is None:
            position = Vector2(0, 0)
        self._position = position
        self.rotation = rotation
        self.scale = scale

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
    def __init__(self,):
        super(BoundingRectangle, self).__init__()

    @property
    def rectangle(self):
        raise NotImplementedError()


class SpriteBoundingRectangle(BoundingRectangle):
    """
    Bounding rectangle calculated using the sprite image
    """
    def __init__(self):
        super(SpriteBoundingRectangle, self).__init__()

    @property
    def rectangle(self):
        return self.game_object.get_component(SpriteRenderer).image.get_rect(center=self.game_object.transform.position)


class StaticBoundingRectangle(BoundingRectangle):
    """
    Statically set bounding rectangle
    """
    def __init__(self, width, height, x=0, y=0):
        super(StaticBoundingRectangle, self).__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = 0

    @property
    def rectangle(self):
        r = Rect(0, 0, self.width, self.height)
        r.center = self.game_object.transform.position + Vector2(self.x, self.y)
        return r


class Collider(BaseComponent):
    """
    Collider class which can expanded for custom collisions, by default uses BoundingRectangle
    on both objects to check for collisions.
    """
    def __init__(self):
        super(Collider, self).__init__()

    def get_collision_shapes(self, game_object):
        """
        Returns a list of rectangles to use for collision detection.

        :param engine.GameObject game_object: Object we are testing collisions against
        :return pygame.Rect:
        """
        return [self.game_object.get_component(BoundingRectangle).rectangle]


class TiledMap(Renderable):
    """
    :type map: tiledmap.TiledMap
    """
    Tile = namedtuple("Tile", ['x', 'y', 'properties'])

    def __init__(self, map_path=None):
        super(TiledMap, self).__init__()
        self.map = tiledmap.load(map_path) if map_path is not None else None

    def spawn(self):
        self.fill_scene_with_objects()

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
        for x in range(top_left[0], bottom_right[0] + 1):
            for y in range(top_left[1], bottom_right[1] + 1):
                tile = self._get_tile_tuple(x, y)
                if all(prop in tile.properties for prop in properties):
                    if all(key in tile.properties and tile.properties[key] == value
                                                          for key,value in properties_values.items()):
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
        from engine import GameObject

        tiled_map = self.map
        scene = self.game_object.scene
        for group in tiled_map.visible_object_groups:
            for obj in tiled_map.layers[group]:
                game_object = GameObject()
                translation = Vector2(0, 0)
                if obj.image is not None:
                    translation.x = obj.image.get_width()/2
                    translation.y = obj.image.get_height()/2

                obj_position = Vector2(obj.x, obj.y) + translation
                game_object.add_components(Transform(position=obj_position))
                if obj.image is not None:
                    animation_data = obj.properties.get("animation_data", None)
                    game_object.add_components(SpriteRenderer(image=obj.image, animation_data=animation_data))

                self._resolve_components(obj.properties.get("components", "").split(";"), game_object)

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

            for key,value in layer_properties.items():
                try:
                    if value in ["true", "false"]:
                        value = value.title()
                    properties[key] = ast.literal_eval(value)
                except (SyntaxError, ValueError) as e:
                    properties[key] = value

        return self.Tile(x=x, y=y, properties=properties)

    def _resolve_components(self, components, game_object):
        import game.components as game_components
        for component_declaration in components:
            # TODO: Replace with regex
            component_name = component_declaration.split("(")[0]
            parameters = component_declaration.split("(")[1][:-1]

            try:
                regex_results = re.findall("([a-zA-Z0-9]+)=([a-zA-Z0-9]+)", parameters)
                parameters = {}
                for param in regex_results:
                    parameters[param[0]] = ast.literal_eval(param[1])

            except ( SyntaxError, ValueError ) as e:
                logging.warning("Could not parse parameters for {component}".format(component=component_name))
                continue

            component_class = None
            module = sys.modules[__name__]
            if hasattr(module, component_name):
                component_class = getattr(module, component_name)
            elif hasattr(game_components, component_name):
                component_class = getattr(game_components, component_name)

            if component_class is not None:
                game_object.add_components(component_class(**parameters))
            else:
                logging.warning("Could not find class: '{0}'".format(component_name))

    def __format_out_of_position(self, x, y):
        return "Position({0}, {1}) out of map".format(x, y)
