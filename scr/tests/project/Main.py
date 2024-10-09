import engine
import random
import pygame


class Functions:
    @staticmethod
    def reset(self):
        self.objects.add(engine.objects.DynamicObject(self, [20 + random.randint(1, 200), 20 + random.randint(1, 200)], [0, 0, 80, 110], self.player_animation, "player", speed=5, gravity=300, jumpPower=10, slidingStep=1))

        self.player = self.objects.getByGroup("player")[0]

        self.focus = self.player.id

        self.camera.setFocus(self.player)
        
    @staticmethod
    def test(game, dynamicObject=None, staticObject=None):
        print("hello world!")


class Game(engine.Application):
    def __init__(self):
        engine.Application.__init__(self, "project/project.property")

        self.sprite = engine.Sprite(self, "project/sprite.png", [32, 32])

        self.particle_sprite = engine.Sprite(self, "project/particle.png")

        self.player_animation = engine.Animation(
            self, "project/project.animation", {
                "move": ["project/player/player_run_1.png", "project/player/player_run_2.png"] * 2,
                "jump": ["project/player/player_jump.png"],
                "fall": ["project/player/player_fall.png"],
                "idle": ["project/player/player_idle.png"]
            }
        )

        self.objects.collisions = engine.Collision("project/project.collision")

        for i in range(100):
            var = random.randint(1, 4)

            if i % var == 0 or i < 15 or True:
                self.objects.add(engine.objects.StaticObject(self, [0 + i * 32, 400], [0, 0, 32, 32], self.sprite, "block"))

        self.objects.add(engine.objects.DynamicObject(self, [20 + random.randint(1, 200), 20 + random.randint(1, 200)], [0, 0, 80, 110], self.player_animation, "player", speed=5, gravity=300, jumpPower=10, slidingStep=1))

        self.player = self.objects.getByGroup("player")[0]

        self.focus = self.player.id

        self.setCamera(engine.camera.FocusCamera(self, self.player))
        self.setFunctionClass(Functions)

        self.setKeyEvent(["PRESS", "d"], lambda: self.player.typeMove("right"))
        self.setKeyEvent(["PRESS", "a"], lambda: self.player.typeMove("left"))
        self.setKeyEvent(["KEYDOWN", "SPACE"], lambda: self.player.typeMove("jump"))
        self.setKeyEvent(["KEYDOWN", "r"], lambda: Functions.reset(self))

        self.sprites = [
            engine.Sprite(self, "project/button/base.png"),
            engine.Sprite(self, "project/button/mouse.png"),
            engine.Sprite(self, "project/button/click.png")
        ]

        self.button = engine.Button(
            self, [300, 20, 200, 100], *self.sprites, None, engine.Label(self, [300, 20, 200, 100], "Hello world!"),
            function=lambda: Functions.reset(self)
        )

    def update(self) -> None:
        super().update()

        for _ in range(5):
            particle_function = engine.ParticleFunction(self, {
                "x": lambda variables, pos, step: pos.x + (step / 10) * variables["speed"],
                "y": lambda variables, pos, step: pos.y + (step / 1000) * variables["var"],

                "resize": lambda variables, pos, step: (step > 50, 10 - ((step - 40) / 5), 10 - ((step - 40) / 5)),
                "death": lambda variables, pos, step: step > 75
            }, variables={"var": random.randint(-10, 10), "speed": random.randint(10, 12) / 10})

            particle = engine.ImageParticle(self, [random.randint(0, 50), 100], self.particle_sprite, particle_function, "p1")

            self.particles.add(particle)

    def render(self) -> None:
        super().render()

        self.button.draw()


if __name__ == "__main__":
    game = Game()
    game.start()
