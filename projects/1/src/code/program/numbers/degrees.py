import math


def degrees(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["radians"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["radians"]["value"]["value"] is not None:
        radians = float(nodes["objects"][str(id)]["inputs"]["radians"]["value"]["value"])

    else:
        radians = float(nodes["objects"][str(id)]["inputs"]["radians"]["standard"])

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = math.degrees(radians)

    return queue
