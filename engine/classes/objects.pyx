from libc.math cimport sqrt, sin, cos

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox, CircleHitbox

from engine.classes.sprite import Sprite

from engine.vector.angle import AngleVector

from engine.vector.float import Vec2f, Vec4f
from engine.vector.int import Vec2i, Vec4i

from engine.functions.alpha import alphaRect
from engine.ui.text import print_text, get_font, get_ttf

from engine.variables import *

import pygame
import typing
import random
import typing
import math


def hex_to_rgb(color: str) -> typing.List[int]:
    color = color.lstrip('#')
    return list(int(color[i:i+2], 16) for i in (0, 2, 4))


def buildHitbox(hitbox: typing.Any) -> typing.Any:
    if isinstance(hitbox, (list, tuple)):
        if len(hitbox) == 4:
            return SquareHitbox(hitbox)

        if len(hitbox) == 3:
            return CircleHitbox(hitbox)

    if isinstance(hitbox, dict):
        if hitbox["type"] == "SquareHitbox":
            return SquareHitbox([parameter["value"] for parameter in hitbox["hitbox"]["SquareHitbox"].values()])

        if hitbox["type"] == "CircleHitbox":
            return CircleHitbox([parameter["value"] for parameter in hitbox["hitbox"]["CircleHitbox"].values()])

    raise TypeError()


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
    cdef public int alpha
    cdef public object animator
    cdef public bint doCollisionUpdate

    cdef public int lastFrameUpdateNumber

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, CircleHitbox, typing.List[float], Vec4f, Vec4i],
        sprite: VSprite = None,
        group: str = "",
        mass: int = 1000,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
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

        self.doCollisionUpdate = True

        self.game = game
        self.collisions = self.game.objects.collisions.get(group)

        self.id = random.randint(1, 1000000000) if id is None else id

        self.group = group
        self.procesionPos = Vec2f(0, 0)
        self.pos = pos if type(pos) == Vec2f else Vec2f(*pos)
        self.hitbox = hitbox if type(hitbox) in (SquareHitbox, CircleHitbox) else buildHitbox(hitbox)
        self.mass = mass
        self.layer = layer
        self.invisible = invisible
        self.alpha = alpha
        self.sprite = sprite if type(sprite) != list else Sprite(self.game, self, *sprite)
        self.distance = sqrt(self.pos.x ** 2 + self.pos.y ** 2)
        self.animator = animator

        self.lastFrameUpdateNumber = -1

    def __str__(self):
        return f"StaticObject(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"StaticObject(id = {self.id} pos = {self.pos})"

    def destroy(self):
        self.game.objects.removeById(self.id)

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
            return

        self.game.doCollisionsUpdate = max(self.game.doCollisionsUpdate, x != 0 or y != 0)

        collisions = self.game.cache["collisions"][self.id] if self.id in self.game.cache["collisions"] else []

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

            self.pos.x += (abs(x) / step) * (1 if x >= 0 else -1) * useX
            self.pos.y += (abs(y) / step) * (1 if y >= 0 else -1) * useY

        self.pos.x = round(self.pos.x)
        self.pos.y = round(self.pos.y)

        self.distance = sqrt(self.pos.x ** 2 + self.pos.y ** 2)

        self.game.objects.tree.update(self)

    def draw(self, px: float, py: float):
        if self.lastFrameUpdateNumber == self.game.fpsc:
            return

        self.lastFrameUpdateNumber = self.game.fpsc

        if self.sprite is not None:
            if self.game.usingWidth + self.sprite.pos.x + self.sprite.width + 100 > self.pos.x + px > - 100 - self.sprite.pos.x - self.sprite.width and 100 + self.game.usingHeight + self.sprite.pos.y + self.sprite.height > self.pos.y + py > - 100 - self.sprite.pos.y - self.sprite.height:
                sprite = self.sprite.get()

                if not self.invisible or self.game.forcedViewObject:
                    if sprite is not None:
                        # sprite = sprite.copy()
                        sprite.set_alpha(min(255, max(0, self.alpha)))

                        self.game.screen.blit(sprite, (self.pos.x + self.sprite.pos.x - self.sprite.cx + px, self.pos.y + self.sprite.pos.y - self.sprite.cy + py))

        if self.game.debug or (self.group.startswith("__") and self.group.endswith("__") and not self.group == "__debug_unvisiable__"):
            self.hitbox.draw(self.game.screen, self.pos.x, self.pos.y, px, py)

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False, append: bool = False, filter: typing.Callable = None) -> bool:
        hitbox = self.getEditHitbox(x, y, append)

        if self.id not in self.game.cache["collisions"]:
            return False

        flag = False

        for obj in self.game.cache["collisions"][self.id]:
            if Collision.any(hitbox.position(self.pos.x, self.pos.y), obj["object"].hitbox.position(obj["object"].pos.x, obj["object"].pos.y)) and (filter is None or filter(obj["object"])):
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

        if self.id not in self.game.cache["collisions"]:
            return [False, -1]

        for obj in self.game.cache["collisions"][self.id]:
            if obj["object"].group == group or group is None:
                if Collision.any(hitbox.position(self.pos.x, self.pos.y), obj["object"].hitbox.position(obj["object"].pos.x, obj["object"].pos.y)):
                    return [True, obj["object"]]

        return [False, -1]

    def getEditHitbox(self, x: float = 0, y: float = 0, append: bool = False) -> SquareHitbox:
        if append:
            hitbox = self.hitbox.position(0, 0, 1)

        else:
            hitbox = self.hitbox.copy()

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

        if name == "spriteHitbox":
            return self.sprite.pos.get() + [self.sprite.width, self.sprite.height]

        return getattr(self, name)

    def setParameter(self, name: str, value: typing.Any) -> None:
        if name == "hitbox":
            self.hitbox = SquareHitbox(value)

        else:
            setattr(self, name, value)


