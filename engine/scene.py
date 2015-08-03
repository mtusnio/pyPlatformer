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
        obj.id = self.maxIndex
        self.maxIndex += 1
        obj.scene = self

    def removeobject(self, obj):
        """
        :param engine.gameobject.GameObject obj: Game object to remove from the scene
        """
        if obj.id is None or not self.objects.has_key(obj.id) or self.objects[obj.id] != obj:
            raise ValueError("Object not found in scene")

        del self.objects[obj.id]
        obj.scene = None

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
