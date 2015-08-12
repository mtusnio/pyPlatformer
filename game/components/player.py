__author__ = 'Maverick'
from engine import components


class Player(components.BaseComponent):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

    def update(self):
        player = self.game_object
        camera = player.scene.camera
        camera.transform.position = player.transform.position
