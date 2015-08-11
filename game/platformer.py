__author__ = 'Maverick'
from engine import GameObject, Scene, Application, Input
import engine.components
import components
import pygame
from engine import tiledmap


class Platformer(Application):
    def __init__(self):
        super(Platformer, self).__init__()

    def init(self, width, height):
        super(self.__class__, self).init(width, height)
        self.scene = Scene(self)

        map_obj = GameObject()
        map_obj.add_components(engine.components.Transform(),
                               engine.components.TiledMap(path="assets\levels\level01.tmx"))
        self.scene.add_object(map_obj)

        self.scene.camera = GameObject()
        self.scene.camera.add_components(engine.components.Transform(), engine.components.Camera(),
                                         components.CameraControls())
        self.scene.add_object(self.scene.camera)

        Input.bindings["forward"] = pygame.K_w
        Input.bindings["left"] = pygame.K_a
        Input.bindings["back"] = pygame.K_s
        Input.bindings["right"] = pygame.K_d

        tiledmap.fill_scene_with_objects(self.scene, map_obj.get_component(engine.components.TiledMap).map)