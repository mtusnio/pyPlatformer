__author__ = 'Maverick'

from pytmx.util_pygame import handle_transformation, smart_convert
from pytmx import TiledMap
import engine, components, math
import pygame
import logging


def image_loader(filename, colorkey, **kwargs):
    if colorkey:
        colorkey = pygame.Color('#{0}'.format(colorkey))

    pixelalpha = kwargs.get('pixelalpha', True)
    image = smart_convert(pygame.image.load(filename), colorkey, pixelalpha)

    def load_image(rect=None, flags=None):
        if rect:
            try:
                tile = image.subsurface(rect)
            except ValueError:
                logging.error('Tile bounds outside bounds of tileset image')
                raise
        else:
            tile = image.copy()

        if flags:
            tile = handle_transformation(tile, flags)

        return tile

    return load_image


def load(filename, *args, **kwargs):
    kwargs["image_loader"] = image_loader
    return TiledMap(filename, *args, **kwargs)