cdef class DynamicObject(StaticObject):
    cdef public dict vectors
    cdef public float gravity
    cdef public float slidingStep

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f],
        hitbox: typing.Union[SquareHitbox, CircleHitbox, typing.List[float], Vec4f],
        sprite: VSprite = None,
        group: str = None,
        mass: int = 1000,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
        animator: typing.Any = None,
        gravity: float = 300,
        slidingStep: float = INF,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, sprite, group, mass, layer, id, invisible, alpha, animator, variables, specials)

        self.doCollisionUpdate = True

        self.vectors = {
            "__fall__": AngleVector(0, 0)
        }

        self.gravity = gravity
        self.slidingStep = slidingStep

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

        if self.gravity == 0:
            self.vectors["__fall__"].power = 0

        elif self.collision(0, 1):
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

        if now.id not in self.game.cache["collisions"]:
            return []

        visited.add(now.id)

        hitbox = now.getEditHitbox(x, y, append)

        objects = []

        for obj in self.game.cache["collisions"][now.id]:
            if obj is None or obj["functions"] is None:
                continue

            if not (isinstance(obj["object"], DynamicObject) and "collision" in obj["functions"]["types"]):
                continue

            if isinstance(obj["object"], KinematicObject):
                continue

            if Collision.any(SquareHitbox([now.pos.x + hitbox.x + phitbox[0], now.pos.y + hitbox.y + phitbox[1], hitbox.width + phitbox[2], hitbox.height + phitbox[3]]), SquareHitbox([obj["object"].pos.x + obj["object"].hitbox.x, obj["object"].pos.y + obj["object"].hitbox.y, obj["object"].hitbox.width, obj["object"].hitbox.height])):
                objects.append(obj["object"])

                objects.extend(self.getObjectStructure(x, y, append, phitbox, obj["object"], visited))

        return objects

    def draw(self, px: float, py: float):
        super().draw(px, py)

        if self.game.debug:
            moving = self.getVectorsPower() * 6

            if abs(moving.x) > FLOAT_PRECISION or abs(moving.y) > FLOAT_PRECISION:
                hitbox = self.hitbox.rect()

                pygame.draw.line(
                    self.game.screen, (255, 0, 0) if "debug_color" not in self.specials else self.specials["debug_color"],
                    (px + self.pos.x + hitbox.x + hitbox.width / 2, py + self.pos.y + hitbox.y + hitbox.height / 2), (px + self.pos.x + hitbox.x + hitbox.width / 2 + moving.x, py + self.pos.y + hitbox.y + hitbox.height / 2 + moving.y), 1
                )

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False, append: bool = False, filter: typing.Callable = None) -> bool:
        hitbox = self.getEditHitbox(x, y, append)

        if self.id not in self.game.cache["collisions"]:
            return False

        flag = False

        for obj in self.game.cache["collisions"][self.id]:
            if Collision.any(hitbox.position(self.pos.x, self.pos.y), obj["object"].hitbox.position(obj["object"].pos.x, obj["object"].pos.y)) and (filter is None or filter(obj["object"])):
                if allowFunctions:
                    if obj["functions"] is not None:
                        for element in obj["functions"]["functions"]:
                            getattr(self.game.functions, element.replace("function::", "").replace("()", ""))(self.game, self, obj)

                if obj["functions"] is not None and "collision" in obj["functions"]["types"]:
                    if isinstance(obj["object"], DynamicObject) and isinstance(self, DynamicObject):
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

                    flag = True

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


