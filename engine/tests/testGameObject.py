from engine.gameobject import GameObject
import engine.components
import unittest
import engine.components

class TestGameObjectComponents(unittest.TestCase):
    def setUp(self):
        import engine.components
        self.testComponents = [ engine.components.BaseComponent(), engine.components.BaseComponent(),
                                engine.components.BaseComponent(), engine.components.BaseComponent() ]

    def test_newcomponents(self):
        import itertools
        obj = self._get_obj_with_components()

        self.assertEqual(len(obj.components), len(self.testComponents))
        self.assertEqual(set(self.testComponents), obj.components)
        self.assertEqual(len(obj.components), len(list(itertools.ifilter(lambda x: x.gameobject == obj, obj.components))))

    def test_noadd(self):
        obj = GameObject()
        obj.add_components()

        self.assertEqual(len(obj.components), 0)

    def test_addexisting(self):
        obj = GameObject()
        newList = self.testComponents + [engine.components.BaseComponent()]
        obj.add_components(*self.testComponents)
        obj.add_components(*newList)

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
        obj = GameObject()
        testcomponent = engine.components.SpriteRenderer()
        obj.add_components(testcomponent)

        self.assertEqual(len(obj.get_components(engine.components.BaseComponent)), len(obj.components))
        self.assertEqual(testcomponent, obj.get_components(engine.components.SpriteRenderer)[0])

    def test_hascomponent(self):
        obj = GameObject()
        self.assertFalse(obj.has_component(engine.components.BaseComponent))
        obj.add_components(engine.components.Transform(), engine.components.SpriteRenderer())
        self.assertFalse(obj.has_component(engine.components.Camera))
        self.assertTrue(obj.has_component(engine.components.SpriteRenderer))
        self.assertTrue(obj.has_component(engine.components.BaseComponent))

    def _test_remove_components(self, obj, count):
        import itertools
        components = list(obj.components)[0:count]
        length = len(obj.components)
        obj.remove_components(*components)

        self.assertEqual(len(obj.components), length - count)
        self.assertSetEqual(obj.components & set(components), set())
        self.assertEqual(len(components), len(list(itertools.ifilter(lambda x: x.gameobject is None, components))))

    def _get_obj_with_components(self):
        obj = GameObject()
        obj.add_components(*self.testComponents)
        return obj
