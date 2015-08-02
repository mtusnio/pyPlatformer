import collections


class Scene(object):
    def __init__(self):
        self.objects = collections.OrderedDict()
        self.maxIndex = 0
        self.camera = None

    def addobject(self, obj):
        """
        :param engine.gameobject.GameObject obj: Game object to add to the scene
        """
        self.objects[self.maxIndex] = obj
        self.maxIndex += 1
        obj.scene = self

    def simulate_preframe(self, dt):
        """
        Renders a frame before rendering is done
        :param float dt: Frametime
        """
        pass

    def simulate_postframe(self, dt):
        """
        Renders a frame after rendering is done
        :param float dt: Frametime
        """
        pass
