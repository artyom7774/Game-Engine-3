def ifKeyInDict(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["dict"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"] is not None:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"])

    else:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["key"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"] is not None:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"])

    else:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["standard"])

    if key in dict_:
        for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
            queue.append(name["id"])

    else:
        for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
            queue.append(name["id"])

    return queue
