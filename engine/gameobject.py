class GameObject(object):
    def __init__(self):
        self.components = set()
        self.scene = None
        self.id = None

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

    def get_components(self, cls):
        """
        Returns all components which inherit from supplied class
        :param cls: Class of component to return
        :return : list
        """
        ret = []
        for component in self.components:
            if isinstance(component, cls):
                ret.append(component)
        return ret

    def get_component(self, cls):
        """
        Returns first found component of specified class
        :param cls: Class of component to return
        :return: First component that matches the class, None if none found
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
        pass

    def update_postframe(self):
        """
        Runs object simulation after rendering
        """
        pass