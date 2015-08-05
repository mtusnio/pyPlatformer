__author__ = 'Maverick'
import unittest
from engine.input import BindingDoesNotExist, Input, KeyStatus



class TestBindings(unittest.TestCase):
    def setUp(self):
        self._forward_key = 10
        self._back_key = 32
        Input.bindings["forward"] = self._forward_key
        Input.bindings["back"] = self._back_key

    def test_nobinding(self):
        functions = [Input.get_binding_status, Input.is_binding_pressed, Input.is_binding_depressed]

        for func in functions:
            with self.assertRaises(BindingDoesNotExist):
                func("deadbinding")

    def test_binding_status(self):
        Input.key_status.clear()
        self.assertEqual(Input.get_binding_status("forward"), KeyStatus.DEPRESSED)
        self.assertEqual(Input.get_binding_status("back"), KeyStatus.DEPRESSED)
        Input.key_status[self._forward_key] = KeyStatus.PRESSED_THIS_FRAME
        self.assertEqual(Input.get_binding_status("forward"), KeyStatus.PRESSED_THIS_FRAME)
        self.assertEqual(Input.get_binding_status("back"), KeyStatus.DEPRESSED)

    def test_binding_pressed(self):
        Input.key_status.clear()
        self.assertFalse(Input.is_binding_pressed("forward"))
        self.assertFalse(Input.is_binding_pressed("back"))
        Input.key_status[self._forward_key] = KeyStatus.PRESSED_THIS_FRAME
        self.assertTrue(Input.is_binding_pressed("forward"))
        self.assertFalse(Input.is_binding_pressed("back"))
        Input.key_status[self._back_key] = KeyStatus.PRESSED
        self.assertTrue(Input.is_binding_pressed("forward"))
        self.assertTrue(Input.is_binding_pressed("back"))

    def test_binding_depressed(self):
        Input.key_status.clear()
        self.assertTrue(Input.is_binding_depressed("forward"))
        self.assertTrue(Input.is_binding_depressed("back"))
        Input.key_status[self._forward_key] = KeyStatus.DEPRESSED_THIS_FRAME
        Input.key_status[self._back_key] = KeyStatus.PRESSED
        self.assertTrue(Input.is_binding_depressed("forward"))
        self.assertFalse(Input.is_binding_depressed("back"))
        Input.key_status[self._forward_key] = KeyStatus.PRESSED_THIS_FRAME
        self.assertFalse(Input.is_binding_depressed("forward"))
        self.assertFalse(Input.is_binding_depressed("back"))
