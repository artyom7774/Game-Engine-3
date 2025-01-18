def getKeyOfElement(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["dict"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"] is not None:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"])

    else:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["element"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"] is not None:
        element = str(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"])

    else:
        element = str(nodes["objects"][str(id)]["inputs"]["element"]["standard"])

    answer = "NULL"

    for key, value in dict_.items():
        if str(value) == str(element):
            answer = key

            break

    for ids, connector in nodes["objects"][str(id)]["outputs"]["key"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
