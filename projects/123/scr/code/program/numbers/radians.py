import math


def radians(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["degrees"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["degrees"]["value"]["value"] is not None:
        degrees = float(nodes["objects"][str(id)]["inputs"]["degrees"]["value"]["value"])

    else:
        degrees = float(nodes["objects"][str(id)]["inputs"]["degrees"]["standard"])

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = math.radians(degrees)

    return queue
