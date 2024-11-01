from engine.classes.collision import Collision

from engine.classes.objects import DynamicObject

from engine.variables import *

import typing

if typing.TYPE_CHECKING:
    from engine.classes.group import ObjectGroup

else:
    pass


def binaryLeft(objects: typing.List[VObject], distance: float) -> int:
    left, right = 0, len(objects) - 1
    while left < right:
        mid = (left + right) // 2

        if objects[mid].distance < distance:
            left = mid + 1

        else:
            right = mid

    return left if objects[left].distance >= distance else 0


def binaryRight(objects: typing.List[VObject], distance: float) -> int:
    left, right = 0, len(objects) - 1

    while left < right:
        mid = (left + right + 1) // 2

        if objects[mid].distance > distance:
            right = mid - 1

        else:
            left = mid

    return right if objects[right].distance <= distance else len(objects) - 1


class GetUsingObjects:
    @staticmethod
    def getUsingObjectsBase(game, group: "ObjectGroup") -> None:
        dynamics = [obj for obj in group.objects if type(obj) == DynamicObject]

        for obj in dynamics:
            GetUsingObjects.getUsingObjectsIteration(game, group.objects, obj)

    @staticmethod
    def getUsingObjectsCircle(game, group: "ObjectGroup") -> None:
        sortedObjects = []
        dynamicsObjects = []

        for obj in group.objects:
            if type(obj) == DynamicObject:
                dynamicsObjects.append(obj)

            else:
                sortedObjects.append(obj)

        for obj in dynamicsObjects:
            position = binaryLeft(sortedObjects, obj.distance) - 1

            # print(len(sortedObjects), position)

            sortedObjects.insert(position, obj)

        game.cash["object_sorted_by_distance"] = sortedObjects

        # game.cash["object_sorted_by_distance"] = sorted(group.objects, key=lambda obj: obj.distance)

        for obj in dynamicsObjects:
            l = binaryLeft(game.cash["object_sorted_by_distance"], obj.distance - group.maxLenghtObject)
            r = binaryRight(game.cash["object_sorted_by_distance"], obj.distance + group.maxLenghtObject) + 1

            GetUsingObjects.getUsingObjectsIteration(game, game.cash["object_sorted_by_distance"][l:r], obj)

    @staticmethod
    def getUsingObjectsIteration(game, objects, obj: "VObject"):
        game.cash["collisions"][obj.id] = []

        hitbox = obj.hitbox.copy()

        hitbox.x -= hitbox.width
        hitbox.y -= hitbox.height

        hitbox.width *= 3
        hitbox.height *= 3

        for j, second in enumerate(objects):
            if obj.id == second.id:
                continue

            var = obj.collisions.get(second.group)

            if var is not None:
                if True or Collision.rect(second.pos.x + second.hitbox.x, second.pos.y + second.hitbox.y, second.hitbox.width, second.hitbox.height, obj.pos.x + hitbox.x, obj.pos.y + hitbox.y, hitbox.width, hitbox.height):
                    game.cash["collisions"][obj.id].append({"object": second, "functions": var})
