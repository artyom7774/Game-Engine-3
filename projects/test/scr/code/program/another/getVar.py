def getVar(program, path: str, nodes: dict, id: int, variables: dict) -> dict:
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
        answer = variables["globals"][name]["value"]

    else:
        answer = variables["locals"][path][name]["value"]

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
