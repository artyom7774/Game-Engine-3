from engine.special.exception import EngineError


def setVar(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["global"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["global"]["value"]["value"] is not None:
        gl = nodes["objects"][str(id)]["inputs"]["global"]["value"]["value"]

    else:
        gl = nodes["objects"][str(id)]["inputs"]["global"]["standard"]

    try:
        if nodes["objects"][str(id)]["inputs"]["value"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"] is not None:
            value = eval(nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"])

        else:
            value = eval(nodes["objects"][str(id)]["inputs"]["value"]["standard"])

    except BaseException:
        if nodes["objects"][str(id)]["inputs"]["value"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"] is not None:
            value = nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"]

        else:
            value = nodes["objects"][str(id)]["inputs"]["value"]["standard"]

    if gl:
        type = variables["globals"][name]["type"]

    else:
        type = variables["locals"][path][name]["type"]

    if type == "number":
        value = float(value) if float(value) - int(value) != 0 else int(value)

    if gl:
        if name not in variables["globals"]:
            raise EngineError(f"not found global variable with name = {name}")

        variables["globals"][name]["value"] = value

    else:
        if name not in variables["locals"][path]:
            raise EngineError(f"not found local variable with name = {name}")

        variables["locals"][path][name]["value"] = value

    return queue
