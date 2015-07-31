import sys, pygame

pygame.init()

width, height = 1440, 900

pygame.display.set_mode((width,height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
