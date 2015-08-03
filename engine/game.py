__author__ = 'Maverick'
import pygame
import renderer
import sys


class MissingSceneError(Exception):
    """
    Thrown if the run function starts with no scene assigned to it
    """
    pass


class Game(object):
    def __init__(self):
        self.bindings = None
        self.input = None
        self.scene = None
        self.renderer = None

    def init(self, width, height):
        """
        Initializes the game, runs pygame.init()
        :param int width: width of the game window
        :param int height: height of the game window
        """
        pygame.init()
        self.renderer = renderer.Renderer(pygame.display.set_mode((width,height)))

    def run(self):
        """
        Runs one frame of the game. init() needs to be run first
        """
        clock = pygame.time.Clock()

        if self.scene is None:
            raise MissingSceneError()

        while True:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            dt = 1/clock.get_fps() if clock.get_fps() != 0 else 0.16

            self.scene.setup_frame(dt)
            self.scene.simulate_preframe()
            self.renderer.render(self.scene)
            self.scene.simulate_postframe()

            pygame.display.flip()

