def ifElementInList(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

    else:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["element"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"] is not None:
        element = str(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"])

    else:
        element = str(nodes["objects"][str(id)]["inputs"]["element"]["standard"])

    find = False

    for index, elem in enumerate(list_):
        if str(elem) == str(element):
            find = True

            break

    if find:
        for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
            queue.append(name["id"])

    else:
        for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
            queue.append(name["id"])

    return queue
