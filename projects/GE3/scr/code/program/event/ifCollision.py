def ifCollision(program, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["group"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"] is not None:
        group = nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"]

    else:
        group = nodes["objects"][str(id)]["inputs"]["group"]["standard"]

    if nodes["objects"][str(id)]["inputs"]["append"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["append"]["value"]["value"] is not None:
        append = (nodes["objects"][str(id)]["inputs"]["append"]["value"]["value"] == True)

    else:
        append = (nodes["objects"][str(id)]["inputs"]["append"]["standard"] == True)

    answer = program.objects.getById(ids).collisionGetID(0, 0, append, group)

    if answer[0]:
        for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
            queue.append(name["id"])

        for ids, connector in nodes["objects"][str(id)]["outputs"]["id_in_group"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer[1].id

    else:
        for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
            queue.append(name["id"])

    return queue
