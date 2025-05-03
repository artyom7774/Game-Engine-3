OBJECT_PARAMETERS = ["hitbox", "group", "mass", "layer", "invisible", "speed", "gravity", "jumpPower", "slidingStep", "message", "fontSize", "fontColor", "alignment"]


def getObjectParameter(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        operation = int(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        operation = int(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    answer = program.objects.getById(ids).getParameter(OBJECT_PARAMETERS[operation])

    for ids, connector in nodes["objects"][str(id)]["outputs"]["value"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
