def setVar(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
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

    if nodes["objects"][str(id)]["inputs"]["value"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"] is not None:
        value = nodes["objects"][str(id)]["inputs"]["value"]["value"]["value"]

    else:
        value = nodes["objects"][str(id)]["inputs"]["value"]["standard"]

    if gl:
        type = variables["globals"][name]["type"]

    else:
        type = variables["locals"][path][name]["type"]

    if type == "number":
        value = float(value)

    if gl:
        variables["globals"][name]["value"] = value

    else:
        variables["locals"][path][name]["value"] = value

    return queue
