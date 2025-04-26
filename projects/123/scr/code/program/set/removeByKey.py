def removeByKey(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

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

    for ids, connector in nodes["objects"][str(id)]["outputs"]["dict"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = dict_

    return queue
