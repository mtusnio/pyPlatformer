__author__ = 'Maverick'
from engine import components


class Player(components.BaseComponent):
    GRAVITY = 320.0

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.flying = True

    def update(self):
        player = self.game_object

        camera = player.scene.camera
        camera.transform.position = player.transform.position

        tiled_map = player.scene.get_object_of_type(components.TiledMap)
        if tiled_map is None:
            return

        transform = player.transform
        pos = transform.position
        if not tiled_map.is_position_in_map(pos):
            return
        x, y = tiled_map.get_tile_for_position(pos)

        dt = self.game_object.scene.dt
        #if self.flying:
        #    transform.position[1] += self.GRAVITY * dt

    def collide(self, game_object, *rectangles):
        pass

