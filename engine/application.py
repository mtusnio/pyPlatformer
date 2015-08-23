__author__ = 'Maverick'
import pygame
from . import renderer
import sys
from engine.input import Input, KeyStatus
import logging


class MissingSceneError(Exception):
    """
    Thrown if the run function starts with no scene assigned to it
    """
    pass


class Application(object):
    def __init__(self):
        self.bindings = None
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

        level = logging.INFO
        if sys.flags.debug:
            level = logging.DEBUG

        logging.basicConfig(format='%(levelname)s:%(message)s', level=level)

        fps_report = 0
        while True:
            clock.tick()
            if len(pygame.event.get(pygame.QUIT)) > 0:
                sys.exit()

            dt = 1/clock.get_fps() if clock.get_fps() != 0 else 0.04

            fps_report += dt
            if fps_report >= 5:
                fps_report = 0
                logging.info("FPS: {fps}".format(fps=1.0/dt))

            self._handle_input(pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
                                                 pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]))

            self.scene.setup_frame(dt)
            self.scene.simulate_preframe()
            self.renderer.render(self.scene)
            self.scene.simulate_postframe()

            pygame.display.flip()

    def _handle_input(self, events):
        key_status = Input.key_status

        for key,val in key_status.items():
            if val == KeyStatus.DEPRESSED_THIS_FRAME:
                key_status[key] = KeyStatus.DEPRESSED
            elif val == KeyStatus.PRESSED_THIS_FRAME:
                key_status[key] = KeyStatus.PRESSED

        for event in events:
            if event.type == pygame.KEYDOWN:
                key_status[event.key] = KeyStatus.PRESSED_THIS_FRAME
            elif event.type == pygame.KEYUP:
                key_status[event.key] = KeyStatus.DEPRESSED_THIS_FRAME
