from engine.classes.objects import DynamicObject, Button

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox

from engine.variables import *

import typing


class ObjectGroup:
    def __init__(self, game, objects: typing.List[VObject] = None) -> None:
        if objects is None:
            objects = []

        self.game = game

        self.collisions = Collision()

        self.objects = []
        self.buttonObjects = []

        for obj in self.objects:
            if type(obj) == Button:
                self.buttonObjects.append(obj)

            self.add(obj)

        self.objectById = {}
        self.objectByGroup = {}

        self.maxLenghtObject = -INF
        self.minLenghtObject = +INF

    def empty(self):
        self.maxLenghtObject = -INF
        self.minLenghtObject = +INF

        for obj in self.objects:
            self.remove(obj)

    def add(self, obj: VObject) -> None:
        self.updateMinLenghtObject(obj)
        self.updateMaxLenghtObject(obj)

        if isinstance(obj, DynamicObject):
            self.objects.insert(0, obj)

        else:
            self.objects.append(obj)

        if type(obj) == Button:
            self.buttonObjects.append(obj)

        self.objectById[obj.id] = obj

        if obj.group not in self.objectByGroup:
            self.objectByGroup[obj.group] = {}

        self.objectByGroup[obj.group][obj.id] = obj

    def remove(self, obj: VObject) -> None:
        self.objects.remove(obj)

        if type(obj) == Button:
            self.buttonObjects.remove(obj)

        if obj.id in self.objectById:
            self.objectById.pop(obj.id)

        if obj.id in self.objectByGroup[obj.group]:
            self.objectByGroup[obj.group].pop(obj.id)

    def getById(self, id: int) -> VObject:
        return self.objectById.get(id)

    def removeByGroup(self, group: str) -> None:
        if group not in self.objectByGroup:
            return

        objects = list(self.objectByGroup[group].values())

        for obj in objects:
            self.remove(obj)

    def removeById(self, id: int) -> None:
        if id not in self.objectById:
            return

        self.remove(self.objectById[id])

    def getByGroup(self, group) -> typing.List[VObject]:
        return [element for element in self.objectByGroup[group].values()]

    def updateMinLenghtObject(self, obj: VObject) -> None:
        self.minLenghtObject = min(self.minLenghtObject, obj.hitbox.width + obj.hitbox.height)

    def updateMaxLenghtObject(self, obj: VObject) -> None:
        self.maxLenghtObject = max(self.maxLenghtObject, obj.hitbox.width + obj.hitbox.height)

    def update(self) -> None:
        right = [obj for obj in self.objects if not hasattr(obj, "getVectorsPower") or obj.getVectorsPower().x >= 0]
        left = [obj for obj in self.objects if hasattr(obj, "getVectorsPower") and obj.getVectorsPower().x < 0]

        right.sort(key=lambda x: x.pos.y)
        left.sort(key=lambda x: x.pos.y)

        for obj in right + left:
            obj.update()

    def draw(self) -> None:
        self.game.camera.update()

        px = self.game.camera.x()
        py = self.game.camera.y()

        for obj in sorted(self.objects, key=lambda x: x.layer):
            obj.draw(px, py)

            """
            sprite = None

            if obj.sprite is not None:
                if type(obj.sprite) == Sprite:
                    sprite = obj.sprite.get()

                elif type(obj.sprite) == list:
                    alphaRect(self.game.screen, obj.sprite, SquareHitbox([obj.pos.x, obj.pos.y, obj.hitbox.width, obj.hitbox.height]))

                    continue

                elif type(obj.sprite) == types.FunctionType:
                    obj.sprite()

                    continue

                else:
                    sprite = obj.sprite.get(obj)

            if not obj.invisible or self.game.forcedViewObject:
                if obj.sprite is not None and sprite is not None and type(obj.sprite) != list:
                    # obj.sprite.pos.x = 0
                    # obj.sprite.pos.y = 0

                    # print(obj.sprite.pos)

                    if self.game.usingWidth + 200 > obj.pos.x + obj.sprite.pos.x + px > -200 and self.game.usingHeight + 200 > obj.pos.y + obj.sprite.pos.y + py > -200:
                        self.game.screen.blit(sprite, (obj.pos.x + obj.sprite.pos.x + px, obj.pos.y + obj.sprite.pos.y + py))

            if self.game.debug or (obj.group.startswith("__") and obj.group.endswith("__") and not obj.group == "__debug_unvisiable__"):
                pygame.draw.rect(
                    self.game.screen, (255, 0, 0) if "debug_color" not in obj.specials else obj.specials["debug_color"],
                    (math.trunc(obj.pos.x) + obj.hitbox.x + px, math.trunc(obj.pos.y) + obj.hitbox.y + py, obj.hitbox.width, obj.hitbox.height), 1
                )

            if self.game.debug and type(obj) == DynamicObject:
                moving = obj.getVectorsPower() * 6

                # print(moving)

                pygame.draw.line(
                    self.game.screen, (255, 0, 0) if "debug_color" not in obj.specials else obj.specials["debug_color"],
                    (px + obj.pos.x + obj.hitbox.x + obj.hitbox.width / 2, py + obj.pos.y + obj.hitbox.y + obj.hitbox.height / 2), (px + obj.pos.x + obj.hitbox.x + obj.hitbox.width / 2 + moving.x, py + obj.pos.y + obj.hitbox.y + obj.hitbox.height / 2 + moving.y), 1
                )
            """
