import sys, pygame
from engine import scene, renderer, gameobject, components

pygame.init()

width, height = 1440, 900

gameScene = scene.Scene()
gameRenderer = renderer.Renderer(pygame.display.set_mode((width,height)))

spriteObj = gameobject.GameObject()
spriteObj.addcomponents(components.SpriteRenderer(path="assets\sprite.png"), components.Transform())
gameScene.addobject(spriteObj)

cameraObj = gameobject.GameObject()
cameraObj.addcomponents(components.Transform(), components.Camera())
gameScene.addobject(cameraObj)
scene.camera = cameraObj

clock = pygame.time.Clock()
while True:
    lastClock = clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    dt = 1/clock.get_fps() if clock.get_fps() != 0 else 0.16

    gameScene.setupframe(dt)
    gameScene.simulate_preframe()
    gameRenderer.render(gameScene)
    gameScene.simulate_postframe()
    pygame.display.flip()