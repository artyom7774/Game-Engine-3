from engine.classes.objects import StaticObject, DynamicObject, KinematicObject, Particle, Button

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox

from engine import profiler

from engine.variables import *

import typing
import random

MAX_COUNT_NODE_OBJECTS = 10
OBJECT_POS_PRECISION = 1
MIN_NODE_SIZE = 100


class QuadTreeNode:
    def __init__(self, game, objects, rect) -> None:
        self.game = game

        self.id = random.randint(1, 1000000000)

        self.objects = objects

        self.rects = None
        self.rect = rect

        self.childrens = None

        if len(self.objects) >= MAX_COUNT_NODE_OBJECTS:
            self.divide()

    def add(self, obj) -> None:
        if self.childrens is None:
            if str(obj.id) not in self.game.objects.tree.links:
                self.game.objects.tree.links[str(obj.id)] = []

            self.game.objects.tree.links[str(obj.id)].append(self)
            self.objects.append(obj)

            self.divide()

            return

        for i, rect in enumerate(self.rects):
            if Collision.any(SquareHitbox(rect), obj.hitbox.position(obj.pos.x, obj.pos.y, OBJECT_POS_PRECISION)):
                self.childrens[i].add(obj)

    def remove(self, obj) -> None:
        if self.childrens is None:
            if obj in self.objects:
                self.objects.remove(obj)

            return

        for i, rect in enumerate(self.rects):
            if Collision.any(SquareHitbox(rect), obj.hitbox.position(obj.pos.x, obj.pos.y, OBJECT_POS_PRECISION)):
                self.childrens[i].remove(obj)

    def divide(self) -> None:
        if len(self.objects) >= MAX_COUNT_NODE_OBJECTS and min(self.rect[2], self.rect[3]) // 2 >= MIN_NODE_SIZE:
            for obj in self.objects:
                self.game.objects.tree.links[str(obj.id)] = []

            self.childrens = []

            self.rects = [
                [self.rect[0], self.rect[1], self.rect[2] // 2, self.rect[3] // 2],
                [self.rect[0] + self.rect[2] // 2, self.rect[1], self.rect[2] // 2, self.rect[3] // 2],
                [self.rect[0], self.rect[1] + self.rect[3] // 2, self.rect[2] // 2, self.rect[3] // 2],
                [self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2, self.rect[2] // 2, self.rect[3] // 2]
            ]

            for rect in self.rects:
                self.childrens.append(QuadTreeNode(self.game, list(filter(lambda obj: Collision.any(SquareHitbox(rect), obj.hitbox.position(obj.pos.x, obj.pos.y, OBJECT_POS_PRECISION)), self.objects)), rect))

            self.objects = []

    def getAnotherNodes(self, square: typing.List[int]) -> typing.List["QuadTreeNode"]:
        if self.childrens is None:
            return [self]

        out = []

        for i, rect in enumerate(self.rects):
            if Collision.any(SquareHitbox(rect), SquareHitbox(square)):
                out.extend(self.childrens[i].getAnotherNodes(square))

        return out

    def getAnotherObjects(self, square: typing.List[int]) -> typing.Set["VObject"]:
        if self.childrens is None:
            return set(self.objects)

        out = set()

        for i, rect in enumerate(self.rects):
            if Collision.any(SquareHitbox(rect), SquareHitbox(square)):
                out |= self.childrens[i].getAnotherObjects(square)

        return out


class QuadTree:
    size = 1e3

    def __init__(self, game) -> None:
        self.game = game

        self.root = None
        self.links = {}

        self.init()

    def init(self) -> None:
        self.root = QuadTreeNode(self.game, self.game.objects.objects, [-self.size, -self.size, 2 * self.size, 2 * self.size])

    def resize(self, size) -> None:
        if size < self.size:
            return

        self.size = 2 * size

        self.init()

    def update(self, obj) -> None:
        if type(obj) != StaticObject:
            return

        objects = self.root.getAnotherNodes([obj.pos.x + obj.hitbox.x, obj.pos.y + obj.hitbox.y, obj.hitbox.width, obj.hitbox.height])
        link = self.links[str(obj.id)]

        if len(objects) == len(link) and [objects[i].id == link[i].id for i in range(len(objects))]:
            return

        self.links[str(obj.id)] = []

        self.remove(obj)
        self.add(obj)

    def add(self, obj) -> None:
        if type(obj) != StaticObject:
            return

        self.root.add(obj)

    def remove(self, obj) -> None:
        if type(obj) != StaticObject:
            return

        self.root.remove(obj)

    @profiler.profile()
    def getUsingDynamicObject(self, rect, obj) -> typing.List[VObject]:
        dynamicsObjects = set()

        for cobj in self.game.objects.objects:
            if type(cobj) == StaticObject:
                continue

            if cobj.id == obj.id:
                continue

            base = cobj.hitbox.position(cobj.pos.x, cobj.pos.y, OBJECT_POS_PRECISION)

            if Collision.any(SquareHitbox(rect), base):
                dynamicsObjects.add(cobj)

        return dynamicsObjects

    def getUsingObjects(self, obj) -> typing.List[VObject]:
        resulting = obj.getVectorsPower()

        hitbox = obj.hitbox.rect()

        base = obj.hitbox.position(obj.pos.x, obj.pos.y, OBJECT_POS_PRECISION).rect().get()
        rect = [obj.pos.x + hitbox.x + 2 * resulting.x - OBJECT_POS_PRECISION, obj.pos.y + hitbox.y + 2 * resulting.y - OBJECT_POS_PRECISION, hitbox.width + 2 * OBJECT_POS_PRECISION, hitbox.height + 2 * OBJECT_POS_PRECISION]

        full = [
            min(base[0], rect[0]),
            min(base[1], rect[1]),
            max(base[0] + base[2], rect[0] + rect[2]) - min(base[0], rect[0]),
            max(base[1] + base[3], rect[1] + rect[3]) - min(base[1], rect[1])
        ]

        return list(self.root.getAnotherObjects(full) | self.getUsingDynamicObject(full, obj))


class ObjectGroup:
    def __init__(self, game, objects: typing.List[VObject] = None) -> None:
        if objects is None:
            objects = []

        self.game = game

        self.tree = None

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

    def init(self) -> None:
        self.tree = QuadTree(self.game)

    def empty(self) -> None:
        collisions = self.collisions

        self.game.objects = ObjectGroup(self.game)
        self.game.objects.collisions = collisions

    def add(self, obj: VObject) -> None:
        if isinstance(obj, Particle) and self.game.particleInAnotherGroup:
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

        self.tree.add(obj)

        self.tree.resize(abs(obj.pos.x) + abs(obj.pos.y))

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

        self.tree.remove(obj)

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