cdef class KinematicObject(DynamicObject):
    cdef public float kinematicMoveX
    cdef public float kinematicMoveY

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f],
        sprite: VSprite = None,
        group: str = None,
        mass: int = 1000,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
        animator: typing.Any = None,
        gravity: float = 300,
        slidingStep: float = INF,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        DynamicObject.__init__(self, game, pos, hitbox, sprite, group, mass, layer, id, invisible, alpha, animator, gravity, slidingStep, variables, specials)

        self.doCollisionUpdate = True

        self.kinematicMoveX = 0
        self.kinematicMoveY = 0

    def __str__(self):
        return f"KinematicObject(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"KinematicObject(id = {self.id} pos = {self.pos})"

    def update(self):
        super().update()

        self.kinematicMoveX = 0
        self.kinematicMoveY = 0

    def move(self, x: float, y: float):
        self.kinematicMoveX = x
        self.kinematicMoveY = y

        affected_objects = self.getAffectedObjects()

        for obj in affected_objects:
            if isinstance(obj, DynamicObject) and not isinstance(obj, KinematicObject):
                if obj.id not in self.game.objects.movedByKinematic:
                    self.game.objects.movedByKinematic[obj.id] = 1

                    obj.move(x, y)

        self.pos.x += x
        self.pos.y += y

    def getAffectedObjects(self) -> typing.List["VObject"]:
        affected = []

        if self.id not in self.game.cache["collisions"]:
            return affected

        hitbox = self.getEditHitbox(0, 0, True)

        for obj in self.game.cache["collisions"][self.id]:
            if obj is None or obj["object"] is None:
                continue

            if Collision.any(hitbox.position(self.pos.x, self.pos.y), obj["object"].hitbox.position(obj["object"].pos.x, obj["object"].pos.y)):
                affected.append(obj["object"])

                if isinstance(obj["object"], DynamicObject) and not isinstance(obj["object"], KinematicObject):
                    affected.extend(self.getStackedObjects(obj["object"], set([self.id])))

        return affected

    def getStackedObjects(self, obj: "VObject", visited: typing.Set[int]) -> typing.List["VObject"]:
        stacked = []

        visited.add(obj.id)

        if obj.id not in self.game.cache["collisions"]:
            return stacked

        hitbox = obj.getEditHitbox(0, 0, True)

        for collision in self.game.cache["collisions"][obj.id]:
            if collision is None or collision["object"] is None:
                continue

            if collision["object"].id in visited:
                continue

            if Collision.any(hitbox.position(self.pos.x, self.pos.y, 1), collision["object"].hitbox.position(collision["object"].pos.x, collision["object"].pos.y)):
                if isinstance(collision["object"], DynamicObject) and not isinstance(collision["object"], KinematicObject):
                    stacked.append(collision["object"])

                    stacked.extend(self.getStackedObjects(collision["object"], visited))

        return stacked


