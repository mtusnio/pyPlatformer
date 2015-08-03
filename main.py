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
    lastClock = clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    dt = lastClock / 1000.0

    gameScene.simulate_preframe(dt)
    gameRenderer.render(gameScene)
    gameScene.simulate_postframe(dt)
    pygame.display.flip()