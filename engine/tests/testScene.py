import unittest
from engine import Scene, GameObject, components
from engine.scene import ObjectInScene


class TestSceneObjects(unittest.TestCase):
    def test_scene_adds_objects(self):
        scene = Scene(None)
        objects = [GameObject() for x in range(0, 1000)]
        for obj in objects:
            scene.add_object(obj)
        scene.setup_frame(1.0)
        self.assertEqual(len(scene.objects), len(objects))
        self.assertEqual(set(scene.objects.values()), set(objects))

    def test_scene_assigns_unique_ids(self):
        rng = list(range(0, 1000))
        scene = Scene(None)
        for obj in [GameObject() for x in rng]:
            scene.add_object(obj)
        scene.setup_frame(1.0)
        self.assertEqual(set(scene.objects.keys()), set(rng))

    def test_scene_sets_game_objects_scene_attribute(self):
        scene = Scene(None)
        obj = GameObject()
        scene.add_object(obj)
        scene.setup_frame(1.0)
        self.assertTrue(obj.scene, scene)

    def test_scene_does_not_allow_duplicated_additions(self):
        scene = Scene(None)
        obj = GameObject()
        scene.add_object(obj)
        with self.assertRaises(ObjectInScene):
            scene.add_object(obj)

    def test_scene_throws_exception_after_setup_if_object_queued_in_two_scenes(self):
        first_scene = Scene(None)
        second_scene = Scene(None)

        obj = GameObject()
        first_scene.add_object(obj)
        second_scene.add_object(obj)

        first_scene.setup_frame(1.0)
        with self.assertRaises(ObjectInScene):
            second_scene.setup_frame(1.0)

    def test_scene_does_not_allow_objects_from_another_scene(self):
        first_scene = Scene(None)
        second_scene = Scene(None)

        obj = GameObject()
        first_scene.add_object(obj)
        first_scene.setup_frame(1.0)
        with self.assertRaises(ObjectInScene):
            second_scene.add_object(obj)

    def test_removes_problematic_object_from_queue(self):
        first_scene = Scene(None)
        obj = GameObject()
        first_scene.add_object(obj)
        second_scene = Scene(None)
        second_scene.add_object(obj)
        first_scene.setup_frame(1.0)
        try:
            second_scene.setup_frame(1.0)
        except ObjectInScene:
            pass
        self.assertNotIn(obj, second_scene.objects_spawn_queue)


    def test_scene_remove_queued_object(self):
        scene = Scene(None)
        obj = GameObject()
        scene.add_object(obj)
        scene.remove_object(obj)
        scene.setup_frame(1.0)
        self.assertEqual(0, len(scene.objects))

    def test_remove_on_empty_exception(self):
        scene = Scene(None)
        with self.assertRaises(ValueError):
            scene.remove_object(GameObject())

    def test_remove_object(self):
        scene = Scene(None)
        objects = [GameObject() for x in range(0, 1000)]
        for obj in objects:
            scene.add_object(obj)
        scene.setup_frame(1.0)
        cut = len(objects)//2
        for obj in objects[:cut]:
            scene.remove_object(obj)
        self.assertEqual(len(objects) - cut, len(scene.objects))
        self.assertSetEqual(set(objects[cut:]), set(scene.objects.values()))

    def test_removed_objects_are_cleared_on_frame_end(self):
        scene = Scene(None)
        objects = [GameObject() for x in range(0, 100)]
        for obj in objects:
            scene.add_object(obj)

        scene.setup_frame(1.0)
        scene.simulate_preframe()
        scene.simulate_postframe()

        scene.remove_object(objects[0])

        scene.setup_frame(1.0)
        scene.simulate_preframe()
        scene.simulate_postframe()

        self.assertIsNone(objects[0].scene)
        self.assertIsNone(objects[0].id)

    def test_find_first_of_type(self):
        scene = Scene(None)
        first = GameObject(components.Camera())
        second = GameObject(components.Camera())
        scene.add_object(first)
        scene.add_object(second)
        scene.setup_frame(1.0)

        tested_component = first.get_component(components.Camera)
        self.assertIs(scene.get_object_of_type(components.Camera), tested_component)

    def test_find_ordered_objects_of_type(self):
        scene = Scene(None)
        objects = [GameObject(components.Camera()) for x in range(0, 5)]
        for obj in objects:
            scene.add_object(obj)
        scene.setup_frame(1.0)
        component_list = [x.get_component(components.Camera) for x in objects]
        self.assertEqual(component_list,
                         scene.get_objects_of_type(components.Camera))
        self.assertNotEqual(component_list[::-1],
                            scene.get_objects_of_type(components.Camera))

    def test_return_named_object(self):
        scene = Scene(None)
        game_objects = [GameObject() for x in range(0, 10)]
        for index,obj in enumerate(game_objects):
            obj.name = str(index)
            scene.add_object(obj)
        scene.setup_frame(1.0)
        self.assertIs(game_objects[2], scene.get_object_by_name("2"))

    def test_return_named_objects(self):
        scene = Scene(None)
        game_objects = [GameObject() for x in range(0, 10)]
        for index,obj in enumerate(game_objects):
            obj.name = str(index % 2)
            scene.add_object(obj)
        scene.setup_frame(1.0)
        self.assertEqual([x for x in game_objects if int(x.name) % 2 == 0], scene.get_objects_by_name("0"))

    def test_return_nameless(self):
        scene = Scene(None)
        game_objects = [GameObject() for x in range(0, 10)]
        for index,obj in enumerate(game_objects):
            obj.name = None if index % 2 == 0 else "name"
            scene.add_object(obj)
        scene.setup_frame(1.0)
        self.assertEqual([x for x in game_objects if x.name is None], scene.get_objects_by_name(None))

    def test_find_no_objects_of_type(self):
        scene = Scene(None)
        obj = GameObject(components.Camera())
        scene.add_object(obj)

        self.assertIsNone(scene.get_object_of_type(components.Renderable))
        self.assertItemsEqual(scene.get_objects_of_type(components.Renderable), [])
