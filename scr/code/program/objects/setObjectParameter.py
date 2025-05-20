from engine.classes.sprite import Sprite
from engine.vector.int import Vec2i

import typing

OBJECT_PARAMETERS = ["hitbox", "group", "mass", "layer", "invisible", "gravity", "slidingStep", "message", "fontSize", "alignment", "fontColor", "backgroundColor", "ramaColor", "spriteHitbox", "liveTime", "minusSpriteSizePerFrame"]
OBJECT_PARAMETERS_TYPES = ["list", "text", "int", "int", "logic", "float", "float", "text", "int", "list", "eval", "eval", "eval", "list", "float", "float"]


def setObjectParameter(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    def decode(operation, text: str) -> typing.Any:
        if OBJECT_PARAMETERS_TYPES[operation] == "eval":
            try:
                return eval(text)

            except BaseException:
                return text

        if OBJECT_PARAMETERS_TYPES[operation] == "list":
            return eval(text)

        if OBJECT_PARAMETERS_TYPES[operation] == "text":
            return text

        if OBJECT_PARAMETERS_TYPES[operation] == "int":
            return int(text)

        if OBJECT_PARAMETERS_TYPES[operation] == "float":
            return float(text)

        if OBJECT_PARAMETERS_TYPES[operation] == "logic":
            return True if text in ("True", "true", "1", "+") else False

    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        operation = int(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        operation = int(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["value"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"] is not None:
        value = decode(operation, nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"])

    else:
        value = decode(operation, nodes["objects"][str(id)]["inputs"]["value"]["standard"])

    if OBJECT_PARAMETERS[operation] == "spriteHitbox":
        obj = program.objects.getById(ids)

        if obj.sprite is not None:
            obj.sprite = Sprite(program, obj, obj.sprite.path, Vec2i(value[0], value[1]), Vec2i(value[2], value[3]))

    else:
        program.objects.getById(ids).setParameter(OBJECT_PARAMETERS[operation], value)

    return queue
