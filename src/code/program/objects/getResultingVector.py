from engine.special.exception import EngineError


def getResultingVector(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    obj = program.objects.getById(ids)

    if obj is None:
        raise EngineError(f"not found object with id = {ids}")

    pos = obj.getVectorsPower()

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.x

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["y"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.y

    return queue
