__author__ = 'Maverick'
import unittest
from engine.input import BindingDoesNotExist, Input, KeyStatus



class TestBindings(unittest.TestCase):
    def setUp(self):
        self._forward_key = 10
        self._back_key = 32
        Input.bindings["forward"] = self._forward_key
        Input.bindings["back"] = self._back_key

    def test_no_binding_returns_exception(self):
        with self.assertRaises(BindingDoesNotExist):
            Input.bindings["deadbinding"]

    def test_key_changes_binding_status(self):
        Input.key_status.clear()
        self.assertEqual(Input.get_binding_status("forward"), KeyStatus.DEPRESSED)
        self.assertEqual(Input.get_binding_status("back"), KeyStatus.DEPRESSED)
        Input.key_status[self._forward_key] = KeyStatus.PRESSED_THIS_FRAME
        self.assertEqual(Input.get_binding_status("forward"), KeyStatus.PRESSED_THIS_FRAME)
        self.assertEqual(Input.get_binding_status("back"), KeyStatus.DEPRESSED)

    def test_binding_recognises_pressed(self):
        Input.key_status.clear()
        Input.key_status[self._forward_key] = KeyStatus.PRESSED_THIS_FRAME
        self.assertTrue(Input.is_binding_pressed("forward"))
        Input.key_status[self._back_key] = KeyStatus.PRESSED
        self.assertTrue(Input.is_binding_pressed("forward"))
        self.assertTrue(Input.is_binding_pressed("back"))

    def test_all_bindings_are_depressed_by_default(self):
        Input.key_status.clear()
        self.assertTrue(Input.get_binding_status("forward") == KeyStatus.DEPRESSED)
        self.assertTrue(Input.get_binding_status("back") == KeyStatus.DEPRESSED)

    def test_binding_recognises_depressed(self):
        Input.key_status.clear()
        Input.key_status[self._forward_key] = KeyStatus.DEPRESSED_THIS_FRAME
        self.assertTrue(Input.is_binding_depressed("forward"))
        self.assertTrue(Input.is_binding_depressed("back"))
