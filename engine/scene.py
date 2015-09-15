import collections
from .components import *


class ObjectInScene(Exception):
    """
    Thrown if, when adding an object or setting up a frame, it's detected that an object has already been
    added to a scene"""
    def __init__(self, obj, message=None):
        super(ObjectInScene, self).__init__(message)
        self.object = obj


class Scene(object):
    """
    :type objects: dict[int, GameObject]
    :type camera: GameObject
    :type dt: float
    :type time: float
    :type game: Application
    """
    def __init__(self, game):
        self.objects = collections.OrderedDict()
        self.camera = None
        self.dt = 0
        self.time = 0
        self.game = game
        self.objects_spawn_queue = []

        self._maxIndex = 0
        self._current_collisions = set()

    def add_object(self, obj):
        """
        Adds a new object to the scene; the object will be queued and created in the world at the start of next frame
        Raises ObjectInScene if object is already assigned to a scene

        :param engine.GameObject obj: Game object to add to the scene
        """
        if obj.id is not None or obj.scene:
            raise ObjectInScene(obj, "Object has an id or is assigned to a scene")

        if obj in self.objects_spawn_queue:
            raise ObjectInScene(obj, "Object is already queued to be added")

        self.objects_spawn_queue.append(obj)

    def remove_object(self, obj):
        """
        Removes an object from the scene, reverts the scene & id variables to None. If object is in queue, it will
        remove the object from the queue instead and treated as if it had never been added
        Raises ValueError if the object is not in queue or in scene's objects

        :param engine.gameobject.GameObject obj: Game object to remove from the scene
        """
        if obj not in self.objects_spawn_queue and (obj.id is None or \
                        obj.id not in self.objects or self.objects[obj.id] != obj):
            raise ValueError("Object not found in scene")

        if obj in self.objects_spawn_queue:
            self.objects_spawn_queue.remove(obj)
        else:
            del self.objects[obj.id]
            obj.scene = None
            obj.id = None

    def setup_frame(self, dt):
        """
        Performs initial setup needed before every frame, including adding queued objects
        Raises ObjectInScene if any queued objects have been added to another scene. Leaves the scene in working state
        for the next frame, but will stop adding objects until next setup_frame call

        :param float dt: Time (in seconds) passed since the previous frame
        """
        self.dt = dt
        self.time += dt
        self._add_awaiting_objects()

    def simulate_preframe(self):
        """
        Renders a frame before rendering is done
        """
        self._check_collisions()

        for obj in list(self.objects.values()):
            if not obj.started:
                obj.start()

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

    def _add_awaiting_objects(self):
        if len(self.objects_spawn_queue) > 0:
            objects_list = enumerate(self.objects_spawn_queue)
            for index, obj in objects_list:
                if obj.id is not None or obj.scene is not None:
                    del self.objects_spawn_queue[0:index+1]
                    raise ObjectInScene(obj, "Queued object was added to another scene")

                self.objects[self._maxIndex] = obj
                obj.id = self._maxIndex
                self._maxIndex += 1
                obj.scene = self
                obj.spawn()
        del self.objects_spawn_queue[:]

    def _check_collisions(self):
        checked = set()
        current_collisions = set()
        for pair in self._current_collisions:
            checked.add((pair[0].game_object, pair[1].game_object))
            checked.add((pair[1].game_object, pair[0].game_object))
            if self._run_collision_check(pair[0], pair[1]):
                current_collisions.add(pair)
            else:
                self._run_collision_for_pair(pair[0], pair[1], True)

        self._current_collisions = current_collisions

        for obj1 in list(self.objects.values()):
            collider1 = obj1.get_component(Collider)
            if collider1 is not None:
                for obj2 in list(self.objects.values()):
                    if obj1 is not obj2 and (obj1, obj2) not in checked:
                        collider2 = obj2.get_component(Collider)
                        if collider2 is not None:
                            checked.add((obj1, obj2))
                            checked.add((obj2, obj1))
                            if self._run_collision_check(collider1, collider2):
                                self._run_collision_for_pair(collider1, collider2)
                                self._current_collisions.add((collider1, collider2))

    def _run_collision_for_pair(self, collider1, collider2, end=False):
        for cmp in collider1.get_components():
            if end:
                cmp.end_collision(collider2.game_object)
            else:
                cmp.start_collision(collider2.game_object)

        for cmp in collider2.get_components():
            if end:
                cmp.end_collision(collider1.game_object)
            else:
                cmp.start_collision(collider1.game_object)

    def _run_collision_check(self, collider1, collider2):
        return collider1.get_collision_shape().colliderect(collider2.get_collision_shape())




