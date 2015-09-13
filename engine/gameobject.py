from .components import Transform


class GameObject(object):
    def __init__(self, *components):
        self.components = []
        self.scene = None
        self.id = None
        self.name = None
        self.started = False

        self.add_components(*components)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(self.id) * hash(self.name)

    def destroy(self):
        for cmp in self.components:
            cmp.destroy()
        if self.scene is not None:
            self.scene.remove_object(self)
        cmp = []

    def add_components(self, *components):
        """
        :param component: Component list to add
        """
        self.components.extend([ x for x in components if x not in self.components])
        for component in components:
            component.game_object = self

        for component in components:
            component.on_add()

    def remove_components(self, *components):
        """
        :param components: List of components to remove
        """
        removed = [x for x in components if x in self.components]
        self.components = [x for x in self.components if x not in components]
        for component in removed:
            component.game_object = None

    def get_components(self, cls=None):
        """
        Returns all components which inherit from supplied class

        :param cls: Class of component to return, all will be returned if None
        :return list: List of all components fitting the parameters
        """
        if cls is None:
            return list(self.components)

        ret = []
        for component in self.components:
            if isinstance(component, cls):
                ret.append(component)
        return ret

    def get_component(self, cls):
        """
        Returns first found component of specified class

        :param cls: Class of component to return
        :return engine.components.BaseComponent: First component that matches the class, None if none found
        """
        components = self.get_components(cls)
        return components[0] if len(components) > 0 else None

    def has_component(self, cls):
        """
        Returns true if the object has the specified component

        :param cls: Class of component to check
        :return boolean: true if object has this component
        """
        return len(self.get_components(cls)) > 0

    def spawn(self):
        """
        Called immediately after an object was created in the scene
        """
        for cmp in self.components:
            cmp.spawn()

    def start(self):
        """
        Called right before the object's first update
        """
        for cmp in self.components:
            cmp.start()
        self.started = True

    def update(self):
        """
        Runs object simulation before rendering
        """
        for component in self.components:
            component.update()

    def update_postframe(self):
        """
        Runs object simulation after rendering
        """
        for component in self.components:
            component.update_postframe()

    @property
    def transform(self):
        """
        Shortcut function, behaves exactly like get_component for the transform component

        :rtype Transform
        """
        return self.get_component(Transform)
