def getIndexOfElement(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

    else:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["element"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"] is not None:
        element = str(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"])

    else:
        element = str(nodes["objects"][str(id)]["inputs"]["element"]["standard"])

    answer = -1

    for index, elem in enumerate(list_):
        if str(elem) == str(element):
            answer = index

            break

    for ids, connector in nodes["objects"][str(id)]["outputs"]["index"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
