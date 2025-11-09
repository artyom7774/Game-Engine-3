from engine.special.exception import EngineError

def getByIndex(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
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

    if nodes["objects"][str(id)]["inputs"]["index"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["index"]["value"]["value"] is not None:
        index = int(nodes["objects"][str(id)]["inputs"]["index"]["value"]["value"])

    else:
        index = int(nodes["objects"][str(id)]["inputs"]["index"]["standard"])

    try:
        answer = list_[index]

    except IndexError:
        raise EngineError(f"index {index} not in list {list_}")

    for ids, connector in nodes["objects"][str(id)]["outputs"]["element"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
