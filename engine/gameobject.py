class GameObject(object):
    def __init__(self):
        self.components = set()
        self.scene = None

    def addcomponents(self, *components):
        """
        :param component: Component list to add
        """
        self.components = self.components.union(set(components))
        for cmp in components:
            cmp.gameobject = self

    def removecomponents(self, *components):
        """
        :param components: List of components to remove
        """
        self.components = self.components.difference(set(components))
        for cmp in components:
            cmp.gameobject = None

    def getcomponents(self, cls):
        """
        Returns all components which inherit from supplied class
        :param cls: Class of component to return
        :return : list
        """
        ret = []
        for cmp in self.components:
            if isinstance(cmp, cls):
                ret.append(cmp)
        return ret

    def getcomponent(self, cls):
        """
        Returns first found component of specified class
        :param cls: Class of component to return
        :return: First component that matches the class, None if none found
        """
        components = self.getcomponents(cls);
        return components[0] if len(components) > 0 else None

    def hascomponent(self, cls):
        """
        Returns true if the object has the specified component
        :param cls: Class of component to check
        :return boolean: true if object has this component
        """
        return len(self.getcomponents(cls) > 0)

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