__author__ = 'Maverick'
from engine import components, Input, input
import logging


class CameraControls(components.BaseComponent):
    def update(self):
        try:
            transform = self.game_object.get_component(components.Transform)
            dt = self.game_object.scene.dt
            if transform is not None:
                if Input.is_binding_pressed("forward"):
                    transform.position[1] -= 800 * dt
                if Input.is_binding_pressed("back"):
                    transform.position[1] += 800 * dt
                if Input.is_binding_pressed("left"):
                    transform.position[0] -= 800 * dt
                if Input.is_binding_pressed("right"):
                    transform.position[0] += 800 * dt

        except input.BindingDoesNotExist as e:
            logging.warning(str(e))
