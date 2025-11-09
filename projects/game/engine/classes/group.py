from engine.classes.objects import DynamicObject, KinematicObject, Particle, Button

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
        self.particles = []

        self.buttons = []

        for obj in self.objects:
            if type(obj) == Button:
                self.buttons.append(obj)

            self.add(obj)

        self.objectById = {}
        self.objectByGroup = {}

        self.movedByKinematic = {}

        self.maxLengthObject = -INF
        self.minLengthObject = +INF

    def empty(self):
        self.maxLengthObject = -INF
        self.minLengthObject = +INF

        for obj in self.objects:
            self.remove(obj)

    def add(self, obj: VObject) -> None:
        self.updateMinLengthObject(obj)
        self.updateMaxLengthObject(obj)

        if isinstance(obj, Particle):
            self.particles.append(obj)

        elif isinstance(obj, DynamicObject):
            self.objects.insert(0, obj)

        else:
            self.objects.append(obj)

        if type(obj) == Button:
            self.buttons.append(obj)

        self.objectById[obj.id] = obj

        if obj.group not in self.objectByGroup:
            self.objectByGroup[obj.group] = {}

        self.objectByGroup[obj.group][obj.id] = obj

    def remove(self, obj: VObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)

        elif obj in self.particles:
            self.particles.remove(obj)

        if type(obj) == Button:
            self.buttons.remove(obj)

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
            return False

        self.remove(self.objectById[id])

        return True

    def getByGroup(self, group) -> typing.List[VObject]:
        return [element for element in self.objectByGroup[group].values()] if self.objectByGroup.get(group) is not None else None

    def updateMinLengthObject(self, obj: VObject) -> None:
        self.minLengthObject = min(self.minLengthObject, obj.hitbox.width + obj.hitbox.height)

    def updateMaxLengthObject(self, obj: VObject) -> None:
        self.maxLengthObject = max(self.maxLengthObject, obj.hitbox.width + obj.hitbox.height)

    def update(self) -> None:
        right = [obj for obj in self.objects if not hasattr(obj, "getVectorsPower") or obj.getVectorsPower().x >= 0]
        left = [obj for obj in self.objects if hasattr(obj, "getVectorsPower") and obj.getVectorsPower().x < 0]

        right.sort(key=lambda x: x.pos.y)
        left.sort(key=lambda x: x.pos.y)

        self.movedByKinematic = {}

        for obj in right + left + self.particles:
            obj.update()

    def draw(self) -> None:
        self.game.camera.update()

        px = self.game.camera.x()
        py = self.game.camera.y()

        for obj in sorted(self.particles + self.objects, key=lambda x: x.layer):
            obj.draw(px, py)
