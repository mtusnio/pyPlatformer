import pygame
import components
import copy

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen

    def render(self, scene):
        """
        Renders current state of scene
        :param engine.scene.Scene scene: engine.scene.Scene
        """
        self.screen.fill((0, 0, 0))

        for obj in scene.objects.values():
            sprites = obj.getcomponents(components.SpriteRenderer)
            for spr in sprites:
                if spr.image is not None:
                    self._rendersprite(spr)

    def _rendersprite(self, sprite):
        objtransform = sprite.gameobject.getcomponent(components.Transform)
        if objtransform is None:
            self.screen.blit(sprite.image, sprite.image.get_rect())
        else:
            surface = pygame.transform.rotozoom(copy.copy(sprite.image), objtransform.rotation, objtransform.scale)
            self.screen.blit(surface, surface.get_rect(center=objtransform.position))
