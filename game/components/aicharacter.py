__author__ = 'Maverick'
from engine.components import BaseComponent
from game.components import CharacterController, Character
from engine.math.functions import clamp, sign


class AICharacter(Character):
    MOVEMENT_SPEED = 600

    def __init__(self, health=1, path=None, loop=False, movement_speed=MOVEMENT_SPEED, damages=True):
        super(AICharacter, self).__init__(health)
        if path is None:
            path = []
        self._path_nodes_names = path
        self.path = []
        self.loop = loop
        self.current_path_index = 0
        self.stopped = False
        self.movement_speed = movement_speed
        self.damages = damages

    def start(self):
        for node_name in self._path_nodes_names:
            node = self.scene.get_object_by_name(node_name)
            if node is not None:
                self.path.append(node)

    def update(self):
        if len(self.path) == 0 or self.stopped:
            return

        epsilon = 3

        node = self.path[self.current_path_index]
        diff = node.transform.position - self.transform.position
        # For now we're handling only horizontal movement
        diff.y = 0
        if diff.length() > epsilon:
            character_controller = self.get_component(CharacterController)
            new_velocity = diff.normalize() * self.movement_speed * self.scene.dt + character_controller.velocity
            character_controller.velocity.x = clamp(new_velocity.x, -self.movement_speed, self.movement_speed)
        else:
            self.current_path_index += 1
            if self.current_path_index >= len(self.path):
                if self.loop:
                    self.current_path_index = 0
                else:
                    self.current_path_index = len(self.path) - 1
                    self.stopped = True
