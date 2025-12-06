from engine.special.exception import EngineError


def addListElement(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    try:
        if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
            list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

        else:
            list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    except BaseException:
        raise EngineError("type of list is not currect")

    if nodes["objects"][str(id)]["inputs"]["element"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"] is not None:
        if type(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]) == str:
            element = eval(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"])

        else:
            element = eval(str(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]))

    else:
        if type(nodes["objects"][str(id)]["inputs"]["element"]["standard"]) == str:
            element = eval(nodes["objects"][str(id)]["inputs"]["element"]["standard"])

        else:
            element = eval(str(nodes["objects"][str(id)]["inputs"]["element"]["standard"]))

    list_.append(element)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["list"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = list_

    return queue
