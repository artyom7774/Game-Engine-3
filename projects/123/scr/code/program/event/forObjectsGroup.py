def forObjectsGroup(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["group"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"] is not None:
        group = str(nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"])

    else:
        group = str(nodes["objects"][str(id)]["inputs"]["group"]["standard"])

    """
    for ids, connector in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.x
    """

    objects = program.objects.getByGroup(group)
    n = len(objects)

    for i, obj in enumerate(objects):
        for ids, connector in nodes["objects"][str(id)]["outputs"]["id"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = obj.id

        for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            compiler.queue(name["id"])

    return queue
