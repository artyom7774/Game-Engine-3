def functionEvent(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["params"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["params"]["value"]["value"] is not None:
        params = list(nodes["objects"][str(id)]["inputs"]["params"]["value"]["value"])

    else:
        params = list(nodes["objects"][str(id)]["inputs"]["params"]["standard"])

    for ids, connector in nodes["objects"][str(id)]["outputs"]["params"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = params

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    return queue
