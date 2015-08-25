import collections
from .components import *


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
        if obj.id is None or obj.id not in self.objects or self.objects[obj.id] != obj:
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
        """
        self._check_collisions()

        for obj in list(self.objects.values()):
            obj.update()

    def simulate_postframe(self):
        """
        Renders a frame after rendering is done
        """
        for obj in list(self.objects.values()):
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
        for key, obj in self.objects.items():
            component = obj.get_component(component_type)
            if component is not None:
                ret.append(component)
        return ret

    def get_object_by_name(self, name):
        """
        Returns first found object with the specified name
        :param name: String name of the object, if None it will return first nameless object
        :return: Game object
        """
        objs = self.get_objects_by_name(name)
        return None if len(objs) == 0 else objs[0]

    def get_objects_by_name(self, name):
        """
        Returns all objects with the given name
        :param None name: String name of the objects, None will return all nameless objects
        :return: List of game objects
        """
        ret = []
        for key,obj in self.objects.items():
            if obj.name == name:
                ret.append(obj)
        return ret

    def _check_collisions(self):
        checked = set()
        for obj1 in list(self.objects.values()):
            collider1 = obj1.get_component(Collider)
            if collider1 is not None:
                for obj2 in list(self.objects.values()):
                    if obj1 is not obj2 and (obj1, obj2) not in checked:
                        collider2 = obj2.get_component(Collider)
                        if collider2 is not None:
                            checked.add((obj1, obj2))
                            checked.add((obj2, obj1))
                            self._run_collision_check(collider1, collider2)

    def _run_collision_check(self, collider1, collider2):
        first_rects = collider1.get_collision_shapes(collider2.game_object)
        second_rects = collider2.get_collision_shapes(collider1.game_object)

        first_collision_data = []
        second_collision_data = []

        found_indices = set()
        for rectangle in first_rects:
            indices = rectangle.collidelistall(second_rects)
            if len(indices) > 0:
                found_rectangles = [second_rects[i] for i in indices if i not in found_indices]
                first_collision_data.extend(found_rectangles)
                second_collision_data.append(rectangle)

        assert (len(first_collision_data) > 0 and len(second_collision_data) > 0) \
               or (len(first_collision_data) == 0 and len(second_collision_data) == 0)

        if len(first_collision_data) > 0 and len(second_collision_data) > 0:
            for component in collider1.game_object.get_components():
                if hasattr(component, "collide"):
                    component.collide(collider2.game_object, *first_collision_data)

            for component in collider2.game_object.get_components():
                if hasattr(component, "collide"):
                    component.collide(collider1.game_object, *second_collision_data)
