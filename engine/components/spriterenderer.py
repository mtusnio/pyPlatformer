import pygame
import basecomponent


class SpriteRenderer(basecomponent.BaseComponent):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        if kwargs.has_key("path"):
            self.image = pygame.image.load(kwargs["path"])
        else:
            self.image = None


