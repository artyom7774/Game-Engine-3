from engine.special.exception import EngineError


def forObjectsGroup(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["group"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"] is not None:
        group = str(nodes["objects"][str(id)]["inputs"]["group"]["value"]["value"])

    else:
        group = str(nodes["objects"][str(id)]["inputs"]["group"]["standard"])

    """
    for ids, connector in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.x
    """

    objects = program.objects.getByGroup(group)

    if objects is None:
        raise EngineError(f"group of objects {group} newer existed")

    n = len(objects)

    compiler.loopBreaking[str(id)] = False

    for i, obj in enumerate(objects):
        for ids, connector in nodes["objects"][str(id)]["outputs"]["id"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = obj.id

        for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            compiler.queue(name["id"])

        if compiler.loopBreaking.get(str(id), False):
            break

    else:
        for name in nodes["objects"][str(id)]["outputs"]["after"]["value"].values():
            queue.append(name["id"])

    return queue
