from engine.special.exception import EngineError


def removeByKey(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["dict"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"] is not None:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"])

    else:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["key"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"] is not None:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"])

    else:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["standard"])

    if key in dict_:
        dict_.pop(key)

    else:
        raise EngineError(f"not found key = {key} in dict = {dict_}")

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["dict"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = dict_

    return queue
