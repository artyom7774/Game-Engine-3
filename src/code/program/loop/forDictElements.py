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
        for ids, connectors in nodes["objects"][str(id)]["outputs"]["key"]["value"].items():
            for connector in connectors:
                nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = key

        for ids, connectors in nodes["objects"][str(id)]["outputs"]["element"]["value"].items():
            for connector in connectors:
                nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = value

        for element in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            queue.extend([item["id"] for item in element])

        if compiler.loopBreaking.get(str(id), False):
            break

    else:
        for element in nodes["objects"][str(id)]["outputs"]["after"]["value"].values():
            queue.extend([item["id"] for item in element])

    return {"queue": queue, "timer": timer}
