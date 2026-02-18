from engine.special.exception import EngineError

from engine.classes.sprite import Sprite
from engine.vector.int import Vec2i

import typing
import math

VARIABLE_TYPES = ["number", "text", "logic", "list", "dict"]

def setVariableType(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["variable"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["variable"]["value"]["value"] is not None:
        variable = str(nodes["objects"][str(id)]["inputs"]["variable"]["value"]["value"])

    else:
        variable = str(nodes["objects"][str(id)]["inputs"]["variable"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["type"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["type"]["value"]["value"] is not None:
        type = VARIABLE_TYPES[int(nodes["objects"][str(id)]["inputs"]["type"]["value"]["value"])]

    else:
        type = VARIABLE_TYPES[int(nodes["objects"][str(id)]["inputs"]["type"]["standard"])]

    try:
        if type == "number":
            answer = int(variable) if math.trunc(float(variable)) == math.ceil(float(variable)) else float(variable)

        elif type == "text":
            answer = variable

        elif type == "logic":
            answer = bool(variable)

        elif type == "list":
            answer = list(variable)

        else:
            answer = None

    except BaseException:
        raise EngineError(f"can't set variable {variable} to type {type}")

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["variable"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
