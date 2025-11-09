from engine.special.exception import EngineError


def getVar(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
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

    if gl:
        if name not in variables["globals"]:
            raise EngineError(f"not found global variable with name = {name}")

        answer = variables["globals"][name]["value"]

    else:
        if name not in variables["locals"][path]:
            raise EngineError(f"not found local variable with name = {name}")

        answer = variables["locals"][path][name]["value"]

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
