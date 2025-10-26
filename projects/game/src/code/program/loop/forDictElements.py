from engine.special.exception import EngineError


def forDictElements(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    timer = []
    queue = []

    try:
        if nodes["objects"][str(id)]["inputs"]["dict"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"] is not None:
            dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"])

        else:
            dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["standard"])

    except BaseException:
        raise EngineError("type of dict is not currect")

    compiler.loopBreaking[str(id)] = False

    for key, value in dict_.items():
        for ids, connector in nodes["objects"][str(id)]["outputs"]["key"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = key

        for ids, connector in nodes["objects"][str(id)]["outputs"]["element"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = value

        for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            compiler.queue(name["id"])

        if compiler.loopBreaking.get(str(id), False):
            break

    else:
        for name in nodes["objects"][str(id)]["outputs"]["after"]["value"].values():
            queue.append(name["id"])

    return {"queue": queue, "timer": timer}
