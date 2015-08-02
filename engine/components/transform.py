import basecomponent
from engine import math


class Transform(basecomponent.BaseComponent):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.position = kwargs.get("position", math.Vector2())
        self.rotation = kwargs.get("rotation", 0)
        self.scale = kwargs.get("scale", 1)