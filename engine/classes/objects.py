from pickle import FLOAT

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox

from engine.classes.sprite import Sprite

from engine.vector.angle import AngleVector
from engine.vector.float import Vec2f, Vec4f
from engine.vector.int import Vec2i, Vec4i

from engine.variables import *

import random
import typing
import math


class StaticObject:
    def __init__(
        self, game,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f, Vec4i],
        sprite: VSprite = None,
        group: str = None,

        layer: int = 0,

        id: int = None,

        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None
    ) -> None:
        if variables is not None:
            self.variables = variables

        else:
            self.variables = {}

        if specials is not None:
            self.specials = specials

        else:
            self.specials = {}

        self.game = game

        self.collisions = self.game.objects.collisions.get(group)

        if id is None:
            self.id = random.randint(1, 1000000000)

        else:
            self.id = id

        self.group = group

        self.pos = pos if type(pos) == Vec2f else Vec2f(*pos)
        self.hitbox = hitbox if type(hitbox) == SquareHitbox else SquareHitbox(hitbox)

        self.drawPriority = layer

        self.sprite = sprite if type(sprite) != list else Sprite(self.game, self, *sprite)

        self.spriteDeltaX = 0
        self.spriteDeltaY = 0

        if type(self.sprite) == Sprite:
            self.spriteDeltaX = self.pos.x - self.sprite.pos.x
            self.spriteDeltaY = self.pos.y - self.sprite.pos.y

        self.distance = math.sqrt(self.pos.x ** 2 + self.pos.y ** 2)

    def __str__(self):
        return f"StaticObject(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"StaticObject(id = {self.id} pos = {self.pos})"

    def update(self, collisions: typing.List["VObject"] = None) -> None:
        self.collision(0, 0, True)

    def move(self, x: float = 0, y: float = 0) -> None:
        y = 0 if abs(y) < FLOAT_PRECISION else y
        x = 0 if abs(x) < FLOAT_PRECISION else x

        if x == 0 and y == 0:
            return 0

        self.game.doCollisionsUpdate = max(self.game.doCollisionsUpdate, x != 0 or y != 0)

        collisions = self.game.cash["collisions"][self.id] if self.id in self.game.cash["collisions"] else []

        step = math.ceil(abs(x) + abs(y) + 1)

        hitbox = self.getEditHitbox(x, y)

        lastPos = Vec2f(self.pos.x, self.pos.y)

        useX = True
        useY = True

        for _ in range(step):
            for i, obj in enumerate(collisions):
                if "collision" in obj["functions"]["types"]:
                    if self.collision(x, 0):
                        useX = False

                    if self.collision(0, y):
                        useY = False

            else:
                self.pos.x += (abs(x) / step) * (1 if x >= 0 else -1) * useX
                self.pos.y += (abs(y) / step) * (1 if y >= 0 else -1) * useY

        # self.pos.x = round(self.pos.x)
        # self.pos.y = round(self.pos.y)

        if self.sprite is not None:
            self.sprite.pos.x = math.trunc(self.pos.x + self.spriteDeltaX)
            self.sprite.pos.y = math.trunc(self.pos.y + self.spriteDeltaY)

        self.distance = math.sqrt(self.pos.x ** 2 + self.pos.y ** 2)

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False) -> bool:
        hitbox = self.getEditHitbox(x, y)

        if self.id not in self.game.cash["collisions"]:
            return False

        for obj in self.game.cash["collisions"][self.id]:
            if Collision.rect(self.pos.x + hitbox.x, self.pos.y + hitbox.y, hitbox.width, hitbox.height, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                if allowFunctions:
                    for element in obj["functions"]["functions"]:
                        getattr(self.game.functions, element.replace("function::", "").replace("()", ""))(self.game, self, obj)

                if "collision" in obj["functions"]["types"]:
                    return True

        return False

    def getEditHitbox(self, x: float = 0, y: float = 0) -> SquareHitbox:
        hitbox = self.hitbox.copy()

        if x > 0:
            hitbox.x += 1

        if x < 0:
            hitbox.x -= 1

        if y < 0:
            hitbox.y -= 1

        if y > 0:
            hitbox.y += 1

        return hitbox


class DynamicObject(StaticObject):
    def __init__(
        self, game,
        pos: typing.Union[typing.List[float], Vec2f],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f],
        sprite: VSprite = None,
        group: str = None,

        layer: int = 0,

        speed: int = 5,

        id: int = None,

        gravity: int = 300,
        jumpPower: int = 10,
        slidingStep: int = INF,

        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, sprite, group, layer, id, variables, specials)

        self.vectors = {
            "__fall__": AngleVector(0, 0)
        }

        self.gravity = gravity

        self.jumpPower = jumpPower
        self.slidingStep = slidingStep

        self.speed = speed

    def __str__(self):
        return f"DynamicObject(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"DynamicObject(id = {self.id} pos = {self.pos})"

    def update(self, collisions: list = None) -> None:
        if collisions is None:
            collisions = []

        super().update(collisions)

        # for name, vector in self.vectors.items():
        #     print(name, vector.angle, vector.power)

        # print("---")

        if self.collision(0, -1):
            # self.vectors["__fall__"].power = max([vector.power for name, vector in self.vectors.items()])
            """
            y = 0

            for name, vector in self.vectors.items():
                if name.startswith("jump"):
                    if vector.power * math.cos(math.radians(vector.angle)) < 0:
                        y += vector.power * math.cos(math.radians(vector.angle))

            print(y)

            self.moveByAngle(0, -y - 2, 1, "wall", True)

            self.vectors["__fall__"].power = 1
            """

        if self.collision(0, 1):
            self.vectors["__fall__"].power = 1

        else:
            self.vectors["__fall__"].power += self.gravity / 1000

        pos = Vec2f()

        rem = []

        for name, vector in self.vectors.items():
            x = vector.power * math.sin(math.radians(vector.angle))
            y = vector.power * math.cos(math.radians(vector.angle))

            pos.x += x
            pos.y += y

            vector.power -= vector.decreaseSpeed

            if vector.power <= FLOAT_PRECISION and name != "__fall__":
                rem.append(name)

            # self.move(math.trunc(x + 0.5 * (x >= 0)), math.trunc(y + 0.5 * (y >= 0)))

        for name in rem:
            self.vectors.pop(name)

        self.move(pos.x, pos.y)

    def moveByAngle(self, angle: int, speed: int = None, slidingStep: int = None, name: str = "vector", specifical: bool = False):
        id = random.randint(1, 1000000000) if not specifical else 1

        self.vectors[f"{name} ({id})"] = AngleVector(180 - angle, self.speed if speed is None else speed, self.slidingStep if slidingStep is None else slidingStep)

    def moveByType(self, move: str) -> None:
        if move == "jump":
            # if self.vectors["fall"].power <= 0 and self.vectors["jump"].power <= 0 and self.collision(0, 1):
            self.moveByAngle(0, self.jumpPower, 1, "jump")

            self.vectors["__fall__"].power = 1

        else:
            raise NameError(f"move type {move} is not defined")

    def getVectorsPower(self) -> Vec2i:
        pos = Vec2f(0, 0)

        for name, vector in self.vectors.items():
            if name.startswith("__") and name.endswith("__"):
                continue

            pos.x += vector.power * math.sin(math.radians(vector.angle))
            pos.y += vector.power * math.cos(math.radians(vector.angle))

        if pos.y <= FLOAT_PRECISION:
            pos.x += self.vectors["__fall__"].power * math.sin(math.radians(self.vectors["__fall__"].angle))
            pos.y += self.vectors["__fall__"].power * math.cos(math.radians(self.vectors["__fall__"].angle))

        pos.x = 0 if abs(pos.x) < FLOAT_PRECISION else pos.x
        pos.y = 0 if abs(pos.y) < FLOAT_PRECISION else pos.y

        return pos


class KinematicObject:
    pass
