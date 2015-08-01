import unittest


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


class TestGameObjectComponents(unittest.TestCase):
    def setUp(self):
        import engine.components
        self.testComponents = [ engine.components.basecomponent.BaseComponent(), engine.components.basecomponent.BaseComponent(),
                                engine.components.basecomponent.BaseComponent(), engine.components.basecomponent.BaseComponent() ]

    def test_newcomponents(self):
        obj = GameObject()
        obj.addcomponents(*self.testComponents)
        self.assertEqual(len(obj.components), len(self.testComponents))
        self.assertEqual(set(self.testComponents), obj.components)

    def test_noadd(self):
        obj = GameObject()
        obj.addcomponents()
        self.assertEqual(len(obj.components), 0)

    def test_addexisting(self):
        import engine.components
        obj = GameObject()
        newList = self.testComponents + [engine.components.basecomponent.BaseComponent()]
        obj.addcomponents(*self.testComponents)
        obj.addcomponents(*newList)
        self.assertEqual(len(obj.components), len(newList))
        self.assertEqual(set(newList), obj.components)

    def test_clear(self):
        obj = self._get_obj_with_components()
        obj.removecomponents(*obj.components)
        self.assertEqual(len(obj.components), 0)

    def test_removeone(self):
        self._test_remove_components(self._get_obj_with_components(), 1)

    def test_removemultiple(self):
        self._test_remove_components(self._get_obj_with_components(), 3)

    def test_gameobjectchanged(self):
        import itertools
        obj = self._get_obj_with_components()
        self.assertEqual(len(obj.components), len(list(itertools.ifilter(lambda x: x.gameobject == obj, obj.components))))
        removedComponents = list(obj.components)
        obj.removecomponents(*obj.components)
        self.assertEqual(len(removedComponents), len(list(itertools.ifilter(lambda x: x.gameobject == None, removedComponents))))

    def _test_remove_components(self, obj, count):
        components = list(obj.components)[0:count]
        length = len(obj.components)
        obj.removecomponents(*components)
        self.assertEqual(len(obj.components), length - count)
        self.assertSetEqual(obj.components & set(components), set())

    def _get_obj_with_components(self):
        obj = GameObject()
        obj.addcomponents(*self.testComponents)
        return obj

if __name__ == "__main__":
    unittest.main()