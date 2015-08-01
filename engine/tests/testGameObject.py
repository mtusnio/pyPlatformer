from engine.gameobject import GameObject
import unittest


class TestGameObjectComponents(unittest.TestCase):
    def setUp(self):
        import engine.components
        self.testComponents = [ engine.components.basecomponent.BaseComponent(), engine.components.basecomponent.BaseComponent(),
                                engine.components.basecomponent.BaseComponent(), engine.components.basecomponent.BaseComponent() ]

    def test_newcomponents(self):
        import itertools
        obj = self._get_obj_with_components()

        self.assertEqual(len(obj.components), len(self.testComponents))
        self.assertEqual(set(self.testComponents), obj.components)
        self.assertEqual(len(obj.components), len(list(itertools.ifilter(lambda x: x.gameobject == obj, obj.components))))

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

    def test_removeone(self):
        self._test_remove_components(self._get_obj_with_components(), 1)

    def test_removemultiple(self):
        self._test_remove_components(self._get_obj_with_components(), 3)

    def test_removeall(self):
        obj = self._get_obj_with_components()
        self._test_remove_components(obj, len(obj.components))

    def test_getcomponents(self):
        import engine.components
        obj = GameObject()
        testcomponent = engine.components.spriterenderer.SpriteRenderer()
        obj.addcomponents(testcomponent)

        self.assertEqual(len(obj.getcomponents(engine.components.basecomponent.BaseComponent)), len(obj.components))
        self.assertEqual(testcomponent, obj.getcomponents(engine.components.spriterenderer.SpriteRenderer)[0])

    def _test_remove_components(self, obj, count):
        import itertools
        components = list(obj.components)[0:count]
        length = len(obj.components)
        obj.removecomponents(*components)

        self.assertEqual(len(obj.components), length - count)
        self.assertSetEqual(obj.components & set(components), set())
        self.assertEqual(len(components), len(list(itertools.ifilter(lambda x: x.gameobject is None, components))))

    def _get_obj_with_components(self):
        obj = GameObject()
        obj.addcomponents(*self.testComponents)
        return obj
