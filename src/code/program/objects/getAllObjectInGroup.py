def getAllObjectInGroup(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["group"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"] is not None:
        group = str(nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"])

    else:
        group = str(nodes["objects"][str(id)]["inputs"]["group"]["standard"])

    """
    for ids, connector in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.x
    """

    group = program.objects.getByGroup(group)

    objects = [obj.id for obj in group] if group is not None else []

    for ids, connector in nodes["objects"][str(id)]["outputs"]["objects"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = objects

    return queue
