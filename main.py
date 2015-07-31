import sys, pygame
import time
from engine import scene, renderer

pygame.init()

width, height = 1440, 900

gameScene = scene.Scene()
gameRenderer = renderer.Renderer(pygame.display.set_mode((width,height)))

lastClock = time.clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    dt = time.clock() - lastClock

    gameScene.simulate_preframe(dt)
    gameRenderer.render(gameScene)
    gameScene.simulate_postframe(dt)
    pygame.display.flip()

    lastClock = time.clock()
