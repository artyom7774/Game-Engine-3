def mirrorAnimation(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["horizontal"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["horizontal"]["value"]["value"] is not None:
        horizontal = bool(nodes["objects"][str(id)]["inputs"]["horizontal"]["value"]["value"])

    else:
        horizontal = bool(nodes["objects"][str(id)]["inputs"]["horizontal"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["vertical"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["vertical"]["value"]["value"] is not None:
        vertical = bool(nodes["objects"][str(id)]["inputs"]["vertical"]["value"]["value"])

    else:
        vertical = bool(nodes["objects"][str(id)]["inputs"]["vertical"]["standard"])

    program.objects.getById(ids).animator.flipAnimation(horizontal, vertical)

    return queue
