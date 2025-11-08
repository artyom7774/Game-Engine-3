from engine.special.exception import EngineError


def getObjectIDByName(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if name.endswith(".objc"):
        name = name[:-5]

    answer = program.objectIDByName[program.scene][name] if name in program.objectIDByName[program.scene] else None

    if answer is None:
        raise EngineError(f"not found object with name = {name}")

    for ids, connector in nodes["objects"][str(id)]["outputs"]["id"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
