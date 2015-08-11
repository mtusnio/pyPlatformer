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

        camera_position = (math.Vector2(0, 0), 0)
        if scene.camera is not None:
            camera = scene.camera.get_component(components.Camera)
            transform = scene.camera.get_component(components.Transform)
            if transform is not None:
                camera_position = (math.Vector2(transform.position[0], -transform.position[1]), transform.rotation)

        for obj in scene.objects.values():
            renderables = obj.get_components(components.Renderable)
            for rend in renderables:
                if rend.should_render is True:
                    self._render(rend, camera_position)

    def _render(self, renderable, camera_position):
        if isinstance(renderable, components.SpriteRenderer):
            if renderable.image is not None:
                obj_transform = renderable.game_object.get_component(components.Transform)
                if obj_transform is None:
                    self.screen.blit(renderable.image, renderable.image.get_rect())
                else:
                    surface = pygame.transform.rotozoom(copy.copy(renderable.image), obj_transform.rotation - camera_position[1], obj_transform.scale)
                    position = obj_transform.position - camera_position[0]
                    self.screen.blit(surface, surface.get_rect(center=position))
        elif isinstance(renderable, components.TiledMap):
            pass