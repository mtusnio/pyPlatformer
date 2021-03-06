import pygame
from . import components
from engine.math import Vector2, Rect
from pygame import transform
from .interface import SpriteElement


class Renderer(object):
    """
    :type screen: pygame.Surface
    """
    def __init__(self, screen):
        self.screen = screen

    def render(self, scene):
        """
        Renders current state of scene

        :param engine.scene.Scene scene: Scene to render
        """
        tiled_map = scene.get_object_of_type(components.TiledMap)
        if tiled_map is not None:
            color = ["".join(tiled_map.map.background_color[i:i+2])
                     for i in range(1, len(tiled_map.map.background_color) - 1, 2)]
            self.screen.fill(tuple(int(x, 16) for x in color))
        else:
            self.screen.fill((0, 0, 0))

        camera_position = (Vector2(0, 0), 0)
        if scene.camera is not None:
            camera = scene.camera.get_component(components.Camera)
            transform = scene.camera.get_component(components.Transform)
            if transform is not None:
                camera_position = (Vector2(transform.position[0], transform.position[1]), transform.rotation)

        camera_position[0][0] -= self.screen.get_width()/2
        camera_position[0][1] -= self.screen.get_height()/2

        for obj in list(scene.objects.values()):
            renderables = obj.get_components(components.Renderable)
            for rend in renderables:
                if rend.should_render is True:
                    self._render(rend, camera_position)

        if scene.interface is not None:
            self._render_interface(scene.interface)

    def _render(self, renderable, camera_position):
        surface_rect = self.screen.get_rect(center=camera_position[0] + Vector2(self.screen.get_width()/2, self.screen.get_height()/2))

        obj_transform = renderable.game_object.get_component(components.Transform)
        if obj_transform is not None:
            position = Vector2(obj_transform.position[0], obj_transform.position[1]) - camera_position[0]
            rotation = obj_transform.rotation - camera_position[1]
            scale = obj_transform.scale
        else:
            position = Vector2(0, 0)
            rotation = 0
            scale = 1

        if isinstance(renderable, components.SpriteRenderer):
            if renderable.image is not None and \
                    surface_rect.colliderect(renderable.image.get_rect(center=obj_transform.position)):
                self._render_image(renderable.image, position, rotation, scale,
                                   renderable.vertical_flip, renderable.horizontal_flip)
        elif isinstance(renderable, components.TiledMap):
            tiled_map = renderable.map
            if tiled_map is not None:
                tile_width = tiled_map.tilewidth
                tile_height = tiled_map.tileheight
                for layer in tiled_map.visible_tile_layers:
                    for x, y, image in tiled_map.layers[layer].tiles():
                        tile_position = Vector2(x * tile_width + tile_width/2, y * tile_height + tile_height/2)
                        if renderable.get_rectangle_for_tile((x,y)).colliderect(surface_rect):
                            self._render_image(image, tile_position + position, rotation, scale)

    def _render_image(self, image, position, rotation, scale, ver_flip=False, hor_flip=False):
        surface = pygame.transform.rotozoom(image, rotation, scale)
        if ver_flip or hor_flip:
            surface = pygame.transform.flip(surface, hor_flip, ver_flip)

        self.screen.blit(surface, surface.get_rect(center=position))

    def _render_interface(self, interface):
        """

        :param engine.interface.Canvas interface: Interface to render
        """
        for element in interface.get_children():
            if isinstance(element, SpriteElement):
                sprite = element.sprite
                if sprite is not None:
                    try:
                        surface = transform.smoothscale(sprite, (element.width, element.height))
                    except ValueError:
                        surface = transform.scale(sprite, (element.width, element.height))
                    self.screen.blit(surface, surface.get_rect(x=element.position.x, y=element.position.y))
