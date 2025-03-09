def runAnimation(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["animation"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["animation"]["value"]["value"] is not None:
        animation = str(nodes["objects"][str(id)]["inputs"]["animation"]["value"]["value"])

    else:
        animation = str(nodes["objects"][str(id)]["inputs"]["animation"]["standard"])

    program.objects.getById(ids).animator.runAnimation(animation)

    return queue
