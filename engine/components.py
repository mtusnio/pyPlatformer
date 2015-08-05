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
        super(self.__class__, self).__init__(**kwargs)
        self.fov = kwargs.get("fov", 80)


class SpriteRenderer(BaseComponent):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        if kwargs.has_key("path"):
            self.image = pygame.image.load(kwargs["path"])
        else:
            self.image = None


class Transform(BaseComponent):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.position = kwargs.get("position", math.Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.scale = kwargs.get("scale", 1)