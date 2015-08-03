import unittest
from engine import Scene, GameObject

class TestSceneObjects(unittest.TestCase):
    def test_addobjects(self):
        scene = Scene()
        objects = [GameObject() for x in xrange(0, 10)]
        for obj in objects:
            scene.addobject(obj)
        self.assertEqual(len(scene.objects), len(objects))

        ids = set()
        for key, obj in scene.objects.iteritems():
            self.assertNotIn(obj.id, ids)
            ids.add(obj.id)
            self.assertEqual(scene, obj.scene)
            self.assertIn(obj, objects)

        with self.assertRaises(ValueError):
            scene.addobject(objects[0])

    def test_removeobject(self):
        scene = Scene()

        objects = [GameObject() for x in xrange(0, 10)]
        for obj in objects:
            scene.addobject(obj)

        with self.assertRaises(ValueError):
            scene.removeobject(GameObject())

        cut = len(objects)//2
        for obj in objects[:cut]:
            scene.removeobject(obj)
        self.assertEqual(len(objects) - cut, len(scene.objects))
        self.assertSetEqual(set(objects[cut:]), set(scene.objects.values()))
