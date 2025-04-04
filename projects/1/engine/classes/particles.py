from engine.classes.sprite import Sprite

from engine.vector.float import Vec2f

from engine.variables import *
from math import *

import random
import typing


class ParticleFunction:
    """
    x:      lambda variables, pos, step: x + px (x + add to x (int))
    y:      lambda variables, pos, step: y + py (y + add to y (int))

    death:  lambda variables, pos, step: flag (do kill (True or False))
    resize: lambda variables, pos, step: flag, width, height (do resize (True or False), new image width (int), new image height (int))
    """

    def __init__(self, game, functions: typing.Dict[str, typing.Callable] = None, variables: typing.Dict[str, typing.Any] = None) -> None:
        if functions is None:
            self.functions = {}

        else:
            self.functions = functions

        if variables is None:
            self.variables = {}

        else:
            self.variables = variables

        self.game = game

        if "x" not in self.functions:
            self.functions["x"] = lambda variables, pos, step: pos.x

        if "y" not in self.functions:
            self.functions["y"] = lambda variables, pos, step: pos.y

        if "death" not in self.functions:
            self.functions["death"] = lambda variables, pos, step: False

        if "resize" not in self.functions:
            self.functions["resize"] = lambda variables, pos, step: (False, 0, 0)

    def update(self, particle: VParticle) -> None:
        particle.pos.x = self.functions["x"](self.variables, particle.pos, particle.step)
        particle.pos.y = self.functions["y"](self.variables, particle.pos, particle.step)

        if self.functions["death"](self.variables, particle.pos, particle.step):
            self.game.particles.pop(particle)

        var = self.functions["resize"](self.variables, particle.pos, particle.step)

        if var[0]:
            particle.sprite.resize(var[1], var[2])


class ImageParticle:
    def __init__(
            self, game, pos: typing.Union[Vec2f, typing.List[float]],
            sprite: VSprite, function: ParticleFunction, group: str = None
    ) -> None:
        self.game = game

        self.id = random.randint(1, 1000000000)

        self.pos = pos if type(pos) == Vec2f else Vec2f(*pos)

        self.function = function
        self.sprite = sprite

        self.group = group

        self.step = 1

    def copy(self) -> "ImageParticle":
        return ImageParticle(self.game, Vec2f(*self.pos), self.sprite.copy(), self.function, self.group)

    def update(self) -> None:
        self.function.update(self)

        self.step += 1

    def draw(self, px: float = 0, py: float = 0) -> None:
        self.game.screen.blit(self.sprite.get(), (self.pos.x + px, self.pos.y + py))
