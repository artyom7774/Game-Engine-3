from engine.special.exception import EngineError


def ifCollision(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["group"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"] is not None:
        groupList = nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"]

    else:
        groupList = nodes["objects"][str(id)]["inputs"]["group"]["standard"]

    if nodes["objects"][str(id)]["inputs"]["append"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["append"]["value"]["value"] is not None:
        append = (nodes["objects"][str(id)]["inputs"]["append"]["value"]["value"] == True)

    else:
        append = (nodes["objects"][str(id)]["inputs"]["append"]["standard"] == True)

    obj = program.objects.getById(ids)

    if obj is None:
        EngineError(f"not found object with id = {ids}")

    for group in groupList.split(", "):
        answer = obj.collisionGetID(0, 0, append, group) if obj is not None else [False, -1]

        if answer[0]:
            for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
                queue.append(name["id"])

            for ids, connector in nodes["objects"][str(id)]["outputs"]["id_in_group"]["value"].items():
                nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer[1].id

            break

        else:
            for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
                queue.append(name["id"])

            for ids, connector in nodes["objects"][str(id)]["outputs"]["id_in_group"]["value"].items():
                nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = -1

    return queue
