__author__ = 'Maverick'
import pygame
from engine import math
import tiledmap

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
        self.image_path = kwargs.get("path", None)
        if self.image_path is not None:
            self.image = pygame.image.load(self.image_path)
        else:
            self.image = None


class Transform(BaseComponent):
    """
    :type position: math.Vector2
    :type rotation: float
    :type scale: float
    """
    def __init__(self, **kwargs):
        super(Transform, self).__init__(**kwargs)
        self.position = kwargs.get("position", math.Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.scale = kwargs.get("scale", 1)


class TiledMap(Renderable):
    """
    :type map_path: basestring
    :type map: tiledmap.TiledMap
    """
    def __init__(self, **kwargs):
        super(TiledMap, self).__init__(**kwargs)
        self.map_path = kwargs.get("map_path", None)
        self.map = tiledmap.load(self.map_path) if self.map_path is not None else None
