def removeObject(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        id = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        id = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    program.objects.removeById(id)

    return queue
