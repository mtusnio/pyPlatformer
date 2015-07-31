import collections


class Scene(object):
    def __init__(self):
        self.objects = collections.OrderedDict()

    def simulate_preframe(self, dt):
        """
        Accepts frame length as dt and simulates the frame before rendering has been done.
        :param dt: float
        """
        pass

    def simulate_postframe(self, dt):
        """
        Accepts frame length as dt and simulates the frame after rendering has been done.
        :param dt: float
        :return:
        """
        pass