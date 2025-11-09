import math


def sqrt(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["number"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"] is not None:
        number = float(nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"])

    else:
        number = float(nodes["objects"][str(id)]["inputs"]["number"]["standard"])

    answer = math.sqrt(number)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
