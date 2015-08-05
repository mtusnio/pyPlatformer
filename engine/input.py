__author__ = 'Maverick'
from enum import Enum
from collections import defaultdict


class BindingDoesNotExist(Exception):
    """
    Exception thrown when we try to access a binding which has not been specified
    """
    def __init__(self, binding):
        self.binding = binding

    def __str__(self):
        return "Binding not found: {binding}".format(binding=self.binding)


class KeyStatus(Enum):
    DEPRESSED = 1
    DEPRESSED_THIS_FRAME = 2
    PRESSED_THIS_FRAME = 3
    PRESSED = 4


class Input(object):
    bindings = {}
    key_status = defaultdict(lambda: KeyStatus.DEPRESSED)

    @classmethod
    def get_binding_status(cls, binding_name):
        if binding_name not in cls.bindings:
            raise BindingDoesNotExist(binding_name)

        return cls.key_status[cls.bindings[binding_name]]

    @classmethod
    def is_binding_pressed(cls, binding_name):
        if binding_name not in cls.bindings:
            raise BindingDoesNotExist(binding_name)

        return cls.get_binding_status(binding_name) in [KeyStatus.PRESSED_THIS_FRAME, KeyStatus.PRESSED]

    @classmethod
    def is_binding_depressed(cls, binding_name):
        if binding_name not in cls.bindings:
            raise BindingDoesNotExist(binding_name)

        return cls.get_binding_status(binding_name) in [KeyStatus.DEPRESSED_THIS_FRAME, KeyStatus.DEPRESSED]

