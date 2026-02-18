def len_(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["element"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"] is not None:
        if type(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]) == str:
            element = eval(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"])

        else:
            element = eval(str(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]))

    else:
        if type(nodes["objects"][str(id)]["inputs"]["element"]["value"]["value"]) == str:
            element = eval(nodes["objects"][str(id)]["inputs"]["element"]["standard"])

        else:
            element = eval(str(nodes["objects"][str(id)]["inputs"]["element"]["standard"]))

    answer = len(element) if type(element) in (list, tuple, dict) else 1

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
