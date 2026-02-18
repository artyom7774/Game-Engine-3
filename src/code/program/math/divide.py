from engine.special.exception import EngineError

import math


def divide(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["a"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"] is not None:
        a = float(nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"])

    else:
        a = float(nodes["objects"][str(id)]["inputs"]["a"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["b"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"] is not None:
        b = float(nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"])

    else:
        b = float(nodes["objects"][str(id)]["inputs"]["b"]["standard"])

    if b == 0:
        raise EngineError("division by zero")

    answer = int(a / b) if math.trunc(round(a / b, 10)) == math.ceil(round(a / b, 10)) else round(a / b, 10)

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
