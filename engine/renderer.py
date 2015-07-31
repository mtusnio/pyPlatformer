import pygame
from components.spriterenderer import SpriteRenderer

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen

    def render(self, scene):
        """
        Renders current state of scene
        :param engine.scene.Scene scene: engine.scene.Scene
        """
        self.screen.fill((0, 0, 0))

        for obj in scene.objects:
            sprites = obj.getcomponents(SpriteRenderer)
            for spr in sprites:
                self._rendersprite(spr)

    def _rendersprite(self, sprite):
        self.screen.blit(sprite.image)