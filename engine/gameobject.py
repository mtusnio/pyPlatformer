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