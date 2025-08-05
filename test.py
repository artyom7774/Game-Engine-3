import engine


class Game(engine.Application):
    def __init__(self):
        engine.Application.__init__(self, 1000, 700, 1000, 700, 60, 20, "Test", "", debug=True)

        self.objects.collisions = engine.Collision("player <-> object - collision")

        obj = engine.objects.DynamicObject(self, (0, 0), engine.CircleHitbox([50, 50, 50]))
        obj = engine.objects.DynamicObject(self, (0, 0), engine.CircleHitbox([50, 50, 50]), engine.Sprite(self, obj, "player.png", 0, 0, 100, 100), group="player")

        self.objects.add(obj)

        obj = engine.objects.StaticObject(self, (80, 600), engine.CircleHitbox([0, 0, 100, 50]), engine.Sprite(self, obj, "player.png", 0, 0, 100, 50), group="object")

        self.objects.add(obj)

        self.setCamera(engine.camera.FocusCamera(self, self.objects.getByGroup("player")[0]))


if __name__ == "__main__":
    game = Game()
    game.start()
