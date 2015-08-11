__author__ = 'Maverick'
from engine import GameObject, Scene, Game, Input
import engine.components
import components
import pygame


class Platformer(Game):
    def __init__(self):
        super(Platformer, self).__init__()

    def init(self, width, height):
        super(self.__class__, self).init(width, height)
        self.scene = Scene(self)

        sprite_obj = GameObject()
        sprite_obj.add_components(engine.components.SpriteRenderer(path="assets\sprite.png"),
                                  engine.components.Transform())
        self.scene.add_object(sprite_obj)

        self.scene.camera = GameObject()
        self.scene.camera.add_components(engine.components.Transform(), engine.components.Camera(),
                                         components.CameraControls())
        self.scene.add_object(self.scene.camera)

        Input.bindings["forward"] = pygame.K_w
        Input.bindings["left"] = pygame.K_a
        Input.bindings["back"] = pygame.K_s
        Input.bindings["right"] = pygame.K_d