import basecomponent

class Camera(basecomponent.BaseComponent):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.fov = kwargs.get("fov", 80)
