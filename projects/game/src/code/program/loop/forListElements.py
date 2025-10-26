from engine.special.exception import EngineError


def forListElements(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    timer = []
    queue = []

    try:
        if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
            list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

        else:
            list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    except BaseException:
        raise EngineError("type of list is not currect")

    compiler.loopBreaking[str(id)] = False

    for i, element in enumerate(list_):
        for ids, connector in nodes["objects"][str(id)]["outputs"]["index"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = i

        for ids, connector in nodes["objects"][str(id)]["outputs"]["element"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = element

        for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            compiler.queue(name["id"])

        if compiler.loopBreaking.get(str(id), False):
            break

    else:
        for name in nodes["objects"][str(id)]["outputs"]["after"]["value"].values():
            queue.append(name["id"])

    return {"queue": queue, "timer": timer}
