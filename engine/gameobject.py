from components import Transform


class GameObject(object):
    def __init__(self, *components):
        self.components = set()
        self.scene = None
        self.id = None

        self.add_components(*components)

    def add_components(self, *components):
        """
        :param component: Component list to add
        """
        self.components = self.components.union(set(components))
        for component in components:
            component.game_object = self

    def remove_components(self, *components):
        """
        :param components: List of components to remove
        """
        self.components = self.components.difference(set(components))
        for component in components:
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
        pass

    @property
    def transform(self):
        """
        Shortcut function, behaves exactly like get_component for the transform component
        :rtype Transform
        """
        return self.get_component(Transform)
