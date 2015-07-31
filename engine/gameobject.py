class GameObject(object):
    def __init__(self):
        self.components = set()
        self.scene = None

    def update(self):
        """
        Runs object simulation before rendering
        """
        pass

    def update_postframe(self):
        """
        Runs object simulation after rendering
        """
        pass

