def moveObject(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = str(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = str(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["angle"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["angle"]["value"]["value"] is not None:
        angle = float(nodes["objects"][str(id)]["inputs"]["angle"]["value"]["value"])

    else:
        angle = float(nodes["objects"][str(id)]["inputs"]["angle"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["power"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["power"]["value"]["value"] is not None:
        power = float(nodes["objects"][str(id)]["inputs"]["power"]["value"]["value"])

    else:
        power = float(nodes["objects"][str(id)]["inputs"]["power"]["standard"])

    obj = program.objects.getById(int(ids))

    obj.moveByAngle(angle, power, specifical=id)

    return queue
