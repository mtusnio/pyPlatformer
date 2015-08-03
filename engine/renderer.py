import pygame
import components
import copy
from engine import math


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen

    def render(self, scene):
        """
        Renders current state of scene
        :param engine.scene.Scene scene: engine.scene.Scene
        """
        self.screen.fill((0, 0, 0))

        cameraposition = (math.Vector2(0, 0), 0)
        if scene.camera is not None:
            camera = scene.camera.get_component(components.Camera)
            transform = scene.camera.get_component(components.Transform)
            if transform is not None:
                cameraposition = (transform.position, transform.rotation)

        for obj in scene.objects.values():
            sprites = obj.get_components(components.SpriteRenderer)
            for spr in sprites:
                if spr.image is not None:
                    self._render_sprite(spr, cameraposition)

    def _render_sprite(self, sprite, cameraposition):
        objtransform = sprite.gameobject.get_component(components.Transform)
        if objtransform is None:
            self.screen.blit(sprite.image, sprite.image.get_rect())
        else:
            surface = pygame.transform.rotozoom(copy.copy(sprite.image), objtransform.rotation - cameraposition[1], objtransform.scale)
            position = objtransform.position - cameraposition[0]
            self.screen.blit(surface, surface.get_rect(center=position))
