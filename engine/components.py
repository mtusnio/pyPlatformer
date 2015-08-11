__author__ = 'Maverick'
import pygame
from engine import math


class BaseComponent(object):
    def __init__(self, **kwargs):
        self.game_object = None

    def update(self):
        """
        Runs once per frame before rendering
        """
        pass


class Camera(BaseComponent):
    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.fov = kwargs.get("fov", 80)


class Renderable(BaseComponent):
    def __init__(self, **kwargs):
        super(Renderable, self).__init__(**kwargs)
        self.should_render = True


class SpriteRenderer(Renderable):
    def __init__(self, **kwargs):
        super(SpriteRenderer, self).__init__(**kwargs)
        if kwargs.has_key("path"):
            self.image = pygame.image.load(kwargs["path"])
        else:
            self.image = None


class Transform(BaseComponent):
    def __init__(self, **kwargs):
        super(Transform, self).__init__(**kwargs)
        self.position = kwargs.get("position", math.Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.scale = kwargs.get("scale", 1)


class TiledMap(Renderable):
    def __init(self, **kwargs):
        super(TiledMap, self).__init__(**kwargs)
        self.map_path = kwargs.get("map_path", None)
        self.map = tiledmap.load(self.map_path) if self.map_path is not None else None
