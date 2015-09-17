from engine.components import SpriteRenderer


class BlinkEffect(SpriteRenderer.Effect):
    def __init__(self, length, frequency=0.25):
        super(BlinkEffect, self).__init__()
        self.length = length
        self.end = 0
        self.time_since_last_blink = 0
        self.frequency = frequency
        self.scene = None

    def on_start(self):
        self.scene = self.sprite_renderer.scene
        self.end = self.scene.time + self.length

    def run(self):
        if self.scene.time >= self.end:
            self.sprite_renderer.should_render = True
            self.finished = True
            return

        self.time_since_last_blink += self.scene.dt

        if self.time_since_last_blink >= self.frequency:
            self.sprite_renderer.should_render = not self.sprite_renderer.should_render
            self.time_since_last_blink = 0

