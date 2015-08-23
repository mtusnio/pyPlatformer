from engine.gameobject import GameObject
import engine.components
import unittest
import engine.components


class TestGameObjectComponents(unittest.TestCase):
    def setUp(self):
        import engine.components
        self.testComponents = [ engine.components.BaseComponent(), engine.components.BaseComponent(),
                                engine.components.BaseComponent(), engine.components.BaseComponent() ]

    def test_create_object_with_components(self):
        obj = GameObject(*self.testComponents)

        self.assertSetEqual(set(self.testComponents), obj.components)

    def test_add_components(self):
        import itertools
        obj = self._get_obj_with_components()

        self.assertEqual(len(obj.components), len(self.testComponents))
        self.assertSetEqual(set(self.testComponents), obj.components)
        self.assertSetEqual(set(obj.components), set([x for x in obj.components if x.game_object == obj]))

    def test_add_no_component(self):
        obj = GameObject()
        obj.add_components()

        self.assertEqual(len(obj.components), 0)

    def test_add_existing_component(self):
        obj = GameObject()
        newList = self.testComponents + [engine.components.BaseComponent()]
        obj.add_components(*self.testComponents)
        obj.add_components(*newList)

        self.assertEqual(len(obj.components), len(newList))
        self.assertEqual(set(newList), obj.components)

    def test_remove_one_component(self):
        self._test_remove_components(self._get_obj_with_components(), 1)

    def test_remove_many_components(self):
        self._test_remove_components(self._get_obj_with_components(), 3)

    def test_get_component(self):
        obj = GameObject()
        testcomponent = engine.components.SpriteRenderer()
        obj.add_components(testcomponent)

        self.assertEqual(len(obj.get_components(engine.components.BaseComponent)), len(obj.components))
        self.assertEqual(testcomponent, obj.get_components(engine.components.SpriteRenderer)[0])

    def test_get_all_components(self):
        obj = GameObject()
        test_components = [engine.components.SpriteRenderer(), engine.components.Transform(), engine.components.SpriteBoundingRectangle()]
        obj.add_components(*test_components)

        self.assertSetEqual(set(test_components), set(obj.get_components()))

    def test_has_component(self):
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
        self.assertEqual(len(components), len(list(filter(lambda x: x.game_object is None, components))))

    def _get_obj_with_components(self):
        obj = GameObject()
        obj.add_components(*self.testComponents)
        return obj
