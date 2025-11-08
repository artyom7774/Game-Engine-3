import math


def modulo(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["a"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"] is not None:
        a = float(nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"])

    else:
        a = float(nodes["objects"][str(id)]["inputs"]["a"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["b"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"] is not None:
        b = float(nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"])

    else:
        b = float(nodes["objects"][str(id)]["inputs"]["b"]["standard"])

    answer = int(a % b) if math.trunc(round(a % b, 10)) == math.ceil(round(a % b, 10)) else round(a % b, 10)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