cdef class Particle(DynamicObject):
    cdef public int liveTime
    cdef public float spriteSize
    cdef public float minusSpriteSizePerFrame

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f],
        sprite: VSprite = None,
        group: str = None,
        mass: int = 1000,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
        animator: typing.Any = None,
        gravity: float = 300,
        slidingStep: float = INF,
        liveTime: int = 60,
        minusSpriteSizePerFrame: float = 0.01,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        DynamicObject.__init__(self, game, pos, hitbox, sprite, group, mass, layer, id, invisible, alpha, animator, gravity, slidingStep, variables, specials)

        self.doCollisionUpdate = False

        self.liveTime = liveTime
        self.minusSpriteSizePerFrame = minusSpriteSizePerFrame

        self.spriteSize = 1

    def __str__(self):
        return f"Particle(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"Particle(id = {self.id} pos = {self.pos})"

    def collision(self, x: float = 0, y: float = 0, allowFunctions: bool = False, append: bool = False, filter: typing.Callable = None) -> bool:
        return False

    def update(self, collisions: list = None):
        super().update(collisions)

        self.liveTime -= 1

        self.sprite.pos.x -= math.ceil((1 - self.spriteSize) * self.sprite.size.x // 2)
        self.sprite.pos.y -= math.ceil((1 - self.spriteSize) * self.sprite.size.y // 2)

        self.spriteSize -= self.minusSpriteSizePerFrame

        self.sprite.pos.x += math.ceil((1 - self.spriteSize) * self.sprite.size.x // 2)
        self.sprite.pos.y += math.ceil((1 - self.spriteSize) * self.sprite.size.y // 2)

        if self.liveTime <= 0 or self.spriteSize <= 0:
            self.destroy()

        if self.sprite is not None and not self.game.noRefactorUpdate:
            self.sprite.resize(round(self.sprite.size.x * self.spriteSize), round(self.sprite.size.y * self.spriteSize))


cdef class Text(StaticObject):
    cdef public str font
    cdef public str message
    cdef public int fontSize
    cdef public object fontColor
    cdef public object alignment
    cdef public str vertical
    cdef public str horizontal
    cdef public int tx
    cdef public int ty
    cdef public int hstep
    cdef public object fontClass

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f, Vec4i],
        group: str = None,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
        font: str = "Arial",
        message: str = "Text",
        fontSize: int = 13,
        fontColor: object = "#FFFFFF",
        alignment: typing.List[bool] = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, None, group, 0, layer, id, invisible, alpha, None, variables, specials)

        self.doCollisionUpdate = False

        if alignment is not None:
            self.alignment = alignment

        else:
            self.alignment = ["center", "center"]

        self.font = font
        self.message = message
        self.fontSize = fontSize
        self.alpha = alpha
        self.fontColor = fontColor
        self.alignment = alignment

        self.fontClass = get_font(self.font, self.fontSize)

        self.vertical = alignment[0]
        self.horizontal = alignment[1]

        self.hstep = self.fontClass.size("Ag")[1]

        self.tx = 0
        self.ty = 0

    def __str__(self):
        return f"Text(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"Text(id = {self.id} pos = {self.pos})"

    def draw(self, px: float, py: float):
        width, height = self.fontClass.size(self.message)

        if self.game.usingWidth + width > self.pos.x + px > -width and self.game.usingHeight + height > self.pos.y + py > -height:
            if not self.invisible or self.game.forcedViewObject:
                if self.horizontal == "center":
                    self.tx = self.hitbox.width / 2 - width / 2

                if self.horizontal == "left":
                    self.tx = 4

                if self.horizontal == "right":
                    self.tx = self.hitbox.width - width - 4

                if self.vertical == "center":
                    self.ty = (self.hitbox.height - self.hstep) / 2

                if self.vertical == "up":
                    self.ty = 2

                if self.vertical == "down":
                    self.ty = self.hitbox.height - self.hstep - 2

                print_text(self.game.screen, self.pos.x + self.tx + px, self.pos.y + self.ty + py, self.message, self.fontSize, self.font, self.fontColor, self.alpha)

        if self.game.debug or (self.group.startswith("__") and self.group.endswith("__") and not self.group == "__debug_unvisiable__"):
            pygame.draw.rect(
                self.game.screen, (255, 0, 0) if "debug_color" not in self.specials else self.specials["debug_color"],
                (math.trunc(self.pos.x) + self.hitbox.x + px, math.trunc(self.pos.y) + self.hitbox.y + py, self.hitbox.width, self.hitbox.height), 1
            )


cdef class Field(Text):
    cdef object out
    cdef object text
    cdef str splitSymbol

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f, Vec4i],
        group: str = None,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
        font: str = "Arial",
        message: str = "Text",
        fontSize: int = 13,
        fontColor: object = "#FFFFFF",
        alignment: typing.List[bool] = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        Text.__init__(self, game, pos, hitbox, group, layer, id, invisible, alpha, font, message, fontSize, fontColor, alignment, variables, specials)

        self.doCollisionUpdate = False

        self.splitSymbol = "ꙮ"

        self.text = list(self.message)

        for i in range(len(self.text)):
            if self.text[i] == " " and self.text[i - 1] not in (" ", "~") and i > 0:
                self.text[i] = self.splitSymbol

        self.text = ("".join(self.text)).split(self.splitSymbol)

        self.hstep = self.fontClass.size("Ag")[1]

        self.out = []

    def __str__(self):
        return f"Field(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"Field(id = {self.id} pos = {self.pos})"

    def draw(self, px: float, py: float):
        if not self.invisible or self.game.forcedViewObject:
            self.init()

            if self.vertical == "center":
                ty = (self.hitbox.height - len(self.out) * self.hstep) / 2

            elif self.vertical == "up":
                ty = 2

            elif self.vertical == "down":
                ty = self.hitbox.height - len(self.out) * self.hstep - 2

            else:
                raise NameError(f"horizontal {self.horizontal} is not difined")

            for i, element in enumerate(self.out):
                if self.horizontal == "center":
                    print_text(self.game.screen, self.pos.x + (self.hitbox.width / 2 - self.fontClass.size(element)[0] / 2) + px, self.pos.y + i * self.hstep + ty + py, element, self.fontSize, self.font, self.fontColor, self.alpha)

                elif self.horizontal == "left":
                    print_text(self.game.screen, self.pos.x + 4 + px, self.pos.y + i * self.hstep + ty + py, element, self.fontSize, self.font, self.fontColor, self.alpha)

                elif self.horizontal == "right":
                    print_text(self.game.screen, (self.pos.x + self.hitbox.width) - self.fontClass.size(element)[0] - 4 + px, self.pos.y + i * self.hstep + ty + py, element, self.fontSize, self.font, self.fontColor, self.alpha)

                else:
                    raise NameError(f"horizontal {self.horizontal} is not difined")

        if self.game.debug or (self.group.startswith("__") and self.group.endswith("__") and not self.group == "__debug_unvisiable__"):
            pygame.draw.rect(
                self.game.screen, (255, 0, 0) if "debug_color" not in self.specials else self.specials["debug_color"],
                (math.trunc(self.pos.x) + self.hitbox.x + px, math.trunc(self.pos.y) + self.hitbox.y + py, self.hitbox.width, self.hitbox.height), 1
            )

    def init(self) -> None:
        self.text = list(self.message)

        for i in range(len(self.text)):
            if self.text[i] == " " and self.text[i - 1] not in (" ", "~") and i > 0:
                self.text[i] = self.splitSymbol

        self.text = ("".join(self.text)).split(self.splitSymbol)

        l = 0
        r = len(self.text) - 1

        if self.text[0] == "/t":
            self.out = [" " * 4]

        else:
            self.out = [self.text[0]]

        while l < r:
            if self.fontClass.size(self.out[-1] + self.text[l + 1] + " ")[0] < self.hitbox.width:
                if self.text[l + 1] == "/n":
                    self.out.append("")

                elif self.text[l + 1] == "/t":
                    self.out[len(self.out) - 1] += " " * 4

                elif len(self.out[len(self.out) - 1]) == 0:
                    self.out[len(self.out) - 1] += f"{self.text[l + 1]}"

                else:
                    self.out[len(self.out) - 1] += f" {self.text[l + 1]}"

                l += 1

            else:
                self.out.append("")

        # self.ay = self.hitbox.height / 2 - (self.fontClass.size("Ag")[1] / 2 * len(self.out))

        var = (len(self.out) - self.hitbox.height // self.hstep) * self.hstep

        return var if var > 0 else 0


cdef class Button(StaticObject):
    cdef public str font
    cdef public str message
    cdef public int fontSize
    cdef public object fontColor
    cdef public object ramaColor
    cdef public object backgroundColor
    cdef public object alignment
    cdef public str vertical
    cdef public str horizontal
    cdef public int tx
    cdef public int ty
    cdef public int hstep
    cdef public object fontClass
    cdef public bint pressed
    cdef public bint event

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f, Vec4i],
        group: str = None,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        alpha: int = 255,
        font: str = "Arial",
        message: str = "Text",
        fontSize: int = 13,
        ramaColor: typing.List[str] = ["#000000", "#000000", "#000000"],
        fontColor: typing.List[str] = ["#FFFFFF", "#FFFFFF", "#FFFFFF"],
        backgroundColor: typing.List[str] = ["#AAAAAA", "#888888", "#444444"],
        alignment: typing.List[bool] = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, None, group, 0, layer, id, invisible, alpha, None, variables, specials)

        self.doCollisionUpdate = False

        if alignment is not None:
            self.alignment = alignment

        else:
            self.alignment = ["center", "center"]

        self.font = font
        self.message = message
        self.fontSize = fontSize
        self.alpha = alpha
        self.alignment = alignment

        self.ramaColor = ramaColor
        self.fontColor = fontColor
        self.backgroundColor = backgroundColor

        self.fontClass = get_font(self.font, self.fontSize)

        self.vertical = alignment[0]
        self.horizontal = alignment[1]

        self.hstep = self.fontClass.size("Ag")[1]

        self.pressed = False
        self.event = False

        self.tx = 0
        self.ty = 0

    def __str__(self):
        return f"Button(id = {self.id} pos = {self.pos})"

    def __repr__(self):
        return f"Button(id = {self.id} pos = {self.pos})"

    def draw(self, px: float, py: float):
        width, height = self.fontClass.size(self.message)

        if self.event:
            self.event = False

        if self.pos.x + px < self.game.mouse[0] < self.pos.x + px + self.hitbox.width:
            if self.pos.y + py < self.game.mouse[1] < self.pos.y + py + self.hitbox.height:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True

                    active = 2

                else:
                    if self.pressed:
                        self.pressed = False

                        self.event = True

                    active = 1

            else:
                self.pressed = False

                active = 0

        else:
            self.pressed = False

            active = 0

        if not self.invisible or self.game.forcedViewObject:
            alphaRect(self.game.screen, hex_to_rgb(self.backgroundColor[active]) + [self.alpha], SquareHitbox([self.pos.x + px, self.pos.y + py, self.hitbox.width, self.hitbox.height]))
            alphaRect(self.game.screen, hex_to_rgb(self.ramaColor[active]) + [self.alpha], SquareHitbox([self.pos.x + px, self.pos.y + py, self.hitbox.width, self.hitbox.height]), 1)

        if self.game.usingWidth + width > self.pos.x + px > -width and self.game.usingHeight + height > self.pos.y + py > -height:
            if not self.invisible or self.game.forcedViewObject:
                if self.horizontal == "center":
                    self.tx = self.hitbox.width / 2 - width / 2

                if self.horizontal == "left":
                    self.tx = 4

                if self.horizontal == "right":
                    self.tx = self.hitbox.width - width - 4

                if self.vertical == "center":
                    self.ty = (self.hitbox.height - self.hstep) / 2

                if self.vertical == "up":
                    self.ty = 2

                if self.vertical == "down":
                    self.ty = self.hitbox.height - self.hstep - 2

                print_text(self.game.screen, self.pos.x + self.tx + px, self.pos.y + self.ty + py, self.message, self.fontSize, self.font, self.fontColor[active], self.alpha)

        if self.game.debug or (self.group.startswith("__") and self.group.endswith("__") and not self.group == "__debug_unvisiable__"):
            pygame.draw.rect(
                self.game.screen, (255, 0, 0) if "debug_color" not in self.specials else self.specials["debug_color"],
                (math.trunc(self.pos.x) + self.hitbox.x + px, math.trunc(self.pos.y) + self.hitbox.y + py, self.hitbox.width, self.hitbox.height), 1
            )
