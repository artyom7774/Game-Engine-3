from libc.math cimport sqrt, sin, cos

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox

from engine.classes.sprite import Sprite

from engine.vector.angle import AngleVector

from engine.vector.float import Vec2f, Vec4f
from engine.vector.int import Vec2i, Vec4i

from engine.variables import *

import typing
import random
import typing
import math

cdef class StaticObject:
    cdef public object game
    cdef public object procesionPos
    cdef public object pos
    cdef public object hitbox
    cdef public int layer
    cdef public object sprite
    cdef public float distance
    cdef public int mass
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
        mass: int = 1000,
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
        self.mass = mass
        self.layer = layer
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

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False, append: bool = False, filter: typing.Callable = None) -> bool:
        hitbox = self.getEditHitbox(x, y, append)

        if self.id not in self.game.cash["collisions"]:
            return False

        flag = False

        for obj in self.game.cash["collisions"][self.id]:
            if Collision.rect(self.pos.x + hitbox.x, self.pos.y + hitbox.y, hitbox.width, hitbox.height, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height) and (filter is None or filter(obj["object"])):
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

    def getParameter(self, name: str) -> None:
        if name == "hitbox":
            return self.hitbox.get()

        return getattr(self, name)

    def setParameter(self, name: str, value: typing.Any) -> None:
        if name == "hitbox":
            self.hitbox = SquareHitbox(value)

        setattr(self, name, value)


cdef class DynamicObject(StaticObject):
    cdef public dict vectors
    cdef public float gravity
    cdef public float jumpPower
    cdef public float slidingStep
    cdef public float speed

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f],
        sprite: VSprite = None,
        group: str = None,
        mass: int = 1000,
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
        StaticObject.__init__(self, game, pos, hitbox, sprite, group, mass, layer, id, invisible, animator, variables, specials)

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

        if self.collision(0, -1):
            pass

        if self.collision(0, 1):
            if self.vectors["__fall__"].power > 0:
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

    def getObjectStructure(self, x, y, append, phitbox: typing.List[int], now: VObject, visited: typing.Optional[set] = None) -> typing.List[VObject]:
        if visited is None:
            visited = set()

        if now.id in visited:
            return []

        visited.add(now.id)

        hitbox = now.getEditHitbox(x, y, append)

        objects = []

        for obj in self.game.cash["collisions"][now.id]:
            if obj is None or obj["functions"] is None:
                continue

            if (isinstance(obj["object"], DynamicObject) and "collision" in obj["functions"]["types"]):
                if Collision.rect(now.pos.x + hitbox.x + phitbox[0], now.pos.y + hitbox.y + phitbox[1], hitbox.width + phitbox[2], hitbox.height + phitbox[3], obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                    objects.append(obj["object"])

                    objects.extend(
                        self.getObjectStructure(
                            x, y, append, phitbox,
                            obj["object"], visited
                        )
                    )

        return objects

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False, append: bool = False, filter: typing.Callable = None) -> bool:
        hitbox = self.getEditHitbox(x, y, append)

        if self.id not in self.game.cash["collisions"]:
            return False

        flag = False

        for obj in self.game.cash["collisions"][self.id]:
            if Collision.rect(self.pos.x + hitbox.x, self.pos.y + hitbox.y, hitbox.width, hitbox.height, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height) and (filter is None or filter(obj["object"])):
                if allowFunctions:
                    if obj["functions"] is not None:
                        for element in obj["functions"]["functions"]:
                            getattr(self.game.functions, element.replace("function::", "").replace("()", ""))(self.game, self, obj)

                if obj["functions"] is not None and "collision" in obj["functions"]["types"]:
                    if isinstance(obj["object"], DynamicObject) and isinstance(self, DynamicObject) and self.group == "player":
                        right = self.getObjectStructure(x, y, append, [1, 1, 0, -2], self)
                        left = self.getObjectStructure(x, y, append, [-1, 1, 0, -2], self)
                        up = self.getObjectStructure(x, y, append, [1, -1, -2, 0], self)

                        if x > 0 and len(right) >= 1:
                            right.append(self)

                            speedX = sum([obj.mass * obj.getVectorsPower().x for obj in right]) / sum([obj.mass for obj in right])

                            for obj in right:
                                obj.moveByAngle(90, speedX - obj.getVectorsPower().x, float(INF))

                        if x < 0 and len(left) >= 1:
                            left.append(self)

                            speedX = sum([obj.mass * obj.getVectorsPower().x for obj in left]) / sum([obj.mass for obj in left])

                            for obj in left:
                                obj.moveByAngle(90, speedX - obj.getVectorsPower().x, float(INF))

                        if abs(self.getVectorsPower().y) > FLOAT_PRECISION and len(up) >= 1:
                            up.append(self)

                            speedY = sum([obj.mass * obj.getVectorsPower().y for obj in up]) / sum([obj.mass for obj in up])

                            for obj in up:
                                if obj.id == self.id:
                                    continue

                                obj.vectors["__fall__"].power = speedY - obj.getVectorsPower().y

                        """
                        speedX = (self.mass * self.getVectorsPower().x + obj["object"].mass * obj["object"].getVectorsPower().x) / (self.mass + obj["object"].mass)
                        speedY = (self.mass * self.getVectorsPower().y + obj["object"].mass * obj["object"].getVectorsPower().y) / (self.mass + obj["object"].mass)

                        if Collision.rect(self.pos.x + hitbox.x + 1, self.pos.y + hitbox.y + 1, hitbox.width, hitbox.height - 2, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                            self.moveByAngle(90, speedX - self.getVectorsPower().x)
                            obj["object"].moveByAngle(90, speedX - obj["object"].getVectorsPower().x)

                        if Collision.rect(self.pos.x + hitbox.x - 1, self.pos.y + hitbox.y + 1, hitbox.width, hitbox.height - 2, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                            self.moveByAngle(90, speedX - self.getVectorsPower().x)
                            obj["object"].moveByAngle(90, speedX - obj["object"].getVectorsPower().x)

                        if y > 0:
                            pass

                        if abs(self.getVectorsPower().y) > FLOAT_PRECISION and Collision.rect(self.pos.x + hitbox.x + 1, self.pos.y + hitbox.y - 1, hitbox.width - 2, hitbox.height, obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height):
                            obj["object"].vectors["__fall__"].power = speedY - obj["object"].getVectorsPower().y
                        """

                    if allowFunctions:
                        flag = True

                    else:
                        return True

        return flag

    def moveByAngle(self, angle: float, speed: float = None, slidingStep: float = None, name: str = "vector", specifical: int = None):
        id = random.randint(1, 1000000000) if specifical is None else int(specifical)

        self.vectors[f"{name} ({id})"] = AngleVector(180 - angle, self.speed if speed is None else speed, self.slidingStep if slidingStep is None else slidingStep)

    def moveByType(self, move: str, power: float = None) -> None:
        if move == "jump":
            self.vectors["__fall__"].power = -self.jumpPower if power is None else power

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
