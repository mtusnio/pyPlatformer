import collections


class GameObject(object):
    def __init__(self):
        self.components = collections.OrderedDict()
        self.scene = None

    def addcomponent(self, component):
        """
        :param engine.components.basecomponent.BaseComponent component: Component to add
        """


    def removecomponent(self, component):
        pass

    def run_preframe(self):
        """
        Runs object simulation before rendering
        """
        pass

    def run_postframe(self):
        """
        Runs object simulation after rendering
        """
        pass

