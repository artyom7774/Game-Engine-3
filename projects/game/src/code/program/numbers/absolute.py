import math


def absolute(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["number"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"] is not None:
        x = float(nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"])

    else:
        x = float(nodes["objects"][str(id)]["inputs"]["number"]["standard"])

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = abs(x)

    return queue
