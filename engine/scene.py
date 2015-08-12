import collections


class Scene(object):
    """
    :type objects: dict[int, GameObject]
    :type camera: GameObject
    :type dt: float
    :type game: Application
    """
    def __init__(self, game):
        self.objects = collections.OrderedDict()
        self.camera = None
        self.dt = 0
        self.game = game
        self._maxIndex = 0

    def add_object(self, obj):
        """
        Adds a new object to the scene and changes its scene & id variables
        :param engine.GameObject obj: Game object to add to the scene
        """
        if obj.id is not None or obj.scene:
            raise ValueError("Object has an id or is assigned to a scene")

        self.objects[self._maxIndex] = obj
        obj.id = self._maxIndex
        self._maxIndex += 1
        obj.scene = self

    def remove_object(self, obj):
        """
        Removes an object from the scene, reverts the scene & id variables to None
        :param engine.gameobject.GameObject obj: Game object to remove from the scene
        """
        if obj.id is None or not self.objects.has_key(obj.id) or self.objects[obj.id] != obj:
            raise ValueError("Object not found in scene")

        del self.objects[obj.id]
        obj.scene = None
        obj.id = None

    def setup_frame(self, dt):
        """
        Performs initial setup needed before every frame
        :param float dt: Time (in seconds) passed since the previous frame
        """
        self.dt = dt

    def simulate_preframe(self):
        """
        Renders a frame before rendering is done
        :param float dt: Frametime
        """
        for obj in self.objects.values():
            obj.update()

    def simulate_postframe(self):
        """
        Renders a frame after rendering is done
        :param float dt: Frametime
        """
        for obj in self.objects.values():
            obj.update_postframe()

    def get_object_of_type(self, component_type):
        """
        Finds the first instance of an component of the specified type attached to an object
        :param engine.components.BaseComponent component_type: Class of the desired component
        :return: Found component, None if none exist
        """
        objects = self.get_objects_of_type(component_type)
        return objects[0] if len(objects) > 0 else None

    def get_objects_of_type(self, component_type):
        """
        Finds all objects which have the specified component
        :param engine.components.BaseComponent component_type: Class of the desired component
        :return: List of all components which were found
        """
        ret = []
        for key, obj in self.objects.iteritems():
            component = obj.get_component(component_type)
            if component is not None:
                ret.append(component)
        return ret

