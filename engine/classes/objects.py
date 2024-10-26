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

        if self.collision(0, 0):
            return 0

        self.game.doCollisionsUpdate = max(self.game.doCollisionsUpdate, x != 0 or y != 0)

        collisions = self.game.cash["collisions"][self.id] if self.id in self.game.cash["collisions"] else []

        step = max(abs(x), abs(y)) + 1

        hitbox = self.getEditHitbox(x, y)

        lastPos = Vec2i(self.pos.x, self.pos.y)

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

        self.pos.x = round(self.pos.x)
        self.pos.y = round(self.pos.y)

        # TODO: починить коллизию при 135 градусов

        if self.sprite is not None:
            self.sprite.pos.x += self.pos.x - lastPos.x
            self.sprite.pos.y += self.pos.y - lastPos.y

        self.distance = math.sqrt(self.pos.x ** 2 + self.pos.y ** 2)

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False) -> bool:
        # TODO кешировать функцию по fpsc (номер кадра), x, y, allowFunctions

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
            "fall": AngleVector(0, 0),
            "jump": AngleVector(180, 0),
            "move": AngleVector(90, 0)
        }

        self.gravity = gravity

        self.jumpPower = jumpPower
        self.slidingStep = slidingStep

        self.speed = speed

    def __str__(self):
        return f"DynamicObject(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"DynamicObject(id = {self.id} pos = {self.pos})"

    def update(self, collisions=None) -> None:
        if collisions is None:
            collisions = []

        super().update(collisions)

        if not self.collision(0, 1) and self.vectors["jump"].power <= 0:
            self.vectors["fall"].power += self.gravity / 1000

        else:
            self.vectors["fall"].power = self.vectors["jump"].power

        if abs(self.vectors["move"].power) > 0:
            x = self.vectors["move"].power * math.sin(math.radians(self.vectors["move"].angle))
            y = self.vectors["move"].power * math.cos(math.radians(self.vectors["move"].angle))

            self.move(math.trunc(x), math.trunc(y))

            self.vectors["move"].power = max(0, self.vectors["move"].power - self.slidingStep)

        if self.vectors["jump"].power > 0:
            x = self.vectors["jump"].power * math.sin(math.radians(self.vectors["jump"].angle))
            y = self.vectors["jump"].power * math.cos(math.radians(self.vectors["jump"].angle))

            if self.collision(0, -1):
                self.vectors["jump"].power = 0
                self.vectors["fall"].power = FLOAT_PRECISION

            else:
                self.vectors["jump"].power -= self.gravity / 1000

        elif self.vectors["fall"].power > 0:
            x = self.vectors["fall"].power * math.sin(math.radians(self.vectors["fall"].angle))
            y = self.vectors["fall"].power * math.cos(math.radians(self.vectors["fall"].angle))

        else:
            return 0

        self.move(math.trunc(x), math.trunc(y))

    def moveByAngle(self, angle: int, speed: int = None):
        self.vectors["move"].angle = 180 - angle
        self.vectors["move"].power = self.speed if speed is None else speed

    def moveByType(self, move: str, speed: int = None) -> None:
        if move == "down":
            self.vectors["move"].angle = 0
            self.vectors["move"].power = self.speed if speed is None else speed

        elif move == "right":
            self.vectors["move"].angle = 90
            self.vectors["move"].power = self.speed if speed is None else speed

        elif move == "up":
            self.vectors["move"].angle = 180
            self.vectors["move"].power = self.speed if speed is None else speed

        elif move == "left":
            self.vectors["move"].angle = 270
            self.vectors["move"].power = self.speed if speed is None else speed

        elif move == "jump":
            if self.vectors["fall"].power <= 0 and self.vectors["jump"].power <= 0 and self.collision(0, 1):
                self.vectors["jump"].power = self.jumpPower

        else:
            raise NameError(f"move type {move} is not defined")

    def getVectorsPower(self) -> Vec2i:
        pos = Vec2i(0, 0)

        pos.x += self.vectors["move"].power * math.sin(math.radians(self.vectors["move"].angle))
        pos.y += self.vectors["move"].power * math.cos(math.radians(self.vectors["move"].angle))

        pos.x += self.vectors["jump"].power * math.sin(math.radians(self.vectors["jump"].angle))
        pos.y += self.vectors["jump"].power * math.cos(math.radians(self.vectors["jump"].angle))

        if self.vectors["jump"].power <= FLOAT_PRECISION:
            pos.x += self.vectors["fall"].power * math.sin(math.radians(self.vectors["fall"].angle))
            pos.y += self.vectors["fall"].power * math.cos(math.radians(self.vectors["fall"].angle))

        pos.x = 0 if abs(pos.x) < FLOAT_PRECISION else pos.x
        pos.y = 0 if abs(pos.y) < FLOAT_PRECISION else pos.y

        return pos


class KinematicObject:
    pass
