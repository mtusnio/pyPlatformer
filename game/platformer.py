__author__ = 'Maverick'
from engine import GameObject, components, Scene, Game


class Platformer(Game):
    def __init__(self):
        super(self.__class__, self).__init__()

    def init(self, width, height):
        super(self.__class__, self).init(width, height)
        self.scene = Scene(self)

        sprite_obj = GameObject()
        sprite_obj.add_components(components.SpriteRenderer(path="assets\sprite.png"), components.Transform())
        self.scene.add_object(sprite_obj)

        self.scene.camera = GameObject()
        self.scene.camera.add_components(components.Transform(), components.Camera())
        self.scene.add_object(self.scene.camera)