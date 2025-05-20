def getByKey(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
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

    answer = dict_[key]

    for ids, connector in nodes["objects"][str(id)]["outputs"]["element"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
