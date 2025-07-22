from engine.special.exception import EngineError


def getIndexOfElement(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
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

    answer = None

    for index, elem in enumerate(list_):
        if str(elem) == str(element):
            answer = index

            break

    if answer is None:
        raise EngineError(f"not found element = {element} in list = {list_}")

    for ids, connector in nodes["objects"][str(id)]["outputs"]["index"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
