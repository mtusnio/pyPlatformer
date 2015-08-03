__author__ = 'Maverick'
from engine import GameObject, components, Scene, Game


class Platformer(Game):
    def __init__(self):
        super(self.__class__, self).__init__()

    def init(self, width, height):
        super(self.__class__, self).init(width, height)
        self.scene = Scene(self)

        spriteobj = GameObject()
        spriteobj.addcomponents(components.SpriteRenderer(path="assets\sprite.png"), components.Transform())
        self.scene.addobject(spriteobj)

        self.scene.camera = GameObject()
        self.scene.camera.addcomponents(components.Transform(), components.Camera())
        self.scene.addobject(self.scene.camera)