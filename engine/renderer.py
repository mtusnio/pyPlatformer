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
                camera_position = (math.Vector2(transform.position[0], transform.position[1]), transform.rotation)

        camera_position[0][0] -= self.screen.get_width()/2
        camera_position[0][1] += self.screen.get_height()/2

        for obj in scene.objects.values():
            renderables = obj.get_components(components.Renderable)
            for rend in renderables:
                if rend.should_render is True:
                    self._render(rend, camera_position)

    def _render(self, renderable, camera_position):
        obj_transform = renderable.game_object.get_component(components.Transform)
        if obj_transform is not None:
            position = math.Vector2(obj_transform.position[0], obj_transform.position[1]) - camera_position[0]
            rotation = obj_transform.rotation - camera_position[1]
            scale = obj_transform.scale
        else:
            position = math.Vector2(0, 0)
            rotation = 0
            scale = 1

        if isinstance(renderable, components.SpriteRenderer):
            if renderable.image is not None:
                self._render_image(renderable.image, position, rotation, scale)
        elif isinstance(renderable, components.TiledMap):
            tiled_map = renderable.map
            if tiled_map is not None:
                for layer in tiled_map.visible_tile_layers:
                    for x, y, image in tiled_map.layers[layer].tiles():
                        tile_position = math.Vector2(x * image.get_width(), math.fabs(y - tiled_map.height) *
                                        image.get_height())
                        self._render_image(image, tile_position + position, rotation, scale)

    def _render_image(self, image, position, rotation, scale):
        position[1] = -position[1]
        surface = pygame.transform.rotozoom(image, rotation, scale)
        self.screen.blit(surface, surface.get_rect(center=position))