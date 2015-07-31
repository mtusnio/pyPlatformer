import pygame
import basecomponent

class SpriteRenderer(basecomponent.BaseComponent):
    def __init__(self, **kwargs):
        super(basecomponent.BaseComponent, self).__init__(kwargs)
        self.image = pygame.image.load(kwargs["path"])



