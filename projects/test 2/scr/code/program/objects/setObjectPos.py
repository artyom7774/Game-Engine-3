def setObjectPos(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = str(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = str(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["x"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"] is not None:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"])

    else:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["y"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"] is not None:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"])

    else:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["standard"])

    obj = program.objects.getById(int(ids))

    obj.pos.x = x
    obj.pos.y = y

    return queue
