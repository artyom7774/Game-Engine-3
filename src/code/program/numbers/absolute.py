import math


def absolute(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["number"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"] is not None:
        x = float(nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"])

    else:
        x = float(nodes["objects"][str(id)]["inputs"]["number"]["standard"])

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = int(abs(x)) if math.trunc(x) == math.ceil(x) else abs(x)

    return queue
