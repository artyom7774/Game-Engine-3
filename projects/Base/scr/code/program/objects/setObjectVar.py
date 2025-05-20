def setObjectVar(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"]

    else:
        ids = nodes["objects"][str(id)]["inputs"]["id"]["standard"]

    if nodes["objects"][str(id)]["inputs"]["value"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"] is not None:
        value = nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"]

    else:
        value = nodes["objects"][str(id)]["inputs"]["value"]["standard"]

    type = variables["objects"][program.scene][program.objectNameByID[program.scene][str(ids)]][name]["type"]

    if type == "number":
        value = float(value)

    variables["objects"][program.scene][program.objectNameByID[program.scene][str(ids)]][name]["value"] = value

    return queue
