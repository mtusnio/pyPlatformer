import collections


class Scene(object):
    def __init__(self):
        self.objects = collections.OrderedDict()
        self.camera = None
        self._maxIndex = 0

    def addobject(self, obj):
        """
        Adds a new object to the scene and changes its scene & id variables
        :param engine.gameobject.GameObject obj: Game object to add to the scene
        """
        self.objects[self._maxIndex] = obj
        obj.id = self._maxIndex
        self._maxIndex += 1
        obj.scene = self

    def removeobject(self, obj):
        """
        Removes an object from the scene, reverts the scene & id variables to None
        :param engine.gameobject.GameObject obj: Game object to remove from the scene
        """
        if obj.id is None or not self.objects.has_key(obj.id) or self.objects[obj.id] != obj:
            raise ValueError("Object not found in scene")

        del self.objects[obj.id]
        obj.scene = None
        obj.id = None

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
