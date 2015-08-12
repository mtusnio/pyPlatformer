__author__ = 'Maverick'
import pygame
from engine import math
import tiledmap
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
    :type image_path: basestring
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
    :type position: math.Vector2
    :type rotation: float
    :type scale: float
    """
    def __init__(self, **kwargs):
        super(Transform, self).__init__(**kwargs)
        self._position = kwargs.get("position", math.Vector2(0, 0))
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


class TiledMap(Renderable):
    """
    :type map_path: basestring
    :type map: tiledmap.TiledMap
    """
    def __init__(self, **kwargs):
        super(TiledMap, self).__init__(**kwargs)
        map_path = kwargs.get("path", None)
        self.map = tiledmap.load(map_path) if map_path is not None else None
