from libc.math cimport sqrt, sin, cos

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox

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

    def draw(self, px, py):
        if self.sprite is not None:
            if self.game.usingWidth + self.sprite.pos.x + self.sprite.size.x > self.pos.x + px > -self.sprite.pos.x - self.sprite.size.x and self.game.usingHeight + self.sprite.pos.y + self.sprite.size.y > self.pos.y + py > -self.sprite.pos.y - self.sprite.size.y:
                sprite = self.sprite.get()

                if not self.invisible or self.game.forcedViewObject:
                    if sprite is not None:
                        if self.game.usingWidth + 200 > self.pos.x + self.sprite.pos.x + px > -200 and self.game.usingHeight + 200 > self.pos.y + self.sprite.pos.y + py > -200:
                            self.game.screen.blit(sprite, (self.pos.x + self.sprite.pos.x + px, self.pos.y + self.sprite.pos.y + py))

        if self.game.debug or (self.group.startswith("__") and self.group.endswith("__") and not self.group == "__debug_unvisiable__"):
            pygame.draw.rect(
                self.game.screen, (255, 0, 0) if "debug_color" not in self.specials else self.specials["debug_color"],
                (math.trunc(self.pos.x) + self.hitbox.x + px, math.trunc(self.pos.y) + self.hitbox.y + py, self.hitbox.width, self.hitbox.height), 1
            )

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
    cdef public float slidingStep

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
        animator: typing.Any = None,
        gravity: float = 300,
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

    def draw(self, px, py):
        super().draw(px, py)

        if self.game.debug:
            moving = self.getVectorsPower() * 6

            # print(moving)

            pygame.draw.line(
                self.game.screen, (255, 0, 0) if "debug_color" not in self.specials else self.specials["debug_color"],
                (px + self.pos.x + self.hitbox.x + self.hitbox.width / 2, py + self.pos.y + self.hitbox.y + self.hitbox.height / 2), (px + self.pos.x + self.hitbox.x + self.hitbox.width / 2 + moving.x, py + self.pos.y + self.hitbox.y + self.hitbox.height / 2 + moving.y), 1
            )

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


cdef class Text(StaticObject):
    cdef public str font
    cdef public str message
    cdef public int fontSize
    cdef public int alpha
    cdef public str fontColor
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
        font: str = "Arial",
        message: str = "Text",
        fontSize: int = 13,
        alpha: int = 255,
        fontColor: str = "#FFFFFF",
        alignment: typing.List[bool] = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, None, group, 0, layer, id, invisible, None, variables, specials)

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

    def draw(self, px, py):
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
        font: str = "Arial",
        message: str = "Text",
        fontSize: int = 13,
        fontColor: str = "#FFFFFF",
        alignment: typing.List[bool] = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        Text.__init__(self, game, pos, hitbox, group, layer, id, invisible, font, message, fontSize, fontColor, alignment, variables, specials)

        self.splitSymbol = "ꙮ"

        self.text = list(self.message)

        for i in range(len(self.text)):
            if self.text[i] == " " and self.text[i - 1] not in (" ", "~") and i > 0:
                self.text[i] = self.splitSymbol

        self.text = ("".join(self.text)).split(self.splitSymbol)

        self.hstep = self.fontClass.size("Ag")[1]

        self.out = []

    def draw(self, px, py):
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
    cdef public int alpha
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

    def __init__(
        self, game: object,
        pos: typing.Union[typing.List[float], Vec2f, Vec2i],
        hitbox: typing.Union[SquareHitbox, typing.List[float], Vec4f, Vec4i],
        group: str = None,
        layer: int = 0,
        id: int = None,
        invisible: bool = False,
        font: str = "Arial",
        message: str = "Text",
        fontSize: int = 13,
        alpha: int = 255,
        ramaColor: typing.List[str] = ["#000000", "#000000", "#000000"],
        fontColor: typing.List[str] = ["#FFFFFF", "#FFFFFF", "#FFFFFF"],
        backgroundColor: typing.List[str] = ["#AAAAAA", "#888888", "#444444"],
        alignment: typing.List[bool] = None,
        variables: typing.Dict[str, typing.Any] = None,
        specials: typing.Dict[str, typing.Any] = None,
        *args, **kwargs
    ) -> None:
        StaticObject.__init__(self, game, pos, hitbox, None, group, 0, layer, id, invisible, None, variables, specials)

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

        self.tx = 0
        self.ty = 0

    def draw(self, px, py):
        width, height = self.fontClass.size(self.message)

        if self.pos.x + px < self.game.mouse[0] < self.pos.x + px + self.hitbox.width:
            if self.pos.y + py < self.game.mouse[1] < self.pos.y + py + self.hitbox.height:
                if pygame.mouse.get_pressed()[0]:
                    active = 2

                else:
                    active = 1

            else:
                active = 0

        else:
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
