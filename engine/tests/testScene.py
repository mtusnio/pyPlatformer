import unittest
from engine import Scene, GameObject

class TestSceneObjects(unittest.TestCase):
    def test_addobjects(self):
        scene = Scene()
        objects = [GameObject() for x in xrange(0, 10)]
        for obj in objects:
            scene.add_object(obj)
        self.assertEqual(len(scene.objects), len(objects))

        ids = set()
        for key, obj in scene.objects.iteritems():
            self.assertNotIn(obj.id, ids)
            ids.add(obj.id)
            self.assertEqual(scene, obj.scene)
            self.assertIn(obj, objects)

        with self.assertRaises(ValueError):
            scene.add_object(objects[0])

    def test_removeobject(self):
        scene = Scene()

        objects = [GameObject() for x in xrange(0, 10)]
        for obj in objects:
            scene.add_object(obj)

        with self.assertRaises(ValueError):
            scene.remove_object(GameObject())

        cut = len(objects)//2
        for obj in objects[:cut]:
            scene.remove_object(obj)
        self.assertEqual(len(objects) - cut, len(scene.objects))
        self.assertSetEqual(set(objects[cut:]), set(scene.objects.values()))
