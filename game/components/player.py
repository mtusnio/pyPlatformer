__author__ = 'Maverick'
from engine import Input
from engine.components import BaseComponent
from engine.input import BindingDoesNotExist
from engine.math.functions import sign, clamp
from game.components import CharacterController
import logging


class Player(BaseComponent):

    MOVEMENT_PER_SECOND = 1700
    JUMP_SPEED = 700

    MAX_VERTICAL_SPEED = 1200
    MAX_HORIZONTAL_SPEED = 500

    def update(self):
        player = self.game_object
        camera = player.scene.camera
        camera.transform.position = player.transform.position

        self._handle_input()

    def _handle_input(self):
        dt = self.game_object.scene.dt
        controller = self.game_object.get_component(CharacterController)
        try:
            binding_pressed = False
            if Input.is_binding_pressed("left"):
                binding_pressed = True
                controller.velocity.x -= self.MOVEMENT_PER_SECOND * dt
            if Input.is_binding_pressed("right"):
                binding_pressed = True
                controller.velocity.x += self.MOVEMENT_PER_SECOND * dt

            if not binding_pressed:
                sigma = sign(controller.velocity.x)
                controller.velocity.x -= sigma * min(self.MOVEMENT_PER_SECOND * dt, abs(controller.velocity.x))

            if Input.is_binding_pressed("jump"):
                if not controller.flying:
                    controller.velocity.y = -self.JUMP_SPEED
                    controller.flying = True

        except BindingDoesNotExist as e:
            logging.warning("Binding not found: " + str(e))

        # Velocity clamping
        controller.velocity.x = clamp(controller.velocity.x, -self.MAX_HORIZONTAL_SPEED, self.MAX_HORIZONTAL_SPEED)
        controller.velocity.y = clamp(controller.velocity.y, -self.MAX_VERTICAL_SPEED, self.MAX_VERTICAL_SPEED)

