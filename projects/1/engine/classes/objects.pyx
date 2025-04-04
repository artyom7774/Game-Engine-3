from libc.math cimport sqrt, sin, cos

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

cdef class StaticObject:
    cdef public object game
    cdef public object procesionPos
    cdef public object pos
    cdef public object hitbox
    cdef public int drawPriority
    cdef public object sprite
    cdef public float distance
    cdef public int id
    cdef public str group
    cdef public dict variables
    cdef public dict specials
    cdef public object collisions
    cdef public bint invisible
    cdef public object animator

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f, Vec4i],
        sprite: VSprite = None,
        group: str = None,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        animator: typing.Any = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
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
        self.procesionPos = Vec2f(0, 0)
        self.pos = pos if type(pos) == Vec2f else Vec2f(*pos)
        self.hitbox = hitbox if type(hitbox) == SquareHitbox else SquareHitbox(hitbox)
        self.drawPriority = layer
        self.invisible = invisible
        self.sprite = sprite if type(sprite) != list else Sprite(self.game, self, *sprite)
        self.distance = sqrt(self.pos.x ** 2 + self.pos.y ** 2)
        self.animator = animator

    def __str__(self):
        return f"StaticObject(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"StaticObject(id = {self.id} pos = {self.pos})"

    def update(self, collisions: typing.List["VObject"] = None) -> None:
        if self.animator is not None:
            self.animator.update()

        self.collision(0, 0, True)

    def move(self, x: float = 0, y: float = 0):
        y = 0 if abs(y) < FLOAT_PRECISION else y
        x = 0 if abs(x) < FLOAT_PRECISION else x

        self.procesionPos.x += x
        self.procesionPos.y += y

        x = int(self.procesionPos.x)
        y = int(self.procesionPos.y)

        self.procesionPos.x -= x
        self.procesionPos.y -= y

        if x == 0 and y == 0:
            return 0

        self.game.doCollisionsUpdate = max(self.game.doCollisionsUpdate, x != 0 or y != 0)

        collisions = self.game.cash["collisions"][self.id] if self.id in self.game.cash["collisions"] else []

        step = math.ceil(abs(x) + abs(y))

        hitbox = self.getEditHitbox(x, y)

        useX = True
        useY = True

        for _ in range(step):
            for i, obj in enumerate(collisions):
                if obj["functions"] is not None and "collision" in obj["functions"]["types"]:
                    if self.collision(x, 0):
                        useX = False

                    if self.collision(0, y):
                        useY = False

            else:
                self.pos.x += (abs(x) / step) * (1 if x >= 0 else -1) * useX
                self.pos.y += (abs(y) / step) * (1 if y >= 0 else -1) * useY

        self.pos.x = round(self.pos.x)
        self.pos.y = round(self.pos.y)

        self.distance = sqrt(self.pos.x ** 2 + self.pos.y ** 2)

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False, append: bool = False) -> bool:
        hitbox = self.getEditHitbox(x, y, append)

        if self.id not in self.game.cash["collisions"]:
            return False

        flag = False

        for obj in self.game.cash["collisions"][self.id]:
            if Collision.rect(self.pos.x + hitbox.x, self.pos.y + hitbox.y, hitbox.width, hitbox.height, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                if allowFunctions:
                    if obj["functions"] is not None:
                        for element in obj["functions"]["functions"]:
                            getattr(self.game.functions, element.replace("function::", "").replace("()", ""))(self.game, self, obj)

                if obj["functions"] is not None and "collision" in obj["functions"]["types"]:
                    if allowFunctions:
                        flag = True
                    else:
                        return True

        return flag

    def collisionGetID(self, x: float = 0, y: float = 0, append: bool = False, group: str = None) -> typing.Any:
        hitbox = self.getEditHitbox(x, y, append)

        if self.id not in self.game.cash["collisions"]:
            return [False, -1]

        for obj in self.game.cash["collisions"][self.id]:
            if obj["object"].group == group or group is None:
                if Collision.rect(self.pos.x + hitbox.x, self.pos.y + hitbox.y, hitbox.width, hitbox.height, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                    return [True, obj["object"]]

        return [False, -1]

    def getEditHitbox(self, x: float = 0, y: float = 0, append: bool = False) -> SquareHitbox:
        hitbox = self.hitbox.copy()

        if append:
            hitbox.x -= 1
            hitbox.width += 2
            hitbox.y -= 1
            hitbox.height += 2

        if x > 0:
            hitbox.x += 1

        elif x < 0:
            hitbox.x -= 1

        if y < 0:
            hitbox.y -= 1

        elif y > 0:
            hitbox.y += 1

        return hitbox


cdef class DynamicObject(StaticObject):
    cdef public dict vectors
    cdef public float gravity
    cdef public float jumpPower
    cdef public float slidingStep
    cdef public float speed
    cdef public bint wasJump

    def __cinit__(self, *args, **kwargs):
        self.wasJump = 0

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f],
        sprite: VSprite = None,
        group: str = None,
        layer: int = 0,
        speed: float = 5,
        id: int = None,
        invisible: bool = False,
        animator: typing.Any = None,
        gravity: float = 300,
        jumpPower: float = 10,
        slidingStep: float = INF,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, sprite, group, layer, id, invisible, animator, variables, specials)

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

    def update(self, collisions: list = None):
        if collisions is None:
            collisions = []

        super().update(collisions)

        self.wasJump -= 1

        if self.collision(0, -1):
            pass

        if self.collision(0, 1):
            if self.wasJump <= 0:
                self.vectors["__fall__"].power = 0

        else:
            self.vectors["__fall__"].power += self.gravity / 1000

        pos = Vec2f()
        rem = []

        for name, vector in self.vectors.items():
            x = vector.power * sin(math.radians(vector.angle))
            y = vector.power * cos(math.radians(vector.angle))

            pos.x += x
            pos.y += y

            vector.power -= vector.decreaseSpeed

            # x = max(0, abs(x) - self.slidingStep) * (1 if x >= 0 else -1)
            # y = max(0, abs(y) - self.gravity / 1000) * (1 if y >= 0 else -1)

            # vector.power = sqrt(x ** 2 + y ** 2)
            # vector.angle = math.atan2(y, x)

            if vector.power <= FLOAT_PRECISION and name != "__fall__":
                rem.append(name)

        for name in rem:
            self.vectors.pop(name)

        self.move(pos.x, pos.y)

    def moveByAngle(self, angle: float, speed: float = None, slidingStep: float = None, name: str = "vector", specifical: bool = False):
        id = random.randint(1, 1000000000) if not specifical else 1

        self.vectors[f"{name} ({id})"] = AngleVector(180 - angle, self.speed if speed is None else speed, self.slidingStep if slidingStep is None else slidingStep)

    def moveByType(self, move: str) -> None:
        if move == "jump":
            self.vectors["__fall__"].power = -self.jumpPower

            self.wasJump = 5

        else:
            raise NameError(f"move type {move} is not defined")

    def getVectorsPower(self) -> Vec2i:
        pos = Vec2f(0, 0)

        for name, vector in self.vectors.items():
            if name.startswith("__") and name.endswith("__"):
                continue

            pos.x += vector.power * sin(math.radians(vector.angle))
            pos.y += vector.power * cos(math.radians(vector.angle))

        if pos.y <= FLOAT_PRECISION:
            pos.x += self.vectors["__fall__"].power * sin(math.radians(self.vectors["__fall__"].angle))
            pos.y += self.vectors["__fall__"].power * cos(math.radians(self.vectors["__fall__"].angle))

        pos.x = 0 if abs(pos.x) < FLOAT_PRECISION else pos.x
        pos.y = 0 if abs(pos.y) < FLOAT_PRECISION else pos.y

        return pos
