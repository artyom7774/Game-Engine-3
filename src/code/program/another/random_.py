import random


def random_(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["a"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"] is not None:
        a = int(nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"])

    else:
        a = int(nodes["objects"][str(id)]["inputs"]["a"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["b"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"] is not None:
        b = int(nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"])

    else:
        b = int(nodes["objects"][str(id)]["inputs"]["b"]["standard"])

    answer = a if a == b else (random.randint(a, b) if a < b else random.randint(b, a))

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
