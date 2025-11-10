from engine.special.exception import EngineError


def callFunction(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["params"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["params"]["value"]["value"] is not None:
        params = list(nodes["objects"][str(id)]["inputs"]["params"]["value"]["value"])

    else:
        params = list(nodes["objects"][str(id)]["inputs"]["params"]["standard"])

    functions = compiler.functionsByName(name)

    if functions is None:
        raise EngineError(f"not found function with name = {name}")

    for ids in functions:
        nodes["objects"][str(ids)]["inputs"]["params"]["standard"] = params

        queue.append(ids)

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    return queue
