import collections


class GameObject(object):
    def __init__(self):
        self.components = collections.OrderedDict()
