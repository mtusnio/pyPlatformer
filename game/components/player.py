__author__ = 'Maverick'
from engine import Input
from engine.components import SpriteRenderer
from engine.input import BindingDoesNotExist
from engine.math.functions import sign, clamp
from game.components import CharacterController, Character, AICharacter
from game.spriteeffects import BlinkEffect
import logging


class Player(Character):

    MOVEMENT_PER_SECOND = 1700
    JUMP_SPEED = 600

    MAX_HORIZONTAL_SPEED = 500

    HORIZONTAL_PUSH = 600
    VERTICAL_PUSH = -400

    INVULNERABILITY_TIMER = 1.5

    def __init__(self, health=3):
        super(Player, self).__init__(health)

    def update(self):
        player = self.game_object
        camera = player.scene.camera
        camera.transform.position = player.transform.position

        self._handle_input()

    def kill(self):
        super(Player, self).kill()

    def start_collision(self, obj):
        if self.scene.time - self.last_hurt > self.INVULNERABILITY_TIMER:
            dir = self.transform.position - obj.transform.position
            dir.normalize()
            if obj.get_component(AICharacter) is not None:
                controller = self.get_component(CharacterController)
                controller.velocity.x = sign(dir.x) * self.HORIZONTAL_PUSH
                controller.velocity.y = self.VERTICAL_PUSH
                self.get_component(SpriteRenderer).start_effect(BlinkEffect(self.INVULNERABILITY_TIMER))
                self.damage(1)

    def _handle_input(self):
        dt = self.game_object.scene.dt
        controller = self.game_object.get_component(CharacterController)
        try:
            binding_pressed = False
            if abs(controller.velocity.x) < self.MAX_HORIZONTAL_SPEED:
                if Input.is_binding_pressed("left"):
                    binding_pressed = True
                    controller.velocity.x -= self.MOVEMENT_PER_SECOND * dt
                if Input.is_binding_pressed("right"):
                    binding_pressed = True
                    controller.velocity.x += self.MOVEMENT_PER_SECOND * dt
                controller.velocity.x = clamp(controller.velocity.x, -self.MAX_HORIZONTAL_SPEED, self.MAX_HORIZONTAL_SPEED)

            if not binding_pressed:
                sigma = sign(controller.velocity.x)
                controller.velocity.x -= sigma * min(self.MOVEMENT_PER_SECOND * dt, abs(controller.velocity.x))

            if Input.is_binding_pressed("jump"):
                if not controller.flying:
                    controller.velocity.y = -self.JUMP_SPEED
                    controller.flying = True

        except BindingDoesNotExist as e:
            logging.warning("Binding not found: " + str(e))


