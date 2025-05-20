def moveObjectWithBraking(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
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

    if nodes["objects"][str(id)]["inputs"]["slidingStep"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["slidingStep"]["value"]["value"] is not None:
        slidingStep = float(nodes["objects"][str(id)]["inputs"]["slidingStep"]["value"]["value"])

    else:
        slidingStep = float(nodes["objects"][str(id)]["inputs"]["slidingStep"]["standard"])

    program.objects.getById(int(ids)).moveByAngle(angle, power, slidingStep, specifical=id)

    return queue
