import unittest
from engine import Scene, GameObject, components


class TestSceneObjects(unittest.TestCase):
    def test_scene_adds_objects(self):
        scene = Scene(None)
        objects = [GameObject() for x in xrange(0, 5000)]
        for obj in objects:
            scene.add_object(obj)
        self.assertEqual(len(scene.objects), len(objects))
        self.assertEqual(set(scene.objects.values()), set(objects))

    def test_scene_assigns_unique_ids(self):
        rng = range(0, 10000)
        scene = Scene(None)
        for obj in [GameObject() for x in rng]:
            scene.add_object(obj)

        self.assertEqual(set(scene.objects.keys()), set(rng))

    def test_scene_sets_game_objects_scene_attribute(self):
        scene = Scene(None)
        obj = GameObject()
        scene.add_object(obj)
        self.assertTrue(obj.scene, scene)

    def test_scene_does_not_allow_duplicated_additions(self):
        scene = Scene(None)
        obj = GameObject()
        scene.add_object(obj)
        with self.assertRaises(ValueError):
            scene.add_object(obj)

    def test_remove_on_empty_exception(self):
        scene = Scene(None)
        with self.assertRaises(ValueError):
            scene.remove_object(GameObject())

    def test_removeobject(self):
        scene = Scene(None)
        objects = [GameObject() for x in xrange(0, 1000)]
        for obj in objects:
            scene.add_object(obj)

        cut = len(objects)//2
        for obj in objects[:cut]:
            scene.remove_object(obj)
        self.assertEqual(len(objects) - cut, len(scene.objects))
        self.assertSetEqual(set(objects[cut:]), set(scene.objects.values()))

    def test_find_first_of_type(self):
        scene = Scene(None)
        first = GameObject(components.Camera())
        second = GameObject(components.Camera())
        scene.add_object(first)
        scene.add_object(second)

        tested_component = first.get_component(components.Camera)
        self.assertIs(scene.get_object_of_type(components.Camera), tested_component)

    def test_find_ordered_objects_of_type(self):
        scene = Scene(None)
        objects = [GameObject(components.Camera()) for x in range(0, 5)]
        for obj in objects:
            scene.add_object(obj)

        component_list = [x.get_component(components.Camera) for x in objects]
        self.assertEqual(component_list,
                         scene.get_objects_of_type(components.Camera))
        self.assertNotEqual(component_list[::-1],
                            scene.get_objects_of_type(components.Camera))

    def test_find_no_objects_of_type(self):
        scene = Scene(None)
        obj = GameObject(components.Camera())
        scene.add_object(obj)

        self.assertIsNone(scene.get_object_of_type(components.Renderable))
        self.assertItemsEqual(scene.get_objects_of_type(components.Renderable), [])
