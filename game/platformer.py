__author__ = 'Maverick'
from engine import GameObject, Scene, Application, Input
import engine.components
from . import components
import pygame
from engine import tiledmap


class Platformer(Application):
    def __init__(self):
        super(Platformer, self).__init__()

    def init(self, width, height):
        super(self.__class__, self).init(width, height)
        self.scene = Scene(self)

        map_obj = GameObject()
        self.scene.add_object(map_obj)
        map_obj.add_components(engine.components.Transform(),
                               engine.components.TiledMap(map_path="assets\levels\level01.tmx"))

        self.scene.camera = GameObject()
        self.scene.add_object(self.scene.camera)
        self.scene.camera.add_components(engine.components.Transform(), engine.components.Camera())

        Input.bindings["left"] = pygame.K_a
        Input.bindings["right"] = pygame.K_d
        Input.bindings["jump"] = pygame.K_SPACE