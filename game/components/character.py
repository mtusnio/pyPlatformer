from engine.components import BaseComponent


class Character(BaseComponent):
    def __init__(self, health=1):
        super(Character, self).__init__()
        self.health = health

    def kill(self):
        pass

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.kill()
