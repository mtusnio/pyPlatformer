from engine.components import BaseComponent


class Character(BaseComponent):
    def __init__(self, health=1):
        super(Character, self).__init__()
        self.health = health
        self.last_hurt = 0.0

    def kill(self):
        self.game_object.destroy()

    def damage(self, amount):
        self.health -= amount
        self.last_hurt = self.scene.time
        if self.health <= 0:
            self.health = 0
            self.kill()
