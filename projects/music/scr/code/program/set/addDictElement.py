from engine.special.exception import EngineError


def addDictElement(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    try:
        if nodes["objects"][str(id)]["inputs"]["dict"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"] is not None:
            dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"])

        else:
            dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["standard"])

    except BaseException:
        raise EngineError("type of dict is not currect")

    if nodes["objects"][str(id)]["inputs"]["key"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"] is not None:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"])

    else:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["element"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"] is not None:
        element = eval(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]) if type(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]) == str else nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]

    else:
        element = eval(nodes["objects"][str(id)]["inputs"]["element"]["standard"]) if type(nodes["objects"][str(id)]["inputs"]["element"]["standard"]) == str else nodes["objects"][str(id)]["inputs"]["element"]["standard"]

    dict_[key] = element

    for ids, connector in nodes["objects"][str(id)]["outputs"]["dict"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = dict_

    return queue
